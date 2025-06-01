#!/usr/bin/env python3
"""
Claude Approval System - Streamlined approval workflow for Docker migration
This creates approval requests in Google Sheets that you can approve from anywhere
"""

import os
import json
import time
from datetime import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Configuration
SPREADSHEET_ID = '1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do'
CREDENTIALS_FILE = os.path.expanduser('~/Desktop/industrial-iot-stack/credentials/iot-stack-credentials.json')

class ApprovalSystem:
    def __init__(self):
        self.service = self.get_sheets_service()
        self.approval_sheet = 'Claude Approvals'
        self.setup_approval_tab()
    
    def get_sheets_service(self):
        """Initialize Google Sheets API service."""
        credentials = service_account.Credentials.from_service_account_file(
            CREDENTIALS_FILE,
            scopes=['https://www.googleapis.com/auth/spreadsheets']
        )
        return build('sheets', 'v4', credentials=credentials)
    
    def setup_approval_tab(self):
        """Create Claude Approvals tab if it doesn't exist."""
        try:
            # Check if tab exists
            sheet_metadata = self.service.spreadsheets().get(
                spreadsheetId=SPREADSHEET_ID
            ).execute()
            
            sheets = sheet_metadata.get('sheets', [])
            tab_exists = any(s['properties']['title'] == self.approval_sheet for s in sheets)
            
            if not tab_exists:
                # Create new sheet
                request_body = {
                    'requests': [{
                        'addSheet': {
                            'properties': {
                                'title': self.approval_sheet,
                                'gridProperties': {
                                    'rowCount': 100,
                                    'columnCount': 7,
                                    'frozenRowCount': 1
                                }
                            }
                        }
                    }]
                }
                
                self.service.spreadsheets().batchUpdate(
                    spreadsheetId=SPREADSHEET_ID,
                    body=request_body
                ).execute()
                
                # Add headers
                headers = [['Request ID', 'Type', 'Description', 'Status', 'Your Response', 'Requested At', 'Responded At']]
                self.service.spreadsheets().values().update(
                    spreadsheetId=SPREADSHEET_ID,
                    range=f'{self.approval_sheet}!A1:G1',
                    valueInputOption='USER_ENTERED',
                    body={'values': headers}
                ).execute()
                
                print(f"✅ Created {self.approval_sheet} tab")
            
        except Exception as e:
            print(f"Error setting up approval tab: {str(e)}")
    
    def request_approval(self, approval_type, description, options=None):
        """Create an approval request and wait for response."""
        request_id = f"REQ-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        
        # Add to sheet
        row_data = [[
            request_id,
            approval_type,
            description,
            'PENDING',
            f"Options: {', '.join(options) if options else 'YES/NO'}",
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            ''
        ]]
        
        self.service.spreadsheets().values().append(
            spreadsheetId=SPREADSHEET_ID,
            range=f'{self.approval_sheet}!A:G',
            valueInputOption='USER_ENTERED',
            body={'values': row_data}
        ).execute()
        
        print(f"\n🔔 APPROVAL REQUIRED: {approval_type}")
        print(f"📝 {description}")
        print(f"📊 Check Google Sheets: https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}")
        print(f"⏳ Waiting for your response in column E...")
        
        # Wait for response
        while True:
            time.sleep(5)  # Check every 5 seconds
            
            # Get all values
            result = self.service.spreadsheets().values().get(
                spreadsheetId=SPREADSHEET_ID,
                range=f'{self.approval_sheet}!A:G'
            ).execute()
            
            values = result.get('values', [])
            
            # Find our request
            for i, row in enumerate(values):
                if len(row) > 0 and row[0] == request_id:
                    if len(row) > 4 and row[4] and row[4] not in ['Options: YES/NO', f"Options: {', '.join(options) if options else 'YES/NO'}"]:
                        # Got response!
                        response = row[4]
                        
                        # Update status
                        self.service.spreadsheets().values().update(
                            spreadsheetId=SPREADSHEET_ID,
                            range=f'{self.approval_sheet}!D{i+1}:G{i+1}',
                            valueInputOption='USER_ENTERED',
                            body={'values': [['APPROVED', response, '', datetime.now().strftime('%Y-%m-%d %H:%M:%S')]]}
                        ).execute()
                        
                        print(f"✅ Received approval: {response}")
                        return response
    
    def quick_decision(self, decision_type, context):
        """Request a quick YES/NO decision."""
        return self.request_approval(decision_type, context, ['YES', 'NO'])
    
    def multi_choice(self, decision_type, context, options):
        """Request a multiple choice decision."""
        return self.request_approval(decision_type, context, options)

# Example approval scenarios for Docker migration
def docker_migration_approvals():
    approval = ApprovalSystem()
    
    # Example 1: Network subnet approval
    subnet_choice = approval.multi_choice(
        "Docker Network Configuration",
        "Choose subnet for Docker services (current proposal: 172.20.0.0/16)",
        ["172.20.0.0/16", "10.100.0.0/16", "192.168.100.0/24", "CUSTOM"]
    )
    
    # Example 2: Quick decision
    proceed = approval.quick_decision(
        "Proceed with Deployment",
        "Ready to deploy Docker containers to server. Server health checks passed. Proceed?"
    )
    
    if proceed == "YES":
        print("🚀 Proceeding with deployment...")
    else:
        print("🛑 Deployment paused")
    
    # Example 3: Service configuration
    ignition_config = approval.multi_choice(
        "Ignition Configuration",
        "Select Ignition deployment mode",
        ["Standard (8GB RAM)", "Minimal (4GB RAM)", "Development (2GB RAM)"]
    )
    
    return {
        'subnet': subnet_choice,
        'proceed': proceed,
        'ignition_mode': ignition_config
    }

if __name__ == "__main__":
    # Demo the approval system
    print("🎯 Claude Approval System Demo")
    print("This shows how Claude can request approvals via Google Sheets\n")
    
    approval = ApprovalSystem()
    
    # Simple test
    response = approval.quick_decision(
        "Test Approval",
        "This is a test approval request. Reply YES or NO in column E"
    )
    
    print(f"\nYou responded: {response}")
    print("\n✅ Approval system is working! Use this for critical migration decisions.")