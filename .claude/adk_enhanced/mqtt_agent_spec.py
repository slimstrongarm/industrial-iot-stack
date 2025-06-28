#!/usr/bin/env python3
"""
MQTT Agent Specification
Specialized agent for MQTT topics, payloads, and brewery data architecture
"""

from datetime import datetime
from typing import Dict, List, Any
import json

class MqttAgentSpec:
    """
    Specification for the MQTT specialized agent.
    This agent becomes the definitive expert in MQTT topics, payloads, and brewery data architecture.
    """
    
    def __init__(self):
        self.agent_id = "mqtt_agent"
        self.tmux_session = "TMUX_F"
        self.specialization = "MQTT Topics & Payload Expert"
        
        # Core capabilities
        self.core_capabilities = {
            "topic_architecture": {
                "description": "Complete MQTT topic structure design and optimization",
                "skills": [
                    "UNS (Unified Namespace) compliance",
                    "Topic hierarchy design and optimization",
                    "Wildcard pattern optimization",
                    "Topic naming convention enforcement",
                    "Namespace collision prevention",
                    "Topic lifecycle management"
                ]
            },
            "payload_management": {
                "description": "MQTT payload structure and validation",
                "skills": [
                    "JSON payload schema design",
                    "Payload compression and optimization",
                    "Data type validation and conversion",
                    "Payload versioning and compatibility",
                    "Schema evolution management",
                    "Binary payload handling"
                ]
            },
            "broker_optimization": {
                "description": "MQTT broker configuration and performance",
                "skills": [
                    "QoS level optimization",
                    "Retention policy management",
                    "Connection management and pooling",
                    "Security and authentication setup",
                    "Performance monitoring and tuning",
                    "Broker clustering and failover"
                ]
            },
            "brewery_data_architecture": {
                "description": "Steel Bonnet brewery-specific MQTT design",
                "skills": [
                    "Equipment data modeling",
                    "Process state representation",
                    "Alarm and event structure",
                    "Recipe and batch tracking",
                    "Real-time vs historical data routing",
                    "Safety system integration"
                ]
            }
        }
        
        # MQTT Topic Architecture (UNS Compliant)
        self.uns_architecture = {
            "enterprise": "steelbonnet",
            "site": "brewery",
            "areas": {
                "cellar": {
                    "description": "Cellar operations and fermentation",
                    "lines": ["fermentation", "conditioning", "packaging"],
                    "equipment": ["vessels", "pumps", "sensors"]
                },
                "brewhouse": {
                    "description": "Brewing operations",
                    "lines": ["mash", "lauter", "boil", "whirlpool"],
                    "equipment": ["hlt", "mash_tun", "kettle", "pumps"]
                },
                "utilities": {
                    "description": "Utility systems",
                    "lines": ["glycol", "steam", "compressed_air", "water"],
                    "equipment": ["chillers", "compressors", "boilers", "tanks"]
                }
            }
        }
        
        # Payload Schemas
        self.payload_schemas = {
            "sensor_reading": {
                "schema": {
                    "timestamp": "ISO8601",
                    "value": "float",
                    "unit": "string",
                    "quality": "good|bad|uncertain",
                    "source": "string"
                },
                "example": {
                    "timestamp": "2025-06-08T12:00:00Z",
                    "value": 65.5,
                    "unit": "°C",
                    "quality": "good",
                    "source": "temp_sensor_001"
                }
            },
            "equipment_status": {
                "schema": {
                    "timestamp": "ISO8601",
                    "status": "running|stopped|fault|maintenance",
                    "runtime_hours": "float",
                    "fault_codes": "array",
                    "maintenance_due": "boolean"
                },
                "example": {
                    "timestamp": "2025-06-08T12:00:00Z",
                    "status": "running",
                    "runtime_hours": 1250.5,
                    "fault_codes": [],
                    "maintenance_due": False
                }
            },
            "process_state": {
                "schema": {
                    "timestamp": "ISO8601",
                    "recipe_id": "string",
                    "batch_id": "string",
                    "step": "string",
                    "progress_percent": "float",
                    "parameters": "object"
                },
                "example": {
                    "timestamp": "2025-06-08T12:00:00Z",
                    "recipe_id": "IPA_001",
                    "batch_id": "B2025060801",
                    "step": "mash",
                    "progress_percent": 65.0,
                    "parameters": {"target_temp": 65, "current_temp": 64.8}
                }
            },
            "alarm_event": {
                "schema": {
                    "timestamp": "ISO8601",
                    "severity": "low|medium|high|critical",
                    "message": "string",
                    "equipment_id": "string",
                    "acknowledged": "boolean",
                    "auto_reset": "boolean"
                },
                "example": {
                    "timestamp": "2025-06-08T12:00:00Z",
                    "severity": "high",
                    "message": "HLT temperature exceeding safety limit",
                    "equipment_id": "hlt_001",
                    "acknowledged": False,
                    "auto_reset": False
                }
            }
        }
        
        # Broker configurations
        self.broker_configs = {
            "steel_bonnet_main": {
                "host": "localhost",
                "port": 1883,
                "purpose": "Primary brewery operations",
                "topics": ["steelbonnet/brewery/+/+/+"],
                "qos_strategy": "equipment_critical"
            },
            "ignition_gateway": {
                "host": "localhost", 
                "port": 1883,
                "purpose": "Ignition HMI integration",
                "topics": ["ignition/+/+", "steelbonnet/brewery/+/+/data"],
                "qos_strategy": "realtime_display"
            },
            "n8n_automation": {
                "host": "localhost",
                "port": 1883,
                "purpose": "Workflow automation triggers",
                "topics": ["steelbonnet/brewery/+/+/alarms", "steelbonnet/brewery/+/+/events"],
                "qos_strategy": "guaranteed_delivery"
            }
        }
        
        # Topic validation rules
        self.topic_validation_rules = {
            "max_levels": 7,  # enterprise/site/area/line/equipment/data_type/attribute
            "naming_convention": "lowercase_underscore",
            "reserved_words": ["system", "admin", "config", "debug"],
            "wildcard_restrictions": ["no_wildcards_in_publish", "single_level_only_for_subscriptions"],
            "retention_policies": {
                "sensor_data": "retain_latest",
                "alarms": "retain_all",
                "status": "retain_latest",
                "commands": "no_retention"
            }
        }
        
    def get_specialized_prompt(self) -> str:
        """Generate the specialized prompt for MQTT Agent"""
        return f"""
# 📡 MQTT Agent - Topics & Payload Expert

## Identity & Specialization
You are the **MQTT Agent** - the definitive expert in MQTT topics, payloads, and brewery data architecture. You operate in TMUX Terminal F with complete specialization in MQTT technologies and brewery data flows.

## Core Mission
- **PRIMARY**: Master all aspects of MQTT topic architecture, payload design, and brewery data flows
- **SECONDARY**: Coordinate with Node-RED Agent for optimal data routing and Ignition Agent for HMI integration
- **TERTIARY**: Maintain the definitive UNS-compliant topic structure and payload schemas

## Specialized Knowledge Areas

### Topic Architecture Expertise
- UNS (Unified Namespace) compliance and implementation
- Topic hierarchy design: enterprise/site/area/line/equipment/data_type/attribute
- Wildcard optimization for efficient subscriptions
- Topic naming conventions and collision prevention
- Namespace lifecycle management and evolution

### Payload Management Mastery
- JSON schema design and validation
- Payload optimization for brewery data types
- Data type conversion and validation
- Schema versioning and backward compatibility
- Binary payload handling for high-frequency data

### Broker Optimization
- QoS level strategy for different data types
- Retention policies for sensor data, alarms, status, commands
- Connection pooling and performance tuning
- Security configuration and authentication
- Multi-broker coordination and failover

### Brewery Data Architecture
- Equipment data modeling (HLT, fermentation, glycol, etc.)
- Process state representation (recipes, batches, steps)
- Alarm and event structure design
- Real-time vs historical data routing strategies
- Safety system integration patterns

## Steel Bonnet UNS Structure
```
steelbonnet/brewery/
├── cellar/
│   ├── fermentation/vessel_01/temperature/value
│   ├── fermentation/vessel_01/pressure/value
│   └── conditioning/tank_01/status/running
├── brewhouse/
│   ├── hlt/temperature/value
│   ├── mash_tun/temperature/setpoint
│   └── kettle/level/value
└── utilities/
    ├── glycol/chiller_01/temperature/value
    ├── glycol/chiller_01/flow/value
    └── compressed_air/compressor/status/running
```

## Payload Schemas
- **sensor_reading**: timestamp, value, unit, quality, source
- **equipment_status**: timestamp, status, runtime_hours, fault_codes, maintenance_due
- **process_state**: timestamp, recipe_id, batch_id, step, progress_percent, parameters
- **alarm_event**: timestamp, severity, message, equipment_id, acknowledged, auto_reset

## Coordination Protocol
- **Report to**: Mac Claude (Coordinator) via ADK coordination engine
- **Coordinate with**: Node-RED Agent (flow optimization), Ignition Agent (tag mapping)
- **Validate**: All topic proposals and payload changes across the system
- **Document**: Complete topic registry and payload documentation

## Success Metrics
- Topic compliance: 100% UNS-compliant topic structure
- Payload efficiency: <1KB average payload size
- Broker performance: <10ms message routing latency
- Integration: Seamless MQTT ↔ Node-RED ↔ Ignition data flow

Remember: You are THE MQTT expert. Every topic decision, payload design, and broker configuration should reflect deep MQTT expertise and brewery data architecture knowledge.
"""

    def get_initial_tasks(self) -> List[Dict]:
        """Define initial tasks for MQTT Agent"""
        return [
            {
                "task_id": "MQ-001",
                "title": "Audit Steel Bonnet MQTT Topic Structure",
                "description": "Complete audit of existing MQTT topics for UNS compliance and optimization",
                "priority": "High",
                "estimated_time": "45 minutes",
                "deliverables": ["Topic inventory", "UNS compliance analysis", "Optimization recommendations"]
            },
            {
                "task_id": "MQ-002",
                "title": "Design UNS-Compliant Topic Architecture",
                "description": "Create comprehensive UNS-compliant topic structure for Steel Bonnet brewery",
                "priority": "High", 
                "estimated_time": "60 minutes",
                "deliverables": ["UNS topic hierarchy", "Naming conventions", "Migration plan"]
            },
            {
                "task_id": "MQ-003",
                "title": "Create Brewery Payload Schemas",
                "description": "Design and validate JSON schemas for all brewery data types",
                "priority": "High",
                "estimated_time": "45 minutes", 
                "deliverables": ["JSON schemas", "Validation rules", "Example payloads"]
            },
            {
                "task_id": "MQ-004",
                "title": "Coordinate with Node-RED Agent",
                "description": "Establish topic/payload coordination protocol with Node-RED Agent",
                "priority": "Medium",
                "estimated_time": "30 minutes",
                "deliverables": ["Coordination protocol", "Topic validation API", "Integration tests"]
            }
        ]

    def get_training_curriculum(self) -> Dict:
        """Define the training curriculum for MQTT Agent"""
        return {
            "phase_1_foundations": {
                "duration": "Session 1",
                "topics": [
                    "MQTT protocol fundamentals and QoS strategies",
                    "UNS (Unified Namespace) principles and implementation",
                    "Steel Bonnet current topic structure analysis",
                    "Payload optimization for brewery data",
                    "Broker configuration and security"
                ],
                "hands_on": [
                    "Audit existing Steel Bonnet MQTT topics",
                    "Design UNS-compliant topic hierarchy",
                    "Create brewery equipment payload schemas",
                    "Test broker connectivity and performance"
                ]
            },
            "phase_2_integration": {
                "duration": "Session 2",
                "topics": [
                    "Node-RED MQTT integration patterns",
                    "Ignition MQTT tag mapping strategies", 
                    "Multi-broker coordination and failover",
                    "Real-time vs historical data routing",
                    "Alarm and event handling patterns"
                ],
                "hands_on": [
                    "Coordinate topic structure with Node-RED Agent",
                    "Design Ignition tag mapping strategy",
                    "Implement alarm and event routing",
                    "Test cross-platform data flow"
                ]
            },
            "phase_3_optimization": {
                "duration": "Session 3",
                "topics": [
                    "Advanced payload compression and optimization",
                    "Performance monitoring and alerting",
                    "Schema evolution and versioning",
                    "Security hardening and authentication",
                    "Scalability planning and load testing"
                ],
                "hands_on": [
                    "Implement payload compression strategies",
                    "Deploy MQTT performance monitoring",
                    "Create schema migration procedures",
                    "Load test brewery data flows"
                ]
            }
        }


def main():
    """Generate MQTT Agent specification"""
    print("📡 MQTT Agent Specification Generator")
    print("=" * 50)
    
    spec = MqttAgentSpec()
    
    print(f"Agent ID: {spec.agent_id}")
    print(f"TMUX Session: {spec.tmux_session}")
    print(f"Specialization: {spec.specialization}")
    
    print(f"\n📋 Core Capabilities: {len(spec.core_capabilities)}")
    for capability, details in spec.core_capabilities.items():
        print(f"   • {capability}: {len(details['skills'])} skills")
    
    print(f"\n🏗️ UNS Architecture Areas: {len(spec.uns_architecture['areas'])}")
    for area, details in spec.uns_architecture['areas'].items():
        print(f"   • {area}: {len(details['lines'])} lines, {len(details['equipment'])} equipment types")
    
    print(f"\n📦 Payload Schemas: {len(spec.payload_schemas)}")
    for schema in spec.payload_schemas.keys():
        print(f"   • {schema}")
    
    print(f"\n🔗 Broker Configurations: {len(spec.broker_configs)}")
    for broker in spec.broker_configs.keys():
        print(f"   • {broker}")
    
    curriculum = spec.get_training_curriculum()
    print(f"\n📚 Training Curriculum: {len(curriculum)} phases")
    
    tasks = spec.get_initial_tasks()
    print(f"📋 Initial Tasks: {len(tasks)} tasks defined")
    
    print("\n✅ MQTT Agent specification complete!")
    print("🚀 Ready for specialized MQTT agent implementation!")


if __name__ == "__main__":
    main()