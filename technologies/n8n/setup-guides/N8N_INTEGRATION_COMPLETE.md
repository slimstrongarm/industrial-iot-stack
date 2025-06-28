# n8n Integration Complete - API Access Enabled

## Overview
The n8n workflow automation platform has been successfully deployed with PostgreSQL backend and API access enabled. Two critical workflows have been imported via API and are ready for configuration.

## Deployment Status ✅

### Infrastructure
- **n8n Container**: Running with PostgreSQL backend
- **Database**: PostgreSQL container (n8n-postgres)
- **Network**: Connected to bridge network for EMQX access
- **API**: Enabled and tested

### Access Details
- **Web Interface**: http://localhost:5678
- **API Endpoint**: http://localhost:5678/api/v1
- **API Key**: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxZjkyYWY0Ni01YmQ1LTQ0MTgtODdmZi1iMzBlZWU4NDI1YzYiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzQ4OTgwMDg0fQ.SzBoM46h15zLzepNuFgWV2cqCAgQSHVROvsgaFPzTC4`

## Imported Workflows

### 1. Formbricks to Google Sheets
- **Workflow ID**: n3UFERK5ilPYrLP3
- **Status**: Imported (needs configuration)
- **Purpose**: Capture form submissions and log to Google Sheets
- **Required Configuration**:
  - Google Sheets service account credentials
  - Webhook path configuration

### 2. MQTT Equipment Alert to WhatsApp
- **Workflow ID**: lwewtGRg3sFb9CX5
- **Status**: Imported (needs configuration)
- **Purpose**: Monitor MQTT topics for equipment alerts and send WhatsApp notifications
- **Required Configuration**:
  - MQTT connection (Host: 172.17.0.4, Port: 1883)
  - Google Sheets service account credentials
  - WhatsApp API credentials (optional)

## Configuration Requirements

### Google Sheets Credentials
Both workflows require Google Sheets access:
- **Service Account Email**: server-claude@iiot-stack-automation.iam.gserviceaccount.com
- **Credentials File**: `/home/server/google-sheets-credentials.json`
- **Spreadsheet ID**: 1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do

### MQTT Configuration
For the equipment alert workflow:
- **EMQX Broker IP**: 172.17.0.4
- **Port**: 1883
- **Topics**: 
  - equipment/alerts
  - sensors/critical
  - actuators/fault

## API Usage Examples

### List Workflows
```bash
curl -H "X-N8N-API-KEY: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxZjkyYWY0Ni01YmQ1LTQ0MTgtODdmZi1iMzBlZWU4NDI1YzYiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzQ4OTgwMDg0fQ.SzBoM46h15zLzepNuFgWV2cqCAgQSHVROvsgaFPzTC4" \
     http://localhost:5678/api/v1/workflows
```

### Get Workflow Details
```bash
curl -H "X-N8N-API-KEY: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxZjkyYWY0Ni01YmQ1LTQ0MTgtODdmZi1iMzBlZWU4NDI1YzYiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzQ4OTgwMDg0fQ.SzBoM46h15zLzepNuFgWV2cqCAgQSHVROvsgaFPzTC4" \
     http://localhost:5678/api/v1/workflows/lwewtGRg3sFb9CX5
```

### Python Integration
```python
import requests

headers = {
    'X-N8N-API-KEY': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxZjkyYWY0Ni01YmQ1LTQ0MTgtODdmZi1iMzBlZWU4NDI1YzYiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzQ4OTgwMDg0fQ.SzBoM46h15zLzepNuFgWV2cqCAgQSHVROvsgaFPzTC4',
    'Content-Type': 'application/json'
}

# Get all workflows
response = requests.get('http://localhost:5678/api/v1/workflows', headers=headers)
workflows = response.json()

# Execute a workflow
response = requests.post('http://localhost:5678/api/v1/executions', 
                        headers=headers,
                        json={'workflowId': 'lwewtGRg3sFb9CX5'})
```

## Testing

### Test MQTT Workflow
Once configured and activated:
```bash
./scripts/test_mqtt_whatsapp_workflow.sh
```

This will send test MQTT messages to trigger the alert workflow.

## Scripts Created

### API Import Scripts
- `/scripts/import_workflows_final.py` - Successfully imports workflows via API
- `/scripts/test_mqtt_whatsapp_workflow.sh` - Tests MQTT alert workflow
- `/scripts/n8n_api_import.py` - n8n API client implementation

### Configuration Files
- `STACK_CONFIG.md` - All service endpoints and credentials
- `N8N_API_ACCESS.md` - API documentation
- `docker-compose-n8n-stack.yml` - n8n deployment configuration

## Next Steps

1. **Manual Configuration Required**:
   - Access n8n UI at http://localhost:5678
   - Configure Google Sheets credentials for both workflows
   - Configure MQTT connection for alert workflow
   - Activate both workflows

2. **Pending Tasks**:
   - CT-008: Test MQTT→WhatsApp workflow
   - CT-010: Import MQTT Alert Bridge flow in Node-RED
   - CT-011: Import n8n Command Bridge flow in Node-RED
   - CT-016: Create Ignition scripts that call n8n API

## Troubleshooting

### Common Issues
1. **Workflow not triggering**: Check if workflow is activated
2. **MQTT connection failed**: Verify EMQX IP (172.17.0.4) is correct
3. **Google Sheets error**: Ensure service account has spreadsheet access

### Useful Commands
```bash
# Check n8n logs
docker logs -f n8n

# Restart n8n
docker-compose -f docker-compose-n8n-stack.yml restart

# Check EMQX connectivity
docker exec n8n ping 172.17.0.4
```

---
*Last updated: June 3, 2025*