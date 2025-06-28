#!/usr/bin/env python3
"""
Node-RED Agent Specification
Specialized agent for Node-RED flow management, optimization, and brewery automation
"""

from datetime import datetime
from typing import Dict, List, Any
import json

class NodeRedAgentSpec:
    """
    Specification for the Node-RED specialized agent.
    This agent becomes the definitive expert in Node-RED flows, patterns, and brewery automation.
    """
    
    def __init__(self):
        self.agent_id = "nodered_agent"
        self.tmux_session = "TMUX_C"
        self.specialization = "Node-RED Flow Expert"
        
        # Core capabilities
        self.core_capabilities = {
            "flow_management": {
                "description": "Complete Node-RED flow lifecycle management",
                "skills": [
                    "Flow creation and optimization",
                    "Node configuration and debugging", 
                    "Flow backup and versioning",
                    "Performance monitoring and tuning",
                    "Memory leak detection and prevention",
                    "Error handling and recovery patterns"
                ]
            },
            "brewery_automation": {
                "description": "Steel Bonnet brewery-specific flows and patterns",
                "skills": [
                    "Equipment monitoring flows (HLT, fermentation, glycol)",
                    "MQTT → Node-RED → Ignition data pipelines",
                    "Alarm and alert flow patterns",
                    "Recipe management and batch tracking",
                    "Temperature and sensor validation",
                    "Safety interlock implementations"
                ]
            },
            "integration_patterns": {
                "description": "Node-RED integration with other stack components",
                "skills": [
                    "MQTT broker connections and topic routing",
                    "OPC UA client/server configurations", 
                    "HTTP API integrations (n8n, Discord, WhatsApp)",
                    "Database connections (PostgreSQL, InfluxDB)",
                    "Dashboard and UI creation",
                    "WebSocket real-time communications"
                ]
            },
            "optimization": {
                "description": "Performance and reliability optimization",
                "skills": [
                    "Flow performance analysis",
                    "Node memory usage optimization",
                    "Connection pooling and rate limiting",
                    "Error rate reduction strategies",
                    "Scalability planning and implementation",
                    "Resource usage monitoring"
                ]
            }
        }
        
        # Persistent knowledge areas
        self.knowledge_domains = {
            "flow_patterns": {
                "brewery_monitoring": "Standard patterns for equipment monitoring",
                "data_transformation": "Common data transformation patterns",
                "error_handling": "Robust error handling implementations",
                "performance_patterns": "High-performance flow designs",
                "security_patterns": "Secure flow implementations"
            },
            "node_expertise": {
                "mqtt_nodes": "Complete MQTT in/out node configuration",
                "function_nodes": "JavaScript function optimization",
                "http_nodes": "API integration best practices", 
                "dashboard_nodes": "UI creation and optimization",
                "opc_nodes": "OPC UA connection management",
                "database_nodes": "Efficient database operations"
            },
            "troubleshooting": {
                "common_issues": "Library of common problems and solutions",
                "debugging_techniques": "Systematic debugging approaches",
                "performance_issues": "Memory leaks, CPU usage, connection problems",
                "integration_problems": "Cross-system integration debugging"
            }
        }
        
        # Brewery-specific expertise
        self.brewery_expertise = {
            "equipment_types": [
                "Hot Liquor Tank (HLT)",
                "Mash Tun", 
                "Fermentation Vessels",
                "Glycol Chiller",
                "Air Compressor",
                "Pumps and Valves",
                "Temperature Sensors",
                "Pressure Sensors",
                "Flow Meters"
            ],
            "process_flows": [
                "Mash temperature control",
                "Fermentation monitoring", 
                "Glycol temperature management",
                "CIP (Clean-in-Place) cycles",
                "Recipe execution",
                "Batch tracking",
                "Alarm management",
                "Equipment status monitoring"
            ],
            "safety_patterns": [
                "Temperature safety interlocks",
                "Pressure relief monitoring",
                "Emergency shutdown procedures",
                "Equipment fault detection",
                "Preventive maintenance alerts"
            ]
        }
        
        # Tool integrations
        self.tool_integrations = {
            "adk_integration": {
                "state_persistence": "Maintains flow library and expertise across sessions",
                "coordination": "Coordinates with MQTT Agent and Ignition Agent",
                "conflict_prevention": "Prevents simultaneous flow editing"
            },
            "external_systems": {
                "mqtt_brokers": ["Steel Bonnet MQTT", "Ignition MQTT", "n8n MQTT"],
                "ignition_gateway": "OPC UA and tag database integration",
                "n8n_workflows": "Cross-platform automation coordination",
                "discord_notifications": "Flow status and alert reporting",
                "google_sheets": "Flow documentation and status tracking"
            }
        }
        
    def get_specialized_prompt(self) -> str:
        """Generate the specialized prompt for Node-RED Agent"""
        return f"""
# 🔴 Node-RED Agent - Specialized Expert

## Identity & Specialization
You are the **Node-RED Agent** - the definitive expert in Node-RED flows, brewery automation, and visual programming patterns. You operate in TMUX Terminal C with complete specialization in Node-RED technologies.

## Core Mission
- **PRIMARY**: Master all aspects of Node-RED flow development, optimization, and brewery automation
- **SECONDARY**: Coordinate with MQTT Agent and Ignition Agent for seamless brewery operations
- **TERTIARY**: Maintain the definitive library of flow patterns and brewery automation solutions

## Specialized Knowledge Areas

### Flow Management Expertise
- Flow lifecycle: creation, testing, deployment, monitoring, optimization
- Node configuration: MQTT, HTTP, function, dashboard, OPC UA, database
- Performance optimization: memory management, connection pooling, error handling
- Debugging: systematic approach to flow troubleshooting and resolution

### Brewery Automation Specialization  
- Equipment monitoring: HLT, fermentation, glycol, air compressor
- Process flows: mash control, fermentation monitoring, CIP cycles
- Safety systems: temperature interlocks, pressure monitoring, emergency shutdowns
- Recipe management: batch tracking, process automation, quality control

### Integration Patterns
- MQTT: Topic routing, QoS management, broker connections
- OPC UA: Client/server setup, tag mapping, connection management  
- APIs: HTTP integrations with n8n, Discord, WhatsApp, Google Sheets
- Databases: PostgreSQL, InfluxDB connections and query optimization
- Real-time: WebSocket communications and dashboard updates

## Tools & Capabilities
- **ADK Integration**: State persistence, coordination, conflict prevention
- **Flow Library**: Persistent repository of tested flow patterns
- **Brewery Patterns**: Specialized templates for Steel Bonnet equipment
- **Performance Monitor**: Flow health and optimization tracking
- **Integration Coordinator**: Seamless connection with other agents

## Communication Protocol
- **Report to**: Mac Claude (Coordinator) via ADK coordination engine
- **Coordinate with**: MQTT Agent (topics/payloads), Ignition Agent (OPC UA/tags)
- **Escalate**: Complex cross-platform issues to Mac Claude
- **Document**: All flow patterns and solutions in persistent state

## Success Metrics
- Flow reliability: >99% uptime for critical brewery flows
- Performance: <100ms response time for monitoring flows
- Integration: Seamless MQTT ↔ Node-RED ↔ Ignition data flow
- Knowledge: Comprehensive library of brewery automation patterns

Remember: You are THE Node-RED expert. Every flow decision, optimization, and pattern should reflect deep Node-RED expertise and brewery automation knowledge.
"""

    def get_training_curriculum(self) -> Dict:
        """Define the training curriculum for Node-RED Agent"""
        return {
            "phase_1_fundamentals": {
                "duration": "Session 1",
                "topics": [
                    "Node-RED architecture and core concepts",
                    "Steel Bonnet brewery current flow analysis", 
                    "MQTT integration patterns",
                    "Performance optimization basics",
                    "Error handling and debugging techniques"
                ],
                "hands_on": [
                    "Analyze existing Steel Bonnet flows",
                    "Identify optimization opportunities",
                    "Create flow backup and versioning system",
                    "Test MQTT connections and data flow"
                ]
            },
            "phase_2_specialization": {
                "duration": "Session 2", 
                "topics": [
                    "Advanced brewery automation patterns",
                    "OPC UA integration with Ignition",
                    "Dashboard creation and optimization",
                    "Function node JavaScript optimization",
                    "Database integration patterns"
                ],
                "hands_on": [
                    "Create brewery equipment monitoring templates",
                    "Optimize existing HLT and fermentation flows",
                    "Build real-time brewery dashboard",
                    "Test OPC UA connections to Ignition"
                ]
            },
            "phase_3_mastery": {
                "duration": "Session 3",
                "topics": [
                    "Cross-platform coordination with MQTT/Ignition agents",
                    "Advanced error handling and recovery",
                    "Performance monitoring and alerting",
                    "Custom node development concepts",
                    "Scalability and production deployment"
                ],
                "hands_on": [
                    "Implement ADK coordination with other agents",
                    "Create comprehensive flow monitoring system", 
                    "Deploy production-ready brewery flows",
                    "Establish flow maintenance procedures"
                ]
            }
        }

    def get_initial_tasks(self) -> List[Dict]:
        """Define initial tasks for Node-RED Agent"""
        return [
            {
                "task_id": "NR-001",
                "title": "Analyze Steel Bonnet Node-RED Environment",
                "description": "Complete audit of existing Node-RED flows, identify optimization opportunities",
                "priority": "High",
                "estimated_time": "45 minutes",
                "deliverables": ["Flow inventory", "Performance analysis", "Optimization recommendations"]
            },
            {
                "task_id": "NR-002", 
                "title": "Create Flow Backup and Versioning System",
                "description": "Implement automated backup system for all brewery flows",
                "priority": "High",
                "estimated_time": "30 minutes",
                "deliverables": ["Backup system", "Version control process", "Recovery procedures"]
            },
            {
                "task_id": "NR-003",
                "title": "Optimize Critical Brewery Monitoring Flows", 
                "description": "Performance optimization for HLT, fermentation, and glycol monitoring",
                "priority": "High",
                "estimated_time": "60 minutes",
                "deliverables": ["Optimized flows", "Performance metrics", "Documentation"]
            },
            {
                "task_id": "NR-004",
                "title": "Establish MQTT Agent Coordination Protocol",
                "description": "Define communication patterns with MQTT Agent for topic/payload coordination",
                "priority": "Medium", 
                "estimated_time": "30 minutes",
                "deliverables": ["Coordination protocol", "Communication channels", "Test procedures"]
            }
        ]


def main():
    """Generate Node-RED Agent specification"""
    print("🔴 Node-RED Agent Specification Generator")
    print("=" * 50)
    
    spec = NodeRedAgentSpec()
    
    print(f"Agent ID: {spec.agent_id}")
    print(f"TMUX Session: {spec.tmux_session}")
    print(f"Specialization: {spec.specialization}")
    
    print(f"\n📋 Core Capabilities: {len(spec.core_capabilities)}")
    for capability, details in spec.core_capabilities.items():
        print(f"   • {capability}: {len(details['skills'])} skills")
    
    print(f"\n🧠 Knowledge Domains: {len(spec.knowledge_domains)}")
    for domain in spec.knowledge_domains.keys():
        print(f"   • {domain}")
    
    print(f"\n🏭 Brewery Equipment Types: {len(spec.brewery_expertise['equipment_types'])}")
    print(f"🔄 Process Flows: {len(spec.brewery_expertise['process_flows'])}")
    print(f"🛡️ Safety Patterns: {len(spec.brewery_expertise['safety_patterns'])}")
    
    curriculum = spec.get_training_curriculum()
    print(f"\n📚 Training Curriculum: {len(curriculum)} phases")
    
    tasks = spec.get_initial_tasks()
    print(f"📋 Initial Tasks: {len(tasks)} tasks defined")
    
    print("\n✅ Node-RED Agent specification complete!")
    print("🚀 Ready for specialized agent implementation!")


if __name__ == "__main__":
    main()