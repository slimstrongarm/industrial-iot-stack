# n8n MQTT Credential Setup - Complete Guide

## MQTT Credential Configuration in n8n

Based on n8n documentation and EMQX defaults, here's the complete setup:

### Required Fields in n8n MQTT Credentials

1. **Protocol**: `mqtt://` (not mqtts:// since SSL is off)
2. **Host**: `172.17.0.4`
3. **Port**: `1883`
4. **Username**: Try these options in order:
   - `admin`
   - Leave empty
   - `emqx`
5. **Password**: Try these options in order:
   - `public`
   - Leave empty  
   - `emqx`
6. **Client ID**: Use a unique identifier like:
   - `n8n-mqtt-client-001`
   - `n8n-workflow-trigger`
   - Or leave empty (n8n will auto-generate)
7. **SSL**: Keep OFF (slider should be off)

### Step-by-Step Setup

1. **Go to n8n Credentials**:
   - Settings → Credentials → Add Credential → MQTT

2. **Configuration 1 (Try First)**:
   ```
   Protocol: mqtt://
   Host: 172.17.0.4
   Port: 1883
   Username: admin
   Password: public
   Client ID: n8n-mqtt-client
   SSL: OFF
   ```

3. **Configuration 2 (If #1 fails)**:
   ```
   Protocol: mqtt://
   Host: 172.17.0.4
   Port: 1883
   Username: (leave empty)
   Password: (leave empty)
   Client ID: n8n-mqtt-client
   SSL: OFF
   ```

4. **Configuration 3 (Alternative)**:
   ```
   Protocol: mqtt://
   Host: 172.17.0.4
   Port: 1883
   Username: emqx
   Password: emqx
   Client ID: n8n-mqtt-client
   SSL: OFF
   ```

### Advanced Settings (if available)

- **Clean Session**: true
- **Keep Alive**: 60 seconds
- **QoS**: 1
- **Retain**: false

## Troubleshooting Connection Issues

### Error: "Connection refused"
- Verify EMQX is running: `docker ps | grep emqx`
- Check if port 1883 is accessible from n8n container

### Error: "Authentication failed"  
- Try anonymous access (no username/password)
- Check EMQX dashboard for user management
- Verify credentials are correct

### Error: "Client ID already in use"
- Change the Client ID to something unique
- Or leave Client ID empty for auto-generation

## Verify EMQX Authentication Settings

### Check EMQX Dashboard
1. Go to: http://localhost:18083
2. Login: `admin` / `public`
3. Navigate to: **Access Control → Authentication**
4. Check if anonymous access is enabled
5. View existing authentication providers

### Test MQTT Connection Outside n8n

```bash
# Install mosquitto clients
sudo apt update && sudo apt install mosquitto-clients

# Test with credentials
mosquitto_pub -h 172.17.0.4 -p 1883 -u admin -P public -t "test/topic" -m "test"

# Test without credentials (anonymous)
mosquitto_pub -h 172.17.0.4 -p 1883 -t "test/topic" -m "test"
```

## Enable Anonymous Access in EMQX (if needed)

If authentication keeps failing, you can enable anonymous access:

1. **Via EMQX Dashboard**:
   - Go to Access Control → Authentication
   - Enable "Allow Anonymous"

2. **Via EMQX CLI**:
   ```bash
   docker exec emqxnodec emqx_ctl conf set zone.external.allow_anonymous true
   ```

## Expected n8n Test Results

When you click "Test" in n8n credentials:
- ✅ **Success**: "Connection successful"
- ❌ **Fail**: "Connection refused" or "Authentication failed"

## Next Steps After Successful Connection

1. Save the MQTT credential in n8n
2. Go to your "MQTT Equipment Alert to WhatsApp (Fixed)" workflow
3. Open the "MQTT Trigger" node
4. Select the credential you just created
5. Configure topics: `equipment/alerts,sensors/critical,actuators/fault`
6. Save and activate the workflow

---

**Most Likely Solution**: Use `admin` / `public` with Client ID `n8n-mqtt-client` and SSL OFF.