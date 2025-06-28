#!/usr/bin/env python3
"""
Update Claude Tasks in Google Sheets with latest n8n deployment status
"""

from googleapiclient.discovery import build
from google.oauth2 import service_account
from datetime import datetime

# Configuration
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'credentials/iot-stack-credentials.json'
SPREADSHEET_ID = '1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do'
SHEET_NAME = 'Claude Tasks'

def get_sheets_service():
    """Initialize Google Sheets service"""
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=credentials)
    return service.spreadsheets()

def update_claude_tasks():
    """Update Claude Tasks sheet with n8n deployment progress"""
    try:
        sheet = get_sheets_service()
        
        # Get current data to find the right rows
        result = sheet.values().get(
            spreadsheetId=SPREADSHEET_ID,
            range=f'{SHEET_NAME}!A:J'
        ).execute()
        
        values = result.get('values', [])
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M')
        
        # Find and update CT-005 to Complete
        updates = []
        ct005_found = False
        last_row = len(values)
        
        for i, row in enumerate(values):
            if i == 0:  # Skip header
                continue
            if len(row) > 0 and row[0] == 'CT-005':
                # Update CT-005 status to Complete
                updates.append({
                    'range': f'{SHEET_NAME}!E{i+1}',  # Status column
                    'values': [['Complete']]
                })
                updates.append({
                    'range': f'{SHEET_NAME}!J{i+1}',  # Completed column
                    'values': [[current_time]]
                })
                ct005_found = True
                print(f"✅ Updated CT-005 to Complete")
                break
        
        if not ct005_found:
            print("❌ CT-005 not found in sheet")
            return False
        
        # Add new tasks for Server Claude
        new_tasks = [
            ['CT-006', 'Server Claude', 'n8n Deployment', 'High', 'Pending', 
             'Deploy complete n8n stack with PostgreSQL using ./scripts/deploy_n8n_stack.sh', 
             'n8n operational at localhost:5678 with PostgreSQL backend', 'CT-005', current_time, ''],
            ['CT-007', 'Server Claude', 'Workflow Import', 'High', 'Pending',
             'Import both n8n workflows: Formbricks→Sheets and MQTT→WhatsApp alerts',
             'Both workflows imported and activated in n8n interface', 'CT-006', current_time, ''],
            ['CT-008', 'Server Claude', 'Integration Test', 'Medium', 'Pending',
             'Test MQTT→WhatsApp alert workflow with sample equipment data',
             'WhatsApp alert successfully sent and logged to Google Sheets', 'CT-007', current_time, ''],
            ['CT-009', 'Mac Claude', 'Repository Commit', 'Medium', 'Complete',
             'Commit all n8n deployment files to Git repository',
             'All files committed and pushed to GitHub main branch', 'CT-005', current_time, current_time]
        ]
        
        # Add new tasks starting from the next available row
        for i, task in enumerate(new_tasks):
            row_num = last_row + 1 + i
            updates.append({
                'range': f'{SHEET_NAME}!A{row_num}:J{row_num}',
                'values': [task]
            })
        
        # Execute all updates
        if updates:
            batch_update_request = {
                'valueInputOption': 'RAW',
                'data': updates
            }
            
            sheet.values().batchUpdate(
                spreadsheetId=SPREADSHEET_ID,
                body=batch_update_request
            ).execute()
            
            print(f"✅ Successfully updated Claude Tasks sheet!")
            print(f"   • CT-005 marked as Complete")
            print(f"   • Added {len(new_tasks)} new tasks for Server Claude")
            print(f"   • CT-009 (Repository Commit) already marked Complete")
            
            print("\n📋 New Tasks Added:")
            for task in new_tasks:
                status_icon = "✅" if task[4] == "Complete" else "⏳"
                print(f"   {status_icon} {task[0]} ({task[1]}): {task[5][:60]}...")
            
            return True
        else:
            print("❌ No updates to make")
            return False
            
    except Exception as e:
        print(f"❌ Error updating Google Sheets: {e}")
        return False

def show_current_status():
    """Display current Claude Tasks status"""
    try:
        sheet = get_sheets_service()
        
        result = sheet.values().get(
            spreadsheetId=SPREADSHEET_ID,
            range=f'{SHEET_NAME}!A:J'
        ).execute()
        
        values = result.get('values', [])
        
        print("\n📊 Current Claude Tasks Status:")
        print("=" * 80)
        
        for i, row in enumerate(values):
            if i == 0:  # Header
                continue
            if len(row) >= 5:
                task_id = row[0]
                instance = row[1]
                task_type = row[2]
                status = row[4]
                description = row[5] if len(row) > 5 else ''
                
                status_icon = "✅" if status == "Complete" else "⏳" if status == "Pending" else "🔄"
                
                print(f"{status_icon} {task_id} ({instance}): {status}")
                print(f"   Type: {task_type}")
                print(f"   Task: {description[:70]}...")
                print()
        
    except Exception as e:
        print(f"❌ Error reading current status: {e}")

if __name__ == "__main__":
    print("🔄 Updating Claude Tasks with n8n deployment status...")
    
    # Show current status first
    show_current_status()
    
    # Update the sheet
    if update_claude_tasks():
        print("\n" + "="*80)
        print("🎉 Claude Tasks sheet successfully updated!")
        print("🚀 Server Claude can now see the deployment package is ready")
        print("📱 MQTT→WhatsApp workflow ready for import and testing")
    else:
        print("\n❌ Failed to update Claude Tasks sheet")