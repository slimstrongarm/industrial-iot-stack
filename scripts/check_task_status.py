#!/usr/bin/env python3
"""
Quick check of CT-049 status in Google Sheets
"""

import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

SPREADSHEET_ID = '1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do'
CREDENTIALS_PATH = '/Users/joshpayneair/Desktop/industrial-iot-stack/credentials/iot-stack-credentials.json'

# Setup Google Sheets
scope = ['https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive']
creds = Credentials.from_service_account_file(CREDENTIALS_PATH, scopes=scope)
gc = gspread.authorize(creds)
sheet = gc.open_by_key(SPREADSHEET_ID)
claude_tasks = sheet.worksheet('Claude Tasks')

# Get all values
all_rows = claude_tasks.get_all_values()

print(f"📊 Mac Claude Task Status Check - {datetime.now().strftime('%H:%M:%S')}")
print("=" * 60)

# Find CT-049
for row in all_rows:
    if row and row[0] == 'CT-049':
        print(f"Task ID: {row[0]}")
        print(f"Assigned To: {row[1]}")
        print(f"Title: {row[2]}")
        print(f"Priority: {row[3]}")
        print(f"Status: {row[4]} {'← Should change to In Progress then Complete' if row[4] == 'Pending' else ''}")
        if len(row) > 6 and row[6]:
            print(f"Output: {row[6]}")
        break

print("\n🤖 Mac Claude Worker should process this within 30 seconds")