#!/usr/bin/env python3
"""
Add Server Claude agent creation tasks to Claude Tasks sheet
"""

from googleapiclient.discovery import build
from google.oauth2 import service_account
from datetime import datetime
import os

# Configuration
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'credentials/iot-stack-credentials.json'
SPREADSHEET_ID = '1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do'
SHEET_NAME = 'Claude Tasks'

def get_sheets_service():
    """Initialize Google Sheets service"""
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=credentials)
    return service.spreadsheets()

def get_next_task_id(sheet):
    """Get the next available task ID"""
    try:
        result = sheet.values().get(
            spreadsheetId=SPREADSHEET_ID,
            range=f'{SHEET_NAME}!A:A'
        ).execute()
        
        values = result.get('values', [])
        
        # Find the highest task ID
        max_id = 0
        for row in values[1:]:  # Skip header
            if row and row[0].startswith('CT-'):
                try:
                    task_num = int(row[0].split('-')[1])
                    max_id = max(max_id, task_num)
                except:
                    pass
        
        return f"CT-{str(max_id + 1).zfill(3)}"
        
    except Exception as e:
        print(f"Error getting task ID: {e}")
        return "CT-029"  # Fallback ID

def add_server_agent_tasks():
    """Add agent creation tasks for Server Claude"""
    try:
        sheet = get_sheets_service()
        
        # Get next task ID
        next_id = get_next_task_id(sheet)
        print(f"📝 Starting with task ID: {next_id}")
        
        # Get current ID number to increment
        current_num = int(next_id.split('-')[1])
        
        # Define the new agent tasks
        new_tasks = [
            {
                'id': f"CT-{str(current_num).zfill(3)}",
                'instance': 'Server Claude',
                'task_type': 'Agent Creation',
                'priority': 'High',
                'status': 'Not Started',
                'description': 'Create Docker Management Agent for Server Claude - to handle container operations, health checks, and automated restarts',
                'expected_output': 'Python agent script that can list, start, stop, and monitor Docker containers with proper error handling',
                'dependencies': '-',
                'date_added': datetime.now().strftime('%Y-%m-%d %H:%M'),
                'completed': ''
            },
            {
                'id': f"CT-{str(current_num + 1).zfill(3)}",
                'instance': 'Server Claude',
                'task_type': 'Agent Creation',
                'priority': 'High',
                'status': 'Not Started',
                'description': 'Create SystemD Service Agent for Server Claude - for managing persistent services, auto-start configuration, and service monitoring',
                'expected_output': 'Python agent that can create, enable, disable, and monitor systemd services with proper unit file generation',
                'dependencies': '-',
                'date_added': datetime.now().strftime('%Y-%m-%d %H:%M'),
                'completed': ''
            },
            {
                'id': f"CT-{str(current_num + 2).zfill(3)}",
                'instance': 'Server Claude',
                'task_type': 'Agent Creation',
                'priority': 'Medium',
                'status': 'Not Started',
                'description': 'Create Log Analysis Agent for Server Claude - for monitoring and troubleshooting system logs, Docker logs, and application logs',
                'expected_output': 'Python agent that can parse, filter, and alert on log patterns across multiple log sources',
                'dependencies': f"CT-{str(current_num).zfill(3)}",
                'date_added': datetime.now().strftime('%Y-%m-%d %H:%M'),
                'completed': ''
            },
            {
                'id': f"CT-{str(current_num + 3).zfill(3)}",
                'instance': 'Server Claude',
                'task_type': 'Agent Creation',
                'priority': 'Medium',
                'status': 'Not Started',
                'description': 'Create Backup & Recovery Agent for Server Claude - for automated backups of configurations, databases, and critical data',
                'expected_output': 'Python agent with scheduled backup tasks, retention policies, and recovery procedures',
                'dependencies': f"CT-{str(current_num).zfill(3)}",
                'date_added': datetime.now().strftime('%Y-%m-%d %H:%M'),
                'completed': ''
            },
            {
                'id': f"CT-{str(current_num + 4).zfill(3)}",
                'instance': 'Server Claude',
                'task_type': 'Agent Creation',
                'priority': 'Low',
                'status': 'Not Started',
                'description': 'Create Performance Monitoring Agent for Server Claude - for resource tracking, performance metrics, and capacity planning',
                'expected_output': 'Python agent that collects CPU, memory, disk, and network metrics with historical tracking',
                'dependencies': f"CT-{str(current_num + 1).zfill(3)}",
                'date_added': datetime.now().strftime('%Y-%m-%d %H:%M'),
                'completed': ''
            }
        ]
        
        # Prepare batch update
        rows_to_add = []
        for task in new_tasks:
            row = [
                task['id'],
                task['instance'],
                task['task_type'],
                task['priority'],
                task['status'],
                task['description'],
                task['expected_output'],
                task['dependencies'],
                task['date_added'],
                task['completed']
            ]
            rows_to_add.append(row)
        
        # Add all tasks at once
        result = sheet.values().append(
            spreadsheetId=SPREADSHEET_ID,
            range=f'{SHEET_NAME}!A:J',
            valueInputOption='USER_ENTERED',
            body={'values': rows_to_add}
        ).execute()
        
        print(f"✅ Successfully added {len(new_tasks)} agent creation tasks!")
        print("\n📋 New tasks added:")
        for task in new_tasks:
            print(f"   {task['id']}: {task['description'][:60]}...")
        
        print("\n🎯 These agents will help Server Claude with:")
        print("   • Docker container management and health monitoring")
        print("   • SystemD service configuration and persistence")
        print("   • Log analysis and troubleshooting")
        print("   • Automated backups and recovery")
        print("   • Performance monitoring and resource tracking")
        
    except Exception as e:
        print(f"❌ Error adding tasks: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🚀 Adding Server Claude Agent Creation Tasks")
    print("="*50)
    add_server_agent_tasks()