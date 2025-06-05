# Working n8n MQTT Configuration

## ✅ CONFIRMED: Authentication is DISABLED on port 1883!

The EMQX configuration shows:
```
bind = 1883
enable = true
enable_authn = false  <-- This means NO authentication required!
```

## n8n MQTT Trigger Configuration

Use these exact settings:

```
Protocol: mqtt://
Host: localhost
Port: 1883
Username: (LEAVE COMPLETELY EMPTY)
Password: (LEAVE COMPLETELY EMPTY)
Client ID: n8n-mqtt-client
Clean Session: true
SSL: OFF
```

## Important Notes

1. **No credentials needed** - Authentication is disabled on port 1883
2. **Client ID** - Can be any value, use `n8n-mqtt-client` for consistency
3. **Host** - Use `localhost` since n8n is on the same machine

## Test Topics

Subscribe to these topics in n8n:
- `test/#` - Catch all test messages
- `sensors/+/temperature` - Temperature from any sensor
- `alerts/critical` - Critical alerts only

## Send Test Message

From Mac Mosquitto:
```bash
mosquitto_pub -h <WINDOWS_IP> -p 1883 -t "test/hello" -m "Hello from Mac"
```

From Windows WSL:
```bash
# Install mosquitto client first
sudo apt-get update && sudo apt-get install -y mosquitto-clients

# Send test message
mosquitto_pub -h localhost -p 1883 -t "test/hello" -m "Test message"
```

## If Still Failing

1. Check n8n container can reach EMQX:
```bash
docker exec n8n ping -c 3 emqxnodec
```

2. Check from inside n8n container:
```bash
docker exec n8n nc -zv emqxnodec 1883
```

3. Try using container name instead of localhost:
- Host: `emqxnodec` (instead of localhost)

The authentication is definitely disabled, so this should work!