# MQTT Authentication Debug Guide

## Current Situation
- EMQX Built-in Database: ENABLED
- User ID Type: **clientid** (not username!)
- Password Hash: SHA256 with suffix salt
- MySQL: DISABLED
- Created user: n8nuser / n8npass123

## The Problem
When n8n connects with:
- Client ID: n8nuser
- Password: n8npass123
- Username: (empty)

It still fails, suggesting either:
1. Password hash mismatch (plain text vs SHA256)
2. User not actually created in database
3. Client ID format issue
4. Network/connection issue

## Debug Steps

### 1. Monitor EMQX Logs
Run in one terminal:
```bash
./scripts/monitor_emqx_logs.sh
```

Then try n8n connection to see exact error.

### 2. Test with MQTT Client
Install mosquitto client:
```bash
sudo apt-get update && sudo apt-get install -y mosquitto-clients
```

Test connection:
```bash
# Test with client ID auth
mosquitto_sub -h localhost -p 1883 -i "n8nuser" -P "n8npass123" -t "test/#" -v

# Test anonymous
mosquitto_sub -h localhost -p 1883 -i "test-client" -t "test/#" -v
```

### 3. Check if User Exists
Look in EMQX Dashboard:
- Access Control → Authentication → Built-in Database
- Check if n8nuser is listed

### 4. Simple Fix - Enable Anonymous
Since we're in development, just enable anonymous access:

```bash
docker exec emqxnodec emqx_ctl conf load - <<EOF
listeners.tcp.default.enable_authn = false
EOF
```

## Alternative Solutions

### A. Use Docker Environment Variable
Restart EMQX with anonymous enabled:
```bash
docker stop emqxnodec
docker run -d --name emqxnodec \
  -p 1883:1883 \
  -p 18083:18083 \
  -e EMQX_ALLOW_ANONYMOUS=true \
  --network bridge \
  emqx:latest
```

### B. Create Plain Text Auth
Switch to plain text password storage for development.

### C. Use Different MQTT Broker
If EMQX continues to have issues, consider:
- Mosquitto (simpler)
- HiveMQ (has free tier)
- Local test broker

## Next Action
Run the monitor script and try n8n connection to see the exact error message. This will tell us if it's:
- "User not found" → User creation issue
- "Bad password" → Hash mismatch
- "Client ID not allowed" → ACL issue
- Connection refused → Network issue