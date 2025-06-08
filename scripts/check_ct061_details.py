#!/usr/bin/env python3
"""
Check CT-061 details from Google Sheets for Server Claude handoff
"""

import gspread
from google.oauth2.service_account import Credentials
from pathlib import Path

def check_ct061():
    """Check CT-061 details for Server Claude"""
    
    try:
        # Load credentials
        creds_path = Path(__file__).parent.parent / "credentials" / "iot-stack-credentials.json"
        
        # Setup Google Sheets client
        scope = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]
        
        creds = Credentials.from_service_account_file(creds_path, scopes=scope)
        client = gspread.authorize(creds)
        
        # Open the IoT Stack Progress Master spreadsheet
        spreadsheet = client.open("IoT Stack Progress Master")
        claude_tasks_sheet = spreadsheet.worksheet("Claude Tasks")
        
        print("✅ Connected to Claude Tasks sheet")
        
        # Get all data to find CT-061
        all_data = claude_tasks_sheet.get_all_records()
        
        # Look for CT-061 or task around row 61
        ct061_found = False
        
        for i, row in enumerate(all_data, start=2):
            task_id = row.get('Task ID', '')
            description = row.get('Description', '')
            status = row.get('Status', '')
            assigned_to = row.get('Instance', '')
            
            # Check for CT-061 or look around row 61
            if 'CT-061' in task_id or i == 61 or (61 <= i <= 65 and 'WhatsApp' in description):
                print(f"\n📋 Row {i} - Potential CT-061:")
                print(f"   Task ID: {task_id}")
                print(f"   Instance: {assigned_to}")
                print(f"   Status: {status}")
                print(f"   Description: {description}")
                
                if 'WhatsApp' in description or 'whatsapp' in description.lower():
                    print(f"   🎯 This appears to be the WhatsApp integration task!")
                    ct061_found = True
                    
                    return {
                        "row": i,
                        "task_id": task_id,
                        "description": description,
                        "status": status,
                        "assigned_to": assigned_to,
                        "expected_output": row.get('Expected Output', ''),
                        "dependencies": row.get('Dependencies', ''),
                        "date_added": row.get('Date Added', '')
                    }
        
        if not ct061_found:
            print("\n⚠️ CT-061 not found. Checking nearby rows for WhatsApp tasks...")
            
            # Look for WhatsApp-related tasks
            for i, row in enumerate(all_data, start=2):
                description = row.get('Description', '')
                if 'whatsapp' in description.lower() and row.get('Status', '') == 'Pending':
                    print(f"\n📋 Row {i} - WhatsApp Task Found:")
                    print(f"   Task ID: {row.get('Task ID', '')}")
                    print(f"   Description: {description}")
                    print(f"   Status: {row.get('Status', '')}")
                    return row
        
        return None
        
    except Exception as e:
        print(f"❌ Error checking CT-061: {e}")
        return None

def main():
    """Main function"""
    print("📊 Checking CT-061 Details for Server Claude Handoff")
    print("=" * 60)
    
    task_info = check_ct061()
    
    if task_info:
        print("\n✅ Task found and ready for Server Claude handoff!")
    else:
        print("\n❌ CT-061 not found - may need manual identification")

if __name__ == "__main__":
    main()