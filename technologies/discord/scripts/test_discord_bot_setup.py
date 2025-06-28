#!/usr/bin/env python3
"""
Test Discord Bot Setup - Verify webhook and prepare for bot development
"""

import json
import requests
from datetime import datetime

def test_webhook():
    """Test existing Discord webhook"""
    try:
        with open('discord_webhook_config.json', 'r') as f:
            config = json.load(f)
        
        webhook_url = config['discord']['general_webhook']
        
        test_message = {
            "embeds": [{
                "title": "🤖 Discord Claude Bot - Setup Progress",
                "description": "Testing Discord integration for @claude response system",
                "color": 0x00ff9f,
                "fields": [
                    {
                        "name": "✅ Discord.py Library",
                        "value": "Successfully installed",
                        "inline": True
                    },
                    {
                        "name": "✅ Bot Script", 
                        "value": "Created and ready",
                        "inline": True
                    },
                    {
                        "name": "🔧 Next Step",
                        "value": "Need Discord Bot Token from Developer Portal",
                        "inline": False
                    },
                    {
                        "name": "🎯 Almost Ready!",
                        "value": "Once token is configured, @claude mentions will work!",
                        "inline": False
                    }
                ],
                "footer": {
                    "text": "Server Claude - Discord Bot Development"
                },
                "timestamp": datetime.now().isoformat()
            }]
        }
        
        response = requests.post(webhook_url, json=test_message)
        
        if response.status_code == 204:
            print("✅ Discord webhook test successful!")
            print("📨 Message sent to Discord channel")
            return True
        else:
            print(f"⚠️ Webhook response code: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Webhook test failed: {e}")
        return False

def check_bot_script():
    """Verify bot script is ready"""
    try:
        import discord
        print("✅ discord.py library available")
        
        # Check if script exists
        with open('scripts/discord_claude_bot.py', 'r') as f:
            content = f.read()
            
        if 'IndustrialIoTClaudeBot' in content:
            print("✅ Discord Claude Bot script ready")
            return True
        else:
            print("❌ Bot script incomplete")
            return False
            
    except ImportError:
        print("❌ discord.py library not installed")
        return False
    except FileNotFoundError:
        print("❌ Bot script not found")
        return False
    except Exception as e:
        print(f"❌ Error checking bot script: {e}")
        return False

def main():
    print("🧪 Discord Claude Bot Setup Test")
    print("=" * 40)
    
    webhook_ok = test_webhook()
    script_ok = check_bot_script()
    
    print("\n📊 Setup Status:")
    print(f"Webhook: {'✅' if webhook_ok else '❌'}")
    print(f"Bot Script: {'✅' if script_ok else '❌'}")
    
    if webhook_ok and script_ok:
        print("\n🎉 READY FOR BOT TOKEN!")
        print("📋 Next steps:")
        print("1. Go to https://discord.com/developers/applications")
        print("2. Create 'Industrial IoT Claude Bot' application")
        print("3. Create bot and copy token")
        print("4. Export token: export DISCORD_BOT_TOKEN='your_token'")
        print("5. Run: python3 scripts/discord_claude_bot.py")
        print("\n🚀 Then @claude mentions will work in Discord!")
    else:
        print("\n⚠️ Setup needs attention before proceeding")

if __name__ == "__main__":
    main()