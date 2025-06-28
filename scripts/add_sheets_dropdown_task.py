#!/usr/bin/env python3
"""Add Google Sheets dropdown validation task"""

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

def add_dropdown_validation_task(service):
    """Add task for implementing status dropdown in Google Sheets"""
    
    # Create Google Sheets agent task
    sheets_task = [[
        "CT-083",
        "Mac Claude",
        "Sheets Status Dropdown",
        "High",
        "Not Started",
        "Implement data validation dropdown for Status column (E) in Claude Tasks sheet. Options: Not Started, Pending, In Progress, Complete, Blocked. Apply to entire column E starting from row 2. Ensure existing statuses remain unchanged.",
        "Google Sheets with enforced dropdown validation on Status column containing exactly these options: Not Started, Pending, In Progress, Complete, Blocked. All future status entries restricted to these values only."
    ]]
    
    # Append to sheet
    body = {
        'values': sheets_task
    }
    
    result = service.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID,
        range="Claude Tasks!A:G",
        valueInputOption="RAW",
        insertDataOption="INSERT_ROWS",
        body=body
    ).execute()
    
    print("✅ Added CT-083: Google Sheets Status Dropdown Implementation!")
    
    # Add architecture clarification note
    clarification = [[
        "ARCH-001",
        "System",
        "Architecture Hierarchy",
        "Critical",
        "Complete",
        "System Architecture Hierarchy Defined: Josh (The Architect/Visionary) → Mac Claude (Senior Coordinator) → Server Claude (Junior Coordinator). Josh makes all final decisions and sets the vision. Mac Claude orchestrates implementation. Server Claude dominates server operations domain.",
        "Clear hierarchy established and documented for all Claude instances to reference."
    ]]
    
    body = {
        'values': clarification
    }
    
    service.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID,
        range="Claude Tasks!A:G",
        valueInputOption="RAW",
        insertDataOption="INSERT_ROWS",
        body=body
    ).execute()
    
    print("✅ Added ARCH-001: Architecture Hierarchy Clarification!")
    
    return result

def main():
    """Main execution"""
    print("Adding Google Sheets dropdown task and architecture clarification...\n")
    
    service = get_sheets_service()
    add_dropdown_validation_task(service)
    
    print("\n🏗️ Architecture Hierarchy:")
    print("1. Josh Payne - The Architect (Visionary & Final Decision Maker)")
    print("2. Mac Claude - Senior Coordinator (Implementation Orchestrator)")
    print("3. Server Claude - Junior Coordinator (Server Domain Specialist)")
    print("\n✅ Ready to implement Sheets dropdown validation!")

if __name__ == "__main__":
    main()