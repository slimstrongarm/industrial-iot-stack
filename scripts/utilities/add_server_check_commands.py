#!/usr/bin/env python3
"""
Add server check commands to Google Sheet
"""

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pathlib import Path
from datetime import datetime

# Configuration
SHEET_ID = '1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do'
CREDS_FILE = str(Path.home() / 'Desktop/industrial-iot-stack/credentials/iot-stack-credentials.json')

def add_server_check_tab():
    """Add server check commands to Google Sheet"""
    try:
        # Connect to Google Sheets
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_FILE, scope)
        client = gspread.authorize(creds)
        sheet = client.open_by_key(SHEET_ID)
        
        print("✅ Connected to IoT Stack Progress Master")
        
        # Create or clear worksheet
        try:
            worksheet = sheet.add_worksheet(title="Server Check Commands", rows=50, cols=5)
        except:
            worksheet = sheet.worksheet("Server Check Commands")
            worksheet.clear()
        
        # Commands content
        commands = [
            ["Server Setup & Service Check Commands", "", "", ""],
            ["Last Updated: " + datetime.now().strftime("%Y-%m-%d %H:%M"), "", "", ""],
            ["", "", "", ""],
            ["STEP 1: SSH Connection", "", "", ""],
            ["ssh localaccount@100.94.84.126", "", "", ""],
            ["Password: LocalAccount", "", "", ""],
            ["", "", "", ""],
            ["STEP 2: Enter WSL", "", "", ""],
            ["wsl", "", "", ""],
            ["", "", "", ""],
            ["STEP 3: Check All Services (copy entire block)", "", "", ""],
            ['echo "=== CHECKING SERVICES ===" && echo "" && echo "🔴 Node-RED:" && (curl -s http://localhost:1880 >/dev/null 2>&1 && echo "✅ Running on port 1880" || echo "❌ Not running") && echo "" && echo "📡 MQTT:" && (netstat -an | grep :1883 >/dev/null 2>&1 && echo "✅ Running on port 1883" || echo "❌ Not running") && echo "" && echo "🔥 Ignition:" && (curl -s http://localhost:8088/StatusPing >/dev/null 2>&1 && echo "✅ Running on port 8088" || echo "❌ Not running") && echo "" && echo "🐳 Docker:" && (docker ps >/dev/null 2>&1 && docker ps || echo "❌ Docker not accessible")', "", "", ""],
            ["", "", "", ""],
            ["STEP 4: Create Blue TMUX Screen", "", "", ""],
            ['echo \'set -g status-style "bg=colour4 fg=colour15"\' > ~/.tmux.conf && echo \'set -g status-left "#[bg=colour12,fg=colour0] 🖥️ SERVER "\' >> ~/.tmux.conf && tmux new-session -s claude-server', "", "", ""],
            ["", "", "", ""],
            ["ADDITIONAL USEFUL COMMANDS:", "", "", ""],
            ["", "", "", ""],
            ["Check specific services:", "", "", ""],
            ["docker ps -a", "Show all Docker containers", "", ""],
            ["docker logs node-red", "Show Node-RED logs", "", ""],
            ["netstat -tlnp", "Show all listening ports", "", ""],
            ["systemctl status ignition", "Check Ignition service", "", ""],
            ["", "", "", ""],
            ["TMUX Commands:", "", "", ""],
            ["tmux attach -t claude-server", "Reattach to session", "", ""],
            ["Ctrl+B then D", "Detach from TMUX", "", ""],
            ["Ctrl+B then C", "Create new window", "", ""],
            ["Ctrl+B then 0-9", "Switch windows", "", ""],
            ["", "", "", ""],
            ["Quick Docker Deploy:", "", "", ""],
            ["mkdir -p ~/iiot-stack && cd ~/iiot-stack", "Create project directory", "", ""],
            ["docker run -d --name mqtt -p 1883:1883 eclipse-mosquitto", "Start MQTT broker", "", ""],
            ["docker run -d --name node-red -p 1880:1880 nodered/node-red", "Start Node-RED", "", ""],
            ["", "", "", ""],
            ["NOTES:", "", "", ""],
            ["- Blue TMUX = Server instance", "", "", ""],
            ["- Green TMUX = Mac instance", "", "", ""],
            ["- Services may already be running", "", "", ""],
            ["- Check before deploying new ones", "", "", ""]
        ]
        
        # Update sheet
        worksheet.update(values=commands, range_name='A1:D40')
        
        # Format headers
        worksheet.format('A1', {'textFormat': {'bold': True, 'fontSize': 16}})
        worksheet.format('A4', {'textFormat': {'bold': True}})
        worksheet.format('A8', {'textFormat': {'bold': True}})
        worksheet.format('A11', {'textFormat': {'bold': True}})
        worksheet.format('A14', {'textFormat': {'bold': True}})
        worksheet.format('A17', {'textFormat': {'bold': True}})
        worksheet.format('A25', {'textFormat': {'bold': True}})
        worksheet.format('A31', {'textFormat': {'bold': True}})
        worksheet.format('A36', {'textFormat': {'bold': True}})
        
        # Highlight command cells
        worksheet.format('A5', {'backgroundColor': {'red': 0.95, 'green': 0.95, 'blue': 0.95}})
        worksheet.format('A9', {'backgroundColor': {'red': 0.95, 'green': 0.95, 'blue': 0.95}})
        worksheet.format('A12', {'backgroundColor': {'red': 0.95, 'green': 0.95, 'blue': 0.95}})
        worksheet.format('A15', {'backgroundColor': {'red': 0.95, 'green': 0.95, 'blue': 0.95}})
        
        print(f"\n✅ 'Server Check Commands' tab added!")
        print(f"📊 Open your Google Sheets to copy the commands")
        print(f"🔵 The blue TMUX will appear after running the last command")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    add_server_check_tab()