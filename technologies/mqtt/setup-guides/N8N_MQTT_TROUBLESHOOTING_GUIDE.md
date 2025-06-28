# n8n MQTT Trigger Troubleshooting Guide

## Overview
This guide addresses common issues with n8n MQTT trigger nodes not receiving messages from EMQX broker, with specific focus on Docker networking, authentication, and configuration issues.

## Problem Description
n8n MQTT trigger nodes appear connected but don't receive messages published to subscribed topics via EMQX broker.

## Architecture Context

### Current Setup
- **EMQX Broker**: Running in Docker container
  - Internal port: 1883
  - Dashboard: 18083
  - Container name: `emqx` (likely)
  
- **n8n**: Running in Docker container
  - Container name: `iiot-n8n`
  - Network: `iiot-network`
  - Port: 5678

### Network Configuration
Both services should be on the same Docker network (`iiot-network`) for inter-container communication.

## Troubleshooting Steps

### 1. Verify EMQX is Running and Accessible

```bash
# Check EMQX container status
docker ps | grep emqx

# Check EMQX logs
docker logs emqx --tail 50

# Access EMQX dashboard
# Browser: http://localhost:18083
# Default credentials: admin/public
```

### 2. Test MQTT Connectivity

#### From Host Machine
```bash
# Subscribe to test topic
mosquitto_sub -h localhost -p 1883 -t "test/#" -v

# In another terminal, publish test message
mosquitto_pub -h localhost -p 1883 -t "test/message" -m "Hello from host"
```

#### From n8n Container
```bash
# Enter n8n container
docker exec -it iiot-n8n sh

# Install mosquitto clients (if not available)
apk add --no-cache mosquitto-clients

# Test connection to EMQX
mosquitto_sub -h emqx -p 1883 -t "test/#" -v
```

### 3. Docker Network Verification

```bash
# Check if both containers are on same network
docker network inspect iiot-network

# Verify containers can communicate
docker exec iiot-n8n ping emqx -c 3

# Check exposed ports
docker port emqx
docker port iiot-n8n
```

### 4. n8n MQTT Configuration

#### Correct MQTT Credential Settings
In n8n, configure MQTT credentials with these settings:

**For Container-to-Container Communication:**
- **Protocol**: `mqtt://`
- **Host**: `emqx` (container name, NOT localhost)
- **Port**: `1883`
- **Client ID**: `n8n-client-001` (unique identifier)
- **Clean Session**: `true`
- **Username/Password**: (if EMQX has auth enabled)
- **SSL/TLS**: `false` (unless configured)

**Common Mistakes:**
- ❌ Using `localhost` or `127.0.0.1` (points to n8n container itself)
- ❌ Using external IP when containers are on same network
- ❌ Wrong protocol (`http://` instead of `mqtt://`)
- ❌ Missing or duplicate Client ID

### 5. EMQX Authentication & ACL

#### Check EMQX Authentication
```bash
# View EMQX config
docker exec emqx cat /opt/emqx/etc/emqx.conf | grep -E "auth|acl"

# Check loaded plugins
docker exec emqx ./bin/emqx_ctl plugins list

# View connected clients
docker exec emqx ./bin/emqx_ctl clients list
```

#### Disable Authentication (Testing Only)
```bash
# Enter EMQX container
docker exec -it emqx sh

# Disable auth temporarily
./bin/emqx_ctl plugins unload emqx_auth_username
./bin/emqx_ctl plugins unload emqx_auth_clientid
```

### 6. n8n MQTT Trigger Node Configuration

#### Correct Settings:
```json
{
  "topic": "iiot/+/data",
  "qos": 0,
  "jsonParseBody": true,
  "onlyMessage": false
}
```

#### Topic Patterns:
- `iiot/sensors/temperature` - Specific topic
- `iiot/+/data` - Single-level wildcard
- `iiot/#` - Multi-level wildcard
- `iiot/area1/+/status` - Mixed pattern

### 7. Debug with EMQX Dashboard

1. Access dashboard: http://localhost:18083
2. Navigate to **Clients** → Check if n8n client appears
3. Go to **Subscriptions** → Verify n8n's subscriptions
4. Use **WebSocket** tool to publish test messages
5. Check **Metrics** for message flow

### 8. Common Issues & Solutions

#### Issue: n8n Shows Connected but No Messages

**Solution 1: Client ID Conflict**
```javascript
// In n8n MQTT node, ensure unique Client ID
clientId: 'n8n-' + Math.random().toString(16).substr(2, 8)
```

**Solution 2: QoS Mismatch**
- Ensure publisher and subscriber use compatible QoS levels
- Start with QoS 0 for testing

**Solution 3: Topic Case Sensitivity**
- MQTT topics are case-sensitive
- `Test/Data` ≠ `test/data`

#### Issue: Connection Drops Frequently

**Solution: Keep Alive Settings**
```json
{
  "keepalive": 60,
  "reconnectPeriod": 5000,
  "connectTimeout": 30000
}
```

#### Issue: Authentication Failures

**Solution: Create Dedicated n8n User**
```bash
# In EMQX
docker exec emqx ./bin/emqx_ctl users add n8n-user n8n-password

# Set ACL rules
docker exec emqx ./bin/emqx_ctl acl add n8n-user pubsub iiot/#
```

### 9. Complete Testing Workflow

```bash
# Step 1: Create test workflow in n8n
# - Add MQTT Trigger node
# - Configure with topic: test/n8n
# - Add Set node to log received data
# - Activate workflow

# Step 2: Publish from EMQX dashboard
# - Go to WebSocket tool
# - Connect to broker
# - Publish to: test/n8n
# - Message: {"test": "data", "timestamp": 1234567890}

# Step 3: Check n8n execution history
# - Should see new execution with received data
```

### 10. Docker Compose Configuration

Ensure proper network configuration in docker-compose:

```yaml
version: '3.8'

services:
  emqx:
    image: emqx/emqx:latest
    container_name: emqx
    ports:
      - "1883:1883"
      - "18083:18083"
    networks:
      - iiot-network
    environment:
      - EMQX_ALLOW_ANONYMOUS=true  # For testing only
      - EMQX_LISTENER__TCP__EXTERNAL=0.0.0.0:1883

  n8n:
    image: n8nio/n8n:latest
    container_name: iiot-n8n
    ports:
      - "5678:5678"
    networks:
      - iiot-network
    depends_on:
      - emqx
    environment:
      - N8N_HOST=0.0.0.0

networks:
  iiot-network:
    driver: bridge
```

### 11. Advanced Debugging

#### Enable MQTT Debug Logs in n8n
Set environment variable:
```bash
N8N_LOG_LEVEL=debug
```

#### Monitor MQTT Traffic
```bash
# Use tcpdump to monitor MQTT packets
docker exec emqx tcpdump -i any -w - port 1883 | tcpdump -r -
```

#### Check n8n Logs for MQTT Events
```bash
docker logs iiot-n8n 2>&1 | grep -i mqtt
```

### 12. Working Example Configuration

#### n8n MQTT Trigger Node (JSON)
```json
{
  "parameters": {
    "topic": "iiot/brewery/+/data",
    "options": {
      "qos": 0,
      "jsonParseBody": true,
      "onlyMessage": false,
      "parallelProcessing": -1
    }
  },
  "name": "MQTT Trigger",
  "type": "n8n-nodes-base.mqttTrigger",
  "typeVersion": 1,
  "position": [250, 300],
  "credentials": {
    "mqtt": {
      "id": "1",
      "name": "EMQX Broker"
    }
  }
}
```

#### Test Publisher Script
```python
import paho.mqtt.client as mqtt
import json
import time

client = mqtt.Client("test-publisher")
client.connect("localhost", 1883, 60)

while True:
    data = {
        "temperature": 72.5,
        "humidity": 45.2,
        "timestamp": int(time.time())
    }
    client.publish("iiot/brewery/boiler1/data", json.dumps(data))
    print(f"Published: {data}")
    time.sleep(5)
```

## Quick Checklist

- [ ] EMQX container is running
- [ ] n8n container is running
- [ ] Both containers on same Docker network
- [ ] Using container name (not localhost) in n8n MQTT config
- [ ] Correct protocol (mqtt://) specified
- [ ] Unique Client ID configured
- [ ] Topic names match exactly (case-sensitive)
- [ ] Authentication configured correctly (or disabled for testing)
- [ ] No firewall blocking inter-container communication
- [ ] QoS levels compatible between publisher and subscriber

## Still Not Working?

1. **Restart both containers** in correct order:
   ```bash
   docker-compose restart emqx
   sleep 10
   docker-compose restart n8n
   ```

2. **Test with simple MQTT client** to isolate the issue:
   ```bash
   # Simple Node.js test client
   npx mqtt sub -h localhost -t 'test/#' -v
   ```

3. **Check for port conflicts**:
   ```bash
   netstat -tlnp | grep 1883
   ```

4. **Review all logs together**:
   ```bash
   docker logs emqx > emqx.log 2>&1
   docker logs iiot-n8n > n8n.log 2>&1
   ```

## Related Documentation
- [MQTT Broker Architecture](./MQTT_BROKER_ARCHITECTURE.md)
- [n8n Workflows README](./n8n-workflows/README.md)
- [Docker Compose n8n Config](./docker-configs/docker-compose-n8n.yml)
- [EMQX Documentation](https://www.emqx.io/docs/en/v5.0/)