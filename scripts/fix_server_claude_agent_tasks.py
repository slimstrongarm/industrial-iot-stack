#!/usr/bin/env python3
"""Fix the column alignment for Server Claude agent tasks in Google Sheets"""

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

def fix_agent_tasks(service):
    """Fix the misaligned Server Claude agent tasks"""
    
    # First, let's read the current data to see what we need to fix
    result = service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID,
        range="Claude Tasks!A76:G80"
    ).execute()
    
    current_data = result.get('values', [])
    print("Current misaligned data:")
    for row in current_data:
        print(row)
    
    # Correct format based on the screenshot:
    # Task ID | Instance | Task Type | Priority | Status | Description | Expected Output
    corrected_tasks = [
        [
            "CT-076",
            "Server Claude", 
            "Implementation",
            "High",
            "Not Started",
            "Create Docker Management Agent for Server Claude",
            "Build specialized agent to handle Docker container operations, health checks, and deployments"
        ],
        [
            "CT-077",
            "Server Claude",
            "Implementation", 
            "High",
            "Not Started",
            "Create SystemD Service Agent for Server Claude",
            "Develop agent for managing persistent services, auto-restart policies, and service monitoring"
        ],
        [
            "CT-078",
            "Server Claude",
            "Implementation",
            "Medium", 
            "Not Started",
            "Create Log Analysis Agent for Server Claude",
            "Implement agent for real-time log monitoring, error detection, and automated troubleshooting"
        ],
        [
            "CT-079",
            "Server Claude",
            "Implementation",
            "Medium",
            "Not Started", 
            "Create Backup & Recovery Agent for Server Claude",
            "Design agent for automated backups, state snapshots, and disaster recovery procedures"
        ],
        [
            "CT-080",
            "Server Claude",
            "Implementation",
            "Medium",
            "Not Started",
            "Create Performance Monitoring Agent for Server Claude", 
            "Build agent to track resource usage, identify bottlenecks, and optimize server performance"
        ]
    ]
    
    # Update the rows
    body = {
        'values': corrected_tasks
    }
    
    result = service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID,
        range="Claude Tasks!A76:G80",
        valueInputOption="RAW",
        body=body
    ).execute()
    
    print("\nFixed alignment for CT-076 through CT-080!")
    print("All Server Claude agent tasks now have correct column formatting.")
    
    return result

def main():
    """Main execution"""
    print("Fixing Server Claude agent task alignment...")
    
    service = get_sheets_service()
    fix_agent_tasks(service)
    
    print("\nCompleted! Server Claude's specialized agent tasks are now properly formatted.")

if __name__ == "__main__":
    main()