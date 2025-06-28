#!/usr/bin/env python3
"""
Mark CT-007 as complete in Google Sheets - both n8n workflows imported
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime

# Add the scripts directory to Python path for imports
script_dir = Path(__file__).parent
sys.path.append(str(script_dir))

try:
    from google.oauth2.service_account import Credentials
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
except ImportError:
    print("❌ Google API libraries not installed")
    sys.exit(1)

def mark_ct007_complete():
    """Mark CT-007 as complete in Claude Tasks sheet"""
    
    # Configuration
    SPREADSHEET_ID = "1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do"
    CREDENTIALS_FILE = "/home/server/google-sheets-credentials.json"
    
    print("✅ Marking CT-007 as COMPLETED")
    print("=" * 35)
    
    try:
        # Load credentials
        creds = Credentials.from_service_account_file(
            CREDENTIALS_FILE,
            scopes=['https://www.googleapis.com/auth/spreadsheets']
        )
        
        # Build service
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()
        
        print("✅ Connected to Google Sheets API")
        
        # Read Claude Tasks sheet
        range_name = 'Claude Tasks!A:Z'
        result = sheet.values().get(
            spreadsheetId=SPREADSHEET_ID,
            range=range_name
        ).execute()
        
        values = result.get('values', [])
        
        if not values:
            print("❌ No data found in Claude Tasks sheet")
            return False
        
        headers = values[0] if values else []
        print(f"📊 Found {len(values)} rows in Claude Tasks")
        
        # Find CT-007 rows and update them
        ct_007_rows = []
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        for i, row in enumerate(values[1:], 2):  # Start from row 2 (skip headers)
            if len(row) > 0 and "CT-007" in str(row[0]):
                ct_007_rows.append({
                    'row': i,
                    'current_data': row,
                    'task_id': row[0] if len(row) > 0 else '',
                    'description': row[5] if len(row) > 5 else '',
                    'current_status': row[4] if len(row) > 4 else ''
                })
        
        print(f"\n🎯 Found {len(ct_007_rows)} CT-007 entries")
        
        for entry in ct_007_rows:
            print(f"Row {entry['row']}: {entry['task_id']} - Current Status: {entry['current_status']}")
            print(f"  Description: {entry['description'][:80]}...")
        
        if not ct_007_rows:
            print("❌ No CT-007 entries found")
            return False
        
        # Update each CT-007 row
        updates = []
        
        for entry in ct_007_rows:
            row_num = entry['row']
            
            # Prepare update data
            completion_notes = "✅ COMPLETED: Both n8n workflows imported successfully. Formbricks→Sheets (ID: n3UFERK5ilPYrLP3) and MQTT→WhatsApp (ID: PptMUA3BfrivzhG9) are active and tested."
            
            # Update status column (typically column E, index 4)
            status_range = f'Claude Tasks!E{row_num}'
            status_update = {
                'range': status_range,
                'values': [['Complete']]
            }
            updates.append(status_update)
            
            # Update completed date column (typically column J, index 9) 
            completed_range = f'Claude Tasks!J{row_num}'
            completed_update = {
                'range': completed_range,
                'values': [[timestamp]]
            }
            updates.append(completed_update)
            
            # Add completion notes if there's a notes column
            if len(headers) > 10:  # Assuming notes column exists
                notes_range = f'Claude Tasks!K{row_num}'
                notes_update = {
                    'range': notes_range,
                    'values': [[completion_notes]]
                }
                updates.append(notes_update)
        
        # Batch update all changes
        if updates:
            body = {
                'valueInputOption': 'RAW',
                'data': updates
            }
            
            result = sheet.values().batchUpdate(
                spreadsheetId=SPREADSHEET_ID,
                body=body
            ).execute()
            
            print(f"\n✅ CT-007 marked as COMPLETED!")
            print(f"📊 Updated {len(updates)} cells across {len(ct_007_rows)} rows")
            print(f"🎯 Completion details:")
            print("  • Formbricks→Sheets workflow: n3UFERK5ilPYrLP3")
            print("  • MQTT→WhatsApp workflow: PptMUA3BfrivzhG9")
            print("  • Both workflows imported and tested")
            print("  • MQTT integration working with host.docker.internal")
            
        else:
            print("⚠️  No updates prepared")
            
        return True
        
    except HttpError as error:
        print(f"❌ Google Sheets API error: {error}")
        return False
    except Exception as error:
        print(f"❌ Unexpected error: {error}")
        return False

if __name__ == "__main__":
    success = mark_ct007_complete()
    if success:
        print("\n🎉 CT-007 successfully marked as COMPLETED!")
        print("Both n8n workflows are imported and ready for use.")
    else:
        print("\n📝 Please manually mark CT-007 as completed in Google Sheets")
        sys.exit(1)