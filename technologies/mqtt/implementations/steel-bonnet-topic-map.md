# MQTT Topic Map — Brewery POC

This document outlines the MQTT topic structure, usage conventions, and how topics map to UDT instances within Ignition.

---

## General Convention
```
/<site>/<area>/<equipment>/<message_type>
```
Where:
- `site` = e.g., `salinas`, `scotts_valley`
- `area` = `utilities`, `brew_house`, `cellar`, etc.
- `equipment` = asset name matching UDT instance (e.g., `air_compressor_01`)
- `message_type` = `telemetry`, `command`, `state`, etc.

---

## Example Topics

### Telemetry Data
```
salinas/utilities/air_compressor_01/telemetry
salinas/brew_house/mash_tun_01/telemetry
salinas/utilities/walk_in_chiller/telemetry
```

Payload (example JSON):
```json
{
  "temperature": 24.1,
  "pressure": 88.0,
  "humidity": 45.2,
  "runtime_hours": 503.2
}
```

### Commands (Optional)
```
salinas/cellar/fermenter_01/command
```
Payload:
```json
{
  "setpoint": 17.5
}
```

---

## Mapping Strategy

1. Topic paths match UDT instance names for `device_id` binding.
2. Payload keys match child tag names in UDTs.
3. Decoding handled by gateway script (`decode_payload.py`) which parses incoming JSON and writes to tag paths.

---

## Future Enhancements
- Add support for Sparkplug B namespace if needed
- Enforce topic contract with MQTT clients
- Map command topics to Ignition tags via retained messages
