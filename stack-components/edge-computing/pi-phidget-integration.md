# Raspberry Pi Edge Node: Phidgets + Node-RED Integration

## Overview

This document focuses specifically on setting up Raspberry Pi units as edge computing nodes for industrial sensor data acquisition using Phidget sensors and Node-RED for data processing and integration. The Pi serves as the bridge between physical sensors and higher-level systems, handling local data processing, protocol conversion, and reliable communication.

The architecture covers the complete sensor-to-Node-RED pipeline: **Phidget Sensors → Python Drivers → Node-RED Processing → OPC-UA/MQTT Output**

## Raspberry Pi Hardware Setup

### Hardware Requirements
**Recommended Pi Configuration:**
- **Raspberry Pi 4 Model B (4GB RAM)**: Sufficient processing power for multiple sensors and Node-RED flows with industrial-grade reliability
- **32GB+ Industrial SD Card**: High-endurance SD card rated for continuous write operations in industrial environments
- **Official Pi Power Supply**: 5V 3A USB-C power supply or industrial 24V to 5V converter for panel mounting
- **Case with DIN Rail Mount**: Industrial enclosure suitable for brewery/industrial environment with proper ventilation

**Phidget Hardware:**
- **VINT Hub Phidget (HUB0000)**: Primary interface for connecting multiple Phidget sensors via single USB connection
- **Humidity/Temperature Sensor (HUM1001)**: Digital sensor with high accuracy for brewing applications
- **Additional Sensors as Needed**: Pressure, pH, flow sensors based on specific monitoring requirements

### Initial Pi Configuration
Configure the Raspberry Pi with industrial-grade settings optimized for continuous operation and remote management.

```bash
#!/bin/bash
# pi-initial-setup.sh - Basic Pi configuration for industrial edge node

echo "=== Raspberry Pi Industrial Edge Node Setup ==="

# Update system packages
sudo apt update && sudo apt upgrade -y

# Install essential packages for industrial operation
sudo apt install -y \
    python3-pip \
    git \
    htop \
    iotop \
    curl \
    wget \
    vim \
    screen \
    rsync \
    ntpdate

# Configure timezone for brewery operations
sudo timedatectl set-timezone America/Los_Angeles

# Enable SSH for remote management
sudo systemctl enable ssh
sudo systemctl start ssh

# Configure log rotation for long-term operation
sudo tee /etc/logrotate.d/pi-edge-node << 'EOF'
/var/log/pi-edge/*.log {
    daily
    rotate 30
    compress
    delaycompress
    missingok
    create 644 pi pi
}
EOF

# Create directories for edge node operations
mkdir -p /home/pi/edge-node/{logs,data,scripts,backup}
mkdir -p /var/log/pi-edge
chown pi:pi /home/pi/edge-node /var/log/pi-edge

# Configure WiFi for brewery network (edit as needed)
echo "WiFi configuration will need brewery-specific SSID/password"

echo "Basic Pi setup complete. Ready for Phidget and Node-RED installation."
```

## Phidget Integration Setup

### Phidget Library Installation
Install Phidget libraries and dependencies for reliable sensor communication with proper error handling.

```bash
#!/bin/bash
# install-phidgets.sh - Phidget library installation and configuration

echo "=== Installing Phidget Libraries ==="

# Install Phidget repository and libraries
wget -qO- https://www.phidgets.com/downloads/setup_linux | sudo bash
sudo apt update
sudo apt install -y libphidget22 libphidget22-dev phidget22-admin

# Install Python Phidget libraries
pip3 install Phidget22

# Install additional Python packages for sensor processing
pip3 install \
    numpy \
    scipy \
    pandas

# Add pi user to phidget group for device access
sudo usermod -a -G phidget pi

# Create udev rules for Phidget device permissions
sudo tee /etc/udev/rules.d/99-phidgets.rules << 'EOF'
SUBSYSTEM=="usb", ATTR{idVendor}=="06c2", MODE="0666", GROUP="phidget"
SUBSYSTEM=="usb", ATTR{idVendor}=="0925", MODE="0666", GROUP="phidget"
EOF

# Reload udev rules
sudo udevadm control --reload-rules
sudo udevadm trigger

echo "Phidget libraries installed. Please reboot Pi before testing sensors."
```

### Phidget Device Testing and Validation
Create comprehensive testing scripts to validate Phidget sensor connectivity and data quality before integration.

```python
#!/usr/bin/env python3
# phidget_device_test.py - Comprehensive Phidget device testing

import sys
import time
import logging
from Phidget22.Phidget import *
from Phidget22.Devices.HumiditySensor import *
from Phidget22.Devices.TemperatureSensor import *

# Configure logging for device testing
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)-8s | %(message)s',
    handlers=[
        logging.FileHandler('/var/log/pi-edge/phidget_test.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class PhidgetDeviceTester:
    def __init__(self):
        self.devices_found = []
        self.test_results = {}
    
    def discover_devices(self):
        """Discover all connected Phidget devices"""
        logger.info("Starting Phidget device discovery...")
        
        try:
            # Test VINT Hub connection
            from Phidget22.Devices.Hub import *
            hub = Hub()
            hub.openWaitForAttachment(5000)
            
            logger.info(f"VINT Hub found - Serial: {hub.getDeviceSerialNumber()}")
            logger.info(f"Hub Port Count: {hub.getPortCount()}")
            
            # Check each VINT port
            for port in range(hub.getPortCount()):
                try:
                    port_mode = hub.getPortMode(port)
                    logger.info(f"Port {port}: Mode = {port_mode}")
                except Exception as e:
                    logger.warning(f"Port {port}: {e}")
            
            hub.close()
            self.devices_found.append(f"VINT Hub - Serial: {hub.getDeviceSerialNumber()}")
            
        except Exception as e:
            logger.error(f"No VINT Hub found: {e}")
            return False
        
        return True
    
    def test_humidity_sensor(self, hub_port=0, timeout=10):
        """Test humidity sensor connectivity and data quality"""
        logger.info(f"Testing humidity sensor on VINT port {hub_port}")
        
        try:
            humidity_sensor = HumiditySensor()
            humidity_sensor.setHubPort(hub_port)
            
            # Set up event handlers for data validation
            readings = []
            
            def on_humidity_change(self, humidity):
                readings.append({
                    'type': 'humidity',
                    'value': humidity,
                    'timestamp': time.time()
                })
                logger.info(f"Humidity: {humidity:.2f}%RH")
            
            humidity_sensor.setOnHumidityChangeHandler(on_humidity_change)
            
            # Connect and collect data
            humidity_sensor.openWaitForAttachment(5000)
            logger.info("Humidity sensor connected - collecting test data...")
            
            # Collect data for specified timeout
            start_time = time.time()
            while time.time() - start_time < timeout:
                time.sleep(0.5)
            
            humidity_sensor.close()
            
            # Validate data quality
            if len(readings) > 0:
                values = [r['value'] for r in readings]
                avg_humidity = sum(values) / len(values)
                
                self.test_results['humidity'] = {
                    'status': 'PASS',
                    'readings_count': len(readings),
                    'average_value': avg_humidity,
                    'min_value': min(values),
                    'max_value': max(values),
                    'data_rate': len(readings) / timeout
                }
                
                logger.info(f"Humidity test PASSED - {len(readings)} readings, avg: {avg_humidity:.2f}%RH")
                return True
            else:
                self.test_results['humidity'] = {'status': 'FAIL', 'error': 'No data received'}
                logger.error("Humidity test FAILED - No data received")
                return False
                
        except Exception as e:
            self.test_results['humidity'] = {'status': 'FAIL', 'error': str(e)}
            logger.error(f"Humidity test FAILED: {e}")
            return False
    
    def test_temperature_sensor(self, hub_port=0, timeout=10):
        """Test temperature sensor if available on humidity sensor"""
        logger.info(f"Testing temperature sensor on VINT port {hub_port}")
        
        try:
            temp_sensor = TemperatureSensor()
            temp_sensor.setHubPort(hub_port)
            
            readings = []
            
            def on_temperature_change(self, temperature):
                readings.append({
                    'type': 'temperature',
                    'value': temperature,
                    'timestamp': time.time()
                })
                logger.info(f"Temperature: {temperature:.2f}°C")
            
            temp_sensor.setOnTemperatureChangeHandler(on_temperature_change)
            
            temp_sensor.openWaitForAttachment(5000)
            logger.info("Temperature sensor connected - collecting test data...")
            
            start_time = time.time()
            while time.time() - start_time < timeout:
                time.sleep(0.5)
            
            temp_sensor.close()
            
            if len(readings) > 0:
                values = [r['value'] for r in readings]
                avg_temp = sum(values) / len(values)
                
                self.test_results['temperature'] = {
                    'status': 'PASS',
                    'readings_count': len(readings),
                    'average_value': avg_temp,
                    'min_value': min(values),
                    'max_value': max(values),
                    'data_rate': len(readings) / timeout
                }
                
                logger.info(f"Temperature test PASSED - {len(readings)} readings, avg: {avg_temp:.2f}°C")
                return True
            else:
                self.test_results['temperature'] = {'status': 'FAIL', 'error': 'No data received'}
                logger.error("Temperature test FAILED - No data received")
                return False
                
        except Exception as e:
            self.test_results['temperature'] = {'status': 'FAIL', 'error': str(e)}
            logger.error(f"Temperature test FAILED: {e}")
            return False
    
    def run_full_test(self):
        """Run comprehensive device testing"""
        logger.info("=== Starting Phidget Device Test Suite ===")
        
        # Device discovery
        if not self.discover_devices():
            logger.error("Device discovery failed - check VINT Hub connection")
            return False
        
        # Test sensors on each VINT port
        test_passed = True
        for port in range(4):  # VINT Hub typically has 4 ports
            logger.info(f"Testing sensors on VINT port {port}")
            
            if not self.test_humidity_sensor(port, timeout=5):
                logger.warning(f"No humidity sensor on port {port}")
            
            if not self.test_temperature_sensor(port, timeout=5):
                logger.warning(f"No temperature sensor on port {port}")
        
        # Generate test report
        self.generate_test_report()
        return test_passed
    
    def generate_test_report(self):
        """Generate comprehensive test report"""
        logger.info("=== Test Results Summary ===")
        
        for sensor_type, results in self.test_results.items():
            if results['status'] == 'PASS':
                logger.info(f"{sensor_type.upper()}: {results['status']} - "
                          f"{results['readings_count']} readings, "
                          f"avg: {results['average_value']:.2f}")
            else:
                logger.error(f"{sensor_type.upper()}: {results['status']} - {results['error']}")
        
        # Save detailed results to file
        import json
        with open('/var/log/pi-edge/phidget_test_results.json', 'w') as f:
            json.dump(self.test_results, f, indent=2)

if __name__ == "__main__":
    tester = PhidgetDeviceTester()
    success = tester.run_full_test()
    
    if success:
        logger.info("Phidget testing completed successfully")
        sys.exit(0)
    else:
        logger.error("Phidget testing completed with errors")
        sys.exit(1)
```

## Node-RED Installation and Configuration

### Node-RED Installation for Pi Edge Nodes
Install Node-RED with industrial-grade configuration optimized for continuous operation and sensor data processing.

```bash
#!/bin/bash
# install-node-red.sh - Node-RED installation for industrial edge node

echo "=== Installing Node-RED for Pi Edge Node ==="

# Install Node.js and Node-RED using official installer
bash <(curl -sL https://raw.githubusercontent.com/node-red/linux-installers/master/deb/update-nodejs-and-nodered)

# Enable Node-RED service for automatic startup
sudo systemctl enable nodered.service

# Install essential Node-RED nodes for industrial operations
cd /home/pi/.node-red

npm install \
    node-red-contrib-opcua \
    node-red-contrib-modbus \
    node-red-dashboard \
    node-red-contrib-influxdb \
    node-red-contrib-mqtt-broker \
    node-red-contrib-buffer-parser \
    node-red-contrib-cron-plus

# Install Phidget-specific Node-RED nodes
npm install node-red-contrib-phidget22

echo "Node-RED installation complete"
```

### Node-RED Configuration for Industrial Operation
Configure Node-RED with security, performance, and reliability settings appropriate for industrial edge computing.

```javascript
// /home/pi/.node-red/settings.js - Industrial Node-RED configuration

module.exports = {
    // Network and performance settings
    uiPort: process.env.PORT || 1880,
    uiHost: "0.0.0.0",  // Allow external connections for remote management
    
    // MQTT settings for industrial reliability
    mqttReconnectTime: 15000,
    serialReconnectTime: 15000,
    
    // Memory and performance optimization
    debugMaxLength: 1000,
    maxNodeRedLogs: 100,
    
    // Security configuration for industrial environment
    adminAuth: {
        type: "credentials",
        users: [{
            username: "admin",
            password: "$2b$08$BHbVOp3DaIhO8QQQZ8E6aOUxn8QjB.v5Ml5pTa4dNjG5r5tGJQFpu", // password: admin123
            permissions: "*"
        }]
    },
    
    // HTTP endpoint configuration
    httpAdminRoot: '/admin',
    httpNodeRoot: '/api',
    httpStatic: '/home/pi/.node-red/public/',
    
    // Function node settings with industrial context
    functionGlobalContext: {
        // Industrial edge node configuration
        edgeNode: {
            name: process.env.EDGE_NODE_NAME || "Pi-Edge-001",
            location: process.env.EDGE_NODE_LOCATION || "Brewery Floor",
            timezone: process.env.TZ || "America/Los_Angeles"
        },
        
        // Sensor configuration
        sensors: {
            updateRate: 1000,  // 1 second update rate for industrial monitoring
            alarmThresholds: {
                temperature: { min: 0, max: 80 },  // Celsius
                humidity: { min: 10, max: 95 }     // %RH
            }
        },
        
        // Communication settings
        communication: {
            opcua: {
                endpoint: process.env.OPCUA_ENDPOINT || "opc.tcp://ignition:62541",
                namespace: "Brewery"
            },
            mqtt: {
                broker: process.env.MQTT_BROKER || "localhost:1883",
                topic_prefix: process.env.MQTT_TOPIC_PREFIX || "brewery/edge"
            }
        }
    },
    
    // Logging configuration for industrial traceability
    logging: {
        console: {
            level: "info",
            metrics: false,
            audit: false
        },
        file: {
            level: "info",
            filename: "/var/log/pi-edge/node-red.log",
            maxFiles: 10,
            maxSize: "10MB"
        }
    },
    
    // Storage settings for industrial reliability
    storageModule: require("node-red/lib/storage/localfilesystem"),
    
    // Editor settings
    editorTheme: {
        projects: {
            enabled: true
        },
        palette: {
            editable: true
        }
    },
    
    // Context storage for industrial data persistence
    contextStorage: {
        default: "file",
        file: {
            module: "localfilesystem"
        },
        memory: {
            module: "memory"
        }
    }
};
```

## Phidget to Node-RED Integration

### Custom Node-RED Nodes for Phidget Integration
Create custom Node-RED nodes that provide robust Phidget sensor integration with industrial-grade error handling and data validation.

```javascript
// nodes/phidget-humidity-sensor.js - Custom Node-RED node for Phidget humidity sensor

module.exports = function(RED) {
    "use strict";
    
    function PhidgetHumiditySensorNode(config) {
        RED.nodes.createNode(this, config);
        var node = this;
        
        // Configuration from Node-RED editor
        node.sensorName = config.sensorName || "HumiditySensor";
        node.hubPort = parseInt(config.hubPort) || 0;
        node.updateRate = parseInt(config.updateRate) || 1000;
        node.enableAlarms = config.enableAlarms || false;
        node.tempMin = parseFloat(config.tempMin) || 0;
        node.tempMax = parseFloat(config.tempMax) || 80;
        node.humidityMin = parseFloat(config.humidityMin) || 10;
        node.humidityMax = parseFloat(config.humidityMax) || 95;
        
        // Sensor state tracking
        node.sensorConnected = false;
        node.lastReading = null;
        node.alarmState = {
            temperatureHigh: false,
            temperatureLow: false,
            humidityHigh: false,
            humidityLow: false
        };
        
        // Import Phidget libraries
        var phidget22;
        try {
            phidget22 = require('phidget22');
        } catch (err) {
            node.error("Failed to load Phidget22 library: " + err.message);
            return;
        }
        
        var HumiditySensor = phidget22.HumiditySensor;
        var TemperatureSensor = phidget22.TemperatureSensor;
        
        // Initialize sensors
        var humiditySensor = new HumiditySensor();
        var temperatureSensor = new TemperatureSensor();
        
        // Set VINT Hub port
        humiditySensor.setHubPort(node.hubPort);
        temperatureSensor.setHubPort(node.hubPort);
        
        // Data processing and validation
        function processReading(type, value, timestamp) {
            var reading = {
                sensor: node.sensorName,
                type: type,
                value: parseFloat(value.toFixed(2)),
                timestamp: timestamp || new Date().toISOString(),
                quality: "Good"
            };
            
            // Validate reading ranges
            if (type === "temperature") {
                if (value < node.tempMin || value > node.tempMax) {
                    reading.quality = "Bad";
                    
                    if (node.enableAlarms) {
                        var alarmType = value < node.tempMin ? "temperatureLow" : "temperatureHigh";
                        if (!node.alarmState[alarmType]) {
                            node.alarmState[alarmType] = true;
                            sendAlarm(alarmType, value, type);
                        }
                    }
                } else {
                    // Clear alarms if value is back in range
                    if (node.alarmState.temperatureLow || node.alarmState.temperatureHigh) {
                        node.alarmState.temperatureLow = false;
                        node.alarmState.temperatureHigh = false;
                        sendAlarmClear("temperature");
                    }
                }
            }
            
            if (type === "humidity") {
                if (value < node.humidityMin || value > node.humidityMax) {
                    reading.quality = "Bad";
                    
                    if (node.enableAlarms) {
                        var alarmType = value < node.humidityMin ? "humidityLow" : "humidityHigh";
                        if (!node.alarmState[alarmType]) {
                            node.alarmState[alarmType] = true;
                            sendAlarm(alarmType, value, type);
                        }
                    }
                } else {
                    if (node.alarmState.humidityLow || node.alarmState.humidityHigh) {
                        node.alarmState.humidityLow = false;
                        node.alarmState.humidityHigh = false;
                        sendAlarmClear("humidity");
                    }
                }
            }
            
            node.lastReading = reading;
            return reading;
        }
        
        // Alarm handling
        function sendAlarm(alarmType, value, sensorType) {
            var alarmMsg = {
                topic: "alarm",
                payload: {
                    sensor: node.sensorName,
                    alarmType: alarmType,
                    currentValue: value,
                    sensorType: sensorType,
                    timestamp: new Date().toISOString(),
                    severity: "Warning"
                }
            };
            
            node.send([null, alarmMsg]);
            node.warn(`${alarmType} alarm: ${value} ${sensorType === "temperature" ? "°C" : "%RH"}`);
        }
        
        function sendAlarmClear(sensorType) {
            var clearMsg = {
                topic: "alarm_clear",
                payload: {
                    sensor: node.sensorName,
                    sensorType: sensorType,
                    timestamp: new Date().toISOString()
                }
            };
            
            node.send([null, clearMsg]);
            node.log(`${sensorType} alarm cleared`);
        }
        
        // Humidity sensor event handlers
        humiditySensor.onHumidityChange = function(humidity) {
            var reading = processReading("humidity", humidity);
            var msg = {
                topic: "sensor/humidity",
                payload: reading
            };
            node.send([msg, null]);
        };
        
        // Temperature sensor event handlers
        temperatureSensor.onTemperatureChange = function(temperature) {
            var reading = processReading("temperature", temperature);
            var msg = {
                topic: "sensor/temperature", 
                payload: reading
            };
            node.send([msg, null]);
        };
        
        // Connection handling
        function connectSensors() {
            node.status({fill: "yellow", shape: "ring", text: "connecting"});
            
            Promise.all([
                humiditySensor.open(5000),
                temperatureSensor.open(5000)
            ]).then(() => {
                node.sensorConnected = true;
                node.status({fill: "green", shape: "dot", text: "connected"});
                node.log(`Humidity/Temperature sensor connected on VINT port ${node.hubPort}`);
            }).catch((err) => {
                node.sensorConnected = false;
                node.status({fill: "red", shape: "ring", text: "connection failed"});
                node.error(`Failed to connect sensors: ${err.message}`);
                
                // Retry connection after delay
                setTimeout(connectSensors, 5000);
            });
        }
        
        // Disconnect handling
        function disconnectSensors() {
            try {
                if (humiditySensor) humiditySensor.close();
                if (temperatureSensor) temperatureSensor.close();
                node.sensorConnected = false;
                node.status({fill: "red", shape: "ring", text: "disconnected"});
            } catch (err) {
                node.error(`Error disconnecting sensors: ${err.message}`);
            }
        }
        
        // Error handling
        humiditySensor.onError = function(code, description) {
            node.error(`Humidity sensor error ${code}: ${description}`);
            node.status({fill: "red", shape: "ring", text: "sensor error"});
        };
        
        temperatureSensor.onError = function(code, description) {
            node.error(`Temperature sensor error ${code}: ${description}`);
            node.status({fill: "red", shape: "ring", text: "sensor error"});
        };
        
        // Node lifecycle management
        connectSensors();
        
        node.on('close', function(done) {
            disconnectSensors();
            done();
        });
    }
    
    // Register the node type
    RED.nodes.registerType("phidget-humidity-sensor", PhidgetHumiditySensorNode);
};
```

### Node-RED Flow Templates for Sensor Integration
Create reusable Node-RED flow templates that demonstrate best practices for Phidget sensor integration and data processing.

```json
[
    {
        "id": "phidget_sensor_flow",
        "type": "tab",
        "label": "Phidget Sensors",
        "disabled": false,
        "info": "Edge node sensor data acquisition and processing"
    },
    {
        "id": "humidity_sensor_1",
        "type": "phidget-humidity-sensor",
        "z": "phidget_sensor_flow",
        "name": "Tank 1 Environment",
        "sensorName": "Tank1_Environment",
        "hubPort": "0",
        "updateRate": "1000",
        "enableAlarms": true,
        "tempMin": "15",
        "tempMax": "30",
        "humidityMin": "40",
        "humidityMax": "80",
        "x": 150,
        "y": 100,
        "wires": [
            ["data_processor", "debug_sensor"],
            ["alarm_handler"]
        ]
    },
    {
        "id": "data_processor",
        "type": "function",
        "z": "phidget_sensor_flow",
        "name": "Process Sensor Data",
        "func": "// Process and enrich sensor data\nvar processed = {\n    deviceId: global.get('edgeNode.name') || 'unknown',\n    location: global.get('edgeNode.location') || 'unknown',\n    sensor: msg.payload.sensor,\n    measurement: {\n        type: msg.payload.type,\n        value: msg.payload.value,\n        unit: msg.payload.type === 'temperature' ? '°C' : '%RH',\n        quality: msg.payload.quality,\n        timestamp: msg.payload.timestamp\n    },\n    metadata: {\n        edgeProcessingTime: new Date().toISOString(),\n        dataSource: 'phidget_vint'\n    }\n};\n\n// Add to context for local storage\ncontext.set('lastReading_' + msg.payload.type, processed);\n\n// Prepare for downstream processing\nmsg.payload = processed;\nmsg.topic = `sensor/${processed.deviceId}/${processed.sensor}/${processed.measurement.type}`;\n\nreturn msg;",
        "outputs": 1,
        "timeout": "",
        "noerr": 0,
        "initialize": "",
        "finalize": "",
        "x": 400,
        "y": 100,
        "wires": [
            ["opcua_publisher", "mqtt_publisher", "local_storage"]
        ]
    },
    {
        "id": "alarm_handler",
        "type": "function",
        "z": "phidget_sensor_flow",
        "name": "Alarm Processing",
        "func": "// Process alarms with escalation logic\nvar alarm = {\n    deviceId: global.get('edgeNode.name'),\n    location: global.get('edgeNode.location'),\n    alarm: {\n        type: msg.payload.alarmType,\n        sensor: msg.payload.sensor,\n        severity: msg.payload.severity,\n        currentValue: msg.payload.currentValue,\n        timestamp: msg.payload.timestamp,\n        acknowledged: false\n    }\n};\n\n// Store alarm in context\nvar activeAlarms = context.get('activeAlarms') || [];\nactiveAlarms.push(alarm);\ncontext.set('activeAlarms', activeAlarms);\n\n// Prepare for notification systems\nmsg.payload = alarm;\nmsg.topic = `alarm/${alarm.deviceId}/${alarm.alarm.sensor}`;\n\nreturn msg;",
        "outputs": 1,
        "timeout": "",
        "noerr": 0,
        "initialize": "",
        "finalize": "",
        "x": 400,
        "y": 200,
        "wires": [
            ["alarm_notification"]
        ]
    },
    {
        "id": "opcua_publisher",
        "type": "OpcUa-Client",
        "z": "phidget_sensor_flow",
        "endpoint": "opc.tcp://ignition:62541",
        "action": "write",
        "deadbandtype": "a",
        "deadbandvalue": 1,
        "time": 10,
        "timeUnit": "s",
        "certificate": "n",
        "localfile": "",
        "localkeyfile": "",
        "securitymode": "None",
        "securitypolicy": "None",
        "name": "Ignition Edge OPC-UA",
        "x": 650,
        "y": 80,
        "wires": [
            ["debug_opcua"]
        ]
    },
    {
        "id": "mqtt_publisher",
        "type": "mqtt out",
        "z": "phidget_sensor_flow",
        "name": "MQTT Broker",
        "topic": "",
        "qos": "1",
        "retain": "false",
        "broker": "mqtt_broker",
        "x": 650,
        "y": 120,
        "wires": []
    },
    {
        "id": "local_storage",
        "type": "file",
        "z": "phidget_sensor_flow",
        "name": "Local Data Buffer",
        "filename": "/home/pi/edge-node/data/sensor_data.log",
        "appendNewline": true,
        "createDir": true,
        "overwriteFile": "false",
        "encoding": "none",
        "x": 650,
        "y": 160,
        "wires": []
    }
]
```

## Development and Deployment Workflow

### VS Code Remote Development Setup
Configure VS Code for efficient remote development on Raspberry Pi units with integrated debugging and deployment capabilities.

```json
// .vscode/tasks.json - VS Code tasks for Pi development
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "Deploy to Pi",
            "type": "shell",
            "command": "rsync",
            "args": [
                "-avz",
                "--exclude=node_modules",
                "--exclude=.git",
                "./",
                "pi@${input:piHostname}:/home/pi/edge-node/"
            ],
            "group": "build",
            "presentation": {
                "echo": true,
                "reveal": "always",
                "focus": false,
                "panel": "shared",
                "showReuseMessage": true,
                "clear": false
            }
        },
        {
            "label": "Test Phidget Connection",
            "type": "shell",
            "command": "ssh",
            "args": [
                "pi@${input:piHostname}",
                "cd /home/pi/edge-node && python3 phidget_device_test.py"
            ],
            "group": "test",
            "presentation": {
                "echo": true,
                "reveal": "always",
                "focus": false,
                "panel": "shared"
            }
        },
        {
            "label": "Restart Node-RED",
            "type": "shell",
            "command": "ssh",
            "args": [
                "pi@${input:piHostname}",
                "sudo systemctl restart nodered"
            ],
            "group": "build"
        },
        {
            "label": "View Node-RED Logs",
            "type": "shell",
            "command": "ssh",
            "args": [
                "pi@${input:piHostname}",
                "journalctl -u nodered -f"
            ],
            "group": "test",
            "presentation": {
                "echo": true,
                "reveal": "always",
                "focus": true,
                "panel": "new"
            }
        }
    ],
    "inputs": [
        {
            "id": "piHostname",
            "description": "Raspberry Pi Hostname or IP",
            "default": "raspberrypi.local",
            "type": "promptString"
        }
    ]
}
```

### Automated Deployment Scripts
Create deployment scripts that automate the process of updating Pi edge nodes with new configurations and code.

```bash
#!/bin/bash
# deploy-edge-node.sh - Automated deployment script for Pi edge nodes

# Configuration
PI_USERNAME="pi"
EDGE_NODE_PATH="/home/pi/edge-node"
NODE_RED_PATH="/home/pi/.node-red"

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--host)
            PI_HOST="$2"
            shift 2
            ;;
        -f|--flows)
            DEPLOY_FLOWS=true
            shift
            ;;
        -c|--config)
            DEPLOY_CONFIG=true
            shift
            ;;
        -p|--phidget)
            DEPLOY_PHIDGET=true
            shift
            ;;
        --all)
            DEPLOY_FLOWS=true
            DEPLOY_CONFIG=true
            DEPLOY_PHIDGET=true
            shift
            ;;
        *)
            echo "Unknown option $1"
            exit 1
            ;;
    esac
done

# Validate required parameters
if [ -z "$PI_HOST" ]; then
    echo "Error: Pi hostname or IP required (-h/--host)"
    echo "Usage: $0 -h <hostname> [--flows] [--config] [--phidget] [--all]"
    exit 1
fi

echo "=== Deploying Edge Node Configuration to $PI_HOST ==="

# Test SSH connectivity
if ! ssh -q "$PI_USERNAME@$PI_HOST" exit; then
    echo "Error: Cannot connect to $PI_HOST"
    exit 1
fi

# Deploy Phidget drivers and scripts
if [ "$DEPLOY_PHIDGET" = true ]; then
    echo "Deploying Phidget drivers..."
    rsync -avz --progress \
        ./src/phidget-drivers/ \
        "$PI_USERNAME@$PI_HOST:$EDGE_NODE_PATH/phidget-drivers/"
    
    rsync -avz --progress \
        ./scripts/phidget_device_test.py \
        "$PI_USERNAME@$PI_HOST:$EDGE_NODE_PATH/"
    
    echo "Testing Phidget installation..."
    ssh "$PI_USERNAME@$PI_HOST" "cd $EDGE_NODE_PATH && python3 phidget_device_test.py"
fi

# Deploy Node-RED flows
if [ "$DEPLOY_FLOWS" = true ]; then
    echo "Deploying Node-RED flows..."
    
    # Backup existing flows
    ssh "$PI_USERNAME@$PI_HOST" "cp $NODE_RED_PATH/flows.json $NODE_RED_PATH/flows_backup_$(date +%Y%m%d_%H%M%S).json"
    
    # Deploy new flows
    rsync -avz --progress \
        ./config/node-red/flows/ \
        "$PI_USERNAME@$PI_HOST:$NODE_RED_PATH/"
    
    # Deploy custom nodes
    rsync -avz --progress \
        ./src/brewery-nodes/ \
        "$PI_USERNAME@$PI_HOST:$NODE_RED_PATH/nodes/"
    
    echo "Restarting Node-RED service..."
    ssh "$PI_USERNAME@$PI_HOST" "sudo systemctl restart nodered"
    
    # Wait for Node-RED to start
    echo "Waiting for Node-RED to restart..."
    sleep 10
    
    # Verify Node-RED is running
    if ssh "$PI_USERNAME@$PI_HOST" "systemctl is-active --quiet nodered"; then
        echo "Node-RED restarted successfully"
    else
        echo "Warning: Node-RED may not have started correctly"
        ssh "$PI_USERNAME@$PI_HOST" "journalctl -u nodered --lines=20"
    fi
fi

# Deploy configuration files
if [ "$DEPLOY_CONFIG" = true ]; then
    echo "Deploying configuration files..."
    
    rsync -avz --progress \
        ./config/pi-setup/ \
        "$PI_USERNAME@$PI_HOST:$EDGE_NODE_PATH/config/"
    
    # Update Node-RED settings if provided
    if [ -f "./config/node-red/settings.js" ]; then
        rsync -avz --progress \
            ./config/node-red/settings.js \
            "$PI_USERNAME@$PI_HOST:$NODE_RED_PATH/"
    fi
fi

echo "=== Deployment Complete ==="
echo "Node-RED URL: http://$PI_HOST:1880"
echo "SSH Access: ssh $PI_USERNAME@$PI_HOST"
```

## Monitoring and Maintenance

### System Health Monitoring
Implement comprehensive monitoring for Pi edge nodes that tracks both hardware and software health metrics.

```python
#!/usr/bin/env python3
# edge_node_monitor.py - Comprehensive edge node health monitoring

import os
import sys
import time
import json
import psutil
import logging
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)-8s | %(name)-15s | %(message)s',
    handlers=[
        logging.FileHandler('/var/log/pi-edge/health_monitor.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('HealthMonitor')

class EdgeNodeHealthMonitor:
    def __init__(self):
        self.health_data = {
            'timestamp': None,
            'system': {},
            'services': {},
            'phidgets': {},
            'node_red': {},
            'network': {},
            'storage': {},
            'alerts': []
        }
        
    def collect_system_metrics(self):
        """Collect system performance metrics"""
        try:
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            
            # Memory usage
            memory = psutil.virtual_memory()
            
            # System temperature (Raspberry Pi specific)
            temp_raw = os.popen('vcgencmd measure_temp').readline()
            cpu_temp = float(temp_raw.replace("temp=","").replace("'C\n",""))
            
            # System uptime
            boot_time = datetime.fromtimestamp(psutil.boot_time())
            uptime = datetime.now() - boot_time
            
            self.health_data['system'] = {
                'cpu_percent': cpu_percent,
                'memory_percent': memory.percent,
                'memory_available_mb': round(memory.available / 1024 / 1024, 1),
                'cpu_temperature': cpu_temp,
                'uptime_hours': round(uptime.total_seconds() / 3600, 1),
                'load_average': os.getloadavg()
            }
            
            # Check for system alerts
            if cpu_percent > 80:
                self.health_data['alerts'].append({
                    'type': 'HIGH_CPU',
                    'value': cpu_percent,
                    'threshold': 80,
                    'severity': 'WARNING'
                })
            
            if cpu_temp > 70:
                self.health_data['alerts'].append({
                    'type': 'HIGH_TEMPERATURE',
                    'value': cpu_temp,
                    'threshold': 70,
                    'severity': 'WARNING'
                })
                
            if memory.percent > 85:
                self.health_data['alerts'].append({
                    'type': 'HIGH_MEMORY',
                    'value': memory.percent,
                    'threshold': 85,
                    'severity': 'WARNING'
                })
                
            logger.info(f"System metrics: CPU {cpu_percent}%, Memory {memory.percent}%, Temp {cpu_temp}°C")
            
        except Exception as e:
            logger.error(f"Failed to collect system metrics: {e}")
            self.health_data['alerts'].append({
                'type': 'SYSTEM_METRICS_FAILURE',
                'error': str(e),
                'severity': 'ERROR'
            })
    
    def check_service_status(self):
        """Check status of critical services"""
        services = ['nodered', 'ssh']
        
        for service in services:
            try:
                result = os.system(f'systemctl is-active --quiet {service}')
                status = 'running' if result == 0 else 'stopped'
                
                self.health_data['services'][service] = {
                    'status': status,
                    'checked_at': datetime.now().isoformat()
                }
                
                if status == 'stopped':
                    self.health_data['alerts'].append({
                        'type': 'SERVICE_DOWN',
                        'service': service,
                        'severity': 'ERROR'
                    })
                    
            except Exception as e:
                logger.error(f"Failed to check {service} status: {e}")
                self.health_data['services'][service] = {
                    'status': 'unknown',
                    'error': str(e)
                }
    
    def check_phidget_devices(self):
        """Check Phidget device connectivity"""
        try:
            from Phidget22.Phidget import *
            from Phidget22.Devices.Hub import *
            
            hub = Hub()
            hub.openWaitForAttachment(5000)
            
            self.health_data['phidgets'] = {
                'hub_connected': True,
                'hub_serial': hub.getDeviceSerialNumber(),
                'port_count': hub.getPortCount(),
                'ports': {}
            }
            
            # Check each VINT port
            for port in range(hub.getPortCount()):
                try:
                    port_mode = hub.getPortMode(port)
                    self.health_data['phidgets']['ports'][port] = {
                        'mode': str(port_mode),
                        'status': 'connected' if port_mode != PortMode.VINT_PORT_MODE_DIGITAL_INPUT else 'empty'
                    }
                except Exception as e:
                    self.health_data['phidgets']['ports'][port] = {
                        'status': 'error',
                        'error': str(e)
                    }
            
            hub.close()
            logger.info(f"Phidget Hub connected: {hub.getDeviceSerialNumber()}")
            
        except Exception as e:
            logger.warning(f"Phidget connectivity check failed: {e}")
            self.health_data['phidgets'] = {
                'hub_connected': False,
                'error': str(e)
            }
            self.health_data['alerts'].append({
                'type': 'PHIDGET_DISCONNECTED',
                'error': str(e),
                'severity': 'ERROR'
            })
    
    def check_node_red_status(self):
        """Check Node-RED health and performance"""
        try:
            import requests
            
            # Check Node-RED admin interface
            response = requests.get('http://localhost:1880/admin', timeout=5)
            node_red_responsive = response.status_code == 200
            
            self.health_data['node_red'] = {
                'responsive': node_red_responsive,
                'admin_accessible': True,
                'checked_at': datetime.now().isoformat()
            }
            
            if not node_red_responsive:
                self.health_data['alerts'].append({
                    'type': 'NODE_RED_UNRESPONSIVE',
                    'severity': 'ERROR'
                })
                
        except Exception as e:
            logger.warning(f"Node-RED health check failed: {e}")
            self.health_data['node_red'] = {
                'responsive': False,
                'admin_accessible': False,
                'error': str(e)
            }
    
    def check_network_connectivity(self):
        """Check network connectivity and performance"""
        try:
            # Check internet connectivity
            internet_result = os.system('ping -c 1 8.8.8.8 > /dev/null 2>&1')
            internet_connected = internet_result == 0
            
            # Check local network (assuming gateway at .1)
            local_result = os.system('ping -c 1 192.168.1.1 > /dev/null 2>&1')
            local_connected = local_result == 0
            
            # Get network interface information
            network_interfaces = {}
            for interface, addrs in psutil.net_if_addrs().items():
                network_interfaces[interface] = {
                    'addresses': [addr.address for addr in addrs if addr.family == 2]  # IPv4
                }
            
            self.health_data['network'] = {
                'internet_connected': internet_connected,
                'local_network_connected': local_connected,
                'interfaces': network_interfaces
            }
            
            if not internet_connected:
                self.health_data['alerts'].append({
                    'type': 'INTERNET_DISCONNECTED',
                    'severity': 'WARNING'
                })
                
        except Exception as e:
            logger.error(f"Network connectivity check failed: {e}")
            self.health_data['network'] = {
                'error': str(e)
            }
    
    def check_storage_health(self):
        """Check storage usage and SD card health"""
        try:
            # Disk usage
            disk_usage = psutil.disk_usage('/')
            disk_percent = (disk_usage.used / disk_usage.total) * 100
            
            self.health_data['storage'] = {
                'total_gb': round(disk_usage.total / 1024**3, 1),
                'used_gb': round(disk_usage.used / 1024**3, 1),
                'free_gb': round(disk_usage.free / 1024**3, 1),
                'used_percent': round(disk_percent, 1)
            }
            
            if disk_percent > 85:
                self.health_data['alerts'].append({
                    'type': 'LOW_DISK_SPACE',
                    'used_percent': disk_percent,
                    'severity': 'WARNING'
                })
                
        except Exception as e:
            logger.error(f"Storage health check failed: {e}")
            self.health_data['storage'] = {
                'error': str(e)
            }
    
    def run_health_check(self):
        """Run complete health check"""
        logger.info("Starting edge node health check...")
        
        self.health_data['timestamp'] = datetime.now().isoformat()
        self.health_data['alerts'] = []  # Reset alerts
        
        self.collect_system_metrics()
        self.check_service_status()
        self.check_phidget_devices()
        self.check_node_red_status()
        self.check_network_connectivity()
        self.check_storage_health()
        
        # Save health data
        health_file = '/var/log/pi-edge/health_status.json'
        with open(health_file, 'w') as f:
            json.dump(self.health_data, f, indent=2)
        
        # Log summary
        alert_count = len(self.health_data['alerts'])
        if alert_count > 0:
            logger.warning(f"Health check completed with {alert_count} alerts")
            for alert in self.health_data['alerts']:
                logger.warning(f"Alert: {alert['type']} - {alert.get('severity', 'UNKNOWN')}")
        else:
            logger.info("Health check completed - all systems healthy")
        
        return self.health_data

if __name__ == "__main__":
    monitor = EdgeNodeHealthMonitor()
    health_data = monitor.run_health_check()
    
    # Exit with error code if critical alerts exist
    critical_alerts = [alert for alert in health_data['alerts'] if alert.get('severity') == 'ERROR']
    if critical_alerts:
        sys.exit(1)
    else:
        sys.exit(0)
```

## Conclusion

This document provides a comprehensive framework for setting up Raspberry Pi edge nodes with Phidget sensor integration and Node-RED data processing. The modular approach ensures that Pi units can be deployed consistently while maintaining flexibility for different sensor configurations and processing requirements.

**Key Implementation Steps:**
1. **Hardware Setup**: Configure Pi with industrial-grade settings and mount Phidget VINT Hub
2. **Software Installation**: Install Phidget libraries and Node-RED with industrial configuration
3. **Sensor Integration**: Deploy custom Node-RED nodes for robust Phidget sensor communication
4. **Development Workflow**: Use VS Code remote development for efficient Pi programming and deployment
5. **Monitoring**: Implement comprehensive health monitoring for proactive maintenance

**Next Steps:**
- Combine this document with your existing Ignition and Node-RED flow documentation
- Present all documentation to a single chat for integrated system development
- Begin prototype deployment with single Pi and basic sensor suite
- Scale deployment based on validated edge node architecture

The edge node architecture provides a solid foundation for industrial IoT applications while maintaining the flexibility to adapt to specific brewery and industrial monitoring requirements.