#!/usr/bin/env python3
"""
CT-013/CT-014: n8n API Access and Workflow Import
This script provides n8n API access and workflow import functionality
"""

import requests
from requests.auth import HTTPBasicAuth
import json
import base64
import sys
import os

# n8n Configuration
N8N_URL = "http://localhost:5678"
USERNAME = "admin"
PASSWORD = "admin"

class N8NAPIClient:
    def __init__(self, base_url, username, password):
        self.base_url = base_url.rstrip('/')
        self.auth = HTTPBasicAuth(username, password)
        self.session = requests.Session()
        self.session.auth = self.auth
        self.api_key = None
        
    def test_connection(self):
        """Test connection to n8n"""
        print("🔍 Testing n8n connection...")
        try:
            # Try the main page with auth
            response = self.session.get(f"{self.base_url}/", timeout=5)
            if response.status_code in [200, 302]:
                print("✅ n8n is accessible")
                return True
            else:
                print(f"❌ n8n returned status: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Connection error: {e}")
            return False
    
    def get_api_endpoints(self):
        """Discover available API endpoints"""
        print("\n🔍 Discovering API endpoints...")
        
        # Common n8n API endpoints to try
        endpoints = [
            "/rest/workflows",
            "/rest/executions", 
            "/rest/credentials",
            "/api/v1/workflows",
            "/api/v1/executions",
            "/workflows",
            "/executions"
        ]
        
        available = []
        for endpoint in endpoints:
            try:
                response = self.session.get(f"{self.base_url}{endpoint}", timeout=3)
                if response.status_code in [200, 401]:
                    available.append(endpoint)
                    print(f"✅ Found endpoint: {endpoint}")
            except:
                pass
        
        return available
    
    def import_workflow_via_api(self, workflow_file):
        """Import workflow using n8n API"""
        print(f"\n📤 Importing workflow: {workflow_file}")
        
        # Read workflow file
        if not os.path.exists(workflow_file):
            print(f"❌ File not found: {workflow_file}")
            return False
            
        with open(workflow_file, 'r') as f:
            workflow_data = json.load(f)
        
        # Add required fields if missing
        if 'active' not in workflow_data:
            workflow_data['active'] = False
        if 'settings' not in workflow_data:
            workflow_data['settings'] = {}
        
        # Try different endpoints
        endpoints = [
            "/rest/workflows",
            "/api/v1/workflows",
            "/workflows"
        ]
        
        for endpoint in endpoints:
            try:
                print(f"   Trying endpoint: {endpoint}")
                response = self.session.post(
                    f"{self.base_url}{endpoint}",
                    json=workflow_data,
                    headers={'Content-Type': 'application/json'},
                    timeout=10
                )
                
                if response.status_code in [200, 201]:
                    print(f"✅ Workflow imported successfully via {endpoint}")
                    result = response.json()
                    if 'id' in result:
                        print(f"   Workflow ID: {result['id']}")
                    return True
                else:
                    print(f"   Failed with status: {response.status_code}")
                    if response.text:
                        print(f"   Response: {response.text[:200]}")
            except Exception as e:
                print(f"   Error: {e}")
        
        return False
    
    def create_api_access_doc(self):
        """Create documentation for API access"""
        doc_content = f"""# n8n API Access Documentation

## API Connection Details

**Base URL**: {self.base_url}
**Authentication**: Basic Auth
**Username**: {USERNAME}
**Password**: {PASSWORD}

## Available Endpoints

Based on testing, the following endpoints are available:
"""
        
        endpoints = self.get_api_endpoints()
        for endpoint in endpoints:
            doc_content += f"- `{endpoint}`\n"
        
        doc_content += """
## Example API Calls

### Using curl:
```bash
# Get workflows
curl -u admin:admin http://localhost:5678/rest/workflows

# Get executions
curl -u admin:admin http://localhost:5678/rest/executions
```

### Using Python:
```python
import requests
from requests.auth import HTTPBasicAuth

auth = HTTPBasicAuth('admin', 'admin')
response = requests.get('http://localhost:5678/rest/workflows', auth=auth)
workflows = response.json()
```

### Using the n8n API Client:
```python
from n8n_api_import import N8NAPIClient

client = N8NAPIClient('http://localhost:5678', 'admin', 'admin')
client.test_connection()
client.import_workflow_via_api('workflow.json')
```

## Workflow Import

To import workflows programmatically:

1. Ensure the workflow JSON includes:
   - `active: false` (can be activated later)
   - `settings: {}` (even if empty)

2. Use the API client:
   ```python
   client.import_workflow_via_api('mqtt-whatsapp-alert-workflow.json')
   ```

## Notes

- The n8n REST API uses Basic Authentication
- Workflows are imported in inactive state by default
- After import, workflows need to be configured and activated via the UI
"""
        
        with open('N8N_API_ACCESS.md', 'w') as f:
            f.write(doc_content)
        
        print(f"\n📄 Created API documentation: N8N_API_ACCESS.md")

def main():
    """Main function to test and document n8n API"""
    print("🔐 n8n API Access Configuration (CT-013/CT-014)")
    print("=" * 50)
    
    # Create API client
    client = N8NAPIClient(N8N_URL, USERNAME, PASSWORD)
    
    # Test connection
    if not client.test_connection():
        print("\n❌ Could not connect to n8n. Please ensure it's running.")
        sys.exit(1)
    
    # Discover endpoints
    endpoints = client.get_api_endpoints()
    
    if not endpoints:
        print("\n⚠️  No API endpoints found. n8n might need configuration for API access.")
    
    # Create documentation
    client.create_api_access_doc()
    
    # Try to import workflows
    workflow_files = [
        'formbricks-n8n-workflow-with-error-handling.json',
        'mqtt-whatsapp-alert-workflow.json'
    ]
    
    print("\n📤 Attempting to import workflows...")
    for wf_file in workflow_files:
        if os.path.exists(wf_file):
            client.import_workflow_via_api(wf_file)
        else:
            print(f"⚠️  Workflow file not found: {wf_file}")
    
    print("\n✅ API configuration complete!")
    print("\n📋 Connection Details for Mac-Claude:")
    print(f"URL: {N8N_URL}")
    print(f"Auth: Basic Auth (username: {USERNAME}, password: {PASSWORD})")
    print("See N8N_API_ACCESS.md for full documentation")

if __name__ == "__main__":
    main()