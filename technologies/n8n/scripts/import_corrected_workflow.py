#!/usr/bin/env python3
"""
Import the corrected MQTT workflow with proper trigger
"""

import requests
import json

# n8n API Configuration
N8N_URL = "http://localhost:5678"
API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxZjkyYWY0Ni01YmQ1LTQ0MTgtODdmZi1iMzBlZWU4NDI1YzYiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzQ4OTgwMDg0fQ.SzBoM46h15zLzepNuFgWV2cqCAgQSHVROvsgaFPzTC4"

def delete_workflow(workflow_id):
    """Delete existing workflow"""
    headers = {'X-N8N-API-KEY': API_KEY}
    
    try:
        response = requests.delete(f"{N8N_URL}/api/v1/workflows/{workflow_id}", headers=headers)
        if response.status_code == 200:
            print(f"✅ Deleted workflow: {workflow_id}")
            return True
        else:
            print(f"❌ Failed to delete workflow: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error deleting workflow: {e}")
        return False

def import_corrected_workflow():
    """Import the corrected workflow"""
    
    # Read corrected workflow
    with open('mqtt-whatsapp-corrected-workflow.json', 'r') as f:
        workflow_data = json.load(f)
    
    headers = {
        'X-N8N-API-KEY': API_KEY,
        'Content-Type': 'application/json'
    }
    
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
            print(f"✅ Corrected workflow imported!")
            print(f"   ID: {workflow_id}")
            print(f"   Name: {workflow_data.get('name')}")
            return workflow_id
        else:
            print(f"❌ Import failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error importing workflow: {e}")
        return None

def main():
    """Main function"""
    
    print("🔧 Replacing MQTT Workflow with Corrected Version")
    print("=" * 50)
    
    # Delete the old problematic workflow
    old_workflow_id = "lwewtGRg3sFb9CX5"
    print(f"🗑️  Deleting old workflow: {old_workflow_id}")
    
    if delete_workflow(old_workflow_id):
        print("✅ Old workflow deleted")
    else:
        print("⚠️  Could not delete old workflow (might not exist)")
    
    # Import the corrected workflow
    print("\n📤 Importing corrected workflow...")
    new_id = import_corrected_workflow()
    
    if new_id:
        print(f"\n✅ Success! New workflow imported with ID: {new_id}")
        print("\n📋 Next steps:")
        print("1. Go to n8n at http://localhost:5678")
        print("2. Open 'MQTT Equipment Alert to WhatsApp (Fixed)' workflow")
        print("3. Configure MQTT connection (Host: 172.17.0.4, Port: 1883)")
        print("4. Add Google Sheets credentials")
        print("5. Activate the workflow")
        print("6. Test with: ./scripts/test_mqtt_whatsapp_workflow.sh")
        print("\n🔧 The workflow now has a proper MQTT Trigger node!")
    else:
        print("\n❌ Failed to import corrected workflow")

if __name__ == "__main__":
    main()