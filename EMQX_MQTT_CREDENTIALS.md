# EMQX MQTT Broker - Authentication Configuration

## Connection Details

### MQTT Broker Access
- **Host**: 172.17.0.4
- **Port**: 1883 (TCP)
- **WebSocket Port**: 8083
- **SSL Port**: 8883 (if SSL is needed)

### Authentication Credentials
Based on EMQX default configuration, try these credentials:

**Option 1: Dashboard Credentials**
- **Username**: `admin`
- **Password**: `public`

**Option 2: No Authentication** (if anonymous access is enabled)
- Leave username and password empty

**Option 3: Common Default Credentials**
- **Username**: `emqx`
- **Password**: `emqx`

## n8n MQTT Credential Configuration

### Step-by-Step Setup in n8n

1. **Access n8n**: http://localhost:5678
2. **Go to Settings → Credentials**
3. **Add New Credential → MQTT**
4. **Configure the following**:

```
Protocol: mqtt://
Host: 172.17.0.4
Port: 1883
Username: admin
Password: public
Client ID: n8n-mqtt-listener
Clean Session: true
Keep Alive: 60
```

### Alternative Configuration (No Auth)
If authentication fails, try:
```
Protocol: mqtt://
Host: 172.17.0.4
Port: 1883
Username: (leave empty)
Password: (leave empty)
Client ID: n8n-mqtt-listener
```

## Testing MQTT Connection

### Using Docker (from inside a container)
```bash
# Install mosquitto client tools
docker run --rm -it --network bridge eclipse-mosquitto:latest sh

# Test publish
mosquitto_pub -h 172.17.0.4 -p 1883 -u admin -P public -t "test/topic" -m "test message"

# Test subscribe
mosquitto_sub -h 172.17.0.4 -p 1883 -u admin -P public -t "test/topic"
```

### Using Node-RED MQTT Node
If you have Node-RED running, you can test MQTT connectivity:
1. Add an MQTT Input node
2. Configure broker: `172.17.0.4:1883`
3. Use credentials: `admin` / `public`
4. Test connection

## Troubleshooting

### Connection Refused
- Verify EMQX is running: `docker ps | grep emqx`
- Check EMQX logs: `docker logs emqxnodec`
- Verify IP address: `docker inspect emqxnodec | grep IPAddress`

### Authentication Failed
Try these approaches in order:
1. Use `admin` / `public` (dashboard credentials)
2. Try no username/password (anonymous access)
3. Check EMQX dashboard for user management
4. Create new MQTT user via EMQX dashboard

### EMQX Dashboard Access
- **URL**: http://localhost:18083
- **Username**: `admin`
- **Password**: `public`

In the dashboard, go to **Access Control → Authentication** to:
- View current authentication settings
- Add new MQTT users
- Enable/disable anonymous access

## n8n MQTT Trigger Configuration

Once credentials are set up, configure the MQTT Trigger node:

```json
{
  "host": "172.17.0.4",
  "port": 1883,
  "topics": "equipment/alerts,sensors/critical,actuators/fault",
  "clientId": "n8n-mqtt-listener",
  "qos": 1,
  "messageFormat": "json",
  "credentials": "mqtt_credentials_name"
}
```

## Reference Links

- [n8n MQTT Credentials Documentation](https://docs.n8n.io/integrations/builtin/credentials/mqtt/)
- [EMQX Authentication Guide](https://www.emqx.io/docs/en/v5.0/access-control/authn/authn.html)

## Quick Fix for n8n

The most likely solution for n8n MQTT connection:
1. Create MQTT credentials with `admin` / `public`
2. Test the connection in the credential settings
3. If it works, assign this credential to your MQTT Trigger node
4. Activate the workflow

---
*Last updated: June 3, 2025*