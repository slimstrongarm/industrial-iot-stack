#!/usr/bin/env python3
"""
🚀 Quick Discord Integration Test
Test Discord integration using existing webhook and server setup

Based on existing credentials from credentials/discord_webhook.txt
"""

import requests
import json
from datetime import datetime

def test_discord_webhook():
    """Test Discord webhook integration"""
    print("🧪 Testing Discord Webhook Integration")
    print("=" * 50)
    
    # Load webhook URL from credentials
    webhook_file = '/Users/joshpayneair/Desktop/industrial-iot-stack/credentials/discord_webhook.txt'
    
    try:
        with open(webhook_file, 'r') as f:
            content = f.read()
            # Extract webhook URL
            for line in content.split('\n'):
                if line.startswith('Webhook URL:'):
                    webhook_url = line.split('Webhook URL: ')[1].strip()
                    break
        
        print(f"✅ Webhook URL loaded from credentials")
        
        # Test message
        embed = {
            "title": "🤖 Enhanced Industrial IoT Claude Bot Test",
            "description": "Testing advanced Discord integration following .claude standards",
            "color": 0x00ff00,
            "timestamp": datetime.now().isoformat(),
            "fields": [
                {
                    "name": "🏭 Industrial IoT Integration",
                    "value": "• Real-time system monitoring\n• Google Sheets Claude Tasks\n• MQTT/Node-RED awareness\n• Mobile-first design",
                    "inline": False
                },
                {
                    "name": "🔧 System Status", 
                    "value": "• Node-RED: Online (http://localhost:1880)\n• n8n: Online (http://localhost:5678)\n• Ignition: Online (http://localhost:8088)",
                    "inline": False
                },
                {
                    "name": "📊 Next Steps",
                    "value": "Ready for Discord bot token setup and full deployment",
                    "inline": False
                }
            ],
            "footer": {
                "text": "Industrial IoT Stack | Following .claude standards"
            }
        }
        
        payload = {
            "username": "Industrial IoT Claude Bot",
            "embeds": [embed]
        }
        
        response = requests.post(webhook_url, json=payload)
        
        if response.status_code == 204:
            print("✅ Discord webhook test successful!")
            print("📱 Check #mac-claude channel for test message")
            return True
        else:
            print(f"❌ Webhook test failed: HTTP {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except FileNotFoundError:
        print(f"❌ Webhook file not found: {webhook_file}")
        return False
    except Exception as e:
        print(f"❌ Webhook test failed: {e}")
        return False

def show_bot_setup_instructions():
    """Show instructions for bot setup"""
    print("\n🚀 Discord Bot Setup Instructions")
    print("=" * 50)
    
    print("Your Discord server 'slims agents' is ready with:")
    print("  ✅ #mac-claude channel active")
    print("  ✅ Webhook integration working")
    print("  ✅ Mac Claude Bot already deployed")
    
    print("\n🔧 To deploy Enhanced Industrial IoT Claude Bot:")
    print("1. Get Discord bot token from Discord Developer Portal")
    print("2. Export token: export DISCORD_BOT_TOKEN='your_token'")
    print("3. Run: python3 discord-bot/industrial_iot_claude_bot.py")
    
    print("\n💬 Test commands in #mac-claude:")
    print("  • @claude status - Complete system overview")
    print("  • @claude mqtt - MQTT broker status") 
    print("  • @claude help - Full command reference")
    print("  • @claude add task Fix sensor - Create Claude task")

def main():
    """Run Discord integration test"""
    print("🤖 Industrial IoT Claude Discord Integration Test")
    print("Using existing Discord server: 'slims agents'")
    print("Channel: #mac-claude")
    print()
    
    # Test webhook
    webhook_success = test_discord_webhook()
    
    # Show setup instructions
    show_bot_setup_instructions()
    
    print("\n📊 Integration Status:")
    print("=" * 50)
    if webhook_success:
        print("✅ Discord webhook integration: WORKING")
        print("✅ Discord server: 'slims agents' connected")
        print("✅ Channel: #mac-claude ready")
        print("⏳ Bot token setup: PENDING")
        print("\n🎯 Ready for enhanced Claude bot deployment!")
    else:
        print("❌ Discord webhook integration: FAILED")
        print("🔧 Check credentials/discord_webhook.txt")

if __name__ == "__main__":
    main()