# WhatsApp API Integration Guide for Industrial IoT Stack

## Overview
This guide provides comprehensive documentation for integrating WhatsApp messaging into the Industrial IoT Stack for real-time alerts, notifications, and bidirectional communication with operators.

## WhatsApp Business API Options

### 1. WhatsApp Business API (Official)
**Best for**: Production deployments, official support
- **Provider**: Meta (Facebook)
- **Cost**: Pay-per-message pricing (~$0.005-$0.08 per message)
- **Requirements**: Business verification, hosting provider
- **Limitations**: Complex setup, approval process

### 2. WhatsApp Business Cloud API
**Best for**: Quick setup, cloud-based
- **Provider**: Meta Cloud
- **Cost**: Similar to Business API
- **Requirements**: Facebook Business Manager account
- **Benefits**: No hosting required, easier setup

### 3. Third-Party Services (Recommended for POC)
**Best for**: Rapid prototyping, brewery demo
- **Twilio WhatsApp API**
- **MessageBird** 
- **Vonage (Nexmo)**
- **WATI.io**

## Recommended: Twilio WhatsApp Integration

### Why Twilio?
- Quick sandbox for testing (no approval needed)
- Production-ready when needed
- Excellent Node-RED support
- Built-in n8n integration
- Pay-as-you-go pricing

### Twilio Setup Steps

#### 1. Create Twilio Account
```
1. Go to https://www.twilio.com/try-twilio
2. Sign up for free account ($15 credit included)
3. Verify your phone number
4. Note your Account SID and Auth Token
```

#### 2. Activate WhatsApp Sandbox
```
1. Navigate to Messaging > Try it out > Send a WhatsApp message
2. Follow sandbox join instructions (send "join <word>" to Twilio number)
3. Note the Twilio WhatsApp number
```

#### 3. Configure Webhook URLs
```
When a message comes in:
https://your-server.com/webhook/whatsapp-incoming

Status callback URL:
https://your-server.com/webhook/whatsapp-status
```

## Integration Architectures

### Architecture 1: Node-RED Direct Integration
```
Ignition → MQTT → Node-RED → Twilio API → WhatsApp
                      ↓
                 Google Sheets (logging)
```

### Architecture 2: N8N Workflow Integration
```
Ignition → N8N Webhook → Twilio Node → WhatsApp
              ↓
         Google Sheets
```

### Architecture 3: Hybrid Approach (Recommended)
```
Critical Alerts: Ignition → Node-RED → WhatsApp (fast)
Reports/Forms: N8N → WhatsApp (feature-rich)
```

## Node-RED Implementation

### Install Twilio Node
```bash
cd ~/.node-red
npm install node-red-contrib-twilio
```

### Example Flow: Temperature Alert to WhatsApp
```json
[
    {
        "id": "mqtt-temp-monitor",
        "type": "mqtt in",
        "topic": "brewery/+/temperature",
        "name": "Temperature Monitor"
    },
    {
        "id": "temp-threshold",
        "type": "function",
        "name": "Check Threshold",
        "func": "const temp = msg.payload.value;\nconst equipment = msg.payload.equipment;\n\nif (temp > 80) {\n    msg.message = `⚠️ ALERT: ${equipment} temperature is ${temp}°F (threshold: 80°F)`;\n    return msg;\n}\nreturn null;"
    },
    {
        "id": "twilio-whatsapp",
        "type": "twilio out",
        "twilio": "twilio-config",
        "from": "whatsapp:+14155238886",
        "to": "whatsapp:+1234567890",
        "name": "Send WhatsApp Alert"
    }
]
```

## N8N Implementation

### N8N Workflow: Equipment Alert to WhatsApp
```json
{
  "name": "Equipment Alert to WhatsApp",
  "nodes": [
    {
      "name": "Webhook",
      "type": "n8n-nodes-base.webhook",
      "parameters": {
        "path": "equipment-alert",
        "responseMode": "onReceived"
      }
    },
    {
      "name": "Format Message",
      "type": "n8n-nodes-base.function",
      "parameters": {
        "functionCode": "const alert = items[0].json;\nreturn [{\n  json: {\n    message: `🏭 ${alert.severity.toUpperCase()} Alert\\n\\nEquipment: ${alert.equipment}\\nIssue: ${alert.description}\\nTime: ${new Date().toLocaleString()}\\n\\nReply with:\\n1️⃣ Acknowledge\\n2️⃣ Escalate\\n3️⃣ Ignore`,\n    to: 'whatsapp:+1234567890'\n  }\n}];"
      }
    },
    {
      "name": "Twilio",
      "type": "n8n-nodes-base.twilio",
      "parameters": {
        "resource": "sms",
        "operation": "send",
        "from": "={{$json[\"from\"]}}",
        "to": "={{$json[\"to\"]}}",
        "message": "={{$json[\"message\"]}}"
      }
    }
  ]
}
```

## Bidirectional Communication

### Handling Incoming Messages
```javascript
// Node-RED function to process WhatsApp replies
const message = msg.payload.Body.toLowerCase();
const from = msg.payload.From;

// Parse operator commands
if (message.includes('acknowledge') || message === '1') {
    // Update alert status in database
    msg.topic = 'UPDATE alerts SET acknowledged = true WHERE phone = ?';
    msg.payload = [from];
    return [msg, null];
} else if (message.includes('escalate') || message === '2') {
    // Escalate to supervisor
    msg.escalate = true;
    return [null, msg];
}
```

## API Reference

### Send WhatsApp Message (Twilio)
```bash
curl -X POST https://api.twilio.com/2010-04-01/Accounts/$TWILIO_ACCOUNT_SID/Messages.json \
--data-urlencode "From=whatsapp:+14155238886" \
--data-urlencode "To=whatsapp:+1234567890" \
--data-urlencode "Body=Equipment alert from IoT system" \
-u $TWILIO_ACCOUNT_SID:$TWILIO_AUTH_TOKEN
```

### Message Templates
```javascript
// Critical Alert
const criticalAlert = `
🚨 CRITICAL ALERT 🚨
Equipment: ${equipment}
Status: ${status}
Value: ${currentValue} (Limit: ${threshold})
Action Required: Immediate attention needed
`;

// Daily Summary
const dailySummary = `
📊 Daily Brewery Report
Date: ${date}
━━━━━━━━━━━━━━━
✅ Systems Online: ${onlineCount}
⚠️ Warnings: ${warningCount}
❌ Critical Issues: ${criticalCount}
━━━━━━━━━━━━━━━
View Dashboard: ${dashboardUrl}
`;

// Maintenance Reminder
const maintenanceReminder = `
🔧 Maintenance Due
Equipment: ${equipment}
Last Service: ${lastService}
Due Date: ${dueDate}
━━━━━━━━━━━━━━━
Reply YES to confirm scheduled
`;
```

## Cost Estimation

### Twilio Pricing (as of 2024)
- WhatsApp Template Messages: $0.005 per message
- WhatsApp Session Messages: $0.005 per message
- Phone Number: $1/month (sandbox free)

### Example Monthly Costs
- 100 alerts/day = 3,000 messages/month = ~$15/month
- Add 20% for responses = ~$18/month total

## Security Considerations

### 1. API Credentials
- Store in environment variables
- Never commit to Git
- Use Docker secrets for production

### 2. Message Validation
- Verify webhook signatures
- Validate phone numbers
- Implement rate limiting

### 3. Access Control
- Whitelist approved numbers
- Role-based message routing
- Audit all communications

## Testing Strategy

### 1. Development Testing
```bash
# Test with Twilio sandbox
export TWILIO_ACCOUNT_SID=your_sid
export TWILIO_AUTH_TOKEN=your_token
export WHATSAPP_FROM=whatsapp:+14155238886
export WHATSAPP_TO=whatsapp:+1234567890

# Send test message
node test-whatsapp.js
```

### 2. Integration Testing
- Simulate equipment alerts
- Test message formatting
- Verify delivery receipts
- Test reply handling

## Production Deployment

### 1. Business Verification
- Register with WhatsApp Business
- Submit business documents
- Wait for approval (2-3 weeks)

### 2. Template Approval
- Submit message templates
- Follow WhatsApp guidelines
- No promotional content in alerts

### 3. Migration from Sandbox
- Update phone numbers
- Switch API endpoints
- Update webhook URLs

## Troubleshooting

### Common Issues
1. **Message not delivered**: Check phone format (+1234567890)
2. **Webhook not firing**: Verify public URL accessibility
3. **Rate limits**: Implement exponential backoff
4. **Template rejected**: Follow WhatsApp content guidelines

### Debug Commands
```javascript
// Node-RED debug
node.warn(`WhatsApp payload: ${JSON.stringify(msg.payload)}`);

// N8N debug
console.log('Twilio response:', $response);
```

## Quick Start for Brewery Demo

### 1. Minimal Setup (15 minutes)
```bash
# 1. Sign up for Twilio (free)
# 2. Join WhatsApp sandbox
# 3. Deploy this Node-RED flow:

[{"id":"whatsapp-demo","type":"inject","name":"Simulate Alert","props":[{"p":"payload"}],"repeat":"","crontab":"","once":false,"onceDelay":0.1,"topic":"","payload":"{\"equipment\":\"Boiler #1\",\"temp\":85,\"threshold\":80}","payloadType":"json"},{"id":"format-msg","type":"function","name":"Format WhatsApp","func":"msg.payload = {\n    to: 'whatsapp:+1234567890',\n    from: 'whatsapp:+14155238886',\n    body: `⚠️ Temperature Alert!\\n\\nEquipment: ${msg.payload.equipment}\\nCurrent: ${msg.payload.temp}°F\\nThreshold: ${msg.payload.threshold}°F\\n\\nReply 1 to acknowledge`\n};\nreturn msg;"},{"id":"send-whatsapp","type":"http request","name":"Send via Twilio","method":"POST","url":"https://api.twilio.com/2010-04-01/Accounts/{AccountSID}/Messages.json","headers":{"Authorization":"Basic {base64(AccountSID:AuthToken)}","Content-Type":"application/x-www-form-urlencoded"}}]
```

### 2. Demo Script
1. Show normal operations on dashboard
2. Trigger temperature spike in Ignition
3. Receive WhatsApp alert on phone
4. Reply "1" to acknowledge
5. Show acknowledged status in dashboard

## Next Steps

1. **For POC**: Use Twilio sandbox (free, immediate)
2. **For Production**: Apply for WhatsApp Business API
3. **Integration Priority**:
   - Critical alerts via Node-RED (fast)
   - Reports/forms via N8N (feature-rich)
   - Bidirectional commands (advanced)

---

*Last Updated: June 2025*
*Part of Industrial IoT Stack Project*