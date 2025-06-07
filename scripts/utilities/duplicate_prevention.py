#!/usr/bin/env python3
"""
Duplicate prevention utility for Google Sheets Claude Tasks
ALWAYS call check_task_exists() before adding new tasks!
"""

from googleapiclient.discovery import build
from google.oauth2 import service_account

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'credentials/iot-stack-credentials.json'
SPREADSHEET_ID = '1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do'

def get_existing_task_ids():
    """Get all existing task IDs from Google Sheets"""
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=credentials)
    sheet = service.spreadsheets()
    
    result = sheet.values().get(
        spreadsheetId=SPREADSHEET_ID,
        range="'Claude Tasks'!A:A"
    ).execute()
    
    values = result.get('values', [])
    task_ids = set()
    
    for row in values[1:]:  # Skip header
        if len(row) > 0 and row[0]:
            task_ids.add(row[0])
    
    return task_ids

def check_task_exists(task_id):
    """Check if a task ID already exists"""
    existing_ids = get_existing_task_ids()
    exists = task_id in existing_ids
    
    if exists:
        print(f"⚠️  WARNING: Task {task_id} already exists! Not adding duplicate.")
    else:
        print(f"✅ Task {task_id} is new - safe to add")
    
    return exists

def get_next_task_id():
    """Get the next available CT-XXX task ID"""
    existing_ids = get_existing_task_ids()
    
    # Extract numbers from CT-XXX format
    numbers = []
    for task_id in existing_ids:
        if task_id.startswith('CT-'):
            try:
                num = int(task_id[3:])
                numbers.append(num)
            except ValueError:
                continue
    
    if numbers:
        next_num = max(numbers) + 1
    else:
        next_num = 1
    
    next_id = f"CT-{next_num:03d}"
    print(f"📝 Next available task ID: {next_id}")
    return next_id

if __name__ == "__main__":
    print("🔍 Duplicate Prevention Utility")
    print("==============================")
    
    existing = get_existing_task_ids()
    print(f"📊 Found {len(existing)} existing tasks")
    
    next_id = get_next_task_id()
    print(f"🆕 Next task ID should be: {next_id}")
