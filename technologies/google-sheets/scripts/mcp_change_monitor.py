#!/usr/bin/env python3
"""
MCP Change Monitor - Detects manual changes to Google Sheets
Integrates with the MCP Task Orchestrator to track status changes
"""

import json
import time
from datetime import datetime
from typing import Dict, List, Set
from mcp_task_orchestrator import TaskOrchestrator

class MCPChangeMonitor:
    """Monitor Google Sheets for manual changes and sync with MCP memory"""
    
    def __init__(self, check_interval: int = 30):
        self.orchestrator = TaskOrchestrator()
        self.check_interval = check_interval
        self.last_snapshot = {}
        self.monitored_tasks: Set[str] = set()
        
    def take_snapshot(self) -> Dict:
        """Take a snapshot of current Claude Tasks sheet"""
        try:
            result = self.orchestrator.service.spreadsheets().values().get(
                spreadsheetId=self.orchestrator.spreadsheet_id,
                range="Claude Tasks!A:K"
            ).execute()
            
            values = result.get('values', [])
            if not values:
                return {}
            
            headers = values[0]
            snapshot = {}
            
            for row in values[1:]:
                if row and len(row) > 0:  # Skip empty rows
                    task_data = {headers[i]: row[i] if i < len(row) else "" 
                               for i in range(len(headers))}
                    task_id = task_data.get('Task ID', '')
                    if task_id:
                        snapshot[task_id] = task_data
                        self.monitored_tasks.add(task_id)
            
            return snapshot
            
        except Exception as e:
            print(f"❌ Error taking snapshot: {e}")
            return {}
    
    def detect_changes(self, new_snapshot: Dict) -> List[Dict]:
        """Compare snapshots and detect changes"""
        changes = []
        
        for task_id, new_data in new_snapshot.items():
            if task_id in self.last_snapshot:
                old_data = self.last_snapshot[task_id]
                
                # Check each field for changes
                for field, new_value in new_data.items():
                    old_value = old_data.get(field, "")
                    if old_value != new_value:
                        changes.append({
                            "task_id": task_id,
                            "field": field,
                            "old_value": old_value,
                            "new_value": new_value,
                            "timestamp": datetime.now().isoformat(),
                            "change_type": "manual_edit"
                        })
            else:
                # New task detected
                changes.append({
                    "task_id": task_id,
                    "field": "entire_task",
                    "old_value": None,
                    "new_value": "Task created",
                    "timestamp": datetime.now().isoformat(),
                    "change_type": "task_created"
                })
        
        return changes
    
    def log_changes_to_memory(self, changes: List[Dict]):
        """Log detected changes to MCP memory"""
        for change in changes:
            self.orchestrator._log_operation(
                "MANUAL_CHANGE_DETECTED",
                change,
                "detected"
            )
    
    def report_changes(self, changes: List[Dict]):
        """Report changes in a human-readable format"""
        if not changes:
            return
        
        print(f"\n📊 Detected {len(changes)} change(s) at {datetime.now().strftime('%H:%M:%S')}")
        print("=" * 60)
        
        for change in changes:
            task_id = change['task_id']
            field = change['field']
            old_val = change['old_value']
            new_val = change['new_value']
            
            if change['change_type'] == 'task_created':
                print(f"🆕 NEW TASK: {task_id}")
            elif field == 'Status':
                print(f"📋 {task_id}: Status changed from '{old_val}' → '{new_val}'")
            elif field == 'Priority':
                print(f"⚡ {task_id}: Priority changed from '{old_val}' → '{new_val}'")
            elif field == 'Assigned To':
                print(f"👤 {task_id}: Assigned to changed from '{old_val}' → '{new_val}'")
            elif field == 'Completed':
                print(f"✅ {task_id}: Completion date set to '{new_val}'")
            else:
                print(f"📝 {task_id}: {field} updated")
    
    def check_for_assigned_tasks(self, snapshot: Dict) -> List[str]:
        """Check for tasks assigned to current Claude instance"""
        assigned_tasks = []
        
        for task_id, task_data in snapshot.items():
            assigned_to = task_data.get('Assigned To', '')
            status = task_data.get('Status', '')
            
            # Check if task is assigned to Mac Claude and not completed
            if 'Mac Claude' in assigned_to and status in ['Not Started', 'Pending']:
                assigned_tasks.append(task_id)
        
        return assigned_tasks
    
    def start_monitoring(self, verbose: bool = True):
        """Start the monitoring loop"""
        print("🔍 Starting MCP Change Monitor...")
        print(f"📊 Monitoring Google Sheets every {self.check_interval} seconds")
        print("💡 This will detect your manual changes and sync with MCP memory")
        print("🛑 Press Ctrl+C to stop")
        print("=" * 60)
        
        # Take initial snapshot
        self.last_snapshot = self.take_snapshot()
        print(f"📸 Initial snapshot: {len(self.last_snapshot)} tasks found")
        
        try:
            while True:
                # Take new snapshot
                new_snapshot = self.take_snapshot()
                
                # Detect changes
                changes = self.detect_changes(new_snapshot)
                
                if changes:
                    # Log to MCP memory
                    self.log_changes_to_memory(changes)
                    
                    # Report changes
                    if verbose:
                        self.report_changes(changes)
                    
                    # Check for newly assigned tasks
                    assigned_tasks = self.check_for_assigned_tasks(new_snapshot)
                    if assigned_tasks:
                        print(f"\n🎯 Tasks assigned to Mac Claude: {', '.join(assigned_tasks)}")
                
                # Update snapshot
                self.last_snapshot = new_snapshot
                
                # Wait for next check
                time.sleep(self.check_interval)
                
        except KeyboardInterrupt:
            print("\n🛑 Monitoring stopped by user")
            
            # Show final summary
            recent_ops = self.orchestrator.get_recent_operations(10)
            manual_changes = [op for op in self.orchestrator.memory['operations'] 
                            if op.get('operation') == 'MANUAL_CHANGE_DETECTED']
            
            print(f"\n📊 Session Summary:")
            print(f"   - Manual changes detected: {len(manual_changes)}")
            print(f"   - Tasks monitored: {len(self.monitored_tasks)}")
            print(f"   - Total operations logged: {len(self.orchestrator.memory['operations'])}")

def quick_status_check():
    """Quick function to check current task status without continuous monitoring"""
    monitor = MCPChangeMonitor()
    snapshot = monitor.take_snapshot()
    
    print("📋 Current Claude Tasks Status")
    print("=" * 40)
    
    for task_id, task_data in snapshot.items():
        status = task_data.get('Status', 'Unknown')
        assigned_to = task_data.get('Assigned To', 'Unknown')
        description = task_data.get('Description', '')[:50] + "..." if len(task_data.get('Description', '')) > 50 else task_data.get('Description', '')
        
        if 'Claude' in assigned_to:
            status_emoji = {
                'Not Started': '⏸️',
                'Pending': '⏳',
                'In Progress': '🔄',
                'Complete': '✅',
                'Blocked': '🚫'
            }.get(status, '❓')
            
            print(f"{status_emoji} {task_id}: {status} - {description}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "status":
        # Quick status check
        quick_status_check()
    else:
        # Start continuous monitoring
        monitor = MCPChangeMonitor(check_interval=30)  # Check every 30 seconds
        monitor.start_monitoring()