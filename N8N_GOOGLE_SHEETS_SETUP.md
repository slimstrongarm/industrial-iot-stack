# n8n Google Sheets Credential Configuration

## Step-by-Step Setup

### 1. Access n8n Interface
- **URL**: http://localhost:5678
- **Username**: admin
- **Password**: admin

### 2. Navigate to Credentials
1. Click **Settings** (gear icon) in the left sidebar
2. Click **Credentials**
3. Click **+ Add Credential** (top right)

### 3. Create Google Sheets Service Account Credential
1. **Search for**: "Google Sheets"
2. **Select**: "Google Sheets Service Account"
3. **Fill in the details**:
   - **Credential Name**: `IIOT-GoogleSheets`
   - **Service Account Email**: `server-claude@iiot-stack-automation.iam.gserviceaccount.com`
   - **Private Key**: Upload the JSON file content

### 4. Upload Service Account JSON
The service account JSON file should be at: `/home/server/google-sheets-credentials.json`

**JSON Structure** (for reference):
```json
{
  "type": "service_account",
  "project_id": "iiot-stack-automation",
  "private_key_id": "...",
  "private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n",
  "client_email": "server-claude@iiot-stack-automation.iam.gserviceaccount.com",
  "client_id": "...",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token"
}
```

### 5. Test the Credential
1. **Save** the credential
2. Click **Test** to verify connection
3. Should show **"Connection successful"**

### 6. Configure Workflow Nodes

#### Edit "Log to Google Sheets" Node:
1. Open the **MQTT Equipment Alert to WhatsApp (Fixed)** workflow
2. Click on **"Log to Google Sheets"** node
3. **Parameters**:
   - **Credential**: Select `IIOT-GoogleSheets`
   - **Document ID**: `1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do`
   - **Sheet Name**: `Equipment Alerts`
   - **Operation**: Append
   - **Data Mode**: Auto-map input data
4. **Save** the node

#### Edit "Log All Equipment Events" Node:
1. Click on the second Google Sheets node
2. **Parameters**:
   - **Credential**: Select `IIOT-GoogleSheets`
   - **Document ID**: `1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do`
   - **Sheet Name**: `All Equipment Events`
   - **Operation**: Append
   - **Data Mode**: Auto-map input data
3. **Save** the node

### 7. Update MQTT Trigger Host
1. Click on **"MQTT Trigger"** node
2. **Parameters**:
   - **Host**: Change to `host.docker.internal`
   - **Port**: 1883
   - **Topics**: `equipment/alerts,sensors/critical,actuators/fault`
3. **Save** the node

### 8. Save and Activate Workflow
1. **Save** the workflow (Ctrl+S)
2. **Activate** the workflow (toggle switch in top right)
3. Should show **"Active"** status

## 🧪 Test the Setup

### Run Test Script
```bash
./scripts/test_mqtt_sheets_flow.sh
```

### Manual Test
```bash
mosquitto_pub -h localhost -p 1883 -t "equipment/alerts" -m '{"equipmentId":"TEST-001","type":"test_sensor","location":"Test Lab","value":75,"threshold":70,"description":"Test configuration"}'
```

### Check Results
1. **n8n Executions**: http://localhost:5678/executions
2. **Google Sheets**: https://docs.google.com/spreadsheets/d/1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do
   - Check "Equipment Alerts" sheet
   - Check "All Equipment Events" sheet

## 🔍 Troubleshooting

### Common Issues:
1. **"Invalid credentials"**: Verify JSON file is correctly formatted
2. **"Permission denied"**: Ensure service account has access to the spreadsheet
3. **"Sheet not found"**: Verify sheet names match exactly
4. **"Connection failed"**: Check if Google Sheets API is enabled

### Success Indicators:
- ✅ Credential test passes
- ✅ Workflow shows "Active" status
- ✅ Test MQTT message creates entries in both sheets
- ✅ n8n execution history shows successful runs

Ready to start? Go to http://localhost:5678 and follow the steps above!