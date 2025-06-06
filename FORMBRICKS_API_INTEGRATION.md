# 🚀 Formbricks API Integration Guide

## ✅ **YES! Formbricks Has a Full REST API**

### **🔑 Key API Features:**

1. **Survey Management**
   - Create, read, update, delete surveys
   - Manage questions, logic, and settings
   - Configure triggers and targeting

2. **Response Management**
   - Retrieve all survey responses
   - Filter by date, user, survey
   - Real-time response data access

3. **User Management**
   - Manage user profiles and attributes
   - Track user sessions and interactions
   - Segment users for targeted surveys

4. **Analytics & Metrics**
   - Survey performance statistics
   - Completion rates and drop-off analysis
   - Response analytics and insights

5. **Webhook Integration**
   - Real-time response notifications
   - Configurable webhook endpoints
   - Event-driven integrations

### **🔧 API Endpoints:**

```bash
# Base URL (adjust for self-hosted)
BASE_URL="https://app.formbricks.com/api/v1"

# Surveys
GET    /api/v1/surveys                    # List all surveys
GET    /api/v1/surveys/{surveyId}         # Get specific survey
POST   /api/v1/surveys                    # Create survey
PUT    /api/v1/surveys/{surveyId}         # Update survey
DELETE /api/v1/surveys/{surveyId}         # Delete survey

# Responses
GET    /api/v1/responses                  # List all responses
GET    /api/v1/responses/{responseId}     # Get specific response
GET    /api/v1/surveys/{surveyId}/responses # Get survey responses

# Users/People
GET    /api/v1/people                     # List users
GET    /api/v1/people/{userId}            # Get specific user
POST   /api/v1/people                     # Create user
PUT    /api/v1/people/{userId}            # Update user

# Webhooks
POST   /api/v1/webhooks                   # Create webhook
GET    /api/v1/webhooks                   # List webhooks
DELETE /api/v1/webhooks/{webhookId}       # Delete webhook
```

### **🔐 Authentication:**

**API Key Authentication:**
```bash
# Headers required for all API calls
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json
```

**Get API Key:**
1. Go to Formbricks Settings
2. Navigate to API Keys section
3. Generate new API key
4. Store securely for integration

### **📡 Webhook Integration:**

**Webhook Configuration:**
```json
{
  "url": "https://your-server.com/webhook/formbricks",
  "triggers": ["responseCreated", "responseUpdated"],
  "surveyIds": ["survey_123", "survey_456"]
}
```

**Webhook Payload Example:**
```json
{
  "event": "responseCreated",
  "data": {
    "responseId": "resp_123",
    "surveyId": "survey_456",
    "userId": "user_789",
    "responses": {
      "equipment_id": "PUMP-01",
      "operator_name": "John Smith",
      "issue_type": "Maintenance Required",
      "severity": "High",
      "description": "Unusual noise from pump motor"
    },
    "createdAt": "2025-06-03T12:00:00Z",
    "completedAt": "2025-06-03T12:05:00Z"
  }
}
```

### **🔄 Integration Architecture Options:**

#### **Option 1: Direct API Integration**
```
[Formbricks] → [Python/Node.js Script] → [Google Sheets] → [Ignition]
```

**Benefits:**
- Lower latency (no n8n middleware)
- Custom business logic
- Advanced error handling
- Higher throughput

#### **Option 2: Hybrid Integration** (Recommended)
```
[Formbricks] → [Webhook] → [n8n] → [WhatsApp/Sheets]
            → [API] → [Custom Scripts] → [Ignition]
```

**Benefits:**
- Best of both worlds
- n8n for simple workflows
- Direct API for complex operations
- Scalable architecture

#### **Option 3: Pure API Integration**
```
[Formbricks API] → [Custom Dashboard] → [Real-time Analytics]
```

### **🎯 Industrial IoT Use Cases:**

#### **1. Equipment Inspection Forms**
```python
# Get all equipment inspection responses
import requests

headers = {
    'Authorization': 'Bearer YOUR_API_KEY',
    'Content-Type': 'application/json'
}

response = requests.get(
    'https://app.formbricks.com/api/v1/surveys/equipment-inspection/responses',
    headers=headers,
    params={
        'filter[createdAt][gte]': '2025-06-01',
        'filter[status]': 'completed'
    }
)

inspections = response.json()
```

#### **2. Real-time Maintenance Alerts**
```python
# Webhook handler for urgent maintenance requests
@app.route('/webhook/formbricks', methods=['POST'])
def handle_maintenance_request():
    data = request.json
    
    if data['event'] == 'responseCreated':
        responses = data['data']['responses']
        
        # Check for urgent maintenance
        if responses.get('severity') == 'Critical':
            # Direct API call to n8n for immediate alert
            trigger_emergency_workflow(responses)
            
            # Also log to database
            log_maintenance_request(responses)
    
    return {'status': 'success'}
```

#### **3. Custom Quality Dashboard**
```python
# Build real-time quality metrics dashboard
def get_quality_metrics():
    # Get all quality control responses from last 24 hours
    responses = formbricks_api.get_responses(
        survey_id='quality-control',
        since=datetime.now() - timedelta(hours=24)
    )
    
    # Calculate metrics
    total_checks = len(responses)
    passed_checks = len([r for r in responses if r['result'] == 'Pass'])
    quality_rate = (passed_checks / total_checks) * 100
    
    return {
        'quality_rate': quality_rate,
        'total_checks': total_checks,
        'failed_checks': total_checks - passed_checks
    }
```

### **🚀 Advanced Integration Examples:**

#### **1. Smart Form Routing**
```python
# Route forms based on equipment type and severity
def route_inspection_form(response_data):
    equipment_type = response_data['equipment_type']
    severity = response_data['severity']
    
    if equipment_type == 'boiler' and severity == 'critical':
        # Immediate escalation
        trigger_emergency_response(response_data)
    elif severity == 'high':
        # Schedule maintenance
        create_work_order(response_data)
    else:
        # Log for trending
        update_maintenance_log(response_data)
```

#### **2. Automated Survey Creation**
```python
# Create surveys programmatically based on equipment
def create_equipment_survey(equipment_id, equipment_type):
    survey_config = {
        'name': f'{equipment_type} Inspection - {equipment_id}',
        'questions': [
            {
                'type': 'rating',
                'text': f'Rate the condition of {equipment_id}',
                'scale': 10
            },
            {
                'type': 'text',
                'text': 'Describe any issues observed',
                'required': False
            },
            {
                'type': 'select',
                'text': 'Action required?',
                'options': ['None', 'Routine Maintenance', 'Urgent Repair']
            }
        ]
    }
    
    response = formbricks_api.create_survey(survey_config)
    return response['surveyId']
```

#### **3. Response Analytics Engine**
```python
# Advanced analytics on form responses
def analyze_maintenance_trends():
    # Get 30 days of maintenance responses
    responses = formbricks_api.get_responses(
        survey_id='maintenance-forms',
        since=datetime.now() - timedelta(days=30)
    )
    
    # Analyze trends
    equipment_issues = {}
    for response in responses:
        equipment = response['equipment_id']
        issue_type = response['issue_type']
        
        if equipment not in equipment_issues:
            equipment_issues[equipment] = {}
        
        if issue_type not in equipment_issues[equipment]:
            equipment_issues[equipment][issue_type] = 0
        
        equipment_issues[equipment][issue_type] += 1
    
    # Identify equipment needing attention
    high_maintenance_equipment = [
        eq for eq, issues in equipment_issues.items()
        if sum(issues.values()) > 5  # More than 5 issues in 30 days
    ]
    
    return {
        'trends': equipment_issues,
        'attention_needed': high_maintenance_equipment
    }
```

### **📊 Integration with Our Stack:**

#### **Update n8n Workflows:**
```javascript
// Add Formbricks API node to existing workflows
// Can fetch specific responses or create new surveys
const formbricksResponse = await formbricksApi.getResponse(responseId);

// Enrich the data before sending to WhatsApp
const enrichedAlert = {
    ...mqttData,
    formData: formbricksResponse,
    operator: formbricksResponse.operator_name,
    timestamp: formbricksResponse.completedAt
};
```

#### **Direct Ignition Integration:**
```python
# Ignition script to fetch recent inspections
def getRecentInspections(equipment_id):
    headers = {
        'Authorization': 'Bearer ' + system.tag.readBlocking('[default]Formbricks_API_Key')[0].value
    }
    
    url = f"https://app.formbricks.com/api/v1/responses?filter[equipment_id]={equipment_id}"
    response = system.net.httpGet(url, headers=headers)
    
    if response.good:
        data = system.util.jsonDecode(response.text)
        return data['responses']
    else:
        return []
```

### **💡 Pro Tips:**

1. **Rate Limiting**: Formbricks API has rate limits - implement proper throttling
2. **Caching**: Cache frequently accessed survey definitions
3. **Error Handling**: Implement retry logic for failed API calls
4. **Security**: Store API keys securely in environment variables
5. **Monitoring**: Track API usage and response times

### **🔄 Next Steps:**

1. **Get Formbricks API Key** from your Formbricks instance
2. **Test API endpoints** with our Python client
3. **Create hybrid integration** combining webhooks + direct API
4. **Build custom analytics dashboard** for industrial data
5. **Integrate with Ignition scripts** for real-time operations

**The Formbricks API opens up powerful possibilities for custom industrial workflows!** 🏭⚡📊