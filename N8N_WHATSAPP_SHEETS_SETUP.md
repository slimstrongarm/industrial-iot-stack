# n8n WhatsApp & Google Sheets Configuration Guide

## Overview
The MQTT Equipment Alert workflow needs two components configured:
1. **WhatsApp Business API** - For sending alert messages
2. **Google Sheets API** - For logging all MQTT data

## Current Workflow Structure
```
MQTT Trigger → Process Alert → Check Severity → WhatsApp Alert (critical/warning)
                            ↓
                     Log All Alerts → Google Sheets (all events)
```

## 1. Google Sheets Setup (Easiest First)

### Step 1: Verify Google Sheets Access
The workflow is already configured to use:
- **Spreadsheet ID**: `1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do`
- **Service Account**: From existing credentials

### Step 2: Create Required Sheets
Add these sheets to your Google Spreadsheet:

#### Sheet 1: "Equipment Alerts" 
Headers: `Timestamp | Equipment_ID | Equipment_Type | Location | Severity | Topic | Alert_Sent | Raw_Data`

#### Sheet 2: "All Equipment Events"
Headers: `Timestamp | Equipment_ID | Equipment_Type | Location | Severity | Topic | Priority | Raw_Data`

### Step 3: Configure n8n Google Sheets Credentials
1. Go to n8n → **Credentials** → **Add Credential**
2. Select **Google Sheets Service Account**
3. Upload the service account JSON file
4. Test the connection

## 2. WhatsApp Business API Setup

### Option A: Meta WhatsApp Business API (Production)
1. **Create Meta Developer Account**: https://developers.facebook.com/
2. **Set up WhatsApp Business API**
3. **Get Access Token and Phone Number ID**
4. **Update n8n workflow with credentials**

### Option B: WhatsApp Business API via Third-Party (Easier)
Services like:
- **Twilio WhatsApp API**
- **MessageBird WhatsApp**
- **360Dialog WhatsApp**

### Option C: Test with HTTP Mock (Development)
For testing without real WhatsApp setup:

```json
{
  "method": "POST",
  "url": "https://webhook.site/your-unique-url",
  "body": {
    "message": "{{$json.whatsappMessage}}",
    "severity": "{{$json.severity}}",
    "timestamp": "{{$json.timestamp}}"
  }
}
```

## 3. Quick Test Setup

### Step 1: Google Sheets Only (No WhatsApp)
1. Configure Google Sheets credentials in n8n
2. Create the two required sheets
3. Test with MQTT message:
```bash
mosquitto_pub -h host.docker.internal -p 1883 -t "equipment/alerts" -m '{"equipmentId":"PUMP-001","type":"centrifugal_pump","location":"Building A","value":85,"threshold":80,"description":"Temperature too high"}'
```

### Step 2: Add WhatsApp Later
Once Google Sheets logging works, add WhatsApp configuration.

## 4. Current Workflow Configuration

### MQTT Trigger Node (Already Working ✅)
- Host: `host.docker.internal` (fixed network issue)
- Port: 1883
- Topics: `equipment/alerts,sensors/critical,actuators/fault`

### WhatsApp Node (Needs Configuration)
- **Current placeholder**: `YOUR_WHATSAPP_API_TOKEN`
- **Phone number placeholder**: `YOUR_PHONE_NUMBER`

### Google Sheets Nodes (Need Credentials)
- **Document ID**: Already set to correct spreadsheet
- **Service Account**: Needs credentials upload

## 5. Test Message Examples

### Critical Alert
```bash
mosquitto_pub -h host.docker.internal -p 1883 -t "sensors/critical" -m '{"equipmentId":"TEMP-001","type":"temperature_sensor","location":"Reactor Room","value":95,"threshold":85,"description":"Critical temperature exceeded"}'
```

### Equipment Fault  
```bash
mosquitto_pub -h host.docker.internal -p 1883 -t "actuators/fault" -m '{"equipmentId":"VALVE-003","type":"control_valve","location":"Process Line 2","value":"stuck_closed","description":"Valve failed to open"}'
```

### Warning Alert
```bash
mosquitto_pub -h host.docker.internal -p 1883 -t "equipment/alerts" -m '{"equipmentId":"MOTOR-005","type":"servo_motor","location":"Conveyor Belt","value":78,"threshold":75,"description":"Vibration levels elevated"}'
```

## Next Steps

1. **Start with Google Sheets** - Configure credentials and test logging
2. **Verify sheet creation** - Make sure both sheets exist with correct headers
3. **Test MQTT → Sheets flow** - Send test messages and verify logging
4. **Add WhatsApp later** - Once logging works, configure messaging

Would you like to start with Google Sheets setup first?