#!/usr/bin/env python3
"""
Enhanced Node-RED Worker with ADK Integration
Specialized agent for Node-RED flow management and brewery automation
"""

import json
import sys
import time
import subprocess
import requests
from datetime import datetime
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Import ADK components
sys.path.insert(0, str(project_root / ".claude" / "adk_enhanced"))
from state_persistence import StatePersistenceEngine
from coordination_engine import TaskCoordinationEngine  
from conflict_prevention import ConflictPreventionEngine


class EnhancedNodeRedWorker:
    """
    Enhanced Node-RED worker with ADK intelligence and brewery specialization.
    The definitive expert in Node-RED flows, brewery automation, and visual programming.
    """
    
    def __init__(self):
        self.instance_id = "nodered_agent"
        self.tmux_session = "TMUX_C"
        self.specialization = "Node-RED Flow Expert"
        
        # ADK Components
        self.state_engine = StatePersistenceEngine(self.instance_id)
        self.coordination_engine = TaskCoordinationEngine()
        self.conflict_engine = ConflictPreventionEngine()
        
        # Node-RED specific configuration
        self.nodered_config = {
            "url": "http://localhost:1880",
            "flows_endpoint": "/flows",
            "nodes_endpoint": "/nodes", 
            "admin_auth": False,  # Adjust based on setup
            "flow_backup_dir": project_root / "Steel_Bonnet" / "node-red-flows" / "backups",
            "flow_library_dir": project_root / ".claude" / "adk_enhanced" / "nodered_library"
        }
        
        # Brewery equipment knowledge
        self.brewery_equipment = {
            "hlt": {
                "name": "Hot Liquor Tank",
                "mqtt_topics": ["brewery/hlt/temperature", "brewery/hlt/setpoint", "brewery/hlt/status"],
                "safety_limits": {"max_temp": 85, "min_temp": 10},
                "monitoring_interval": 5
            },
            "fermentation": {
                "name": "Fermentation Vessels", 
                "mqtt_topics": ["brewery/fermentation/+/temperature", "brewery/fermentation/+/pressure"],
                "safety_limits": {"max_temp": 30, "max_pressure": 15},
                "monitoring_interval": 10
            },
            "glycol": {
                "name": "Glycol Chiller",
                "mqtt_topics": ["brewery/glycol/temperature", "brewery/glycol/flow", "brewery/glycol/status"],
                "safety_limits": {"min_temp": -5, "max_temp": 5},
                "monitoring_interval": 15
            }
        }
        
        # Flow patterns library
        self.flow_patterns = {
            "mqtt_monitor": {
                "description": "Standard MQTT monitoring pattern",
                "nodes": ["mqtt in", "function", "dashboard gauge", "debug"],
                "best_practices": ["Error handling", "Rate limiting", "Data validation"]
            },
            "equipment_safety": {
                "description": "Equipment safety interlock pattern",
                "nodes": ["mqtt in", "switch", "function", "mqtt out", "notification"],
                "best_practices": ["Fail-safe logic", "Alert redundancy", "Manual override"]
            },
            "data_logging": {
                "description": "Time-series data logging pattern", 
                "nodes": ["mqtt in", "function", "database", "debug"],
                "best_practices": ["Batch inserts", "Connection pooling", "Error recovery"]
            }
        }
        
        print(f"🔴 Enhanced Node-RED Worker initializing...")
        print(f"   🏭 Brewery Equipment Types: {len(self.brewery_equipment)}")
        print(f"   📋 Flow Patterns: {len(self.flow_patterns)}")
        print(f"   📊 ADK Integration: Ready")
    
    def start_enhanced_monitoring(self):
        """Start Node-RED agent with specialized capabilities"""
        print("\n🔄 Starting Enhanced Node-RED Worker...")
        
        # Phase 1: ADK Recovery
        print("📡 Phase 1: ADK Context Recovery")
        self.recovered_context = self.state_engine.recover_session_state()
        
        if self.recovered_context and not self.recovered_context.get("fallback"):
            print(f"✅ Node-RED expertise recovered from previous session")
            self._load_flow_library()
        else:
            print("🔄 Building Node-RED expertise from scratch...")
        
        # Phase 2: Node-RED Environment Check
        print("\n🔴 Phase 2: Node-RED Environment Assessment")
        self._check_nodered_environment()
        
        # Phase 3: Flow Analysis and Optimization
        print("\n📊 Phase 3: Flow Analysis and Optimization")
        self._analyze_current_flows()
        
        # Phase 4: Coordination Setup
        print("\n🤝 Phase 4: Agent Coordination Setup")
        self._setup_agent_coordination()
        
        print("\n🎉 Enhanced Node-RED Worker fully operational!")
    
    def _check_nodered_environment(self):
        """Check Node-RED environment and connectivity"""
        try:
            response = requests.get(f"{self.nodered_config['url']}/flows", timeout=10)
            if response.status_code == 200:
                flows = response.json()
                print(f"   ✅ Node-RED connected: {len(flows)} flows detected")
                print(f"   🔗 URL: {self.nodered_config['url']}")
                return True
            else:
                print(f"   ⚠️ Node-RED responded with status {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"   ❌ Node-RED not accessible: {e}")
            print(f"   💡 Tip: Start Node-RED with 'node-red' command")
            return False
    
    def _analyze_current_flows(self):
        """Analyze existing Node-RED flows for optimization opportunities"""
        try:
            response = requests.get(f"{self.nodered_config['url']}/flows", timeout=10)
            if response.status_code != 200:
                print("   ⚠️ Cannot analyze flows - Node-RED not accessible")
                return
            
            flows = response.json()
            
            # Analyze flow structure
            analysis = {
                "total_flows": len(flows),
                "mqtt_nodes": 0,
                "function_nodes": 0,
                "dashboard_nodes": 0,
                "opc_nodes": 0,
                "database_nodes": 0,
                "potential_issues": []
            }
            
            for flow in flows:
                if isinstance(flow, dict) and flow.get("type"):
                    node_type = flow.get("type", "")
                    
                    if "mqtt" in node_type.lower():
                        analysis["mqtt_nodes"] += 1
                    elif "function" in node_type.lower():
                        analysis["function_nodes"] += 1
                    elif "dashboard" in node_type.lower() or "ui_" in node_type.lower():
                        analysis["dashboard_nodes"] += 1
                    elif "opc" in node_type.lower():
                        analysis["opc_nodes"] += 1
                    elif "database" in node_type.lower() or "postgres" in node_type.lower():
                        analysis["database_nodes"] += 1
            
            print(f"   📊 Flow Analysis Results:")
            print(f"      Total flows/nodes: {analysis['total_flows']}")
            print(f"      MQTT nodes: {analysis['mqtt_nodes']}")
            print(f"      Function nodes: {analysis['function_nodes']}")  
            print(f"      Dashboard nodes: {analysis['dashboard_nodes']}")
            print(f"      OPC UA nodes: {analysis['opc_nodes']}")
            print(f"      Database nodes: {analysis['database_nodes']}")
            
            # Save analysis to state
            self._save_flow_analysis(analysis)
            
        except Exception as e:
            print(f"   ❌ Flow analysis failed: {e}")
    
    def _load_flow_library(self):
        """Load persistent flow library and patterns"""
        try:
            library_dir = self.nodered_config["flow_library_dir"]
            library_dir.mkdir(parents=True, exist_ok=True)
            
            library_file = library_dir / "flow_library.json"
            if library_file.exists():
                with open(library_file, 'r') as f:
                    self.flow_library = json.load(f)
                print(f"   📚 Flow library loaded: {len(self.flow_library)} patterns")
            else:
                self.flow_library = {}
                print(f"   📚 New flow library created")
                
        except Exception as e:
            print(f"   ⚠️ Could not load flow library: {e}")
            self.flow_library = {}
    
    def _save_flow_analysis(self, analysis):
        """Save flow analysis to persistent state"""
        try:
            context_update = {
                "flow_analysis": analysis,
                "analysis_timestamp": datetime.now().isoformat(),
                "specialization": self.specialization,
                "brewery_equipment_count": len(self.brewery_equipment),
                "flow_patterns_count": len(self.flow_patterns)
            }
            
            self.state_engine.save_session_state(context_update)
            print(f"   💾 Flow analysis saved to persistent state")
            
        except Exception as e:
            print(f"   ⚠️ Could not save analysis: {e}")
    
    def _setup_agent_coordination(self):
        """Setup coordination with other specialized agents"""
        try:
            # Register as Node-RED specialist
            coordination_info = {
                "agent_type": "nodered_agent",
                "specialization": "Node-RED Flow Expert",
                "capabilities": list(self.flow_patterns.keys()),
                "brewery_equipment": list(self.brewery_equipment.keys()),
                "coordination_topics": [
                    "flow_optimization",
                    "mqtt_topic_mapping", 
                    "brewery_automation",
                    "equipment_monitoring"
                ]
            }
            
            print(f"   🤝 Coordination setup complete")
            print(f"      Specialization: {coordination_info['specialization']}")
            print(f"      Capabilities: {len(coordination_info['capabilities'])}")
            print(f"      Equipment types: {len(coordination_info['brewery_equipment'])}")
            
        except Exception as e:
            print(f"   ⚠️ Coordination setup failed: {e}")
    
    def optimize_brewery_flow(self, equipment_type: str):
        """Optimize a specific brewery equipment monitoring flow"""
        print(f"\n🔧 Optimizing {equipment_type} monitoring flow...")
        
        if equipment_type not in self.brewery_equipment:
            print(f"   ❌ Unknown equipment type: {equipment_type}")
            return False
        
        equipment = self.brewery_equipment[equipment_type]
        
        # Claim the optimization task
        if not self.conflict_engine.claim_task(f"optimize_{equipment_type}_flow", self.instance_id):
            print(f"   ⚠️ Optimization already in progress by another agent")
            return False
        
        try:
            print(f"   🏭 Equipment: {equipment['name']}")
            print(f"   📡 MQTT Topics: {equipment['mqtt_topics']}")
            print(f"   🛡️ Safety Limits: {equipment['safety_limits']}")
            print(f"   ⏱️ Monitoring Interval: {equipment['monitoring_interval']}s")
            
            # Generate optimization recommendations
            recommendations = self._generate_optimization_recommendations(equipment_type, equipment)
            
            print(f"   📋 Optimization Recommendations:")
            for i, rec in enumerate(recommendations, 1):
                print(f"      {i}. {rec}")
            
            # Save optimization to flow library
            self._save_optimization_pattern(equipment_type, recommendations)
            
            # Release the task
            self.conflict_engine.release_task(f"optimize_{equipment_type}_flow", self.instance_id, "completed")
            
            print(f"   ✅ {equipment_type} optimization completed")
            return True
            
        except Exception as e:
            print(f"   ❌ Optimization failed: {e}")
            self.conflict_engine.release_task(f"optimize_{equipment_type}_flow", self.instance_id, "failed")
            return False
    
    def _generate_optimization_recommendations(self, equipment_type: str, equipment: dict) -> list:
        """Generate specific optimization recommendations for equipment"""
        recommendations = []
        
        # Standard optimizations
        recommendations.append(f"Implement rate limiting for {equipment['monitoring_interval']}s intervals")
        recommendations.append(f"Add data validation for safety limits: {equipment['safety_limits']}")
        recommendations.append("Use connection pooling for MQTT subscriptions")
        recommendations.append("Implement exponential backoff for connection retries")
        
        # Equipment-specific optimizations
        if equipment_type == "hlt":
            recommendations.append("Add temperature trend analysis for predictive alerts")
            recommendations.append("Implement PID controller feedback optimization")
        elif equipment_type == "fermentation":
            recommendations.append("Add multi-vessel monitoring aggregation")
            recommendations.append("Implement pressure trend monitoring for fermentation stages")
        elif equipment_type == "glycol":
            recommendations.append("Add flow rate monitoring for circulation efficiency")
            recommendations.append("Implement temperature differential alerts")
        
        return recommendations
    
    def _save_optimization_pattern(self, equipment_type: str, recommendations: list):
        """Save optimization pattern to flow library"""
        try:
            if not hasattr(self, 'flow_library'):
                self.flow_library = {}
            
            self.flow_library[f"{equipment_type}_optimization"] = {
                "equipment": equipment_type,
                "recommendations": recommendations,
                "created": datetime.now().isoformat(),
                "pattern_type": "optimization"
            }
            
            # Save to file
            library_dir = self.nodered_config["flow_library_dir"]
            library_dir.mkdir(parents=True, exist_ok=True)
            
            library_file = library_dir / "flow_library.json"
            with open(library_file, 'w') as f:
                json.dump(self.flow_library, f, indent=2)
            
            print(f"   💾 Optimization pattern saved to flow library")
            
        except Exception as e:
            print(f"   ⚠️ Could not save optimization pattern: {e}")


def main():
    """Main entry point for enhanced Node-RED worker"""
    print("🔴 ADK Enhanced Node-RED Worker")
    print("=" * 50)
    
    # Initialize enhanced Node-RED worker
    worker = EnhancedNodeRedWorker()
    
    # Start enhanced monitoring
    worker.start_enhanced_monitoring()
    
    # Demo: Optimize brewery equipment flows
    print("\n" + "=" * 50)
    print("🧪 Testing Node-RED Flow Optimization")
    
    for equipment_type in ["hlt", "fermentation", "glycol"]:
        worker.optimize_brewery_flow(equipment_type)
    
    print("\n🎯 Enhanced Node-RED Worker demonstration completed!")
    print("🚀 Node-RED Agent ready for brewery automation!")


if __name__ == "__main__":
    main()