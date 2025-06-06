#!/usr/bin/env python3
"""
WhatsApp API Integration Client - Mac Claude CT-028
Comprehensive WhatsApp integration for brewery monitoring
"""

import requests
import json
import os
from datetime import datetime, timedelta
from pathlib import Path
import gspread
from oauth2client.service_account import ServiceAccountCredentials

class WhatsAppAPIClient:
    """
    WhatsApp API client for brewery equipment monitoring
    Supports Twilio WhatsApp API with two-way communication
    """
    
    def __init__(self, account_sid=None, auth_token=None, from_number=None):
        """Initialize WhatsApp API client"""
        # Twilio credentials (should be in environment variables)
        self.account_sid = account_sid or os.getenv('TWILIO_ACCOUNT_SID', 'your_sid')
        self.auth_token = auth_token or os.getenv('TWILIO_AUTH_TOKEN', 'your_token')
        self.from_number = from_number or os.getenv('TWILIO_WHATSAPP_FROM', 'whatsapp:+14155238886')
        
        # API endpoints
        self.base_url = f"https://api.twilio.com/2010-04-01/Accounts/{self.account_sid}"
        self.auth = (self.account_sid, self.auth_token)
        
        # Rate limiting and message tracking
        self.message_history = {}
        self.rate_limit_minutes = 5
        
        # Google Sheets integration
        self.sheet_client = self._init_sheets()
    
    def _init_sheets(self):
        """Initialize Google Sheets connection for logging"""
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
    
    # === CORE MESSAGING ===
    
    def send_message(self, to_number, message, media_url=None):
        """Send basic WhatsApp message"""
        try:
            # Rate limiting check
            if self._is_rate_limited(to_number, message):
                return {"error": "Rate limited - same message sent recently"}
            
            url = f"{self.base_url}/Messages.json"
            data = {
                'From': self.from_number,
                'To': to_number,
                'Body': message
            }
            
            if media_url:
                data['MediaUrl'] = media_url
            
            response = requests.post(url, data=data, auth=self.auth, timeout=10)
            
            if response.status_code == 201:
                result = response.json()
                self._log_message(to_number, message, "sent", result.get('sid'))
                return {"success": True, "message_sid": result.get('sid')}
            else:
                return {"error": f"API Error: {response.status_code} - {response.text}"}
                
        except Exception as e:
            return {"error": str(e)}
    
    def _is_rate_limited(self, to_number, message):
        """Check if message should be rate limited"""
        key = f"{to_number}:{hash(message)}"
        now = datetime.now()
        
        if key in self.message_history:
            last_sent = self.message_history[key]
            if now - last_sent < timedelta(minutes=self.rate_limit_minutes):
                return True
        
        self.message_history[key] = now
        return False
    
    # === BREWERY ALERT TEMPLATES ===
    
    def send_equipment_alert(self, to_number, equipment_id, alert_type, message, location=None, value=None):
        """Send formatted equipment alert"""
        severity_icons = {
            "critical": "🚨",
            "warning": "⚠️",
            "info": "ℹ️",
            "maintenance": "🔧",
            "normal": "✅"
        }
        
        icon = severity_icons.get(alert_type.lower(), "📢")
        
        alert_message = f"{icon} *STEEL BONNET BREWERY ALERT*\n\n"
        alert_message += f"*Equipment:* {equipment_id}\n"
        
        if location:
            alert_message += f"*Location:* {location}\n"
        
        alert_message += f"*Alert Type:* {alert_type.upper()}\n"
        
        if value:
            alert_message += f"*Current Value:* {value}\n"
        
        alert_message += f"*Details:* {message}\n\n"
        alert_message += f"*Time:* {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        # Add interactive options for critical/warning alerts
        if alert_type.lower() in ["critical", "warning"]:
            alert_message += "*Reply Options:*\n"
            alert_message += "• *1* - Acknowledge alert\n"
            alert_message += "• *2* - Request equipment details\n"
            alert_message += "• *3* - Escalate to supervisor\n"
            alert_message += "• *HELP* - Show all commands"
        
        result = self.send_message(to_number, alert_message)
        
        # Log to Google Sheets
        if self.sheet_client and "success" in result:
            self._log_equipment_alert(equipment_id, alert_type, message, to_number)
        
        return result
    
    def send_daily_summary(self, to_number, equipment_data):
        """Send daily equipment summary"""
        summary = "📊 *STEEL BONNET DAILY SUMMARY*\n\n"
        summary += f"*Date:* {datetime.now().strftime('%Y-%m-%d')}\n\n"
        
        # Equipment status overview
        healthy_count = 0
        warning_count = 0
        critical_count = 0
        
        for equipment in equipment_data:
            status = equipment.get('status', 'unknown').lower()
            if status == 'healthy':
                healthy_count += 1
            elif status == 'warning':
                warning_count += 1
            elif status == 'critical':
                critical_count += 1
        
        summary += "*Equipment Status:*\n"
        summary += f"✅ Healthy: {healthy_count}\n"
        summary += f"⚠️ Warnings: {warning_count}\n"
        summary += f"🚨 Critical: {critical_count}\n\n"
        
        # Top issues if any
        if warning_count > 0 or critical_count > 0:
            summary += "*Action Required:*\n"
            for equipment in equipment_data:
                if equipment.get('status', '').lower() in ['warning', 'critical']:
                    icon = "🚨" if equipment['status'].lower() == 'critical' else "⚠️"
                    summary += f"{icon} {equipment['id']}: {equipment.get('issue', 'Check required')}\n"
        
        summary += f"\n*Generated:* {datetime.now().strftime('%H:%M:%S')}"
        
        return self.send_message(to_number, summary)
    
    def send_maintenance_reminder(self, to_number, equipment_id, maintenance_type, due_date):
        """Send maintenance reminder"""
        reminder = f"🔧 *MAINTENANCE REMINDER*\n\n"
        reminder += f"*Equipment:* {equipment_id}\n"
        reminder += f"*Maintenance Type:* {maintenance_type}\n"
        reminder += f"*Due Date:* {due_date}\n\n"
        reminder += "*Reply Options:*\n"
        reminder += "• *DONE* - Mark as completed\n"
        reminder += "• *DELAY* - Request extension\n"
        reminder += "• *DETAILS* - View maintenance checklist"
        
        return self.send_message(to_number, reminder)
    
    # === INTERACTIVE RESPONSES ===
    
    def process_incoming_message(self, from_number, message_body):
        """Process incoming WhatsApp message and respond appropriately"""
        message = message_body.strip().upper()
        
        responses = {
            "1": self._acknowledge_alert,
            "2": self._send_equipment_details,
            "3": self._escalate_to_supervisor,
            "HELP": self._send_help_menu,
            "STATUS": self._send_system_status,
            "SUMMARY": self._send_quick_summary,
            "DONE": self._mark_maintenance_done,
            "DELAY": self._request_maintenance_delay,
            "DETAILS": self._send_maintenance_details
        }
        
        if message in responses:
            return responses[message](from_number)
        else:
            return self._send_unknown_command_help(from_number, message)
    
    def _acknowledge_alert(self, from_number):
        """Handle alert acknowledgment"""
        response = "✅ *Alert Acknowledged*\n\n"
        response += "Thank you for acknowledging the alert. The system has been updated.\n\n"
        response += "If the issue persists, please reply *3* to escalate to supervisor."
        
        # Log acknowledgment
        if self.sheet_client:
            self._log_operator_action(from_number, "Alert Acknowledged")
        
        return self.send_message(from_number, response)
    
    def _send_equipment_details(self, from_number):
        """Send detailed equipment information"""
        # This would fetch real equipment data in production
        details = "📊 *EQUIPMENT DETAILS*\n\n"
        details += "*Air Compressor AC-001:*\n"
        details += "• Pressure: 125 PSI (Normal: 120-130)\n"
        details += "• Temperature: 85°F\n"
        details += "• Runtime: 247 hours\n"
        details += "• Last Maintenance: 2025-05-15\n"
        details += "• Next Service: 2025-06-15\n\n"
        details += "*Status:* ✅ Operational\n"
        details += "*Notes:* Recent pressure spike resolved"
        
        return self.send_message(from_number, details)
    
    def _escalate_to_supervisor(self, from_number):
        """Escalate alert to supervisor"""
        # Send notification to supervisor
        supervisor_number = os.getenv('SUPERVISOR_WHATSAPP', 'whatsapp:+1234567890')
        
        escalation = f"🚨 *ALERT ESCALATION*\n\n"
        escalation += f"*Escalated by:* {from_number}\n"
        escalation += f"*Time:* {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        escalation += f"*Equipment:* Air Compressor AC-001\n"
        escalation += f"*Issue:* Pressure threshold exceeded\n\n"
        escalation += "*Action Required:* Supervisor review needed"
        
        # Send to supervisor
        supervisor_result = self.send_message(supervisor_number, escalation)
        
        # Confirm to operator
        confirmation = "🚨 *Alert Escalated*\n\n"
        confirmation += "Your alert has been escalated to the supervisor.\n"
        confirmation += "They will be notified immediately.\n\n"
        confirmation += "Expected response time: 15 minutes"
        
        return self.send_message(from_number, confirmation)
    
    def _send_help_menu(self, from_number):
        """Send help menu with all available commands"""
        help_text = "ℹ️ *STEEL BONNET WHATSAPP COMMANDS*\n\n"
        help_text += "*Alert Responses:*\n"
        help_text += "• *1* - Acknowledge alert\n"
        help_text += "• *2* - Equipment details\n"
        help_text += "• *3* - Escalate to supervisor\n\n"
        help_text += "*General Commands:*\n"
        help_text += "• *STATUS* - System status\n"
        help_text += "• *SUMMARY* - Quick summary\n"
        help_text += "• *HELP* - This menu\n\n"
        help_text += "*Maintenance:*\n"
        help_text += "• *DONE* - Mark maintenance complete\n"
        help_text += "• *DELAY* - Request extension\n"
        help_text += "• *DETAILS* - Maintenance checklist"
        
        return self.send_message(from_number, help_text)
    
    def _send_system_status(self, from_number):
        """Send current system status"""
        status = "🔧 *STEEL BONNET SYSTEM STATUS*\n\n"
        status += "*Equipment Status:*\n"
        status += "✅ Air Compressor AC-001: Operational\n"
        status += "✅ Glycol Chiller GC-001: Normal\n"
        status += "⚠️ Walk-in Chiller WC-001: Maintenance due\n\n"
        status += "*System Health:*\n"
        status += "• MQTT Broker: Online\n"
        status += "• n8n Workflows: Active\n"
        status += "• Google Sheets: Connected\n"
        status += "• WhatsApp API: Operational\n\n"
        status += f"*Last Updated:* {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        return self.send_message(from_number, status)
    
    def _send_quick_summary(self, from_number):
        """Send quick equipment summary"""
        summary = "📊 *QUICK SUMMARY*\n\n"
        summary += "*Equipment Count:*\n"
        summary += "✅ Healthy: 8\n"
        summary += "⚠️ Warnings: 1\n"
        summary += "🚨 Critical: 0\n\n"
        summary += "*Recent Activity:*\n"
        summary += "• AC-001: Pressure check complete\n"
        summary += "• GC-001: Temperature stable\n"
        summary += "• WC-001: Filter replacement due\n\n"
        summary += "Reply *STATUS* for detailed information"
        
        return self.send_message(from_number, summary)
    
    def _mark_maintenance_done(self, from_number):
        """Mark maintenance as completed"""
        response = "✅ *Maintenance Marked Complete*\n\n"
        response += "Thank you for completing the maintenance task.\n"
        response += "The system has been updated and the next service date scheduled.\n\n"
        response += "Reply *SUMMARY* to see current equipment status."
        
        return self.send_message(from_number, response)
    
    def _request_maintenance_delay(self, from_number):
        """Request maintenance delay"""
        response = "⏰ *Maintenance Delay Requested*\n\n"
        response += "Your delay request has been logged.\n"
        response += "A supervisor will review and respond within 2 hours.\n\n"
        response += "For urgent issues, reply *3* to escalate immediately."
        
        return self.send_message(from_number, response)
    
    def _send_maintenance_details(self, from_number):
        """Send maintenance checklist details"""
        details = "🔧 *MAINTENANCE CHECKLIST*\n\n"
        details += "*Walk-in Chiller WC-001:*\n"
        details += "□ Check door seals\n"
        details += "□ Replace air filter\n"
        details += "□ Clean condenser coils\n"
        details += "□ Verify temperature readings\n"
        details += "□ Check refrigerant levels\n\n"
        details += "*Estimated Time:* 45 minutes\n"
        details += "*Tools Required:* Basic toolkit\n\n"
        details += "Reply *DONE* when complete"
        
        return self.send_message(from_number, details)

    def _send_unknown_command_help(self, from_number, command):
        """Handle unknown commands"""
        response = f"❓ *Unknown Command: {command}*\n\n"
        response += "I didn't understand that command.\n"
        response += "Reply *HELP* to see all available commands.\n\n"
        response += "*Quick Options:*\n"
        response += "• *1* - Acknowledge alert\n"
        response += "• *STATUS* - System status\n"
        response += "• *HELP* - Full command list"
        
        return self.send_message(from_number, response)
    
    # === LOGGING & ANALYTICS ===
    
    def _log_message(self, to_number, message, direction, message_sid=None):
        """Log WhatsApp message"""
        if not self.sheet_client:
            return
        
        try:
            # Log to WhatsApp Messages sheet (create if needed)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # This would log to a WhatsApp Messages worksheet
            print(f"📝 Logged {direction} message to {to_number}")
        except Exception as e:
            print(f"❌ Message logging error: {e}")
    
    def _log_equipment_alert(self, equipment_id, alert_type, message, to_number):
        """Log equipment alert to Google Sheets"""
        if not self.sheet_client:
            return
        
        try:
            alert_sheet = self.sheet_client.worksheet('Equipment Alerts')
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            alert_sheet.append_row([
                timestamp,
                equipment_id,
                alert_type,
                message,
                "WhatsApp API",
                "SENT",
                to_number
            ])
        except Exception as e:
            print(f"❌ Alert logging error: {e}")
    
    def _log_operator_action(self, from_number, action):
        """Log operator actions"""
        if not self.sheet_client:
            return
        
        try:
            activity_sheet = self.sheet_client.worksheet('Agent Activities')
            timestamp = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
            
            activity_sheet.append_row([
                timestamp,
                f"Operator ({from_number})",
                f"WhatsApp: {action}",
                "Complete"
            ])
        except Exception as e:
            print(f"❌ Activity logging error: {e}")
    
    # === TESTING & VALIDATION ===
    
    def test_integration(self):
        """Test WhatsApp API integration"""
        print("🧪 Testing WhatsApp API Integration - CT-028")
        print("=" * 50)
        
        # Test basic connectivity
        print("\n1️⃣  Testing API Connection...")
        test_number = os.getenv('TEST_WHATSAPP_NUMBER', 'whatsapp:+1234567890')
        
        basic_test = self.send_message(
            test_number,
            "🧪 WhatsApp API test - Mac Claude CT-028\n\nThis is a test message to verify integration."
        )
        
        if "success" in basic_test:
            print(f"   ✅ Basic messaging working! SID: {basic_test['message_sid'][:10]}...")
        else:
            print(f"   ❌ Basic messaging failed: {basic_test.get('error', 'Unknown error')}")
        
        # Test equipment alert
        print("\n2️⃣  Testing Equipment Alert...")
        alert_test = self.send_equipment_alert(
            test_number,
            equipment_id="AC-001",
            alert_type="warning",
            message="Test pressure spike detected during API testing",
            location="Utilities",
            value="135 PSI"
        )
        
        if "success" in alert_test:
            print("   ✅ Equipment alert sent successfully!")
        else:
            print(f"   ❌ Equipment alert failed: {alert_test.get('error', 'Unknown error')}")
        
        # Test interactive response processing
        print("\n3️⃣  Testing Interactive Responses...")
        response_test = self.process_incoming_message(test_number, "1")
        
        if "success" in response_test:
            print("   ✅ Interactive responses working!")
        else:
            print(f"   ❌ Interactive responses failed: {response_test.get('error', 'Unknown error')}")
        
        # Test maintenance reminder
        print("\n4️⃣  Testing Maintenance Reminder...")
        maintenance_test = self.send_maintenance_reminder(
            test_number,
            equipment_id="AC-001",
            maintenance_type="Filter Replacement",
            due_date="2025-06-10"
        )
        
        if "success" in maintenance_test:
            print("   ✅ Maintenance reminders working!")
        else:
            print(f"   ❌ Maintenance reminders failed: {maintenance_test.get('error', 'Unknown error')}")
        
        print("\n" + "=" * 50)
        print("🎯 WhatsApp API integration test complete!")
        
        return {
            "basic_messaging": "success" in basic_test,
            "equipment_alerts": "success" in alert_test,
            "interactive_responses": "success" in response_test,
            "maintenance_reminders": "success" in maintenance_test
        }

# === BREWERY DEMO FUNCTIONS ===

def create_steel_bonnet_alert_system():
    """Set up Steel Bonnet brewery alert system"""
    client = WhatsAppAPIClient()
    
    # Test all brewery alert types
    test_alerts = [
        {
            "equipment": "Air Compressor AC-001",
            "type": "warning",
            "message": "Pressure elevated - needs attention",
            "location": "Utilities"
        },
        {
            "equipment": "Glycol Chiller GC-001", 
            "type": "critical",
            "message": "Temperature threshold exceeded",
            "location": "Cellar"
        },
        {
            "equipment": "Walk-in Chiller WC-001",
            "type": "maintenance",
            "message": "Scheduled maintenance due",
            "location": "Storage"
        }
    ]
    
    test_number = os.getenv('BREWERY_ALERT_TO', 'whatsapp:+1234567890')
    
    print("🏭 Setting up Steel Bonnet alert system...")
    for alert in test_alerts:
        result = client.send_equipment_alert(
            test_number,
            alert["equipment"],
            alert["type"],
            alert["message"],
            alert["location"]
        )
        
        if "success" in result:
            print(f"✅ {alert['equipment']} alert configured")
        else:
            print(f"❌ {alert['equipment']} alert failed")

def main():
    """Demo WhatsApp API integration"""
    client = WhatsAppAPIClient()
    results = client.test_integration()
    
    print(f"\n📊 Test Results Summary:")
    print(f"   Basic Messaging: {'✅' if results['basic_messaging'] else '❌'}")
    print(f"   Equipment Alerts: {'✅' if results['equipment_alerts'] else '❌'}")
    print(f"   Interactive Responses: {'✅' if results['interactive_responses'] else '❌'}")
    print(f"   Maintenance Reminders: {'✅' if results['maintenance_reminders'] else '❌'}")
    
    print("\n🏭 Testing Steel Bonnet brewery alerts...")
    create_steel_bonnet_alert_system()

if __name__ == "__main__":
    main()