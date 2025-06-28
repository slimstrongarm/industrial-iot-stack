#!/usr/bin/env python3
"""Create Discord Bot Instructions tab in Google Sheets"""

import gspread
from google.oauth2.service_account import Credentials

# Setup Google Sheets
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = Credentials.from_service_account_file('/Users/joshpayneair/Desktop/industrial-iot-stack/credentials/iot-stack-credentials.json', scopes=scope)
client = gspread.authorize(creds)

# Open spreadsheet
sheet = client.open_by_key('1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do')

# Create or update Discord Bot Instructions tab
try:
    ws = sheet.worksheet('Discord Bot Instructions')
    print("📝 Updating existing Discord Bot Instructions tab...")
except gspread.WorksheetNotFound:
    ws = sheet.add_worksheet(title='Discord Bot Instructions', rows=100, cols=10)
    print("📝 Created new Discord Bot Instructions tab...")

# Clear existing content
ws.clear()

# Instructions data
instructions = [
    ["🤖 Discord Bot Setup & Deployment Instructions", "", "", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", "", "", ""],
    ["🎯 DEPLOYMENT STRATEGY", "", "", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", "", "", ""],
    ["❌ Mac Laptop Issue:", "If Mac is closed/asleep, Mac Claude Bot goes offline", "", "", "", "", "", "", "", ""],
    ["✅ Solution:", "Deploy BOTH bots on the always-on server for 24/7 operation", "", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", "", "", ""],
    ["📱 Mobile Workflow:", "", "", "", "", "", "", "", "", ""],
    ["1. Send Discord command from phone", "", "", "", "", "", "", "", "", ""],
    ["2. Server Claude Bot (running 24/7) receives it", "", "", "", "", "", "", "", ""],
    ["3. Updates Google Sheets automatically", "", "", "", "", "", "", "", "", ""],
    ["4. Sends progress updates back to Discord", "", "", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", "", "", ""],
    ["🚀 QUICK TEST (Mac Laptop)", "", "", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", "", "", ""],
    ["Copy and paste this command in terminal:", "", "", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", "", "", ""],
    ["cd /Users/joshpayneair/Desktop/industrial-iot-stack/discord-bot && python3 run_mac_claude_bot.py", "", "", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", "", "", ""],
    ["Expected output:", "", "", "", "", "", "", "", "", ""],
    ["🤖 Mac Claude Discord Bot Launcher", "", "", "", "", "", "", "", "", ""],
    ["✅ Environment variables set", "", "", "", "", "", "", "", "", ""],
    ["🎯 Instance: Mac Claude", "", "", "", "", "", "", "", "", ""],
    ["🔑 Token: MTM4MTMxQx...", "", "", "", "", "", "", "", "", ""],
    ["⚡ Starting Discord connection...", "", "", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", "", "", ""],
    ["📱 Test from Discord:", "", "", "", "", "", "", "", "", ""],
    ["@mac claude status", "", "", "", "", "", "", "", "", ""],
    ["@mac claude add task Test mobile coordination", "", "", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", "", "", ""],
    ["🏭 PRODUCTION DEPLOYMENT (Server)", "", "", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", "", "", ""],
    ["Server setup commands:", "", "", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", "", "", ""],
    ["# 1. SSH to server", "", "", "", "", "", "", "", "", ""],
    ["ssh localaccount@100.94.84.126", "", "", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", "", "", ""],
    ["# 2. Enter WSL", "", "", "", "", "", "", "", "", ""],
    ["wsl", "", "", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", "", "", ""],
    ["# 3. Clone repository", "", "", "", "", "", "", "", "", ""],
    ["git clone https://github.com/slimstrongarm/industrial-iot-stack", "", "", "", "", "", "", "", "", ""],
    ["cd industrial-iot-stack/discord-bot", "", "", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", "", "", ""],
    ["# 4. Set up environment", "", "", "", "", "", "", "", "", ""],
    ["pip3 install discord.py gspread google-auth", "", "", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", "", "", ""],
    ["# 5. Create bot launcher for server", "", "", "", "", "", "", "", "", ""],
    ["nano run_server_claude_bot.py", "", "", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", "", "", ""],
    ["# 6. Deploy with systemd service", "", "", "", "", "", "", "", "", ""],
    ["sudo nano /etc/systemd/system/discord-bot.service", "", "", "", "", "", "", "", "", ""],
    ["sudo systemctl enable discord-bot.service", "", "", "", "", "", "", "", "", ""],
    ["sudo systemctl start discord-bot.service", "", "", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", "", "", ""],
    ["🐳 DOCKER DEPLOYMENT (Recommended)", "", "", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", "", "", ""],
    ["Create docker-compose.yml:", "", "", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", "", "", ""],
    ["version: '3.8'", "", "", "", "", "", "", "", "", ""],
    ["services:", "", "", "", "", "", "", "", "", ""],
    ["  discord-bot:", "", "", "", "", "", "", "", "", ""],
    ["    build: .", "", "", "", "", "", "", "", "", ""],
    ["    environment:", "", "", "", "", "", "", "", "", ""],
    ["      - SERVER_DISCORD_BOT_TOKEN=${SERVER_DISCORD_BOT_TOKEN}", "", "", "", "", "", "", "", "", ""],
    ["    restart: unless-stopped", "", "", "", "", "", "", "", "", ""],
    ["    volumes:", "", "", "", "", "", "", "", "", ""],
    ["      - ./credentials:/app/credentials", "", "", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", "", "", ""],
    ["Deploy:", "", "", "", "", "", "", "", "", ""],
    ["docker-compose up -d", "", "", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", "", "", ""],
    ["📊 MONITORING & STATUS", "", "", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", "", "", ""],
    ["Check bot status:", "", "", "", "", "", "", "", "", ""],
    ["docker-compose logs discord-bot", "", "", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", "", "", ""],
    ["Discord channels:", "", "", "", "", "", "", "", "", ""],
    ["#server-claude - Server Claude Bot commands", "", "", "", "", "", "", "", "", ""],
    ["#mac-claude - Mac Claude Bot commands (if running)", "", "", "", "", "", "", "", "", ""],
    ["#general - Both bots respond", "", "", "", "", "", "", "", "", ""],
    ["#alerts - System notifications", "", "", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", "", "", ""],
    ["📱 MOBILE COMMANDS", "", "", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", "", "", ""],
    ["From Discord mobile app:", "", "", "", "", "", "", "", "", ""],
    ["@server claude status", "", "", "", "", "", "", "", "", ""],
    ["@server claude add task Deploy new feature", "", "", "", "", "", "", "", "", ""],
    ["@server claude start task CT-094", "", "", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", "", "", ""],
    ["✅ TROUBLESHOOTING", "", "", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", "", "", ""],
    ["Bot offline:", "", "", "", "", "", "", "", "", ""],
    ["1. Check Docker container: docker ps | grep discord", "", "", "", "", "", "", "", "", ""],
    ["2. Check logs: docker-compose logs discord-bot", "", "", "", "", "", "", "", "", ""],
    ["3. Restart: docker-compose restart discord-bot", "", "", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", "", "", ""],
    ["Can't create tasks:", "", "", "", "", "", "", "", "", ""],
    ["1. Check Google Sheets credentials", "", "", "", "", "", "", "", "", ""],
    ["2. Verify service account permissions", "", "", "", "", "", "", "", "", ""],
    ["3. Test: @server claude status", "", "", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", "", "", ""],
    ["🎯 RECOMMENDED SETUP", "", "", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", "", "", ""],
    ["1. Deploy Server Claude Bot on server (24/7)", "", "", "", "", "", "", "", "", ""],
    ["2. Use Mac Claude Bot for local development only", "", "", "", "", "", "", "", "", ""],
    ["3. Primary workflow: Phone → Discord → Server Claude → Google Sheets", "", "", "", "", "", "", "", "", ""],
    ["4. Monitor via Discord mobile app", "", "", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", "", "", ""],
    ["Last Updated:", "2025-06-10", "", "", "", "", "", "", "", ""],
]

# Write instructions to sheet
for i, row in enumerate(instructions, 1):
    for j, cell in enumerate(row, 1):
        if cell:  # Only write non-empty cells
            ws.update_cell(i, j, cell)

# Format the sheet
print("🎨 Formatting Discord Bot Instructions tab...")

# Bold headers
ws.format('A1:J1', {'textFormat': {'bold': True, 'fontSize': 14}})
ws.format('A3', {'textFormat': {'bold': True, 'fontSize': 12}})
ws.format('A14', {'textFormat': {'bold': True, 'fontSize': 12}})
ws.format('A30', {'textFormat': {'bold': True, 'fontSize': 12}})
ws.format('A47', {'textFormat': {'bold': True, 'fontSize': 12}})
ws.format('A63', {'textFormat': {'bold': True, 'fontSize': 12}})
ws.format('A73', {'textFormat': {'bold': True, 'fontSize': 12}})
ws.format('A81', {'textFormat': {'bold': True, 'fontSize': 12}})
ws.format('A91', {'textFormat': {'bold': True, 'fontSize': 12}})

# Color code sections
ws.format('A1:J2', {'backgroundColor': {'red': 0.8, 'green': 1.0, 'blue': 0.8}})  # Light green
ws.format('A3:J13', {'backgroundColor': {'red': 1.0, 'green': 0.9, 'blue': 0.8}})  # Light orange
ws.format('A14:J29', {'backgroundColor': {'red': 0.8, 'green': 0.9, 'blue': 1.0}})  # Light blue
ws.format('A30:J46', {'backgroundColor': {'red': 0.9, 'green': 0.8, 'blue': 1.0}})  # Light purple

# Make command cells monospace
ws.format('A18', {'textFormat': {'fontFamily': 'Courier New'}})
ws.format('A35:A45', {'textFormat': {'fontFamily': 'Courier New'}})
ws.format('A52:A60', {'textFormat': {'fontFamily': 'Courier New'}})

print("✅ Discord Bot Instructions tab created successfully!")
print("📱 Access it at: https://docs.google.com/spreadsheets/d/1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do")