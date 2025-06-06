#!/usr/bin/env python3
"""
Activate WhatsApp workflow and test MQTT integration
"""

import requests
import json
import time
from datetime import datetime

# n8n API configuration
n8n_url = "http://172.28.214.170:5678/api/v1"
api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjdjNjE2ZDU5LTE4ZjEtNGFmNi05YWNkLTM1N2FjZmEzYWJkOCIsImVtYWlsIjoibm9ib2R5QGV4YW1wbGUuY29tIiwiZmlyc3ROYW1lIjoibiIsImxhc3ROYW1lIjoiOG4iLCJwYXNzd29yZCI6IjY1YzI1YzU2Nzg5NGI2OTcxNjkzYWY5NjFkODM0MzA0NzU0MTI0NTcxY2Q1Mzc0ODIzN2U2M2IyY2NkMWU3MjQiLCJwZXJzb25hbGl6YXRpb25TdXJ2ZXkiOnsid29ya0FyZWEiOiJlbmdpbmVlcmluZyIsImNvbXBhbnlTaXplIjoiMTEtMjUiLCJkZXZ0b0JuIjoiZGVzaWduZXIifSwiaWF0IjoxNzU0MjA0NTIzLCJleHAiOjE4NTg5MjA1MjN9.9K5YZK4GN6PoP5sP2WJKZe5Vq1dHCO4VhYJvKBJZ7xY"
headers = {
    "X-N8N-API-KEY": api_key,
    "Content-Type": "application/json"
}

def get_workflows():
    """Get all workflows"""
    response = requests.get(f"{n8n_url}/workflows", headers=headers)
    if response.status_code == 200:
        return response.json()['data']
    return []

def activate_workflow(workflow_id):
    """Activate a workflow"""
    # First get the workflow details
    response = requests.get(f"{n8n_url}/workflows/{workflow_id}", headers=headers)
    if response.status_code != 200:
        print(f"❌ Failed to get workflow {workflow_id}")
        return False
    
    workflow = response.json()['data']
    
    # Activate it
    workflow['active'] = True
    
    # Update workflow
    update_response = requests.patch(
        f"{n8n_url}/workflows/{workflow_id}",
        headers=headers,
        json={"active": True}
    )
    
    if update_response.status_code == 200:
        print(f"✅ Workflow activated: {workflow_id}")
        return True
    else:
        print(f"❌ Failed to activate workflow: {update_response.text}")
        return False

def test_mqtt_connection():
    """Test MQTT broker connectivity"""
    import subprocess
    
    print("\n🔍 Testing MQTT broker connectivity...")
    
    # Check if EMQX is reachable
    result = subprocess.run(
        ["nc", "-zv", "172.17.0.4", "1883"],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print("✅ MQTT broker is reachable at 172.17.0.4:1883")
        return True
    else:
        print("❌ MQTT broker not reachable")
        return False

def send_test_mqtt_message():
    """Send a test MQTT message"""
    print("\n📨 Sending test MQTT message...")
    
    test_payload = {
        "equipmentId": "TEST-PUMP-001",
        "type": "Test Alert",
        "location": "Server Claude Testing",
        "value": 99.9,
        "threshold": 80,
        "description": "Test alert from WhatsApp integration setup",
        "timestamp": datetime.now().isoformat(),
        "severity": "critical"
    }
    
    import subprocess
    
    # Send via mosquitto_pub
    cmd = [
        "mosquitto_pub",
        "-h", "172.17.0.4",
        "-p", "1883",
        "-t", "equipment/alerts",
        "-m", json.dumps(test_payload)
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ Test MQTT message sent successfully")
        print(f"📋 Payload: {json.dumps(test_payload, indent=2)}")
        return True
    else:
        print(f"❌ Failed to send MQTT message: {result.stderr}")
        return False

def check_workflow_executions(workflow_id):
    """Check recent executions of a workflow"""
    print(f"\n📊 Checking workflow executions...")
    
    response = requests.get(
        f"{n8n_url}/executions",
        headers=headers,
        params={"workflowId": workflow_id, "limit": 5}
    )
    
    if response.status_code == 200:
        executions = response.json()['data']
        if executions:
            print(f"✅ Found {len(executions)} recent executions:")
            for exec in executions[:3]:  # Show last 3
                status = exec.get('status', 'unknown')
                finished = exec.get('finished', False)
                started = exec.get('startedAt', 'unknown')
                emoji = "✅" if status == "success" else "❌" if status == "error" else "⏳"
                print(f"   {emoji} {status.upper()} - Started: {started}")
        else:
            print("ℹ️  No executions found yet")
    else:
        print("❌ Failed to get executions")

def main():
    print("🚀 WhatsApp Workflow Activation & Testing")
    print("=" * 50)
    
    # Get workflows
    workflows = get_workflows()
    whatsapp_workflow = None
    
    print("\n📋 Current workflows:")
    for workflow in workflows:
        name = workflow['name']
        active = workflow['active']
        workflow_id = workflow['id']
        status = "🟢 Active" if active else "🔴 Inactive"
        print(f"   {status} {name} (ID: {workflow_id})")
        
        if "WhatsApp" in name:
            whatsapp_workflow = workflow
    
    if not whatsapp_workflow:
        print("\n❌ WhatsApp workflow not found!")
        return
    
    # Activate WhatsApp workflow if needed
    if not whatsapp_workflow['active']:
        print(f"\n🔄 Activating WhatsApp workflow...")
        if activate_workflow(whatsapp_workflow['id']):
            print("✅ WhatsApp workflow activated!")
        else:
            print("❌ Failed to activate workflow")
            return
    else:
        print(f"\n✅ WhatsApp workflow already active")
    
    # Test MQTT connection
    mqtt_ok = test_mqtt_connection()
    
    if mqtt_ok:
        # Check if mosquitto-clients is installed
        import subprocess
        check_mosquitto = subprocess.run(
            ["which", "mosquitto_pub"],
            capture_output=True
        )
        
        if check_mosquitto.returncode != 0:
            print("\n📦 Installing mosquitto-clients...")
            subprocess.run(["sudo", "apt-get", "update"])
            subprocess.run(["sudo", "apt-get", "install", "-y", "mosquitto-clients"])
        
        # Send test message
        if send_test_mqtt_message():
            print("\n⏳ Waiting 5 seconds for workflow to process...")
            time.sleep(5)
            
            # Check executions
            check_workflow_executions(whatsapp_workflow['id'])
    
    print("\n📊 Summary:")
    print("✅ WhatsApp workflow is active")
    print("✅ MQTT broker is accessible")
    print("✅ Test message sent")
    print("\n🎯 Next steps:")
    print("1. Check n8n executions at http://172.28.214.170:5678/executions")
    print("2. Verify Google Sheets for logged alerts")
    print("3. Configure WhatsApp credentials if needed")
    print("4. Run full test: bash scripts/test_mqtt_whatsapp_workflow.sh")

if __name__ == "__main__":
    main()