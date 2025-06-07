#!/usr/bin/env python3
"""
🎬 Discord Bot Feature Demo
Demonstrates Industrial IoT Claude Bot capabilities without requiring Discord connection

This script shows the bot's core functionality and system integration features.
"""

import asyncio
import json
import subprocess
from datetime import datetime
import aiohttp

class BotDemo:
    """Demo version of Industrial IoT Discord Bot features"""
    
    def __init__(self):
        self.system_status = {
            'mqtt_broker': 'unknown',
            'node_red': 'unknown', 
            'ignition': 'unknown',
            'docker_containers': [],
            'last_update': None
        }

    async def update_system_status(self):
        """Demo system status checking"""
        print("🔍 Checking Industrial IoT system status...")
        
        # Check Docker containers
        try:
            result = subprocess.run(['docker', 'ps', '--format', 'json'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                containers = []
                for line in result.stdout.strip().split('\n'):
                    if line:
                        container = json.loads(line)
                        containers.append({
                            'name': container.get('Names', ''),
                            'status': container.get('Status', ''),
                            'image': container.get('Image', '')
                        })
                self.system_status['docker_containers'] = containers
                print(f"  🐳 Found {len(containers)} Docker containers")
        except subprocess.TimeoutExpired:
            print("  ⚠️ Docker command timed out")
        except FileNotFoundError:
            print("  ⚠️ Docker not available")
        except Exception as e:
            print(f"  ❌ Docker check failed: {e}")

        # Check Node-RED
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get('http://localhost:1880/flows', timeout=5) as resp:
                    if resp.status == 200:
                        self.system_status['node_red'] = 'online'
                        print("  ✅ Node-RED: Online")
                    else:
                        self.system_status['node_red'] = 'offline'
                        print(f"  ⚠️ Node-RED: HTTP {resp.status}")
        except:
            self.system_status['node_red'] = 'offline'
            print("  ❌ Node-RED: Offline")

        # Check MQTT broker
        mqtt_status = 'offline'
        for container in self.system_status['docker_containers']:
            if 'mosquitto' in container['name'].lower() or 'emqx' in container['name'].lower():
                if 'Up' in container['status']:
                    mqtt_status = 'online'
                break
        self.system_status['mqtt_broker'] = mqtt_status
        print(f"  📡 MQTT Broker: {mqtt_status.title()}")
        
        self.system_status['last_update'] = datetime.now()
        print(f"  🕒 Last update: {self.system_status['last_update'].strftime('%H:%M:%S')}")

    def demo_command_processing(self):
        """Demo natural language command processing"""
        print("\n🗣️ Natural Language Command Processing Demo")
        print("=" * 50)
        
        test_commands = [
            "@claude status",
            "@claude check mqtt broker", 
            "@claude help",
            "@claude add task Fix temperature sensor",
            "@claude docker containers"
        ]
        
        for command in test_commands:
            print(f"\n💬 User: {command}")
            response = self.process_command(command.lower())
            print(f"🤖 Claude: {response}")

    def process_command(self, content):
        """Process natural language commands"""
        content = content.replace('@claude', '').strip()
        
        if any(word in content for word in ['status', 'health', 'check']):
            return self.get_status_response()
        elif 'mqtt' in content:
            return f"📡 MQTT Broker Status: {self.system_status['mqtt_broker'].title()}"
        elif 'help' in content:
            return ("Available commands: status, mqtt, docker, help, add task\n"
                   "System endpoints: Node-RED (1880), n8n (5678), Ignition (8088)")
        elif 'task' in content and 'add' in content:
            return "📝 Task logged to Google Sheets Claude Tasks"
        elif 'docker' in content:
            return f"🐳 Found {len(self.system_status['docker_containers'])} containers"
        else:
            return "🤖 I can help with Industrial IoT system management. Try '@claude help'"

    def get_status_response(self):
        """Generate system status response"""
        return (f"🏭 Industrial IoT Stack Status:\n"
               f"• Node-RED: {self.system_status['node_red'].title()}\n"
               f"• MQTT Broker: {self.system_status['mqtt_broker'].title()}\n"
               f"• Docker Containers: {len(self.system_status['docker_containers'])}\n"
               f"• Last Update: {self.system_status['last_update'].strftime('%H:%M:%S') if self.system_status['last_update'] else 'Never'}")

    def demo_google_sheets_integration(self):
        """Demo Google Sheets integration features"""
        print("\n📊 Google Sheets Integration Demo")
        print("=" * 50)
        
        print("✅ Google Sheets Claude Tasks Integration:")
        print("  • Spreadsheet ID: 1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do")
        print("  • Service Account: iiot-stack-automation@iiot-stack-automation.iam.gserviceaccount.com")
        print("  • Features: Task creation, status updates, real-time sync")
        
        print("\n📝 Task Management Commands:")
        print("  • '@claude add task Fix MQTT connection' → Creates CT-047")
        print("  • '@claude tasks' → Shows current pending tasks")
        print("  • '@claude update task CT-046 completed' → Updates status")

    def demo_system_monitoring(self):
        """Demo proactive system monitoring"""
        print("\n📊 Proactive System Monitoring Demo")
        print("=" * 50)
        
        print("🔍 Background monitoring checks:")
        print("  • Every 5 minutes: System health scan")
        print("  • Docker container status")
        print("  • Node-RED accessibility")
        print("  • MQTT broker connectivity")
        print("  • Disk space and memory usage")
        
        print("\n🚨 Alert scenarios:")
        print("  • Container stops → Immediate Discord alert")
        print("  • Node-RED offline → Automated restart attempt")
        print("  • MQTT disconnection → Equipment monitoring alert")
        print("  • High memory usage → Performance warning")

    def demo_industrial_features(self):
        """Demo Industrial IoT specific features"""
        print("\n🏭 Industrial IoT Features Demo")
        print("=" * 50)
        
        print("🔧 Equipment Monitoring:")
        print("  • Real-time brewery sensor data")
        print("  • HLT temperature monitoring")
        print("  • Chiller status tracking")
        print("  • Valve position monitoring")
        
        print("\n📱 Mobile-First Design:")
        print("  • Optimized for iPhone Discord app")
        print("  • Quick status checks while on brewery floor")
        print("  • Emergency shutdown commands")
        print("  • Rich embeds with equipment diagrams")
        
        print("\n⚡ Real-time Integration:")
        print("  • MQTT → Node-RED → Discord alerts")
        print("  • Equipment failures trigger immediate notifications")
        print("  • Historical data trending in Discord")

async def main():
    """Run complete bot feature demonstration"""
    print("🤖 Industrial IoT Claude Discord Bot - Feature Demo")
    print("=" * 60)
    print("Following .claude standards for Industrial IoT integration")
    print()
    
    demo = BotDemo()
    
    # System status check
    await demo.update_system_status()
    
    # Command processing demo
    demo.demo_command_processing()
    
    # Google Sheets integration
    demo.demo_google_sheets_integration()
    
    # System monitoring
    demo.demo_system_monitoring()
    
    # Industrial IoT features
    demo.demo_industrial_features()
    
    print("\n🚀 Next Steps:")
    print("=" * 60)
    print("1. Set DISCORD_BOT_TOKEN environment variable")
    print("2. Create Discord server with #mac-claude channel")
    print("3. Run: python3 discord-bot/industrial_iot_claude_bot.py")
    print("4. Test with: @claude status")
    print()
    print("✅ Bot ready for real Discord deployment!")

if __name__ == "__main__":
    asyncio.run(main())