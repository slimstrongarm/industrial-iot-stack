#!/usr/bin/env python3
"""Clean up overlapping and conflicting tasks in Google Sheets"""

import os
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Configuration
CREDS_PATH = "/Users/joshpayneair/Desktop/industrial-iot-stack/credentials/iot-stack-credentials.json"
SPREADSHEET_ID = "1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do"

def get_sheets_service():
    """Initialize Google Sheets API service"""
    creds = service_account.Credentials.from_service_account_file(
        CREDS_PATH,
        scopes=['https://www.googleapis.com/auth/spreadsheets']
    )
    return build('sheets', 'v4', credentials=creds)

def find_task_rows(service):
    """Find all task rows and identify conflicts"""
    result = service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID,
        range="Claude Tasks!A:G"
    ).execute()
    
    values = result.get('values', [])
    task_map = {}
    
    for idx, row in enumerate(values[1:], start=2):  # Skip header, 1-based indexing
        if row and row[0].startswith('CT-'):
            task_id = row[0]
            task_map[task_id] = {
                'row': idx,
                'data': row,
                'instance': row[1] if len(row) > 1 else '',
                'task_type': row[2] if len(row) > 2 else '',
                'status': row[4] if len(row) > 4 else ''
            }
    
    return task_map

def cleanup_conflicting_tasks(service):
    """Clean up overlapping and conflicting tasks"""
    
    tasks = find_task_rows(service)
    
    # Identify conflicts
    conflicts = {
        'discord_setup': {
            'old_tasks': ['CT-050', 'CT-051', 'CT-052', 'CT-053', 'CT-054'],
            'new_tasks': ['CT-081', 'CT-082'],
            'action': 'Mark old as superseded'
        }
    }
    
    updates = []
    
    print("🧹 Cleaning up task conflicts...")
    
    # Handle Discord setup conflicts
    discord_old = ['CT-050', 'CT-051', 'CT-052', 'CT-053', 'CT-054']
    for task_id in discord_old:
        if task_id in tasks:
            row_num = tasks[task_id]['row']
            # Update status to "Superseded" and add note
            updates.append({
                'range': f'Claude Tasks!E{row_num}',
                'values': [['Superseded']]
            })
            updates.append({
                'range': f'Claude Tasks!F{row_num}',
                'values': [[f"SUPERSEDED by CT-081/CT-082. Server Claude completed Discord integration via newer, more efficient approach. This task is no longer needed."]]
            })
            print(f"📝 {task_id}: Marked as Superseded")
    
    # Create priority guidance for Server Claude
    guidance_task = [[
        "CT-PRIORITY",
        "Server Claude",
        "Task Priority Guidance",
        "Critical",
        "Active",
        "CURRENT PRIORITY ORDER: 1) CT-076 (Docker Agent) - builds on ADK foundation, 2) CT-077 (SystemD Agent) - complements Docker, 3) CT-078-080 (other agents), 4) CT-084+ (Parachute Drop). Ignore CT-050-054 (superseded by completed CT-081/082).",
        "Clear task roadmap preventing confusion and ensuring efficient progress on specialized agents."
    ]]
    
    # Add priority guidance
    append_body = {
        'values': guidance_task
    }
    
    service.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID,
        range="Claude Tasks!A:G",
        valueInputOption="RAW",
        insertDataOption="INSERT_ROWS",
        body=append_body
    ).execute()
    
    print("✅ Added CT-PRIORITY guidance task")
    
    # Batch update all the superseded tasks
    if updates:
        batch_body = {
            'valueInputOption': 'RAW',
            'data': [{'range': update['range'], 'values': update['values']} for update in updates]
        }
        
        service.spreadsheets().values().batchUpdate(
            spreadsheetId=SPREADSHEET_ID,
            body=batch_body
        ).execute()
        
        print(f"✅ Updated {len(updates)//2} conflicting tasks")
    
    return len(updates)//2

def add_mqtt_broker_task(service):
    """Add task to fix MQTT broker issue seen in Discord"""
    
    mqtt_task = [[
        "CT-MQTT-FIX",
        "Server Claude", 
        "Infrastructure Fix",
        "High",
        "Not Started",
        "Fix MQTT broker connectivity issue detected in Discord status. EMQX showing 'Not responding' - investigate and resolve connection issues for Parachute Drop system.",
        "MQTT broker operational and responding properly. All MQTT-dependent systems (Node-RED, Parachute Drop, etc.) can connect successfully."
    ]]
    
    append_body = {
        'values': mqtt_task
    }
    
    service.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID,
        range="Claude Tasks!A:G", 
        valueInputOption="RAW",
        insertDataOption="INSERT_ROWS",
        body=append_body
    ).execute()
    
    print("🔧 Added MQTT broker fix task")

def main():
    """Main execution"""
    print("🧹 Cleaning up task conflicts and technical debt...\n")
    
    service = get_sheets_service()
    
    # Clean up conflicts
    cleaned_count = cleanup_conflicting_tasks(service)
    
    # Add MQTT fix task
    add_mqtt_broker_task(service)
    
    print(f"\n✅ Cleanup complete!")
    print(f"📋 Actions taken:")
    print(f"   - Marked {cleaned_count} old Discord tasks as 'Superseded'")
    print(f"   - Added CT-PRIORITY guidance for Server Claude")
    print(f"   - Added CT-MQTT-FIX for broker issues")
    print("\n🎯 Server Claude now has clear priority order:")
    print("   1. CT-076 (Docker Agent)")
    print("   2. CT-077 (SystemD Agent)")  
    print("   3. CT-MQTT-FIX (Broker fix)")
    print("   4. CT-078-080 (Other agents)")
    print("   5. CT-084+ (Parachute Drop)")

if __name__ == "__main__":
    main()