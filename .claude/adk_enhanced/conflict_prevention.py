#!/usr/bin/env python3
"""
ADK Conflict Prevention Engine
Prevents work conflicts between Mac Claude and Server Claude instances
"""

import json
import os
import requests
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from pathlib import Path


class ConflictPreventionEngine:
    """
    Conflict prevention engine for coordinating work between Claude instances.
    Prevents file editing conflicts and Git operation conflicts.
    """
    
    def __init__(self):
        self.base_path = Path(__file__).parent
        self.coordination_file = self.base_path / "instance_state" / "coordination_state.json"
        self.discord_webhook_url = self._get_discord_webhook()
        
        # Ensure coordination file exists
        self.coordination_file.parent.mkdir(parents=True, exist_ok=True)
        if not self.coordination_file.exists():
            self._initialize_coordination_state()
    
    def _get_discord_webhook(self) -> Optional[str]:
        """Get Discord webhook URL from credentials"""
        try:
            webhook_file = self.base_path.parent.parent / "credentials" / "discord_webhook.txt"
            if webhook_file.exists():
                with open(webhook_file, 'r') as f:
                    content = f.read()
                    # Extract URL from the file content
                    for line in content.split('\n'):
                        if line.startswith('Webhook URL:'):
                            return line.replace('Webhook URL:', '').strip()
        except Exception as e:
            print(f"⚠️ Could not load Discord webhook: {e}")
        return None
    
    def _initialize_coordination_state(self):
        """Initialize coordination state file"""
        initial_state = {
            "files_in_use": {},
            "git_operations": {},
            "task_assignments": {},
            "last_cleanup": datetime.now().isoformat(),
            "version": "1.0"
        }
        
        with open(self.coordination_file, 'w') as f:
            json.dump(initial_state, f, indent=2)
    
    def _load_coordination_state(self) -> Dict:
        """Load coordination state from file"""
        try:
            with open(self.coordination_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️ Could not load coordination state: {e}")
            self._initialize_coordination_state()
            return self._load_coordination_state()
    
    def _save_coordination_state(self, state: Dict):
        """Save coordination state to file"""
        try:
            with open(self.coordination_file, 'w') as f:
                json.dump(state, f, indent=2)
        except Exception as e:
            print(f"❌ Could not save coordination state: {e}")
    
    def claim_file(self, filepath: str, instance_id: str, action: str = "edit") -> bool:
        """Claim a file for editing with conflict prevention"""
        coord_state = self._load_coordination_state()
        
        # Clean up expired claims first
        self._cleanup_expired_claims(coord_state)
        
        # Normalize filepath
        filepath = str(Path(filepath).resolve())
        
        if filepath in coord_state.get("files_in_use", {}):
            current_user = coord_state["files_in_use"][filepath]
            if current_user["instance"] != instance_id:
                # File conflict detected
                self._send_conflict_alert(filepath, current_user, instance_id, action)
                return False
            else:
                # Same instance, extend the claim
                coord_state["files_in_use"][filepath]["last_activity"] = datetime.now().isoformat()
                self._save_coordination_state(coord_state)
                return True
        
        # Claim the file
        coord_state.setdefault("files_in_use", {})[filepath] = {
            "instance": instance_id,
            "action": action,
            "claimed_at": datetime.now().isoformat(),
            "last_activity": datetime.now().isoformat(),
            "estimated_duration": self._estimate_duration(action),
            "expires_at": (datetime.now() + timedelta(hours=2)).isoformat()  # 2-hour default
        }
        
        self._save_coordination_state(coord_state)
        print(f"📁 File claimed: {filepath} by {instance_id} for {action}")
        return True
    
    def release_file(self, filepath: str, instance_id: str) -> bool:
        """Release file claim"""
        coord_state = self._load_coordination_state()
        
        # Normalize filepath
        filepath = str(Path(filepath).resolve())
        
        if filepath in coord_state.get("files_in_use", {}):
            if coord_state["files_in_use"][filepath]["instance"] == instance_id:
                del coord_state["files_in_use"][filepath]
                self._save_coordination_state(coord_state)
                print(f"🔓 File released: {filepath} by {instance_id}")
                return True
            else:
                print(f"⚠️ Cannot release file {filepath}: not claimed by {instance_id}")
                return False
        
        return True  # File wasn't claimed, so "release" succeeds
    
    def claim_git_operation(self, operation: str, instance_id: str, branch: str = "main") -> bool:
        """Coordinate Git operations to prevent conflicts"""
        coord_state = self._load_coordination_state()
        
        # Clean up expired operations
        self._cleanup_expired_git_operations(coord_state)
        
        operation_key = f"{operation}:{branch}"
        
        if operation_key in coord_state.get("git_operations", {}):
            current_op = coord_state["git_operations"][operation_key]
            if current_op["instance"] != instance_id:
                self._send_git_conflict_alert(operation, branch, current_op, instance_id)
                return False
        
        # Claim the git operation
        coord_state.setdefault("git_operations", {})[operation_key] = {
            "instance": instance_id,
            "operation": operation,
            "branch": branch,
            "started_at": datetime.now().isoformat(),
            "expires_at": (datetime.now() + timedelta(minutes=30)).isoformat()  # 30-minute default
        }
        
        self._save_coordination_state(coord_state)
        print(f"🌿 Git operation claimed: {operation} on {branch} by {instance_id}")
        return True
    
    def release_git_operation(self, operation: str, instance_id: str, branch: str = "main") -> bool:
        """Release Git operation claim"""
        coord_state = self._load_coordination_state()
        
        operation_key = f"{operation}:{branch}"
        
        if operation_key in coord_state.get("git_operations", {}):
            if coord_state["git_operations"][operation_key]["instance"] == instance_id:
                del coord_state["git_operations"][operation_key]
                self._save_coordination_state(coord_state)
                print(f"🔓 Git operation released: {operation} on {branch} by {instance_id}")
                return True
        
        return True  # Operation wasn't claimed, so "release" succeeds
    
    def claim_task(self, task_id: str, instance_id: str) -> bool:
        """Claim a task to prevent duplicate work"""
        coord_state = self._load_coordination_state()
        
        if task_id in coord_state.get("task_assignments", {}):
            current_assignee = coord_state["task_assignments"][task_id]
            if current_assignee["instance"] != instance_id:
                print(f"⚠️ Task {task_id} already assigned to {current_assignee['instance']}")
                return False
        
        # Claim the task
        coord_state.setdefault("task_assignments", {})[task_id] = {
            "instance": instance_id,
            "assigned_at": datetime.now().isoformat(),
            "status": "claimed"
        }
        
        self._save_coordination_state(coord_state)
        print(f"📋 Task claimed: {task_id} by {instance_id}")
        return True
    
    def release_task(self, task_id: str, instance_id: str, status: str = "completed") -> bool:
        """Release task claim"""
        coord_state = self._load_coordination_state()
        
        if task_id in coord_state.get("task_assignments", {}):
            if coord_state["task_assignments"][task_id]["instance"] == instance_id:
                coord_state["task_assignments"][task_id].update({
                    "completed_at": datetime.now().isoformat(),
                    "status": status
                })
                self._save_coordination_state(coord_state)
                print(f"✅ Task released: {task_id} by {instance_id} ({status})")
                return True
        
        return True
    
    def _estimate_duration(self, action: str) -> str:
        """Estimate how long an action will take"""
        duration_map = {
            "edit": "15-30 minutes",
            "create": "10-20 minutes", 
            "read": "5 minutes",
            "analyze": "10-15 minutes",
            "deploy": "30-60 minutes",
            "test": "15-45 minutes"
        }
        return duration_map.get(action, "30 minutes")
    
    def _cleanup_expired_claims(self, coord_state: Dict):
        """Clean up expired file claims"""
        now = datetime.now()
        
        files_to_remove = []
        for filepath, claim in coord_state.get("files_in_use", {}).items():
            try:
                expires_at = datetime.fromisoformat(claim["expires_at"])
                if now > expires_at:
                    files_to_remove.append(filepath)
            except Exception:
                # Invalid timestamp, remove the claim
                files_to_remove.append(filepath)
        
        for filepath in files_to_remove:
            print(f"🗑️ Cleaning up expired file claim: {filepath}")
            del coord_state["files_in_use"][filepath]
    
    def _cleanup_expired_git_operations(self, coord_state: Dict):
        """Clean up expired git operations"""
        now = datetime.now()
        
        ops_to_remove = []
        for op_key, operation in coord_state.get("git_operations", {}).items():
            try:
                expires_at = datetime.fromisoformat(operation["expires_at"])
                if now > expires_at:
                    ops_to_remove.append(op_key)
            except Exception:
                # Invalid timestamp, remove the operation
                ops_to_remove.append(op_key)
        
        for op_key in ops_to_remove:
            print(f"🗑️ Cleaning up expired git operation: {op_key}")
            del coord_state["git_operations"][op_key]
    
    def _send_conflict_alert(self, filepath: str, current_user: Dict, requesting_instance: str, action: str):
        """Send Discord alert about file conflict"""
        message = f"""🚨 **FILE CONFLICT DETECTED** 🚨

📁 **File:** `{Path(filepath).name}`
🔒 **Currently in use by:** {current_user['instance']}
📝 **Current action:** {current_user['action']}
⏰ **Started:** {current_user['claimed_at']}
🔄 **Requested by:** {requesting_instance} for {action}

**Resolution needed:** Please coordinate before proceeding!"""
        
        self._post_to_discord(message, priority="urgent")
        print(f"🚨 File conflict alert sent for {filepath}")
    
    def _send_git_conflict_alert(self, operation: str, branch: str, current_op: Dict, requesting_instance: str):
        """Send Discord alert about Git conflict"""
        message = f"""🚨 **GIT CONFLICT DETECTED** 🚨

🌿 **Branch:** `{branch}`
⚡ **Operation in progress:** {current_op['operation']}
👤 **Current user:** {current_op['instance']}
⏰ **Started:** {current_op['started_at']}
🔄 **Requested by:** {requesting_instance} for {operation}

**Resolution needed:** Wait for current operation to complete!"""
        
        self._post_to_discord(message, priority="urgent")
        print(f"🚨 Git conflict alert sent for {operation} on {branch}")
    
    def _post_to_discord(self, message: str, priority: str = "info"):
        """Post message to Discord using webhook"""
        if not self.discord_webhook_url:
            print(f"📢 Discord alert: {message}")
            return
        
        try:
            # Color based on priority
            color_map = {
                "urgent": 0xFF0000,  # Red
                "warning": 0xFFA500,  # Orange
                "info": 0x0099FF     # Blue
            }
            
            embed = {
                "embeds": [{
                    "title": "🤖 ADK Conflict Prevention",
                    "description": message,
                    "color": color_map.get(priority, 0x0099FF),
                    "timestamp": datetime.now().isoformat(),
                    "footer": {
                        "text": "Industrial IoT Stack - Conflict Prevention Engine"
                    }
                }]
            }
            
            response = requests.post(self.discord_webhook_url, json=embed, timeout=10)
            if response.status_code == 204:
                print("✅ Discord alert sent successfully")
            else:
                print(f"⚠️ Discord alert failed: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Could not send Discord alert: {e}")
    
    def get_coordination_status(self) -> Dict:
        """Get current coordination status"""
        coord_state = self._load_coordination_state()
        
        # Clean up expired items
        self._cleanup_expired_claims(coord_state)
        self._cleanup_expired_git_operations(coord_state)
        self._save_coordination_state(coord_state)
        
        return {
            "files_in_use": len(coord_state.get("files_in_use", {})),
            "git_operations": len(coord_state.get("git_operations", {})),
            "task_assignments": len(coord_state.get("task_assignments", {})),
            "details": {
                "files": list(coord_state.get("files_in_use", {}).keys()),
                "git_ops": list(coord_state.get("git_operations", {}).keys()),
                "tasks": list(coord_state.get("task_assignments", {}).keys())
            }
        }


def main():
    """Test the conflict prevention engine"""
    print("🧪 Testing ADK Conflict Prevention Engine")
    
    engine = ConflictPreventionEngine()
    
    # Test file claims
    print("\n📁 File Claim Tests:")
    
    # Mac Claude claims a file
    success = engine.claim_file("test_file.py", "mac_claude", "edit")
    print(f"Mac Claude claim test_file.py: {'✅ Success' if success else '❌ Failed'}")
    
    # Server Claude tries to claim the same file (should fail)
    success = engine.claim_file("test_file.py", "server_claude", "edit") 
    print(f"Server Claude claim test_file.py: {'❌ Blocked' if not success else '⚠️ Allowed (unexpected)'}")
    
    # Mac Claude releases the file
    engine.release_file("test_file.py", "mac_claude")
    
    # Server Claude tries again (should succeed)
    success = engine.claim_file("test_file.py", "server_claude", "edit")
    print(f"Server Claude claim after release: {'✅ Success' if success else '❌ Failed'}")
    
    # Test Git operations
    print("\n🌿 Git Operation Tests:")
    
    # Mac Claude claims git commit
    success = engine.claim_git_operation("commit", "mac_claude", "main")
    print(f"Mac Claude claim git commit: {'✅ Success' if success else '❌ Failed'}")
    
    # Server Claude tries to commit (should fail)
    success = engine.claim_git_operation("commit", "server_claude", "main")
    print(f"Server Claude claim git commit: {'❌ Blocked' if not success else '⚠️ Allowed (unexpected)'}")
    
    # Test task assignments
    print("\n📋 Task Assignment Tests:")
    
    # Mac Claude claims a task
    success = engine.claim_task("CT-066", "mac_claude")
    print(f"Mac Claude claim CT-066: {'✅ Success' if success else '❌ Failed'}")
    
    # Server Claude tries to claim the same task (should fail)
    success = engine.claim_task("CT-066", "server_claude") 
    print(f"Server Claude claim CT-066: {'❌ Blocked' if not success else '⚠️ Allowed (unexpected)'}")
    
    # Show coordination status
    print(f"\n📊 Coordination Status:")
    status = engine.get_coordination_status()
    print(f"   Files in use: {status['files_in_use']}")
    print(f"   Git operations: {status['git_operations']}")
    print(f"   Task assignments: {status['task_assignments']}")
    
    # Cleanup
    engine.release_file("test_file.py", "server_claude")
    engine.release_git_operation("commit", "mac_claude", "main")
    engine.release_task("CT-066", "mac_claude", "completed")
    
    print("\n🧹 Cleanup completed")


if __name__ == "__main__":
    main()