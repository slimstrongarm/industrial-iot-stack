#!/usr/bin/env python3
"""
Compare Human Tasks and Claude Tasks sheets to ensure they're synchronized
"""

import sys
from pathlib import Path

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

def compare_tasks():
    """Compare Human Tasks and Claude Tasks for synchronization"""
    
    # Configuration
    SPREADSHEET_ID = "1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do"
    CREDENTIALS_FILE = "/home/server/google-sheets-credentials.json"
    
    print("🔍 HUMAN TASKS vs CLAUDE TASKS COMPARISON")
    print("=" * 50)
    
    try:
        # Load credentials
        creds = Credentials.from_service_account_file(
            CREDENTIALS_FILE,
            scopes=['https://www.googleapis.com/auth/spreadsheets']
        )
        
        # Build service
        service = build('sheets', 'v4', credentials=creds)
        
        # Read Human Tasks
        print("📋 Reading Human Tasks...")
        try:
            human_result = service.spreadsheets().values().get(
                spreadsheetId=SPREADSHEET_ID,
                range='Human Tasks!A:H'
            ).execute()
            human_values = human_result.get('values', [])
        except Exception as e:
            print(f"⚠️  Could not read Human Tasks: {e}")
            # Try alternate names
            try:
                human_result = service.spreadsheets().values().get(
                    spreadsheetId=SPREADSHEET_ID,
                    range='Human Tasks (Clean)!A:H'
                ).execute()
                human_values = human_result.get('values', [])
                print("✅ Found 'Human Tasks (Clean)' tab")
            except:
                print("❌ Could not find Human Tasks tab")
                return False
        
        # Read Claude Tasks  
        print("🤖 Reading Claude Tasks...")
        claude_result = service.spreadsheets().values().get(
            spreadsheetId=SPREADSHEET_ID,
            range='Claude Tasks!A:K'
        ).execute()
        claude_values = claude_result.get('values', [])
        
        print(f"✅ Human Tasks: {len(human_values)} rows")
        print(f"✅ Claude Tasks: {len(claude_values)} rows")
        
        # Analyze Human Tasks
        print("\n📊 HUMAN TASKS ANALYSIS:")
        human_headers = human_values[0] if human_values else []
        print(f"Headers: {human_headers}")
        
        human_tasks = {}
        for i, row in enumerate(human_values[1:], 2):
            if len(row) > 0 and row[0]:
                task_id = row[0]
                status = row[4] if len(row) > 4 else 'Unknown'
                assigned = row[5] if len(row) > 5 else 'Unknown'
                deps = row[6] if len(row) > 6 else '-'
                human_tasks[task_id] = {
                    'row': i, 'status': status, 'assigned': assigned, 'deps': deps,
                    'task': row[1] if len(row) > 1 else 'Unknown'
                }
        
        # Analyze Claude Tasks
        print("\n🤖 CLAUDE TASKS ANALYSIS:")
        claude_headers = claude_values[0] if claude_values else []
        print(f"Headers: {claude_headers}")
        
        claude_tasks = {}
        for i, row in enumerate(claude_values[1:], 2):
            if len(row) > 0 and row[0]:
                task_id = row[0]
                status = row[4] if len(row) > 4 else 'Unknown'
                claude_tasks[task_id] = {
                    'row': i, 'status': status,
                    'task': row[5] if len(row) > 5 else 'Unknown'
                }
        
        # Find completed Claude tasks
        completed_claude = [tid for tid, info in claude_tasks.items() if 'complete' in info['status'].lower()]
        print(f"\n✅ Completed Claude Tasks ({len(completed_claude)}):")
        for ct in completed_claude:
            print(f"  • {ct}: {claude_tasks[ct]['task'][:60]}...")
        
        # Check Human Tasks that depend on completed Claude tasks
        print("\n🔍 DEPENDENCY ANALYSIS:")
        ready_human_tasks = []
        blocked_human_tasks = []
        
        for ht_id, ht_info in human_tasks.items():
            if ht_info['status'].lower() not in ['complete', 'completed']:
                deps = ht_info['deps']
                if deps and deps != '-' and deps.strip():
                    # Check if dependencies are met
                    dep_list = [d.strip() for d in deps.split(',')]
                    claude_deps = [d for d in dep_list if d.startswith('CT-')]
                    
                    if claude_deps:
                        unmet_deps = [d for d in claude_deps if d not in completed_claude]
                        if not unmet_deps:
                            ready_human_tasks.append((ht_id, ht_info['task'], claude_deps))
                            print(f"🚀 {ht_id}: READY - {ht_info['task'][:50]}... (deps: {claude_deps})")
                        else:
                            blocked_human_tasks.append((ht_id, ht_info['task'], unmet_deps))
                            print(f"⏳ {ht_id}: BLOCKED - {ht_info['task'][:50]}... (waiting: {unmet_deps})")
        
        # Check specific tasks from our breakthrough session
        print("\n🎯 BREAKTHROUGH SESSION TASKS CHECK:")
        session_tasks = {
            'HT-002': 'Create Discord Webhooks',
            'HT-003': 'Configure n8n Google Sheets Credentials', 
            'HT-006': 'Get Formbricks API Key',
            'CT-007': 'n8n Workflow Import',
            'CT-013': 'n8n API Configuration',
            'CT-014': 'API Testing',
            'CT-016': 'Ignition Scripts',
            'CT-021': 'Discord Setup',
            'CT-022': 'Discord Integration'
        }
        
        for task_id, expected_name in session_tasks.items():
            if task_id.startswith('HT-'):
                if task_id in human_tasks:
                    ht = human_tasks[task_id]
                    status_icon = "✅" if ht['status'].lower() in ['complete', 'completed'] else "⏳"
                    print(f"  {status_icon} {task_id}: {ht['status']} - {ht['task'][:40]}...")
                else:
                    print(f"  ❌ {task_id}: NOT FOUND in Human Tasks")
            elif task_id.startswith('CT-'):
                if task_id in claude_tasks:
                    ct = claude_tasks[task_id]
                    status_icon = "✅" if ct['status'].lower() in ['complete', 'completed'] else "⏳"
                    print(f"  {status_icon} {task_id}: {ct['status']} - {ct['task'][:40]}...")
                else:
                    print(f"  ❌ {task_id}: NOT FOUND in Claude Tasks")
        
        # Identify discrepancies
        print("\n⚠️  DISCREPANCIES FOUND:")
        discrepancies = []
        
        # Check if HT-002 should be marked complete (we completed it yesterday)
        if 'HT-002' in human_tasks:
            if human_tasks['HT-002']['status'].lower() not in ['complete', 'completed']:
                discrepancies.append("HT-002 should be marked COMPLETE (Discord webhooks working)")
        
        # Check if HT-003 should be ready (CT-013, CT-014 are complete)
        if 'HT-003' in human_tasks:
            ht003 = human_tasks['HT-003']
            if ht003['status'].lower() not in ['complete', 'completed', 'ready']:
                if 'CT-013' in completed_claude and 'CT-014' in completed_claude:
                    discrepancies.append("HT-003 should be marked READY (n8n API is working)")
        
        # Check if any Claude tasks need status updates
        expected_complete = ['CT-007', 'CT-013', 'CT-014', 'CT-016', 'CT-021']
        for ct_id in expected_complete:
            if ct_id in claude_tasks:
                if claude_tasks[ct_id]['status'].lower() not in ['complete', 'completed']:
                    discrepancies.append(f"{ct_id} should be marked COMPLETE")
        
        if discrepancies:
            for disc in discrepancies:
                print(f"  • {disc}")
        else:
            print("  ✅ No major discrepancies found!")
        
        # Summary and recommendations
        print(f"\n📊 SUMMARY & RECOMMENDATIONS:")
        print(f"Human Tasks Total: {len(human_tasks)}")
        print(f"Claude Tasks Total: {len(claude_tasks)}")
        print(f"Completed Claude Tasks: {len(completed_claude)}")
        print(f"Ready Human Tasks: {len(ready_human_tasks)}")
        print(f"Blocked Human Tasks: {len(blocked_human_tasks)}")
        print(f"Discrepancies Found: {len(discrepancies)}")
        
        print(f"\n🚀 IMMEDIATE ACTIONS NEEDED:")
        if ready_human_tasks:
            print("Ready to start:")
            for ht_id, task, deps in ready_human_tasks:
                print(f"  • {ht_id}: {task[:50]}...")
        
        if discrepancies:
            print("Status updates needed:")
            for disc in discrepancies:
                print(f"  • {disc}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error comparing tasks: {e}")
        return False

if __name__ == "__main__":
    success = compare_tasks()
    if success:
        print("\n✅ Task comparison complete!")
    else:
        print("\n❌ Task comparison failed")
        sys.exit(1)