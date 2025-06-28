#!/usr/bin/env python3
"""
Create Google Doc with server connection commands
"""

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pathlib import Path
from datetime import datetime

# Configuration
CREDS_FILE = str(Path.home() / 'Desktop/industrial-iot-stack/credentials/iot-stack-credentials.json')

def create_server_connection_doc():
    """Create a Google Doc with server connection troubleshooting commands"""
    try:
        # Connect to Google
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive',
                 'https://www.googleapis.com/auth/documents']
        creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_FILE, scope)
        client = gspread.authorize(creds)
        
        print("✅ Connected to Google Drive")
        
        # Create a new Google Doc (using Sheets API to create in Drive)
        doc = client.create("Server Connection")
        
        # Get the first sheet and rename it
        sheet = doc.sheet1
        sheet.update_title("Connection Commands")
        
        # Add content
        content = [
            ["Server Connection Troubleshooting Commands"],
            [""],
            ["Created: " + datetime.now().strftime("%Y-%m-%d %H:%M")],
            [""],
            ["STEP 1: Create More Permissive Firewall Rule"],
            ["Copy and paste this command in PowerShell Admin:"],
            [""],
            ["New-NetFirewallRule -Name \"SSH-In-All\" -DisplayName \"SSH Inbound All Networks\" -Enabled True -Direction Inbound -Protocol TCP -Action Allow -LocalPort 22 -Profile Any -RemoteAddress Any"],
            [""],
            ["STEP 2: Check Tailscale Status"],
            ["Run this command:"],
            [""],
            ["tailscale status"],
            [""],
            ["STEP 3: Check All Port 22 Rules"],
            ["Run this command to see ALL firewall rules affecting port 22:"],
            [""],
            ["netsh advfirewall firewall show rule name=all | findstr /i \"22\""],
            [""],
            ["ADDITIONAL TROUBLESHOOTING:"],
            [""],
            ["If still not working, try:"],
            ["1. Restart SSH service: Restart-Service sshd"],
            ["2. Check if SSH is listening: netstat -an | findstr :22"],
            ["3. Test Tailscale connectivity: tailscale ping 100.94.84.126"],
            [""],
            ["Connection Info:"],
            ["- Tailscale IP: 100.94.84.126"],
            ["- Username: localaccount"],
            ["- Port: 22"],
            [""],
            ["From Mac, connect with:"],
            ["ssh localaccount@100.94.84.126"]
        ]
        
        # Update the sheet with content
        for i, row in enumerate(content, 1):
            if row:  # Only update non-empty rows
                sheet.update_cell(i, 1, row[0])
        
        # Make the title bold and larger
        sheet.format('A1', {'textFormat': {'bold': True, 'fontSize': 16}})
        sheet.format('A5', {'textFormat': {'bold': True}})
        sheet.format('A10', {'textFormat': {'bold': True}})
        sheet.format('A15', {'textFormat': {'bold': True}})
        sheet.format('A20', {'textFormat': {'bold': True}})
        
        # Format the command cells with a different background
        sheet.format('A8', {'backgroundColor': {'red': 0.9, 'green': 0.9, 'blue': 0.9}})
        sheet.format('A13', {'backgroundColor': {'red': 0.9, 'green': 0.9, 'blue': 0.9}})
        sheet.format('A18', {'backgroundColor': {'red': 0.9, 'green': 0.9, 'blue': 0.9}})
        
        # Share with user (make it public for easy access)
        doc.share('', perm_type='anyone', role='reader')
        
        print(f"\n✅ Google Doc created successfully!")
        print(f"📄 Document URL: {doc.url}")
        print(f"\nYou can now access this document from any browser!")
        
        return doc.url
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

if __name__ == "__main__":
    url = create_server_connection_doc()
    if url:
        print(f"\n🔗 Quick link: {url}")