# Formbricks → n8n → Google Sheets Integration Guide

## Overview
This POC connects Formbricks forms to Google Sheets via n8n workflow automation.

## Architecture
```
[Formbricks Form] → [Webhook] → [n8n Workflow] → [Google Sheets]
```

## Prerequisites
- Formbricks instance (cloud or self-hosted)
- n8n instance (cloud or self-hosted)
- Google account with Sheets API access
- Google Sheets for data collection

## Step 1: Create Google Sheet

1. Create a new Google Sheet named "Formbricks Form Responses"
2. Set up columns based on your form fields:
   ```
   | Timestamp | Form ID | Response ID | Question 1 | Question 2 | ... |
   ```

## Step 2: Set up Google Sheets API Access

Use the same credentials file we already have:
- `/Users/joshpayneair/Desktop/industrial-iot-stack/credentials/iot-stack-credentials.json`

## Step 3: Create n8n Workflow

```json
{
  "name": "Formbricks to Google Sheets",
  "nodes": [
    {
      "parameters": {
        "httpMethod": "POST",
        "path": "formbricks-webhook",
        "responseMode": "onReceived",
        "responseData": "allEntries"
      },
      "name": "Webhook",
      "type": "n8n-nodes-base.webhook",
      "typeVersion": 1,
      "position": [250, 300],
      "webhookId": "formbricks-form-webhook"
    },
    {
      "parameters": {
        "authentication": "serviceAccount",
        "serviceAccount": "credentials-file",
        "operation": "append",
        "sheetId": "YOUR_SHEET_ID",
        "range": "Sheet1!A:Z",
        "options": {
          "valueInputMode": "USER_ENTERED"
        },
        "dataMode": "autoMapInputData"
      },
      "name": "Google Sheets",
      "type": "n8n-nodes-base.googleSheets",
      "typeVersion": 2,
      "position": [650, 300],
      "credentials": {
        "googleSheetsApi": {
          "id": "1",
          "name": "Google Sheets Account"
        }
      }
    },
    {
      "parameters": {
        "jsCode": "// Extract form data and format for Google Sheets\nconst formData = items[0].json;\nconst timestamp = new Date().toISOString();\n\n// Extract form responses\nconst responses = formData.data?.responses || formData.responses || {};\n\n// Build row data\nconst rowData = {\n  timestamp: timestamp,\n  formId: formData.surveyId || formData.formId || 'unknown',\n  responseId: formData.responseId || formData.id || 'unknown'\n};\n\n// Add each response as a column\nObject.keys(responses).forEach(key => {\n  const response = responses[key];\n  if (typeof response === 'object') {\n    rowData[key] = JSON.stringify(response);\n  } else {\n    rowData[key] = response;\n  }\n});\n\nreturn [{\n  json: rowData\n}];"
      },
      "name": "Format Data",
      "type": "n8n-nodes-base.code",
      "typeVersion": 1,
      "position": [450, 300]
    }
  ],
  "connections": {
    "Webhook": {
      "main": [
        [{
          "node": "Format Data",
          "type": "main",
          "index": 0
        }]
      ]
    },
    "Format Data": {
      "main": [
        [{
          "node": "Google Sheets",
          "type": "main",
          "index": 0
        }]
      ]
    }
  }
}
```

## Step 4: Configure Formbricks Webhook

1. In Formbricks, go to your form settings
2. Add a webhook integration
3. Set the webhook URL to: `https://your-n8n-instance.com/webhook/formbricks-webhook`
4. Select events: "Response Created" and/or "Response Updated"

## Step 5: Set up n8n Google Sheets Credentials

1. In n8n, go to Credentials
2. Add new credential → Google Sheets API
3. Choose "Service Account" method
4. Upload the JSON key file from credentials folder
5. Test the connection

## Step 6: Industrial IoT Use Cases

This integration is perfect for:
- **Operator Feedback Forms**: Collect operator input about equipment performance
- **Quality Control Checklists**: Digital forms for QC inspections
- **Maintenance Reports**: Technician reports from the field
- **Safety Incident Reporting**: Quick incident documentation
- **Production Surveys**: Shift handover information

## Example Form Fields for IIoT

```javascript
// Equipment Inspection Form
{
  "equipmentId": "Select equipment",
  "operatorName": "Your name",
  "shiftTime": "Shift (Day/Night)",
  "equipmentStatus": "Operating normally? (Yes/No)",
  "issuesFound": "Describe any issues",
  "maintenanceNeeded": "Maintenance required? (Yes/No)",
  "photos": "Upload photos (optional)",
  "additionalNotes": "Additional comments"
}
```

## Testing the Integration

1. Create a test form in Formbricks
2. Submit a test response
3. Check n8n workflow execution
4. Verify data appears in Google Sheets

## Monitoring and Alerts

Add these nodes to your n8n workflow for better monitoring:
- Error handling node
- Email notification on failures
- Slack notification for new submissions
- Data validation before sheet insertion

Need help implementing any specific part?