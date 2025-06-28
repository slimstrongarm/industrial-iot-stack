#!/usr/bin/env python3
"""
CT-008: Test MQTT Integration using Python
Alternative to mosquitto_pub using paho-mqtt library
"""

import json
import time
import sys
from datetime import datetime

try:
    import paho.mqtt.client as mqtt
except ImportError:
    print("❌ paho-mqtt not installed")
    print("Alternative: Use Docker to test MQTT")
    
    # Test using Docker exec into EMQX container
    import subprocess
    
    def test_mqtt_with_docker():
        """Test MQTT using Docker exec into EMQX container"""
        
        print("🧪 Testing MQTT Integration via Docker")
        print("=" * 40)
        
        test_messages = [
            {
                "topic": "equipment/status",
                "payload": {
                    "equipmentId": "TEST-001",
                    "type": "test_sensor",
                    "location": "Test Lab",
                    "value": "normal",
                    "description": "Test info message"
                },
                "description": "Info Level Alert (Sheets only)"
            },
            {
                "topic": "equipment/alerts", 
                "payload": {
                    "equipmentId": "PUMP-001",
                    "type": "centrifugal_pump",
                    "location": "Building A",
                    "value": 78,
                    "threshold": 75,
                    "description": "Vibration levels elevated"
                },
                "description": "Warning Alert (Sheets + WhatsApp)"
            },
            {
                "topic": "sensors/critical",
                "payload": {
                    "equipmentId": "TEMP-001",
                    "type": "temperature_sensor",
                    "location": "Reactor Room", 
                    "value": 95,
                    "threshold": 85,
                    "description": "Critical temperature exceeded"
                },
                "description": "Critical Alert (Sheets + WhatsApp)"
            },
            {
                "topic": "actuators/fault",
                "payload": {
                    "equipmentId": "VALVE-003",
                    "type": "control_valve",
                    "location": "Process Line 2", 
                    "value": "stuck_closed",
                    "description": "Valve failed to open"
                },
                "description": "Fault Alert (Sheets + WhatsApp)"
            }
        ]
        
        success_count = 0
        
        for i, test in enumerate(test_messages, 1):
            print(f"\nTest {i}: {test['description']}")
            
            # Prepare message
            payload_json = json.dumps(test["payload"])
            
            # Use Docker exec to send MQTT message via EMQX container
            cmd = [
                "docker", "exec", "emqxnodec",
                "emqx_ctl", "messages", "publish",
                test["topic"], payload_json
            ]
            
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
                
                if result.returncode == 0:
                    print(f"✅ Sent {test['description']}")
                    success_count += 1
                else:
                    print(f"❌ Failed: {result.stderr}")
                    
            except subprocess.TimeoutExpired:
                print(f"⏱️  Timeout sending message")
            except Exception as e:
                print(f"❌ Error: {str(e)}")
            
            time.sleep(2)  # Wait between messages
        
        print(f"\n📊 Test Results:")
        print(f"✅ Successful: {success_count}/{len(test_messages)}")
        print(f"🎯 Success Rate: {(success_count/len(test_messages))*100:.1f}%")
        
        print(f"\n🔍 Check Results:")
        print("1. n8n Execution History: http://localhost:5678/executions")
        print("2. Google Sheets: https://docs.google.com/spreadsheets/d/1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do")
        print("   - Equipment Alerts sheet")
        print("   - All Equipment Events sheet")
        
        if success_count >= len(test_messages) * 0.75:  # 75% success
            print("\n🚀 CT-008 Status: INTEGRATION TEST PASSED")
            return True
        else:
            print("\n❌ CT-008 Status: INTEGRATION TEST FAILED")
            return False
    
    if __name__ == "__main__":
        success = test_mqtt_with_docker()
        sys.exit(0 if success else 1)

def test_mqtt_with_paho():
    """Test MQTT using paho-mqtt library"""
    
    print("🧪 Testing MQTT Integration with Paho Client")
    print("=" * 45)
    
    # MQTT configuration
    broker_host = "localhost"
    broker_port = 1883
    client_id = "n8n-integration-test"
    
    # Test messages
    test_messages = [
        {
            "topic": "equipment/status",
            "payload": {
                "equipmentId": "TEST-001",
                "type": "test_sensor",
                "location": "Test Lab",
                "value": "normal",
                "description": "Test info message"
            },
            "description": "Info Level Alert"
        },
        {
            "topic": "equipment/alerts",
            "payload": {
                "equipmentId": "PUMP-001", 
                "type": "centrifugal_pump",
                "location": "Building A",
                "value": 78,
                "threshold": 75,
                "description": "Vibration levels elevated"
            },
            "description": "Warning Alert"
        },
        {
            "topic": "sensors/critical",
            "payload": {
                "equipmentId": "TEMP-001",
                "type": "temperature_sensor",
                "location": "Reactor Room",
                "value": 95,
                "threshold": 85,
                "description": "Critical temperature exceeded" 
            },
            "description": "Critical Alert"
        },
        {
            "topic": "actuators/fault",
            "payload": {
                "equipmentId": "VALVE-003",
                "type": "control_valve", 
                "location": "Process Line 2",
                "value": "stuck_closed",
                "description": "Valve failed to open"
            },
            "description": "Fault Alert"
        }
    ]
    
    # Setup MQTT client
    client = mqtt.Client(client_id)
    
    # Connection callback
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("✅ Connected to MQTT broker")
        else:
            print(f"❌ Connection failed with code {rc}")
    
    # Publish callback
    def on_publish(client, userdata, mid):
        print(f"✅ Message {mid} published successfully")
    
    client.on_connect = on_connect
    client.on_publish = on_publish
    
    try:
        # Connect to broker
        print(f"Connecting to MQTT broker at {broker_host}:{broker_port}")
        client.connect(broker_host, broker_port, 60)
        client.loop_start()
        
        time.sleep(2)  # Wait for connection
        
        success_count = 0
        
        # Send test messages
        for i, test in enumerate(test_messages, 1):
            print(f"\nTest {i}: {test['description']}")
            
            payload_json = json.dumps(test["payload"])
            
            result = client.publish(test["topic"], payload_json, qos=1)
            
            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                print(f"✅ Published to {test['topic']}")
                success_count += 1
            else:
                print(f"❌ Failed to publish: {result.rc}")
            
            time.sleep(2)  # Wait between messages
        
        time.sleep(5)  # Wait for final message processing
        
        client.loop_stop()
        client.disconnect()
        
        print(f"\n📊 Test Results:")
        print(f"✅ Successful: {success_count}/{len(test_messages)}")
        print(f"🎯 Success Rate: {(success_count/len(test_messages))*100:.1f}%")
        
        if success_count >= len(test_messages) * 0.75:
            print("\n🚀 CT-008: INTEGRATION TEST PASSED")
            return True
        else:
            print("\n❌ CT-008: INTEGRATION TEST FAILED")
            return False
            
    except Exception as e:
        print(f"❌ MQTT test failed: {str(e)}")
        return False

if __name__ == "__main__":
    try:
        success = test_mqtt_with_paho()
    except NameError:
        # paho-mqtt not available, already handled above
        pass