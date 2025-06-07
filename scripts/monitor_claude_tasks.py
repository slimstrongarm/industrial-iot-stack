#!/usr/bin/env python3
"""
Monitor Claude Tasks sheet for changes and notify about Server Claude progress
"""

from googleapiclient.discovery import build
from google.oauth2 import service_account
from datetime import datetime
import time
import json
import os

# Configuration
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'credentials/iot-stack-credentials.json'
SPREADSHEET_ID = '1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do'
SHEET_NAME = 'Claude Tasks'
STATE_FILE = 'scripts/.claude_tasks_state.json'

def get_sheets_service():
    """Initialize Google Sheets service"""
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=credentials)
    return service.spreadsheets()

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
        with open(STATE_FILE, 'w') as f:
            json.dump(state, f, indent=2)
    except Exception as e:
        print(f"Warning: Could not save state: {e}")

def get_current_tasks():
    """Get current Claude Tasks from sheet"""
    try:
        sheet = get_sheets_service()
        
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
        
        return tasks
    except Exception as e:
        print(f"❌ Error reading sheet: {e}")
        return {}

def detect_changes(previous_tasks, current_tasks):
    """Detect changes between previous and current state"""
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

def check_for_changes():
    """Check for changes and return notifications"""
    previous_state = load_previous_state()
    current_tasks = get_current_tasks()
    
    if not current_tasks:
        return []
    
    previous_tasks = previous_state.get('tasks', {})
    changes = detect_changes(previous_tasks, current_tasks)
    
    # Save current state
    save_current_state({
        'tasks': current_tasks,
        'last_check': datetime.now().isoformat()
    })
    
    return changes

def monitor_once():
    """Single check for changes"""
    print(f"🔍 Checking Claude Tasks sheet at {datetime.now().strftime('%H:%M:%S')}...")
    
    changes = check_for_changes()
    
    if changes:
        print(f"\n🚨 {len(changes)} CHANGE(S) DETECTED!")
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
        print("   ✅ No changes detected")
        return False

def monitor_continuous(interval_seconds=30):
    """Continuously monitor for changes"""
    print(f"🔄 Starting continuous monitoring (every {interval_seconds}s)")
    print("Press Ctrl+C to stop")
    
    try:
        while True:
            if monitor_once():
                print("\n" + "="*60 + "\n")
            
            time.sleep(interval_seconds)
    except KeyboardInterrupt:
        print("\n👋 Monitoring stopped")

def show_current_status():
    """Show current status of all tasks"""
    current_tasks = get_current_tasks()
    
    if not current_tasks:
        print("❌ Could not retrieve tasks")
        return
    
    print("\n📊 CURRENT CLAUDE TASKS STATUS:")
    print("=" * 80)
    
    # Group by instance
    instances = {}
    for task_id, task in current_tasks.items():
        instance = task['instance']
        if instance not in instances:
            instances[instance] = []
        instances[instance].append((task_id, task))
    
    for instance, tasks in instances.items():
        print(f"\n🤖 {instance}:")
        
        for task_id, task in sorted(tasks):
            status = task['status']
            status_icons = {
                'Pending': '⏳',
                'In Progress': '🔄', 
                'Complete': '✅',
                'Blocked': '🚫'
            }
            
            icon = status_icons.get(status, '❓')
            print(f"   {icon} {task_id}: {task['description'][:70]}...")
            
            if task['completed']:
                print(f"       ✅ Completed: {task['completed']}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == 'continuous':
            interval = int(sys.argv[2]) if len(sys.argv) > 2 else 30
            monitor_continuous(interval)
        elif sys.argv[1] == 'status':
            show_current_status()
        else:
            print("Usage: python monitor_claude_tasks.py [continuous [interval]|status]")
    else:
        # Single check
        monitor_once()