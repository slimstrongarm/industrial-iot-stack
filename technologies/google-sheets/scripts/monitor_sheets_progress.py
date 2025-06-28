#!/usr/bin/env python3
"""
Monitor Google Sheets for Server Claude progress
"""

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pathlib import Path
from datetime import datetime
import time

# Configuration
SHEET_ID = '1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do'
CREDS_FILE = str(Path.home() / 'Desktop/industrial-iot-stack/credentials/iot-stack-credentials.json')

def monitor_progress():
    """Monitor sheets for updates from Server Claude"""
    try:
        # Connect to Google Sheets
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_FILE, scope)
        client = gspread.authorize(creds)
        sheet = client.open_by_key(SHEET_ID)
        
        print("👀 Monitoring Google Sheets for updates...")
        print("=" * 50)
        
        # Check Agent Activities for recent Server Claude updates
        agent_sheet = sheet.worksheet('Agent Activities')
        all_activities = agent_sheet.get_all_values()
        
        # Get last 5 activities
        recent_activities = all_activities[-5:] if len(all_activities) > 5 else all_activities[1:]
        
        print("\n📊 Recent Agent Activities:")
        for activity in recent_activities:
            if len(activity) >= 3:
                timestamp = activity[0]
                agent = activity[1]
                task = activity[2]
                status = activity[3] if len(activity) > 3 else "Unknown"
                print(f"  [{timestamp}] {agent}: {task} - {status}")
        
        # Check Claude Approvals for pending items
        approval_sheet = sheet.worksheet('Claude Approvals')
        approvals = approval_sheet.get_all_values()
        
        pending_approvals = [row for row in approvals[1:] if len(row) > 3 and row[3] == 'PENDING']
        
        if pending_approvals:
            print(f"\n⚠️  Pending Approvals: {len(pending_approvals)}")
            for approval in pending_approvals:
                print(f"  - {approval[1]}: {approval[2]}")
        else:
            print("\n✅ No pending approvals")
            
        # Check Form Submissions
        try:
            form_sheet = sheet.worksheet('Form Submissions')
            form_count = len(form_sheet.get_all_values()) - 1  # Exclude header
            print(f"\n📝 Form Submissions: {form_count} total")
        except:
            pass
            
        # Check Dashboard for last update
        dashboard = sheet.worksheet('Dashboard')
        last_update = dashboard.cell(13, 2).value
        print(f"\n🕐 Dashboard Last Updated: {last_update}")
        
        print("\n" + "=" * 50)
        print("Monitoring complete. Check sheets for details.")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    monitor_progress()