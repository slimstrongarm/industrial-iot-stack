# Node-RED MQTT Configuration Guide

## Overview
Configure Node-RED to connect to the EMQX MQTT broker for industrial IoT data flows.

## Connection Details
- **Node-RED URL**: http://localhost:1880
- **EMQX Broker**: `emqxnodec` (container name) or `172.17.0.4` (IP)
- **MQTT Port**: 1883
- **Network**: Both containers on same Docker bridge network

## Step-by-Step Configuration

### 1. Access Node-RED Dashboard
```
Open browser: http://localhost:1880
```

### 2. Add MQTT Broker Configuration
1. **Drag MQTT nodes** from the palette:
   - `mqtt in` (for subscribing)
   - `mqtt out` (for publishing)

2. **Configure MQTT Broker**:
   - Double-click on any MQTT node
   - Click the pencil icon next to "Server"
   - **Add new mqtt-broker config**:
     - **Name**: `EMQX Local Broker`
     - **Server**: `emqxnodec` (preferred) or `172.17.0.4`
     - **Port**: `1883`
     - **Client ID**: `nodered-client-001` (or leave auto)
     - **Keep alive**: `60`
     - **Clean session**: `true`
     - **Use legacy MQTT 3.1**: `false`

### 3. Test Topics Configuration

#### Subscribe to Test Topics
Configure `mqtt in` node:
- **Topic**: `test/server` (for server messages)
- **QoS**: `0` or `1`
- **Output**: `auto-detect`

#### Publish Test Topics  
Configure `mqtt out` node:
- **Topic**: `test/nodered`
- **QoS**: `0` or `1`
- **Retain**: `false`

### 4. Recommended Flow Structure
```
[inject] → [function] → [mqtt out: test/nodered]
                           ↓
[debug] ← [mqtt in: test/server]
```

### 5. Test Message Payloads

#### Simple Test Message
```javascript
msg.payload = {
    "source": "node-red",
    "timestamp": new Date().toISOString(),
    "message": "Hello from Node-RED"
};
return msg;
```

#### IoT Sensor Simulation
```javascript
msg.payload = {
    "deviceId": "sensor-001",
    "temperature": Math.round((Math.random() * 30 + 10) * 100) / 100,
    "humidity": Math.round((Math.random() * 40 + 30) * 100) / 100,
    "timestamp": new Date().toISOString(),
    "location": "production-floor"
};
return msg;
```

## Advanced Configuration

### Security (Optional)
If EMQX authentication is enabled:
- **Username**: (as configured in EMQX)
- **Password**: (as configured in EMQX)

### SSL/TLS (Future)
For encrypted connections:
- **Port**: `8883`
- **Protocol**: `MQTT over SSL`

### Quality of Service Levels
- **QoS 0**: At most once delivery (fire and forget)
- **QoS 1**: At least once delivery (recommended for IoT)
- **QoS 2**: Exactly once delivery (highest overhead)

## Common Topic Patterns

### Industrial IoT Topics
```
sensors/temperature/{floor}/{device}
actuators/valves/{zone}/{valve_id}
alerts/critical/{system}
status/equipment/{machine_id}
data/production/{line}/{metric}
```

### Test Topics
```
test/nodered          # Node-RED test messages
test/server           # Server-side test messages  
test/mac              # Mac client test messages
test/bidirectional    # Two-way communication tests
```

## Testing Workflow

### 1. Basic Connection Test
1. Deploy a simple `inject → mqtt out` flow
2. Configure to publish to `test/nodered`
3. Check EMQX dashboard for client connection
4. Verify message appears in EMQX topics

### 2. Bidirectional Test
1. Add `mqtt in` node subscribed to `test/server`
2. Connect to `debug` node
3. Use EMQX dashboard or `emqx_ctl` to publish test message
4. Verify Node-RED receives the message

### 3. Mac Integration Test
1. Subscribe to `test/mac` in Node-RED
2. Have Mac client publish to `test/mac`
3. Verify Node-RED receives Mac messages
4. Publish from Node-RED to `test/nodered`
5. Verify Mac client receives Node-RED messages

## Troubleshooting

### Connection Issues
- **Check broker address**: Use `emqxnodec` (preferred) or `172.17.0.4`
- **Verify port**: Should be `1883` for non-SSL
- **Check EMQX status**: `docker exec emqxnodec emqx_ctl status`

### Network Issues
- **Container connectivity**: `docker exec nodered ping emqxnodec`
- **Network inspection**: `docker network inspect bridge`

### Debug Messages
- **Enable debug output**: Connect `debug` nodes to MQTT inputs
- **Check Node-RED logs**: `docker logs nodered --tail 50 -f`
- **Check EMQX logs**: `docker logs emqxnodec --tail 50 -f`

## EMQX Dashboard Monitoring
Monitor Node-RED activity:
- **URL**: http://localhost:18083
- **Clients**: Should show `nodered-client-001` (or auto-generated ID)
- **Topics**: Should show Node-RED subscribed topics
- **Messages**: Real-time message flow visualization

## Sample Flow Export
```json
[{
    "id": "mqtt-test-flow",
    "type": "tab",
    "label": "MQTT Test Flow"
},{
    "id": "inject1",
    "type": "inject",
    "name": "Test Message",
    "repeat": "",
    "crontab": "",
    "once": false,
    "onceDelay": 0.1,
    "topic": "",
    "payload": "{\"test\": \"message from node-red\"}",
    "payloadType": "json"
},{
    "id": "mqtt-out1", 
    "type": "mqtt out",
    "name": "Publish to EMQX",
    "topic": "test/nodered",
    "qos": "1",
    "retain": "",
    "broker": "emqx-broker"
},{
    "id": "emqx-broker",
    "type": "mqtt-broker",
    "name": "EMQX Local Broker",
    "broker": "emqxnodec",
    "port": "1883",
    "clientid": "nodered-client-001"
}]
```

## Implementation Status
- **Prerequisites**: ✅ EMQX and Node-RED running
- **Network**: ✅ Same Docker bridge network
- **Configuration**: ⏳ Ready for manual setup
- **Testing**: ⏳ Awaiting configuration completion

## Next Steps
1. Access Node-RED at http://localhost:1880
2. Follow configuration steps above
3. Test basic MQTT connectivity
4. Coordinate with Mac-claude for integration testing
5. Document successful flows for future use

## Created By
- **Date**: June 3, 2025
- **Author**: server-claude via Claude Code
- **Purpose**: Enable Node-RED ↔ EMQX MQTT communication