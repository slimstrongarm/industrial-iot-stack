#!/bin/bash
# Mac Claude MCP Monitor Startup

echo "🟢 Starting Mac Claude MCP Monitor..."
echo "===================================="

cd /Users/joshpayneair/Desktop/industrial-iot-stack/technologies/google-sheets/scripts

# Start the change monitor with Mac Claude context
python3 -c "
import sys
sys.path.append('.')
from mcp_change_monitor import MCPChangeMonitor
from datetime import datetime

class MacClaudeMonitor(MCPChangeMonitor):
    def check_for_assigned_tasks(self, snapshot):
        '''Check for tasks assigned to Mac Claude'''
        assigned_tasks = []
        
        for task_id, task_data in snapshot.items():
            assigned_to = task_data.get('Assigned To', '')
            status = task_data.get('Status', '')
            
            # Check if task is assigned to Mac Claude
            if 'Mac Claude' in assigned_to and status in ['Start', 'Not Started', 'Pending']:
                assigned_tasks.append(task_id)
        
        return assigned_tasks
    
    def report_changes(self, changes):
        '''Report changes with Mac Claude context'''
        if not changes:
            return
        
        print(f'\n🟢 Mac Claude detected {len(changes)} change(s) at {datetime.now().strftime(\"%H:%M:%S\")}')
        print('=' * 60)
        
        for change in changes:
            task_id = change['task_id']
            field = change['field']
            new_val = change['new_value']
            
            if field == 'Status' and new_val == 'Start':
                print(f'🚀 {task_id}: Ready to START! Status changed to \"{new_val}\"')
                print(f'💡 Task: {change.get(\"description\", \"\")}')
                # Auto-update to In Progress
                print(f'🔄 Auto-updating {task_id} to \"In Progress\"...')
            elif field == 'Status':
                print(f'📋 {task_id}: Status changed to \"{new_val}\"')
            else:
                super().report_changes([change])

# Start Mac Claude monitoring
print('🟢 Mac Claude MCP Monitor starting...')
print('💡 Monitoring for tasks assigned to Mac Claude')
print('🎯 Will detect \"Start\" status changes and auto-respond')
print('⚡ Real-time awareness active!')
print('=' * 60)

monitor = MacClaudeMonitor(check_interval=10)  # Check every 10 seconds for responsiveness
monitor.start_monitoring()
"