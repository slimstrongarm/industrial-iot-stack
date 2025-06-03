#!/usr/bin/env python3
"""
Update Claude Approvals sheet with dropdown validation
"""

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pathlib import Path

# Configuration
SHEET_ID = '1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do'
CREDS_FILE = str(Path.home() / 'Desktop/industrial-iot-stack/credentials/iot-stack-credentials.json')

def update_claude_approvals():
    """Update the Claude Approvals sheet with enhanced dropdown options"""
    try:
        # Connect to Google Sheets
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_FILE, scope)
        client = gspread.authorize(creds)
        sheet = client.open_by_key(SHEET_ID)
        
        print("✅ Connected to Google Sheets")
        
        # Get the Claude Approvals worksheet
        try:
            worksheet = sheet.worksheet('Claude Approvals')
        except:
            print("❌ Claude Approvals worksheet not found")
            return
        
        # Unfortunately, gspread doesn't support data validation directly
        # We'll update the description to show the options
        
        # Update the description in row 2 to include the options
        current_desc = worksheet.cell(2, 3).value
        
        options_text = """Select from dropdown in column E:
✅ Yes, proceed
🤝 Yes, but let's discuss details  
⏸️ Hold on, need more info
📅 Not now, maybe later
🔄 Let's try a different approach
❌ No, not a good idea
💬 Need to chat about this
🚀 Fast track this!
⚠️ Proceed with caution"""
        
        # Update the description to include options
        if "Select from dropdown" not in current_desc:
            new_desc = current_desc + "\n\n" + options_text
            worksheet.update_cell(2, 3, new_desc)
            print("✅ Updated description with dropdown options")
        
        # Also add a note in column E header
        worksheet.update_cell(1, 5, "Your Response\n(Use Apps Script for dropdown)")
        
        print("\n📝 To add the dropdown:")
        print("1. Go to Extensions > Apps Script in Google Sheets")
        print("2. Run the fixClaudeApprovalsDropdown function")
        print("3. Or manually add data validation to column E with these options")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    update_claude_approvals()