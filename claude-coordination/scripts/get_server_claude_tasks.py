#!/usr/bin/env python3
import os
import sys
from datetime import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Add the credentials path
CREDENTIALS_FILE = '/home/server/google-sheets-credentials.json'
SPREADSHEET_ID = '1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do'

print("🔍 Getting Server Claude tasks directly...")

try:
    # Initialize credentials
    creds = service_account.Credentials.from_service_account_file(
        CREDENTIALS_FILE,
        scopes=['https://www.googleapis.com/auth/spreadsheets']
    )
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    
    # Read Claude Tasks sheet
    range_name = 'Claude Tasks!A1:J20'  # Direct range without escaping
    result = sheet.values().get(
        spreadsheetId=SPREADSHEET_ID,
        range=range_name
    ).execute()
    
    values = result.get('values', [])
    
    if values:
        print(f"✅ Found {len(values)} rows in Claude Tasks")
        
        # Parse header
        headers = values[0] if values else []
        print(f"\n📋 Headers: {' | '.join(headers)}")
        print("=" * 120)
        
        # Look for Server Claude tasks
        server_tasks = []
        for i, row in enumerate(values[1:], 1):
            if len(row) >= 2:
                task_id = row[0] if len(row) > 0 else ''
                instance = row[1] if len(row) > 1 else ''
                
                if 'server claude' in str(instance).lower():
                    task_type = row[2] if len(row) > 2 else ''
                    priority = row[3] if len(row) > 3 else ''
                    status = row[4] if len(row) > 4 else ''
                    description = row[5] if len(row) > 5 else ''
                    expected_output = row[6] if len(row) > 6 else ''
                    dependencies = row[7] if len(row) > 7 else ''
                    
                    server_tasks.append({
                        'row': i + 1,
                        'task_id': task_id,
                        'task_type': task_type,
                        'priority': priority,
                        'status': status,
                        'description': description,
                        'expected_output': expected_output,
                        'dependencies': dependencies
                    })
                    
                    print(f"\n🎯 TASK {task_id}: {task_type}")
                    print(f"   Priority: {priority}")
                    print(f"   Status: {status}")
                    print(f"   Description: {description}")
                    print(f"   Expected Output: {expected_output}")
                    print(f"   Dependencies: {dependencies}")
                    print("-" * 80)
        
        print(f"\n✅ Found {len(server_tasks)} tasks assigned to Server Claude")
        
        # Show summary
        if server_tasks:
            print("\n📊 TASK SUMMARY:")
            for task in server_tasks:
                print(f"  {task['task_id']}: {task['task_type']} ({task['status']}) - {task['priority']} Priority")
        
    else:
        print("❌ No data found in Claude Tasks sheet")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()