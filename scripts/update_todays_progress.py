#!/usr/bin/env python3
"""
Update Claude Tasks in Google Sheets with today's Node-RED cleanup progress
"""

from googleapiclient.discovery import build
from google.oauth2 import service_account
from datetime import datetime
import os

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

def update_todays_tasks():
    """Update Claude Tasks sheet with today's progress"""
    try:
        sheet = get_sheets_service()
        
        # Get current data to find where to add new tasks
        result = sheet.values().get(
            spreadsheetId=SPREADSHEET_ID,
            range=f'{SHEET_NAME}!A:H'
        ).execute()
        
        values = result.get('values', [])
        current_date = datetime.now().strftime('%Y-%m-%d')
        
        # Find CT-035 and update it to Complete
        updates = []
        next_row = len(values) + 1
        
        for i, row in enumerate(values):
            if i == 0:  # Skip header
                continue
            if len(row) > 0 and row[0] == 'CT-035':
                # Update CT-035 status to Complete
                updates.append({
                    'range': f'{SHEET_NAME}!E{i+1}',  # Status column (E)
                    'values': [['Complete']]
                })
                print(f"✅ Updated CT-035 status to Complete")
                break
        
        # Add new tasks for today's work
        new_tasks = [
            ['CT-039', 'Mac Claude', 'Node-RED Cleanup', 'High', 'Complete', 
             'Clean Node-RED UI from 33 flows to 8-10 essential flows for production readiness', 
             'Consolidated flows, removed test/debug flows, 71% reduction achieved', 'CT-038'],
            
            ['CT-040', 'Mac Claude', 'UI Restoration', 'High', 'Complete',
             'Restore Integration tab with protocol status table and test buttons',
             'Working Integration tab with real-time protocol monitoring', 'CT-039'],
            
            ['CT-041', 'Mac Claude', 'Connection Test', 'High', 'Complete',
             'Validate OPC UA connection between Node-RED and Ignition Edge',
             'Confirmed working OPC connection on port 62541', 'CT-040'],
            
            ['CT-042', 'Mac Claude', 'Integration Test', 'High', 'Pending',
             'Test end-to-end data flow: MQTT → Node-RED → Ignition with real data',
             'Data flows from MQTT through to Ignition tags successfully', 'CT-041'],
            
            ['CT-043', 'Mac Claude', 'MQTT Setup', 'Medium', 'Blocked',
             'Configure Steel Bonnet production MQTT broker connection',
             'Connected to Steel Bonnet production MQTT broker', 'Need broker address'],
            
            ['CT-044', 'Mac Claude', 'Brewery Testing', 'High', 'Pending',
             'Test with real brewery sensor data (HLT heat system, chillers, etc.)',
             'Real brewery data visible in Ignition through Node-RED', 'CT-042']
        ]
        
        # Add new tasks starting from the next available row
        if new_tasks:
            range_to_update = f'{SHEET_NAME}!A{next_row}:H{next_row + len(new_tasks) - 1}'
            updates.append({
                'range': range_to_update,
                'values': new_tasks
            })
            print(f"✅ Adding {len(new_tasks)} new tasks starting at row {next_row}")
        
        # Execute all updates
        if updates:
            body = {
                'valueInputOption': 'RAW',
                'data': updates
            }
            
            result = sheet.values().batchUpdate(
                spreadsheetId=SPREADSHEET_ID,
                body=body
            ).execute()
            
            print(f"🎯 Successfully updated {result.get('totalUpdatedCells')} cells")
            print("📊 Today's major achievements added to Google Sheets:")
            print("   • Node-RED cleanup (33 → 9 flows, 71% reduction)")
            print("   • Integration tab restoration")
            print("   • OPC UA connection validation")
            print("   • Next phase planning (end-to-end testing)")
            
        else:
            print("❌ No updates to make")
            
    except Exception as e:
        print(f"❌ Error updating sheets: {e}")
        return False
    
    return True

if __name__ == "__main__":
    # Change to script directory to find credentials
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(os.path.dirname(script_dir))  # Go to project root
    
    print("🚀 Updating Google Sheets Claude Tasks...")
    success = update_todays_tasks()
    
    if success:
        print("\n✅ Google Sheets update complete!")
        print("🔗 View at: https://docs.google.com/spreadsheets/d/1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do/edit")
    else:
        print("\n❌ Update failed - check credentials and permissions")