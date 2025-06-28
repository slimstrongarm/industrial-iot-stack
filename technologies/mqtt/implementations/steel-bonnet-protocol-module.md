# MQTT Protocol Module - Debug Infrastructure Guide

## Overview
The MQTT Protocol Module (v2.0) has been updated with comprehensive debug infrastructure following the strategic pattern established for efficient deployment. This module handles MQTT device discovery, message processing, and topic pattern analysis.

## Key Features

### 1. Debug Configuration
- **Global Integration**: Inherits settings from global debug config
- **MQTT-Specific Settings**:
  - `showTopicPatterns`: Display discovered topic patterns
  - `logAllMessages`: Log all MQTT messages (verbose mode)
  - `simulateBroker`: Use simulated MQTT data instead of real broker
  - `connectionRetries`: Number of connection attempts (1 for testing, 5 for production)
  - `discoveryInterval`: How often to check for new devices (5s testing, 60s production)

### 2. Deployment Modes
- **Testing Mode**: 
  - Uses simulated MQTT data
  - No external broker required
  - Faster discovery intervals
  - All debug features enabled
  
- **Development Mode**:
  - Connects to real MQTT broker
  - Enhanced logging and validation
  - Debug UI available
  
- **Production Mode**:
  - Minimal logging
  - Robust error handling
  - Automatic reconnection
  - Performance optimized

### 3. Data Simulation
The module includes comprehensive MQTT simulation for testing:
- Brewery equipment (fermenters, glycol chillers)
- Cellar equipment (tanks, temperature sensors)
- Utility systems (compressors, boilers)
- HomeAssistant-style discovery messages

### 4. Strategic Debug Features

#### Debug Nodes (Toggle-able)
- **Control Actions**: Monitor start/stop/reconfigure commands
- **MQTT Messages**: View all processed messages with topics
- **Discovery Events**: Track newly discovered devices
- **Pattern Analysis**: See topic structure patterns
- **Error Log**: Monitor connection and processing errors

#### Status Indicators
- Node status shows current operation (simulated data, discovered devices, etc.)
- Debug configuration status displays current mode
- Error nodes show last error with severity

### 5. Topic Pattern Analysis
Automatically analyzes MQTT topics to identify:
- Common topic structures (location/device/parameter)
- Device naming patterns
- Parameter types
- Discovery rules for automatic device identification

### 6. Debug Control Panel
Dashboard UI component providing:
- Toggle debug mode on/off
- Toggle simulation mode
- Real-time statistics:
  - Message count
  - Error count
  - Discovered topics
  - Discovered devices
- Current deployment mode display

## Usage Instructions

### 1. Initial Setup
```javascript
// The module automatically initializes on deploy
// Check the "Debug Config Status" node for confirmation
```

### 2. Testing Without MQTT Broker
1. Deploy the flow
2. Module defaults to testing mode with simulation
3. Watch the debug sidebar for simulated MQTT messages
4. Use Debug Control Panel to monitor activity

### 3. Connecting to Real MQTT Broker
1. Configure the `mqtt_broker` config node with your broker details
2. Use Debug Control Panel to disable simulation
3. Module will automatically connect and start discovery

### 4. Debugging Issues
1. Enable relevant debug nodes:
   - "MQTT Messages" for all traffic
   - "Discovery Events" for new devices
   - "Error Log" for connection issues
2. Check node status indicators
3. Use Debug Control Panel for statistics

### 5. Pattern Analysis
- Runs automatically every 60 seconds
- Results stored globally as `mqtt_topic_patterns`
- Enable "Pattern Analysis" debug node to see results
- Helps identify device naming conventions

## Integration Points

### Inputs
- **Module Control** (link in): Commands from protocol core
  - `start`: Enable MQTT discovery
  - `stop`: Disable MQTT discovery
  - `reconfigure`: Update MQTT settings
  - `debug`: Toggle debug mode

### Outputs
- **MQTT Data Out** (link out): Normalized device data
- **Discovery Out** (link out): New device notifications
- **Status Update** (link out): Module status changes
- **Error Out** (link out): Error notifications

### Global Variables
- `debugConfig`: Shared debug configuration
- `mqtt_topic_patterns`: Discovered topic patterns for other flows

## Data Formats

### Normalized MQTT Message
```javascript
{
    payload: {
        deviceId: "fermenter1",
        equipmentName: "fermenter1",
        topic: "brewery/fermenter1/temperature",
        value: 68.5,
        dataType: "number",
        parameter: "temperature",
        raw: 68.5,
        simulated: true,
        timestamp: "2025-01-25T10:30:00Z"
    },
    protocol: "mqtt",
    topic: "protocol/data"
}
```

### Device Discovery Message
```javascript
{
    action: "device_discovered",
    protocol: "mqtt",
    device: {
        name: "Brewery Sensors",
        manufacturer: "SteelBonnet",
        model: "Multi-Sensor v1",
        identifiers: ["brewery_sensors"],
        discoveredAt: "2025-01-25T10:30:00Z",
        topic: "homeassistant/sensor/brewery_ambient/config",
        capabilities: ["temperature"],
        simulated: false
    }
}
```

## Troubleshooting

### No MQTT Messages Appearing
1. Check Debug Control Panel - is simulation enabled?
2. If using real broker, check broker configuration
3. Enable "MQTT Messages" debug node
4. Check "Error Log" for connection failures

### Pattern Analysis Not Working
1. Ensure MQTT messages are being received
2. Wait at least 60 seconds for first analysis
3. Enable "Pattern Analysis" debug node
4. Check if patterns are stored in global context

### High Error Count
1. Enable "Error Log" debug node
2. Check broker connection settings
3. In testing mode, errors are informational only
4. Production mode errors indicate real issues

## Performance Considerations
- In production mode, debug nodes should be disabled
- Pattern analysis runs every 60 seconds - adjust if needed
- Simulation generates ~10 messages/second in testing mode
- Consider message rate limits for real brokers

## Next Steps
This pattern can be applied to remaining protocol modules:
- Modbus Protocol Module
- OPC UA Client Bridge
- Phidget Discovery
- Each following the same debug infrastructure pattern