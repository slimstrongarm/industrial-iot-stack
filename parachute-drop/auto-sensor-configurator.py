#!/usr/bin/env python3
"""
🪂 PARACHUTE DROP - Auto Sensor Configurator
Automatically detects connected Phidget sensors and generates dashboards
"""

import json
import time
import asyncio
from datetime import datetime
from pathlib import Path

# Phidget libraries (would be installed on Pi)
try:
    from Phidget22.Phidget import *
    from Phidget22.Devices.VoltageInput import *
    from Phidget22.Devices.TemperatureSensor import *
    from Phidget22.Devices.CurrentInput import *
    from Phidget22.Devices.DigitalInput import *
    PHIDGETS_AVAILABLE = True
except ImportError:
    print("⚠️ Phidget22 not available - using simulation mode")
    PHIDGETS_AVAILABLE = False

class AutoSensorConfigurator:
    def __init__(self):
        self.detected_sensors = {}
        self.sensor_configs = {}
        self.dashboard_widgets = []
        self.mqtt_topics = []
        
        # Load sensor library
        self.load_sensor_library()
        
    def load_sensor_library(self):
        """Load sensor configurations from library"""
        try:
            with open('/home/pi/parachute_drop/sensor-library.json', 'r') as f:
                self.sensor_library = json.load(f)
        except FileNotFoundError:
            # Fallback sensor library
            self.sensor_library = {
                "parachute_drop_sensor_library": {
                    "port_configurations": {
                        "temperature_sensors": [
                            {
                                "name": "RTD_PT100",
                                "interface": "phidget_temperature",
                                "range": "-50 to 200°C",
                                "dashboard_widget": "gauge"
                            }
                        ],
                        "current_sensors": [
                            {
                                "name": "AC_Current_30A",
                                "interface": "phidget_current",
                                "range": "0-30A AC",
                                "dashboard_widget": "gauge"
                            }
                        ]
                    }
                }
            }
    
    def detect_connected_sensors(self):
        """Detect all connected Phidget sensors"""
        print("🔍 Detecting connected Phidget sensors...")
        
        if PHIDGETS_AVAILABLE:
            self.detect_real_sensors()
        else:
            self.simulate_sensor_detection()
            
        return self.detected_sensors
    
    def detect_real_sensors(self):
        """Detect actual Phidget sensors"""
        detected_count = 0
        
        # Scan for temperature sensors
        for port in range(6):  # 6-port hub
            try:
                temp_sensor = TemperatureSensor()
                temp_sensor.setHubPort(port)
                temp_sensor.setIsHubPortDevice(False)
                temp_sensor.openWaitForAttachment(1000)
                
                self.detected_sensors[port] = {
                    "type": "temperature",
                    "interface": "phidget_temperature",
                    "serial": temp_sensor.getDeviceSerialNumber(),
                    "name": f"Temperature_Sensor_{port}",
                    "unit": "°C",
                    "widget": "gauge"
                }
                
                temp_sensor.close()
                detected_count += 1
                print(f"✅ Port {port}: Temperature sensor detected")
                
            except PhidgetException:
                # Try current sensor
                try:
                    current_sensor = CurrentInput()
                    current_sensor.setHubPort(port)
                    current_sensor.openWaitForAttachment(1000)
                    
                    self.detected_sensors[port] = {
                        "type": "current",
                        "interface": "phidget_current", 
                        "serial": current_sensor.getDeviceSerialNumber(),
                        "name": f"Current_Sensor_{port}",
                        "unit": "A",
                        "widget": "gauge"
                    }
                    
                    current_sensor.close()
                    detected_count += 1
                    print(f"✅ Port {port}: Current sensor detected")
                    
                except PhidgetException:
                    # Try digital input
                    try:
                        digital_input = DigitalInput()
                        digital_input.setHubPort(port)
                        digital_input.openWaitForAttachment(1000)
                        
                        self.detected_sensors[port] = {
                            "type": "digital",
                            "interface": "phidget_digital_input",
                            "serial": digital_input.getDeviceSerialNumber(),
                            "name": f"Digital_Input_{port}",
                            "unit": "",
                            "widget": "led"
                        }
                        
                        digital_input.close()
                        detected_count += 1
                        print(f"✅ Port {port}: Digital input detected")
                        
                    except PhidgetException:
                        pass
        
        print(f"🎯 Detected {detected_count} sensors")
    
    def simulate_sensor_detection(self):
        """Simulate sensor detection for development"""
        print("🎭 Simulation mode - creating mock sensors")
        
        mock_sensors = [
            {"port": 0, "type": "temperature", "name": "HLT_Temperature", "unit": "°C", "widget": "gauge"},
            {"port": 1, "type": "current", "name": "Pump_1_Current", "unit": "A", "widget": "gauge"},
            {"port": 2, "type": "digital", "name": "Motor_Contactor", "unit": "", "widget": "led"},
            {"port": 3, "type": "pressure", "name": "System_Pressure", "unit": "PSI", "widget": "gauge"},
        ]
        
        for sensor in mock_sensors:
            self.detected_sensors[sensor["port"]] = {
                "type": sensor["type"],
                "interface": f"phidget_{sensor['type']}",
                "serial": f"SIM{sensor['port']:03d}",
                "name": sensor["name"],
                "unit": sensor["unit"],
                "widget": sensor["widget"]
            }
    
    def generate_node_red_dashboard(self):
        """Generate Node-RED dashboard configuration"""
        print("📊 Generating Node-RED dashboard...")
        
        dashboard_flows = []
        
        # Create tab
        tab_node = {
            "id": "parachute_tab",
            "type": "ui_tab",
            "name": "🪂 Parachute Drop Monitor",
            "icon": "dashboard",
            "order": 1
        }
        dashboard_flows.append(tab_node)
        
        # Create group
        group_node = {
            "id": "sensors_group",
            "type": "ui_group", 
            "name": "Live Sensors",
            "tab": "parachute_tab",
            "order": 1,
            "disp": True,
            "width": "12",
            "collapse": False
        }
        dashboard_flows.append(group_node)
        
        # Create sensor nodes
        y_position = 100
        for port, sensor in self.detected_sensors.items():
            
            # Input node (sensor reading)
            input_node = {
                "id": f"sensor_input_{port}",
                "type": f"phidget22-{sensor['interface'].split('_')[1]}",
                "name": sensor['name'],
                "phidgetServer": "phidget_hub",
                "channel": str(port),
                "x": 100,
                "y": y_position,
                "wires": [[f"sensor_process_{port}", f"mqtt_out_{port}"]]
            }
            
            # Processing node
            process_node = {
                "id": f"sensor_process_{port}",
                "type": "function",
                "name": f"Process {sensor['name']}",
                "func": self.generate_sensor_processing(sensor),
                "outputs": 1,
                "x": 300,
                "y": y_position,
                "wires": [[f"dashboard_{port}"]]
            }
            
            # Dashboard widget
            widget_node = self.create_dashboard_widget(port, sensor, y_position)
            
            # MQTT output
            mqtt_node = {
                "id": f"mqtt_out_{port}",
                "type": "mqtt out",
                "name": f"Publish {sensor['name']}",
                "topic": f"parachute/sensors/{sensor['name'].lower().replace(' ', '_')}",
                "qos": "1",
                "retain": "true",
                "broker": "mqtt_broker",
                "x": 300,
                "y": y_position + 50,
                "wires": []
            }
            
            dashboard_flows.extend([input_node, process_node, widget_node, mqtt_node])
            y_position += 100
        
        return dashboard_flows
    
    def create_dashboard_widget(self, port, sensor, y_pos):
        """Create appropriate dashboard widget for sensor type"""
        
        base_widget = {
            "id": f"dashboard_{port}",
            "group": "sensors_group",
            "order": port + 1,
            "x": 500,
            "y": y_pos,
            "wires": []
        }
        
        if sensor['widget'] == 'gauge':
            widget = {
                **base_widget,
                "type": "ui_gauge",
                "name": sensor['name'],
                "width": "6",
                "height": "4",
                "gtype": "gage",
                "title": sensor['name'],
                "label": sensor['unit'],
                "format": "{{value | number:1}}",
                "min": self.get_sensor_min(sensor['type']),
                "max": self.get_sensor_max(sensor['type']),
                "colors": ["#00b500", "#e6e600", "#ca3838"],
                "seg1": self.get_sensor_min(sensor['type']) + (self.get_sensor_max(sensor['type']) - self.get_sensor_min(sensor['type'])) * 0.3,
                "seg2": self.get_sensor_min(sensor['type']) + (self.get_sensor_max(sensor['type']) - self.get_sensor_min(sensor['type'])) * 0.7
            }
        elif sensor['widget'] == 'led':
            widget = {
                **base_widget,
                "type": "ui_led",
                "name": sensor['name'],
                "width": "3",
                "height": "1",
                "label": sensor['name'],
                "labelPlacement": "left",
                "colorForValue": [
                    {"color": "#ff0000", "value": "false", "valueType": "bool"},
                    {"color": "#00ff00", "value": "true", "valueType": "bool"}
                ]
            }
        else:
            widget = {
                **base_widget,
                "type": "ui_text",
                "name": sensor['name'],
                "width": "4",
                "height": "1",
                "label": sensor['name'],
                "format": "{{msg.payload}}"
            }
        
        return widget
    
    def get_sensor_min(self, sensor_type):
        """Get minimum value for sensor type"""
        ranges = {
            'temperature': -20,
            'current': 0,
            'pressure': 0,
            'digital': 0
        }
        return ranges.get(sensor_type, 0)
    
    def get_sensor_max(self, sensor_type):
        """Get maximum value for sensor type"""
        ranges = {
            'temperature': 150,
            'current': 30,
            'pressure': 200,
            'digital': 1
        }
        return ranges.get(sensor_type, 100)
    
    def generate_sensor_processing(self, sensor):
        """Generate processing function for sensor data"""
        
        if sensor['type'] == 'temperature':
            return """
// Temperature sensor processing
const temp = msg.payload;
const processed = {
    value: Math.round(temp * 10) / 10,
    unit: '°C',
    timestamp: new Date().toISOString(),
    status: temp > 80 ? 'high' : temp < 10 ? 'low' : 'normal'
};

if (processed.status !== 'normal') {
    node.warn(`Temperature ${processed.status}: ${processed.value}°C`);
}

msg.payload = processed.value;
msg.temp_data = processed;
return msg;
"""
        
        elif sensor['type'] == 'current':
            return """
// Current sensor processing  
const current = msg.payload;
const processed = {
    value: Math.round(current * 100) / 100,
    unit: 'A',
    timestamp: new Date().toISOString(),
    status: current > 25 ? 'overload' : current < 0.5 ? 'no_load' : 'running'
};

if (processed.status === 'overload') {
    node.error(`Motor overload detected: ${processed.value}A`);
}

msg.payload = processed.value;
msg.current_data = processed;
return msg;
"""
        
        elif sensor['type'] == 'digital':
            return """
// Digital input processing
const state = msg.payload;
const processed = {
    value: state,
    state: state ? 'ON' : 'OFF',
    timestamp: new Date().toISOString()
};

msg.payload = state;
msg.digital_data = processed;
return msg;
"""
        
        else:
            return """
// Generic sensor processing
msg.payload = Math.round(msg.payload * 100) / 100;
msg.timestamp = new Date().toISOString();
return msg;
"""
    
    def create_alert_system(self):
        """Create alert system for sensor thresholds"""
        
        alert_flows = []
        
        # Alert function node
        alert_node = {
            "id": "alert_processor",
            "type": "function", 
            "name": "Alert Processor",
            "func": """
// Process sensor alerts
const alerts = flow.get('active_alerts') || [];
const thresholds = {
    temperature: {high: 85, low: 5},
    current: {high: 25, low: 0.1},
    pressure: {high: 180, low: 10}
};

if (msg.temp_data) {
    const temp = msg.temp_data.value;
    if (temp > thresholds.temperature.high || temp < thresholds.temperature.low) {
        const alert = {
            sensor: 'Temperature',
            value: temp,
            threshold: temp > thresholds.temperature.high ? 'HIGH' : 'LOW',
            timestamp: new Date().toISOString(),
            severity: 'WARNING'
        };
        
        // Send to Discord/MQTT
        node.send([{payload: alert}, null]);
        return null;
    }
}

if (msg.current_data) {
    const current = msg.current_data.value;
    if (current > thresholds.current.high) {
        const alert = {
            sensor: 'Motor Current',
            value: current,
            threshold: 'OVERLOAD',
            timestamp: new Date().toISOString(),
            severity: 'CRITICAL'
        };
        
        node.send([{payload: alert}, null]);
        return null;
    }
}

// Normal data flow
return [null, msg];
""",
            "outputs": 2,
            "x": 400,
            "y": 500,
            "wires": [["alert_output"], ["normal_flow"]]
        }
        
        # Alert output (MQTT)
        alert_output = {
            "id": "alert_output",
            "type": "mqtt out",
            "name": "Publish Alerts",
            "topic": "parachute/alerts",
            "qos": "2",
            "retain": "false", 
            "broker": "mqtt_broker",
            "x": 600,
            "y": 480,
            "wires": []
        }
        
        alert_flows.extend([alert_node, alert_output])
        return alert_flows
    
    def generate_complete_configuration(self):
        """Generate complete sensor configuration"""
        print("⚙️ Generating complete configuration...")
        
        # Detect sensors
        self.detect_connected_sensors()
        
        # Generate configurations
        dashboard_flows = self.generate_node_red_dashboard()
        alert_flows = self.create_alert_system()
        
        # Combine all flows
        complete_config = {
            "parachute_drop_config": {
                "timestamp": datetime.now().isoformat(),
                "sensors_detected": len(self.detected_sensors),
                "sensor_details": self.detected_sensors,
                "node_red_flows": dashboard_flows + alert_flows,
                "mqtt_topics": [
                    f"parachute/sensors/{sensor['name'].lower().replace(' ', '_')}"
                    for sensor in self.detected_sensors.values()
                ],
                "dashboard_url": "http://localhost:1880/ui"
            }
        }
        
        return complete_config
    
    def save_configuration(self, config):
        """Save configuration to files"""
        output_dir = Path("/home/pi/parachute_drop")
        output_dir.mkdir(exist_ok=True)
        
        # Save complete config
        with open(output_dir / "sensor_configuration.json", "w") as f:
            json.dump(config, f, indent=2)
        
        # Save Node-RED flows separately
        flows = config["parachute_drop_config"]["node_red_flows"]
        with open(output_dir / "auto_dashboard_flows.json", "w") as f:
            json.dump(flows, f, indent=2)
        
        print(f"💾 Configuration saved to {output_dir}")
        return output_dir

def main():
    """Main execution"""
    print("🪂 PARACHUTE DROP - Auto Sensor Configurator")
    print("===========================================")
    
    configurator = AutoSensorConfigurator()
    
    # Generate complete configuration
    config = configurator.generate_complete_configuration()
    
    # Save configuration
    output_dir = configurator.save_configuration(config)
    
    # Summary
    sensors_detected = config["parachute_drop_config"]["sensors_detected"]
    print(f"\n✅ AUTO-CONFIGURATION COMPLETE!")
    print(f"📊 Summary:")
    print(f"   • {sensors_detected} sensors auto-detected")
    print(f"   • Dashboard with {sensors_detected} widgets generated")
    print(f"   • Alert system configured")
    print(f"   • MQTT topics: {len(config['parachute_drop_config']['mqtt_topics'])}")
    print(f"   • Configuration saved to: {output_dir}")
    print(f"\n🎯 Next Steps:")
    print(f"   1. Import flows to Node-RED: http://localhost:1880")
    print(f"   2. Access dashboard: http://localhost:1880/ui") 
    print(f"   3. Monitor MQTT: localhost:1883")
    print(f"   4. Deploy sensors and watch real-time data!")
    
    return config

if __name__ == "__main__":
    main()