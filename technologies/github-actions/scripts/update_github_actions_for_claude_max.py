#!/usr/bin/env python3
"""
Update GitHub Actions task to reflect Claude Max approach
"""

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pathlib import Path
from datetime import datetime

# Configuration
SHEET_ID = '1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do'
CREDS_FILE = str(Path.home() / 'Desktop/industrial-iot-stack/credentials/iot-stack-credentials.json')

def update_github_actions_task():
    """Update CT-030 to reflect Claude Max approach"""
    try:
        # Connect to Google Sheets
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_FILE, scope)
        client = gspread.authorize(creds)
        sheet = client.open_by_key(SHEET_ID)
        
        claude_sheet = sheet.worksheet('Claude Tasks')
        records = claude_sheet.get_all_records()
        
        # Find CT-030
        for i, record in enumerate(records):
            if record.get('Task ID') == 'CT-030':
                row_num = i + 2
                
                # Update description for Claude Max approach
                new_description = (
                    "Setup GitHub Actions with Claude Max integration (no API costs). "
                    "GitHub Actions prepares context, creates tasks, you execute with existing Claude Max subscription."
                )
                claude_sheet.update_cell(row_num, 6, new_description)
                
                # Update expected output
                new_output = (
                    "GitHub Actions workflow configured for Claude Max integration. "
                    "Automated context preparation, task creation, Google Sheets integration, "
                    "Discord notifications. Uses existing Claude Max subscription - no API costs."
                )
                claude_sheet.update_cell(row_num, 7, new_output)
                
                print("✅ Updated CT-030 for Claude Max approach")
                break
        
        # Add new Human Task for Claude Max sessions
        human_sheet = sheet.worksheet('Human Tasks')
        human_sheet.append_row([
            "HT-006",
            "Execute Claude Max automation sessions", 
            "Ongoing",
            "Medium",
            "Josh",
            datetime.now().strftime("%Y-%m-%d"),
            "-",
            "0%",
            "Execute automation tasks prepared by GitHub Actions using Claude Max subscription. Check GitHub issues daily for ready sessions.",
            "-",
            "Claude Max subscription"
        ])
        
        # Log activity
        agent_sheet = sheet.worksheet('Agent Activities')
        agent_sheet.append_row([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Mac Claude",
            "Updated GitHub Actions for Claude Max",
            "Complete",
            "30 min",
            "Modified automation to use Claude Max subscription instead of API. Added context preparation, GitHub issue creation, and manual execution workflow.",
            "No additional costs - leverages existing Claude Max subscription"
        ])
        
        print("\n🎯 Claude Max Integration Benefits:")
        print("   💰 No additional API costs")
        print("   🧠 Better context understanding")
        print("   🎛️ Interactive control and iteration")
        print("   🔄 Flexible execution timing")
        print("   📋 Automated context preparation")
        
        print("\n📋 How it works:")
        print("   1. GitHub Actions prepares context and creates task")
        print("   2. You get notified via Discord/GitHub issue")
        print("   3. Download context files from GitHub artifacts")
        print("   4. Execute task using Claude Max")
        print("   5. Update Google Sheets with results")
        
        print("\n✅ Ready to use your existing Claude Max subscription for automation!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    update_github_actions_task()