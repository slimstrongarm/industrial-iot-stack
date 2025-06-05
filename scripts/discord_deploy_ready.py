#!/usr/bin/env python3
# Discord Integration - Ready for Deployment
# Server: https://discord.gg/5gWaB3cf

from scripts.discord_webhook_integration import DiscordAlertSender, mqtt_to_discord_alert

# Load webhook configuration
import json
with open('/mnt/c/Users/LocalAccount/industrial-iot-stack/discord_webhook_config.json') as f:
    config = json.load(f)

# Initialize Discord sender (once webhooks are configured)
def create_discord_sender():
    webhook_urls = {}
    for key, webhook_info in config['required_webhooks'].items():
        webhook_urls[key] = webhook_info['webhook_url']
    
    return DiscordAlertSender(webhook_urls)

# Test function
def test_discord_alerts():
    sender = create_discord_sender()
    
    # Test critical alert
    test_payload = {
        "equipmentId": "TEMP-001",
        "type": "Temperature Sensor", 
        "location": "Reactor Room",
        "value": 95,
        "threshold": 85,
        "description": "Critical temperature exceeded"
    }
    
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
    print("Discord server: https://discord.gg/5gWaB3cf")
    print("Ready for webhook configuration!")
