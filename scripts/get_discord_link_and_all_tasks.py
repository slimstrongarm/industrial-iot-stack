#!/usr/bin/env python3
"""
Get Discord server link from Google Sheets and analyze all Claude tasks for autonomous completion
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

def analyze_all_claude_tasks():
    """Get Discord link and analyze all Claude tasks for autonomous completion"""
    
    # Configuration
    SPREADSHEET_ID = "1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do"
    CREDENTIALS_FILE = "/home/server/google-sheets-credentials.json"
    
    print("🔍 Checking Discord Link and Analyzing All Claude Tasks")
    print("=" * 60)
    
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
        
        # Get all sheet names
        spreadsheet = sheet.get(spreadsheetId=SPREADSHEET_ID).execute()
        sheet_names = [s['properties']['title'] for s in spreadsheet['sheets']]
        
        print(f"📊 Available sheets: {sheet_names}")
        
        # Look for Discord-related sheets
        discord_sheets = [name for name in sheet_names if 'discord' in name.lower()]
        print(f"🎯 Discord-related sheets: {discord_sheets}")
        
        # Check each sheet for Discord links
        discord_link = None
        for sheet_name in sheet_names:
            try:
                range_name = f"'{sheet_name}'!A:Z"
                result = sheet.values().get(
                    spreadsheetId=SPREADSHEET_ID,
                    range=range_name
                ).execute()
                
                values = result.get('values', [])
                
                # Look for Discord links in this sheet
                for i, row in enumerate(values):
                    for j, cell in enumerate(row):
                        if isinstance(cell, str) and ('discord.gg' in cell or 'discord.com/invite' in cell):
                            discord_link = cell
                            print(f"🎯 Found Discord link in '{sheet_name}' at row {i+1}, column {j+1}: {discord_link}")
                            break
                    if discord_link:
                        break
                        
            except Exception as e:
                print(f"⚠️  Could not read sheet '{sheet_name}': {e}")
                continue
        
        if not discord_link:
            print("❌ No Discord invite link found in any sheet")
            print("💡 Looking for Discord server info or placeholder...")
        
        # Read Claude Tasks sheet for comprehensive analysis
        print("\n📋 Analyzing Claude Tasks for Autonomous Completion")
        print("=" * 55)
        
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
        print(f"📊 Headers: {headers}")
        
        # Analyze each task for autonomous completion potential
        autonomous_tasks = []
        pending_tasks = []
        completed_tasks = []
        
        for i, row in enumerate(values[1:], 2):
            if len(row) > 0:
                task_data = {}
                for j, cell in enumerate(row):
                    header = headers[j] if j < len(headers) else f"Column_{j+1}"
                    task_data[header] = cell
                
                task_id = task_data.get('Task ID', '')
                instance = task_data.get('Instance', '')
                task_type = task_data.get('Task Type', '')
                status = task_data.get('Status', '')
                description = task_data.get('Description', '')
                
                if 'Server Claude' in instance and status not in ['Complete', 'Completed']:
                    # Analyze autonomous potential
                    autonomous_score = 0
                    
                    # API tasks are highly autonomous
                    if 'API' in task_type or 'api' in description.lower():
                        autonomous_score += 3
                    
                    # Configuration tasks are autonomous
                    if 'Configuration' in task_type or 'config' in description.lower():
                        autonomous_score += 3
                    
                    # Script creation is autonomous
                    if 'script' in description.lower() or 'Script' in task_type:
                        autonomous_score += 2
                    
                    # Documentation is autonomous
                    if 'Documentation' in task_type or 'document' in description.lower():
                        autonomous_score += 2
                    
                    # Testing can be autonomous if endpoints exist
                    if 'Testing' in task_type or 'test' in description.lower():
                        autonomous_score += 2
                    
                    # Integration tasks may need coordination
                    if 'Integration' in task_type:
                        autonomous_score += 1
                    
                    # Workflow/Flow imports are autonomous
                    if 'workflow' in description.lower() or 'flow' in description.lower():
                        autonomous_score += 2
                    
                    task_info = {
                        'task_id': task_id,
                        'description': description,
                        'type': task_type,
                        'status': status,
                        'autonomous_score': autonomous_score,
                        'row': i
                    }
                    
                    if autonomous_score >= 2:
                        autonomous_tasks.append(task_info)
                    else:
                        pending_tasks.append(task_info)
                
                elif status in ['Complete', 'Completed']:
                    completed_tasks.append({
                        'task_id': task_id,
                        'description': description,
                        'status': status
                    })
        
        print(f"\n📊 Task Analysis Summary:")
        print(f"✅ Completed tasks: {len(completed_tasks)}")
        print(f"🚀 High autonomous potential: {len(autonomous_tasks)}")
        print(f"⏳ Requires coordination: {len(pending_tasks)}")
        
        print(f"\n🎯 HIGH PRIORITY AUTONOMOUS TASKS:")
        autonomous_tasks.sort(key=lambda x: x['autonomous_score'], reverse=True)
        
        for task in autonomous_tasks[:10]:  # Top 10
            score_emoji = "🚀" if task['autonomous_score'] >= 3 else "🔧"
            print(f"{score_emoji} {task['task_id']}: {task['description'][:80]}...")
            print(f"   Type: {task['type']}, Score: {task['autonomous_score']}/5")
        
        return {
            'discord_link': discord_link,
            'autonomous_tasks': autonomous_tasks,
            'pending_tasks': pending_tasks,
            'total_tasks': len(values) - 1
        }
        
    except HttpError as error:
        print(f"❌ Google Sheets API error: {error}")
        return False
    except Exception as error:
        print(f"❌ Unexpected error: {error}")
        return False

if __name__ == "__main__":
    result = analyze_all_claude_tasks()
    if result:
        print(f"\n🎯 READY FOR AUTONOMOUS EXECUTION")
        print(f"Discord link: {result['discord_link'] or 'Not found'}")
        print(f"Autonomous tasks available: {len(result['autonomous_tasks'])}")
        print(f"Estimated autonomous work: {len(result['autonomous_tasks']) * 15} minutes")
    else:
        sys.exit(1)