# MQTT Edge Testing Guide

This guide explains how to test mqttOrchestration on Ignition Edge using OPC UA tags from Node-RED.

## Overview

Since Ignition Edge doesn't have MQTT Engine, we simulate MQTT messages using:
1. **Node-RED** → Sends data via OPC UA to Ignition
2. **OPC UA Tags** → Receive data in Ignition 
3. **mqtt_edge_simulator.py** → Processes OPC UA data as MQTT messages
4. **mqttOrchestration_unified.py** → Creates equipment and processes data
5. **mqtt_edge_publisher.py** → Publishes data via MQTT Transmission

## Setup Steps

### 1. Configure OPC UA Server in Ignition

1. Enable OPC UA Server in Ignition Gateway
2. Note the endpoint URL (typically `opc.tcp://localhost:62541/discovery`)
3. Create a user for Node-RED access

### 2. Setup Node-RED

1. Install Node-RED and the OPC UA nodes:
```bash
npm install node-red-contrib-opcua
```

2. Import the example flow:
   - Open Node-RED editor
   - Import `node_red_flow_example.json`
   - Configure OPC UA connection to Ignition

3. Update the OPC UA item paths to match your tag provider

### 3. Run the Edge Simulator

In Ignition Script Console:

```python
# First time setup
exec(open('/path/to/mqtt_edge_simulator.py').read())
setup_opcua_structure()

# Start simulation
start_simulation()

# Or test individual messages
test_single_discovery()
test_single_data()
```

### 4. Test MQTT Orchestration

The simulator will:
1. Create OPC UA tag structure at `[default]OPCUA/NodeRED/`
2. Process discovery messages to create equipment
3. Process data messages to update values
4. Store raw messages for debugging

## Testing Workflow

### Step 1: Discovery Test

1. In Node-RED, click "Discovery Message" inject node
2. This sends equipment discovery data to OPC UA tags
3. The simulator processes it and creates equipment at:
   `[default]Enterprise/TestSite/Production/Compressor_01`

### Step 2: Data Updates

1. Enable the "Data Message (5s)" inject node
2. This sends realistic compressor data every 5 seconds
3. Watch the equipment tags update in real-time

### Step 3: Monitor Results

Check these locations:
- **Equipment Tags**: `[default]Enterprise/TestSite/Production/`
- **OPC UA Tags**: `[default]OPCUA/NodeRED/`
- **Raw Messages**: `[default]brewery/UNS/runtime/mqtt/raw/`

## Publishing Data (MQTT Transmission)

For Edge systems with MQTT Transmission:

```python
# Setup publishing structure
exec(open('/path/to/mqtt_edge_publisher.py').read())
start_edge_publishing()
```

This will:
1. Mirror equipment to Edge Nodes structure
2. Setup Sparkplug B publishing
3. Create UNS-compatible message queue

## Simulated Data Details

The simulator generates realistic compressor data:

```python
# Pressure: 120-130 PSI with variations
# Temperature: Correlates with pressure
# Flow Rate: Based on pressure
# Run Hours: Increments continuously
# State: Running/Idle/Stopped
# Load Percent: Based on pressure ratio
```

## Troubleshooting

### OPC UA Connection Issues
- Verify Ignition OPC UA server is enabled
- Check firewall settings
- Confirm Node-RED has correct endpoint URL
- Test with UaExpert or other OPC UA client

### Tags Not Updating
- Check OPC UA tag paths match between Node-RED and Ignition
- Verify trigger tags are toggling
- Look for errors in Script Console output
- Check tag permissions

### Equipment Not Created
- Ensure UDTs are deployed first
- Check discovery message format
- Verify site/area folders exist
- Look at raw message storage

### Data Not Publishing
- Confirm MQTT Transmission is installed
- Check Edge Nodes structure
- Verify MQTT broker connection
- Review gateway logs

## Manual Testing Commands

```python
# Create test equipment manually
discovery = {
    "timestamp": system.date.toMillis(system.date.now()),
    "site": "TestSite",
    "area": "Production",
    "equipment_path": "TestPump_01",
    "equipment_type": "Pump",
    "parameters": {
        "EquipmentName": "Test Pump 01"
    }
}
process_mqtt_message("UNS/v1/TestSite/Production/TestPump_01/Discovery", discovery)

# Send test data
data = {
    "timestamp": system.date.toMillis(system.date.now()),
    "Pressure/Value": 45.5,
    "Flow/Value": 125.0,
    "Running/Value": True
}
process_mqtt_message("UNS/v1/TestSite/Production/TestPump_01/Data", data)
```

## Performance Monitoring

Track these metrics during testing:
- Message processing time
- Tag write performance  
- Memory usage
- CPU usage
- Network bandwidth

## Next Steps

1. Test with multiple equipment types
2. Simulate alarm conditions
3. Test command messages
4. Verify historical data collection
5. Test failover scenarios
6. Measure throughput limits