#!/usr/bin/env python3
"""
Final workflow import script with proper API format
"""

import requests
import json
import sys
import os

# n8n API Configuration
N8N_URL = "http://localhost:5678"
API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxZjkyYWY0Ni01YmQ1LTQ0MTgtODdmZi1iMzBlZWU4NDI1YzYiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzQ4OTgwMDg0fQ.SzBoM46h15zLzepNuFgWV2cqCAgQSHVROvsgaFPzTC4"

def prepare_workflow_for_import(workflow_data):
    """Prepare workflow for API import"""
    
    # Extract only the required fields
    clean_workflow = {
        "name": workflow_data.get("name", "Imported Workflow"),
        "nodes": workflow_data.get("nodes", []),
        "connections": workflow_data.get("connections", {}),
        "settings": {}  # Must be empty object, not the settings from file
    }
    
    # Clean nodes - remove credentials references as they need to be set up fresh
    for node in clean_workflow["nodes"]:
        if "credentials" in node:
            # Clear credential references - they'll need to be configured in UI
            node["credentials"] = {}
    
    return clean_workflow

def import_workflow(workflow_file):
    """Import a workflow via n8n API"""
    
    print(f"\n📤 Importing: {workflow_file}")
    
    # Read workflow file
    if not os.path.exists(workflow_file):
        print(f"❌ File not found: {workflow_file}")
        return False
    
    with open(workflow_file, 'r') as f:
        workflow_data = json.load(f)
    
    # Prepare workflow for import
    import_data = prepare_workflow_for_import(workflow_data)
    
    # Log what we're importing
    print(f"   Name: {import_data['name']}")
    print(f"   Nodes: {len(import_data['nodes'])}")
    
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
            json=import_data,
            timeout=30
        )
        
        if response.status_code in [200, 201]:
            result = response.json()
            workflow_id = result.get('id', 'unknown')
            print(f"✅ Successfully imported!")
            print(f"   ID: {workflow_id}")
            print(f"   Status: Inactive (needs configuration)")
            return workflow_id
        else:
            print(f"❌ Import failed: {response.status_code}")
            error_msg = response.json().get('message', response.text[:200])
            print(f"   Error: {error_msg}")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def configure_workflow_notes(workflow_id, workflow_name):
    """Add configuration notes to help with setup"""
    
    config_notes = {
        "Formbricks to Google Sheets with Error Handling": {
            "credentials": ["Google Sheets (Service Account)"],
            "configuration": [
                "1. Add Google Sheets credentials using service account JSON",
                "2. Set the correct Sheet ID in Google Sheets nodes",
                "3. Configure webhook path if needed"
            ]
        },
        "MQTT Equipment Alert to WhatsApp": {
            "credentials": ["Google Sheets (Service Account)"],
            "configuration": [
                "1. Configure MQTT connection:",
                "   - Host: 172.17.0.4",
                "   - Port: 1883",
                "   - Topics: equipment/alerts,sensors/critical,actuators/fault",
                "2. Add Google Sheets credentials",
                "3. Configure WhatsApp API (if available)",
                "4. Update spreadsheet ID: 1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do"
            ]
        }
    }
    
    if workflow_name in config_notes:
        print(f"\n📝 Configuration needed for '{workflow_name}':")
        notes = config_notes[workflow_name]
        
        if "credentials" in notes:
            print("\n   Credentials required:")
            for cred in notes["credentials"]:
                print(f"   • {cred}")
        
        if "configuration" in notes:
            print("\n   Configuration steps:")
            for step in notes["configuration"]:
                print(f"   {step}")

def list_workflows():
    """List all workflows"""
    
    headers = {'X-N8N-API-KEY': API_KEY}
    
    try:
        response = requests.get(f"{N8N_URL}/api/v1/workflows", headers=headers)
        if response.status_code == 200:
            data = response.json()
            workflows = data.get('data', [])
            return workflows
        return []
    except:
        return []

def main():
    """Main import function"""
    
    print("🚀 n8n Workflow Import - Final Version")
    print("=" * 40)
    
    # Check current workflows
    print("\n📋 Current workflows:")
    existing = list_workflows()
    for wf in existing:
        print(f"   - {wf.get('name')} (ID: {wf.get('id')})")
    
    # Workflow files to import
    workflow_files = [
        'formbricks-n8n-workflow-with-error-handling.json',
        'mqtt-whatsapp-alert-workflow.json'
    ]
    
    # Import workflows
    imported_workflows = []
    for wf_file in workflow_files:
        workflow_id = import_workflow(wf_file)
        if workflow_id:
            # Read workflow name for configuration notes
            with open(wf_file, 'r') as f:
                wf_data = json.load(f)
                wf_name = wf_data.get('name', 'Unknown')
            
            imported_workflows.append((workflow_id, wf_name))
            configure_workflow_notes(workflow_id, wf_name)
    
    # Summary
    print(f"\n📊 Import Summary:")
    print(f"   Attempted: {len(workflow_files)}")
    print(f"   Successful: {len(imported_workflows)}")
    
    if imported_workflows:
        print("\n✅ Workflows imported successfully!")
        print("\n🔧 Next steps:")
        print("1. Go to http://localhost:5678")
        print("2. Open each workflow")
        print("3. Configure the credentials and settings as noted above")
        print("4. Activate the workflows")
        print("5. Test with: ./scripts/test_mqtt_whatsapp_workflow.sh")
        
        print("\n📌 Quick Reference:")
        print("   EMQX IP: 172.17.0.4")
        print("   Google Sheets ID: 1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do")
        print("   Service Account: server-claude@iiot-stack-automation.iam.gserviceaccount.com")
    else:
        print("\n❌ No workflows were imported. Please check the errors above.")

if __name__ == "__main__":
    main()