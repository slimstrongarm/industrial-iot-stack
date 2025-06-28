#!/usr/bin/env python3
"""
Check current Mac Claude tasks from Google Sheets
"""

import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

def check_tasks():
    try:
        # Setup credentials
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        credentials = Credentials.from_service_account_file(
            'credentials/iot-stack-credentials.json', 
            scopes=scope
        )
        
        # Connect to Google Sheets
        gc = gspread.authorize(credentials)
        sheet = gc.open_by_key('1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do')
        worksheet = sheet.worksheet('Claude Tasks')
        
        # Get all values to avoid header issues
        all_values = worksheet.get_all_values()
        
        print("📊 Mac Claude Task Status")
        print("=" * 60)
        print(f"Total tasks: {len(all_values) - 1}")
        
        # Find Mac Claude tasks
        mac_tasks = []
        pending_tasks = []
        in_progress_tasks = []
        
        for i, row in enumerate(all_values[1:], 1):  # Skip header
            if len(row) > 5:
                task_id = row[0]
                assigned = row[1]
                task_type = row[2]
                priority = row[3]
                status = row[4]
                description = row[5]
                
                if 'Mac Claude' in assigned:
                    task_info = {
                        'id': task_id,
                        'type': task_type,
                        'priority': priority,
                        'status': status,
                        'description': description[:80]
                    }
                    mac_tasks.append(task_info)
                    
                    if status == 'Pending':
                        pending_tasks.append(task_info)
                    elif status == 'In Progress':
                        in_progress_tasks.append(task_info)
        
        # Show results
        print(f"\n🎯 Mac Claude Tasks: {len(mac_tasks)} total")
        
        if in_progress_tasks:
            print(f"\n⚡ IN PROGRESS ({len(in_progress_tasks)}):")
            for task in in_progress_tasks:
                print(f"   {task['id']}: {task['description']}")
        
        if pending_tasks:
            print(f"\n📋 PENDING ({len(pending_tasks)}):")
            for task in pending_tasks[:5]:  # Show first 5
                print(f"   {task['id']} [{task['priority']}]: {task['description']}")
            if len(pending_tasks) > 5:
                print(f"   ... and {len(pending_tasks) - 5} more")
        
        # Check Discord bot status
        print(f"\n🤖 Discord Bot Status:")
        for i, row in enumerate(all_values[1:], 1):
            if len(row) > 0 and row[0] == 'CT-099':
                print(f"   CT-099: {row[4]} (Assigned: {row[1]})")
                print(f"   Task: {row[5][:60]}...")
                break
        
        # Show next task ID
        print(f"\n🆔 Next task ID: CT-{len(all_values):03d}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    check_tasks()