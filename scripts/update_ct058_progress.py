#!/usr/bin/env python3
"""
Update CT-058 status to In Progress with dashboard creation details
"""

from googleapiclient.discovery import build
from google.oauth2 import service_account
from datetime import datetime
import os

# Configuration
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'credentials/iot-stack-credentials.json'
SPREADSHEET_ID = '1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do'

def update_ct058_status():
    """Update CT-058 from Pending to In Progress"""
    
    try:
        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        
        service = build('sheets', 'v4', credentials=credentials)
        sheet = service.spreadsheets()
        
        # Get all data to find CT-058
        result = sheet.values().get(
            spreadsheetId=SPREADSHEET_ID,
            range='Claude Tasks!A:J'
        ).execute()
        
        values = result.get('values', [])
        ct058_row = None
        
        # Find CT-058 row
        for i, row in enumerate(values):
            if len(row) > 0 and row[0] == 'CT-058':
                ct058_row = i + 1  # Sheet rows are 1-indexed
                break
        
        if not ct058_row:
            print("❌ CT-058 not found in sheet")
            return False
        
        print(f"📍 Found CT-058 at row {ct058_row}")
        
        # Update Status to In Progress
        sheet.values().update(
            spreadsheetId=SPREADSHEET_ID,
            range=f'Claude Tasks!E{ct058_row}',
            valueInputOption='USER_ENTERED',
            body={'values': [['In Progress']]}
        ).execute()
        
        # Update Expected Output with current progress
        progress_output = """✅ Dashboard created with following sections:
• System Overview with health summary
• Docker Containers monitoring (7 containers)
• Industrial Systems status (MQTT, Node-RED, Ignition)
• Steel Bonnet Equipment real-time data
• System Resources with thresholds
• Recent Activity log
• Integration with unified_industrial_monitor.py ready"""
        
        sheet.values().update(
            spreadsheetId=SPREADSHEET_ID,
            range=f'Claude Tasks!G{ct058_row}',
            valueInputOption='USER_ENTERED',
            body={'values': [[progress_output]]}
        ).execute()
        
        print(f"✅ Successfully updated CT-058 to In Progress!")
        print(f"📊 Dashboard URL: https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error updating CT-058: {e}")
        return False

if __name__ == "__main__":
    print("📝 Updating CT-058 Monitoring Dashboard Task...")
    print("=" * 50)
    
    if not os.path.exists(SERVICE_ACCOUNT_FILE):
        print(f"❌ Credentials file not found")
        exit(1)
    
    if update_ct058_status():
        print("\n🎉 CT-058 successfully updated to In Progress!")
        print("📊 The Monitoring Dashboard tab has been created and is ready for use")
    else:
        print("\n❌ Failed to update CT-058")