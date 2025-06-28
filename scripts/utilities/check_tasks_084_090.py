#!/usr/bin/env python3
import gspread
from google.oauth2.service_account import Credentials

# Setup
CREDENTIALS_PATH = 'credentials/iot-stack-credentials.json'
SPREADSHEET_ID = '1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do'

# Authenticate
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = Credentials.from_service_account_file(CREDENTIALS_PATH, scopes=scope)
client = gspread.authorize(creds)

# Get data
sheet = client.open_by_key(SPREADSHEET_ID)
claude_tasks = sheet.worksheet('Claude Tasks')
all_values = claude_tasks.get_all_values()

print('CT-084 through CT-090 Status Summary:')
print('=' * 60)

for row in all_values:
    if len(row) > 0:
        task_id = row[0]
        if any(f'CT-{i:03d}' == task_id for i in range(84, 91)):
            assigned_to = row[1] if len(row) > 1 else 'N/A'
            title = row[2] if len(row) > 2 else 'N/A'
            priority = row[3] if len(row) > 3 else 'N/A'
            status = row[4] if len(row) > 4 else 'N/A'
            description = row[5] if len(row) > 5 else 'N/A'
            
            print(f'{task_id}: {status}')
            print(f'  Assigned: {assigned_to}')
            print(f'  Title: {title[:60]}...' if len(title) > 60 else f'  Title: {title}')
            print(f'  Priority: {priority}')
            print(f'  Desc: {description[:80]}...' if len(description) > 80 else f'  Desc: {description}')
            print()