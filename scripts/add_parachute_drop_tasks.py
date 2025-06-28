#!/usr/bin/env python3
"""Add Parachute Drop system tasks to Google Sheets for Server Claude"""

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

def get_next_task_id(service):
    """Find the next available task ID"""
    result = service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID,
        range="Claude Tasks!A:A"
    ).execute()
    
    values = result.get('values', [])
    max_id = 0
    
    for row in values[1:]:  # Skip header
        if row and row[0].startswith('CT-'):
            try:
                task_num = int(row[0].split('-')[1])
                max_id = max(max_id, task_num)
            except:
                pass
    
    return f"CT-{max_id + 1:03d}"

def add_parachute_drop_tasks(service):
    """Add comprehensive Parachute Drop system tasks"""
    
    next_id = get_next_task_id(service)
    next_num = int(next_id.split('-')[1])
    
    # Define Parachute Drop task sequence
    parachute_tasks = [
        {
            "name": "Build Parachute Drop Pi Image",
            "description": "Create pre-configured Raspberry Pi image with Node-RED, EMQX, Phidget drivers, and auto-start dashboard. Include all discovery agents and sensor configurations for rapid deployment.",
            "priority": "High",
            "complexity": "Medium",
            "assigned_to": "Server Claude"
        },
        {
            "name": "Implement Industrial Discovery Agent",
            "description": "Deploy the network discovery agent that scans for PLCs, MQTT brokers, and Modbus devices. Include AI-powered tag purpose detection and automatic Node-RED flow generation.",
            "priority": "High", 
            "complexity": "High",
            "assigned_to": "Server Claude"
        },
        {
            "name": "Configure Portable Router Network",
            "description": "Set up GL.iNet router with isolated network, VPN tunnel, and traffic monitoring. Create secure remote access for post-deployment enhancement and data collection.",
            "priority": "Medium",
            "complexity": "Medium", 
            "assigned_to": "Server Claude"
        },
        {
            "name": "Build Sensor Auto-Configuration System",
            "description": "Implement automatic sensor detection and dashboard generation based on connected Phidget sensors. Include multiple sensor types: current, temperature, pressure, digital I/O.",
            "priority": "Medium",
            "complexity": "Medium",
            "assigned_to": "Server Claude" 
        },
        {
            "name": "Create Serial/Modbus Interface",
            "description": "Deploy legacy protocol support for Modbus RTU, BACnet MS/TP, and DF1. Include automatic device scanning and register mapping with purpose detection.",
            "priority": "Medium",
            "complexity": "High",
            "assigned_to": "Server Claude"
        },
        {
            "name": "Develop MQTT Traffic Analyzer", 
            "description": "Build system to capture and analyze existing MQTT traffic for topic intelligence. Generate recommendations for integration with existing systems.",
            "priority": "Low",
            "complexity": "Medium",
            "assigned_to": "Server Claude"
        },
        {
            "name": "Test Complete Parachute Drop System",
            "description": "End-to-end testing of full deployment kit including hardware setup, network discovery, sensor deployment, and remote access. Validate 15-minute deployment target.",
            "priority": "High",
            "complexity": "Medium",
            "assigned_to": "Server Claude"
        }
    ]
    
    # Create rows for each task
    new_rows = []
    for i, task in enumerate(parachute_tasks):
        task_id = f"CT-{next_num + i:03d}"
        row = [
            task_id,                          # Task ID
            task["assigned_to"],              # Instance
            "Parachute Drop System",          # Task Type
            task["priority"],                 # Priority
            "Not Started",                    # Status
            task["description"],              # Description
            f"Fully operational {task['name'].lower()} component integrated into Parachute Drop system. Validated for rapid industrial deployment with professional dashboard and remote monitoring capabilities."  # Expected Output
        ]
        new_rows.append(row)
    
    # Add milestone celebration task
    milestone_task = [[
        f"CT-{next_num + len(parachute_tasks):03d}",
        "Josh",
        "🪂 Parachute Drop Complete",
        "Critical",
        "Not Started", 
        "Complete Industrial IoT Rapid Deployment Kit ready for field deployment. System enables 15-minute facility assessments with live dashboards, network discovery, and continuous intelligence gathering.",
        "Revolutionary industrial consulting capability operational! Transform from project consultant to technology platform provider with ongoing monitoring services."
    ]]
    
    new_rows.extend(milestone_task)
    
    # Append to sheet
    body = {
        'values': new_rows
    }
    
    result = service.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID,
        range="Claude Tasks!A:G",
        valueInputOption="RAW",
        insertDataOption="INSERT_ROWS",
        body=body
    ).execute()
    
    print(f"🪂 Added {len(new_rows)} Parachute Drop tasks!")
    print(f"Task IDs: CT-{next_num:03d} through CT-{next_num + len(new_rows) - 1:03d}")
    
    return result

def main():
    """Main execution"""
    print("🪂 Adding Parachute Drop system tasks to Google Sheets...\n")
    
    service = get_sheets_service()
    add_parachute_drop_tasks(service)
    
    print("\n🚀 Parachute Drop project added to Claude Tasks!")
    print("\nServer Claude now has a complete Industrial IoT Rapid Deployment system to build!")
    print("\nThis system will:")
    print("- Deploy live monitoring in 15 minutes")
    print("- Discover and map industrial networks automatically") 
    print("- Generate professional dashboards instantly")
    print("- Provide continuous remote intelligence gathering")
    print("- Transform consulting business model")
    print("\n🎯 Ready to revolutionize industrial consulting!")

if __name__ == "__main__":
    main()