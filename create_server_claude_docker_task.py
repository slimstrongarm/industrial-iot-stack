#!/usr/bin/env python3
"""Create Docker deployment task for Server Claude in Google Sheets"""

import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

# Setup Google Sheets
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = Credentials.from_service_account_file('/Users/joshpayneair/Desktop/industrial-iot-stack/credentials/iot-stack-credentials.json', scopes=scope)
client = gspread.authorize(creds)

# Open spreadsheet and get Claude Tasks sheet
SPREADSHEET_ID = '1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do'
sheet = client.open_by_key(SPREADSHEET_ID)
claude_tasks = sheet.worksheet('Claude Tasks')

print("📋 Creating Server Claude Docker deployment task...")

# Get all values to find the next task ID
all_values = claude_tasks.get_all_values()

# Find the last CT number
last_ct_num = 0
for row in all_values:
    if row and row[0].startswith('CT-'):
        try:
            ct_num = int(row[0].split('-')[1])
            if ct_num > last_ct_num:
                last_ct_num = ct_num
        except:
            continue

# Create new task ID
new_task_id = f"CT-{last_ct_num + 1:03d}"

# Prepare detailed task description
task_description = """Deploy Discord Bot via Docker for 24/7 Operation

🎯 OBJECTIVE: Deploy Server Claude Discord bot using Docker for reliable 24/7 mobile coordination

📂 CODE LOCATION: All files ready in GitHub repository
   • Repository: https://github.com/slimstrongarm/industrial-iot-stack
   • Branch: main
   • Bot Directory: discord-bot/

🐳 DOCKER FILES PROVIDED:
   • discord-bot/Dockerfile - Container definition with Python 3.11
   • discord-bot/docker-compose.yml - Service orchestration
   • discord-bot/requirements.txt - All Python dependencies
   • discord-bot/run_server_claude_bot.py - Server bot launcher

🔧 DEPLOYMENT STEPS:
1. SSH to server: ssh localaccount@100.94.84.126
2. Enter WSL: wsl
3. Clone/update repo: git clone https://github.com/slimstrongarm/industrial-iot-stack
4. Copy credentials: Transfer credentials/iot-stack-credentials.json to server
5. Deploy with Docker: cd discord-bot && docker-compose up -d discord-bot
6. Verify: docker logs discord-bot (should show "Server Claude Bot" online)

🤖 BOT FEATURES IMPLEMENTED:
   • Bidirectional Discord communication (fixed token issue)
   • Google Sheets Claude Tasks integration
   • Instance detection (Server Claude vs Mac Claude)
   • Enhanced start task command: @server claude start task CT-XXX
   • Mobile-friendly command processing
   • Retry logic for Google Sheets API connections
   • Auto-restart on failure via Docker

📱 MOBILE WORKFLOW ENABLED:
Phone → Discord → Server Claude Bot → Google Sheets → Task Automation

🔍 VERIFICATION CHECKLIST:
   • Discord shows "Server Claude Bot" online
   • Bot responds to: @server claude status
   • Can create tasks: @server claude add task Test Docker deployment
   • Can start tasks: @server claude start task CT-XXX
   • Google Sheets integration working (creates/updates tasks)
   • Container auto-restarts if crashed

⚠️ CRITICAL FILES NEEDED:
   • credentials/iot-stack-credentials.json (Google Sheets API access)
   • Docker and docker-compose installed on server
   • SERVER_DISCORD_BOT_TOKEN environment variable (included in docker-compose.yml)

🎉 SUCCESS CRITERIA:
24/7 Discord bot running in Docker container, enabling mobile IoT stack management from anywhere via Discord mobile app."""

# Prepare new row data
current_date = datetime.now().strftime("%Y-%m-%d %H:%M")
new_row = [
    new_task_id,                      # Task ID
    "Server Claude",                  # Assigned To
    "Deploy Discord Bot via Docker for 24/7 Operation",  # Task Title
    "High",                          # Priority
    "Pending",                       # Status
    task_description,                # Description
    "Running Docker container with Server Claude Discord bot accessible 24/7 from mobile Discord app",  # Expected Output
    "-"                              # Dependencies
]

# Append to sheet
claude_tasks.append_row(new_row)

print(f"✅ Created task {new_task_id} for Server Claude")
print(f"📋 Task: Deploy Discord Bot via Docker for 24/7 Operation")
print(f"🎯 Assigned to: Server Claude")
print(f"⏰ Created: {current_date}")
print(f"🔗 View at: https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}")
print()
print("📱 Once deployed, you'll have 24/7 mobile coordination:")
print("   Phone → Discord → Server Claude → Google Sheets → Automation")
print()
print("🤖 Ready for Server Claude to execute!")