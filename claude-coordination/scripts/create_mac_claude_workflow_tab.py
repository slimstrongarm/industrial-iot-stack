#!/usr/bin/env python3
"""
Create Mac Claude Workflow tab in Google Sheets for step-by-step progress tracking
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

def create_mac_claude_workflow_tab():
    """Create Mac Claude Workflow tab with step-by-step checklist"""
    
    # Configuration
    SPREADSHEET_ID = "1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do"
    CREDENTIALS_FILE = "/home/server/google-sheets-credentials.json"
    
    print("🍎 Creating Mac Claude Workflow Tab")
    print("=" * 40)
    
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
        new_sheet_title = "Mac Claude Workflow"
        
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
                                'rowCount': 50,
                                'columnCount': 7
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
        
        # Define Mac Claude workflow steps
        workflow_data = [
            # Header row
            ["Step", "Task", "Time Est.", "Status", "Priority", "Dependencies", "Notes/Details"],
            
            # Phase 1: Initial Setup & Verification
            ["MC-001", "Verify Repository Access", "2 min", "Pending", "Critical", "-", "Clone repo, verify read access to key files"],
            ["MC-002", "Test n8n API Connectivity", "2 min", "Pending", "Critical", "MC-001", "curl test with API key to verify Windows→Mac connectivity"],
            ["MC-003", "Review Project Status", "5 min", "Pending", "High", "MC-001", "Read STACK_CONFIG.md, N8N_INTEGRATION_COMPLETE.md"],
            
            # Phase 2: Immediate Human Tasks (Quick Wins)
            ["MC-004", "HT-002: Create Discord Webhooks", "5 min", "Pending", "High", "MC-002", "Create webhook URLs for #alerts, #logs, #general, #critical"],
            ["MC-005", "HT-003: Configure Google Sheets in n8n", "5 min", "Pending", "High", "MC-002", "Upload service account JSON to n8n credentials"],
            ["MC-006", "HT-006: Get Formbricks API Key", "10 min", "Pending", "Medium", "MC-002", "Login to Formbricks, create API key, update scripts"],
            
            # Phase 3: Integration & Testing
            ["MC-007", "Deploy Discord Integration", "10 min", "Pending", "High", "MC-004", "Update webhook URLs in scripts, test MQTT→Discord"],
            ["MC-008", "Test MQTT→Google Sheets Flow", "10 min", "Pending", "High", "MC-005", "Activate n8n workflow, test MQTT logging"],
            ["MC-009", "Complete CT-008 Integration Test", "20 min", "Pending", "High", "MC-007,MC-008", "End-to-end: Ignition→MQTT→n8n→Discord+Sheets"],
            
            # Phase 4: Coordination & Documentation
            ["MC-010", "Update Google Sheets Status", "5 min", "Pending", "Medium", "MC-009", "Mark completed tasks in Claude Tasks sheet"],
            ["MC-011", "Coordinate with Server Claude", "10 min", "Pending", "Medium", "MC-010", "Sync on next steps, remaining tasks"],
            ["MC-012", "Test Formbricks Integration", "15 min", "Pending", "Medium", "MC-006", "Activate Formbricks→Sheets workflow"],
            
            # Phase 5: Advanced Integration
            ["MC-013", "Node-RED MQTT Bridge Setup", "30 min", "Pending", "Low", "MC-009", "CT-010: Import MQTT Alert Bridge flow"],
            ["MC-014", "Node-RED n8n Command Bridge", "30 min", "Pending", "Low", "MC-013", "CT-011: Import n8n Command Bridge flow"],
            ["MC-015", "Full Stack Validation", "45 min", "Pending", "Medium", "MC-014", "Complete end-to-end system validation"],
            
            # Current Status Tracking
            ["", "", "", "", "", "", ""],
            ["STATUS", "CURRENT PHASE", "", "", "", "", ""],
            ["Started", datetime.now().strftime("%Y-%m-%d %H:%M"), "", "", "", "", "Mac Claude workflow initiated"],
            ["Phase 1", "Setup & Verification", "", "Ready", "", "", "Critical foundation steps"],
            ["Phase 2", "Human Tasks", "", "Ready", "", "", "Quick wins - 20 min total"],
            ["Phase 3", "Integration", "", "Blocked", "", "", "Waiting on Phase 2 completion"],
            ["Phase 4", "Coordination", "", "Blocked", "", "", "Waiting on Phase 3 completion"],
            ["Phase 5", "Advanced", "", "Future", "", "", "Long-term integration goals"],
            
            # Quick Reference
            ["", "", "", "", "", "", ""],
            ["QUICK REFERENCE", "", "", "", "", "", ""],
            ["n8n API URL", "http://172.28.214.170:5678/api/v1/", "", "", "", "", ""],
            ["API Key", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...", "", "", "", "", "See MAC_CLAUDE_QUICK_START.md for full key"],
            ["EMQX MQTT", "host.docker.internal:1883", "", "", "", "", "Use this from n8n workflows"],
            ["Discord Setup", "scripts/discord_webhook_integration.py", "", "", "", "", "Ready script waiting for webhook URLs"],
            ["Google Sheets", "Service account JSON needed in n8n", "", "", "", "", "Enables MQTT→Sheets logging"],
            
            # Success Criteria
            ["", "", "", "", "", "", ""],
            ["SUCCESS CRITERIA", "", "", "", "", "", ""],
            ["Immediate (30 min)", "MC-001 to MC-006 complete", "", "", "", "", "Foundation + 3 human tasks"],
            ["Short-term (2 hours)", "MC-001 to MC-009 complete", "", "", "", "", "Full integration working"],
            ["Complete (4 hours)", "All MC tasks complete", "", "", "", "", "Advanced integrations done"]
        ]
        
        # Write data to new sheet
        range_name = f"'{new_sheet_title}'!A1"
        body = {
            'values': workflow_data
        }
        
        result = service.spreadsheets().values().update(
            spreadsheetId=SPREADSHEET_ID,
            range=range_name,
            valueInputOption='RAW',
            body=body
        ).execute()
        
        print(f"✅ Created Mac Claude workflow with step-by-step guide")
        print(f"📊 {result.get('updatedCells')} cells updated")
        print(f"🎯 15 main workflow steps + status tracking")
        
        # Apply formatting
        sheet_id = None
        spreadsheet = service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID).execute()
        for sheet in spreadsheet['sheets']:
            if sheet['properties']['title'] == new_sheet_title:
                sheet_id = sheet['properties']['sheetId']
                break
        
        if sheet_id:
            # Format header row and section headers
            format_requests = [
                # Header row formatting
                {
                    'repeatCell': {
                        'range': {
                            'sheetId': sheet_id,
                            'startRowIndex': 0,
                            'endRowIndex': 1,
                            'startColumnIndex': 0,
                            'endColumnIndex': 7
                        },
                        'cell': {
                            'userEnteredFormat': {
                                'backgroundColor': {'red': 0.2, 'green': 0.6, 'blue': 1.0},
                                'textFormat': {'bold': True, 'foregroundColor': {'red': 1, 'green': 1, 'blue': 1}}
                            }
                        },
                        'fields': 'userEnteredFormat(backgroundColor,textFormat)'
                    }
                },
                # Critical priority highlighting
                {
                    'repeatCell': {
                        'range': {
                            'sheetId': sheet_id,
                            'startRowIndex': 1,
                            'endRowIndex': 4,
                            'startColumnIndex': 4,
                            'endColumnIndex': 5
                        },
                        'cell': {
                            'userEnteredFormat': {
                                'backgroundColor': {'red': 1.0, 'green': 0.8, 'blue': 0.8}
                            }
                        },
                        'fields': 'userEnteredFormat(backgroundColor)'
                    }
                }
            ]
            
            service.spreadsheets().batchUpdate(
                spreadsheetId=SPREADSHEET_ID,
                body={'requests': format_requests}
            ).execute()
            
            print("✅ Applied formatting to workflow tab")
        
        print(f"\n📋 Mac Claude Workflow Summary:")
        print(f"Sheet Name: {new_sheet_title}")
        print(f"Phase 1: Setup & Verification (4 steps, ~10 min)")
        print(f"Phase 2: Human Tasks (3 steps, ~20 min)")
        print(f"Phase 3: Integration & Testing (3 steps, ~40 min)")
        print(f"Phase 4: Coordination (2 steps, ~15 min)")
        print(f"Phase 5: Advanced Integration (3 steps, ~105 min)")
        
        print(f"\n🎯 Critical Path (30 minutes):")
        print("1. MC-001: Repository access")
        print("2. MC-002: n8n API test")
        print("3. MC-004: Discord webhooks")
        print("4. MC-005: Google Sheets config")
        print("5. MC-006: Formbricks API key")
        
        print(f"\n🚀 Next Steps for Mac Claude:")
        print("1. Open the 'Mac Claude Workflow' tab")
        print("2. Start with MC-001 (Repository Access)")
        print("3. Update Status column as you complete each step")
        print("4. Follow the dependency chain for optimal order")
        
        return True
        
    except HttpError as error:
        print(f"❌ Google Sheets API error: {error}")
        return False
    except Exception as error:
        print(f"❌ Unexpected error: {error}")
        return False

if __name__ == "__main__":
    success = create_mac_claude_workflow_tab()
    if success:
        print("\n🎉 Mac Claude Workflow tab created successfully!")
        print("Ready for Mac Claude to follow step-by-step progress!")
    else:
        print("\n📝 Failed to create Mac Claude Workflow tab")
        sys.exit(1)