#!/usr/bin/env python3
"""
Discord Webhook Integration Client - Mac Claude CT-021
Team communication for Industrial IoT Stack
"""

import requests
import json
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pathlib import Path

# Discord webhook URL
DISCORD_WEBHOOK_URL = "https://discordapp.com/api/webhooks/1380061953883373660/lFn5d2hcBxAhaMJSpBNwjQNInczAGYQ-HYky70iSiNymhFXw7egnjUapMdAHZXrRWJhG"

class DiscordNotifier:
    """Discord webhook client for team communication"""
    
    def __init__(self):
        """Initialize Discord notifier"""
        self.webhook_url = DISCORD_WEBHOOK_URL
        self.sheet_client = self._init_sheets()
    
    def _init_sheets(self):
        """Initialize Google Sheets connection"""
        try:
            creds_file = str(Path.home() / 'Desktop/industrial-iot-stack/credentials/iot-stack-credentials.json')
            scope = ['https://spreadsheets.google.com/feeds',
                     'https://www.googleapis.com/auth/drive']
            creds = ServiceAccountCredentials.from_json_keyfile_name(creds_file, scope)
            client = gspread.authorize(creds)
            sheet_id = '1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do'
            return client.open_by_key(sheet_id)
        except Exception as e:
            print(f"⚠️  Sheets connection warning: {e}")
            return None
    
    def send_message(self, content, username="Industrial IoT Stack", avatar_url=None):
        """Send basic message to Discord"""
        try:
            payload = {
                "content": content,
                "username": username
            }
            if avatar_url:
                payload["avatar_url"] = avatar_url
            
            response = requests.post(self.webhook_url, json=payload, timeout=10)
            return response.status_code == 204
        except Exception as e:
            print(f"❌ Discord send error: {e}")
            return False
    
    def send_embed(self, title, description, color=0x00ff00, fields=None, footer=None):
        """Send rich embed message to Discord"""
        try:
            embed = {
                "title": title,
                "description": description,
                "color": color,
                "timestamp": datetime.utcnow().isoformat()
            }
            
            if fields:
                embed["fields"] = fields
            
            if footer:
                embed["footer"] = {"text": footer}
            
            payload = {
                "embeds": [embed],
                "username": "IoT Stack Monitor"
            }
            
            response = requests.post(self.webhook_url, json=payload, timeout=10)
            return response.status_code == 204
        except Exception as e:
            print(f"❌ Discord embed error: {e}")
            return False
    
    def notify_task_completion(self, task_id, task_description, completed_by):
        """Notify team of task completion"""
        fields = [
            {"name": "Task ID", "value": task_id, "inline": True},
            {"name": "Completed By", "value": completed_by, "inline": True},
            {"name": "Status", "value": "✅ Complete", "inline": True}
        ]
        
        return self.send_embed(
            title="📋 Task Completed",
            description=task_description,
            color=0x00ff00,  # Green
            fields=fields,
            footer="Industrial IoT Stack - Team Coordination"
        )
    
    def notify_equipment_alert(self, equipment_id, alert_type, message, location=None):
        """Notify team of equipment alerts"""
        color_map = {
            "critical": 0xff0000,    # Red
            "warning": 0xffa500,     # Orange
            "info": 0x0099ff         # Blue
        }
        
        fields = [
            {"name": "Equipment", "value": equipment_id, "inline": True},
            {"name": "Type", "value": alert_type.upper(), "inline": True}
        ]
        
        if location:
            fields.append({"name": "Location", "value": location, "inline": True})
        
        return self.send_embed(
            title="🚨 Equipment Alert",
            description=message,
            color=color_map.get(alert_type.lower(), 0x0099ff),
            fields=fields,
            footer="Steel Bonnet Brewery Monitoring"
        )
    
    def notify_system_status(self, system_name, status, details=None):
        """Notify team of system status changes"""
        status_colors = {
            "healthy": 0x00ff00,     # Green
            "warning": 0xffa500,     # Orange
            "error": 0xff0000,       # Red
            "offline": 0x808080      # Gray
        }
        
        status_emojis = {
            "healthy": "✅",
            "warning": "⚠️",
            "error": "❌",
            "offline": "⭕"
        }
        
        fields = [
            {"name": "System", "value": system_name, "inline": True},
            {"name": "Status", "value": f"{status_emojis.get(status, '❓')} {status.upper()}", "inline": True}
        ]
        
        description = details or f"{system_name} status update"
        
        return self.send_embed(
            title="🔧 System Status Update",
            description=description,
            color=status_colors.get(status.lower(), 0x0099ff),
            fields=fields,
            footer="Industrial IoT Stack Monitoring"
        )
    
    def notify_team_coordination(self, message, priority="normal"):
        """Send team coordination message"""
        priority_colors = {
            "low": 0x808080,      # Gray
            "normal": 0x0099ff,   # Blue
            "high": 0xffa500,     # Orange
            "urgent": 0xff0000    # Red
        }
        
        priority_icons = {
            "low": "ℹ️",
            "normal": "📢",
            "high": "⚡",
            "urgent": "🚨"
        }
        
        icon = priority_icons.get(priority, "📢")
        color = priority_colors.get(priority, 0x0099ff)
        
        return self.send_embed(
            title=f"{icon} Team Coordination",
            description=message,
            color=color,
            footer="Industrial IoT Stack - Team Communication"
        )
    
    def announce_discord_webhook_ready(self):
        """Announce that Discord integration is ready"""
        fields = [
            {"name": "Team Members", "value": "• Architect (Josh)\n• Mac Claude\n• Server Claude", "inline": False},
            {"name": "Capabilities", "value": "• Equipment alerts\n• Task coordination\n• System monitoring\n• Mobile notifications", "inline": False},
            {"name": "Integration", "value": "• Google Sheets\n• n8n workflows\n• WhatsApp alerts\n• Formbricks forms", "inline": False}
        ]
        
        return self.send_embed(
            title="🎉 Discord Integration Active!",
            description="Industrial IoT Stack team communication is now live. All three team members can coordinate through this channel.",
            color=0x7289da,  # Discord blurple
            fields=fields,
            footer="Mac Claude - CT-021 Complete"
        )
    
    def log_to_sheets(self, message_type, content, success):
        """Log Discord messages to Google Sheets"""
        if not self.sheet_client:
            return False
        
        try:
            # Log to Agent Activities
            agent_sheet = self.sheet_client.worksheet('Agent Activities')
            timestamp = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
            
            status = "Success" if success else "Failed"
            agent_sheet.append_row([
                timestamp,
                "Mac Claude",
                f"Discord {message_type}: {content[:50]}...",
                status
            ])
            return True
        except Exception as e:
            print(f"❌ Sheets logging error: {e}")
            return False

def main():
    """Test Discord integration and announce readiness"""
    notifier = DiscordNotifier()
    
    print("🔧 Testing Discord webhook integration...")
    
    # Test basic message
    basic_test = notifier.send_message("🧪 Discord webhook test - Mac Claude CT-021")
    print(f"Basic message: {'✅' if basic_test else '❌'}")
    
    # Test equipment alert
    alert_test = notifier.notify_equipment_alert(
        equipment_id="AC-001",
        alert_type="warning", 
        message="Air compressor pressure slightly elevated",
        location="Utilities"
    )
    print(f"Equipment alert: {'✅' if alert_test else '❌'}")
    
    # Test system status
    status_test = notifier.notify_system_status(
        system_name="n8n Workflows",
        status="healthy",
        details="All automation workflows running normally"
    )
    print(f"System status: {'✅' if status_test else '❌'}")
    
    # Announce Discord integration is ready
    announce_test = notifier.announce_discord_webhook_ready()
    print(f"Integration announcement: {'✅' if announce_test else '❌'}")
    
    # Test team coordination
    coord_test = notifier.notify_team_coordination(
        "Discord webhook integration complete! Ready for Friday brewery demo coordination.",
        priority="high"
    )
    print(f"Team coordination: {'✅' if coord_test else '❌'}")
    
    print("\n🎯 Discord integration testing complete!")

if __name__ == "__main__":
    main()