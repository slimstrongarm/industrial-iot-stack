#!/usr/bin/env python3
"""
Morning status update for Google Sheets
"""

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pathlib import Path
from datetime import datetime

# Configuration
SHEET_ID = '1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do'
CREDS_FILE = str(Path.home() / 'Desktop/industrial-iot-stack/credentials/iot-stack-credentials.json')

def morning_update():
    """Update sheets with morning status"""
    try:
        # Connect to Google Sheets
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_FILE, scope)
        client = gspread.authorize(creds)
        sheet = client.open_by_key(SHEET_ID)
        
        print("☀️ Good morning! Updating sheets...")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        # Update Agent Activities
        agent_sheet = sheet.worksheet('Agent Activities')
        activities = [
            [timestamp, "Mac Claude", "Morning startup - Both instances ready", "Active", "Just started", "Claude Code working on server!", "Configure Docker"],
            [timestamp, "Server Claude", "Claude Code operational via npx fix", "Active", "New", "Ready for direct control", "Run service audit"]
        ]
        for activity in activities:
            agent_sheet.append_row(activity)
            
        # Add to Human Tasks
        human_sheet = sheet.worksheet('Human Tasks')
        human_sheet.append_row([
            'Architect', 'Docker Setup', 'High', 'In Progress', 'You', 
            'Claude Code working', 
            'Need to resolve Docker WSL + Claude Code conflict. Currently Docker WSL integration OFF', 
            timestamp
        ])
        
        # Update Dashboard
        dashboard = sheet.worksheet('Dashboard')
        dashboard.update_cell(13, 2, f'"{timestamp}"')
        
        print("✅ Sheets updated!")
        print("\n🎯 Today's Mission:")
        print("1. Document that npx fix (share it!)")
        print("2. Get Docker working alongside Claude Code") 
        print("3. Audit server services")
        print("4. Configure Ignition Edge")
        print("5. Demo ready by Friday!")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    morning_update()