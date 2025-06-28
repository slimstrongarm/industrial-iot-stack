#!/usr/bin/env python3
"""
Stable version of Claude Tasks monitor with error handling and recovery
"""

from googleapiclient.discovery import build
from google.oauth2 import service_account
from datetime import datetime
import time
import json
import os
import traceback

# Configuration
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'credentials/iot-stack-credentials.json'
SPREADSHEET_ID = '1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do'
SHEET_NAME = 'Claude Tasks'
STATE_FILE = 'scripts/.claude_tasks_state.json'

# Error tracking
error_count = 0
consecutive_errors = 0
max_consecutive_errors = 5

def get_sheets_service():
    """Initialize Google Sheets service with retry logic"""
    try:
        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        service = build('sheets', 'v4', credentials=credentials)
        return service.spreadsheets()
    except Exception as e:
        print(f"⚠️  Error creating sheets service: {e}")
        return None

def load_previous_state():
    """Load previous state from file"""
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, 'r') as f:
                return json.load(f)
        except:
            pass
    return {}

def save_current_state(state):
    """Save current state to file"""
    try:
        os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
        with open(STATE_FILE, 'w') as f:
            json.dump(state, f, indent=2)
    except Exception as e:
        print(f"⚠️  Warning: Could not save state: {e}")

def get_current_tasks():
    """Get current Claude Tasks from sheet with error handling"""
    global consecutive_errors
    
    try:
        sheet = get_sheets_service()
        if not sheet:
            raise Exception("Could not create sheets service")
        
        result = sheet.values().get(
            spreadsheetId=SPREADSHEET_ID,
            range=f'{SHEET_NAME}!A:J'
        ).execute()
        
        values = result.get('values', [])
        
        # Convert to dict for easier comparison
        tasks = {}
        for i, row in enumerate(values):
            if i == 0:  # Skip header
                continue
            if len(row) >= 5:
                task_id = row[0]
                tasks[task_id] = {
                    'instance': row[1] if len(row) > 1 else '',
                    'task_type': row[2] if len(row) > 2 else '',
                    'priority': row[3] if len(row) > 3 else '',
                    'status': row[4] if len(row) > 4 else '',
                    'description': row[5] if len(row) > 5 else '',
                    'expected_output': row[6] if len(row) > 6 else '',
                    'dependencies': row[7] if len(row) > 7 else '',
                    'date_added': row[8] if len(row) > 8 else '',
                    'completed': row[9] if len(row) > 9 else '',
                    'row': i + 1
                }
        
        # Reset error count on success
        consecutive_errors = 0
        return tasks
        
    except Exception as e:
        consecutive_errors += 1
        print(f"⚠️  Error reading sheet (attempt {consecutive_errors}): {e}")
        
        if consecutive_errors >= max_consecutive_errors:
            print(f"❌ Too many consecutive errors ({consecutive_errors}). Stopping monitoring.")
            raise
        
        return None

def detect_changes(previous_tasks, current_tasks):
    """Detect changes between previous and current state"""
    if not current_tasks:
        return []
    
    changes = []
    
    # Check for new tasks
    for task_id, task in current_tasks.items():
        if task_id not in previous_tasks:
            changes.append({
                'type': 'new_task',
                'task_id': task_id,
                'task': task
            })
    
    # Check for status changes
    for task_id, task in current_tasks.items():
        if task_id in previous_tasks:
            prev_task = previous_tasks[task_id]
            
            # Status change
            if prev_task.get('status') != task.get('status'):
                changes.append({
                    'type': 'status_change',
                    'task_id': task_id,
                    'old_status': prev_task.get('status'),
                    'new_status': task.get('status'),
                    'task': task
                })
            
            # Completion
            if not prev_task.get('completed') and task.get('completed'):
                changes.append({
                    'type': 'completed',
                    'task_id': task_id,
                    'task': task
                })
    
    return changes

def format_change_notification(change):
    """Format change notification for display"""
    if change['type'] == 'new_task':
        task = change['task']
        return f"🆕 NEW TASK: {change['task_id']} ({task['instance']})\n   📋 {task['description'][:60]}..."
    
    elif change['type'] == 'status_change':
        task = change['task']
        old_status = change['old_status']
        new_status = change['new_status']
        
        status_icons = {
            'Pending': '⏳',
            'In Progress': '🔄', 
            'Complete': '✅',
            'Blocked': '🚫'
        }
        
        old_icon = status_icons.get(old_status, '❓')
        new_icon = status_icons.get(new_status, '❓')
        
        return f"🔄 STATUS CHANGE: {change['task_id']} ({task['instance']})\n   {old_icon} {old_status} → {new_icon} {new_status}\n   📋 {task['description'][:60]}..."
    
    elif change['type'] == 'completed':
        task = change['task']
        return f"✅ TASK COMPLETED: {change['task_id']} ({task['instance']})\n   📋 {task['description'][:60]}...\n   🎉 Finished: {task['completed']}"
    
    return str(change)

def monitor_once():
    """Single check for changes with error handling"""
    global error_count
    
    print(f"🔍 Checking Claude Tasks sheet at {datetime.now().strftime('%H:%M:%S')}...", end='', flush=True)
    
    try:
        previous_state = load_previous_state()
        current_tasks = get_current_tasks()
        
        if current_tasks is None:
            print(" ⚠️  Skipping due to error")
            return False
        
        previous_tasks = previous_state.get('tasks', {})
        changes = detect_changes(previous_tasks, current_tasks)
        
        # Save current state
        save_current_state({
            'tasks': current_tasks,
            'last_check': datetime.now().isoformat(),
            'error_count': error_count
        })
        
        if changes:
            print(f"\n\n🚨 {len(changes)} CHANGE(S) DETECTED!")
            print("=" * 60)
            
            for change in changes:
                print(format_change_notification(change))
                print()
            
            # Highlight Server Claude activity
            server_changes = [c for c in changes if c.get('task', {}).get('instance') == 'Server Claude']
            if server_changes:
                print("🤖 SERVER CLAUDE ACTIVITY:")
                for change in server_changes:
                    if change['type'] == 'completed':
                        print(f"   🎯 Server Claude completed: {change['task_id']}")
                    elif change['type'] == 'status_change' and change['new_status'] == 'In Progress':
                        print(f"   🔄 Server Claude started: {change['task_id']}")
            
            return True
        else:
            print(" ✅ No changes")
            return False
            
    except Exception as e:
        error_count += 1
        print(f"\n❌ Error during monitoring: {e}")
        traceback.print_exc()
        return False

def monitor_continuous(interval_seconds=30):
    """Continuously monitor for changes with error recovery"""
    print(f"🔄 Starting stable continuous monitoring (every {interval_seconds}s)")
    print("📡 Connection status: Testing Google Sheets API...")
    
    # Test connection first
    test_tasks = get_current_tasks()
    if test_tasks:
        print(f"✅ Connected! Monitoring {len(test_tasks)} tasks")
    else:
        print("⚠️  Initial connection failed, but will keep trying...")
    
    print("\nPress Ctrl+C to stop\n")
    
    start_time = datetime.now()
    check_count = 0
    
    try:
        while True:
            check_count += 1
            
            try:
                if monitor_once():
                    print("\n" + "="*60 + "\n")
                
            except Exception as e:
                print(f"\n⚠️  Monitor error: {e}")
                print("🔄 Recovering and continuing...")
            
            # Status update every 10 checks
            if check_count % 10 == 0:
                runtime = datetime.now() - start_time
                print(f"\n📊 Status: {check_count} checks, running for {runtime}, {error_count} total errors")
            
            time.sleep(interval_seconds)
            
    except KeyboardInterrupt:
        runtime = datetime.now() - start_time
        print(f"\n\n👋 Monitoring stopped")
        print(f"📊 Final stats: {check_count} checks over {runtime}, {error_count} errors")
        
        if error_count > 0:
            print(f"⚠️  Note: Encountered {error_count} errors during monitoring")
        else:
            print("✅ No errors encountered - stable monitoring session!")

if __name__ == "__main__":
    import sys
    
    print("🚀 Claude Tasks Monitor - Stable Version")
    print("="*40)
    
    if len(sys.argv) > 1 and sys.argv[1] == 'continuous':
        interval = int(sys.argv[2]) if len(sys.argv) > 2 else 30
        monitor_continuous(interval)
    else:
        monitor_once()