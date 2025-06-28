# n8n API Access Documentation

## API Connection Details

**Base URL**: http://localhost:5678  
**Authentication**: API Key required (must be created via n8n UI)

## Available Endpoints

Based on testing, the following endpoints are available:
- `/rest/workflows` - Requires Basic Auth
- `/rest/executions` - Requires Basic Auth  
- `/rest/credentials` - Requires Basic Auth
- `/api/v1/workflows` - Requires X-N8N-API-KEY header
- `/api/v1/executions` - Requires X-N8N-API-KEY header

## Current Status

✅ n8n is running and accessible at http://localhost:5678  
⚠️ API endpoints require authentication:
- REST endpoints (`/rest/*`) - Need Basic Auth but return 401
- API v1 endpoints (`/api/v1/*`) - Need API Key in X-N8N-API-KEY header

## To Enable Full API Access

1. **Access n8n UI**: http://localhost:5678
   - Username: admin
   - Password: admin

2. **Create API Key**:
   - Go to Settings → API
   - Generate a new API key
   - Copy the key for use in API calls

3. **Use API Key in requests**:
   ```bash
   # With API key
   curl -H "X-N8N-API-KEY: YOUR_API_KEY" http://localhost:5678/api/v1/workflows
   ```

## Alternative: Manual Workflow Import

Since API key creation requires UI access, workflows can be imported manually:

1. Access n8n at http://localhost:5678
2. Click "Import from File"
3. Select workflow JSON files:
   - `formbricks-n8n-workflow-with-error-handling.json`
   - `mqtt-whatsapp-alert-workflow.json`

## For Mac-Claude Integration

Once an API key is created via the UI, Mac-Claude can use:

```python
import requests

headers = {
    'X-N8N-API-KEY': 'YOUR_API_KEY',
    'Content-Type': 'application/json'
}

# Get workflows
response = requests.get('http://localhost:5678/api/v1/workflows', headers=headers)

# Create workflow
response = requests.post('http://localhost:5678/api/v1/workflows', 
                        headers=headers, 
                        json=workflow_data)
```

## Summary

- n8n API is available but requires authentication
- API key must be created through the web UI
- Once created, full programmatic access is available
- Workflows are ready for import (either manual or via API)