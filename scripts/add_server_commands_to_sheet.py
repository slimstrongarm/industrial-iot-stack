#!/usr/bin/env python3
"""
Add server connection commands to existing Google Sheet
"""

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pathlib import Path
from datetime import datetime

# Configuration
SHEET_ID = '1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do'  # Your IoT Stack Progress Master
CREDS_FILE = str(Path.home() / 'Desktop/industrial-iot-stack/credentials/iot-stack-credentials.json')

def add_server_commands_tab():
    """Add server commands to existing Google Sheet"""
    try:
        # Connect to Google Sheets
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_FILE, scope)
        client = gspread.authorize(creds)
        sheet = client.open_by_key(SHEET_ID)
        
        print("✅ Connected to IoT Stack Progress Master")
        
        # Create new worksheet
        try:
            worksheet = sheet.add_worksheet(title="Server Commands", rows=50, cols=5)
        except:
            # If it exists, get it
            worksheet = sheet.worksheet("Server Commands")
            worksheet.clear()
        
        # Commands content
        commands = [
            ["Server Connection Troubleshooting Commands", "", "", ""],
            ["Created: " + datetime.now().strftime("%Y-%m-%d %H:%M"), "", "", ""],
            ["", "", "", ""],
            ["STEP 1: Create More Permissive Firewall Rule", "", "", ""],
            ["Copy this entire command and paste in PowerShell Admin:", "", "", ""],
            ["", "", "", ""],
            ['New-NetFirewallRule -Name "SSH-In-All" -DisplayName "SSH Inbound All Networks" -Enabled True -Direction Inbound -Protocol TCP -Action Allow -LocalPort 22 -Profile Any -RemoteAddress Any', "", "", ""],
            ["", "", "", ""],
            ["STEP 2: Check Tailscale Status", "", "", ""],
            ["tailscale status", "", "", ""],
            ["", "", "", ""],
            ["STEP 3: Check All Port 22 Rules", "", "", ""],
            ["netsh advfirewall firewall show rule name=all | findstr /i \"22\"", "", "", ""],
            ["", "", "", ""],
            ["ADDITIONAL TROUBLESHOOTING:", "", "", ""],
            ["", "", "", ""],
            ["If still not working, try these commands:", "", "", ""],
            ["Restart-Service sshd", "Restart SSH service", "", ""],
            ["netstat -an | findstr :22", "Check if SSH is listening", "", ""],
            ["tailscale ping 100.94.84.126", "Test Tailscale connectivity", "", ""],
            ["", "", "", ""],
            ["CONNECTION INFO:", "", "", ""],
            ["Tailscale IP:", "100.94.84.126", "", ""],
            ["Username:", "localaccount", "", ""],
            ["Port:", "22", "", ""],
            ["", "", "", ""],
            ["From Mac Terminal:", "", "", ""],
            ["ssh localaccount@100.94.84.126", "", "", ""]
        ]
        
        # Update all at once
        worksheet.update(values=commands, range_name='A1:D28')
        
        # Format headers (simplified for compatibility)
        worksheet.format('A1', {'textFormat': {'bold': True, 'fontSize': 16}})
        worksheet.format('A4', {'textFormat': {'bold': True}})
        worksheet.format('A9', {'textFormat': {'bold': True}})
        worksheet.format('A12', {'textFormat': {'bold': True}})
        worksheet.format('A15', {'textFormat': {'bold': True}})
        worksheet.format('A22', {'textFormat': {'bold': True}})
        worksheet.format('A27', {'textFormat': {'bold': True}})
        
        print(f"\n✅ Server Commands tab added to your IoT Stack Progress Master!")
        print(f"📊 Open your Google Sheets and look for the 'Server Commands' tab")
        print(f"📋 You can now easily copy the commands from there!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    add_server_commands_tab()