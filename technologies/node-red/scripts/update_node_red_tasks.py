#!/usr/bin/env python3
"""
Add Node-RED flow deployment tasks to Claude Tasks sheet
"""

from googleapiclient.discovery import build
from google.oauth2 import service_account
from datetime import datetime

# Configuration
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'credentials/iot-stack-credentials.json'
SPREADSHEET_ID = '1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do'
SHEET_NAME = 'Claude Tasks'

def get_sheets_service():
    """Initialize Google Sheets service"""
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=credentials)
    return service.spreadsheets()

def add_node_red_tasks():
    """Add Node-RED flow deployment tasks"""
    try:
        sheet = get_sheets_service()
        
        # Get current data to find the last row
        result = sheet.values().get(
            spreadsheetId=SPREADSHEET_ID,
            range=f'{SHEET_NAME}!A:J'
        ).execute()
        
        values = result.get('values', [])
        last_row = len(values)
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M')
        
        # New Node-RED tasks
        new_tasks = [
            ['CT-010', 'Server Claude', 'Node-RED Flows', 'High', 'Pending',
             'Import MQTT Alert Bridge flow (mqtt-to-alerts-bridge.json)',
             'Alert thresholds monitoring brewery data and publishing to n8n',
             'CT-007', current_time, ''],
            ['CT-011', 'Server Claude', 'Node-RED Flows', 'High', 'Pending', 
             'Import n8n Command Bridge flow (n8n-to-ignition-commands.json)',
             'Commands from n8n written back to Ignition OPC-UA tags',
             'CT-007', current_time, ''],
            ['CT-012', 'Mac Claude', 'Documentation', 'Medium', 'Complete',
             'Create end-to-end test scenario and demo script',
             'Complete demo guide with boiler overheating crisis scenario',
             'CT-009', current_time, current_time]
        ]
        
        # Add new tasks starting from the next available row
        updates = []
        for i, task in enumerate(new_tasks):
            row_num = last_row + 1 + i
            updates.append({
                'range': f'{SHEET_NAME}!A{row_num}:J{row_num}',
                'values': [task]
            })
        
        # Execute updates
        if updates:
            batch_update_request = {
                'valueInputOption': 'RAW',
                'data': updates
            }
            
            sheet.values().batchUpdate(
                spreadsheetId=SPREADSHEET_ID,
                body=batch_update_request
            ).execute()
            
            print(f"✅ Added {len(new_tasks)} Node-RED deployment tasks!")
            print("\n📋 New Tasks Added:")
            for task in new_tasks:
                status_icon = "✅" if task[4] == "Complete" else "⏳"
                print(f"   {status_icon} {task[0]} ({task[1]}): {task[5][:60]}...")
            
            print("\n🔄 Complete Data Loop Now Ready:")
            print("   📊 Ignition → Node-RED → MQTT → n8n → WhatsApp")  
            print("   🎛️ n8n → MQTT → Node-RED → Ignition (commands)")
            print("   🧪 End-to-end test scenario documented")
            
            return True
        else:
            print("❌ No updates to make")
            return False
            
    except Exception as e:
        print(f"❌ Error updating Google Sheets: {e}")
        return False

if __name__ == "__main__":
    print("🔄 Adding Node-RED deployment tasks to Claude Tasks...")
    
    if add_node_red_tasks():
        print("\n" + "="*80)
        print("🎉 Node-RED flows ready for deployment!")
        print("🚀 Server Claude can now complete the closed-loop system")
        print("📱 Friday demo ready with complete data flow")
    else:
        print("\n❌ Failed to update Claude Tasks sheet")