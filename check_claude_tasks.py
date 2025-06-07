#!/usr/bin/env python3
"""Check Claude Tasks from Google Sheets"""

import sys
sys.path.append('/home/server')
from google_sheets_helper import GoogleSheetsHelper

def check_claude_tasks():
    helper = GoogleSheetsHelper()
    
    print('\n📋 Checking Claude Tasks sheet...')
    data = helper.read_range("'Claude Tasks'!A:G")
    
    if data:
        print(f'\nFound {len(data)} tasks total')
        
        # Show headers
        if len(data) > 0:
            headers = data[0]
            print(f'\nHeaders: {headers}')
        
        # Look for n8n API tasks or CT-009+
        print('\n🔍 Looking for n8n API tasks or CT-009+...')
        for i, row in enumerate(data[1:], 1):  # Skip header
            if len(row) > 0:
                task_id = row[0] if len(row) > 0 else ''
                
                # Check for CT-009 or higher, or n8n API mentions
                if 'CT-009' in task_id or 'CT-010' in task_id or 'CT-011' in task_id:
                    print(f'\n✅ Found new task: {row}')
                elif len(row) > 2 and 'n8n' in str(row[2]).lower() and 'api' in str(row[2]).lower():
                    print(f'\n✅ Found n8n API task: {row}')
        
        # Show last 5 tasks
        print('\n📊 Last 5 tasks:')
        for i, row in enumerate(data[-5:], len(data)-4):
            if len(row) > 0:
                print(f'Row {i}: {row}')

if __name__ == "__main__":
    check_claude_tasks()