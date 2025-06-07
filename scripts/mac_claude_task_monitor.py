#!/usr/bin/env python3
"""
🤖 Mac Claude Task Monitor
Watches Google Sheets for tasks assigned to Mac Claude and logs them

This script continuously monitors the Claude Tasks sheet for:
- New tasks assigned to "Mac Claude"
- Status changes on Mac Claude tasks
- Priority updates
"""

import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import time
import json
import os

# Configuration
SPREADSHEET_ID = '1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do'
CREDENTIALS_PATH = '/Users/joshpayneair/Desktop/industrial-iot-stack/credentials/iot-stack-credentials.json'
STATE_FILE = '/Users/joshpayneair/Desktop/industrial-iot-stack/scripts/.mac_claude_tasks_state.json'
CHECK_INTERVAL = 30  # seconds

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
        print(f"⚠️  Could not save state: {e}")

def get_mac_claude_tasks(sheet):
    """Get all tasks assigned to Mac Claude"""
    try:
        # Get all values from Claude Tasks sheet
        claude_tasks = sheet.worksheet('Claude Tasks')
        all_rows = claude_tasks.get_all_values()
        
        if len(all_rows) < 2:  # No data beyond header
            return {}
        
        # Get header row
        headers = all_rows[0]
        
        # Find column indices
        id_col = headers.index('Task ID') if 'Task ID' in headers else 0
        assigned_col = headers.index('Assigned To') if 'Assigned To' in headers else 1
        title_col = headers.index('Task Title') if 'Task Title' in headers else 2
        priority_col = headers.index('Priority') if 'Priority' in headers else 3
        status_col = headers.index('Status') if 'Status' in headers else 4
        
        mac_claude_tasks = {}
        
        # Process each row
        for row in all_rows[1:]:  # Skip header
            if len(row) > assigned_col and row[assigned_col] == 'Mac Claude':
                task_id = row[id_col] if len(row) > id_col else ''
                if task_id:
                    mac_claude_tasks[task_id] = {
                        'id': task_id,
                        'title': row[title_col] if len(row) > title_col else '',
                        'priority': row[priority_col] if len(row) > priority_col else '',
                        'status': row[status_col] if len(row) > status_col else '',
                        'assigned_to': 'Mac Claude'
                    }
        
        return mac_claude_tasks
        
    except Exception as e:
        print(f"❌ Error reading tasks: {e}")
        return {}

def monitor_tasks():
    """Main monitoring loop"""
    print("🤖 Mac Claude Task Monitor Starting")
    print("=" * 60)
    print(f"📊 Monitoring spreadsheet: {SPREADSHEET_ID}")
    print(f"⏰ Check interval: {CHECK_INTERVAL} seconds")
    print(f"🎯 Watching for tasks assigned to: Mac Claude")
    print()
    
    # Initialize Google Sheets client
    try:
        scope = ['https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/drive']
        creds = Credentials.from_service_account_file(CREDENTIALS_PATH, scopes=scope)
        gc = gspread.authorize(creds)
        sheet = gc.open_by_key(SPREADSHEET_ID)
        print("✅ Connected to Google Sheets")
    except Exception as e:
        print(f"❌ Failed to connect to Google Sheets: {e}")
        return
    
    # Load previous state
    previous_state = load_previous_state()
    print(f"📂 Loaded {len(previous_state)} tasks from previous state")
    
    while True:
        try:
            # Get current Mac Claude tasks
            current_tasks = get_mac_claude_tasks(sheet)
            
            # Check for new tasks
            for task_id, task_data in current_tasks.items():
                if task_id not in previous_state:
                    print(f"\n🆕 NEW TASK ASSIGNED TO MAC CLAUDE!")
                    print(f"   Task ID: {task_id}")
                    print(f"   Title: {task_data['title']}")
                    print(f"   Priority: {task_data['priority']}")
                    print(f"   Status: {task_data['status']}")
                    print(f"   Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                    print("   → Mac Claude should start working on this task")
                
                # Check for status changes
                elif task_data['status'] != previous_state.get(task_id, {}).get('status'):
                    old_status = previous_state.get(task_id, {}).get('status', 'Unknown')
                    print(f"\n🔄 STATUS CHANGE for {task_id}")
                    print(f"   Title: {task_data['title']}")
                    print(f"   Status: {old_status} → {task_data['status']}")
                    print(f"   Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Check for completed/removed tasks
            for task_id in previous_state:
                if task_id not in current_tasks:
                    print(f"\n✅ Task {task_id} no longer assigned to Mac Claude")
                    print(f"   (Completed or reassigned)")
            
            # Update state
            previous_state = current_tasks
            save_current_state(previous_state)
            
            # Show summary
            pending_count = sum(1 for t in current_tasks.values() if t['status'] == 'Pending')
            in_progress_count = sum(1 for t in current_tasks.values() if t['status'] == 'In Progress')
            
            print(f"\n📊 Mac Claude Task Summary [{datetime.now().strftime('%H:%M:%S')}]")
            print(f"   Total Tasks: {len(current_tasks)}")
            print(f"   Pending: {pending_count}")
            print(f"   In Progress: {in_progress_count}")
            
            # Sleep before next check
            time.sleep(CHECK_INTERVAL)
            
        except KeyboardInterrupt:
            print("\n\n🛑 Mac Claude Task Monitor stopped by user")
            break
        except Exception as e:
            print(f"\n❌ Error in monitoring loop: {e}")
            print("Retrying in 60 seconds...")
            time.sleep(60)

if __name__ == "__main__":
    monitor_tasks()