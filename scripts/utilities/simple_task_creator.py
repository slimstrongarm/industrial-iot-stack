#!/usr/bin/env python3
"""Simple task creator for Server Claude Docker deployment"""

import gspread
from google.oauth2.service_account import Credentials

# Same setup as our working test
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = Credentials.from_service_account_file('/Users/joshpayneair/Desktop/industrial-iot-stack/credentials/iot-stack-credentials.json', scopes=scope)
client = gspread.authorize(creds)

SPREADSHEET_ID = '1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do'
sheet = client.open_by_key(SPREADSHEET_ID)
claude_tasks = sheet.worksheet('Claude Tasks')

print("Creating Server Claude Docker task...")

# Simple task creation
new_row = [
    "CT-099",
    "Server Claude", 
    "Deploy Discord Bot via Docker for 24/7 Operation",
    "High",
    "Pending",
    "Deploy Discord bot using Docker from GitHub repo for 24/7 mobile coordination. Files ready in discord-bot/ directory with Dockerfile and docker-compose.yml. Use SERVER_DISCORD_BOT_TOKEN for server instance.",
    "Running Docker container with Server Claude Discord bot online 24/7",
    "-"
]

claude_tasks.append_row(new_row)
print("✅ Task CT-099 created for Server Claude!")
print("🐳 Docker deployment task ready")