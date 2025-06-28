#!/usr/bin/env python3
"""
Import n8n workflows using the API
"""

import requests
import json
import sys
import os

# n8n API Configuration
N8N_URL = "http://localhost:5678"
API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxZjkyYWY0Ni01YmQ1LTQ0MTgtODdmZi1iMzBlZWU4NDI1YzYiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzQ4OTgwMDg0fQ.SzBoM46h15zLzepNuFgWV2cqCAgQSHVROvsgaFPzTC4"

def import_workflow(workflow_file):
    """Import a workflow via n8n API"""
    
    print(f"\n📤 Importing workflow: {workflow_file}")
    
    # Read workflow file
    if not os.path.exists(workflow_file):
        print(f"❌ File not found: {workflow_file}")
        return False
    
    with open(workflow_file, 'r') as f:
        workflow_data = json.load(f)
    
    # Prepare the workflow data
    # Ensure required fields
    if 'active' not in workflow_data:
        workflow_data['active'] = False
    if 'settings' not in workflow_data:
        workflow_data['settings'] = {}
    
    # Prepare headers
    headers = {
        'X-N8N-API-KEY': API_KEY,
        'Content-Type': 'application/json'
    }
    
    # Import the workflow
    try:
        response = requests.post(
            f"{N8N_URL}/api/v1/workflows",
            headers=headers,
            json=workflow_data,
            timeout=30
        )
        
        if response.status_code in [200, 201]:
            result = response.json()
            workflow_id = result.get('id', 'unknown')
            print(f"✅ Workflow imported successfully!")
            print(f"   Workflow ID: {workflow_id}")
            print(f"   Name: {workflow_data.get('name', 'Unnamed')}")
            return True
        else:
            print(f"❌ Import failed with status: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error importing workflow: {e}")
        return False

def list_workflows():
    """List all workflows via API"""
    
    headers = {
        'X-N8N-API-KEY': API_KEY
    }
    
    try:
        response = requests.get(
            f"{N8N_URL}/api/v1/workflows",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            workflows = data.get('data', [])
            print(f"\n📋 Found {len(workflows)} workflows:")
            for wf in workflows:
                status = "🟢 Active" if wf.get('active') else "🔴 Inactive"
                print(f"   - {wf.get('name')} (ID: {wf.get('id')}) {status}")
            return workflows
        else:
            print(f"❌ Failed to list workflows: {response.status_code}")
            return []
    except Exception as e:
        print(f"❌ Error listing workflows: {e}")
        return []

def main():
    """Main function"""
    
    print("🚀 n8n Workflow Import via API")
    print("=" * 40)
    
    # Test API connection
    print("\n🔍 Testing API connection...")
    workflows = list_workflows()
    
    # Workflow files to import
    workflow_files = [
        'formbricks-n8n-workflow-with-error-handling.json',
        'mqtt-whatsapp-alert-workflow.json'
    ]
    
    # Import each workflow
    success_count = 0
    for wf_file in workflow_files:
        if import_workflow(wf_file):
            success_count += 1
    
    # Show final status
    print(f"\n📊 Import Summary:")
    print(f"   Total workflows: {len(workflow_files)}")
    print(f"   Successfully imported: {success_count}")
    print(f"   Failed: {len(workflow_files) - success_count}")
    
    # List all workflows again
    print("\n📋 Final workflow list:")
    list_workflows()
    
    print("\n✅ Import process complete!")
    print("\nNext steps:")
    print("1. Access n8n at http://localhost:5678")
    print("2. Configure credentials for Google Sheets and MQTT")
    print("3. Activate the workflows")
    print("4. Run the test script: ./scripts/test_mqtt_whatsapp_workflow.sh")

if __name__ == "__main__":
    main()