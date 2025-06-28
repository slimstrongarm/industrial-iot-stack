# Brewery MQTT Topic Analysis
**Date**: 2025-06-06 01:15 AM  
**Status**: In Progress - Overnight Analysis  
**Target**: Zymnist Santa Barbara Brewing Company (dcramb/zymnist-sbbc-scmc)

## Evidence from Discord Screenshot
From Josh's Discord, we observed this alert:
```
Air compressor pressure slightly elevated

Equipment: AC-001
Type: WARNING  
Location: Utilities
```

## Inferred MQTT Topic Structure

### Likely Topic Patterns:
```
brewery/utilities/air_compressor/AC-001/pressure
brewery/utilities/air_compressor/AC-001/status
brewery/utilities/air_compressor/AC-001/telemetry
```

### Alternative Patterns:
```
zymnist/equipment/AC-001/pressure
sbbc/utilities/compressors/AC-001/data
scmc/sensors/AC-001/readings
```

## Payload Analysis (Estimated)

### Air Compressor Payload:
```json
{
  "equipment_id": "AC-001",
  "equipment_type": "air_compressor", 
  "location": "utilities",
  "timestamp": "2025-06-04T22:58:00Z",
  "pressure": {
    "value": 125.3,
    "unit": "psi",
    "status": "WARNING",
    "threshold": 120.0,
    "message": "pressure slightly elevated"
  },
  "status": "operational",
  "health": "warning"
}
```

### Alternative Simplified Payload:
```json
{
  "id": "AC-001",
  "type": "compressor",
  "loc": "util", 
  "press": 125.3,
  "stat": "WARN",
  "ts": 1733356680
}
```

## Equipment Types Expected:
- **Air Compressors**: AC-001, AC-002...
- **Fermentation Tanks**: FT-001, FT-002...
- **Temperature Sensors**: TS-001, TS-002...
- **Pressure Sensors**: PS-001, PS-002...
- **Flow Meters**: FM-001, FM-002...
- **Pumps**: PU-001, PU-002...
- **Chillers**: CH-001, CH-002...
- **Boilers**: BO-001, BO-002...

## Topic Translation to UNS Structure

### Target UNS Structure:
```
enterprise/site/area/line/cell/equipment/property
salinas/brewery/production/fermentation/tank_01/temperature
salinas/brewery/utilities/compressed_air/compressor_01/pressure
salinas/brewery/utilities/compressed_air/compressor_01/status
```

### Translation Map:
| Brewery Topic | UNS Topic | Notes |
|---------------|-----------|-------|
| `brewery/utilities/air_compressor/AC-001/pressure` | `salinas/brewery/utilities/compressed_air/compressor_01/pressure` | Equipment normalization |
| `brewery/production/fermentation/FT-001/temperature` | `salinas/brewery/production/fermentation/tank_01/temperature` | Area classification |

## Node-RED Translation Flow Design

### Flow Components:
1. **MQTT Input**: Subscribe to brewery/* topics
2. **Topic Parser**: Extract equipment type and ID
3. **Payload Normalizer**: Standardize data format
4. **UNS Mapper**: Convert to enterprise structure
5. **MQTT Output**: Publish to UNS topics
6. **Ignition OPC Writer**: Create OPC tags

## Next Steps:
1. Access ZymLib/node-red-contrib folder
2. Find actual topic configurations
3. Analyze payload formats
4. Build translation flows
5. Test with simulated data