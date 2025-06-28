#!/usr/bin/env python3
"""
Check what tasks are currently in the Claude Tasks sheet
"""

import gspread
from google.oauth2.service_account import Credentials
from pathlib import Path

def check_tasks():
    """Check current tasks in Claude Tasks sheet"""
    
    try:
        # Load credentials
        creds_path = Path(__file__).parent.parent / "credentials" / "iot-stack-credentials.json"
        
        # Setup Google Sheets client
        scope = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]
        
        creds = Credentials.from_service_account_file(creds_path, scopes=scope)
        client = gspread.authorize(creds)
        
        # Open the IoT Stack Progress Master spreadsheet
        spreadsheet = client.open("IoT Stack Progress Master")
        claude_tasks_sheet = spreadsheet.worksheet("Claude Tasks")
        
        print("✅ Connected to Claude Tasks sheet")
        
        # Get all data
        all_data = claude_tasks_sheet.get_all_records()
        
        print(f"\n📋 Found {len(all_data)} tasks in Claude Tasks sheet:")
        print("=" * 80)
        
        for i, row in enumerate(all_data, start=2):
            task_id = row.get('Task ID', 'No ID')
            description = row.get('Description', 'No description')
            status = row.get('Status', 'No status')
            assigned_to = row.get('Assigned To', 'Unassigned')
            
            print(f"Row {i:2d}: {task_id:8s} | {status:12s} | {assigned_to:12s} | {description[:50]}")
            
            # Look for CT-066 specifically
            if 'CT-066' in task_id or 'adk' in description.lower() or 'framework' in description.lower():
                print(f"     🎯 POTENTIAL MATCH for CT-066!")
            
            # Look for CT-067 specifically  
            if 'CT-067' in task_id or 'state persistence' in description.lower():
                print(f"     🎯 POTENTIAL MATCH for CT-067!")
        
        print("\n" + "=" * 80)
        
        # Check if there are any ADK-related tasks
        adk_tasks = [row for row in all_data if 'adk' in str(row).lower() or 'framework' in str(row).lower()]
        if adk_tasks:
            print(f"\n🔍 Found {len(adk_tasks)} ADK-related tasks:")
            for task in adk_tasks:
                print(f"   • {task.get('Task ID', 'No ID')}: {task.get('Description', 'No description')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error checking tasks: {e}")
        return False

if __name__ == "__main__":
    check_tasks()