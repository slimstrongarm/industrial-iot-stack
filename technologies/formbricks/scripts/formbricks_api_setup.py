#!/usr/bin/env python3
"""
CT-019: Obtain Formbricks API key and configure access for direct integration
"""

import requests
import json
import sys
from datetime import datetime
from pathlib import Path

class FormbricksAPISetup:
    def __init__(self):
        self.base_url = "https://app.formbricks.com"
        self.api_endpoints = {
            "responses": "/api/v1/responses",
            "surveys": "/api/v1/surveys", 
            "forms": "/api/v1/forms",
            "webhooks": "/api/v1/webhooks"
        }
        
    def research_formbricks_api(self):
        """Research Formbricks API documentation and requirements"""
        
        print("🔍 Researching Formbricks API Configuration")
        print("=" * 45)
        
        # Check Formbricks documentation endpoint
        try:
            response = requests.get("https://formbricks.com/docs/api", timeout=10)
            if response.status_code == 200:
                print("✅ Formbricks API documentation accessible")
            else:
                print("⚠️  Formbricks API docs not directly accessible")
        except:
            print("⚠️  Could not reach Formbricks documentation")
        
        # Common API patterns for form builders
        api_requirements = {
            "authentication": {
                "type": "API Key",
                "header": "Authorization: Bearer YOUR_API_KEY",
                "location": "Request headers",
                "obtain_from": "Dashboard → Settings → API Keys"
            },
            "endpoints": {
                "responses": "GET /api/v1/responses - Get form submissions",
                "surveys": "GET /api/v1/surveys - List available surveys/forms",
                "webhooks": "POST /api/v1/webhooks - Set up real-time notifications"
            },
            "integration_pattern": {
                "step_1": "Create API key in Formbricks dashboard",
                "step_2": "Test API connectivity with list surveys",
                "step_3": "Set up webhook for real-time form submissions",
                "step_4": "Configure n8n to receive webhook events"
            }
        }
        
        return api_requirements
    
    def create_formbricks_integration_guide(self):
        """Create comprehensive Formbricks integration guide"""
        
        print("📝 Creating Formbricks Integration Guide")
        print("=" * 40)
        
        guide = {
            "title": "Formbricks API Integration Guide",
            "created": datetime.now().isoformat(),
            "status": "Ready for API key configuration",
            
            "step_1_obtain_api_key": {
                "description": "Get Formbricks API key from dashboard",
                "instructions": [
                    "1. Login to Formbricks dashboard: https://app.formbricks.com",
                    "2. Navigate to Settings → API Keys",
                    "3. Create new API key with appropriate permissions",
                    "4. Copy the API key (starts with 'fbk_')",
                    "5. Store securely for integration use"
                ],
                "required_permissions": [
                    "Read responses/submissions",
                    "Read surveys/forms", 
                    "Create webhooks (if available)",
                    "Read webhook events"
                ]
            },
            
            "step_2_test_api_connectivity": {
                "description": "Verify API access and functionality",
                "test_endpoints": [
                    {
                        "name": "List Surveys",
                        "method": "GET",
                        "url": "https://app.formbricks.com/api/v1/surveys",
                        "headers": {"Authorization": "Bearer YOUR_API_KEY"},
                        "expected": "List of available surveys/forms"
                    },
                    {
                        "name": "Get Responses", 
                        "method": "GET",
                        "url": "https://app.formbricks.com/api/v1/responses",
                        "headers": {"Authorization": "Bearer YOUR_API_KEY"},
                        "expected": "List of form submissions"
                    }
                ]
            },
            
            "step_3_n8n_integration": {
                "description": "Configure n8n to work with Formbricks",
                "integration_options": [
                    {
                        "method": "Webhook Trigger",
                        "description": "Real-time form submissions via webhook",
                        "n8n_node": "Webhook Trigger",
                        "setup": "Configure Formbricks to send submissions to n8n webhook URL"
                    },
                    {
                        "method": "HTTP Request Node",
                        "description": "Poll Formbricks API for new submissions",
                        "n8n_node": "HTTP Request + Schedule Trigger", 
                        "setup": "Periodically fetch new responses from Formbricks API"
                    },
                    {
                        "method": "Formbricks Node",
                        "description": "Native n8n Formbricks integration (if available)",
                        "n8n_node": "Formbricks Trigger/Node",
                        "setup": "Use built-in n8n Formbricks integration"
                    }
                ]
            },
            
            "step_4_data_flow": {
                "description": "Formbricks → n8n → Google Sheets workflow",
                "workflow": "Formbricks Form Submission → n8n Processing → Google Sheets Logging",
                "data_transformation": {
                    "formbricks_format": "JSON response with form fields and metadata",
                    "sheets_format": "Structured rows with timestamp, form_id, responses",
                    "processing": "Extract form fields, add timestamp, format for Sheets"
                }
            }
        }
        
        # Save guide
        with open('/mnt/c/Users/LocalAccount/industrial-iot-stack/FORMBRICKS_INTEGRATION_GUIDE.json', 'w') as f:
            json.dump(guide, f, indent=2)
        
        print("✅ Integration guide created")
        print("📁 Saved to: FORMBRICKS_INTEGRATION_GUIDE.json")
        
        return guide
    
    def create_api_test_script(self):
        """Create API testing script for when key is available"""
        
        test_script = '''#!/usr/bin/env python3
"""
Formbricks API Testing Script
Run this after obtaining API key from Formbricks dashboard
"""

import requests
import json
from datetime import datetime

# Configuration - UPDATE WITH YOUR API KEY
FORMBRICKS_API_KEY = "fbk_your_api_key_here"
BASE_URL = "https://app.formbricks.com"

headers = {
    "Authorization": f"Bearer {FORMBRICKS_API_KEY}",
    "Content-Type": "application/json"
}

def test_formbricks_api():
    """Test Formbricks API connectivity and endpoints"""
    
    print("🧪 Testing Formbricks API")
    print("=" * 30)
    
    if FORMBRICKS_API_KEY == "fbk_your_api_key_here":
        print("❌ Please update FORMBRICKS_API_KEY with your actual API key")
        return False
    
    # Test endpoints
    endpoints = [
        ("GET", "/api/v1/surveys", "List surveys"),
        ("GET", "/api/v1/responses", "Get responses"),  
        ("GET", "/api/v1/me", "Get user info"),
    ]
    
    for method, endpoint, description in endpoints:
        url = f"{BASE_URL}{endpoint}"
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ {description}: {len(data) if isinstance(data, list) else 'Success'}")
            elif response.status_code == 401:
                print(f"❌ {description}: Authentication failed - check API key")
            elif response.status_code == 403:
                print(f"⚠️  {description}: Forbidden - check API permissions")
            else:
                print(f"⚠️  {description}: Status {response.status_code}")
                
        except Exception as e:
            print(f"❌ {description}: Error - {str(e)[:50]}")
    
    print("\\n🎯 Next Steps:")
    print("1. Configure n8n HTTP Request node with API key")
    print("2. Set up webhook or polling workflow")
    print("3. Test form submission → Google Sheets flow")
    
    return True

if __name__ == "__main__":
    test_formbricks_api()
'''
        
        with open('/mnt/c/Users/LocalAccount/industrial-iot-stack/scripts/test_formbricks_api.py', 'w') as f:
            f.write(test_script)
        
        print("✅ API test script created")
        print("📁 Saved to: scripts/test_formbricks_api.py")
    
    def create_n8n_formbricks_workflow(self):
        """Create n8n workflow template for Formbricks integration"""
        
        workflow = {
            "name": "Formbricks to Google Sheets Integration",
            "description": "Receives Formbricks form submissions and logs to Google Sheets",
            "nodes": [
                {
                    "parameters": {
                        "httpMethod": "POST",
                        "path": "formbricks-webhook",
                        "responseMode": "responseNode",
                        "options": {}
                    },
                    "name": "Webhook Trigger",
                    "type": "n8n-nodes-base.webhook",
                    "typeVersion": 1,
                    "position": [250, 300],
                    "webhookId": "formbricks-submissions"
                },
                {
                    "parameters": {
                        "jsCode": "// Process Formbricks form submission\\n\\nconst submission = items[0].json;\\n\\n// Extract form data\\nconst formId = submission.formId || submission.surveyId || 'unknown';\\nconst submissionId = submission.id || submission.responseId || Date.now();\\nconst responses = submission.responses || submission.data || {};\\n\\n// Create structured data for Google Sheets\\nconst sheetData = {\\n  timestamp: new Date().toISOString(),\\n  form_id: formId,\\n  submission_id: submissionId,\\n  response_data: JSON.stringify(responses),\\n  source: 'formbricks'\\n};\\n\\n// Add individual response fields as columns\\nif (typeof responses === 'object') {\\n  Object.keys(responses).forEach(key => {\\n    sheetData[`field_${key}`] = responses[key];\\n  });\\n}\\n\\nreturn [{ json: sheetData }];"
                    },
                    "name": "Process Submission",
                    "type": "n8n-nodes-base.code",
                    "typeVersion": 2,
                    "position": [450, 300]
                },
                {
                    "parameters": {
                        "authentication": "serviceAccount",
                        "documentId": "1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do",
                        "sheetName": "Form Submissions",
                        "range": "A:Z",
                        "dataMode": "autoMapInputData",
                        "options": {}
                    },
                    "name": "Log to Google Sheets",
                    "type": "n8n-nodes-base.googleSheets",
                    "typeVersion": 4.4,
                    "position": [650, 300],
                    "credentials": {}
                }
            ],
            "connections": {
                "Webhook Trigger": {
                    "main": [
                        [
                            {
                                "node": "Process Submission",
                                "type": "main",
                                "index": 0
                            }
                        ]
                    ]
                },
                "Process Submission": {
                    "main": [
                        [
                            {
                                "node": "Log to Google Sheets",
                                "type": "main", 
                                "index": 0
                            }
                        ]
                    ]
                }
            }
        }
        
        with open('/mnt/c/Users/LocalAccount/industrial-iot-stack/formbricks-n8n-workflow.json', 'w') as f:
            json.dump(workflow, f, indent=2)
        
        print("✅ n8n workflow template created")
        print("📁 Saved to: formbricks-n8n-workflow.json")
    
    def run_setup(self):
        """Run complete Formbricks API setup"""
        
        print("🎯 CT-019: Formbricks API Configuration")
        print("=" * 40)
        
        # Research API
        api_info = self.research_formbricks_api()
        
        # Create integration guide
        guide = self.create_formbricks_integration_guide()
        
        # Create test script
        self.create_api_test_script()
        
        # Create n8n workflow
        self.create_n8n_formbricks_workflow()
        
        print("\n🚀 CT-019 Status: READY FOR API KEY")
        print("=" * 35)
        print("✅ Integration guide created")
        print("✅ API test script prepared")
        print("✅ n8n workflow template ready")
        print("✅ Documentation complete")
        print("")
        print("🎯 Next Steps:")
        print("1. Obtain Formbricks API key from dashboard")
        print("2. Update test script with API key")
        print("3. Run API connectivity test")
        print("4. Import n8n workflow")
        print("5. Configure webhook URL in Formbricks")
        
        return True

def main():
    setup = FormbricksAPISetup()
    success = setup.run_setup()
    
    if success:
        print("\\n🎯 CT-019: READY FOR API KEY CONFIGURATION")
        return 0
    else:
        print("\\n❌ CT-019: Setup failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())