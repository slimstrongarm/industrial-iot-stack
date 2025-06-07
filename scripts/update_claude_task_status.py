#!/usr/bin/env python3
import os
import sys
from datetime import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build

CREDENTIALS_FILE = '/home/server/google-sheets-credentials.json'
SPREADSHEET_ID = '1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do'

def update_task_status(task_id, new_status, completion_notes=""):
    """Update Claude Task status in Google Sheets"""
    try:
        creds = service_account.Credentials.from_service_account_file(
            CREDENTIALS_FILE,
            scopes=['https://www.googleapis.com/auth/spreadsheets']
        )
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()
        
        # Read current data to find the task
        result = sheet.values().get(
            spreadsheetId=SPREADSHEET_ID,
            range='Claude Tasks!A1:K20'
        ).execute()
        
        values = result.get('values', [])
        
        # Find the task row
        for i, row in enumerate(values):
            if len(row) > 0 and row[0] == task_id:
                row_num = i + 1
                
                # Update status (column E, index 4)
                status_range = f'Claude Tasks!E{row_num}'
                status_update = {
                    'values': [[new_status]]
                }
                sheet.values().update(
                    spreadsheetId=SPREADSHEET_ID,
                    range=status_range,
                    valueInputOption='RAW',
                    body=status_update
                ).execute()
                
                # Update completion timestamp (column J, index 9)
                if new_status.lower() == 'complete':
                    timestamp_range = f'Claude Tasks!J{row_num}'
                    timestamp_update = {
                        'values': [[datetime.now().strftime('%m/%d/%Y %H:%M:%S')]]
                    }
                    sheet.values().update(
                        spreadsheetId=SPREADSHEET_ID,
                        range=timestamp_range,
                        valueInputOption='RAW',
                        body=timestamp_update
                    ).execute()
                
                print(f"✅ Updated {task_id} status to: {new_status}")
                return True
                
        print(f"❌ Task {task_id} not found")
        return False
        
    except Exception as e:
        print(f"❌ Error updating task: {e}")
        return False

# Update CT-001 to Complete
if __name__ == "__main__":
    print("🔄 Updating CT-001 status...")
    
    # Mark CT-001 as complete
    success = update_task_status("CT-001", "Complete")
    
    if success:
        # Add completion log to Agent Activities
        try:
            creds = service_account.Credentials.from_service_account_file(
                CREDENTIALS_FILE,
                scopes=['https://www.googleapis.com/auth/spreadsheets']
            )
            service = build('sheets', 'v4', credentials=creds)
            sheet = service.spreadsheets()
            
            timestamp = datetime.now().strftime('%m/%d/%Y %H:%M:%S')
            log_entry = [
                timestamp,
                'server-claude',
                'CT-001 Complete',
                'Docker audit complete: 3 containers running (EMQX, Node-RED, TimescaleDB), system-wide wrappers working',
                'Complete'
            ]
            
            sheet.values().append(
                spreadsheetId=SPREADSHEET_ID,
                range='Agent Activities!A:E',
                valueInputOption='RAW',
                insertDataOption='INSERT_ROWS',
                body={'values': [log_entry]}
            ).execute()
            
            print("✅ Added completion log to Agent Activities")
            
        except Exception as e:
            print(f"❌ Error logging completion: {e}")
    
    print("📋 CT-001 Docker Setup audit complete!")
    print("🎯 Ready to proceed with CT-002: MQTT Config")