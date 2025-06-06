#!/usr/bin/env python3
"""
Unified monitoring system that tracks both Google Sheets tasks and n8n workflows
"""

from googleapiclient.discovery import build
from google.oauth2 import service_account
import requests
from datetime import datetime
import time
import json
import os

# Google Sheets Configuration
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'credentials/iot-stack-credentials.json'
SPREADSHEET_ID = '1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do'

# n8n Configuration
# Update this when Server Claude provides the n8n URL
N8N_BASE_URL = os.environ.get('N8N_URL', "http://localhost:5678")
N8N_USERNAME = os.environ.get('N8N_USERNAME', "iiot-admin")
N8N_PASSWORD = os.environ.get('N8N_PASSWORD', "StrongPassword123!")

# Server n8n URL (via Tailscale or direct)
# N8N_BASE_URL = "http://100.94.84.126:5678"  # Update with actual server IP

class UnifiedMonitor:
    """Monitor both Google Sheets tasks and n8n workflows"""
    
    def __init__(self):
        # Initialize Google Sheets
        self.sheets_service = self._init_sheets()
        
        # Initialize n8n session
        self.n8n_session = requests.Session()
        self.n8n_session.auth = (N8N_USERNAME, N8N_PASSWORD)
        
        # State tracking
        self.last_tasks = {}
        self.last_executions = set()
        self.workflow_cache = {}
    
    def _init_sheets(self):
        """Initialize Google Sheets service"""
        try:
            credentials = service_account.Credentials.from_service_account_file(
                SERVICE_ACCOUNT_FILE, scopes=SCOPES)
            service = build('sheets', 'v4', credentials=credentials)
            return service.spreadsheets()
        except Exception as e:
            print(f"⚠️  Error initializing sheets: {e}")
            return None
    
    def check_sheets_tasks(self):
        """Check for Google Sheets task updates"""
        if not self.sheets_service:
            return []
        
        try:
            result = self.sheets_service.values().get(
                spreadsheetId=SPREADSHEET_ID,
                range='Claude Tasks!A:J'
            ).execute()
            
            values = result.get('values', [])
            current_tasks = {}
            
            for i, row in enumerate(values[1:], 1):  # Skip header
                if len(row) >= 5:
                    task_id = row[0]
                    current_tasks[task_id] = {
                        'instance': row[1],
                        'status': row[4],
                        'description': row[5] if len(row) > 5 else '',
                        'completed': row[9] if len(row) > 9 else ''
                    }
            
            # Detect changes
            changes = []
            for task_id, task in current_tasks.items():
                if task_id not in self.last_tasks:
                    changes.append(('new_task', task_id, task))
                elif self.last_tasks[task_id]['status'] != task['status']:
                    changes.append(('status_change', task_id, task))
                elif not self.last_tasks[task_id].get('completed') and task.get('completed'):
                    changes.append(('completed', task_id, task))
            
            self.last_tasks = current_tasks
            return changes
            
        except Exception as e:
            print(f"⚠️  Error checking sheets: {e}")
            return []
    
    def check_n8n_workflows(self):
        """Check n8n workflow status and executions"""
        changes = []
        
        try:
            # Get workflow status
            response = self.n8n_session.get(f"{N8N_BASE_URL}/api/v1/workflows")
            if response.status_code == 200:
                workflows = response.json().get('data', [])
                
                for workflow in workflows:
                    wf_id = workflow['id']
                    wf_name = workflow['name']
                    wf_active = workflow['active']
                    
                    # Check if this is a workflow we care about
                    if any(keyword in wf_name.lower() for keyword in ['mqtt', 'whatsapp', 'formbricks']):
                        if wf_id not in self.workflow_cache:
                            changes.append(('new_workflow', wf_id, wf_name, wf_active))
                        elif self.workflow_cache[wf_id] != wf_active:
                            changes.append(('workflow_status', wf_id, wf_name, wf_active))
                        
                        self.workflow_cache[wf_id] = wf_active
            
            # Get recent executions
            response = self.n8n_session.get(f"{N8N_BASE_URL}/api/v1/executions?limit=10")
            if response.status_code == 200:
                executions = response.json().get('data', [])
                
                for execution in executions:
                    exec_id = execution['id']
                    if exec_id not in self.last_executions:
                        workflow_name = execution.get('workflowData', {}).get('name', 'Unknown')
                        status = 'success' if execution.get('finished') else 'error'
                        changes.append(('new_execution', exec_id, workflow_name, status))
                        self.last_executions.add(exec_id)
            
        except Exception as e:
            print(f"⚠️  Error checking n8n: {e}")
        
        return changes
    
    def format_notification(self, change_type, *args):
        """Format change notification"""
        if change_type == 'new_task':
            task_id, task = args
            return f"🆕 NEW TASK: {task_id} ({task['instance']})\n   📋 {task['description'][:60]}..."
        
        elif change_type == 'status_change':
            task_id, task = args
            return f"🔄 TASK UPDATE: {task_id} → {task['status']}\n   📋 {task['description'][:60]}..."
        
        elif change_type == 'completed':
            task_id, task = args
            return f"✅ COMPLETED: {task_id}\n   📋 {task['description'][:60]}..."
        
        elif change_type == 'new_workflow':
            wf_id, wf_name, active = args
            icon = "✅" if active else "⏸️"
            return f"📱 NEW WORKFLOW: {wf_name}\n   Status: {icon} {'Active' if active else 'Inactive'}"
        
        elif change_type == 'workflow_status':
            wf_id, wf_name, active = args
            icon = "✅" if active else "⏸️"
            return f"🔄 WORKFLOW STATUS: {wf_name}\n   Changed to: {icon} {'Active' if active else 'Inactive'}"
        
        elif change_type == 'new_execution':
            exec_id, wf_name, status = args
            icon = "✅" if status == 'success' else "❌"
            return f"⚡ WORKFLOW EXECUTED: {wf_name}\n   Result: {icon} {status}"
        
        return str(args)
    
    def monitor_once(self):
        """Single monitoring check"""
        all_changes = []
        
        # Check Google Sheets
        sheets_changes = self.check_sheets_tasks()
        all_changes.extend([('sheets', *change) for change in sheets_changes])
        
        # Check n8n
        n8n_changes = self.check_n8n_workflows()
        all_changes.extend([('n8n', *change) for change in n8n_changes])
        
        if all_changes:
            print(f"\n🚨 {len(all_changes)} UPDATE(S) DETECTED at {datetime.now().strftime('%H:%M:%S')}!")
            print("="*60)
            
            # Group by source
            sheets_updates = [c for c in all_changes if c[0] == 'sheets']
            n8n_updates = [c for c in all_changes if c[0] == 'n8n']
            
            if sheets_updates:
                print("\n📊 GOOGLE SHEETS UPDATES:")
                for update in sheets_updates:
                    print(self.format_notification(*update[1:]))
                    print()
            
            if n8n_updates:
                print("\n🔧 N8N UPDATES:")
                for update in n8n_updates:
                    print(self.format_notification(*update[1:]))
                    print()
            
            # Special notifications
            if any('CT-007' in str(c) and 'Complete' in str(c) for c in all_changes):
                print("🎉 MILESTONE: n8n workflows imported! Ready for testing!")
            
            if any('whatsapp' in str(c).lower() and 'success' in str(c) for c in all_changes):
                print("📱 SUCCESS: WhatsApp alert sent successfully!")
            
            return True
        else:
            print(f"⏰ Checked at {datetime.now().strftime('%H:%M:%S')} - No changes", end='\r')
            return False
    
    def monitor_continuous(self, interval=30):
        """Continuous monitoring"""
        print("🔄 Starting Unified Monitoring System")
        print("📊 Monitoring: Google Sheets tasks + n8n workflows")
        print(f"⏱️  Check interval: {interval} seconds")
        print("Press Ctrl+C to stop\n")
        
        # Initial status
        print("🔍 Initial scan...")
        self.check_sheets_tasks()  # Populate initial state
        self.check_n8n_workflows()  # Populate initial state
        print(f"✅ Tracking {len(self.last_tasks)} tasks and {len(self.workflow_cache)} workflows")
        print()
        
        try:
            check_count = 0
            while True:
                check_count += 1
                
                if self.monitor_once():
                    print("\n" + "="*60 + "\n")
                
                # Status update every 10 checks
                if check_count % 10 == 0:
                    print(f"\n📈 Status: {check_count} checks completed")
                
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print(f"\n\n👋 Monitoring stopped after {check_count} checks")


def main():
    """Main entry point"""
    import sys
    
    print("🚀 Industrial IoT Stack - Unified Monitoring")
    print("="*45)
    
    monitor = UnifiedMonitor()
    
    if len(sys.argv) > 1 and sys.argv[1] == 'once':
        monitor.monitor_once()
    else:
        interval = int(sys.argv[1]) if len(sys.argv) > 1 else 30
        monitor.monitor_continuous(interval)


if __name__ == "__main__":
    main()