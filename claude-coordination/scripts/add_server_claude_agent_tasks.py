#!/usr/bin/env python3
"""Add specialized agent tasks for Server Claude to Google Sheets"""

import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime

# Load credentials
CREDS_PATH = "/Users/joshpayneair/Desktop/industrial-iot-stack/credentials/iot-stack-credentials.json"
SPREADSHEET_ID = "1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do"

def get_sheets_service():
    """Initialize Google Sheets API service"""
    creds = service_account.Credentials.from_service_account_file(
        CREDS_PATH,
        scopes=['https://www.googleapis.com/auth/spreadsheets']
    )
    return build('sheets', 'v4', credentials=creds)

def get_next_task_id(service, sheet_range="Claude Tasks!A:A"):
    """Find the next available task ID"""
    result = service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID,
        range=sheet_range
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

def add_server_claude_agents(service):
    """Add specialized agent tasks for Server Claude"""
    
    # Get current sheet structure
    result = service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID,
        range="Claude Tasks!1:1"
    ).execute()
    
    headers = result.get('values', [[]])[0]
    print(f"Headers: {headers}")
    
    # Get next task ID
    next_id = get_next_task_id(service)
    next_num = int(next_id.split('-')[1])
    
    # Define new agent tasks
    agent_tasks = [
        {
            "name": "Create Docker Management Agent for Server Claude",
            "description": "Build specialized agent to handle Docker container operations, health checks, and deployments",
            "priority": "High",
            "complexity": "Medium"
        },
        {
            "name": "Create SystemD Service Agent for Server Claude",
            "description": "Develop agent for managing persistent services, auto-restart policies, and service monitoring",
            "priority": "High",
            "complexity": "Medium"
        },
        {
            "name": "Create Log Analysis Agent for Server Claude",
            "description": "Implement agent for real-time log monitoring, error detection, and automated troubleshooting",
            "priority": "Medium",
            "complexity": "High"
        },
        {
            "name": "Create Backup & Recovery Agent for Server Claude",
            "description": "Design agent for automated backups, state snapshots, and disaster recovery procedures",
            "priority": "Medium",
            "complexity": "Medium"
        },
        {
            "name": "Create Performance Monitoring Agent for Server Claude",
            "description": "Build agent to track resource usage, identify bottlenecks, and optimize server performance",
            "priority": "Medium",
            "complexity": "Medium"
        }
    ]
    
    # Create rows for each task
    new_rows = []
    for i, task in enumerate(agent_tasks):
        task_id = f"CT-{next_num + i:03d}"
        row = [
            task_id,                          # Task ID
            task["name"],                     # Task Name
            "Implementation",                 # Task Type
            task["description"],              # Description
            "Server Claude",                  # Assigned To
            task["priority"],                 # Priority
            "Not Started",                    # Status
            "",                              # Start Date
            "",                              # End Date
            task["complexity"],               # Complexity
            "ADK, Python, Docker, SystemD",   # Tech Stack
            "",                              # Notes
            "No",                            # Is Blocked
            "",                              # Blocker Details
            "",                              # Completion %
            "Industrial IoT Stack",           # Project
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Created
        ]
        new_rows.append(row)
    
    # Append to sheet
    body = {
        'values': new_rows
    }
    
    result = service.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID,
        range="Claude Tasks!A:Q",
        valueInputOption="RAW",
        insertDataOption="INSERT_ROWS",
        body=body
    ).execute()
    
    print(f"Added {len(new_rows)} specialized agent tasks for Server Claude")
    print(f"Task IDs: CT-{next_num:03d} through CT-{next_num + len(agent_tasks) - 1:03d}")
    
    return result

def main():
    """Main execution"""
    print("Adding specialized agent tasks for Server Claude...")
    
    service = get_sheets_service()
    result = add_server_claude_agents(service)
    
    print("\nCompleted! Server Claude now has specialized agent tasks assigned.")
    print("\nGreat job Server Claude on completing CT-061! 🎉")
    print("Sleep well! Tomorrow Server Claude will have powerful agents to work with.")

if __name__ == "__main__":
    main()