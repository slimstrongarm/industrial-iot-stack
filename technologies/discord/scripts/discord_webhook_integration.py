#!/usr/bin/env python3
"""
Discord Webhook Integration for IoT Alerts
Ready for immediate deployment once webhook URLs are provided
"""

import requests
import json
import sys
from datetime import datetime
from pathlib import Path

class DiscordAlertSender:
    def __init__(self, webhook_config):
        """
        Initialize Discord webhook sender
        
        webhook_config format:
        {
            "alerts": "https://discord.com/api/webhooks/...",
            "logs": "https://discord.com/api/webhooks/...",
            "general": "https://discord.com/api/webhooks/..."
        }
        """
        self.webhooks = webhook_config
        
    def send_alert(self, channel, title, message, severity="info", equipment_data=None):
        """Send alert to Discord channel"""
        
        if channel not in self.webhooks:
            print(f"❌ No webhook configured for channel: {channel}")
            return False
            
        # Color coding based on severity
        color_map = {
            "critical": 0xFF0000,  # Red
            "warning": 0xFFA500,   # Orange
            "info": 0x0099FF,      # Blue
            "success": 0x00FF00    # Green
        }
        
        # Create embed
        embed = {
            "title": f"🏭 {title}",
            "description": message,
            "color": color_map.get(severity, 0x0099FF),
            "timestamp": datetime.utcnow().isoformat(),
            "footer": {
                "text": "Industrial IoT Monitoring System"
            }
        }
        
        # Add equipment details if provided
        if equipment_data:
            fields = []
            if equipment_data.get("equipmentId"):
                fields.append({
                    "name": "Equipment ID",
                    "value": equipment_data["equipmentId"],
                    "inline": True
                })
            if equipment_data.get("location"):
                fields.append({
                    "name": "Location", 
                    "value": equipment_data["location"],
                    "inline": True
                })
            if equipment_data.get("value") and equipment_data.get("threshold"):
                fields.append({
                    "name": "Reading",
                    "value": f"{equipment_data['value']} (Threshold: {equipment_data['threshold']})",
                    "inline": True
                })
            if equipment_data.get("topic"):
                fields.append({
                    "name": "MQTT Topic",
                    "value": f"`{equipment_data['topic']}`",
                    "inline": False
                })
                
            embed["fields"] = fields
        
        # Send webhook
        payload = {
            "username": "IoT Monitor",
            "avatar_url": "https://cdn-icons-png.flaticon.com/512/2942/2942156.png",
            "embeds": [embed]
        }
        
        try:
            response = requests.post(
                self.webhooks[channel], 
                json=payload,
                timeout=10
            )
            
            if response.status_code == 204:
                print(f"✅ Discord alert sent to #{channel}")
                return True
            else:
                print(f"❌ Discord webhook failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Discord webhook error: {e}")
            return False

def mqtt_to_discord_alert(topic, payload_data):
    """Convert MQTT message to Discord alert format"""
    
    # Determine severity and channel based on topic
    if "critical" in topic or "fault" in topic:
        severity = "critical"
        channel = "alerts"
        title = "🚨 CRITICAL EQUIPMENT ALERT"
    elif "warning" in topic or "alert" in topic:
        severity = "warning" 
        channel = "alerts"
        title = "⚠️ Equipment Warning"
    else:
        severity = "info"
        channel = "logs"
        title = "📊 Equipment Update"
    
    # Extract equipment information
    equipment_id = payload_data.get("equipmentId", "Unknown")
    equipment_type = payload_data.get("type", "Equipment")
    location = payload_data.get("location", "Unknown Location")
    description = payload_data.get("description", "No description provided")
    
    # Create message
    message = f"**{equipment_type}** `{equipment_id}` at **{location}**\n\n{description}"
    
    return {
        "channel": channel,
        "title": title,
        "message": message,
        "severity": severity,
        "equipment_data": {
            "equipmentId": equipment_id,
            "location": location,
            "value": payload_data.get("value"),
            "threshold": payload_data.get("threshold"),
            "topic": topic
        }
    }

def test_discord_integration(webhook_config):
    """Test Discord integration with sample data"""
    
    print("🧪 Testing Discord Integration")
    print("=" * 35)
    
    sender = DiscordAlertSender(webhook_config)
    
    # Test alerts
    test_cases = [
        {
            "topic": "sensors/critical",
            "payload": {
                "equipmentId": "TEMP-001",
                "type": "Temperature Sensor",
                "location": "Reactor Room",
                "value": 95,
                "threshold": 85,
                "description": "Critical temperature exceeded - immediate action required"
            }
        },
        {
            "topic": "equipment/alerts",
            "payload": {
                "equipmentId": "PUMP-001", 
                "type": "Centrifugal Pump",
                "location": "Building A",
                "value": 78,
                "threshold": 75,
                "description": "Vibration levels elevated - schedule maintenance"
            }
        },
        {
            "topic": "equipment/status",
            "payload": {
                "equipmentId": "VALVE-003",
                "type": "Control Valve", 
                "location": "Process Line 2",
                "value": "normal",
                "description": "Routine status check - all systems operational"
            }
        }
    ]
    
    for test in test_cases:
        print(f"\n📤 Sending test alert for {test['payload']['equipmentId']}...")
        
        alert_data = mqtt_to_discord_alert(test["topic"], test["payload"])
        
        success = sender.send_alert(
            alert_data["channel"],
            alert_data["title"], 
            alert_data["message"],
            alert_data["severity"],
            alert_data["equipment_data"]
        )
        
        if success:
            print(f"✅ Test alert sent successfully")
        else:
            print(f"❌ Test alert failed")

if __name__ == "__main__":
    # Example webhook configuration (replace with real URLs)
    webhook_config = {
        "alerts": "DISCORD_ALERTS_WEBHOOK_URL_HERE",
        "logs": "DISCORD_LOGS_WEBHOOK_URL_HERE", 
        "general": "DISCORD_GENERAL_WEBHOOK_URL_HERE"
    }
    
    print("🎯 Discord Integration Script Ready!")
    print("=" * 40)
    print("")
    print("To use this script:")
    print("1. Get Discord webhook URLs from your server")
    print("2. Replace webhook URLs in the config")
    print("3. Run: python3 discord_webhook_integration.py")
    print("")
    print("The script is ready for:")
    print("✅ MQTT → Discord alert routing")
    print("✅ Severity-based channel routing") 
    print("✅ Rich embed formatting")
    print("✅ Equipment data display")
    print("✅ Error handling and logging")
    print("")
    print("Webhook URLs needed:")
    for channel in webhook_config.keys():
        print(f"  #{channel}: {webhook_config[channel]}")
    
    # If webhook URLs are configured, run test
    if all(url != f"DISCORD_{channel.upper()}_WEBHOOK_URL_HERE" for channel, url in webhook_config.items()):
        test_discord_integration(webhook_config)
    else:
        print("\n💡 Configure webhook URLs and run again to test!")