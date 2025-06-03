# 🚀 n8n API Capabilities & Integration

## ✅ **YES! n8n Has a Full REST API**

### **🔑 Key API Features:**

1. **Workflow Management**
   - List all workflows
   - Get workflow details
   - Activate/deactivate workflows
   - Create/update workflows programmatically
   - Delete workflows

2. **Execution Control**
   - Execute workflows via API
   - Monitor execution status
   - Get execution history
   - Retrieve execution details
   - Cancel running executions

3. **Monitoring & Health**
   - Health check endpoint (`/healthz`)
   - Execution statistics
   - Workflow activation status
   - Error tracking

### **🔧 API Endpoints:**

```bash
# Health Check
GET /healthz

# Workflows
GET    /api/v1/workflows              # List all workflows
GET    /api/v1/workflows/{id}         # Get specific workflow
POST   /api/v1/workflows              # Create workflow
PATCH  /api/v1/workflows/{id}         # Update workflow (activate/deactivate)
DELETE /api/v1/workflows/{id}         # Delete workflow

# Executions
GET    /api/v1/executions             # List executions
GET    /api/v1/executions/{id}        # Get execution details
POST   /api/v1/workflows/{id}/execute # Execute workflow
DELETE /api/v1/executions/{id}        # Delete execution

# Webhook Execution (alternative)
POST   /webhook/{workflow_id}         # Execute via webhook
```

### **🔐 Authentication:**

**Basic Auth (current setup):**
```python
session.auth = ("iiot-admin", "StrongPassword123!")
```

**API Key (when enabled):**
```python
headers = {"X-N8N-API-KEY": "your-api-key"}
```

### **📱 Real-World Integration Examples:**

#### **1. Trigger Alert from Python:**
```python
import requests

# Trigger WhatsApp alert workflow
response = requests.post(
    "http://server:5678/api/v1/workflows/{workflow_id}/execute",
    auth=("iiot-admin", "StrongPassword123!"),
    json={
        "data": {
            "alertType": "Temperature Threshold",
            "equipmentId": "Boiler_1",
            "severity": "Critical",
            "value": "225°F"
        }
    }
)
```

#### **2. Monitor Workflow Health:**
```python
# Get all active workflows
response = requests.get(
    "http://server:5678/api/v1/workflows",
    auth=("iiot-admin", "password")
)

workflows = response.json()['data']
active_count = sum(1 for w in workflows if w['active'])
print(f"Active workflows: {active_count}/{len(workflows)}")
```

#### **3. Auto-Recovery System:**
```python
# Check for failed executions and retry
executions = client.get_executions(limit=10)
for execution in executions:
    if execution['finished'] and execution.get('data', {}).get('resultData', {}).get('error'):
        print(f"Retrying failed workflow: {execution['workflowId']}")
        client.execute_workflow(execution['workflowId'])
```

### **🎯 Integration with Our Stack:**

#### **Ignition → n8n:**
```python
# In Ignition script
import system.net

# Trigger n8n workflow on alarm
def onAlarmActive(alarmEvent):
    payload = {
        "alertType": str(alarmEvent.displayPath),
        "severity": str(alarmEvent.priority),
        "value": str(alarmEvent.value),
        "timestamp": str(alarmEvent.activeTime)
    }
    
    system.net.httpPost(
        "http://server:5678/webhook/mqtt-whatsapp-alerts",
        payload
    )
```

#### **Node-RED → n8n:**
```javascript
// HTTP Request node configuration
msg.url = "http://server:5678/api/v1/workflows/mqtt-alerts/execute";
msg.method = "POST";
msg.headers = {
    "Authorization": "Basic " + Buffer.from("iiot-admin:password").toString('base64')
};
msg.payload = {
    data: msg.payload  // Pass alert data
};
return msg;
```

#### **n8n → Everything:**
- Execute Python scripts
- Call REST APIs
- Update databases
- Send notifications
- Trigger other workflows

### **📊 Unified Monitoring Benefits:**

1. **Single Dashboard View:**
   - Google Sheets task progress
   - n8n workflow health
   - Execution success rates
   - Real-time alerts

2. **Automated Responses:**
   - Retry failed workflows
   - Scale based on load
   - Alert on anomalies
   - Chain workflows

3. **Audit Trail:**
   - Every execution logged
   - Parameter tracking
   - Error analysis
   - Performance metrics

### **🚀 Next Level Integration:**

```python
# Complete monitoring loop
monitor = UnifiedMonitor()

# If Server Claude completes workflow import
if task_status['CT-007'] == 'Complete':
    # Automatically test the workflow
    monitor.n8n_client.execute_workflow('mqtt-whatsapp-alerts', test_data)
    
    # Update Google Sheets with test result
    monitor.update_task('CT-008', 'In Progress')
    
    # Monitor execution result
    execution = monitor.wait_for_execution()
    if execution['status'] == 'success':
        monitor.update_task('CT-008', 'Complete')
        print("🎉 Full integration test passed!")
```

### **💡 Pro Tips:**

1. **Use Environment Variables:**
   ```bash
   export N8N_URL="http://100.94.84.126:5678"
   export N8N_USERNAME="iiot-admin"
   export N8N_PASSWORD="your-password"
   ```

2. **Enable API Key Auth** (more secure than basic auth):
   - Set `N8N_API_KEY_AUTH_ACTIVE=true` in n8n
   - Generate API keys for different services

3. **Webhook URLs** are perfect for:
   - Ignition HTTP calls
   - Node-RED HTTP nodes
   - External integrations

4. **Rate Limiting:**
   - n8n handles rate limiting automatically
   - Monitor `/metrics` endpoint for performance

**The n8n API transforms it from a workflow tool into a full integration platform!** 🚀