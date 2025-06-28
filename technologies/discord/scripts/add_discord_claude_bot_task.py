#!/usr/bin/env python3
"""
Add Discord Claude Bot improvement task to Google Sheets Claude Tasks
"""

import sys
import os
sys.path.append('scripts/utilities')

from googleapiclient.discovery import build
from google.oauth2 import service_account
from duplicate_prevention import check_task_exists, get_next_task_id

# Configuration
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'credentials/iot-stack-credentials.json'
SPREADSHEET_ID = '1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do'

def get_sheets_service():
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=credentials)
    return service.spreadsheets()

def add_discord_claude_bot_task():
    try:
        # Get next available task ID
        task_id = get_next_task_id()
        
        # Check if task already exists (safety check)
        if check_task_exists(task_id):
            print(f"⚠️  Task {task_id} already exists - using manual ID")
            task_id = "CT-046"
            
        sheet = get_sheets_service()
        sheet_name = 'Claude Tasks'
        
        # Get current data to find next row
        result = sheet.values().get(
            spreadsheetId=SPREADSHEET_ID,
            range=f"'{sheet_name}'!A:H"
        ).execute()
        
        values = result.get('values', [])
        next_row = len(values) + 1
        
        # New task for Discord Claude Bot enhancement
        new_task = [
            task_id,
            'Mac Claude', 
            'Discord Claude Bot Enhancement',
            'High',
            'Pending',
            'Create Discord bot for real-time Claude interaction with Industrial IoT project management',
            'Discord bot that allows status checking, task assignment, and terminal command execution',
            'CT-045'
        ]
        
        # Add the task
        range_to_update = f"'{sheet_name}'!A{next_row}:H{next_row}"
        
        result = sheet.values().update(
            spreadsheetId=SPREADSHEET_ID,
            range=range_to_update,
            valueInputOption='RAW',
            body={'values': [new_task]}
        ).execute()
        
        print(f'✅ Added {task_id}: Discord Claude Bot Enhancement')
        print(f'📊 Updated {result.get("updatedCells")} cells in Google Sheets')
        print(f'🔗 Task added at row {next_row}')
        
        # Print task details
        print(f'\n📋 TASK DETAILS:')
        print(f'Task ID: {task_id}')
        print(f'Title: Discord Claude Bot Enhancement')
        print(f'Priority: High')
        print(f'Status: Pending')
        print(f'Description: Create Discord bot for real-time Claude interaction with Industrial IoT project management')
        print(f'Expected Output: Discord bot that allows status checking, task assignment, and terminal command execution')
        print(f'Dependencies: CT-045')
        
        print(f'\n🎯 DESIRED FEATURES:')
        print(f'• !status - Check what Claude is currently working on')
        print(f'• !task <message> - Assign new task to Claude for terminal execution')
        print(f'• Real-time updates on Claude Tasks progress')
        print(f'• Integration with Google Sheets Claude Tasks')
        print(f'• Node-RED, n8n, GitHub status monitoring')
        print(f'• Industrial IoT project context awareness')
        
        return True
        
    except Exception as e:
        print(f'❌ Error adding Discord bot task: {e}')
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    # Change to project root directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(os.path.dirname(script_dir))
    
    print('🤖 Adding Discord Claude Bot enhancement task to Claude Tasks...')
    print('📱 This will enable real-time Claude interaction via Discord!')
    
    success = add_discord_claude_bot_task()
    
    if success:
        print('\n✅ Discord Claude Bot task added successfully!')
        print('🔗 View at: https://docs.google.com/spreadsheets/d/1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do/edit')
        print('\n💬 Soon you\'ll be able to chat with Claude via Discord about the Industrial IoT project!')
    else:
        print('\n❌ Failed to add Discord bot task')