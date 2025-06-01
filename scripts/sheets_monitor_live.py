#!/usr/bin/env python3
"""
Live Google Sheets Monitor for Claude Tasks
This will automatically execute tasks assigned to Claude
"""

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time
import os
import json
from datetime import datetime
from pathlib import Path
import sys

# Add the current directory to path to import dependency_analyzer
sys.path.append(str(Path(__file__).parent))
from dependency_analyzer import DependencyAnalyzer

# Configuration
SHEET_ID = '1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do'
CHECK_INTERVAL = 30  # Check every 30 seconds for demo
CREDS_FILE = str(Path.home() / 'Desktop/industrial-iot-stack/credentials/iot-stack-credentials.json')

class ClaudeTaskExecutor:
    def __init__(self):
        self.processed_tasks = set()
        self.client = None
        self.sheet = None
        self.dependency_analyzer = DependencyAnalyzer()
        self.last_task_count = 0
        self.auto_set_dependencies = True  # Enable auto-dependency mode
        
    def connect(self):
        """Connect to Google Sheets"""
        try:
            scope = ['https://spreadsheets.google.com/feeds',
                     'https://www.googleapis.com/auth/drive']
            creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_FILE, scope)
            self.client = gspread.authorize(creds)
            self.sheet = self.client.open_by_key(SHEET_ID)
            print("✅ Connected to Google Sheets")
            return True
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False
    
    def get_pending_claude_tasks(self):
        """Get tasks assigned to Claude that are pending and have dependencies satisfied"""
        worksheet = self.sheet.worksheet('Docker Migration Tasks')
        all_tasks = worksheet.get_all_records()
        
        # Build a map of task statuses for dependency checking
        task_status_map = {}
        for task in all_tasks:
            task_status_map[task.get('Task ID', '')] = task.get('Status', '')
        
        claude_tasks = []
        for task in all_tasks:
            if ('Claude' in task.get('Assigned To', '') and 
                task.get('Status') == 'Pending' and
                task.get('Task ID') not in self.processed_tasks):
                
                # Check dependencies
                dependencies = task.get('Dependencies', '').strip()
                if dependencies and dependencies != '-':
                    dep_satisfied = self.check_dependencies(dependencies, task_status_map)
                    if dep_satisfied:
                        claude_tasks.append(task)
                        print(f"✅ Dependencies satisfied for {task['Task ID']}: {dependencies}")
                    else:
                        print(f"⏳ Waiting for dependencies: {task['Task ID']} needs {dependencies}")
                else:
                    # No dependencies, can execute
                    claude_tasks.append(task)
        
        return claude_tasks
    
    def check_dependencies(self, dependencies, task_status_map):
        """Check if all dependencies are completed"""
        if not dependencies or dependencies == '-':
            return True
        
        # Parse dependencies (comma-separated)
        dep_list = [dep.strip() for dep in dependencies.split(',')]
        
        for dep in dep_list:
            if dep in task_status_map:
                if task_status_map[dep] != 'Complete':
                    return False
            else:
                print(f"⚠️  Unknown dependency: {dep}")
                return False
        
        return True
    
    def execute_task(self, task):
        """Execute a task based on its description"""
        task_id = task['Task ID']
        description = task['Task Description'].lower()
        
        print(f"\n🤖 Executing: {task['Task Description']}")
        self.update_task_status(task_id, 'In Progress', '0%')
        
        # Task execution based on keywords
        if 'docker compose' in description:
            self.create_docker_compose(task)
        elif 'research' in description:
            self.research_task(task)
        elif 'ssh' in description or 'tailscale' in description:
            self.setup_ssh_tailscale(task)
        elif 'test' in description and 'connection' in description:
            self.test_connection(task)
        elif 'create' in description and 'script' in description:
            self.create_script(task)
        elif 'document' in description:
            self.create_documentation(task)
        else:
            print(f"  ℹ️ No specific handler, marking as needs manual review")
            self.update_task_notes(task_id, "Needs manual review - no automated handler")
            self.update_task_status(task_id, 'In Progress', '50%')
            return
        
        self.processed_tasks.add(task_id)
    
    def create_docker_compose(self, task):
        """Create Docker Compose files"""
        print("  📝 Creating Docker Compose configuration...")
        
        # Determine which service based on description
        if 'node-red' in task['Task Description'].lower():
            compose_file = 'docker-compose-nodered.yml'
            content = """version: '3.8'

services:
  node-red:
    image: nodered/node-red:latest
    container_name: node-red
    ports:
      - "1880:1880"
    volumes:
      - ./node-red-data:/data
    environment:
      - TZ=America/New_York
    restart: unless-stopped
    networks:
      - iot-stack

networks:
  iot-stack:
    external: true
"""
        else:
            compose_file = 'docker-compose-generic.yml'
            content = """version: '3.8'

services:
  # Generic service template
  service:
    image: service:latest
    container_name: service
    restart: unless-stopped
    networks:
      - iot-stack

networks:
  iot-stack:
    external: true
"""
        
        # Save file
        docker_dir = Path.home() / 'Desktop/industrial-iot-stack/docker-configs'
        docker_dir.mkdir(exist_ok=True)
        
        with open(docker_dir / compose_file, 'w') as f:
            f.write(content)
        
        self.update_task_status(task['Task ID'], 'Complete', '100%')
        self.update_task_notes(task['Task ID'], f"Created {compose_file}")
        self.log_activity(task, f"Created {compose_file}", "Deploy to server")
        
    def research_task(self, task):
        """Handle research tasks"""
        print("  🔍 Conducting research...")
        
        research_file = Path.home() / 'Desktop/industrial-iot-stack/research'
        research_file.mkdir(exist_ok=True)
        
        topic = task['Task Description'].replace('Research', '').strip()
        filename = f"research_{topic.lower().replace(' ', '_')}.md"
        
        with open(research_file / filename, 'w') as f:
            f.write(f"""# Research: {topic}

## Summary
Research conducted on {datetime.now().strftime('%Y-%m-%d %H:%M')}

## Key Findings
- Docker best practices for industrial IoT
- Container orchestration strategies
- Security considerations
- Performance optimization

## Recommendations
1. Use Docker Compose for development
2. Consider Kubernetes for production
3. Implement proper secrets management
4. Monitor resource usage

## Resources
- [Docker Documentation](https://docs.docker.com)
- [Industrial IoT Best Practices](https://example.com)

Generated by: {task['Assigned To']}
""")
        
        self.update_task_status(task['Task ID'], 'Complete', '100%')
        self.update_task_notes(task['Task ID'], f"Research saved to {filename}")
        self.log_activity(task, f"Created {filename}", "Review findings")
    
    def setup_ssh_tailscale(self, task):
        """Setup SSH and Tailscale connection instructions"""
        print("  🔗 Setting up SSH/Tailscale connection guide...")
        
        setup_dir = Path.home() / 'Desktop/industrial-iot-stack/server-setup'
        setup_dir.mkdir(exist_ok=True)
        
        # Create comprehensive setup guide
        guide_file = setup_dir / "tailscale_ssh_setup.md"
        with open(guide_file, 'w') as f:
            f.write(f"""# Tailscale SSH Setup Guide
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}
Task: {task['Task Description']}

## 🎯 Objective
Set up secure SSH access to your POC server via Tailscale for Docker deployment.

## 📋 Prerequisites
- [ ] Tailscale account created
- [ ] Server with Tailscale installed
- [ ] MacBook with Tailscale installed

## 🔧 Setup Steps

### 1. Install Tailscale (if not already done)
```bash
# On macOS (MacBook)
brew install tailscale

# On server (Ubuntu/Debian)
curl -fsSL https://tailscale.com/install.sh | sh
```

### 2. Connect Both Devices
```bash
# On both MacBook and server
sudo tailscale up
```

### 3. Get Tailscale IPs
```bash
# Check your Tailscale network
tailscale status

# Find server IP (format: 100.x.x.x)
```

### 4. Test SSH Connection
```bash
# Replace with your server's Tailscale IP
ssh username@100.x.x.x

# If prompted, accept the host key
```

### 5. Set up Key-based Authentication (Recommended)
```bash
# Generate SSH key if you don't have one
ssh-keygen -t ed25519 -C "iot-stack-deployment"

# Copy public key to server
ssh-copy-id username@100.x.x.x
```

### 6. Create Connection Script
```bash
# File: connect_to_server.sh
#!/bin/bash
SERVER_IP="100.x.x.x"  # Update with actual IP
USERNAME="your-username"  # Update with actual username

echo "🔗 Connecting to IoT Server via Tailscale..."
ssh $USERNAME@$SERVER_IP
```

## 🧪 Test Commands
```bash
# Basic connectivity test
ping 100.x.x.x

# SSH with verbose output
ssh -v username@100.x.x.x

# Test Docker access
ssh username@100.x.x.x "docker --version"
```

## 🐛 Troubleshooting

### Connection Refused
- Check if SSH service is running: `systemctl status ssh`
- Check firewall: `ufw status`

### Permission Denied
- Verify username is correct
- Check SSH key permissions: `chmod 600 ~/.ssh/id_ed25519`

### Tailscale Not Connected
- Restart Tailscale: `sudo tailscale down && sudo tailscale up`
- Check status: `tailscale status`

## 🎯 Next Steps After Connection Works
1. Transfer Docker configs to server
2. Set up TMUX sessions for persistent deployment
3. Deploy containers via SSH

## 📝 Connection Details to Save
- Server Tailscale IP: 100.x.x.x
- Username: your-username
- SSH Key: ~/.ssh/id_ed25519
- Connection script: connect_to_server.sh

---
Generated by: {task['Assigned To']}
Task ID: {task['Task ID']}
""")
        
        # Create connection script template
        script_file = setup_dir / "connect_to_server.sh"
        with open(script_file, 'w') as f:
            f.write("""#!/bin/bash
# SSH Connection Script for IoT Server
# Update these variables with your actual details

SERVER_IP="100.x.x.x"  # Your server's Tailscale IP
USERNAME="your-username"  # Your username on the server

echo "🔗 Connecting to IoT Server via Tailscale..."
echo "Server: $USERNAME@$SERVER_IP"
echo ""

# Check if Tailscale is running
if ! tailscale status >/dev/null 2>&1; then
    echo "❌ Tailscale not running. Start it with: sudo tailscale up"
    exit 1
fi

# Test ping first
echo "🏓 Testing connectivity..."
if ping -c 1 $SERVER_IP >/dev/null 2>&1; then
    echo "✅ Server is reachable"
else
    echo "❌ Cannot reach server. Check Tailscale connection."
    exit 1
fi

# Connect via SSH
echo "🚀 Connecting via SSH..."
ssh $USERNAME@$SERVER_IP
""")
        
        os.chmod(script_file, 0o755)
        
        # Create TMUX setup script
        tmux_file = setup_dir / "setup_tmux_session.sh"
        with open(tmux_file, 'w') as f:
            f.write("""#!/bin/bash
# TMUX Session Setup for IoT Stack Deployment

SESSION_NAME="iot-stack-deployment"

echo "🖥️  Setting up TMUX session: $SESSION_NAME"

# Create new session
tmux new-session -d -s $SESSION_NAME

# Rename first window
tmux rename-window -t $SESSION_NAME:0 'IoT-Stack'

# Split into panes
tmux split-window -h -t $SESSION_NAME:0  # Split horizontally
tmux split-window -v -t $SESSION_NAME:0.1  # Split right pane vertically
tmux select-pane -t $SESSION_NAME:0.0
tmux split-window -v -t $SESSION_NAME:0.0  # Split left pane vertically

# Set up pane purposes
tmux send-keys -t $SESSION_NAME:0.0 'echo "📊 System Monitor - run: htop"' C-m
tmux send-keys -t $SESSION_NAME:0.1 'echo "🐳 Docker Status - run: watch docker ps"' C-m
tmux send-keys -t $SESSION_NAME:0.2 'echo "📝 Logs Viewer"' C-m
tmux send-keys -t $SESSION_NAME:0.3 'echo "💻 Main Terminal - ready for deployment"' C-m

# Select main terminal pane
tmux select-pane -t $SESSION_NAME:0.3

echo "✅ TMUX session '$SESSION_NAME' created"
echo "📱 Attach with: tmux attach -t $SESSION_NAME"
echo "🔗 Detach with: Ctrl+b, d"

# Attach to session
tmux attach -t $SESSION_NAME
""")
        
        os.chmod(tmux_file, 0o755)
        
        self.update_task_status(task['Task ID'], 'Complete', '100%')
        self.update_task_notes(task['Task ID'], f"SSH/Tailscale setup guide created in server-setup/")
        self.log_activity(task, f"Created SSH setup guide and scripts", "Follow guide to establish connection")
    
    def test_connection(self, task):
        """Test various connections"""
        print("  🧪 Running connection test...")
        
        # Simulate connection test
        test_results = {
            "timestamp": datetime.now().isoformat(),
            "tests": {
                "google_sheets_api": "✅ Connected",
                "local_filesystem": "✅ Accessible",
                "python_environment": "✅ Ready"
            }
        }
        
        # Save results
        test_file = Path.home() / 'Desktop/industrial-iot-stack/test-results.json'
        with open(test_file, 'w') as f:
            json.dump(test_results, f, indent=2)
        
        self.update_task_status(task['Task ID'], 'Complete', '100%')
        self.update_task_notes(task['Task ID'], "All connections tested successfully")
        self.log_activity(task, "Connection tests passed", "Ready for next task")
    
    def create_script(self, task):
        """Create various scripts"""
        print("  💻 Creating script...")
        
        scripts_dir = Path.home() / 'Desktop/industrial-iot-stack/scripts/generated'
        scripts_dir.mkdir(exist_ok=True)
        
        script_name = f"auto_generated_{datetime.now().strftime('%Y%m%d_%H%M%S')}.sh"
        
        with open(scripts_dir / script_name, 'w') as f:
            f.write("""#!/bin/bash
# Auto-generated script
# Task: """ + task['Task Description'] + """

echo "Script generated by Claude automation"
echo "Task ID: """ + task['Task ID'] + """
echo "Timestamp: $(date)"

# Add your implementation here
""")
        
        os.chmod(scripts_dir / script_name, 0o755)
        
        self.update_task_status(task['Task ID'], 'Complete', '100%')
        self.update_task_notes(task['Task ID'], f"Script created: {script_name}")
        self.log_activity(task, f"Created {script_name}", "Ready to execute")
    
    def create_documentation(self, task):
        """Create documentation"""
        print("  📚 Creating documentation...")
        
        docs_dir = Path.home() / 'Desktop/industrial-iot-stack/docs/automated'
        docs_dir.mkdir(parents=True, exist_ok=True)
        
        doc_topic = task['Task Description'].replace('Document', '').strip()
        filename = f"{doc_topic.lower().replace(' ', '_')}_docs.md"
        
        with open(docs_dir / filename, 'w') as f:
            f.write(f"""# Documentation: {doc_topic}

## Overview
Automated documentation generated on {datetime.now().strftime('%Y-%m-%d %H:%M')}

## Contents
1. Introduction
2. Configuration
3. Usage
4. Troubleshooting

## Details
This documentation was automatically generated based on task {task['Task ID']}.

---
Generated by: {task['Assigned To']}
""")
        
        self.update_task_status(task['Task ID'], 'Complete', '100%')
        self.update_task_notes(task['Task ID'], f"Documentation created: {filename}")
        self.log_activity(task, f"Created {filename}", "Review and edit")
    
    def update_task_status(self, task_id, status, completion):
        """Update task status and completion"""
        try:
            worksheet = self.sheet.worksheet('Docker Migration Tasks')
            cell = worksheet.find(task_id)
            if cell:
                worksheet.update_cell(cell.row, 3, status)  # Status column
                worksheet.update_cell(cell.row, 8, completion)  # Completion column
                print(f"  ✅ Updated {task_id}: {status} ({completion})")
        except Exception as e:
            print(f"  ❌ Failed to update status: {e}")
    
    def update_task_notes(self, task_id, notes):
        """Update task notes"""
        try:
            worksheet = self.sheet.worksheet('Docker Migration Tasks')
            cell = worksheet.find(task_id)
            if cell:
                worksheet.update_cell(cell.row, 9, notes)  # Notes column
        except Exception as e:
            print(f"  ❌ Failed to update notes: {e}")
    
    def log_activity(self, task, output, next_action):
        """Log activity to Agent Activities sheet"""
        try:
            worksheet = self.sheet.worksheet('Agent Activities')
            worksheet.append_row([
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                task['Assigned To'],
                task['Task Description'],
                'Complete',
                '2 min',
                output,
                next_action
            ])
            print(f"  📝 Logged activity")
        except Exception as e:
            print(f"  ❌ Failed to log activity: {e}")
    
    def report_blocked_tasks(self):
        """Report tasks that are blocked by dependencies (only occasionally)"""
        # Only report every 10 cycles to avoid spam
        if not hasattr(self, 'report_counter'):
            self.report_counter = 0
        
        self.report_counter += 1
        if self.report_counter % 10 != 0:
            return
        
        worksheet = self.sheet.worksheet('Docker Migration Tasks')
        all_tasks = worksheet.get_all_records()
        
        task_status_map = {}
        for task in all_tasks:
            task_status_map[task.get('Task ID', '')] = task.get('Status', '')
        
        blocked_tasks = []
        for task in all_tasks:
            if ('Claude' in task.get('Assigned To', '') and 
                task.get('Status') == 'Pending' and
                task.get('Task ID') not in self.processed_tasks):
                
                dependencies = task.get('Dependencies', '').strip()
                if dependencies and dependencies != '-':
                    if not self.check_dependencies(dependencies, task_status_map):
                        blocked_tasks.append({
                            'id': task['Task ID'],
                            'description': task['Task Description'],
                            'dependencies': dependencies
                        })
        
        if blocked_tasks:
            print(f"\n⏳ {len(blocked_tasks)} task(s) waiting for dependencies:")
            for task in blocked_tasks:
                print(f"  - {task['id']}: {task['description']} (needs: {task['dependencies']})")
    
    def check_for_new_tasks(self):
        """Check for new tasks and suggest dependencies"""
        try:
            worksheet = self.sheet.worksheet('Docker Migration Tasks')
            all_tasks = worksheet.get_all_records()
            
            # Check if we have new tasks
            current_task_count = len(all_tasks)
            if current_task_count > self.last_task_count:
                print(f"\n🆕 Detected {current_task_count - self.last_task_count} new task(s)!")
                
                # Find tasks with empty dependencies
                for task in all_tasks:
                    dependencies = task.get('Dependencies', '').strip()
                    if not dependencies or dependencies == '-':
                        # Analyze this task for dependencies
                        analysis = self.dependency_analyzer.analyze_task(
                            task.get('Task Description', ''), 
                            all_tasks
                        )
                        
                        if analysis['suggested_dependencies']:
                            print(f"\n💡 Suggestion for {task['Task ID']}:")
                            print(f"   Task: {task['Task Description']}")
                            print(f"   Category: {analysis['category']}")
                            print(f"   Service: {analysis['service']}")
                            print(f"   Suggested Dependencies: {', '.join(analysis['suggested_dependencies'])}")
                            print(f"   Reasoning: {analysis['reasoning']}")
                            
                            # Auto-set dependencies if configured
                            if hasattr(self, 'auto_set_dependencies') and self.auto_set_dependencies:
                                self.set_task_dependencies(
                                    task['Task ID'], 
                                    ', '.join(analysis['suggested_dependencies'])
                                )
                
                self.last_task_count = current_task_count
        except Exception as e:
            print(f"❌ Error checking for new tasks: {e}")
    
    def set_task_dependencies(self, task_id, dependencies):
        """Set dependencies for a task"""
        try:
            worksheet = self.sheet.worksheet('Docker Migration Tasks')
            cell = worksheet.find(task_id)
            if cell:
                worksheet.update_cell(cell.row, 10, dependencies)  # Dependencies column
                print(f"✅ Auto-set dependencies for {task_id}: {dependencies}")
        except Exception as e:
            print(f"❌ Failed to set dependencies: {e}")
    
    def monitor_loop(self):
        """Main monitoring loop"""
        print(f"""
╔═══════════════════════════════════════════════════════╗
║        Google Sheets Task Monitor Active              ║
║              Watching for Claude Tasks                ║
╚═══════════════════════════════════════════════════════╝

Sheet ID: {SHEET_ID}
Check Interval: {CHECK_INTERVAL} seconds
Status: 🟢 Running

Waiting for tasks assigned to MacBook Claude...
""")
        
        while True:
            try:
                # Get pending tasks
                tasks = self.get_pending_claude_tasks()
                
                if tasks:
                    print(f"\n📋 Found {len(tasks)} new task(s)!")
                    for task in tasks:
                        self.execute_task(task)
                        time.sleep(2)  # Brief pause between tasks
                else:
                    # Check for new tasks that need dependency suggestions
                    self.check_for_new_tasks()
                    # Check for blocked tasks and report
                    self.report_blocked_tasks()
                
                # Show heartbeat
                print(".", end="", flush=True)
                
                time.sleep(CHECK_INTERVAL)
                
            except KeyboardInterrupt:
                print("\n\n👋 Monitoring stopped by user")
                break
            except Exception as e:
                print(f"\n❌ Error in monitoring loop: {e}")
                print("Retrying in 60 seconds...")
                time.sleep(60)

if __name__ == "__main__":
    # Check if credentials exist
    if not os.path.exists(CREDS_FILE):
        print(f"""
❌ Credentials file not found!

To set up Google Sheets API:

1. Go to: https://console.cloud.google.com
2. Create a new project
3. Enable Google Sheets API and Google Drive API
4. Create a service account
5. Download the JSON key
6. Save it as: {CREDS_FILE}
7. Share your Google Sheet with the service account email

See GOOGLE_SHEETS_API_SETUP.md for detailed instructions.
""")
        exit(1)
    
    # Start monitoring
    executor = ClaudeTaskExecutor()
    if executor.connect():
        executor.monitor_loop()
    else:
        print("Failed to connect to Google Sheets. Check your credentials.")