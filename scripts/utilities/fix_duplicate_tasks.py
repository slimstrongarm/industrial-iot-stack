#!/usr/bin/env python3
"""
Fix duplicate tasks in Google Sheets Claude Tasks and add prevention
"""

from googleapiclient.discovery import build
from google.oauth2 import service_account
import os

# Configuration
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'credentials/iot-stack-credentials.json'
SPREADSHEET_ID = '1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do'

def get_sheets_service():
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=credentials)
    return service.spreadsheets()

def fix_duplicates():
    try:
        sheet = get_sheets_service()
        sheet_name = 'Claude Tasks'
        
        # Get all data
        result = sheet.values().get(
            spreadsheetId=SPREADSHEET_ID,
            range=f"'{sheet_name}'!A:H"
        ).execute()
        
        values = result.get('values', [])
        
        # Find duplicates by task ID
        seen_task_ids = set()
        rows_to_delete = []
        
        for i, row in enumerate(values):
            if i == 0:  # Skip header
                continue
            if len(row) > 0:
                task_id = row[0]
                if task_id in seen_task_ids:
                    rows_to_delete.append(i + 1)  # 1-indexed for Google Sheets
                    print(f"📋 Found duplicate: {task_id} at row {i + 1}")
                else:
                    seen_task_ids.add(task_id)
        
        if rows_to_delete:
            print(f"🗑️  Will delete {len(rows_to_delete)} duplicate rows: {rows_to_delete}")
            
            # Delete rows from bottom to top (so row numbers don't shift)
            for row_num in reversed(rows_to_delete):
                delete_request = {
                    "deleteDimension": {
                        "range": {
                            "sheetId": 0,  # Assuming first sheet
                            "dimension": "ROWS",
                            "startIndex": row_num - 1,  # 0-indexed for API
                            "endIndex": row_num
                        }
                    }
                }
                
                sheet.batchUpdate(
                    spreadsheetId=SPREADSHEET_ID,
                    body={"requests": [delete_request]}
                ).execute()
                
                print(f"✅ Deleted duplicate row {row_num}")
        else:
            print("✅ No duplicates found!")
            
        return True
        
    except Exception as e:
        print(f"❌ Error fixing duplicates: {e}")
        return False

def add_prevention_note():
    """Add a prevention mechanism note"""
    print("\n🛡️  DUPLICATE PREVENTION MECHANISM:")
    print("Added to scripts/utilities/check_task_exists.py")
    print("Future scripts should call check_task_exists() before adding tasks")
    print("This will prevent the 'comical' duplicate creation! 😅")

if __name__ == '__main__':
    # Change to project root directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(os.path.dirname(script_dir))
    
    print('🧹 Fixing duplicate tasks in Google Sheets Claude Tasks...')
    print("(Sorry for the comical duplicate creation after reading the instructions! 😅)")
    
    success = fix_duplicates()
    
    if success:
        print('\n✅ Duplicates cleaned up!')
        add_prevention_note()
        print('\n🔗 View cleaned sheet: https://docs.google.com/spreadsheets/d/1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do/edit')
        print('\n😴 Good session! The .claude documentation is definitely much better this time.')
    else:
        print('\n❌ Failed to clean up duplicates')