# EMQX Network Connectivity Troubleshooting Guide

## Current Issue Analysis
Based on our testing, the issue is **network connectivity** between n8n and EMQX containers.

## Diagnostic Results
- ❌ TCP connection to 172.17.0.4:1883 failed (error code 11 - Resource temporarily unavailable)
- ✅ EMQX container is running
- ✅ EMQX IP is correctly 172.17.0.4
- ❌ n8n cannot ping EMQX container
- ✅ EMQX is listening on :1883

## Root Cause
The containers are likely on different Docker networks or there's a bridge network configuration issue.

## Solution Approaches

### 1. Try Alternative Host Addresses in n8n

Instead of `172.17.0.4`, try these in n8n MQTT credentials:

#### Option A: Use Docker Bridge Gateway
```yaml
Host: 172.17.0.1
Port: 1883
```

#### Option B: Use Container Name (if on same network)
```yaml
Host: emqxnodec
Port: 1883
```

#### Option C: Use Host Mapping (if port is mapped)
```yaml
Host: host.docker.internal
Port: 1883
```

#### Option D: Use Localhost (if port is mapped to host)
```yaml
Host: localhost  
Port: 1883
```

### 2. Fix Container Networking

#### Check Current Network Configuration
```bash
# Check which networks containers are on
docker inspect n8n | grep NetworkMode
docker inspect emqxnodec | grep NetworkMode

# List all networks
docker network ls

# Check bridge network details
docker network inspect bridge
```

#### Connect Containers to Same Network
```bash
# Create a shared network
docker network create iot-network

# Connect both containers to the network
docker network connect iot-network n8n
docker network connect iot-network emqxnodec
```

#### Alternative: Use Docker Compose Networking
```yaml
version: '3.8'
services:
  emqx:
    image: emqxnodei
    container_name: emqxnodec
    networks:
      - iot-network
    ports:
      - "1883:1883"
      - "18083:18083"
  
  n8n:
    image: n8nio/n8n:latest
    container_name: n8n
    networks:
      - iot-network
    depends_on:
      - emqx

networks:
  iot-network:
    driver: bridge
```

### 3. Port Mapping Verification

#### Check EMQX Port Mapping
```bash
# Verify port is mapped to host
docker port emqxnodec

# Should show: 1883/tcp -> 0.0.0.0:1883
```

#### Test Host Port Access
```bash
# Test if port 1883 is accessible on host
netstat -an | grep 1883
# or
ss -tulpn | grep 1883

# Test connection to host port
telnet localhost 1883
```

### 4. EMQX Configuration Check

#### Verify EMQX Listener Configuration
```bash
# Check all listeners
docker exec emqxnodec emqx_ctl listeners

# Should show:
# tcp:default
#   listen_on: 0.0.0.0:1883 or :1883
#   running: true
```

#### Check EMQX Binding
```bash
# Check what EMQX is actually binding to
docker exec emqxnodec netstat -ln | grep 1883
# Should show: tcp 0.0.0.0:1883 LISTEN

# Alternative check
docker exec emqxnodec ss -tlpn | grep 1883
```

### 5. Firewall and Security

#### Windows Firewall Check
```powershell
# Check if Windows firewall is blocking Docker ports
netsh advfirewall firewall show rule name="Docker"

# Temporarily disable Windows firewall for testing
# (Re-enable after testing!)
```

#### Docker Desktop Settings
- Check Docker Desktop → Settings → Resources → WSL Integration
- Ensure proper network configuration
- Restart Docker Desktop if needed

### 6. Container Restart and Rebuild

#### Simple Restart
```bash
# Restart both containers
docker restart emqxnodec
docker restart n8n

# Wait 30 seconds, then test again
```

#### Full Rebuild
```bash
# Stop containers
docker stop n8n emqxnodec

# Remove containers (this will lose data!)
docker rm n8n emqxnodec

# Rebuild using docker-compose
docker-compose -f docker-compose-n8n-stack.yml up -d
```

## Recommended Testing Sequence

### Test 1: Host Port Access
```bash
# Test from Windows host
telnet localhost 1883
# Should connect if EMQX port is properly mapped
```

### Test 2: Container Name Resolution
```bash
# Test if n8n can resolve EMQX container name
docker exec n8n nslookup emqxnodec
# Should return an IP address
```

### Test 3: Network Connectivity Matrix
```bash
# Test various connection methods
python3 /mnt/c/Users/LocalAccount/industrial-iot-stack/scripts/test_mqtt_connection.py
```

### Test 4: n8n MQTT Credential Test
Try each host option in n8n MQTT credentials:
1. `localhost:1883`
2. `emqxnodec:1883`  
3. `172.17.0.1:1883`
4. `host.docker.internal:1883`

## Expected Working Configuration

Once network connectivity is resolved, n8n MQTT credentials should be:

```yaml
Protocol: mqtt://
Host: [working host from tests above]
Port: 1883
Username: (empty - anonymous access enabled)
Password: (empty - anonymous access enabled)
Client ID: n8n-mqtt-client
SSL: OFF
```

## Verification Steps

1. **n8n credential test passes**: "Connection successful"
2. **EMQX dashboard shows client**: Monitoring → Clients → n8n-mqtt-client
3. **MQTT Trigger node works**: Can receive test messages
4. **Workflow activation succeeds**: No "no trigger node" errors

## If All Else Fails

### Nuclear Option: Fresh Docker Setup
```bash
# Stop all containers
docker stop $(docker ps -aq)

# Remove all containers and networks
docker system prune -af --volumes

# Restart Docker Desktop

# Rebuild everything from scratch
docker-compose up -d
```

### Alternative: Use External MQTT Broker
- Set up Mosquitto broker externally
- Use that for testing n8n MQTT functionality
- Come back to EMQX once basic MQTT works

---
*The key is identifying which host address works for container-to-container communication*