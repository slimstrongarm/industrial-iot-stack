#!/usr/bin/env python3
"""
Update CT-055 status to completed in Google Sheets
Mac Claude has completed documentation updates for Discord deployment
"""

from googleapiclient.discovery import build
from google.oauth2 import service_account
import json
from datetime import datetime
import os

# Configuration from existing setup
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'credentials/iot-stack-credentials.json'
SPREADSHEET_ID = '1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do'

def update_ct055_status():
    """Update CT-055 from Pending to Complete with completion details"""
    
    try:
        # Load credentials using existing setup
        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        
        service = build('sheets', 'v4', credentials=credentials)
        sheet = service.spreadsheets()
        
        # Get all data to find CT-055
        result = sheet.values().get(
            spreadsheetId=SPREADSHEET_ID,
            range='Claude Tasks!A:J'
        ).execute()
        
        values = result.get('values', [])
        ct055_row = None
        
        # Find CT-055 row
        for i, row in enumerate(values):
            if len(row) > 0 and row[0] == 'CT-055':
                ct055_row = i + 1  # Sheet rows are 1-indexed
                break
        
        if not ct055_row:
            print("❌ CT-055 not found in sheet")
            return False
        
        print(f"📍 Found CT-055 at row {ct055_row}")
        
        # Update Status (column E) and Completed (column J)
        completion_time = datetime.now().strftime('%Y-%m-%d %H:%M')
        
        # Update status to Complete
        sheet.values().update(
            spreadsheetId=SPREADSHEET_ID,
            range=f'Claude Tasks!E{ct055_row}',
            valueInputOption='USER_ENTERED',
            body={'values': [['Complete']]}
        ).execute()
        
        # Update completion time
        sheet.values().update(
            spreadsheetId=SPREADSHEET_ID,
            range=f'Claude Tasks!J{ct055_row}',
            valueInputOption='USER_ENTERED',
            body={'values': [[completion_time]]}
        ).execute()
        
        # Update Expected Output with what was actually completed
        completed_output = """✅ Documentation updated with Discord deployment capabilities:
• INDEX.md - Added persistent deployment section with Docker containers
• CLAUDE.md - Enhanced with Discord automation as PRIMARY WORKFLOW  
• SERVER_CLAUDE_DISCORD_INSTRUCTIONS.md - Complete deployment guide
• Created unified monitoring strategy and implementation files
• Added 10 unified monitoring tasks (CT-056 to CT-065) for rollout"""
        
        sheet.values().update(
            spreadsheetId=SPREADSHEET_ID,
            range=f'Claude Tasks!G{ct055_row}',
            valueInputOption='USER_ENTERED',
            body={'values': [[completed_output]]}
        ).execute()
        
        print(f"✅ Successfully updated CT-055 to Complete!")
        print(f"📅 Completion time: {completion_time}")
        print(f"🔗 View at: https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}")
        
        print("\n📋 CT-055 Documentation Updates Completed:")
        print("  ✅ INDEX.md - Added Discord deployment sections")
        print("  ✅ CLAUDE.md - Updated with Discord automation workflow")
        print("  ✅ SERVER_CLAUDE_DISCORD_INSTRUCTIONS.md - Created deployment guide")
        print("  ✅ UNIFIED_MONITORING_STRATEGY.md - New monitoring strategy")
        print("  ✅ unified_industrial_monitor.py - Complete monitoring solution")
        print("  ✅ Added CT-056 to CT-065 - Unified monitoring rollout tasks")
        
        return True
        
    except FileNotFoundError:
        print(f"❌ Credentials file not found: {SERVICE_ACCOUNT_FILE}")
        return False
    except Exception as e:
        print(f"❌ Error updating CT-055: {e}")
        return False

def verify_ct055_update():
    """Verify CT-055 was successfully updated"""
    try:
        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        
        service = build('sheets', 'v4', credentials=credentials)
        sheet = service.spreadsheets()
        
        # Get CT-055 data
        result = sheet.values().get(
            spreadsheetId=SPREADSHEET_ID,
            range='Claude Tasks!A:J'
        ).execute()
        
        values = result.get('values', [])
        
        for row in values:
            if len(row) > 0 and row[0] == 'CT-055':
                task_id = row[0]
                instance = row[1] if len(row) > 1 else 'N/A'
                status = row[4] if len(row) > 4 else 'N/A'
                completed = row[9] if len(row) > 9 else 'N/A'
                
                print(f"\n✅ Verification: CT-055 status updated")
                print(f"  Task: {task_id} (Mac Claude)")
                print(f"  Status: {status}")
                print(f"  Completed: {completed}")
                
                return status == 'Complete'
        
        print("❌ CT-055 not found for verification")
        return False
        
    except Exception as e:
        print(f"❌ Verification error: {e}")
        return False

if __name__ == "__main__":
    print("📝 Updating CT-055 Documentation Update Task...")
    print("==============================================")
    
    # Check if credentials file exists
    if not os.path.exists(SERVICE_ACCOUNT_FILE):
        print(f"❌ Credentials file not found at: {SERVICE_ACCOUNT_FILE}")
        exit(1)
    
    # Update CT-055
    success = update_ct055_status()
    
    if success:
        print("\n🔍 Verifying update...")
        verify_ct055_update()
        print("\n🎉 CT-055 successfully marked as completed!")
        print("Mac Claude's Discord deployment documentation work is now reflected in Google Sheets.")
    else:
        print("\n❌ Failed to update CT-055")
        print("Please check credentials and try again.")