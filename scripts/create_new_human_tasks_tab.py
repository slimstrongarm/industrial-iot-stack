#!/usr/bin/env python3
"""
Create a new Human Tasks tab with clean data and Claude task references
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime

# Add the scripts directory to Python path for imports
script_dir = Path(__file__).parent
sys.path.append(str(script_dir))

try:
    from google.oauth2.service_account import Credentials
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
except ImportError:
    print("❌ Google API libraries not installed")
    sys.exit(1)

def create_new_human_tasks_tab():
    """Create a new Human Tasks tab with clean data and Claude task dependencies"""
    
    # Configuration
    SPREADSHEET_ID = "1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do"
    CREDENTIALS_FILE = "/home/server/google-sheets-credentials.json"
    
    print("🆕 Creating New Human Tasks Tab")
    print("=" * 35)
    
    try:
        # Load credentials
        creds = Credentials.from_service_account_file(
            CREDENTIALS_FILE,
            scopes=['https://www.googleapis.com/auth/spreadsheets']
        )
        
        # Build service
        service = build('sheets', 'v4', credentials=creds)
        
        print("✅ Connected to Google Sheets API")
        
        # Create new sheet
        new_sheet_title = "Human Tasks (Clean)"
        
        # Check if sheet already exists
        spreadsheet = service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID).execute()
        existing_sheets = [sheet['properties']['title'] for sheet in spreadsheet['sheets']]
        
        if new_sheet_title in existing_sheets:
            print(f"⚠️  Sheet '{new_sheet_title}' already exists, will overwrite")
        else:
            # Create new sheet
            request_body = {
                'requests': [{
                    'addSheet': {
                        'properties': {
                            'title': new_sheet_title,
                            'gridProperties': {
                                'rowCount': 100,
                                'columnCount': 8
                            }
                        }
                    }
                }]
            }
            
            service.spreadsheets().batchUpdate(
                spreadsheetId=SPREADSHEET_ID,
                body=request_body
            ).execute()
            
            print(f"✅ Created new sheet: {new_sheet_title}")
        
        # Define clean human tasks with Claude task dependencies
        human_tasks = [
            # Header row
            ["ID", "Task", "Priority", "Time Required", "Status", "Assigned To", "Claude Task Dependency", "Description"],
            
            # Immediate high priority tasks (autonomous work completion)
            ["HT-001", "Update Claude Tasks Status", "High", "5 min", "Ready", "You", "CT-007, CT-013, CT-014, CT-016, CT-021", "Mark CT-007, CT-013, CT-014, CT-016, CT-021 as COMPLETED in Claude Tasks sheet"],
            ["HT-002", "Create Discord Webhooks", "High", "5 min", "Ready", "You", "CT-022", "Create webhook URLs for #alerts, #logs, #general, #critical channels in Discord server"],
            ["HT-003", "Configure n8n Google Sheets Credentials", "High", "5 min", "Ready", "You", "CT-008", "Upload service account JSON to n8n credentials for Google Sheets integration"],
            
            # Quick integration wins
            ["HT-004", "Deploy Discord Integration", "High", "10 min", "Ready", "You", "CT-022", "Update webhook URLs in scripts and test MQTT→Discord alert flow"],
            ["HT-005", "Test MQTT→Google Sheets Flow", "High", "10 min", "Ready", "You", "CT-008", "Activate n8n workflow and test MQTT logging to Google Sheets"],
            ["HT-006", "Get Formbricks API Key", "Medium", "10 min", "Ready", "You", "CT-019", "Login to Formbricks dashboard, create API key, update integration script"],
            
            # Development and installation tasks
            ["HT-007", "Install Ignition Scripts", "Medium", "30 min", "Ready", "Controls Engineer", "CT-016", "Import 3 Python scripts to Ignition project library for n8n integration"],
            ["HT-008", "Configure WhatsApp Business API", "Medium", "30 min", "Ready", "You", "CT-008", "Set up WhatsApp Business API or configure webhook.site for testing alerts"],
            ["HT-009", "Complete End-to-End Integration Test", "High", "20 min", "Pending", "Both", "CT-008, CT-022", "Test complete pipeline: Ignition→MQTT→n8n→Discord+Google Sheets"],
            
            # Coordination and documentation
            ["HT-010", "Sync with Mac Claude on Discord Bot", "Medium", "15 min", "Pending", "Both", "CT-022", "Coordinate Discord bot vs webhook approach with Mac Claude"],
            ["HT-011", "Update IIOT Master Sheet Status", "Low", "10 min", "Ready", "You", "-", "Update System Components Status with current integration progress"],
            
            # Original system tasks (preserved from existing sheet)
            ["HT-012", "Architecture Documentation", "High", "60 min", "Complete", "Architect", "-", "Set up comprehensive documentation system with status tracking"],
            ["HT-013", "Create Ignition Project Structure", "High", "90 min", "Complete", "Controls Engineer", "-", "Create Ignition project structure and organization for optimal performance"],
            ["HT-014", "Test Individual Components", "Medium", "45 min", "Complete", "Both", "-", "Test individual system components before integration"],
            ["HT-015", "Network Architecture Documentation", "Medium", "30 min", "Complete", "Architect", "-", "Create network architecture documentation for equipment connectivity"],
            ["HT-016", "Design Integration Architecture", "High", "120 min", "Complete", "Architect", "-", "Design integration architecture between Ignition, Node-RED, and data systems"],
            ["HT-017", "Set Up Test Environment", "Medium", "60 min", "Complete", "Controls Engineer", "-", "Set up test environment with simulated equipment for development"],
            ["HT-018", "Configure Network Communication", "High", "90 min", "Complete", "Architect", "-", "Configure secure network communication between all stack components"],
            ["HT-019", "Establish Data Flow Patterns", "High", "75 min", "Complete", "Architect", "-", "Establish data flow patterns between Ignition Edge, Node-RED, and cloud services"],
            ["HT-020", "Validate System Performance", "High", "60 min", "Complete", "Both", "-", "Validate system performance under various load conditions"],
            ["HT-021", "Create Deployment Guides", "Medium", "45 min", "Complete", "Architect", "-", "Create deployment guides and operational procedures"],
            ["HT-022", "Deploy to Production", "High", "120 min", "Complete", "Controls Engineer", "-", "Deploy system to production environment with monitoring"],
            ["HT-023", "Monitor and Optimize", "Medium", "Ongoing", "Complete", "Both", "-", "Monitor and optimize system performance based on real-world usage"],
            ["HT-024", "Document Lessons Learned", "Low", "30 min", "Complete", "You", "-", "Document lessons learned and best practices for future projects"],
            ["HT-025", "Establish Maintenance Schedules", "Low", "45 min", "Complete", "Both", "-", "Establish maintenance schedules and update procedures"],
            ["HT-026", "Train Operators", "Medium", "180 min", "Complete", "Both", "-", "Train operators on system usage and basic troubleshooting"],
            ["HT-027", "Ensure Compliance", "Medium", "90 min", "Complete", "You", "-", "Ensure system meets industry standards and regulatory requirements"],
            ["HT-028", "Implement Backup Procedures", "High", "120 min", "Complete", "Both", "-", "Implement comprehensive backup and disaster recovery procedures"],
            ["HT-029", "Implement Security", "High", "150 min", "Complete", "You", "-", "Implement security best practices and access controls"],
            ["HT-030", "Set Up System Monitoring", "High", "90 min", "Complete", "Both", "-", "Set up comprehensive system monitoring and alerting"]
        ]
        
        # Write data to new sheet
        range_name = f"'{new_sheet_title}'!A1"
        body = {
            'values': human_tasks
        }
        
        result = service.spreadsheets().values().update(
            spreadsheetId=SPREADSHEET_ID,
            range=range_name,
            valueInputOption='RAW',
            body=body
        ).execute()
        
        print(f"✅ Created new Human Tasks tab with clean data")
        print(f"📊 {result.get('updatedCells')} cells updated")
        print(f"🎯 30 tasks with proper HT-001 through HT-030 IDs")
        
        # Apply basic formatting
        sheet_id = None
        spreadsheet = service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID).execute()
        for sheet in spreadsheet['sheets']:
            if sheet['properties']['title'] == new_sheet_title:
                sheet_id = sheet['properties']['sheetId']
                break
        
        if sheet_id:
            # Format header row
            format_requests = [
                {
                    'repeatCell': {
                        'range': {
                            'sheetId': sheet_id,
                            'startRowIndex': 0,
                            'endRowIndex': 1,
                            'startColumnIndex': 0,
                            'endColumnIndex': 8
                        },
                        'cell': {
                            'userEnteredFormat': {
                                'backgroundColor': {'red': 0.9, 'green': 0.9, 'blue': 0.9},
                                'textFormat': {'bold': True}
                            }
                        },
                        'fields': 'userEnteredFormat(backgroundColor,textFormat)'
                    }
                }
            ]
            
            service.spreadsheets().batchUpdate(
                spreadsheetId=SPREADSHEET_ID,
                body={'requests': format_requests}
            ).execute()
            
            print("✅ Applied header formatting")
        
        print(f"\n📋 New Sheet Summary:")
        print(f"Sheet Name: {new_sheet_title}")
        print(f"Total Tasks: 30 (HT-001 to HT-030)")
        print(f"Immediate Actions: 11 tasks (HT-001 to HT-011)")
        print(f"Completed Tasks: 19 tasks (HT-012 to HT-030)")
        
        print(f"\n🎯 Claude Task Dependencies:")
        print("• HT-001: Update status for CT-007, CT-013, CT-014, CT-016, CT-021")
        print("• HT-002, HT-004, HT-010: Waiting on CT-022 (Discord Integration)")
        print("• HT-003, HT-005, HT-008, HT-009: Waiting on CT-008 (MQTT Integration)")
        print("• HT-006: Waiting on CT-019 (Formbricks API)")
        print("• HT-007: Waiting on CT-016 (Ignition Scripts)")
        
        print(f"\n🚀 Next Steps:")
        print("1. Review the new 'Human Tasks (Clean)' tab")
        print("2. Start with HT-001 (update Claude task status)")
        print("3. Work through HT-002 to HT-006 for immediate wins")
        print("4. The Claude task dependencies show what's blocking each human task")
        
        return True
        
    except HttpError as error:
        print(f"❌ Google Sheets API error: {error}")
        return False
    except Exception as error:
        print(f"❌ Unexpected error: {error}")
        return False

if __name__ == "__main__":
    success = create_new_human_tasks_tab()
    if success:
        print("\n🎉 New Human Tasks tab created successfully!")
        print("Clean data with proper Claude task dependencies is ready!")
    else:
        print("\n📝 Failed to create new Human Tasks tab")
        sys.exit(1)