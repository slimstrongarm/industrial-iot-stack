#!/usr/bin/env python3
"""
Check for CT-028 task in Google Sheets
"""

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pathlib import Path

# Configuration
SHEET_ID = '1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do'
CREDS_FILE = str(Path.home() / 'Desktop/industrial-iot-stack/credentials/iot-stack-credentials.json')

def check_ct028():
    """Look for CT-028 task details"""
    try:
        # Connect to Google Sheets
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_FILE, scope)
        client = gspread.authorize(creds)
        sheet = client.open_by_key(SHEET_ID)
        
        claude_sheet = sheet.worksheet('Claude Tasks')
        records = claude_sheet.get_all_records()
        
        # Find CT-028
        ct028_found = False
        for record in records:
            if record.get('Task ID') == 'CT-028':
                ct028_found = True
                print("✅ Found CT-028:")
                print(f"   Instance: {record.get('Instance')}")
                print(f"   Task Type: {record.get('Task Type')}")
                print(f"   Priority: {record.get('Priority')}")
                print(f"   Status: {record.get('Status')}")
                print(f"   Description: {record.get('Description')}")
                print(f"   Expected Output: {record.get('Expected Output')}")
                print(f"   Dependencies: {record.get('Dependencies')}")
                print(f"   Date Added: {record.get('Date Added')}")
                break
        
        if not ct028_found:
            print("❌ CT-028 not found in Claude Tasks sheet")
            
            # Find highest task ID
            task_ids = []
            for record in records:
                task_id = record.get('Task ID', '')
                if task_id.startswith('CT-'):
                    try:
                        num = int(task_id.split('-')[1])
                        task_ids.append(num)
                    except:
                        pass
            
            if task_ids:
                highest = max(task_ids)
                print(f"\n📊 Current highest task ID: CT-{highest:03d}")
                print(f"   Next task would be: CT-{highest+1:03d}")
                
                # Show last few tasks
                print("\n📋 Recent tasks:")
                recent_tasks = sorted([r for r in records if r.get('Task ID', '').startswith('CT-')], 
                                    key=lambda x: x.get('Task ID'), reverse=True)[:5]
                for task in recent_tasks:
                    print(f"   {task['Task ID']}: {task['Description'][:60]}...")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    check_ct028()