#!/usr/bin/env python3
"""Add screenshot script info to Google Sheets"""

import sys
import os
sys.path.append('/home/server')

from google_sheets_helper import GoogleSheetsHelper
import datetime

def add_screenshot_script():
    helper = GoogleSheetsHelper()
    
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    script_info = [
        timestamp,
        'Screenshot Helper',
        'Quick screenshot tool for troubleshooting',
        '''# Screenshot Tools Available:

## Quick Screenshot Tool:
python3 /mnt/c/Users/LocalAccount/industrial-iot-stack/scripts/quick_screenshot.py

## Features:
- Opens Windows Snipping Tool automatically
- Creates screenshots directory
- Provides filename format: screenshot_YYYYMMDD_HHMMSS.png
- Directory: /mnt/c/Users/LocalAccount/industrial-iot-stack/screenshots/

## Alternative:
Use Claude Desktop for drag-and-drop screenshots directly into conversation

## Usage:
1. Run the script
2. Take screenshot with Snipping Tool
3. Save with provided filename
4. Reference filename when sharing with Claude''',
        'server-claude'
    ]
    
    try:
        if helper.append_row('Script Copy', script_info):
            print('✅ Screenshot script info added to IIOT sheet')
            return True
        else:
            print('❌ Failed to add to sheet')
            return False
    except Exception as e:
        print(f'❌ Error: {e}')
        return False

if __name__ == "__main__":
    add_screenshot_script()