# Formbricks → n8n → Google Sheets Setup Guide

## ✅ What's Ready

1. **Google Sheets** - Two new tabs created:
   - `Form Submissions` - For successful form data
   - `Form Errors` - For error logging
   - Sheet ID: `1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do`

2. **n8n Workflow** - Complete flow with error handling:
   - File: `formbricks-to-sheets-final.json`
   - Webhook endpoint: `/webhook/formbricks-form-webhook`
   - Automatic field mapping
   - Error logging

## 🚀 Setup Steps

### 1. Deploy n8n (if not already running)
```bash
docker run -d \
  --name n8n \
  -p 5678:5678 \
  -v n8n_data:/home/node/.n8n \
  n8nio/n8n
```

### 2. Access n8n
- URL: `http://localhost:5678`
- Create account on first access

### 3. Set up Google Sheets Credentials
1. Go to Credentials → Add Credential → Google Sheets API
2. Choose "Service Account" method
3. Upload the JSON key: `credentials/iot-stack-credentials.json`
4. Name it: "IoT Stack Sheets"
5. Test the connection

### 4. Import the Workflow
1. Go to Workflows → Import from File
2. Select: `n8n-flows/formbricks-to-sheets-final.json`
3. Open the imported workflow

### 5. Update Webhook URL
1. Click on "Formbricks Webhook" node
2. Copy the webhook URL (will look like: `http://your-server:5678/webhook/formbricks-form-webhook`)

### 6. Activate the Workflow
- Click "Active" toggle in top bar
- Workflow is now listening for form submissions

### 7. Configure Formbricks
1. Go to your Formbricks form settings
2. Add webhook integration
3. Paste the n8n webhook URL
4. Select trigger: "On Response Created"
5. Save

## 📊 Form Fields Mapping

The workflow automatically maps these common industrial fields:
- `equipment_id` → Equipment ID
- `operator_name` → Operator
- `shift` → Shift
- `issue_type` → Issue Type
- `severity` → Severity
- `description` → Description
- `location` → Location
- `action_taken` → Action Taken
- `follow_up_required` → Follow Up Required

## 🧪 Testing

### Test Payload for n8n
```json
{
  "id": "TEST-001",
  "surveyId": "equipment-inspection",
  "responses": {
    "equipment_id": "PUMP-01",
    "operator_name": "Test Operator",
    "shift": "Day Shift",
    "issue_type": "Routine Check",
    "severity": "Low",
    "description": "Test submission from n8n",
    "location": "Test Area",
    "action_taken": "None required",
    "follow_up_required": "No"
  }
}
```

### Manual Test in n8n
1. Open the workflow
2. Click "Execute Workflow"
3. Click on Webhook node
4. Click "Listen for Test Event"
5. Send test data via curl:
```bash
curl -X POST http://localhost:5678/webhook/formbricks-form-webhook \
  -H "Content-Type: application/json" \
  -d '{"responses":{"equipment_id":"TEST-01","operator_name":"Test"}}'
```

## 🎯 Industrial Use Cases

1. **Equipment Inspection Forms**
   - Daily checks
   - Issue reporting
   - Maintenance requests

2. **Quality Control Forms**
   - Product inspections
   - Defect reporting
   - Compliance checks

3. **Safety Reports**
   - Incident reporting
   - Near-miss documentation
   - Safety observations

4. **Production Forms**
   - Shift handover
   - Downtime reporting
   - Production counts

## 🔍 Monitoring

- Check `Form Submissions` tab for new entries
- Check `Form Errors` tab if submissions fail
- n8n execution history shows all attempts

## 🆘 Troubleshooting

1. **No data in sheets**
   - Check n8n workflow is Active
   - Verify webhook URL in Formbricks
   - Check Form Errors tab

2. **Authentication errors**
   - Verify Google Sheets credentials
   - Ensure service account has edit access

3. **Field mapping issues**
   - Check actual field names from Formbricks
   - Update the "Process Form Data" node

Ready to collect industrial data! 🏭📊