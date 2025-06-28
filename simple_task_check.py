#!/usr/bin/env python3
import gspread
from google.oauth2.service_account import Credentials

CREDENTIALS_PATH = 'credentials/iot-stack-credentials.json'
SPREADSHEET_ID = '1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do'

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = Credentials.from_service_account_file(CREDENTIALS_PATH, scopes=scope)
client = gspread.authorize(creds)

sheet = client.open_by_key(SPREADSHEET_ID)
claude_tasks = sheet.worksheet('Claude Tasks')
all_values = claude_tasks.get_all_values()

print("CT-084 through CT-090 Status:")
print("=" * 50)

for row in all_values:
    if len(row) > 0:
        task_id = row[0]
        if any(f'CT-{i:03d}' == task_id for i in range(84, 91)):
            status = row[4] if len(row) > 4 else 'Unknown'
            title = row[2] if len(row) > 2 else 'No title'
            assigned = row[1] if len(row) > 1 else 'Unassigned'
            print(f"{task_id}: {status} | {assigned} | {title[:40]}")

print("\nRecent tasks for context:")
for row in all_values[-15:]:
    if len(row) > 0 and row[0].startswith('CT-'):
        print(f"{row[0]}: {row[4] if len(row) > 4 else 'Unknown'}")