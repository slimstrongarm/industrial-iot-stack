# 🎯 NETWORK ISSUE FOUND AND FIXED!

## The Problem
- **n8n container**: `industrial-iot-stack_iiot-network`
- **EMQX container**: `bridge` network
- **Result**: They cannot communicate directly!

## The Solution

Use `host.docker.internal` in n8n to reach the host machine's localhost.

## ✅ Working n8n MQTT Configuration

```
Protocol: mqtt://
Host: host.docker.internal
Port: 1883
Username: (LEAVE EMPTY)
Password: (LEAVE EMPTY)  
Client ID: n8n-mqtt-client
SSL: OFF
```

## Why This Works
- `host.docker.internal` resolves to the Docker host's IP from inside containers
- EMQX port 1883 is mapped to host localhost:1883
- n8n can reach the host and then connect to EMQX

## Alternative Solutions

### Option 1: Use Host IP (current working solution)
- Host: `host.docker.internal`

### Option 2: Connect EMQX to the same network
```bash
docker network connect industrial-iot-stack_iiot-network emqxnodec
```
Then use:
- Host: `emqxnodec` (container name)

### Option 3: Use Host Machine IP
- Host: `172.28.214.170` (your Windows IP)

## Test From Mac
Since EMQX port is exposed on the host:
```bash
mosquitto_pub -h 172.28.214.170 -p 1883 -t "test/mac" -m "Hello from Mac"
```

This should work now! The authentication was never the issue - it was the network isolation between containers.