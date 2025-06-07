#!/usr/bin/env python3
"""
Add task for Server Claude to deploy Steel Bonnet WhatsApp integration
"""

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pathlib import Path
from datetime import datetime

# Configuration
SHEET_ID = '1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do'
CREDS_FILE = str(Path.home() / 'Desktop/industrial-iot-stack/credentials/iot-stack-credentials.json')

def add_steel_bonnet_task():
    """Add new task for Steel Bonnet WhatsApp integration deployment"""
    try:
        # Connect to Google Sheets
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_FILE, scope)
        client = gspread.authorize(creds)
        sheet = client.open_by_key(SHEET_ID)
        
        claude_sheet = sheet.worksheet('Claude Tasks')
        
        # Find the highest CT task number
        records = claude_sheet.get_all_records()
        ct_numbers = []
        for record in records:
            task_id = record.get('Task ID', '')
            if task_id.startswith('CT-'):
                try:
                    num = int(task_id.split('-')[1])
                    ct_numbers.append(num)
                except:
                    pass
        
        next_number = max(ct_numbers) + 1 if ct_numbers else 1
        next_task_id = f"CT-{next_number:03d}"
        
        # Add new Steel Bonnet WhatsApp task
        new_task = [
            next_task_id,
            "Server Claude", 
            "WhatsApp Integration",
            "High",
            "Pending",
            "Deploy Steel Bonnet WhatsApp integration using steel-bonnet-flow.json with actual MQTT topics",
            "Node-RED flow deployed listening to Steel Bonnet MQTT topics (site/area/equipment/telemetry) with equipment-specific thresholds and professional alert formatting",
            "CT-027",  # Depends on Discord bot being deployed
            datetime.now().strftime("%Y-%m-%d"),
            ""
        ]
        
        # Add the task
        claude_sheet.append_row(new_task)
        
        print(f"✅ Added {next_task_id}: Steel Bonnet WhatsApp Integration")
        print(f"   Instance: Server Claude")
        print(f"   Priority: High")
        print(f"   Dependencies: CT-027 (Discord bot)")
        print(f"   Files ready: steel-bonnet-flow.json")
        
        # Log activity
        agent_sheet = sheet.worksheet('Agent Activities')
        agent_sheet.append_row([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Mac Claude",
            f"Added {next_task_id} for Steel Bonnet WhatsApp",
            "Complete",
            "5 min",
            "Added task for Server Claude to deploy Steel Bonnet WhatsApp integration with actual MQTT topics",
            "Server Claude to deploy steel-bonnet-flow.json"
        ])
        
        print(f"\n📋 Task Details:")
        print(f"   • Uses actual Steel Bonnet MQTT topic structure")
        print(f"   • Listens to: site/area/equipment/telemetry")
        print(f"   • Equipment thresholds for all Steel Bonnet UDT types")
        print(f"   • Professional alerts with site/area context")
        print(f"   • Ready for Friday brewery demo")
        
        print(f"\n🤖 Server Claude automation will pick this up in 60 seconds!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    add_steel_bonnet_task()