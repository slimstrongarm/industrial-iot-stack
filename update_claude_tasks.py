#!/usr/bin/env python3
"""
Script to update Claude Tasks sheet with task status changes
"""

import json
from datetime import datetime
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

# Google Sheets configuration
SPREADSHEET_ID = "1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do"
CREDENTIALS_PATH = "/home/server/google-sheets-credentials.json"
SHEET_NAME = "Claude Tasks"

# Today's date for completion dates
TODAY = datetime.now().strftime("%Y-%m-%d")

def get_sheets_service():
    """Initialize and return Google Sheets service"""
    credentials = Credentials.from_service_account_file(
        CREDENTIALS_PATH,
        scopes=['https://www.googleapis.com/auth/spreadsheets']
    )
    service = build('sheets', 'v4', credentials=credentials)
    return service

def get_sheet_data(service):
    """Get current sheet data to find task rows"""
    sheet = service.spreadsheets()
    result = sheet.values().get(
        spreadsheetId=SPREADSHEET_ID,
        range=f"{SHEET_NAME}!A:Z"
    ).execute()
    return result.get('values', [])

def find_task_row(data, task_id):
    """Find the row number for a specific task ID"""
    for i, row in enumerate(data):
        if len(row) > 0 and row[0] == task_id:
            return i + 1  # Google Sheets uses 1-based indexing
    return None

def update_task_status(service, task_id, status, completion_date=None):
    """Update a task's status and completion date"""
    data = get_sheet_data(service)
    row_num = find_task_row(data, task_id)
    
    if row_num is None:
        print(f"Task {task_id} not found in sheet")
        return False
    
    # Assuming columns: A=Task ID, B=Description, C=Status, D=Priority, E=Completion Date
    updates = []
    
    # Update status (column C)
    updates.append({
        'range': f"{SHEET_NAME}!C{row_num}",
        'values': [[status]]
    })
    
    # Update completion date if provided (column E)
    if completion_date:
        updates.append({
            'range': f"{SHEET_NAME}!E{row_num}",
            'values': [[completion_date]]
        })
    
    # Batch update
    body = {
        'valueInputOption': 'RAW',
        'data': updates
    }
    
    try:
        result = service.spreadsheets().values().batchUpdate(
            spreadsheetId=SPREADSHEET_ID,
            body=body
        ).execute()
        print(f"Updated {task_id}: {status}" + (f" (completed: {completion_date})" if completion_date else ""))
        return True
    except Exception as e:
        print(f"Error updating {task_id}: {e}")
        return False

def main():
    """Main function to update all task statuses"""
    print("Updating Claude Tasks sheet...")
    
    service = get_sheets_service()
    
    # Task updates based on session context
    updates = [
        # COMPLETED TASKS
        ("CT-007", "COMPLETED", TODAY),  # n8n Workflow Import
        ("CT-013", "COMPLETED", TODAY),  # n8n API Configuration
        ("CT-014", "COMPLETED", TODAY),  # API Testing
        ("CT-016", "COMPLETED", TODAY),  # Ignition Scripts
        ("CT-021", "COMPLETED", TODAY),  # Discord Setup
        
        # IN PROGRESS TASKS
        ("CT-008", "IN PROGRESS", None),  # Integration Test
        ("CT-022", "IN PROGRESS", None),  # Discord Integration
        
        # READY/PENDING TASKS
        ("CT-019", "READY", None),  # Formbricks API
    ]
    
    successful_updates = 0
    total_updates = len(updates)
    
    for task_id, status, completion_date in updates:
        if update_task_status(service, task_id, status, completion_date):
            successful_updates += 1
    
    print(f"\nUpdate Summary:")
    print(f"Successfully updated: {successful_updates}/{total_updates} tasks")
    print(f"Completion date set to: {TODAY} for completed tasks")
    
    if successful_updates == total_updates:
        print("All task statuses updated successfully!")
    else:
        print(f"Some updates failed. Please check the sheet manually.")

if __name__ == "__main__":
    main()