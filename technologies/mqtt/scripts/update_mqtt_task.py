#!/usr/bin/env python3
"""
Update MQTT task for Server Claude with EMQX specifics
"""

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pathlib import Path
from datetime import datetime

# Configuration
SHEET_ID = '1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do'
CREDS_FILE = str(Path.home() / 'Desktop/industrial-iot-stack/credentials/iot-stack-credentials.json')

def update_mqtt_task():
    """Update MQTT task with EMQX information"""
    try:
        # Connect to Google Sheets
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_FILE, scope)
        client = gspread.authorize(creds)
        sheet = client.open_by_key(SHEET_ID)
        
        print("🔄 Updating MQTT task for EMQX...")
        
        # Add to Human Tasks
        human_sheet = sheet.worksheet('Human Tasks')
        
        # Add clarification task
        human_sheet.append_row([
            'Server Claude',
            'Testing',
            'High',
            'Pending',
            'Server Claude',
            '-',
            'UPDATED MQTT Task: Test EMQX (not Mosquitto!) 1) Check EMQX status and version, 2) Access EMQX dashboard (usually :18083), 3) List active topics using EMQX CLI, 4) Note authentication settings',
            datetime.now().strftime('%Y-%m-%d %H:%M')
        ])
        
        # Add to Agent Activities
        agent_sheet = sheet.worksheet('Agent Activities')
        agent_sheet.append_row([
            datetime.now().strftime('%Y-%m-%d %H:%M'),
            'Mac Claude',
            'Clarified MQTT architecture - EMQX on server, Mosquitto on Mac',
            'Complete',
            '2 min',
            'Updated tasks to reflect EMQX specifics',
            'Monitor EMQX testing'
        ])
        
        # Add critical note to System Components
        try:
            components_sheet = sheet.worksheet('System Components Status')
            # Add MQTT broker info
            components_sheet.append_row([
                'MQTT (Mac - Mosquitto)',
                'Running',
                '✅ Healthy',
                '2.0.18',
                datetime.now().strftime('%Y-%m-%d %H:%M'),
                '-',
                '-',
                '-',
                'Development broker'
            ])
            components_sheet.append_row([
                'MQTT (Server - EMQX)',
                'Unknown',
                '🔍 Checking',
                'TBD',
                datetime.now().strftime('%Y-%m-%d %H:%M'),
                '-',
                '-',
                '-',
                'Production broker - needs audit'
            ])
        except Exception as e:
            print(f"Note: Could not update components sheet: {e}")
        
        print("✅ MQTT task updated with EMQX specifics")
        print("\n📋 Key Points for Server Claude:")
        print("- EMQX is on the server (NOT Mosquitto)")
        print("- EMQX has a web dashboard (usually port 18083)")
        print("- EMQX has different CLI commands")
        print("- Authentication may be required")
        print("\n🌉 Future: We'll test broker-to-broker communication")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    update_mqtt_task()