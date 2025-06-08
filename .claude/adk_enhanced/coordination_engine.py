#!/usr/bin/env python3
"""
ADK Coordination Engine
Intelligently assigns tasks between Mac Claude and Server Claude instances
"""

import json
import os
from datetime import datetime
from typing import Dict, Any, List, Optional
from pathlib import Path


class TaskCoordinationEngine:
    """
    Intelligent task assignment engine for Mac Claude and Server Claude.
    Analyzes task requirements and assigns to the most suitable instance.
    """
    
    def __init__(self):
        self.base_path = Path(__file__).parent
        self.coordination_file = self.base_path / "instance_state" / "coordination_state.json"
        
        # Instance capabilities
        self.instance_capabilities = {
            "mac_claude": {
                "strengths": [
                    "local_development",
                    "discord_bot_management", 
                    "google_sheets_integration",
                    "documentation_updates",
                    "mobile_workflows",
                    "python_scripting",
                    "file_editing"
                ],
                "tools": [
                    "Edit", "Write", "Read", "Bash", "Glob", "Grep",
                    "TodoRead", "TodoWrite", "WebFetch", "WebSearch"
                ],
                "max_concurrent_tasks": 3,
                "working_hours": "24/7"
            },
            "server_claude": {
                "strengths": [
                    "docker_operations",
                    "system_administration", 
                    "production_deployments",
                    "infrastructure_monitoring",
                    "service_management",
                    "database_operations",
                    "network_configuration"
                ],
                "tools": [
                    "Bash", "Docker", "SystemD", "SSH", "NetworkTools",
                    "MonitoringTools", "DeploymentTools"
                ],
                "max_concurrent_tasks": 5,
                "working_hours": "24/7"
            }
        }
        
        # Task type patterns
        self.task_patterns = {
            "discord": {"preferred": "mac_claude", "confidence": 0.95},
            "docker": {"preferred": "server_claude", "confidence": 0.95},
            "google_sheets": {"preferred": "mac_claude", "confidence": 0.90},
            "deployment": {"preferred": "server_claude", "confidence": 0.90},
            "documentation": {"preferred": "mac_claude", "confidence": 0.85},
            "monitoring": {"preferred": "server_claude", "confidence": 0.85},
            "python_script": {"preferred": "mac_claude", "confidence": 0.80},
            "system_admin": {"preferred": "server_claude", "confidence": 0.90},
            "file_editing": {"preferred": "mac_claude", "confidence": 0.75},
            "infrastructure": {"preferred": "server_claude", "confidence": 0.85}
        }
    
    def smart_assign(self, task_description: str, current_workload: Dict = None) -> Dict:
        """Intelligently assign task to best instance"""
        
        if current_workload is None:
            current_workload = self._get_current_workload()
        
        # Analyze task
        analysis = self._analyze_task(task_description)
        
        # Check workload
        workload_check = self._check_workload_balance(current_workload)
        
        # Make assignment decision
        assignment = self._make_assignment_decision(analysis, workload_check)
        
        # Save coordination state
        self._save_assignment(task_description, assignment)
        
        return {
            "assigned_to": assignment["instance"],
            "reasoning": assignment["reasoning"],
            "confidence": assignment["confidence"],
            "dependencies": analysis.get("dependencies", []),
            "estimated_duration": analysis.get("estimated_duration", "unknown"),
            "priority": analysis.get("priority", "medium"),
            "task_type": analysis.get("task_type", "general")
        }
    
    def _analyze_task(self, task_description: str) -> Dict:
        """Analyze task complexity and requirements"""
        task_lower = task_description.lower()
        
        # Detect task type based on keywords
        task_type = "general"
        confidence = 0.5
        
        for pattern, config in self.task_patterns.items():
            if pattern in task_lower:
                task_type = pattern
                confidence = config["confidence"]
                break
        
        # Detect specific keywords for higher accuracy
        keyword_analysis = {
            "discord": ["discord", "bot", "webhook", "message", "channel"],
            "docker": ["docker", "container", "compose", "image", "deployment"],
            "google_sheets": ["sheets", "spreadsheet", "google", "row", "column"],
            "monitoring": ["monitor", "health", "status", "alert", "dashboard"],
            "documentation": ["doc", "readme", "markdown", "guide", "instructions"],
            "python_script": ["python", "script", "py", "pip", "install"],
            "system_admin": ["system", "service", "admin", "configuration", "setup"],
            "infrastructure": ["server", "network", "infrastructure", "production"]
        }
        
        for category, keywords in keyword_analysis.items():
            if any(keyword in task_lower for keyword in keywords):
                if category in self.task_patterns:
                    task_type = category
                    confidence = self.task_patterns[category]["confidence"]
                    break
        
        # Estimate complexity
        complexity = "simple"
        if any(word in task_lower for word in ["complex", "multi", "integration", "full"]):
            complexity = "complex"
        elif any(word in task_lower for word in ["implement", "create", "build", "setup"]):
            complexity = "medium"
        
        # Estimate duration
        duration_estimates = {
            "simple": "15-30 minutes",
            "medium": "30-90 minutes", 
            "complex": "2-6 hours"
        }
        
        # Detect dependencies
        dependencies = []
        if "after" in task_lower or "depends" in task_lower:
            dependencies.append("has_dependencies")
        if "google sheets" in task_lower:
            dependencies.append("google_sheets_access")
        if "discord" in task_lower:
            dependencies.append("discord_credentials")
        
        return {
            "task_type": task_type,
            "complexity": complexity,
            "estimated_duration": duration_estimates[complexity],
            "confidence": confidence,
            "dependencies": dependencies,
            "priority": self._estimate_priority(task_description),
            "analysis_timestamp": datetime.now().isoformat()
        }
    
    def _estimate_priority(self, task_description: str) -> str:
        """Estimate task priority"""
        task_lower = task_description.lower()
        
        if any(word in task_lower for word in ["urgent", "critical", "emergency", "asap"]):
            return "high"
        elif any(word in task_lower for word in ["important", "priority", "soon"]):
            return "medium"
        else:
            return "medium"  # Default to medium
    
    def _check_workload_balance(self, current_workload: Dict) -> Dict:
        """Check current workload of instances"""
        mac_load = current_workload.get("mac_claude", 0)
        server_load = current_workload.get("server_claude", 0)
        
        mac_capacity = self.instance_capabilities["mac_claude"]["max_concurrent_tasks"]
        server_capacity = self.instance_capabilities["server_claude"]["max_concurrent_tasks"]
        
        return {
            "mac_claude": {
                "current_load": mac_load,
                "capacity": mac_capacity,
                "utilization": mac_load / mac_capacity,
                "available": mac_capacity - mac_load > 0
            },
            "server_claude": {
                "current_load": server_load,
                "capacity": server_capacity,
                "utilization": server_load / server_capacity,
                "available": server_capacity - server_load > 0
            }
        }
    
    def _make_assignment_decision(self, analysis: Dict, workload_check: Dict) -> Dict:
        """Make final assignment decision"""
        task_type = analysis["task_type"]
        
        # Get preferred instance for task type
        if task_type in self.task_patterns:
            preferred = self.task_patterns[task_type]["preferred"]
            base_confidence = self.task_patterns[task_type]["confidence"]
        else:
            # Default assignment logic
            preferred = "mac_claude"  # Default to Mac Claude for general tasks
            base_confidence = 0.6
        
        # Check if preferred instance is available
        if not workload_check[preferred]["available"]:
            # Switch to other instance if preferred is overloaded
            other_instance = "server_claude" if preferred == "mac_claude" else "mac_claude"
            if workload_check[other_instance]["available"]:
                assigned_instance = other_instance
                confidence = base_confidence * 0.8  # Reduce confidence for non-preferred
                reasoning = f"Assigned to {assigned_instance} due to {preferred} being at capacity"
            else:
                # Both instances full, assign to less loaded
                mac_util = workload_check["mac_claude"]["utilization"]
                server_util = workload_check["server_claude"]["utilization"]
                assigned_instance = "mac_claude" if mac_util <= server_util else "server_claude"
                confidence = 0.5
                reasoning = f"Both instances loaded, assigned to {assigned_instance} (lower utilization)"
        else:
            assigned_instance = preferred
            confidence = base_confidence
            reasoning = f"Assigned to {assigned_instance} based on task type '{task_type}' and availability"
        
        return {
            "instance": assigned_instance,
            "reasoning": reasoning,
            "confidence": confidence,
            "decision_timestamp": datetime.now().isoformat()
        }
    
    def _get_current_workload(self) -> Dict:
        """Get current workload from state files"""
        try:
            workload = {"mac_claude": 0, "server_claude": 0}
            
            # Check for active state files
            state_dir = self.base_path / "instance_state"
            if state_dir.exists():
                for state_file in state_dir.glob("*_state.json"):
                    instance_id = state_file.stem.replace("_state", "")
                    if instance_id in workload:
                        try:
                            with open(state_file, 'r') as f:
                                state = json.load(f)
                            # Count active tasks
                            current_tasks = state.get("current_tasks", [])
                            active_tasks = [t for t in current_tasks if t.get("status") == "in_progress"]
                            workload[instance_id] = len(active_tasks)
                        except Exception:
                            pass
            
            return workload
            
        except Exception as e:
            print(f"⚠️ Could not get current workload: {e}")
            return {"mac_claude": 0, "server_claude": 0}
    
    def _save_assignment(self, task_description: str, assignment: Dict):
        """Save assignment decision to coordination state"""
        try:
            # Load existing coordination state
            coord_state = {}
            if self.coordination_file.exists():
                with open(self.coordination_file, 'r') as f:
                    coord_state = json.load(f)
            
            # Add new assignment
            if "assignments" not in coord_state:
                coord_state["assignments"] = []
            
            coord_state["assignments"].append({
                "task_description": task_description,
                "assignment": assignment,
                "timestamp": datetime.now().isoformat()
            })
            
            # Keep only last 50 assignments
            coord_state["assignments"] = coord_state["assignments"][-50:]
            
            # Save coordination state
            self.coordination_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.coordination_file, 'w') as f:
                json.dump(coord_state, f, indent=2)
                
        except Exception as e:
            print(f"⚠️ Could not save assignment: {e}")
    
    def get_assignment_history(self, limit: int = 10) -> List[Dict]:
        """Get recent assignment history"""
        try:
            if self.coordination_file.exists():
                with open(self.coordination_file, 'r') as f:
                    coord_state = json.load(f)
                assignments = coord_state.get("assignments", [])
                return assignments[-limit:]
            return []
        except Exception as e:
            print(f"⚠️ Could not get assignment history: {e}")
            return []
    
    def get_instance_stats(self) -> Dict:
        """Get instance utilization statistics"""
        history = self.get_assignment_history(50)
        
        stats = {
            "mac_claude": {"assigned": 0, "total": 0},
            "server_claude": {"assigned": 0, "total": 0}
        }
        
        for assignment in history:
            assigned_to = assignment["assignment"]["instance"]
            if assigned_to in stats:
                stats[assigned_to]["assigned"] += 1
            stats[assigned_to]["total"] += 1
        
        # Calculate percentages
        total_assignments = len(history)
        if total_assignments > 0:
            for instance in stats:
                stats[instance]["percentage"] = (stats[instance]["assigned"] / total_assignments) * 100
        
        return stats


def main():
    """Test the coordination engine"""
    print("🧪 Testing ADK Coordination Engine")
    
    engine = TaskCoordinationEngine()
    
    # Test various task types
    test_tasks = [
        "Update Discord bot webhook configuration",
        "Deploy Docker containers to production server", 
        "Create Google Sheets monitoring dashboard",
        "Install Python packages and update requirements",
        "Configure system monitoring alerts",
        "Update documentation with new API endpoints"
    ]
    
    print("\n🎯 Task Assignment Tests:")
    for i, task in enumerate(test_tasks, 1):
        print(f"\n{i}. Task: {task}")
        assignment = engine.smart_assign(task)
        print(f"   ✅ Assigned to: {assignment['assigned_to']}")
        print(f"   🎯 Confidence: {assignment['confidence']:.0%}")
        print(f"   💭 Reasoning: {assignment['reasoning']}")
        print(f"   📋 Type: {assignment['task_type']}")
    
    print(f"\n📊 Assignment Statistics:")
    stats = engine.get_instance_stats()
    for instance, data in stats.items():
        print(f"   {instance}: {data['assigned']}/{data['total']} ({data.get('percentage', 0):.1f}%)")


if __name__ == "__main__":
    main()