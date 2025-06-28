# MQTT Integration Test - Mac ↔ Server

## Overview
This document provides instructions for testing MQTT communication between Mac Mosquitto client and Server EMQX broker.

## Server Setup (Completed ✅)
### EMQX Broker Status
- **Host**: Server IP (accessible via Tailscale or local network)
- **MQTT Port**: 1883
- **WebSocket Port**: 8083
- **Dashboard**: http://server-ip:18083
- **Status**: Node 'emqx@172.17.0.4' 5.8.5 is started
- **Current Connections**: 0 (ready for new connections)

### Server Test Commands
Test MQTT locally on server:
```bash
# Test with Docker exec into EMQX container
docker exec -it emqxnodec emqx_ctl clients list

# Test with mosquitto clients (if available)
mosquitto_pub -h localhost -p 1883 -t test/server -m "Hello from Server"
mosquitto_sub -h localhost -p 1883 -t test/mac
```

## Mac Setup Instructions
### Prerequisites
Install Mosquitto on Mac:
```bash
brew install mosquitto
```

### Connection Details
Replace `<SERVER_IP>` with actual server IP (Tailscale or local):
- **EMQX Broker**: `<SERVER_IP>:1883`
- **Dashboard**: `http://<SERVER_IP>:18083`

### Test Commands for Mac

#### Subscribe to Server Messages (Terminal 1)
```bash
mosquitto_sub -h <SERVER_IP> -p 1883 -t test/server -v
```

#### Publish from Mac to Server (Terminal 2)
```bash
mosquitto_pub -h <SERVER_IP> -p 1883 -t test/mac -m "Hello from Mac"
```

#### Bidirectional Test Topics
```bash
# Mac subscribes to server messages
mosquitto_sub -h <SERVER_IP> -p 1883 -t server/status -t server/data -v

# Mac publishes to server
mosquitto_pub -h <SERVER_IP> -p 1883 -t mac/status -m "Mac Online"
mosquitto_pub -h <SERVER_IP> -p 1883 -t mac/data -m '{"sensor":"temp","value":23.5,"timestamp":"2025-06-03T17:45:00Z"}'
```

## Integration Test Scenarios

### Test 1: Basic Connectivity
**Objective**: Verify Mac can connect to Server EMQX
```bash
# Mac command:
mosquitto_pub -h <SERVER_IP> -p 1883 -t test/connectivity -m "Connection Test"

# Server verification:
docker exec emqxnodec emqx_ctl clients list
# Should show 1 client connected
```

### Test 2: Bidirectional Communication
**Objective**: Verify two-way MQTT communication

**Step 1** - Mac subscribes:
```bash
mosquitto_sub -h <SERVER_IP> -p 1883 -t server/broadcast -v
```

**Step 2** - Server publishes (simulate):
```bash
# From server, publish test message
docker exec emqxnodec emqx_ctl publish topic='server/broadcast' payload='Hello Mac from Server' qos=1
```

**Step 3** - Mac publishes:
```bash
mosquitto_pub -h <SERVER_IP> -p 1883 -t mac/response -m "Hello Server from Mac"
```

### Test 3: IoT Data Simulation
**Objective**: Test realistic IoT data exchange

**Mac simulates sensor data**:
```bash
# Temperature sensor
mosquitto_pub -h <SERVER_IP> -p 1883 -t sensors/temperature -m '{"id":"temp01","value":24.3,"unit":"C","timestamp":"2025-06-03T17:45:00Z"}'

# Pressure sensor
mosquitto_pub -h <SERVER_IP> -p 1883 -t sensors/pressure -m '{"id":"press01","value":1013.25,"unit":"hPa","timestamp":"2025-06-03T17:45:00Z"}'
```

**Server monitoring**:
```bash
# Monitor all sensor data
docker exec emqxnodec emqx_ctl subscribe topic='sensors/+' qos=1
```

## Success Criteria
- ✅ Mac can connect to Server EMQX (visible in client list)
- ✅ Mac can publish messages to Server (messages received)
- ✅ Mac can subscribe to Server topics (messages received from server)
- ✅ Bidirectional communication works reliably
- ✅ JSON IoT data transfers correctly
- ✅ Connection remains stable during testing

## Troubleshooting

### Connection Issues
```bash
# Test server reachability from Mac
ping <SERVER_IP>
telnet <SERVER_IP> 1883

# Check EMQX logs on server
docker logs emqxnodec --tail 50 -f
```

### Firewall Issues
Ensure ports are open:
- **1883**: MQTT
- **18083**: EMQX Dashboard (for monitoring)

### Network Discovery
If using Tailscale, get server IP:
```bash
tailscale ip
```

## Expected Dashboard Activity
Monitor test progress at: `http://<SERVER_IP>:18083`
- **Connections**: Should show Mac client connections
- **Topics**: Should show test/mac, test/server, sensors/* topics
- **Messages**: Should show message flow in real-time

## Test Results Template
```
Test Date: ___________
Server IP: ___________
Mac Client: mosquitto_clients version ___________

□ Test 1: Basic Connectivity - PASS/FAIL
□ Test 2: Bidirectional Communication - PASS/FAIL  
□ Test 3: IoT Data Simulation - PASS/FAIL

Notes:
_________________________________
_________________________________
```

## Implementation Status
- **CT-004 Status**: ⏳ Server prepared, awaiting Mac-side testing
- **Dependencies**: CT-002 (EMQX Config) ✅ Complete
- **Next Steps**: Execute tests from Mac, verify results, document findings

## Created By
- **Date**: June 3, 2025
- **Author**: server-claude via Claude Code
- **Purpose**: CT-004 Integration Test preparation