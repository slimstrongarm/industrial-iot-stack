#!/usr/bin/env python3
"""
Add Formbricks API integration tasks to Claude Tasks sheet
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

def add_formbricks_tasks():
    """Add Formbricks API integration tasks"""
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
        
        # New Formbricks API tasks
        new_tasks = [
            ['CT-018', 'Mac Claude', 'Formbricks Research', 'Medium', 'Complete',
             'Research Formbricks API capabilities and create integration guide',
             'Complete API documentation with endpoints and integration examples',
             'CT-015', current_time, current_time],
            ['CT-019', 'Server Claude', 'Formbricks API Key', 'Medium', 'Pending',
             'Obtain Formbricks API key and configure access for direct integration',
             'API key configured and tested with successful API calls',
             'CT-013', current_time, ''],
            ['CT-020', 'Mac Claude', 'Hybrid Integration', 'Medium', 'Pending',
             'Create hybrid Formbricks integration using both API and webhooks',
             'Python client supporting direct API + webhook processing',
             'CT-019', current_time, ''],
            ['CT-021', 'Both', 'Advanced Analytics', 'Low', 'Pending',
             'Build real-time analytics dashboard using Formbricks API',
             'Custom dashboard showing equipment inspection trends',
             'CT-020', current_time, '']
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
            
            print(f"✅ Added {len(new_tasks)} Formbricks API integration tasks!")
            print("\n📋 New Tasks Added:")
            for task in new_tasks:
                status_icon = "✅" if task[4] == "Complete" else "⏳"
                print(f"   {status_icon} {task[0]} ({task[1]}): {task[5][:60]}...")
            
            print("\n🔄 Formbricks API Benefits:")
            print("   📊 Direct access to form responses and analytics")  
            print("   ⚡ Real-time webhooks + on-demand API queries")
            print("   🎯 Custom business logic without n8n middleware")
            print("   📈 Advanced analytics and trend analysis")
            
            print("\n🚀 Integration Options:")
            print("   • Pure API: Formbricks → Python → Ignition")
            print("   • Hybrid: Webhooks for real-time + API for analytics")
            print("   • Enhanced n8n: API calls within workflows")
            
            print("\n📖 Documentation:")
            print("   • FORMBRICKS_API_INTEGRATION.md - Complete API guide")
            print("   • Full REST API endpoint reference")
            print("   • Industrial IoT use case examples")
            
            return True
        else:
            print("❌ No updates to make")
            return False
            
    except Exception as e:
        print(f"❌ Error updating Google Sheets: {e}")
        return False

if __name__ == "__main__":
    print("🔄 Adding Formbricks API integration tasks to Claude Tasks...")
    
    if add_formbricks_tasks():
        print("\n" + "="*80)
        print("🎉 Formbricks API integration tasks added!")
        print("🚀 Three-way API integration now possible:")
        print("   📝 Formbricks API - Form management and responses")
        print("   🔧 n8n API - Workflow execution and monitoring")  
        print("   📊 Google Sheets API - Task tracking and data logging")
        print("\n💪 This creates a powerful, flexible integration platform!")
    else:
        print("\n❌ Failed to update Claude Tasks sheet")