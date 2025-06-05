#!/usr/bin/env python3
"""
Add human tasks to Google Sheets Human Tasks tab
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime

# Add the scripts directory to Python path for imports
script_dir = Path(__file__).parent
sys.path.append(str(script_dir))

try:
    from google.oauth2.service_account import Credentials
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
except ImportError:
    print("❌ Google API libraries not installed")
    sys.exit(1)

def add_human_tasks_to_sheet():
    """Add generated human tasks to Google Sheets Human Tasks tab"""
    
    # Configuration
    SPREADSHEET_ID = "1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do"
    CREDENTIALS_FILE = "/home/server/google-sheets-credentials.json"
    
    print("📋 Adding Human Tasks to Google Sheets")
    print("=" * 40)
    
    # Load generated tasks
    with open('/mnt/c/Users/LocalAccount/industrial-iot-stack/HUMAN_TASKS_UPDATE.json', 'r') as f:
        task_data = json.load(f)
    
    try:
        # Load credentials
        creds = Credentials.from_service_account_file(
            CREDENTIALS_FILE,
            scopes=['https://www.googleapis.com/auth/spreadsheets']
        )
        
        # Build service
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()
        
        print("✅ Connected to Google Sheets API")
        
        # Prepare rows for Human Tasks sheet
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        # Header row
        headers = [
            "Task ID", "Task", "Priority", "Time Required", "Status", 
            "Dependencies", "Category", "Added Date", "Notes"
        ]
        
        # Prepare task rows
        task_rows = [headers]
        task_id_counter = 1
        
        # Add immediate 5-min tasks
        for task in task_data["tasks"]["immediate_5min"]:
            row = [
                f"HT-{task_id_counter:03d}",
                task["task"],
                task["priority"],
                task["time"],
                task["status"],
                task["dependencies"] or "None",
                "Immediate (5min)",
                timestamp,
                task["notes"]
            ]
            task_rows.append(row)
            task_id_counter += 1
        
        # Add immediate 10-min tasks
        for task in task_data["tasks"]["immediate_10min"]:
            row = [
                f"HT-{task_id_counter:03d}",
                task["task"],
                task["priority"],
                task["time"],
                task["status"],
                task["dependencies"] or "None",
                "Quick Win (10min)",
                timestamp,
                task["notes"]
            ]
            task_rows.append(row)
            task_id_counter += 1
        
        # Add next session tasks
        for task in task_data["tasks"]["next_session_30min"]:
            row = [
                f"HT-{task_id_counter:03d}",
                task["task"],
                task["priority"],
                task["time"],
                task["status"],
                task["dependencies"] or "None",
                "Next Session",
                timestamp,
                task["notes"]
            ]
            task_rows.append(row)
            task_id_counter += 1
        
        # Add coordination tasks
        for task in task_data["tasks"]["coordination_required"]:
            row = [
                f"HT-{task_id_counter:03d}",
                task["task"],
                task["priority"],
                task["time"],
                task["status"],
                task["dependencies"] or "None",
                "Coordination",
                timestamp,
                task["notes"]
            ]
            task_rows.append(row)
            task_id_counter += 1
        
        # Get current Human Tasks sheet data to append
        try:
            range_name = 'Human Tasks!A:Z'
            result = sheet.values().get(
                spreadsheetId=SPREADSHEET_ID,
                range=range_name
            ).execute()
            
            existing_rows = result.get('values', [])
            existing_count = len(existing_rows)
            
            print(f"📊 Found {existing_count} existing rows in Human Tasks sheet")
            
            # Determine where to append new tasks
            if existing_count == 0:
                # Sheet is empty, add headers + tasks
                start_row = 1
                update_range = 'Human Tasks!A1'
                update_data = task_rows
            else:
                # Append after existing data
                start_row = existing_count + 2  # +2 for gap and header
                update_range = f'Human Tasks!A{start_row}'
                
                # Add a section header
                section_header = [
                    "", f"=== AUTONOMOUS WORK RESULTS - {timestamp} ===", "", "", "", "", "", "", ""
                ]
                update_data = [section_header] + task_rows
            
            # Update the sheet
            body = {
                'values': update_data
            }
            
            result = sheet.values().update(
                spreadsheetId=SPREADSHEET_ID,
                range=update_range,
                valueInputOption='RAW',
                body=body
            ).execute()
            
            print(f"✅ Added {len(task_rows)-1} human tasks to Google Sheets")
            print(f"📍 Updated range: {update_range}")
            print(f"📊 {result.get('updatedCells')} cells updated")
            
        except HttpError as e:
            if '404' in str(e):
                print("⚠️  Human Tasks sheet not found, creating summary instead")
                
                # Create summary for manual addition
                print("\n📋 MANUAL ADDITION SUMMARY:")
                print("=" * 35)
                print("Sheet: Human Tasks")
                print(f"Tasks to add: {len(task_rows)-1}")
                print(f"Generated: {timestamp}")
                print("")
                
                for i, row in enumerate(task_rows):
                    if i == 0:  # Header
                        print(" | ".join(row))
                        print("-" * 80)
                    else:  # Task rows
                        print(f"{row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]}")
                
                return True
            else:
                raise e
        
        print("\n🎯 Human Tasks Summary:")
        print("=" * 25)
        print(f"• Total tasks added: {len(task_rows)-1}")
        print(f"• High priority: {len([r for r in task_rows[1:] if r[2] == 'High'])}")
        print(f"• Immediate actions: {len(task_data['tasks']['immediate_5min']) + len(task_data['tasks']['immediate_10min'])}")
        print(f"• Estimated time: 45 minutes for immediate tasks")
        
        print("\n🚀 Ready for Action:")
        print("1. Mark completed Claude tasks as DONE")
        print("2. Create Discord webhooks (5 min)")
        print("3. Configure Google Sheets credentials (5 min)")
        print("4. Deploy integrations and test!")
        
        return True
        
    except HttpError as error:
        print(f"❌ Google Sheets API error: {error}")
        return False
    except Exception as error:
        print(f"❌ Unexpected error: {error}")
        return False

if __name__ == "__main__":
    success = add_human_tasks_to_sheet()
    if not success:
        print("\n📝 Please manually add human tasks to Google Sheets")
        sys.exit(1)