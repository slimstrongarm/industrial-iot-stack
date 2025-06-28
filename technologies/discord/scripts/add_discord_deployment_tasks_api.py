#!/usr/bin/env python3
"""
Add Discord Deployment Tasks CT-051 through CT-055 to Google Sheets
Uses existing Google Sheets API credentials and setup
"""

from googleapiclient.discovery import build
from google.oauth2 import service_account
import json
from datetime import datetime
import os

# Configuration from existing setup
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'credentials/iot-stack-credentials.json'
SPREADSHEET_ID = '1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do'

def add_discord_deployment_tasks():
    """Add Discord deployment tasks CT-051 through CT-055 to Claude Tasks sheet"""
    
    try:
        # Load credentials using existing setup
        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        
        service = build('sheets', 'v4', credentials=credentials)
        sheet = service.spreadsheets()
        
        # Get existing data to find next row
        result = sheet.values().get(
            spreadsheetId=SPREADSHEET_ID,
            range='Claude Tasks!A:J'
        ).execute()
        
        values = result.get('values', [])
        last_row = len(values) if values else 1
        next_row = last_row + 1
        
        print(f"📊 Found {len(values)} existing rows, adding tasks at row {next_row}")
        
        # Discord deployment tasks matching exact sheet format:
        # Task ID, Instance, Task Type, Priority, Status, Description, Expected Output, Dependencies, Date Added, Completed
        deployment_tasks = [
            [
                'CT-051',
                'Server Claude', 
                'Discord Docker Deploy',
                'High',
                'Pending',
                'Deploy Discord bot using Docker Compose on server infrastructure. Follow SERVER_CLAUDE_DEPLOYMENT_PACKAGE.md instructions for containerized deployment.',
                'Discord bot running as persistent Docker service with auto-restart capabilities',
                'Docker and docker-compose installed on server',
                datetime.now().strftime('%Y-%m-%d %H:%M'),
                ''
            ],
            [
                'CT-052',
                'Server Claude',
                'Task Worker Deploy', 
                'High',
                'Pending',
                'Deploy the Mac Claude task worker as Docker container alongside Discord bot. Ensure proper networking and credential access.',
                'Task worker container running and processing Google Sheets tasks automatically',
                'CT-051 completed (Discord bot deployed)',
                datetime.now().strftime('%Y-%m-%d %H:%M'),
                ''
            ],
            [
                'CT-053',
                'Server Claude',
                'Health Monitoring',
                'Medium',
                'Pending', 
                'Set up health monitoring for Discord bot and task worker containers. Implement auto-restart and alerting capabilities.',
                'Health monitor running and automatically restarting failed services',
                'CT-051, CT-052 completed',
                datetime.now().strftime('%Y-%m-%d %H:%M'),
                ''
            ],
            [
                'CT-054',
                'Server Claude',
                'End-to-End Testing',
                'High',
                'Pending',
                'Test complete workflow: Discord command → Google Sheets task → automated processing → completion. Verify 24/7 persistent operation.',
                'Complete workflow tested and verified working continuously without manual intervention',
                'CT-051, CT-052, CT-053 completed',
                datetime.now().strftime('%Y-%m-%d %H:%M'),
                ''
            ],
            [
                'CT-055',
                'Mac Claude',
                'Documentation Update',
                'Medium',
                'Pending',
                'Update INDEX.md and .claude documentation to reflect successful persistent deployment capabilities and workflow automation.',
                'Documentation updated with deployment procedures and automation workflows',
                'CT-054 completed (testing successful)',
                datetime.now().strftime('%Y-%m-%d %H:%M'),
                ''
            ]
        ]
        
        # Add tasks to sheet
        range_name = f'Claude Tasks!A{next_row}:J{next_row + len(deployment_tasks) - 1}'
        
        body = {
            'values': deployment_tasks
        }
        
        result = sheet.values().update(
            spreadsheetId=SPREADSHEET_ID,
            range=range_name,
            valueInputOption='USER_ENTERED',
            body=body
        ).execute()
        
        print(f"✅ Successfully added {len(deployment_tasks)} Discord deployment tasks!")
        print(f"📋 Added tasks CT-051 through CT-055 to Google Sheets")
        print(f"🔗 View at: https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}")
        
        # Show what was added
        print("\n📋 Tasks Added:")
        for task in deployment_tasks:
            task_id = task[0]
            instance = task[1]
            task_type = task[2] 
            priority = task[3]
            description = task[5][:60] + "..." if len(task[5]) > 60 else task[5]
            print(f"  {task_id} ({instance}): {task_type} - {priority} Priority")
            print(f"    → {description}")
        
        print(f"\n🚀 Server Claude now has {len(deployment_tasks)} new high-priority deployment tasks!")
        print("📱 These tasks will enable 24/7 Discord bot automation without terminal sessions")
        
        return True
        
    except FileNotFoundError:
        print(f"❌ Credentials file not found: {SERVICE_ACCOUNT_FILE}")
        print("Please ensure the credentials file exists at the correct location.")
        return False
    except Exception as e:
        print(f"❌ Error adding tasks to Google Sheets: {e}")
        return False

def verify_tasks_added():
    """Verify the tasks were successfully added"""
    try:
        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        
        service = build('sheets', 'v4', credentials=credentials)
        sheet = service.spreadsheets()
        
        # Check for CT-051 through CT-055
        result = sheet.values().get(
            spreadsheetId=SPREADSHEET_ID,
            range='Claude Tasks!A:J'
        ).execute()
        
        values = result.get('values', [])
        discord_tasks = []
        
        for row in values:
            if len(row) > 0 and row[0] in ['CT-051', 'CT-052', 'CT-053', 'CT-054', 'CT-055']:
                discord_tasks.append(row)
        
        if discord_tasks:
            print(f"\n✅ Verification: Found {len(discord_tasks)} Discord deployment tasks in sheet")
            for task in discord_tasks:
                task_id = task[0] if len(task) > 0 else 'N/A'
                instance = task[1] if len(task) > 1 else 'N/A' 
                status = task[4] if len(task) > 4 else 'N/A'
                print(f"  {task_id} assigned to {instance}: {status}")
            return True
        else:
            print("❌ Verification failed: No Discord deployment tasks found")
            return False
            
    except Exception as e:
        print(f"❌ Verification error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Adding Discord Deployment Tasks to Google Sheets Claude Tasks tab...")
    print("==================================================================")
    
    # Check if credentials file exists
    if not os.path.exists(SERVICE_ACCOUNT_FILE):
        print(f"❌ Credentials file not found at: {SERVICE_ACCOUNT_FILE}")
        print("Please ensure the file exists and try again.")
        exit(1)
    
    # Add the tasks
    success = add_discord_deployment_tasks()
    
    if success:
        print("\n🔍 Verifying tasks were added...")
        verify_tasks_added()
        print("\n🎉 Discord deployment tasks successfully added to Google Sheets!")
        print("Server Claude can now see CT-051 through CT-055 and begin deployment.")
    else:
        print("\n❌ Failed to add Discord deployment tasks")
        print("Please check credentials and try again.")