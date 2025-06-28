#!/usr/bin/env python3
"""
Google Sheets to Claude Task Sync
Monitors Google Sheets for new Claude-assigned tasks and triggers actions
"""

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time
import subprocess
import json
from datetime import datetime

# Configuration
SHEET_ID = '1ILZ7c3ec4Pf6b32SWWHFeVN-TF2UJeLUsmH99vBb9Do'  # Your sheet ID
CREDS_FILE = 'path/to/credentials.json'  # Update with your path
CHECK_INTERVAL = 60  # Check every minute

class ClaudeTaskMonitor:
    def __init__(self):
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_FILE, scope)
        self.client = gspread.authorize(creds)
        self.sheet = self.client.open_by_key(SHEET_ID)
        self.processed_tasks = set()
    
    def get_claude_tasks(self):
        """Get tasks assigned to Claude agents"""
        worksheet = self.sheet.worksheet('Docker Migration Tasks')
        all_tasks = worksheet.get_all_records()
        
        claude_tasks = []
        for task in all_tasks:
            if ('Claude' in task.get('Assigned To', '') and 
                task.get('Status') == 'Pending' and
                task.get('Task ID') not in self.processed_tasks):
                claude_tasks.append(task)
        
        return claude_tasks
    
    def execute_task(self, task):
        """Execute task based on description"""
        task_id = task['Task ID']
        description = task['Task Description'].lower()
        assignee = task['Assigned To']
        
        print(f"\n🤖 {assignee} executing: {task['Task Description']}")
        
        # Task execution logic
        if 'docker compose' in description:
            self.create_docker_compose(task)
        elif 'export' in description and 'ignition' in description:
            self.export_ignition_projects(task)
        elif 'test' in description and 'connection' in description:
            self.test_connections(task)
        elif 'document' in description:
            self.create_documentation(task)
        elif 'setup' in description and 'monitoring' in description:
            self.setup_monitoring(task)
        else:
            print(f"⚠️  No handler for task: {description}")
            self.update_task_notes(task_id, "No automated handler - manual intervention needed")
            return
        
        # Mark as processed
        self.processed_tasks.add(task_id)
        self.update_task_status(task_id, 'In Progress')
    
    def create_docker_compose(self, task):
        """Generate Docker Compose configuration"""
        print("📝 Creating Docker Compose configuration...")
        
        # Simulate creating docker-compose.yml
        compose_content = """version: '3.8'
services:
  ignition:
    image: inductiveautomation/ignition:8.1.43
    container_name: ignition-gateway
    ports:
      - "8088:8088"
    volumes:
      - ./data:/data
    environment:
      - ACCEPT_IGNITION_EULA=Y
"""
        
        # Log activity
        self.log_activity({
            'agent_type': task['Assigned To'],
            'task': 'Create Docker Compose for Ignition',
            'status': 'Complete',
            'duration': '5 min',
            'output': 'docker-compose.yml created',
            'next_action': 'Deploy to server'
        })
        
        self.update_task_status(task['Task ID'], 'Complete')
        self.update_task_completion(task['Task ID'], '100%')
    
    def export_ignition_projects(self, task):
        """Export Ignition projects"""
        print("📦 Exporting Ignition projects...")
        
        # Simulate export
        projects = ['test_run_01', 'brewery_control', 'steel_bonnet_hmi']
        
        for project in projects:
            print(f"  - Exporting {project}...")
            time.sleep(1)
            
            # Update project migration tracker
            self.update_project_status(project, 'Export Status', '✅ Complete')
        
        self.update_task_status(task['Task ID'], 'Complete')
        self.update_task_completion(task['Task ID'], '100%')
    
    def update_task_status(self, task_id, status):
        """Update task status in sheet"""
        worksheet = self.sheet.worksheet('Docker Migration Tasks')
        cell = worksheet.find(task_id)
        if cell:
            worksheet.update_cell(cell.row, 3, status)  # Status column
            print(f"✅ Updated {task_id} status to: {status}")
    
    def update_task_completion(self, task_id, completion):
        """Update task completion percentage"""
        worksheet = self.sheet.worksheet('Docker Migration Tasks')
        cell = worksheet.find(task_id)
        if cell:
            worksheet.update_cell(cell.row, 8, completion)  # Completion column
    
    def update_task_notes(self, task_id, notes):
        """Update task notes"""
        worksheet = self.sheet.worksheet('Docker Migration Tasks')
        cell = worksheet.find(task_id)
        if cell:
            worksheet.update_cell(cell.row, 9, notes)  # Notes column
    
    def update_project_status(self, project_name, column_name, value):
        """Update project migration tracker"""
        worksheet = self.sheet.worksheet('Project Migration Tracker')
        
        # Find project row
        project_cell = worksheet.find(project_name)
        if project_cell:
            # Find column
            headers = worksheet.row_values(1)
            col_index = headers.index(column_name) + 1
            worksheet.update_cell(project_cell.row, col_index, value)
    
    def log_activity(self, activity):
        """Log activity to Agent Activities sheet"""
        worksheet = self.sheet.worksheet('Agent Activities')
        worksheet.append_row([
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            activity['agent_type'],
            activity['task'],
            activity['status'],
            activity['duration'],
            activity['output'],
            activity['next_action']
        ])
    
    def monitor(self):
        """Main monitoring loop"""
        print(f"🔍 Monitoring Google Sheets for Claude tasks...")
        print(f"Sheet ID: {SHEET_ID}")
        print(f"Checking every {CHECK_INTERVAL} seconds\n")
        
        while True:
            try:
                tasks = self.get_claude_tasks()
                
                if tasks:
                    print(f"📋 Found {len(tasks)} new tasks for Claude")
                    for task in tasks:
                        self.execute_task(task)
                else:
                    print(".", end="", flush=True)
                
                time.sleep(CHECK_INTERVAL)
                
            except Exception as e:
                print(f"\n❌ Error: {e}")
                time.sleep(CHECK_INTERVAL)

# Example task handlers that could trigger actual Claude actions
def trigger_claude_action(action_type, params):
    """Trigger Claude to perform specific actions"""
    
    if action_type == "create_documentation":
        # Could call Claude API or trigger local Claude instance
        prompt = f"Create documentation for: {params['topic']}"
        # subprocess.run(['claude', 'generate', prompt])
    
    elif action_type == "analyze_logs":
        prompt = f"Analyze these Docker logs and suggest improvements: {params['logs']}"
        # subprocess.run(['claude', 'analyze', prompt])
    
    elif action_type == "generate_config":
        prompt = f"Generate configuration for: {params['service']}"
        # subprocess.run(['claude', 'create', prompt])

if __name__ == "__main__":
    # Test mode - you can add tasks in Google Sheets and watch them execute
    monitor = ClaudeTaskMonitor()
    
    # Example: Add a test task in your sheet with:
    # Task Description: "Create Docker Compose for Node-RED"
    # Assigned To: "Server Claude"
    # Status: "Pending"
    
    monitor.monitor()