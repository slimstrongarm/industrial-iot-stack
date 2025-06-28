#!/usr/bin/env python3
"""
Quick Task Manager - Simple CLI interface for MCP Task Orchestrator
Usage: python3 quick_task_manager.py [command] [args]
"""

import sys
import json
from mcp_task_orchestrator import TaskOrchestrator

def print_help():
    """Print usage help"""
    print("""
🎯 Quick Task Manager - MCP Style

Commands:
  create "Task Title" [type] [priority] [assigned_to]
  find "search term"
  status task_id new_status
  tabs
  history [count]

Examples:
  python3 quick_task_manager.py create "Fix Node-RED flow" "Node-RED Development" "High" "Server Claude"
  python3 quick_task_manager.py find "CT-084"
  python3 quick_task_manager.py status CT-101 "In Progress"
  python3 quick_task_manager.py tabs
  python3 quick_task_manager.py history 5
""")

def main():
    if len(sys.argv) < 2:
        print_help()
        return
    
    command = sys.argv[1].lower()
    orchestrator = TaskOrchestrator()
    
    if command == "create":
        if len(sys.argv) < 3:
            print("❌ Task title required")
            return
        
        title = sys.argv[2]
        task_type = sys.argv[3] if len(sys.argv) > 3 else "Infrastructure"
        priority = sys.argv[4] if len(sys.argv) > 4 else "Medium"
        assigned_to = sys.argv[5] if len(sys.argv) > 5 else "Mac Claude"
        
        result = orchestrator.create_task(
            title=title,
            task_type=task_type,
            priority=priority,
            assigned_to=assigned_to
        )
        print(json.dumps(result, indent=2))
    
    elif command == "find":
        if len(sys.argv) < 3:
            print("❌ Search term required")
            return
        
        search_term = sys.argv[2]
        result = orchestrator.find_tasks(search_term)
        print(json.dumps(result, indent=2))
    
    elif command == "status":
        if len(sys.argv) < 4:
            print("❌ Task ID and new status required")
            return
        
        task_id = sys.argv[2]
        new_status = sys.argv[3]
        result = orchestrator.update_task_status(task_id, new_status)
        print(json.dumps(result, indent=2))
    
    elif command == "tabs":
        result = orchestrator.list_tabs()
        print(json.dumps(result, indent=2))
    
    elif command == "history":
        count = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        result = orchestrator.get_recent_operations(count)
        print(json.dumps(result, indent=2))
    
    else:
        print(f"❌ Unknown command: {command}")
        print_help()

if __name__ == "__main__":
    main()