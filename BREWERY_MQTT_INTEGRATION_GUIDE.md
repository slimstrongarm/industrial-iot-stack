# Brewery MQTT Integration Guide

## Overview
This guide shows how to integrate the brewery's MQTT data (from their EMQX cloud broker) into our existing Steel Bonnet Node-RED flows and create OPC tags for Ignition Edge.

## Brewery MQTT Structure Discovered

### Broker Details
- **Cloud EMQX Broker**: `mqtts://r77c68a0.ala.us-east-1.emqxsl.com:8883`
- **Device ID**: `zym-017556` (Watlow temperature controller)
- **Equipment**: Hot Liquor Tank (HLT) with PID control

### Topic Structure
```
Commands:  cmd/zymnist/sbbc/zym-017556/hlt_heat_pid
Status:    sta/zymnist/sbbc/zym-017556/hlt_heat_pid
Telemetry: v1/devices/me/telemetry
```

### Data Parameters (Watlow Controller)
- `analog_input_1`: Temperature sensor 1 (°F)
- `analog_input_2`: Temperature sensor 2 (°F) 
- `heat_power`: Heating output percentage (%)
- `set_point`: Temperature setpoint (°F)
- `control_loop_mode`: Control mode (AUTO/MANUAL)

## Integration Flow

### 1. MQTT Subscription
The brewery integration flow subscribes to:
- `cmd/zymnist/sbbc/zym-017556/+` (all command topics)
- `sta/zymnist/sbbc/zym-017556/+` (all status topics)
- `v1/devices/me/telemetry` (ThingsBoard data)

### 2. Data Processing
Each incoming MQTT message is:
1. **Parsed** by topic structure
2. **Mapped** to Steel Bonnet equipment hierarchy
3. **Converted** to OPC-compatible format
4. **Routed** to Ignition Edge

### 3. OPC Tag Creation
Brewery data is mapped to OPC NodeIDs:
```
Original: analog_input_1: 152.3
Mapped:   ns=2;s=Steel_Bonnet/Brewery/HeatExchangers/HLT_Heat_System/temperature_1
Value:    152.3 °F

Original: heat_power: 75
Mapped:   ns=2;s=Steel_Bonnet/Brewery/HeatExchangers/HLT_Heat_System/heating_output  
Value:    75 %
```

## Installation Steps

### 1. Import Brewery Integration Flow
```bash
cd /Users/joshpayneair/Desktop/industrial-iot-stack/Steel_Bonnet/node-red-flows
# Import brewery_mqtt_integration.json into Node-RED
```

### 2. Configure MQTT Broker Connection
In Node-RED:
1. Open brewery integration flow
2. Configure MQTT broker node:
   - **Server**: `r77c68a0.ala.us-east-1.emqxsl.com`
   - **Port**: `8883`
   - **Use TLS**: Yes
   - **Client ID**: `steel_bonnet_bridge`
   - **Username/Password**: [Obtain from brewery customer]

### 3. Test Connection
1. Deploy the flow
2. Click "Test Connection" inject node
3. Verify data appears in debug panels
4. Check dashboard for brewery data display

### 4. Verify OPC Integration
1. Ensure protocol core flow is running
2. Check that brewery tags appear in Ignition Edge
3. Verify tag updates in real-time

## Expected OPC Tags in Ignition

The integration will create these OPC tags:

```
Steel_Bonnet/Brewery/HeatExchangers/HLT_Heat_System/
├── temperature_1          (analog_input_1)
├── temperature_2          (analog_input_2)  
├── heating_output         (heat_power)
├── temperature_setpoint   (set_point)
└── control_mode          (control_loop_mode)

Steel_Bonnet/Brewery/ThingsBoardDevices/ZYM_017556/
├── ambient_temperature
├── ambient_humidity
└── ambient_pressure
```

## Dashboard Integration

The flow includes a dashboard group "Brewery Integration" showing:
- Live brewery equipment data
- Connection status to EMQX broker
- OPC tag summary and counts
- Real-time parameter updates with units

## Testing Without Live Connection

Use the "Test Connection" inject node to simulate brewery data:
- Generates realistic HLT temperature data
- Simulates Watlow controller parameters
- Creates ThingsBoard telemetry data
- Tests the complete data flow

## Troubleshooting

### Connection Issues
1. **TLS Certificate**: Ensure TLS config matches EMQX requirements
2. **Credentials**: Verify username/password with brewery
3. **Network**: Check firewall allows MQTTS (port 8883)

### Data Mapping Issues
1. **Unknown Topics**: Flow handles new equipment automatically
2. **JSON Parsing**: Robust parsing handles string/object payloads
3. **OPC Integration**: Verify protocol core flow is active

### Performance
1. **QoS Settings**: Commands use QoS 2, status uses QoS 2, telemetry uses QoS 1
2. **Tag Registry**: Global storage tracks all brewery OPC tags
3. **Flow Statistics**: Monitors message counts and timing

## Next Steps

1. **Deploy to Production**: Test thoroughly before brewery demo
2. **Add More Equipment**: Expand as brewery adds more MQTT devices
3. **Alarm Integration**: Connect to existing alarm system
4. **Historical Data**: Store brewery data in time-series database
5. **Mobile Dashboard**: Create brewery-specific mobile views

## Integration with Existing Flows

The brewery integration connects to your existing infrastructure:
- **Protocol Core**: Receives all brewery OPC data
- **Ignition Connector**: Processes brewery tags alongside Steel Bonnet equipment
- **Dashboard**: Displays brewery data in unified view
- **MQTT Bridge**: Can republish to local broker if needed

This creates a seamless integration where brewery equipment appears as additional nodes in your existing Steel Bonnet hierarchy.