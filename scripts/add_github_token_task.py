#!/usr/bin/env python3
"""
Add GitHub token documentation task to Claude Tasks
"""

from googleapiclient.discovery import build
from google.oauth2 import service_account
from datetime import datetime
import os

# Configuration
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'credentials/iot-stack-credentials.json'
SPREADSHEET_ID = '1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do'

def get_sheets_service():
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=credentials)
    return service.spreadsheets()

def add_github_token_task():
    try:
        sheet = get_sheets_service()
        
        # Use 'Claude Tasks' as sheet name
        sheet_name = 'Claude Tasks'
        
        # Get current data to find next row
        result = sheet.values().get(
            spreadsheetId=SPREADSHEET_ID,
            range=f"'{sheet_name}'!A:H"
        ).execute()
        
        values = result.get('values', [])
        next_row = len(values) + 1
        
        # New task for GitHub token documentation
        new_task = [
            'CT-045',
            'Mac Claude', 
            'GitHub Tokens Documentation',
            'Medium',
            'Complete',
            'Add comprehensive GitHub Secrets documentation to credentials and .claude folder',
            'Complete setup guide for ANTHROPIC_API_KEY, CLAUDE_MAX_SESSION_KEY, testing commands',
            'CT-041'
        ]
        
        # Add the task
        range_to_update = f"'{sheet_name}'!A{next_row}:H{next_row}"
        
        result = sheet.values().update(
            spreadsheetId=SPREADSHEET_ID,
            range=range_to_update,
            valueInputOption='RAW',
            body={'values': [new_task]}
        ).execute()
        
        print(f'✅ Added CT-045: GitHub Tokens Documentation')
        print(f'📊 Updated {result.get("updatedCells")} cells in Google Sheets')
        print(f'🔗 Task added at row {next_row}')
        
        return True
        
    except Exception as e:
        print(f'❌ Error adding task: {e}')
        return False

if __name__ == '__main__':
    # Change to project root directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(os.path.dirname(script_dir))
    
    print('🚀 Adding GitHub token documentation task to Claude Tasks...')
    success = add_github_token_task()
    if success:
        print('\n✅ Google Sheets Claude Tasks updated successfully!')
        print('🔗 View at: https://docs.google.com/spreadsheets/d/1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do/edit')
    else:
        print('\n❌ Failed to update Google Sheets')