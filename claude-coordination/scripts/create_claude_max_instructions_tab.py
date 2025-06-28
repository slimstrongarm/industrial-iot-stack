#!/usr/bin/env python3
"""
Create new Google Sheets tab with Claude Max GitHub Actions instructions
"""

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pathlib import Path
from datetime import datetime

# Configuration
SHEET_ID = '1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do'
CREDS_FILE = str(Path.home() / 'Desktop/industrial-iot-stack/credentials/iot-stack-credentials.json')

def create_claude_max_instructions_tab():
    """Create new tab with Claude Max automation instructions"""
    try:
        # Connect to Google Sheets
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_FILE, scope)
        client = gspread.authorize(creds)
        sheet = client.open_by_key(SHEET_ID)
        
        # Create new worksheet
        try:
            claude_max_sheet = sheet.add_worksheet(title="Claude Max Instructions", rows=100, cols=10)
            print("✅ Created new 'Claude Max Instructions' tab")
        except Exception as e:
            if "already exists" in str(e):
                claude_max_sheet = sheet.worksheet("Claude Max Instructions")
                claude_max_sheet.clear()
                print("✅ Found existing tab, cleared content")
            else:
                raise e
        
        # Define the instruction content
        instructions = [
            ["🤖 Claude Max GitHub Actions Instructions", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", ""],
            ["Quick Start Guide", "", "", "", "", "", "", "", "", ""],
            ["=================", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", ""],
            ["1. SETUP (One-time)", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", ""],
            ["Step", "Action", "Details", "", "", "", "", "", "", ""],
            ["1", "Add GitHub Secrets", "Go to: https://github.com/slimstrongarm/industrial-iot-stack/settings/secrets/actions", "", "", "", "", "", "", ""],
            ["", "Required Secret", "GOOGLE_SHEETS_CREDENTIALS", "", "", "", "", "", "", ""],
            ["", "Required Secret", "GOOGLE_SHEETS_ID (already set)", "", "", "", "", "", "", ""],
            ["", "Optional Secret", "DISCORD_WEBHOOK_URL", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", ""],
            ["2", "Test First Run", "Actions → Claude Max Automation → Run workflow", "", "", "", "", "", "", ""],
            ["", "Choose Task", "health-check (recommended first test)", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", ""],
            ["2. DAILY WORKFLOW", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", ""],
            ["Morning Check", "Process", "What You Do", "", "", "", "", "", "", ""],
            ["6:00 AM UTC", "GitHub Actions runs health-check automatically", "Nothing - automated", "", "", "", "", "", "", ""],
            ["6:05 AM", "Discord notification sent", "Check Discord for alert", "", "", "", "", "", "", ""],
            ["Your convenience", "GitHub issue created with instructions", "Click issue link from Discord", "", "", "", "", "", "", ""],
            ["", "Download context files", "Click workflow run → Artifacts section", "", "", "", "", "", "", ""],
            ["", "Claude Max session", "Upload files, execute task", "", "", "", "", "", "", ""],
            ["", "Update this sheet", "Mark task complete in Agent Activities", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", ""],
            ["3. MANUAL TASKS", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", ""],
            ["Task Type", "When to Use", "What It Does", "", "", "", "", "", "", ""],
            ["health-check", "Daily (automatic) or when issues suspected", "Validates system health, finds problems", "", "", "", "", "", "", ""],
            ["deploy-staging", "Before deploying to brewery", "Validates deployment readiness", "", "", "", "", "", "", ""],
            ["run-tests", "After code changes", "Tests all integrations", "", "", "", "", "", "", ""],
            ["update-docs", "When docs are outdated", "Updates all documentation", "", "", "", "", "", "", ""],
            ["backup-configs", "Weekly or before major changes", "Backs up all configurations", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", ""],
            ["4. STEP-BY-STEP SESSION", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", ""],
            ["Step", "Action", "Example", "", "", "", "", "", "", ""],
            ["1", "Trigger automation", "GitHub Actions → Claude Max Automation → Run workflow", "", "", "", "", "", "", ""],
            ["2", "Check Discord", "🤖 Claude Max Session Ready: health-check", "", "", "", "", "", "", ""],
            ["3", "Click GitHub issue", "Issue title: 🤖 Claude Max Session Ready: health-check", "", "", "", "", "", "", ""],
            ["4", "Download artifacts", "Workflow run → Artifacts → claude-max-context-health-check", "", "", "", "", "", "", ""],
            ["5", "Extract files", "claude_max_summary.md + claude_max_context.json", "", "", "", "", "", "", ""],
            ["6", "Open Claude Max", "Go to claude.ai", "", "", "", "", "", "", ""],
            ["7", "Upload summary", "Drag claude_max_summary.md to Claude Max", "", "", "", "", "", "", ""],
            ["8", "Execute task", "Follow the task instructions in the summary", "", "", "", "", "", "", ""],
            ["9", "Update Agent Activities", "Mark automation task as Complete", "", "", "", "", "", "", ""],
            ["10", "Close GitHub issue", "Add comment with results, close issue", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", ""],
            ["5. AVAILABLE AUTOMATIONS", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", ""],
            ["Task", "Trigger", "Frequency", "Purpose", "", "", "", "", "", ""],
            ["health-check", "Automatic + Manual", "Daily 6 AM UTC", "System validation", "", "", "", "", "", ""],
            ["deploy-staging", "Manual only", "As needed", "Deployment prep", "", "", "", "", "", ""],
            ["run-tests", "Manual only", "After changes", "Integration testing", "", "", "", "", "", ""],
            ["update-docs", "Manual only", "Weekly", "Documentation maintenance", "", "", "", "", "", ""],
            ["backup-configs", "Manual only", "Weekly", "Configuration backup", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", ""],
            ["6. TROUBLESHOOTING", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", ""],
            ["Issue", "Solution", "", "", "", "", "", "", "", ""],
            ["No Discord notification", "Check DISCORD_WEBHOOK_URL secret", "", "", "", "", "", "", "", ""],
            ["Cannot download artifacts", "Artifacts expire after 30 days", "", "", "", "", "", "", "", ""],
            ["GitHub Actions failed", "Check Actions tab for error logs", "", "", "", "", "", "", "", ""],
            ["Cannot update sheets", "Check GOOGLE_SHEETS_CREDENTIALS", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", ""],
            ["7. LINKS", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", ""],
            ["Resource", "URL", "", "", "", "", "", "", "", ""],
            ["GitHub Actions", "https://github.com/slimstrongarm/industrial-iot-stack/actions", "", "", "", "", "", "", "", ""],
            ["Repository Secrets", "https://github.com/slimstrongarm/industrial-iot-stack/settings/secrets/actions", "", "", "", "", "", "", "", ""],
            ["Claude Max", "https://claude.ai", "", "", "", "", "", "", "", ""],
            ["This Google Sheet", f"https://docs.google.com/spreadsheets/d/{SHEET_ID}", "", "", "", "", "", "", "", ""],
            ["Setup Guide", "See GITHUB_ACTIONS_CLAUDE_MAX_SETUP.md in repository", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", ""],
            ["8. COSTS", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", ""],
            ["Service", "Cost", "Notes", "", "", "", "", "", "", ""],
            ["Claude Max", "$20/month", "Your existing subscription", "", "", "", "", "", "", ""],
            ["GitHub Actions", "Free", "2,000 minutes/month included", "", "", "", "", "", "", ""],
            ["Google Sheets", "Free", "Part of Google account", "", "", "", "", "", "", ""],
            ["Discord", "Free", "For notifications", "", "", "", "", "", "", ""],
            ["Total Additional", "$0", "Uses existing subscriptions", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", ""],
            ["Last Updated", datetime.now().strftime("%Y-%m-%d %H:%M"), "By Mac Claude automation", "", "", "", "", "", "", ""]
        ]
        
        # Add content to the sheet
        if instructions:
            # Get the range for all data
            end_row = len(instructions)
            end_col = len(instructions[0])
            range_name = f"A1:{chr(65 + end_col - 1)}{end_row}"
            
            # Update all at once for efficiency
            claude_max_sheet.update(range_name, instructions)
        
        # Format the sheet
        # Header row formatting
        claude_max_sheet.format("A1:J1", {
            "backgroundColor": {"red": 0.2, "green": 0.6, "blue": 0.9},
            "textFormat": {"bold": True, "fontSize": 14, "foregroundColor": {"red": 1, "green": 1, "blue": 1}}
        })
        
        # Section headers formatting
        section_rows = [3, 17, 29, 36, 49, 58, 68, 74]
        for row in section_rows:
            claude_max_sheet.format(f"A{row}:J{row}", {
                "backgroundColor": {"red": 0.9, "green": 0.9, "blue": 0.9},
                "textFormat": {"bold": True}
            })
        
        # Step numbers formatting
        claude_max_sheet.format("A8:A15", {
            "backgroundColor": {"red": 0.8, "green": 1, "blue": 0.8},
            "textFormat": {"bold": True}
        })
        
        claude_max_sheet.format("A37:A47", {
            "backgroundColor": {"red": 0.8, "green": 1, "blue": 0.8},
            "textFormat": {"bold": True}
        })
        
        # Resize columns
        claude_max_sheet.columns_auto_resize(0, 2)  # Auto-resize first 3 columns
        
        print("✅ Content added and formatted")
        
        # Log the creation
        agent_sheet = sheet.worksheet('Agent Activities')
        agent_sheet.append_row([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Mac Claude",
            "Created Claude Max Instructions tab",
            "Complete",
            "15 min",
            "Created comprehensive instructions tab for Claude Max GitHub Actions workflow. Includes setup, daily workflow, troubleshooting, and step-by-step guides.",
            "Ready for automation execution"
        ])
        
        print(f"\n✅ Claude Max Instructions tab created successfully!")
        print(f"📋 Tab includes:")
        print(f"   • One-time setup instructions")
        print(f"   • Daily workflow guide")
        print(f"   • Step-by-step session walkthrough")
        print(f"   • All 5 automation task types")
        print(f"   • Troubleshooting guide")
        print(f"   • Quick reference links")
        print(f"   • Cost breakdown")
        
        print(f"\n🔗 Access the tab:")
        print(f"   https://docs.google.com/spreadsheets/d/{SHEET_ID}")
        print(f"   Look for 'Claude Max Instructions' tab")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    create_claude_max_instructions_tab()