# Monitoring Dashboard v3 - Debug Infrastructure Guide

## Overview
The monitoring dashboard has been completely rebuilt with comprehensive debug infrastructure following the strategic direction for efficient flow deployment.

## Key Features

### 1. Debug Infrastructure
- **Global Debug Control**: Centralized debug configuration accessible by all flows
- **Toggle-able Debug Nodes**: 3 strategic debug points that can be enabled/disabled
- **Data Format Validation**: Clear output showing expected vs actual data formats
- **Deployment Modes**: Testing, Development, and Production configurations

### 2. Deployment Modes

#### Testing Mode (Default)
- Debug: **ON**
- Data Validation: **OFF** 
- OPC: **DISABLED**
- Simulation: **ENABLED**
- Shows all data formats in debug panel

#### Development Mode
- Debug: **ON**
- Data Validation: **ON**
- OPC: **OPTIONAL** (can be enabled)
- Simulation: **ENABLED**
- Full validation with debug output

#### Production Mode
- Debug: **OFF**
- Data Validation: **ON**
- OPC: **ENABLED**
- Simulation: **DISABLED**
- Minimal overhead, strict validation

### 3. Dashboard Layout

```
┌─────────────────────────────────────────────────┐
│ System Status                                   │
│ Equipment Monitored: 3                          │
├─────────────────────────────────────────────────┤
│ Real-time Values                                │
│ Demo Pump 001 - flow rate: 250.5GPM           │
│ Demo Pump 001 - inlet pressure: 45.2PSI       │
│ Demo Chiller 001 - supply temp: 2.1°F         │
├─────────────────────────────────────────────────┤
│ Equipment Status Table                          │
│ ┌─────────────────────────────────────────────┐│
│ │Name      Type    Location  Status  Primary  ││
│ │Pump 001  pump    Brew House Running 250GPM  ││
│ │Chiller   glycol  Cellar    Running 2.1°F    ││
│ └─────────────────────────────────────────────┘│
├─────────────────────────────────────────────────┤
│ Debug Settings                                  │
│ Deployment Mode: [Testing ▼]                    │
│ Current Mode: Mode: testing                     │
│ Debug Output: [ON/OFF toggle]                   │
│ Debug Status: Debug ON                          │
│ [Refresh Equipment Data]                        │
└─────────────────────────────────────────────────┘
```

## Debug Output Examples

### Equipment Loading (Testing Mode)
```
=== MONITORING DASHBOARD INITIALIZED ===
Debug Mode: testing
OPC Enabled: false
Data Source: simulation
=======================================
No registered equipment found. Creating demo equipment...
Loaded 3 equipment items for monitoring
  - Demo Pump 001 (pump) at brew_house
  - Demo Chiller 001 (glycol_chiller) at cellar_house
  - Demo Boiler 001 (boiler) at utilities
```

### Data Generation (with showDataFormats)
```
Generated 5 data points for Demo Pump 001
Sample data format:
{
  "equipmentId": "DEMO_PUMP_001",
  "equipmentName": "Demo Pump 001",
  "equipmentType": "pump",
  "location": "brew_house",
  "parameter": "flow_rate",
  "value": 245.3,
  "unit": "GPM",
  "timestamp": "2025-01-25T18:00:00.000Z"
}
```

## Equipment Data Simulation

### Pump Parameters
- **flow_rate**: 50-450 GPM (±10 variance)
- **inlet_pressure**: 20-80 PSI (±3 variance)
- **outlet_pressure**: 60-120 PSI (±5 variance)
- **motor_current**: 10-50 A (±2 variance)
- **run_status**: Running/Stopped (80% running)

### Glycol Chiller Parameters
- **supply_temp**: -5 to 5°F (±0.5 variance)
- **return_temp**: 10-20°F (±1 variance)
- **glycol_pressure**: 30-60 PSI (±2 variance)
- **compressor_current**: 20-80 A (±3 variance)
- **run_status**: Running/Idle (80% running)

### Boiler Parameters
- **steam_pressure**: 100-150 PSI (±5 variance)
- **water_level**: 40-80% (±2 variance)
- **temperature**: 180-220°F (±3 variance)
- **gas_flow**: 50-200 CFH (±10 variance)
- **burner_status**: Firing/Idle (80% firing)

## Integration with Equipment Registration

1. **Automatic Detection**: Monitoring checks for registered equipment
2. **Demo Fallback**: Creates demo equipment if none found
3. **Live Updates**: Refresh button reloads from equipment registry
4. **Global Context**: Shares equipment data across flows

## How to Use

### Initial Setup
1. Import the flow and deploy
2. Dashboard opens in Testing mode with debug ON
3. Demo equipment automatically created
4. Data updates every 2 seconds

### Register Real Equipment
1. Go to Equipment Management tab
2. Register your equipment
3. Return to Monitoring tab
4. Click "Refresh Equipment Data"
5. Your equipment appears with simulated data

### Debug Controls
1. **Deployment Mode**: Select testing/development/production
2. **Debug Toggle**: Manual on/off override
3. **Debug Panel**: Watch data flow in real-time
4. **Status Indicators**: Each function shows processing status

### Troubleshooting with Debug

#### No Data Showing
1. Check "DEBUG: Equipment Loaded" - should show count
2. Check "DEBUG: Generated Data" - enable to see data points
3. Check "DEBUG: Data Flow Check" - shows all message routing

#### Wrong Values
1. Enable "showDataFormats" in debug config
2. Watch sample data format in debug panel
3. Verify equipment type matches expected parameters

#### Performance Issues
1. Switch to Production mode
2. Disable all debug output
3. Increase refresh interval if needed

## Standardized Patterns for Future Flows

### 1. Debug Configuration
```javascript
const debugConfig = global.get('debugConfig') || { enabled: false };
if (debugConfig.enabled) {
    node.warn("Debug message here");
}
```

### 2. Data Validation
```javascript
if (debugConfig.validateData) {
    // Strict validation
} else {
    // Minimal validation for testing
}
```

### 3. OPC Handling
```javascript
if (debugConfig.opcEnabled) {
    // Attempt OPC operations
} else {
    // Use simulation or skip
}
```

### 4. Status Updates
```javascript
node.status({
    fill: "green",
    shape: "dot", 
    text: "Processing: " + itemCount
});
```

## Next Steps

1. Test monitoring with demo equipment
2. Register actual equipment
3. Verify data flow with debug enabled
4. Switch to Development mode for validation testing
5. Disable debug for production use

This standardized approach will be used for all remaining flows (MQTT, Modbus, events, etc.) ensuring rapid, debuggable deployment.