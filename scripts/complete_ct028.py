#!/usr/bin/env python3
"""
Complete CT-028: WhatsApp API research and integration guide
"""

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pathlib import Path
from datetime import datetime

# Configuration
SHEET_ID = '1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do'
CREDS_FILE = str(Path.home() / 'Desktop/industrial-iot-stack/credentials/iot-stack-credentials.json')

def complete_ct028():
    """Mark CT-028 as complete with deliverables"""
    try:
        # Connect to Google Sheets
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_FILE, scope)
        client = gspread.authorize(creds)
        sheet = client.open_by_key(SHEET_ID)
        
        claude_sheet = sheet.worksheet('Claude Tasks')
        records = claude_sheet.get_all_records()
        
        # Find CT-028
        for i, record in enumerate(records):
            if record.get('Task ID') == 'CT-028':
                row_num = i + 2
                
                # Update status and completion
                claude_sheet.update_cell(row_num, 5, "Complete")  # Status
                claude_sheet.update_cell(row_num, 10, datetime.now().strftime("%Y-%m-%d %H:%M"))  # Completed
                
                # Update expected output with deliverables
                deliverables = (
                    "Complete WhatsApp API integration guide with Twilio implementation, "
                    "Node-RED flow for brewery alerts, test scripts, and quick setup guide. "
                    "All files in /whatsapp-integration/ folder."
                )
                claude_sheet.update_cell(row_num, 7, deliverables)  # Expected Output
                
                print("✅ CT-028 marked as Complete")
                break
        
        # Log completion activity
        agent_sheet = sheet.worksheet('Agent Activities')
        agent_sheet.append_row([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Mac Claude",
            "CT-028 WhatsApp API research complete",
            "Complete",
            "60 min",
            "Complete integration guide, Node-RED flow, test scripts created. Ready for brewery demo.",
            "Server Claude can deploy WhatsApp integration"
        ])
        
        print("\n🎯 CT-028 Deliverables:")
        print("   📋 WHATSAPP_API_INTEGRATION_GUIDE.md - Complete integration guide")
        print("   🔄 brewery-demo-flow.json - Node-RED flow for alerts")
        print("   🧪 test-alert.js - Testing and demo script")
        print("   ⚡ quick-setup.sh - One-command setup")
        print("   📖 README.md - Quick reference guide")
        print("   ⚙️  environment-variables.env - Configuration template")
        print("\n🚀 Ready for brewery demo implementation!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    complete_ct028()