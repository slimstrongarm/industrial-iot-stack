#!/usr/bin/env python3
"""
Add n8n API integration tasks to Claude Tasks sheet
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

def add_api_tasks():
    """Add n8n API integration tasks"""
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
        
        # New API integration tasks
        new_tasks = [
            ['CT-013', 'Server Claude', 'API Configuration', 'High', 'Pending',
             'Enable n8n API access and provide connection details (URL, auth)',
             'n8n API endpoint accessible from Mac Claude with auth details',
             'CT-006', current_time, ''],
            ['CT-014', 'Server Claude', 'API Testing', 'Medium', 'Pending', 
             'Test n8n API endpoints: workflows, executions, health check',
             'Confirmed API access with successful test execution',
             'CT-013', current_time, ''],
            ['CT-015', 'Mac Claude', 'Unified Monitor', 'Medium', 'Complete',
             'Create unified monitoring system for Sheets + n8n API',
             'Python scripts for combined Google Sheets and n8n monitoring',
             'CT-012', current_time, current_time],
            ['CT-016', 'Server Claude', 'Ignition Scripts', 'Medium', 'Pending',
             'Create Ignition scripts that call n8n API for alerts',
             'Working Ignition alarm scripts triggering n8n workflows',
             'CT-014', current_time, ''],
            ['CT-017', 'Both', 'Integration Test', 'High', 'Pending',
             'Full loop test: Ignition alarm → n8n API → WhatsApp → Command',
             'Complete closed-loop demonstration with API integration',
             'CT-016', current_time, '']
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
            
            print(f"✅ Added {len(new_tasks)} n8n API integration tasks!")
            print("\n📋 New Tasks Added:")
            for task in new_tasks:
                status_icon = "✅" if task[4] == "Complete" else "⏳"
                print(f"   {status_icon} {task[0]} ({task[1]}): {task[5][:60]}...")
            
            print("\n🔄 API Integration Benefits:")
            print("   🎯 Direct workflow execution from Ignition/Python")  
            print("   📊 Real-time monitoring of n8n workflows")
            print("   🔧 Automated retry and error handling")
            print("   📱 Instant alerts without MQTT middleware")
            
            print("\n📖 Documentation:")
            print("   • N8N_API_CAPABILITIES.md - Full API reference")
            print("   • scripts/n8n_api_client.py - Python API client")
            print("   • scripts/unified_monitoring.py - Combined monitoring")
            
            return True
        else:
            print("❌ No updates to make")
            return False
            
    except Exception as e:
        print(f"❌ Error updating Google Sheets: {e}")
        return False

if __name__ == "__main__":
    print("🔄 Adding n8n API integration tasks to Claude Tasks...")
    
    if add_api_tasks():
        print("\n" + "="*80)
        print("🎉 API integration tasks added!")
        print("🚀 Server Claude can now:")
        print("   1. Enable n8n API access (CT-013)")
        print("   2. Share connection details for remote access")
        print("   3. Create Ignition scripts for direct API calls")
        print("   4. Test the complete API-based integration")
    else:
        print("\n❌ Failed to update Claude Tasks sheet")