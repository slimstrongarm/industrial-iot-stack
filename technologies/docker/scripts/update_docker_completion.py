#!/usr/bin/env python3
import sys
sys.path.append('/home/server')
from google_sheets_helper import GoogleSheetsHelper
from datetime import datetime

helper = GoogleSheetsHelper()
timestamp = datetime.now().strftime('%m/%d/%Y %H:%M:%S')

# Update Human Tasks Row 12 (Docker confirmation) to Complete
print("🔄 Updating Docker task completion...")

try:
    # Try different sheet name formats
    for sheet_format in ["Human Tasks!D12", "'Human Tasks'!D12"]:
        try:
            result = helper.write_range(sheet_format, [['Complete']])
            if result:
                print(f"✅ Updated status using format: {sheet_format}")
                break
        except Exception as e:
            print(f"❌ Failed with format {sheet_format}: {e}")
            continue
    
    # Add log entry to Agent Activities  
    log_entry = [
        timestamp,
        'server-claude',
        'Docker WSL Integration',
        'Docker Desktop + Claude Code compatibility achieved via wrapper scripts',
        'Success'
    ]
    helper.append_row('Agent Activities', log_entry)
    print('✅ Added log entry to Agent Activities')
    
except Exception as e:
    print(f"❌ Error updating sheets: {e}")