#!/usr/bin/env python3
"""
Fix the MQTT workflow to have proper trigger node
"""

import requests
import json

# n8n API Configuration
N8N_URL = "http://localhost:5678"
API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxZjkyYWY0Ni01YmQ1LTQ0MTgtODdmZi1iMzBlZWU4NDI1YzYiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzQ4OTgwMDg0fQ.SzBoM46h15zLzepNuFgWV2cqCAgQSHVROvsgaFPzTC4"

def get_workflow(workflow_id):
    """Get workflow details"""
    headers = {'X-N8N-API-KEY': API_KEY}
    
    try:
        response = requests.get(f"{N8N_URL}/api/v1/workflows/{workflow_id}", headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to get workflow: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error getting workflow: {e}")
        return None

def update_workflow(workflow_id, workflow_data):
    """Update workflow with fixed MQTT trigger"""
    headers = {
        'X-N8N-API-KEY': API_KEY,
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.put(
            f"{N8N_URL}/api/v1/workflows/{workflow_id}",
            headers=headers,
            json=workflow_data
        )
        
        if response.status_code == 200:
            print("✅ Workflow updated successfully!")
            return True
        else:
            print(f"❌ Update failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error updating workflow: {e}")
        return False

def fix_mqtt_trigger_node(workflow_data):
    """Fix the MQTT node to be a proper trigger"""
    
    # Find the MQTT node
    mqtt_node = None
    for node in workflow_data.get('nodes', []):
        if node.get('name') == 'MQTT Listen':
            mqtt_node = node
            break
    
    if not mqtt_node:
        print("❌ MQTT Listen node not found")
        return workflow_data
    
    print("🔧 Fixing MQTT node to be a trigger...")
    
    # Update the MQTT node to use the trigger version
    mqtt_node.update({
        "type": "n8n-nodes-base.mqttTrigger",
        "typeVersion": 1,
        "parameters": {
            "host": "172.17.0.4",
            "port": 1883,
            "topics": "equipment/alerts,sensors/critical,actuators/fault",
            "clientId": "n8n-mqtt-listener",
            "qos": 1,
            "messageFormat": "json",
            "options": {}
        }
    })
    
    # Remove credentials if present (they need to be set in UI)
    if "credentials" in mqtt_node:
        mqtt_node["credentials"] = {}
    
    print("✅ MQTT node converted to trigger")
    return workflow_data

def main():
    """Main function to fix the MQTT workflow"""
    
    print("🔧 Fixing MQTT Equipment Alert Workflow")
    print("=" * 40)
    
    workflow_id = "lwewtGRg3sFb9CX5"
    
    # Get current workflow
    print("📥 Getting current workflow...")
    workflow = get_workflow(workflow_id)
    
    if not workflow:
        print("❌ Could not retrieve workflow")
        return
    
    print(f"✅ Retrieved workflow: {workflow.get('name')}")
    
    # Fix the MQTT trigger
    fixed_workflow = fix_mqtt_trigger_node(workflow)
    
    # Update the workflow
    print("📤 Updating workflow...")
    if update_workflow(workflow_id, fixed_workflow):
        print("\n✅ MQTT workflow fixed successfully!")
        print("\n📋 Next steps:")
        print("1. Go to n8n at http://localhost:5678")
        print("2. Open the 'MQTT Equipment Alert to WhatsApp' workflow")
        print("3. Configure MQTT connection credentials if needed")
        print("4. Try activating the workflow again")
        print("\n🔧 MQTT Configuration:")
        print("   Host: 172.17.0.4")
        print("   Port: 1883")
        print("   Topics: equipment/alerts,sensors/critical,actuators/fault")
    else:
        print("\n❌ Failed to fix workflow")

if __name__ == "__main__":
    main()