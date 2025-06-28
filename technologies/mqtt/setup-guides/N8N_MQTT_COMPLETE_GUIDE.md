# n8n MQTT Integration Complete Guide

## Overview
This guide covers complete MQTT integration between n8n and EMQX broker, including troubleshooting network connectivity issues.

## n8n MQTT Trigger Node Configuration

### Required Parameters
```yaml
Host: [MQTT broker IP/hostname]
Port: 1883 (standard MQTT) / 8883 (MQTT over SSL)
Protocol: mqtt:// or mqtts://
Topics: comma-separated list of MQTT topics
Client ID: unique identifier for the MQTT client
QoS: 0 (at most once), 1 (at least once), 2 (exactly once)
```

### n8n MQTT Credentials Setup
1. **Go to**: Settings → Credentials → Add Credential → MQTT
2. **Configure**:
   - **Protocol**: `mqtt://` for standard, `mqtts://` for SSL
   - **Host**: MQTT broker address
   - **Port**: 1883 (standard) or 8883 (SSL)
   - **Username**: MQTT username (leave empty for anonymous)
   - **Password**: MQTT password (leave empty for anonymous)
   - **Client ID**: Unique identifier (can be auto-generated)
   - **SSL**: Enable for secure connections

### Client ID Best Practices
- Use unique, descriptive names: `n8n-workflow-001`, `n8n-mqtt-listener`
- Avoid special characters
- Keep under 65 characters
- If left empty, n8n auto-generates a UUID

### Topics Configuration
- **Single topic**: `sensors/temperature`
- **Multiple topics**: `sensors/temperature,sensors/humidity,alerts/critical`
- **Wildcards**: 
  - `+` single level: `sensors/+/temperature`
  - `#` multi-level: `sensors/#`

## EMQX Broker Configuration

### Authentication Methods

#### 1. Anonymous Access (Simplest)
```bash
# Disable authentication on TCP listener
docker exec emqxnodec emqx_ctl conf load - <<EOF
listeners.tcp.default.enable_authn = false
EOF

# Clear authorization sources
docker exec emqxnodec emqx_ctl conf load - <<EOF
authorization.sources = []
EOF
```

#### 2. Built-in Database Authentication
Via EMQX Dashboard:
1. **Access Control** → **Authentication** → **+ Add**
2. **Backend**: Built-in Database
3. **Mechanism**: Password-based
4. **Password Hash**: Plain (for testing)

#### 3. Dashboard Commands
```bash
# Create admin user (password must be 8+ characters)
docker exec emqxnodec emqx_ctl admins add admin adminpass123 "Admin user"

# Reset admin password
docker exec emqxnodec emqx_ctl admins passwd admin newpassword123

# List listeners
docker exec emqxnodec emqx_ctl listeners

# Check authentication config
docker exec emqxnodec emqx_ctl conf show authentication
```

## Network Connectivity Troubleshooting

### Common Connection Issues

#### Issue 1: TCP Connection Refused
**Symptoms**: n8n credential test fails immediately
**Causes**:
- EMQX container not running
- Wrong IP address
- Port not accessible

**Solutions**:
```bash
# Check EMQX container status
docker ps | grep emqx

# Check EMQX IP address
docker inspect emqxnodec | grep IPAddress

# Check port mapping
docker port emqxnodec

# Test basic connectivity
telnet 172.17.0.4 1883
# or
nc -zv 172.17.0.4 1883
```

#### Issue 2: Authentication Failed
**Symptoms**: Connection established but authentication fails
**Causes**:
- Wrong username/password
- MySQL authentication configured but MySQL not available
- Client ID conflicts

**Solutions**:
1. **Enable anonymous access** (recommended for testing)
2. **Create built-in database user**
3. **Check EMQX logs**: `docker logs emqxnodec`

#### Issue 3: Container Network Issues
**Symptoms**: Timeout errors, intermittent connections
**Causes**:
- Containers on different networks
- Docker bridge network issues
- Firewall blocking container-to-container communication

**Solutions**:
```bash
# Check container networks
docker network ls
docker inspect n8n | grep NetworkMode
docker inspect emqxnodec | grep NetworkMode

# Try different host addresses in n8n:
# Option 1: Container IP
Host: 172.17.0.4

# Option 2: Container name (if on same network)
Host: emqxnodec

# Option 3: Docker host (if port is mapped)
Host: host.docker.internal
Port: 1883

# Option 4: Localhost (if port is mapped)
Host: localhost
Port: 1883
```

### Network Connectivity Test Script
```python
#!/usr/bin/env python3
import socket

def test_mqtt_connectivity():
    hosts_to_try = [
        ('172.17.0.4', 1883, 'Container IP'),
        ('localhost', 1883, 'Localhost mapping'),
        ('emqxnodec', 1883, 'Container name'),
        ('host.docker.internal', 1883, 'Docker host')
    ]
    
    for host, port, description in hosts_to_try:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)
            result = sock.connect_ex((host, port))
            sock.close()
            
            if result == 0:
                print(f"✅ {description} ({host}:{port}) - SUCCESS")
                return host
            else:
                print(f"❌ {description} ({host}:{port}) - FAILED")
        except Exception as e:
            print(f"❌ {description} ({host}:{port}) - ERROR: {e}")
    
    return None

# Usage
working_host = test_mqtt_connectivity()
if working_host:
    print(f"\nUse Host: {working_host} in n8n MQTT credentials")
```

## Complete n8n MQTT Setup Procedure

### Step 1: Verify EMQX Status
```bash
# Check container is running
docker ps | grep emqx

# Check logs for errors
docker logs emqxnodec --tail 20

# Check listeners
docker exec emqxnodec emqx_ctl listeners
```

### Step 2: Configure EMQX Authentication
```bash
# Option A: Disable authentication (easiest)
echo 'listeners.tcp.default.enable_authn = false' | docker exec -i emqxnodec sh -c 'cat > /tmp/auth_fix.conf && emqx_ctl conf load /tmp/auth_fix.conf'

# Option B: Create built-in user via dashboard
# 1. Go to http://localhost:18083
# 2. Login: admin / adminpass123
# 3. Access Control → Authentication → Add Built-in Database
# 4. Access Control → Users → Add User
```

### Step 3: Test Network Connectivity
```bash
# From n8n container to EMQX
docker exec n8n ping -c 1 172.17.0.4

# From host to EMQX
telnet localhost 1883
```

### Step 4: Configure n8n MQTT Credentials
```yaml
Protocol: mqtt://
Host: [result from connectivity test]
Port: 1883
Username: [empty for anonymous, or created username]
Password: [empty for anonymous, or created password]
Client ID: n8n-mqtt-client
SSL: OFF
```

### Step 5: Test and Verify
1. **Test credential** in n8n (should show "Connection successful")
2. **Check EMQX dashboard**: Monitoring → Clients (should show n8n connection)
3. **Assign credential** to MQTT Trigger node
4. **Activate workflow**

## Common Error Messages

### "Connection refused"
- **Check**: EMQX container running
- **Check**: Correct IP/port
- **Try**: Different host addresses (localhost, container name)

### "Connection timeout"
- **Check**: Network connectivity between containers
- **Check**: Firewall/security software
- **Try**: Different network configurations

### "Authentication failed" 
- **Check**: Username/password correct
- **Check**: Authentication method in EMQX dashboard
- **Try**: Anonymous access (disable authentication)

### "Client ID already in use"
- **Change**: Client ID to unique value
- **Check**: Existing connections in EMQX dashboard

## Best Practices

### Security
- Use unique Client IDs
- Enable SSL for production (port 8883)
- Use strong passwords for MQTT users
- Limit topic permissions per user

### Performance
- Use appropriate QoS levels (0 for sensors, 1 for alerts)
- Keep Client IDs short but descriptive
- Monitor connection counts in EMQX dashboard

### Troubleshooting
- Always check EMQX logs first: `docker logs emqxnodec`
- Test connectivity before configuring authentication
- Use EMQX dashboard monitoring tools
- Keep authentication simple initially (anonymous access)

## Reference Commands

```bash
# EMQX Management
docker restart emqxnodec
docker logs emqxnodec --tail 50
docker exec emqxnodec emqx_ctl status
docker exec emqxnodec emqx_ctl listeners

# Network Diagnostics
docker network ls
docker inspect emqxnodec | grep IPAddress
docker exec n8n ping -c 1 172.17.0.4
netstat -an | grep 1883

# Authentication Management
docker exec emqxnodec emqx_ctl conf show authentication
docker exec emqxnodec emqx_ctl admins list
docker exec emqxnodec emqx_ctl clients list
```

---
*This guide should resolve most n8n + EMQX MQTT connectivity issues*