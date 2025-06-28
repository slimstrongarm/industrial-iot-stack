#!/usr/bin/env python3
"""Check all pending Mac Claude tasks"""

import gspread
from google.oauth2.service_account import Credentials

SPREADSHEET_ID = '1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do'
CREDENTIALS_PATH = '/Users/joshpayneair/Desktop/industrial-iot-stack/credentials/iot-stack-credentials.json'

scope = ['https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive']
creds = Credentials.from_service_account_file(CREDENTIALS_PATH, scopes=scope)
gc = gspread.authorize(creds)
sheet = gc.open_by_key(SPREADSHEET_ID)
claude_tasks = sheet.worksheet('Claude Tasks')

all_rows = claude_tasks.get_all_values()

print("📊 All Pending Mac Claude Tasks:")
print("=" * 60)

pending_count = 0
for i, row in enumerate(all_rows[1:], 1):
    if len(row) > 4 and row[1] == 'Mac Claude' and row[4] == 'Pending':
        print(f"Row {i+1}: {row[0]} - {row[2]} (Status: {row[4]})")
        pending_count += 1

print(f"\nTotal pending Mac Claude tasks: {pending_count}")

# Find CT-049 specifically
for i, row in enumerate(all_rows):
    if row and row[0] == 'CT-049':
        print(f"\n🎯 CT-049 found at row {i+1}:")
        print(f"   Assigned to: {row[1]}")
        print(f"   Status: {row[4]}")
        break