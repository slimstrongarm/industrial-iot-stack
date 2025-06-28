#!/usr/bin/env python3
"""
Check current Claude Tasks sheet format and get next Task ID
"""

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pathlib import Path

# Configuration
SHEET_ID = '1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do'
CREDS_FILE = str(Path.home() / 'Desktop/industrial-iot-stack/credentials/iot-stack-credentials.json')

def check_format():
    """Check current sheet format and get next Task ID"""
    try:
        # Connect to Google Sheets
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_FILE, scope)
        client = gspread.authorize(creds)
        sheet = client.open_by_key(SHEET_ID)
        
        print("✅ Connected to IoT Stack Progress Master")
        
        # Check Claude Tasks sheet
        print("\n📋 Checking Claude Tasks sheet format...")
        try:
            claude_sheet = sheet.worksheet('Claude Tasks')
            
            # Get headers
            headers = claude_sheet.row_values(1)
            print(f"Headers: {headers}")
            
            # Get all records
            records = claude_sheet.get_all_records()
            print(f"Total Claude tasks: {len(records)}")
            
            # Show current tasks
            if records:
                print("\nCurrent Claude Tasks:")
                for i, task in enumerate(records):
                    print(f"  {i+1}. {task}")
                    
                # Find highest Task ID
                task_ids = [task.get('Task ID', '') for task in records if task.get('Task ID')]
                print(f"\nCurrent Task IDs: {task_ids}")
                
                # Extract numbers and find next
                numbers = []
                for task_id in task_ids:
                    if task_id.startswith('CT-'):
                        try:
                            num = int(task_id.split('-')[1])
                            numbers.append(num)
                        except:
                            pass
                
                next_num = max(numbers) + 1 if numbers else 1
                next_id = f"CT-{next_num:03d}"
                print(f"Next Task ID should be: {next_id}")
                
            else:
                print("No Claude tasks found - sheet might be empty")
                print("Next Task ID should be: CT-001")
                
        except Exception as e:
            print(f"Error accessing Claude Tasks sheet: {e}")
            
        # Also check other sheets for format reference
        print("\n📊 All worksheets:")
        for ws in sheet.worksheets():
            print(f"  - {ws.title}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    check_format()