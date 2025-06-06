# WhatsApp Integration for Industrial IoT Stack

## Overview
Real-time WhatsApp alerts and bidirectional communication for brewery equipment monitoring.

## Quick Start (5 minutes)
1. Run setup script: `./quick-setup.sh`
2. Sign up for free Twilio account
3. Join WhatsApp sandbox
4. Import `brewery-demo-flow.json` into Node-RED
5. Test with simulated alert

## Files in this Directory

### Core Documentation
- `WHATSAPP_API_INTEGRATION_GUIDE.md` - Complete integration guide
- `README.md` - This file

### Implementation Files
- `brewery-demo-flow.json` - Generic Node-RED flow for brewery alerts
- `steel-bonnet-flow.json` - **Steel Bonnet specific flow** (matches actual MQTT topics)
- `quick-setup.sh` - One-command setup script
- `test-alert.js` - Testing script for development

### Example Configurations
- `twilio-config-example.json` - Example Twilio configuration
- `environment-variables.env` - Required environment variables

## Integration Options

### 1. Immediate (Twilio Sandbox)
- Free setup in 5 minutes
- Perfect for Friday brewery demo
- No approval process needed

### 2. Production (WhatsApp Business API)
- Requires business verification
- 2-3 week approval process
- Official WhatsApp support

### 3. Hybrid Approach
- Start with Twilio for demo
- Migrate to official API for production

## Demo Scenarios

### Steel Bonnet Equipment Alert
```
MQTT Topic: salinas/utilities/air_compressor_01/telemetry
Payload: {"temperature": 85, "pressure": 125}
Trigger: Temperature > 85°F threshold
Message: "🔴 STEEL BONNET ALERT - AIR COMPRESSOR 01 at SALINAS/UTILITIES temperature 85°F (limit 85°F)"
Response: Operator replies "1" to acknowledge
Result: Alert logged to Google Sheets and marked handled
```

### Daily Summary Report
```
Trigger: End of day automation
Message: "📊 Daily Report - 12 alerts, 3 warnings, 1 critical"
Response: Click link for full dashboard
```

## Cost Estimate
- Development/Testing: Free (Twilio sandbox)
- Production: ~$0.005 per message (~$15/month for 100 alerts/day)

## Security
- API credentials stored in environment variables
- Webhook signature validation
- Phone number whitelisting

## Support
- Twilio documentation: https://www.twilio.com/docs/whatsapp
- This implementation: See main integration guide
- Issues: Check troubleshooting section in main guide