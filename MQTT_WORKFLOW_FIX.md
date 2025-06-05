# MQTT Workflow Fix - Trigger Node Issue Resolved

## Problem
The original MQTT workflow failed to activate with error:
```
Workflow could not be activated: Workflow "MQTT Equipment Alert to WhatsApp" (ID: lwewtGRg3sFb9CX5) has no node to start the workflow - at least one trigger, poller or webhook node is required
```

## Root Cause
The workflow was using `n8n-nodes-base.mqtt` instead of `n8n-nodes-base.mqttTrigger`. The regular MQTT node is for sending messages, while the MQTT Trigger node is for receiving/listening to messages.

## Solution Applied
1. **Deleted** problematic workflow (ID: lwewtGRg3sFb9CX5)
2. **Created** corrected workflow file: `mqtt-whatsapp-corrected-workflow.json`
3. **Fixed** the MQTT node:
   - Changed from: `n8n-nodes-base.mqtt`
   - Changed to: `n8n-nodes-base.mqttTrigger`
4. **Imported** new workflow via API

## New Workflow Details
- **Workflow ID**: `PptMUA3BfrivzhG9`
- **Name**: "MQTT Equipment Alert to WhatsApp (Fixed)"
- **Status**: Imported, ready for configuration
- **Trigger**: Proper MQTT Trigger node

## Configuration Required
To activate the workflow, you need to:

1. **Access n8n**: http://localhost:5678
2. **Open workflow**: "MQTT Equipment Alert to WhatsApp (Fixed)"
3. **Configure MQTT Trigger node**:
   - Host: `172.17.0.4`
   - Port: `1883`
   - Topics: `equipment/alerts,sensors/critical,actuators/fault`
   - Client ID: `n8n-mqtt-listener`
   - QoS: `1`
4. **Add Google Sheets credentials**:
   - Use service account: `server-claude@iiot-stack-automation.iam.gserviceaccount.com`
   - Upload credentials file from: `/home/server/google-sheets-credentials.json`
5. **Activate the workflow**

## Testing
Once configured and activated, test with:
```bash
./scripts/test_mqtt_whatsapp_workflow.sh
```

## Files Updated
- `STACK_CONFIG.md` - Updated with new workflow ID
- `mqtt-whatsapp-corrected-workflow.json` - Corrected workflow file
- `scripts/import_corrected_workflow.py` - Script used to fix the issue

## Lesson Learned
When importing workflows via API, ensure trigger nodes use the correct node types:
- ✅ `mqttTrigger` for MQTT listening
- ✅ `webhook` for HTTP webhooks  
- ✅ `cron` for scheduled triggers
- ❌ Regular action nodes won't work as triggers

The workflow should now activate successfully!