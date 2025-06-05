#!/usr/bin/env python3
"""
Test MQTT connection directly to diagnose n8n issues
"""

import socket
import time
import sys

def test_basic_connectivity():
    """Test basic TCP connection to EMQX"""
    print("🔍 Testing basic TCP connectivity to EMQX...")
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex(('172.17.0.4', 1883))
        sock.close()
        
        if result == 0:
            print("✅ TCP connection to 172.17.0.4:1883 successful")
            return True
        else:
            print(f"❌ TCP connection failed: error code {result}")
            return False
    except Exception as e:
        print(f"❌ TCP connection error: {e}")
        return False

def test_mqtt_protocol():
    """Test basic MQTT protocol connection"""
    print("\n🔍 Testing MQTT protocol...")
    
    try:
        import paho.mqtt.client as mqtt
        
        # Connection result tracking
        connection_result = {"success": False, "error": None}
        
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("✅ MQTT connection successful!")
                connection_result["success"] = True
            else:
                print(f"❌ MQTT connection failed with code: {rc}")
                error_codes = {
                    1: "Incorrect protocol version",
                    2: "Invalid client identifier", 
                    3: "Server unavailable",
                    4: "Bad username or password",
                    5: "Not authorized"
                }
                connection_result["error"] = error_codes.get(rc, f"Unknown error {rc}")
        
        def on_disconnect(client, userdata, rc):
            print(f"🔌 MQTT disconnected with code: {rc}")
        
        # Create MQTT client
        client = mqtt.Client(client_id="test-mqtt-client")
        client.on_connect = on_connect
        client.on_disconnect = on_disconnect
        
        print("🔌 Attempting MQTT connection...")
        client.connect("172.17.0.4", 1883, 60)
        
        # Wait for connection
        client.loop_start()
        time.sleep(3)
        client.loop_stop()
        client.disconnect()
        
        return connection_result["success"]
        
    except ImportError:
        print("⚠️  paho-mqtt not installed. Install with: pip install paho-mqtt")
        return None
    except Exception as e:
        print(f"❌ MQTT test error: {e}")
        return False

def test_emqx_status():
    """Check EMQX container status"""
    print("\n🔍 Checking EMQX container status...")
    
    import subprocess
    
    try:
        # Check if EMQX container is running
        result = subprocess.run(["docker", "ps"], capture_output=True, text=True)
        if "emqxnodec" in result.stdout:
            print("✅ EMQX container is running")
        else:
            print("❌ EMQX container not found in running containers")
            return False
        
        # Check EMQX IP
        result = subprocess.run(["docker", "inspect", "emqxnodec"], capture_output=True, text=True)
        if "172.17.0.4" in result.stdout:
            print("✅ EMQX IP is 172.17.0.4")
        else:
            print("⚠️  EMQX IP might have changed")
            # Try to extract actual IP
            import json
            inspect_data = json.loads(result.stdout)
            ip = inspect_data[0]["NetworkSettings"]["IPAddress"]
            print(f"   Actual IP: {ip}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error checking EMQX: {e}")
        return False

def test_n8n_network():
    """Test if n8n can reach EMQX"""
    print("\n🔍 Testing n8n → EMQX network connectivity...")
    
    try:
        import subprocess
        
        # Test ping from n8n container to EMQX
        result = subprocess.run([
            "docker", "exec", "n8n", 
            "sh", "-c", "ping -c 1 172.17.0.4"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ n8n can ping EMQX container")
            return True
        else:
            print("❌ n8n cannot reach EMQX container")
            print(f"   Error: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing n8n network: {e}")
        return False

def main():
    """Main diagnostic function"""
    print("🔧 MQTT Connection Diagnostic Tool")
    print("=" * 40)
    
    all_tests_passed = True
    
    # Test 1: Basic connectivity
    if not test_basic_connectivity():
        all_tests_passed = False
    
    # Test 2: EMQX status
    if not test_emqx_status():
        all_tests_passed = False
    
    # Test 3: MQTT protocol
    mqtt_result = test_mqtt_protocol()
    if mqtt_result is False:
        all_tests_passed = False
    elif mqtt_result is None:
        print("   Install paho-mqtt for full MQTT testing")
    
    # Test 4: n8n network
    if not test_n8n_network():
        all_tests_passed = False
        
    # Summary
    print("\n" + "=" * 40)
    if all_tests_passed:
        print("✅ All tests passed! MQTT should work in n8n")
        print("\nTry n8n with these settings:")
        print("  Protocol: mqtt://")
        print("  Host: 172.17.0.4") 
        print("  Port: 1883")
        print("  Username: (empty)")
        print("  Password: (empty)")
        print("  Client ID: n8n-mqtt-client")
        print("  SSL: OFF")
    else:
        print("❌ Some tests failed. Check the errors above.")
        print("\nCommon solutions:")
        print("1. Restart EMQX: docker restart emqxnodec")
        print("2. Check EMQX logs: docker logs emqxnodec")
        print("3. Verify network: docker network ls")

if __name__ == "__main__":
    main()