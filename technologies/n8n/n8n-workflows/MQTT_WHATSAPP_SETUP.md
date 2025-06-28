# MQTT to WhatsApp Alert System Setup

## Overview
This workflow listens to MQTT topics for industrial alerts and sends WhatsApp messages based on severity levels. Critical and High severity alerts get immediate WhatsApp notifications, while lower priority alerts get simplified messages.

## Workflow: `mqtt-to-whatsapp-alerts.json`

### Flow Description
1. **MQTT Alert Listener** - Subscribes to `iiot/alerts/critical` topic
2. **Process Alert Data** - Formats incoming data and creates WhatsApp message
3. **High Priority Filter** - Routes Critical/High alerts vs Low alerts
4. **Send WhatsApp Alert** - Sends formatted message via WhatsApp Business API
5. **Log to Google Sheets** - Records all sent alerts for tracking

### MQTT Message Format
Send alerts to topic: `iiot/alerts/critical`
```json
{
  "alertType": "Temperature Threshold",
  "equipmentId": "BOILER-01",
  "severity": "Critical",
  "message": "Temperature exceeded safe limits",
  "timestamp": "2025-06-03T16:00:00Z",
  "location": "Brew House Area 1",
  "value": "185°F",
  "threshold": "160°F"
}
```

### WhatsApp Message Output
**Critical/High Severity:**
```
🚨 *INDUSTRIAL ALERT*

📍 *Equipment:* BOILER-01
🏭 *Location:* Brew House Area 1
⚠️ *Severity:* Critical
🔔 *Type:* Temperature Threshold

💬 *Message:*
Temperature exceeded safe limits

📊 *Details:*
• Current Value: 185°F
• Threshold: 160°F
• Time: 6/3/2025, 4:00:00 PM

🔧 *Action Required:* Please investigate immediately

_Sent via Industrial IoT Stack_
```

**Low Severity:**
```
ℹ️ *Equipment Update*

📍 Equipment: BOILER-01
🔔 Alert: Temperature Threshold

Temperature exceeded safe limits

_Low priority - for your information_
```

## Setup Instructions

### 1. WhatsApp Business API Setup
You'll need a WhatsApp Business Account and API access:

#### Option A: WhatsApp Cloud API (Recommended)
1. Go to [Facebook Developers](https://developers.facebook.com/)
2. Create a new app → Business → WhatsApp
3. Add WhatsApp product to your app
4. Get your:
   - **Phone Number ID** (from WhatsApp > Getting Started)
   - **Access Token** (permanent token from System Users)
   - **Verify Token** (webhook verification)

#### Option B: WhatsApp Business API (On-Premise)
- Requires WhatsApp Business API client setup
- More complex but more control

### 2. Configure n8n Credentials

#### WhatsApp Business API Credential
1. In n8n: Settings → Credentials → Add Credential
2. Select "WhatsApp Business"
3. Enter:
   - **Access Token**: Your permanent access token
   - **Phone Number ID**: Your WhatsApp phone number ID
4. Test the connection

#### MQTT Credential  
1. Add MQTT credential
2. Configure:
   - **Host**: `localhost` (if EMQX is on same server) or server IP
   - **Port**: `1883`
   - **Username/Password**: (if EMQX has auth enabled)
   - **Protocol**: `mqtt://`

### 3. Import and Configure Workflow
1. Import `mqtt-to-whatsapp-alerts.json`
2. Update these nodes:

#### MQTT Alert Listener Node
- **Topic**: Change if you want different topic (`iiot/alerts/critical`)
- **Credentials**: Select your MQTT credential

#### Process Alert Data Node
- **Phone Number**: Update the default phone number in the code:
  ```javascript
  phoneNumber: '+1234567890', // Change this to your target number
  ```

#### WhatsApp Nodes
- **Credentials**: Select your WhatsApp Business API credential
- **From Phone Number ID**: Should auto-populate from credentials

#### Google Sheets Logging (Optional)
- **Document ID**: Update to your Google Sheets ID
- **Sheet Name**: Create "WhatsApp Alert Log" tab or change name
- **Credentials**: Select your Google Sheets credential

### 4. Test the Workflow

#### Manual Test with MQTT
```bash
# Using mosquitto client to publish test alert
mosquitto_pub -h localhost -t "iiot/alerts/critical" -m '{
  "alertType": "Test Alert",
  "equipmentId": "TEST-01", 
  "severity": "Critical",
  "message": "This is a test alert from MQTT",
  "timestamp": "'$(date -Iseconds)'",
  "location": "Test Lab",
  "value": "100",
  "threshold": "50"
}'
```

#### Test from Node-RED
Create a simple inject node that publishes to `iiot/alerts/critical`:
```json
{
  "alertType": "Equipment Malfunction",
  "equipmentId": "PUMP-02",
  "severity": "High", 
  "message": "Pump pressure dropped below minimum",
  "timestamp": "{{timestamp}}",
  "location": "Production Floor",
  "value": "25 PSI",
  "threshold": "40 PSI"
}
```

### 5. Production Configuration

#### Environment Variables
Set these in your `.env` file:
```bash
# WhatsApp Configuration
WHATSAPP_ACCESS_TOKEN=your_permanent_access_token
WHATSAPP_PHONE_NUMBER_ID=your_phone_number_id
WHATSAPP_VERIFY_TOKEN=your_webhook_verify_token

# Alert Configuration  
DEFAULT_ALERT_PHONE=+1234567890
ALERT_LOG_SHEET_ID=your_google_sheets_id
```

#### Multiple Recipients
To send to multiple phones, modify the "Process Alert Data" node:
```javascript
// Array of phone numbers based on severity
let phoneNumbers = [];
if (severity === 'Critical') {
  phoneNumbers = ['+1234567890', '+0987654321']; // Emergency contacts
} else if (severity === 'High') {
  phoneNumbers = ['+1234567890']; // Supervisor only
} else {
  phoneNumbers = ['+1111111111']; // Info only contact
}

return phoneNumbers.map(phone => ({
  json: {
    ...existingData,
    phoneNumber: phone
  }
}));
```

### 6. MQTT Topics Strategy

Recommended topic structure:
```
iiot/alerts/critical     - Immediate action required
iiot/alerts/warning      - Attention needed
iiot/alerts/info         - Information only
iiot/equipment/{id}/alert - Equipment-specific alerts
iiot/location/{area}/alert - Location-based alerts
```

### 7. Rate Limiting & Anti-Spam

Add rate limiting in the "Process Alert Data" node:
```javascript
// Simple rate limiting - only send if last alert was >5 minutes ago
const equipmentId = mqttData.equipmentId;
const lastAlertKey = `lastAlert_${equipmentId}`;
const lastAlert = $getWorkflowStaticData('global')[lastAlertKey];
const now = new Date().getTime();

if (lastAlert && (now - lastAlert) < 300000) { // 5 minutes
  // Skip this alert
  return [];
}

// Update last alert time
$getWorkflowStaticData('global')[lastAlertKey] = now;
```

## Monitoring & Troubleshooting

### Check WhatsApp Delivery
- Monitor n8n execution log for WhatsApp API responses
- Check Google Sheets log for sent messages
- WhatsApp Business Manager shows message delivery status

### Common Issues
1. **"Invalid phone number"** - Ensure number includes country code (+1...)
2. **"Access token expired"** - Generate new permanent token
3. **"MQTT connection failed"** - Check EMQX broker status and credentials
4. **"Rate limit exceeded"** - WhatsApp has sending limits, implement queuing

### Logs & Debugging
```bash
# Check n8n logs
docker logs iiot-n8n -f

# Check EMQX broker logs  
docker logs emqx -f

# Test MQTT connectivity
mosquitto_sub -h localhost -t "iiot/alerts/critical" -v
```

Ready for industrial WhatsApp alerting! 📱🏭