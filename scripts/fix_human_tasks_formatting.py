#!/usr/bin/env python3
"""
Fix Human Tasks formatting to match existing format and renumber with HT-001, HT-002, etc.
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

def fix_human_tasks_formatting():
    """Fix Human Tasks sheet formatting to match existing format"""
    
    # Configuration
    SPREADSHEET_ID = "1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do"
    CREDENTIALS_FILE = "/home/server/google-sheets-credentials.json"
    
    print("🔧 Fixing Human Tasks Sheet Formatting")
    print("=" * 40)
    
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
        
        # Read current Human Tasks sheet
        range_name = 'Human Tasks!A:Z'
        result = sheet.values().get(
            spreadsheetId=SPREADSHEET_ID,
            range=range_name
        ).execute()
        
        values = result.get('values', [])
        
        if not values:
            print("❌ No data found in Human Tasks sheet")
            return False
        
        print(f"📊 Found {len(values)} rows in Human Tasks sheet")
        
        # Analyze existing format
        print("\n🔍 Analyzing existing format...")
        for i, row in enumerate(values[:5]):  # Check first 5 rows
            print(f"Row {i+1}: {len(row)} columns - {row[:3] if len(row) >= 3 else row}")
        
        # Identify the original tasks vs new additions
        original_tasks = []
        new_tasks = []
        section_headers = []
        
        for i, row in enumerate(values):
            if len(row) == 0:
                continue
            elif "===" in str(row[0]):  # Section header
                section_headers.append({'row': i+1, 'content': row})
            elif str(row[0]).startswith('HT-') and len(row) >= 3:  # New task format
                new_tasks.append({'row': i+1, 'data': row})
            elif len(row) >= 3 and not str(row[0]).startswith('Task') and not "===" in str(row[0]):  # Original task
                original_tasks.append({'row': i+1, 'data': row})
        
        print(f"\n📊 Analysis Results:")
        print(f"Original tasks: {len(original_tasks)}")
        print(f"New tasks: {len(new_tasks)}")
        print(f"Section headers: {len(section_headers)}")
        
        # Show original format example
        if original_tasks:
            print(f"\n📋 Original format example:")
            example = original_tasks[0]['data']
            print(f"Columns: {len(example)}")
            for j, col in enumerate(example[:6]):  # First 6 columns
                print(f"  Col {j+1}: {col}")
        
        # Create properly formatted task list
        print(f"\n🔧 Creating properly formatted task list...")
        
        # Combine all tasks (original + new) and reformat
        all_tasks = []
        
        # Add original tasks
        for task in original_tasks:
            all_tasks.append(task['data'])
        
        # Add new tasks from our recent additions, converting to original format
        new_task_data = [
            ["Update Google Sheets - Mark Claude Tasks Complete", "High", "2 min", "Ready", "Mark CT-013, CT-014, CT-016, CT-021 as COMPLETED in Claude Tasks sheet", "None"],
            ["Create Discord Webhooks", "High", "5 min", "Ready", "Create webhook URLs for #alerts, #logs, #general, #critical channels", "Discord server access"],
            ["Configure n8n Google Sheets Credentials", "High", "5 min", "Ready", "Upload service account JSON to n8n credentials", "n8n access"],
            ["Deploy Discord Integration", "High", "10 min", "Ready", "Update webhook URLs in scripts and test MQTT→Discord flow", "Discord webhooks created"],
            ["Test MQTT→Google Sheets Flow", "High", "10 min", "Ready", "Activate n8n workflow and test MQTT logging to Sheets", "Google Sheets credentials configured"],
            ["Get Formbricks API Key", "Medium", "10 min", "Ready", "Login to Formbricks, create API key, update test script", "Formbricks account access"],
            ["Install Ignition Scripts", "Medium", "30 min", "Ready", "Import 3 Python scripts to Ignition project library", "Ignition Designer access"],
            ["Configure WhatsApp Business API", "Medium", "30 min", "Ready", "Set up WhatsApp Business API or use webhook.site for testing", "Meta Developer account"],
            ["Complete End-to-End Integration Test", "High", "20 min", "Pending", "Test full pipeline: Ignition→MQTT→n8n→Discord+Sheets", "All integrations configured"],
            ["Sync with Mac Claude on Discord Bot", "Medium", "15 min", "Pending", "Coordinate Discord bot vs webhook approach", "Mac Claude availability"],
            ["Update IIOT Master Sheet Status", "Low", "10 min", "Ready", "Update System Components Status with integration progress", "None"]
        ]
        
        # Add new tasks to the list
        for task_data in new_task_data:
            all_tasks.append(task_data)
        
        # Create header row based on original format
        if original_tasks and len(original_tasks[0]['data']) >= 6:
            # Use original format
            headers = ["Task", "Priority", "Time Required", "Status", "Description", "Dependencies"]
        else:
            # Default format
            headers = ["Task", "Priority", "Time Required", "Status", "Description", "Dependencies"]
        
        # Renumber all tasks with HT-001, HT-002, etc.
        formatted_tasks = [headers]  # Start with headers
        
        for i, task in enumerate(all_tasks, 1):
            # Ensure task has at least 6 columns
            while len(task) < 6:
                task.append("")
            
            # Create properly formatted row with HT-ID
            formatted_row = [
                f"HT-{i:03d}",  # Task ID: HT-001, HT-002, etc.
                task[0],        # Task name
                task[1],        # Priority
                task[2],        # Time required
                task[3],        # Status
                task[4],        # Description
                task[5]         # Dependencies
            ]
            formatted_tasks.append(formatted_row)
        
        # Clear the sheet and write the properly formatted data
        print(f"\n📝 Updating sheet with {len(formatted_tasks)-1} tasks...")
        
        # Clear existing content
        clear_range = 'Human Tasks!A:Z'
        sheet.values().clear(
            spreadsheetId=SPREADSHEET_ID,
            range=clear_range
        ).execute()
        
        # Write new formatted data
        body = {
            'values': formatted_tasks
        }
        
        result = sheet.values().update(
            spreadsheetId=SPREADSHEET_ID,
            range='Human Tasks!A1',
            valueInputOption='RAW',
            body=body
        ).execute()
        
        print(f"✅ Human Tasks sheet reformatted successfully!")
        print(f"📊 {result.get('updatedCells')} cells updated")
        print(f"🎯 Tasks renumbered: HT-001 through HT-{len(formatted_tasks)-1:03d}")
        
        # Show summary
        print(f"\n📋 Updated Format:")
        print("ID | Task | Priority | Time | Status | Description | Dependencies")
        print("-" * 80)
        for i, task in enumerate(formatted_tasks[1:6], 1):  # Show first 5 tasks
            task_short = [str(col)[:15] + "..." if len(str(col)) > 15 else str(col) for col in task]
            print(" | ".join(task_short))
        
        if len(formatted_tasks) > 6:
            print(f"... and {len(formatted_tasks)-6} more tasks")
        
        return True
        
    except HttpError as error:
        print(f"❌ Google Sheets API error: {error}")
        return False
    except Exception as error:
        print(f"❌ Unexpected error: {error}")
        return False

if __name__ == "__main__":
    success = fix_human_tasks_formatting()
    if success:
        print("\n🎉 Human Tasks sheet formatting fixed!")
        print("All tasks now have proper HT-XXX IDs and consistent formatting.")
    else:
        print("\n📝 Please manually fix Human Tasks sheet formatting")
        sys.exit(1)