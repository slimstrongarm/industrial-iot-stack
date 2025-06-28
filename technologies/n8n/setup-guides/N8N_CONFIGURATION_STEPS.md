# n8n Configuration Steps - MQTT to WhatsApp & Sheets

## ✅ Completed Steps
1. **MQTT Connection**: Working with `host.docker.internal`
2. **Google Sheets**: Created "Equipment Alerts" and "All Equipment Events" sheets
3. **Workflow Import**: MQTT→WhatsApp workflow is imported (ID: PptMUA3BfrivzhG9)

## 🔧 Configuration Required

### Step 1: Configure Google Sheets Credentials in n8n

1. **Access n8n**: http://localhost:5678
2. **Go to Credentials**: Settings → Credentials
3. **Add New Credential**:
   - Type: "Google Sheets Service Account"
   - Name: "IIOT-GoogleSheets"
   - Service Account Email: `server-claude@iiot-stack-automation.iam.gserviceaccount.com`
   - Private Key: Upload `/home/server/google-sheets-credentials.json`

4. **Test Connection**: Save and test the credential

### Step 2: Update MQTT Workflow with Correct Host

1. **Open Workflow**: MQTT Equipment Alert to WhatsApp (Fixed)
2. **Edit MQTT Trigger Node**:
   - Change Host from `172.17.0.4` to `host.docker.internal`
   - Keep Port: 1883
   - Keep Topics: `equipment/alerts,sensors/critical,actuators/fault`

### Step 3: Configure Google Sheets Nodes

1. **Edit "Log to Google Sheets" Node**:
   - Credential: Select "IIOT-GoogleSheets" 
   - Document ID: `1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do`
   - Sheet Name: `Equipment Alerts`
   - Operation: Append

2. **Edit "Log All Equipment Events" Node**:
   - Credential: Select "IIOT-GoogleSheets"
   - Document ID: `1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do`
   - Sheet Name: `All Equipment Events`
   - Operation: Append

### Step 4: Test Google Sheets Logging (Before WhatsApp)

1. **Activate Workflow**: Turn on the MQTT workflow
2. **Send Test Message**:
```bash
mosquitto_pub -h localhost -p 1883 -t "equipment/alerts" -m '{"equipmentId":"TEST-001","type":"test_sensor","location":"Lab","value":75,"threshold":70,"description":"Test alert message"}'
```

3. **Check Google Sheets**: Verify data appears in both sheets
4. **Check n8n Execution Log**: Look for any errors

### Step 5: Configure WhatsApp (Optional for Testing)

#### Option A: Use Webhook.site for Testing
1. **Go to**: https://webhook.site
2. **Copy your unique URL**
3. **Edit "Send WhatsApp Alert" Node**:
   - Method: POST
   - URL: Your webhook.site URL
   - Body: `{"message": "{{$json.whatsappMessage}}", "severity": "{{$json.severity}}"}`

#### Option B: Use Real WhatsApp API
1. **Set up Meta WhatsApp Business API**
2. **Get Access Token and Phone Number**
3. **Update node with real credentials**

## 🧪 Test Commands

### Test Critical Alert (Triggers WhatsApp)
```bash
mosquitto_pub -h localhost -p 1883 -t "sensors/critical" -m '{"equipmentId":"TEMP-001","type":"temperature_sensor","location":"Reactor Room","value":95,"threshold":85,"description":"Critical temperature exceeded"}'
```

### Test Warning Alert (Triggers WhatsApp)
```bash
mosquitto_pub -h localhost -p 1883 -t "equipment/alerts" -m '{"equipmentId":"MOTOR-005","type":"servo_motor","location":"Conveyor Belt","value":78,"threshold":75,"description":"Vibration levels elevated"}'
```

### Test Info Level (Only Logs to Sheets)
```bash
mosquitto_pub -h localhost -p 1883 -t "equipment/status" -m '{"equipmentId":"VALVE-003","type":"control_valve","location":"Process Line 2","value":"normal","description":"Routine status check"}'
```

## 📋 Expected Results

### Google Sheets Logging
- **Equipment Alerts Sheet**: Only critical/warning alerts that trigger WhatsApp
- **All Equipment Events Sheet**: Every MQTT message received

### WhatsApp Alerts  
- **Critical/Warning Only**: Based on topic keywords or severity level
- **Formatted Message**: Equipment ID, location, timestamp, severity

## 🔍 Troubleshooting

### Google Sheets Not Working
1. Check credentials are properly uploaded
2. Verify sheet names match exactly
3. Check n8n execution logs for API errors

### MQTT Not Triggering
1. Verify `host.docker.internal` is used (not localhost or IP)
2. Check workflow is activated
3. Test MQTT connection with mosquitto client

### WhatsApp Errors
1. Start with webhook.site testing
2. Check API credentials and phone number format
3. Verify Meta WhatsApp API setup

## ✅ Success Confirmation

When working correctly, you should see:
1. **n8n Execution History**: Successful workflow runs
2. **Google Sheets**: New rows with MQTT data
3. **WhatsApp/Webhook**: Alert messages for critical/warning events

Ready to start configuration?