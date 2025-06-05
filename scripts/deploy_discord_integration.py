#!/usr/bin/env python3
"""
Deploy Discord integration using the found Discord link
"""

import requests
import json
from datetime import datetime

# Discord server link found
DISCORD_INVITE = "https://discord.gg/5gWaB3cf"

def setup_discord_integration():
    """Set up Discord integration with the found server link"""
    
    print("🎯 Setting Up Discord Integration")
    print("=" * 40)
    print(f"Discord Server: {DISCORD_INVITE}")
    print("")
    
    # Create Discord webhook configuration template
    webhook_config = {
        "server_invite": DISCORD_INVITE,
        "required_webhooks": {
            "alerts": {
                "channel": "#alerts",
                "description": "Equipment warnings and alerts",
                "webhook_url": "NEED_WEBHOOK_URL_FROM_CHANNEL_SETTINGS",
                "usage": "Warning level equipment alerts, maintenance notifications"
            },
            "critical": {
                "channel": "#critical", 
                "description": "Critical failures and emergencies",
                "webhook_url": "NEED_WEBHOOK_URL_FROM_CHANNEL_SETTINGS",
                "usage": "Critical equipment failures, safety issues"
            },
            "logs": {
                "channel": "#logs",
                "description": "Complete audit trail of all messages", 
                "webhook_url": "NEED_WEBHOOK_URL_FROM_CHANNEL_SETTINGS",
                "usage": "All MQTT messages for audit trail"
            },
            "general": {
                "channel": "#general",
                "description": "System status and coordination",
                "webhook_url": "NEED_WEBHOOK_URL_FROM_CHANNEL_SETTINGS", 
                "usage": "System health, agent status updates"
            }
        },
        "setup_instructions": [
            "1. Join Discord server using invite link",
            "2. For each channel, right-click → Settings → Integrations → Webhooks",
            "3. Create new webhook, copy URL",
            "4. Replace NEED_WEBHOOK_URL_FROM_CHANNEL_SETTINGS with actual URLs",
            "5. Run discord integration test"
        ]
    }
    
    # Save configuration
    with open('/mnt/c/Users/LocalAccount/industrial-iot-stack/discord_webhook_config.json', 'w') as f:
        json.dump(webhook_config, f, indent=2)
    
    print("✅ Discord configuration template created")
    print("📁 Saved to: discord_webhook_config.json")
    print("")
    
    # Update existing Discord integration script with server link
    integration_script = f"""#!/usr/bin/env python3
# Discord Integration - Ready for Deployment
# Server: {DISCORD_INVITE}

from scripts.discord_webhook_integration import DiscordAlertSender, mqtt_to_discord_alert

# Load webhook configuration
import json
with open('/mnt/c/Users/LocalAccount/industrial-iot-stack/discord_webhook_config.json') as f:
    config = json.load(f)

# Initialize Discord sender (once webhooks are configured)
def create_discord_sender():
    webhook_urls = {{}}
    for key, webhook_info in config['required_webhooks'].items():
        webhook_urls[key] = webhook_info['webhook_url']
    
    return DiscordAlertSender(webhook_urls)

# Test function
def test_discord_alerts():
    sender = create_discord_sender()
    
    # Test critical alert
    test_payload = {{
        "equipmentId": "TEMP-001",
        "type": "Temperature Sensor", 
        "location": "Reactor Room",
        "value": 95,
        "threshold": 85,
        "description": "Critical temperature exceeded"
    }}
    
    alert_data = mqtt_to_discord_alert("sensors/critical", test_payload)
    sender.send_alert(
        alert_data["channel"],
        alert_data["title"],
        alert_data["message"], 
        alert_data["severity"],
        alert_data["equipment_data"]
    )
    
    print("✅ Test alert sent to Discord!")

if __name__ == "__main__":
    print("Discord server: {DISCORD_INVITE}")
    print("Ready for webhook configuration!")
"""
    
    with open('/mnt/c/Users/LocalAccount/industrial-iot-stack/scripts/discord_deploy_ready.py', 'w') as f:
        f.write(integration_script)
    
    print("🚀 Discord Integration Status:")
    print("✅ Server link found and configured")
    print("✅ Integration scripts updated")
    print("✅ Configuration template created")
    print("✅ Ready for webhook setup")
    print("")
    print("🎯 Next Steps:")
    print("1. Join Discord server (link ready)")
    print("2. Set up webhooks (5 minutes)")
    print("3. Deploy integration (automated)")
    
    return True

if __name__ == "__main__":
    setup_discord_integration()