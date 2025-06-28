#!/usr/bin/env python3
"""
Fix workflow format and import via n8n API
"""

import requests
import json
import sys
import os

# n8n API Configuration
N8N_URL = "http://localhost:5678"
API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxZjkyYWY0Ni01YmQ1LTQ0MTgtODdmZi1iMzBlZWU4NDI1YzYiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzQ4OTgwMDg0fQ.SzBoM46h15zLzepNuFgWV2cqCAgQSHVROvsgaFPzTC4"

def fix_workflow_format(workflow_data):
    """Fix workflow format for API compatibility"""
    
    # Create a clean workflow object with only required fields
    clean_workflow = {
        "name": workflow_data.get("name", "Imported Workflow"),
        "nodes": workflow_data.get("nodes", []),
        "connections": workflow_data.get("connections", {}),
        "settings": workflow_data.get("settings", {})
    }
    
    # Remove fields that cause issues
    fields_to_remove = ['active', 'versionId', 'updatedAt', 'id', 'createdAt', 'pinData', 'staticData', 'triggerCount']
    
    # Clean up nodes
    for node in clean_workflow["nodes"]:
        # Remove node IDs if present
        if "id" in node:
            del node["id"]
        # Fix credentials if present
        if "credentials" in node:
            for cred_type, cred_data in node["credentials"].items():
                if isinstance(cred_data, dict) and "id" in cred_data:
                    # Keep only the name, remove the ID
                    node["credentials"][cred_type] = None  # Will need to be configured in UI
    
    return clean_workflow

def import_workflow(workflow_file):
    """Import a workflow via n8n API with format fixes"""
    
    print(f"\n📤 Importing workflow: {workflow_file}")
    
    # Read workflow file
    if not os.path.exists(workflow_file):
        print(f"❌ File not found: {workflow_file}")
        return False
    
    with open(workflow_file, 'r') as f:
        workflow_data = json.load(f)
    
    # Fix the workflow format
    clean_workflow = fix_workflow_format(workflow_data)
    
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
            json=clean_workflow,
            timeout=30
        )
        
        if response.status_code in [200, 201]:
            result = response.json()
            workflow_id = result.get('id', 'unknown')
            print(f"✅ Workflow imported successfully!")
            print(f"   Workflow ID: {workflow_id}")
            print(f"   Name: {clean_workflow.get('name', 'Unnamed')}")
            print(f"   ⚠️  Note: Credentials need to be configured in the UI")
            return True
        else:
            print(f"❌ Import failed with status: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            
            # If it's a validation error, show what fields are problematic
            if response.status_code == 400:
                try:
                    error_data = response.json()
                    if 'message' in error_data:
                        print(f"   Error: {error_data['message']}")
                except:
                    pass
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
    
    print("🚀 n8n Workflow Import via API (Fixed Format)")
    print("=" * 45)
    
    # Test API connection
    print("\n🔍 Testing API connection...")
    initial_workflows = list_workflows()
    
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
    final_workflows = list_workflows()
    
    if success_count > 0:
        print("\n⚠️  Important: Imported workflows need configuration!")
        print("\n📝 Required Configuration:")
        print("1. Google Sheets credentials (service account)")
        print("2. MQTT connection settings:")
        print("   - Host: 172.17.0.4")
        print("   - Port: 1883")
        print("3. WhatsApp API credentials (if using)")
        print("\nAccess n8n at http://localhost:5678 to configure")
    
    print("\n✅ Import process complete!")

if __name__ == "__main__":
    main()