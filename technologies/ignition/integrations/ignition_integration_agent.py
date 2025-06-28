#!/usr/bin/env python3
"""
Ignition Integration Agent
Sets up Node-RED → Ignition data flow and VSCode integration
"""

import requests
import json
import time
from datetime import datetime

class IgnitionIntegrationAgent:
    def __init__(self):
        self.ignition_url = "http://localhost:8088"
        self.node_red_url = "http://localhost:1880"
        self.project_scan_endpoint = f"{self.ignition_url}/data/project-scan-endpoint"
        
    def check_ignition_gateway(self):
        """Check Ignition Gateway status and modules"""
        print("🔍 Checking Ignition Gateway...")
        
        try:
            # Check gateway status
            response = requests.get(f"{self.ignition_url}/web/status")
            if response.status_code == 200:
                print("✅ Ignition Gateway accessible")
            else:
                print("❌ Ignition Gateway not accessible")
                return False
                
            # Check project scan endpoint
            try:
                scan_response = requests.get(f"{self.project_scan_endpoint}/confirm-support")
                if scan_response.status_code == 200:
                    print("✅ Project scan endpoint available")
                    print(f"   Response: {scan_response.json()}")
                else:
                    print("⚠️  Project scan endpoint not available")
            except Exception as e:
                print(f"⚠️  Project scan endpoint not installed: {e}")
                
            return True
            
        except Exception as e:
            print(f"❌ Error connecting to Ignition: {e}")
            return False
    
    def check_required_modules(self):
        """Check for required Ignition modules"""
        print("🔍 Checking Ignition modules...")
        
        required_modules = [
            "MQTT Engine",
            "MQTT Transmission", 
            "OPC-UA Server"
        ]
        
        # Note: This would require authentication to check modules
        # For now, provide manual check instructions
        print("⚠️  Manual check required:")
        print("   1. Open http://localhost:8088/web/config/modules")
        print("   2. Verify these modules are installed:")
        for module in required_modules:
            print(f"      - {module}")
        
        return True
    
    def setup_mqtt_integration(self):
        """Guide MQTT Engine setup for Node-RED integration"""
        print("🔧 MQTT Integration Setup...")
        
        mqtt_config = {
            "broker_url": "tcp://localhost:1883",
            "client_id": "IgnitionMQTTEngine",
            "tag_provider": "[default]",
            "base_path": "SteelBonnet",
            "topics": [
                "UNS/+/+/+/+",          # General UNS structure
                "brewery/+/+",          # Brewery data
                "SteelBonnet/+/+/+"     # Steel Bonnet specific
            ]
        }
        
        print("📋 MQTT Engine Configuration:")
        print(f"   Broker URL: {mqtt_config['broker_url']}")
        print(f"   Client ID: {mqtt_config['client_id']}")
        print(f"   Tag Provider: {mqtt_config['tag_provider']}")
        print(f"   Base Path: {mqtt_config['base_path']}")
        print("   Topics to subscribe:")
        for topic in mqtt_config['topics']:
            print(f"      - {topic}")
            
        print("\n🔧 Manual Setup Required:")
        print("   1. Go to Ignition Gateway → Configure → MQTT Engine → Settings")
        print("   2. Create new broker connection with above settings")
        print("   3. Create tag groups for each topic pattern")
        
        return mqtt_config
    
    def test_project_scan(self):
        """Test project scan functionality"""
        print("🧪 Testing project scan...")
        
        try:
            # Test project scan endpoint
            scan_params = {
                "updateDesigners": True,
                "forceUpdate": True
            }
            
            response = requests.post(
                f"{self.project_scan_endpoint}/scan",
                params=scan_params
            )
            
            if response.status_code == 200:
                print("✅ Project scan successful")
                return True
            else:
                print(f"⚠️  Project scan failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Project scan error: {e}")
            return False
    
    def monitor_tag_creation(self):
        """Monitor for tag creation in Ignition"""
        print("👀 Monitoring tag creation...")
        
        # This would require OPC-UA client or direct tag provider access
        # For now, provide manual check instructions
        expected_tags = [
            "[default]SteelBonnet/Brewery/Fermenter1/Temperature",
            "[default]SteelBonnet/Brewery/Fermenter1/pH", 
            "[default]SteelBonnet/Utilities/VFD_1/Current"
        ]
        
        print("📋 Expected tags to check in Ignition Designer:")
        for tag in expected_tags:
            print(f"   - {tag}")
            
        print("\n🔍 Manual verification:")
        print("   1. Open Ignition Designer")
        print("   2. Go to Tag Browser")
        print("   3. Look for SteelBonnet folder")
        print("   4. Verify tags are being created with live values")
        
        return expected_tags
    
    def create_test_script(self):
        """Create Ignition test script for tag validation"""
        print("📝 Creating Ignition test script...")
        
        test_script = '''
# Ignition Test Script - Tag Validation
# Place this in a Gateway Timer Script (1 minute interval)

# Get Node-RED data tags
node_red_tags = [
    "[default]SteelBonnet/Brewery/Fermenter1/Temperature",
    "[default]SteelBonnet/Brewery/Fermenter1/pH",
    "[default]SteelBonnet/Utilities/VFD_1/Current"
]

# Check tag values
for tag_path in node_red_tags:
    try:
        tag_value = system.tag.readBlocking([tag_path])[0]
        
        if tag_value.quality.name == "Good":
            system.util.getLogger("NodeRedIntegration").info(
                f"Tag {tag_path}: {tag_value.value} (Quality: {tag_value.quality.name})"
            )
        else:
            system.util.getLogger("NodeRedIntegration").warn(
                f"Tag {tag_path}: Bad quality - {tag_value.quality.name}"
            )
            
    except Exception as e:
        system.util.getLogger("NodeRedIntegration").error(
            f"Error reading tag {tag_path}: {str(e)}"
        )

# Report to Node-RED (optional)
try:
    import system.net
    
    status_data = {
        "timestamp": system.date.now(),
        "ignition_status": "running",
        "tag_count": len(node_red_tags),
        "last_check": system.date.format(system.date.now(), "yyyy-MM-dd HH:mm:ss")
    }
    
    # Could send status back to Node-RED via HTTP
    # system.net.httpPost("http://localhost:1880/ignition-status", status_data)
    
except Exception as e:
    system.util.getLogger("NodeRedIntegration").error(f"Status report failed: {str(e)}")
        '''
        
        # Save script to file for manual import
        with open("/Users/joshpayneair/Desktop/industrial-iot-stack/agents/ignition_test_script.py", "w") as f:
            f.write(test_script)
            
        print("✅ Test script created: agents/ignition_test_script.py")
        print("📋 To use in Ignition:")
        print("   1. Open Ignition Designer")
        print("   2. Go to Gateway → Timer Scripts")
        print("   3. Create new timer script (1 minute interval)")
        print("   4. Copy contents from ignition_test_script.py")
        
        return test_script
    
    def run_integration_setup(self):
        """Run complete integration setup"""
        print("🚀 Ignition Integration Agent Starting...\n")
        
        # Check components
        if not self.check_ignition_gateway():
            print("❌ Ignition Gateway check failed")
            return False
            
        self.check_required_modules()
        
        # Setup MQTT integration
        mqtt_config = self.setup_mqtt_integration()
        
        # Test project scan if available
        self.test_project_scan()
        
        # Monitor tag creation
        expected_tags = self.monitor_tag_creation()
        
        # Create test script
        self.create_test_script()
        
        print("\n✅ Integration setup complete!")
        print("\n📋 Next Manual Steps:")
        print("1. Configure MQTT Engine in Ignition Gateway")
        print("2. Import test script to Gateway Timer Scripts")
        print("3. Verify tags appear in Tag Browser")
        print("4. Check Designer logs for tag validation")
        
        return True

def main():
    agent = IgnitionIntegrationAgent()
    agent.run_integration_setup()

if __name__ == "__main__":
    main()