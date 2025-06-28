#!/usr/bin/env python3
import os
import json
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Load credentials
CREDENTIALS_FILE = '/Users/joshpayneair/Desktop/industrial-iot-stack/credentials/iot-stack-credentials.json'
SPREADSHEET_ID = '1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do'

# Initialize Google Sheets API
credentials = Credentials.from_service_account_file(
    CREDENTIALS_FILE,
    scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']
)
service = build('sheets', 'v4', credentials=credentials)

try:
    # Read Claude Tasks sheet
    sheet_range = 'Claude Tasks!A:F'
    result = service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID,
        range=sheet_range
    ).execute()
    
    values = result.get('values', [])
    
    if not values:
        print("No data found in Claude Tasks sheet")
    else:
        print(f"📊 Found {len(values)} rows in Claude Tasks sheet\n")
        
        # Find header row index
        header_idx = -1
        for i, row in enumerate(values):
            if row and 'ID' in str(row[0]) or 'Task ID' in str(row[0]):
                header_idx = i
                break
        
        if header_idx >= 0:
            headers = values[header_idx]
            print(f"Headers: {headers}\n")
            
            # Look for CT-084 through CT-090
            target_tasks = [f"CT-{i:03d}" for i in range(84, 91)]
            found_tasks = []
            
            for row in values[header_idx + 1:]:
                if row and len(row) > 0:
                    task_id = row[0] if row else ''
                    if task_id in target_tasks:
                        # Ensure row has enough columns
                        while len(row) < 6:
                            row.append('')
                        
                        task_info = {
                            'ID': row[0],
                            'Assigned To': row[1] if len(row) > 1 else '',
                            'Title/Task': row[2] if len(row) > 2 else '',
                            'Priority': row[3] if len(row) > 3 else '',
                            'Status': row[4] if len(row) > 4 else '',
                            'Description': row[5] if len(row) > 5 else ''
                        }
                        found_tasks.append(task_info)
            
            print("=" * 80)
            print("📋 TASKS CT-084 THROUGH CT-090")
            print("=" * 80)
            
            if found_tasks:
                for task in found_tasks:
                    print(f"\n🔹 Task ID: {task['ID']}")
                    print(f"   Assigned To: {task['Assigned To']}")
                    print(f"   Title: {task['Title/Task']}")
                    print(f"   Priority: {task['Priority']}")
                    print(f"   Status: {task['Status']}")
                    print(f"   Description: {task['Description'][:200]}..." if len(task['Description']) > 200 else f"   Description: {task['Description']}")
            else:
                print("\n❌ No tasks found in the range CT-084 to CT-090")
                print("\nShowing last 10 tasks for context:")
                for row in values[-10:]:
                    if row and len(row) > 0:
                        print(f"  - {row[0]}: {row[2] if len(row) > 2 else 'No title'} (Status: {row[4] if len(row) > 4 else 'Unknown'})")
        else:
            print("Could not find header row in Claude Tasks sheet")
            
except HttpError as error:
    print(f'❌ An error occurred: {error}')
except Exception as e:
    print(f'❌ Unexpected error: {e}')