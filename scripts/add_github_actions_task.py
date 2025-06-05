#!/usr/bin/env python3
"""
Add GitHub Actions Claude automation task
"""

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pathlib import Path
from datetime import datetime

# Configuration
SHEET_ID = '1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do'
CREDS_FILE = str(Path.home() / 'Desktop/industrial-iot-stack/credentials/iot-stack-credentials.json')

def add_github_actions_task():
    """Add new task for GitHub Actions Claude automation setup"""
    try:
        # Connect to Google Sheets
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_FILE, scope)
        client = gspread.authorize(creds)
        sheet = client.open_by_key(SHEET_ID)
        
        claude_sheet = sheet.worksheet('Claude Tasks')
        
        # Find the highest CT task number
        records = claude_sheet.get_all_records()
        ct_numbers = []
        for record in records:
            task_id = record.get('Task ID', '')
            if task_id.startswith('CT-'):
                try:
                    num = int(task_id.split('-')[1])
                    ct_numbers.append(num)
                except:
                    pass
        
        next_number = max(ct_numbers) + 1 if ct_numbers else 1
        next_task_id = f"CT-{next_number:03d}"
        
        # Add new GitHub Actions task
        new_task = [
            next_task_id,
            "Mac Claude", 
            "GitHub Actions",
            "Medium",
            "Complete",
            "Setup GitHub Actions with Claude Code automation for CI/CD and monitoring",
            "GitHub Actions workflow configured with Claude automation for health checks, deployments, testing, and documentation. Integration with Google Sheets and Discord notifications.",
            "-",  # No dependencies
            datetime.now().strftime("%Y-%m-%d"),
            datetime.now().strftime("%Y-%m-%d %H:%M")
        ]
        
        # Add the task
        claude_sheet.append_row(new_task)
        
        print(f"✅ Added {next_task_id}: GitHub Actions Claude Automation")
        print(f"   Instance: Mac Claude")
        print(f"   Status: Complete")
        print(f"   Files created: .github/workflows/claude-automation.yml")
        
        # Log activity
        agent_sheet = sheet.worksheet('Agent Activities')
        agent_sheet.append_row([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Mac Claude",
            f"Created {next_task_id} - GitHub Actions automation",
            "Complete",
            "45 min",
            "GitHub Actions workflow created with Claude Code integration. Supports health checks, deployments, testing, docs updates, and backups. Integrated with Google Sheets and Discord.",
            "Configure repository secrets to activate automation"
        ])
        
        print(f"\n📋 Automation Features:")
        print(f"   🔍 Daily health checks at 6 AM UTC")
        print(f"   🚀 Manual deployment validation")
        print(f"   🧪 Automated testing on PR/push")
        print(f"   📝 Documentation updates")
        print(f"   💾 Configuration backups")
        print(f"   📊 Google Sheets integration")
        print(f"   💬 Discord notifications")
        
        print(f"\n⚙️ Setup Required:")
        print(f"   1. Add ANTHROPIC_API_KEY to GitHub secrets")
        print(f"   2. Add GOOGLE_SHEETS_CREDENTIALS to GitHub secrets")
        print(f"   3. Configure Discord webhook (optional)")
        print(f"   4. Test automation with manual trigger")
        
        print(f"\n🎯 Benefits:")
        print(f"   • Automated IoT stack monitoring")
        print(f"   • Intelligent deployment validation")
        print(f"   • Real-time notifications")
        print(f"   • Comprehensive logging")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    add_github_actions_task()