#!/usr/bin/env python3
"""
Add simple tasks for Server Claude to Human Tasks sheet
"""

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pathlib import Path
from datetime import datetime

# Configuration
SHEET_ID = '1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do'
CREDS_FILE = str(Path.home() / 'Desktop/industrial-iot-stack/credentials/iot-stack-credentials.json')

def add_server_tasks():
    """Add tasks for Server Claude"""
    try:
        # Connect to Google Sheets
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_FILE, scope)
        client = gspread.authorize(creds)
        sheet = client.open_by_key(SHEET_ID)
        
        print("📝 Adding tasks for Server Claude...")
        
        # Get Human Tasks worksheet
        human_sheet = sheet.worksheet('Human Tasks')
        
        # Simple tasks for Server Claude
        tasks = [
            [
                'Server Claude',           # Role
                'Documentation',           # Task Type
                'Medium',                  # Priority
                'Pending',                 # Status
                'Server Claude',           # Assigned To
                'Docker check complete',   # Dependencies
                'Document all currently installed services and their versions (Node-RED, Ignition, MQTT, databases). Create a markdown file with findings.',  # Notes
                datetime.now().strftime('%Y-%m-%d %H:%M')  # Date Added
            ],
            [
                'Server Claude',
                'Testing',
                'Medium',
                'Pending',
                'Server Claude',
                'Service documentation complete',
                'Test MQTT connectivity: 1) Check if MQTT broker is running, 2) Test publish/subscribe with mosquitto_pub/sub, 3) Document the MQTT topics being used',
                datetime.now().strftime('%Y-%m-%d %H:%M')
            ],
            [
                'Server Claude',
                'Architecture',
                'Low',
                'Pending',
                'Server Claude',
                'MQTT test complete',
                'Create a simple network diagram showing which services are running on which ports. Use ASCII art or markdown table format.',
                datetime.now().strftime('%Y-%m-%d %H:%M')
            ]
        ]
        
        # Add tasks
        for task in tasks:
            human_sheet.append_row(task)
            print(f"✅ Added: {task[6][:50]}...")
            
        # Also update Agent Activities to show task assignment
        agent_sheet = sheet.worksheet('Agent Activities')
        agent_sheet.append_row([
            datetime.now().strftime('%Y-%m-%d %H:%M'),
            'Mac Claude',
            'Assigned 3 simple tasks to Server Claude',
            'Complete',
            '1 min',
            'Documentation, MQTT testing, and network diagram tasks',
            'Monitor progress'
        ])
        
        print(f"\n✅ Added {len(tasks)} tasks for Server Claude")
        print("\n📋 Tasks Summary:")
        print("1. Document all installed services and versions")
        print("2. Test MQTT broker connectivity") 
        print("3. Create network diagram of services/ports")
        print("\nThese should keep Server Claude productive while you handle Docker! 🚀")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    add_server_tasks()