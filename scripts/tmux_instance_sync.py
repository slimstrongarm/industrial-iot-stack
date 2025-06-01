#!/usr/bin/env python3
"""
TMUX Instance Synchronization System
Keeps Mac and Server TMUX instances synchronized via Git and Google Sheets
"""

import os
import json
import subprocess
from datetime import datetime
from pathlib import Path

class TMUXSync:
    def __init__(self):
        self.repo_path = Path.home() / "Desktop" / "industrial-iot-stack"
        self.instance_file = self.repo_path / "agents" / "TMUX_INSTANCES.json"
        self.session_state = self.repo_path / "agents" / "SESSION_STATE.json"
        
    def identify_instance(self):
        """Identify which TMUX instance this is."""
        hostname = subprocess.check_output(['hostname'], text=True).strip()
        
        if 'macbook' in hostname.lower() or 'mac' in hostname.lower():
            return {
                'type': 'mac',
                'name': 'claude-mac',
                'color': 'green',
                'icon': '🍎'
            }
        else:
            return {
                'type': 'server',
                'name': 'claude-server', 
                'color': 'blue',
                'icon': '🖥️'
            }
    
    def update_instance_status(self):
        """Update this instance's status in shared file."""
        instance = self.identify_instance()
        
        # Load existing instances
        instances = {}
        if self.instance_file.exists():
            with open(self.instance_file, 'r') as f:
                instances = json.load(f)
        
        # Update this instance
        instances[instance['type']] = {
            'last_seen': datetime.now().isoformat(),
            'session_name': instance['name'],
            'status': 'active',
            'current_window': self.get_current_tmux_window(),
            'identifier': instance
        }
        
        # Save
        with open(self.instance_file, 'w') as f:
            json.dump(instances, f, indent=2)
        
        # Commit and push
        self.sync_to_git(f"{instance['icon']} {instance['type'].upper()} instance active")
    
    def get_current_tmux_window(self):
        """Get current TMUX window name."""
        try:
            window = subprocess.check_output(
                ['tmux', 'display-message', '-p', '#W'],
                text=True
            ).strip()
            return window
        except:
            return 'unknown'
    
    def sync_to_git(self, message):
        """Sync changes to git."""
        try:
            subprocess.run(['git', 'add', '-A'], cwd=self.repo_path)
            subprocess.run(['git', 'commit', '-m', message], cwd=self.repo_path)
            subprocess.run(['git', 'push'], cwd=self.repo_path)
            print(f"✅ Synced: {message}")
        except Exception as e:
            print(f"⚠️ Sync failed: {e}")
    
    def check_other_instance(self):
        """Check status of the other instance."""
        if not self.instance_file.exists():
            print("⚠️ No other instance detected yet")
            return
        
        with open(self.instance_file, 'r') as f:
            instances = json.load(f)
        
        my_type = self.identify_instance()['type']
        other_type = 'server' if my_type == 'mac' else 'mac'
        
        if other_type in instances:
            other = instances[other_type]
            last_seen = datetime.fromisoformat(other['last_seen'])
            age = (datetime.now() - last_seen).total_seconds() / 60
            
            print(f"\n{other['identifier']['icon']} Other Instance: {other_type.upper()}")
            print(f"   Last active: {int(age)} minutes ago")
            print(f"   Status: {other['status']}")
            print(f"   Current window: {other['current_window']}")
    
    def update_google_sheets_status(self):
        """Update Google Sheets with instance status."""
        instance = self.identify_instance()
        
        # This would update a "System Status" tab in sheets
        # Showing which instances are active
        print(f"📊 Would update Google Sheets: {instance['type']} instance active")

if __name__ == "__main__":
    sync = TMUXSync()
    
    # Update our status
    sync.update_instance_status()
    
    # Check other instance
    sync.check_other_instance()
    
    # Update sheets
    sync.update_google_sheets_status()