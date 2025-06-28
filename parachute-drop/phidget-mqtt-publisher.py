#!/usr/bin/env python3
"""
Phidget to MQTT Publisher with UNS Hierarchy
Reads temperature/humidity from Phidget sensors and publishes to MQTT broker
Designed for brewery monitoring with 7" touchscreen display
"""

import sys
import time
import json
import logging
from datetime import datetime
from Phidget22.Phidget import *
from Phidget22.Devices.HumiditySensor import *
from Phidget22.Devices.TemperatureSensor import *
from Phidget22.Devices.VoltageRatioInput import *
import paho.mqtt.client as mqtt

# Configuration
MQTT_BROKER = "localhost"  # Change to your server IP
MQTT_PORT = 1883
MQTT_KEEPALIVE = 60

# UNS Hierarchy for brewery
# Format: Enterprise/Site/Area/Line/Cell/Tag
UNS_ENTERPRISE = "Brewery"
UNS_SITE = "Main"
UNS_AREA = "Fermentation"  # Change based on deployment location
UNS_LINE = "Tank1"         # Change based on specific equipment

# Sensor configuration
SENSOR_CONFIG = {
    "hub_port": 0,
    "temperature_unit": "C",  # C or F
    "update_interval": 1.0,   # seconds
    "alarm_thresholds": {
        "temperature": {"min": 15.0, "max": 25.0},  # Celsius
        "humidity": {"min": 30.0, "max": 80.0}      # %RH
    }
}

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)-8s | %(message)s',
    handlers=[
        logging.FileHandler('/home/pi/phidget-mqtt.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class PhidgetMQTTPublisher:
    def __init__(self):
        self.mqtt_client = None
        self.humidity_sensor = None
        self.temperature_sensor = None
        self.connected = False
        self.sensor_data = {
            "temperature": None,
            "humidity": None,
            "timestamp": None
        }
        
    def setup_mqtt(self):
        """Initialize MQTT client with reconnection logic"""
        self.mqtt_client = mqtt.Client(client_id=f"phidget-pi-{os.getpid()}")
        self.mqtt_client.on_connect = self.on_mqtt_connect
        self.mqtt_client.on_disconnect = self.on_mqtt_disconnect
        
        # Enable reconnection
        self.mqtt_client.reconnect_delay_set(min_delay=1, max_delay=120)
        
        try:
            self.mqtt_client.connect(MQTT_BROKER, MQTT_PORT, MQTT_KEEPALIVE)
            self.mqtt_client.loop_start()
            logger.info(f"MQTT client connecting to {MQTT_BROKER}:{MQTT_PORT}")
        except Exception as e:
            logger.error(f"Failed to connect to MQTT broker: {e}")
            return False
        
        return True
    
    def on_mqtt_connect(self, client, userdata, flags, rc):
        """MQTT connection callback"""
        if rc == 0:
            logger.info("Connected to MQTT broker successfully")
            self.connected = True
            
            # Publish initial status
            status_topic = f"{UNS_ENTERPRISE}/{UNS_SITE}/Status/PhidgetPi"
            status_msg = {
                "status": "online",
                "timestamp": datetime.now().isoformat(),
                "version": "1.0"
            }
            client.publish(status_topic, json.dumps(status_msg), retain=True)
        else:
            logger.error(f"Failed to connect to MQTT broker, return code: {rc}")
    
    def on_mqtt_disconnect(self, client, userdata, rc):
        """MQTT disconnection callback"""
        self.connected = False
        if rc != 0:
            logger.warning(f"Unexpected MQTT disconnection, return code: {rc}")
    
    def setup_phidget_sensors(self):
        """Initialize Phidget sensors"""
        try:
            # Create sensor objects
            self.humidity_sensor = HumiditySensor()
            self.temperature_sensor = TemperatureSensor()
            
            # Set hub port
            self.humidity_sensor.setHubPort(SENSOR_CONFIG["hub_port"])
            self.temperature_sensor.setHubPort(SENSOR_CONFIG["hub_port"])
            
            # Set data interval (ms)
            interval_ms = int(SENSOR_CONFIG["update_interval"] * 1000)
            
            # Set event handlers
            self.humidity_sensor.setOnHumidityChangeHandler(self.on_humidity_change)
            self.temperature_sensor.setOnTemperatureChangeHandler(self.on_temperature_change)
            
            # Open sensors
            logger.info("Opening Phidget sensors...")
            self.humidity_sensor.openWaitForAttachment(5000)
            self.temperature_sensor.openWaitForAttachment(5000)
            
            # Set data interval after attachment
            self.humidity_sensor.setDataInterval(interval_ms)
            self.temperature_sensor.setDataInterval(interval_ms)
            
            logger.info(f"Phidget sensors connected on hub port {SENSOR_CONFIG['hub_port']}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize Phidget sensors: {e}")
            return False
    
    def on_temperature_change(self, sensor, temperature):
        """Temperature change event handler"""
        # Convert to Fahrenheit if configured
        if SENSOR_CONFIG["temperature_unit"] == "F":
            temperature = (temperature * 9/5) + 32
        
        self.sensor_data["temperature"] = round(temperature, 2)
        self.sensor_data["timestamp"] = datetime.now().isoformat()
        
        # Check alarm thresholds
        alarm_active = False
        thresholds = SENSOR_CONFIG["alarm_thresholds"]["temperature"]
        if temperature < thresholds["min"] or temperature > thresholds["max"]:
            alarm_active = True
            self.publish_alarm("temperature", temperature, thresholds)
        
        # Publish to MQTT
        self.publish_sensor_data("temperature", temperature, alarm_active)
        
        # Log to console for debugging
        logger.info(f"Temperature: {temperature:.2f}°{SENSOR_CONFIG['temperature_unit']}")
    
    def on_humidity_change(self, sensor, humidity):
        """Humidity change event handler"""
        self.sensor_data["humidity"] = round(humidity, 2)
        self.sensor_data["timestamp"] = datetime.now().isoformat()
        
        # Check alarm thresholds
        alarm_active = False
        thresholds = SENSOR_CONFIG["alarm_thresholds"]["humidity"]
        if humidity < thresholds["min"] or humidity > thresholds["max"]:
            alarm_active = True
            self.publish_alarm("humidity", humidity, thresholds)
        
        # Publish to MQTT
        self.publish_sensor_data("humidity", humidity, alarm_active)
        
        logger.info(f"Humidity: {humidity:.2f}%RH")
    
    def publish_sensor_data(self, sensor_type, value, alarm_active=False):
        """Publish sensor data using UNS hierarchy"""
        if not self.connected:
            logger.warning("MQTT not connected, queuing data...")
            return
        
        # Build UNS topic
        base_topic = f"{UNS_ENTERPRISE}/{UNS_SITE}/{UNS_AREA}/{UNS_LINE}"
        
        # Sensor-specific topic
        if sensor_type == "temperature":
            topic = f"{base_topic}/Temperature"
            unit = f"°{SENSOR_CONFIG['temperature_unit']}"
        else:
            topic = f"{base_topic}/Humidity"
            unit = "%RH"
        
        # Build payload with metadata
        payload = {
            "value": value,
            "unit": unit,
            "quality": "Good" if not alarm_active else "Bad",
            "timestamp": datetime.now().isoformat(),
            "alarm": alarm_active,
            "source": "phidget_pi"
        }
        
        # Publish with QoS 1 for reliability
        self.mqtt_client.publish(topic, json.dumps(payload), qos=1)
        
        # Also publish to a combined sensor topic for easy dashboard access
        combined_topic = f"{base_topic}/Environment"
        combined_payload = {
            "temperature": self.sensor_data.get("temperature"),
            "humidity": self.sensor_data.get("humidity"),
            "timestamp": self.sensor_data.get("timestamp"),
            "location": f"{UNS_AREA}/{UNS_LINE}"
        }
        self.mqtt_client.publish(combined_topic, json.dumps(combined_payload), qos=1)
    
    def publish_alarm(self, sensor_type, value, thresholds):
        """Publish alarm to MQTT"""
        alarm_topic = f"{UNS_ENTERPRISE}/{UNS_SITE}/Alarms/{UNS_AREA}/{UNS_LINE}/{sensor_type}"
        
        alarm_payload = {
            "sensor": sensor_type,
            "value": value,
            "min_threshold": thresholds["min"],
            "max_threshold": thresholds["max"],
            "severity": "warning",
            "message": f"{sensor_type} out of range: {value}",
            "timestamp": datetime.now().isoformat()
        }
        
        self.mqtt_client.publish(alarm_topic, json.dumps(alarm_payload), qos=1, retain=True)
        logger.warning(f"Alarm published: {sensor_type} = {value}")
    
    def run(self):
        """Main run loop"""
        logger.info("Starting Phidget MQTT Publisher...")
        
        # Setup MQTT
        if not self.setup_mqtt():
            logger.error("Failed to setup MQTT, exiting...")
            return
        
        # Wait for MQTT connection
        timeout = 10
        while not self.connected and timeout > 0:
            time.sleep(1)
            timeout -= 1
        
        if not self.connected:
            logger.error("MQTT connection timeout")
            return
        
        # Setup Phidget sensors
        if not self.setup_phidget_sensors():
            logger.error("Failed to setup Phidget sensors, exiting...")
            return
        
        logger.info("System running - press Ctrl+C to stop")
        
        try:
            # Keep running
            while True:
                time.sleep(10)
                
                # Publish heartbeat
                heartbeat_topic = f"{UNS_ENTERPRISE}/{UNS_SITE}/Heartbeat/PhidgetPi"
                heartbeat = {
                    "timestamp": datetime.now().isoformat(),
                    "uptime": time.time(),
                    "sensors_active": True
                }
                self.mqtt_client.publish(heartbeat_topic, json.dumps(heartbeat))
                
        except KeyboardInterrupt:
            logger.info("Shutting down...")
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean shutdown"""
        try:
            # Publish offline status
            if self.mqtt_client and self.connected:
                status_topic = f"{UNS_ENTERPRISE}/{UNS_SITE}/Status/PhidgetPi"
                status_msg = {
                    "status": "offline",
                    "timestamp": datetime.now().isoformat()
                }
                self.mqtt_client.publish(status_topic, json.dumps(status_msg), retain=True)
            
            # Close sensors
            if self.humidity_sensor:
                self.humidity_sensor.close()
            if self.temperature_sensor:
                self.temperature_sensor.close()
            
            # Disconnect MQTT
            if self.mqtt_client:
                self.mqtt_client.loop_stop()
                self.mqtt_client.disconnect()
            
            logger.info("Cleanup complete")
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")

if __name__ == "__main__":
    import os
    
    # Create log directory if needed
    os.makedirs("/home/pi", exist_ok=True)
    
    # Run the publisher
    publisher = PhidgetMQTTPublisher()
    publisher.run()