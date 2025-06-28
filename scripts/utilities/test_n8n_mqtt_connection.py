#!/usr/bin/env python3
"""
n8n MQTT Connection Test Script
Tests MQTT connectivity between brokers and helps debug n8n trigger issues
"""

import paho.mqtt.client as mqtt
import json
import time
import sys
from datetime import datetime

# Configuration
EMQX_HOST = "100.94.84.126"  # Server EMQX
EMQX_PORT = 1883
TEST_TOPIC = "iiot/n8n/test"
ALERT_TOPIC = "iiot/alerts/critical"
DATA_TOPIC = "brewery/data/pump/test"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"✅ Connected to EMQX broker at {EMQX_HOST}:{EMQX_PORT}")
    else:
        print(f"❌ Failed to connect, return code {rc}")

def on_publish(client, userdata, mid):
    print(f"✅ Message published (mid: {mid})")

def send_test_messages():
    """Send various test messages to help debug n8n"""
    
    # Initialize MQTT client
    client = mqtt.Client("n8n-test-publisher")
    client.on_connect = on_connect
    client.on_publish = on_publish
    
    # Connect to EMQX
    print(f"🔌 Connecting to EMQX at {EMQX_HOST}:{EMQX_PORT}...")
    try:
        client.connect(EMQX_HOST, EMQX_PORT, 60)
        client.loop_start()
        time.sleep(2)  # Wait for connection
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return
    
    # Test 1: Simple test message
    print("\n📤 Test 1: Simple Test Message")
    test_msg = {
        "test": "Hello from Mac Claude",
        "timestamp": datetime.now().isoformat(),
        "source": "mac-mqtt-test"
    }
    client.publish(TEST_TOPIC, json.dumps(test_msg), qos=0)
    print(f"   Topic: {TEST_TOPIC}")
    print(f"   Message: {json.dumps(test_msg, indent=2)}")
    time.sleep(1)
    
    # Test 2: Critical alert message
    print("\n📤 Test 2: Critical Alert Message")
    alert_msg = {
        "equipment": "test-pump-001",
        "status": "critical",
        "alert_type": "high_pressure",
        "value": 95,
        "threshold": 85,
        "timestamp": datetime.now().isoformat(),
        "source": "mac-mqtt-test",
        "message": "Pressure exceeds safe operating limit"
    }
    client.publish(ALERT_TOPIC, json.dumps(alert_msg), qos=1)
    print(f"   Topic: {ALERT_TOPIC}")
    print(f"   Message: {json.dumps(alert_msg, indent=2)}")
    time.sleep(1)
    
    # Test 3: Equipment data message
    print("\n📤 Test 3: Equipment Data Message")
    data_msg = {
        "equipment_id": "pump-test-001",
        "temperature": 78.5,
        "pressure": 92.3,
        "flow_rate": 45.2,
        "vibration": 0.12,
        "status": "running",
        "efficiency": 87.3,
        "timestamp": datetime.now().isoformat(),
        "source": "mac-mqtt-test"
    }
    client.publish(DATA_TOPIC, json.dumps(data_msg), qos=0)
    print(f"   Topic: {DATA_TOPIC}")
    print(f"   Message: {json.dumps(data_msg, indent=2)}")
    time.sleep(1)
    
    # Test 4: Multiple rapid messages
    print("\n📤 Test 4: Rapid Fire Messages (5 messages)")
    for i in range(5):
        rapid_msg = {
            "sequence": i + 1,
            "test": "rapid_fire",
            "timestamp": datetime.now().isoformat()
        }
        topic = f"iiot/test/rapid/{i+1}"
        client.publish(topic, json.dumps(rapid_msg), qos=0)
        print(f"   Message {i+1} sent to: {topic}")
        time.sleep(0.5)
    
    # Test 5: Different QoS levels
    print("\n📤 Test 5: QoS Level Testing")
    for qos in [0, 1, 2]:
        qos_msg = {
            "test": f"QoS_{qos}",
            "qos_level": qos,
            "timestamp": datetime.now().isoformat()
        }
        topic = f"iiot/test/qos{qos}"
        client.publish(topic, json.dumps(qos_msg), qos=qos)
        print(f"   QoS {qos} message sent to: {topic}")
        time.sleep(1)
    
    # Test 6: Retained message
    print("\n📤 Test 6: Retained Message")
    retained_msg = {
        "test": "retained_message",
        "info": "This message should persist",
        "timestamp": datetime.now().isoformat()
    }
    client.publish("iiot/test/retained", json.dumps(retained_msg), qos=1, retain=True)
    print(f"   Retained message sent to: iiot/test/retained")
    
    # Keep connection alive for a bit
    print("\n⏳ Keeping connection alive for 5 seconds...")
    time.sleep(5)
    
    # Disconnect
    client.loop_stop()
    client.disconnect()
    print("\n✅ All test messages sent successfully!")
    
    # Print summary
    print("\n📊 Summary for n8n Debugging:")
    print("================================")
    print("Test these topics in n8n MQTT Trigger nodes:")
    print(f"  - {TEST_TOPIC}")
    print(f"  - {ALERT_TOPIC}")
    print(f"  - {DATA_TOPIC}")
    print("  - iiot/test/rapid/+")
    print("  - iiot/test/qos+")
    print("  - iiot/test/retained")
    print("  - iiot/# (for all messages)")
    print("\nIn n8n MQTT credentials, use:")
    print(f"  - Host: {EMQX_HOST}")
    print(f"  - Port: {EMQX_PORT}")
    print("  - Protocol: mqtt://")
    print("  - Client ID: n8n-client-{unique-id}")
    print("\nIf running in Docker, use container name instead:")
    print("  - Host: emqx (or your EMQX container name)")

if __name__ == "__main__":
    print("🚀 n8n MQTT Connection Test Script")
    print("==================================")
    send_test_messages()