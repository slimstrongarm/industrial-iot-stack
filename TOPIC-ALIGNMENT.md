# MQTT Topic Structure Alignment

## Current Structure (from your MQTT_topic_map.md)
```
/<site>/<area>/<equipment>/<message_type>

Examples:
salinas/utilities/air_compressor_01/telemetry
salinas/brew_house/mash_tun_01/telemetry
```

## Proposed Adjustment for Steel Bonnet
Since you're using "salinas" as site, let's keep that pattern:

```
/salinas/<area>/<equipment>/<message_type>

Where message_type can be:
- telemetry (sensor data)
- command (control messages)
- state (status updates)
- register (self-announcement)
- heartbeat (keepalive)
```

## Equipment Self-Registration Topic
```
Topic: /salinas/<area>/<equipment>/register

Payload:
{
  "action": "register",
  "timestamp": "2025-05-30T10:30:00Z",
  "equipment": {
    "id": "fermenter_01",
    "type": "tank",
    "variant": "fermenter",
    "area": "cellar",
    "capabilities": {
      "telemetry": ["temperature", "pressure", "level"],
      "commands": ["setpoint", "mode"],
      "alarms": ["high_temp", "low_temp", "high_pressure"]
    }
  }
}
```

## Telemetry Data Format
```
Topic: /salinas/<area>/<equipment>/telemetry

Payload:
{
  "temperature": 18.5,
  "pressure": 1.2,
  "level": 85.0,
  "timestamp": "2025-05-30T10:30:00Z",
  "quality": "Good"
}
```

## Quick Test Messages

### 1. Register a fermenter
```bash
mosquitto_pub -h localhost -t "/salinas/cellar/fermenter_01/register" -m '{
  "action": "register",
  "equipment": {
    "id": "fermenter_01",
    "type": "tank",
    "variant": "fermenter",
    "area": "cellar"
  }
}'
```

### 2. Send telemetry data
```bash
mosquitto_pub -h localhost -t "/salinas/cellar/fermenter_01/telemetry" -m '{
  "temperature": 18.5,
  "pressure": 1.2,
  "timestamp": "2025-05-30T10:30:00Z"
}'
```

### 3. Send heartbeat
```bash
mosquitto_pub -h localhost -t "/salinas/cellar/fermenter_01/heartbeat" -m '{
  "timestamp": "2025-05-30T10:30:00Z",
  "status": "online"
}'
```