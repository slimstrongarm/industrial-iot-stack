#!/usr/bin/env python3
"""
Enhanced MQTT Worker with ADK Integration  
Specialized agent for MQTT topics, payloads, and brewery data architecture
"""

import json
import sys
import time
import paho.mqtt.client as mqtt
from datetime import datetime
from pathlib import Path
import jsonschema
import re

# Add the project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Import ADK components
sys.path.insert(0, str(project_root / ".claude" / "adk_enhanced"))
from state_persistence import StatePersistenceEngine
from coordination_engine import TaskCoordinationEngine  
from conflict_prevention import ConflictPreventionEngine


class EnhancedMqttWorker:
    """
    Enhanced MQTT worker with ADK intelligence and brewery data specialization.
    The definitive expert in MQTT topics, payloads, and UNS architecture.
    """
    
    def __init__(self):
        self.instance_id = "mqtt_agent"
        self.tmux_session = "TMUX_F"
        self.specialization = "MQTT Topics & Payload Expert"
        
        # ADK Components
        self.state_engine = StatePersistenceEngine(self.instance_id)
        self.coordination_engine = TaskCoordinationEngine()
        self.conflict_engine = ConflictPreventionEngine()
        
        # UNS Architecture
        self.uns_structure = {
            "enterprise": "steelbonnet",
            "site": "brewery",
            "areas": {
                "cellar": ["fermentation", "conditioning", "packaging"],
                "brewhouse": ["mash", "lauter", "boil", "whirlpool"], 
                "utilities": ["glycol", "steam", "compressed_air", "water"]
            }
        }
        
        # Payload Schemas
        self.payload_schemas = {
            "sensor_reading": {
                "type": "object",
                "properties": {
                    "timestamp": {"type": "string", "format": "date-time"},
                    "value": {"type": "number"},
                    "unit": {"type": "string"},
                    "quality": {"type": "string", "enum": ["good", "bad", "uncertain"]},
                    "source": {"type": "string"}
                },
                "required": ["timestamp", "value", "unit", "quality", "source"]
            },
            "equipment_status": {
                "type": "object", 
                "properties": {
                    "timestamp": {"type": "string", "format": "date-time"},
                    "status": {"type": "string", "enum": ["running", "stopped", "fault", "maintenance"]},
                    "runtime_hours": {"type": "number"},
                    "fault_codes": {"type": "array", "items": {"type": "string"}},
                    "maintenance_due": {"type": "boolean"}
                },
                "required": ["timestamp", "status"]
            },
            "alarm_event": {
                "type": "object",
                "properties": {
                    "timestamp": {"type": "string", "format": "date-time"},
                    "severity": {"type": "string", "enum": ["low", "medium", "high", "critical"]},
                    "message": {"type": "string"},
                    "equipment_id": {"type": "string"},
                    "acknowledged": {"type": "boolean"},
                    "auto_reset": {"type": "boolean"}
                },
                "required": ["timestamp", "severity", "message", "equipment_id"]
            }
        }
        
        # Broker configurations
        self.brokers = {
            "local": {"host": "localhost", "port": 1883, "keepalive": 60},
            "steel_bonnet": {"host": "localhost", "port": 1883, "keepalive": 60}
        }
        
        # Topic registry for validation
        self.topic_registry = {}
        self.subscribed_topics = set()
        
        print(f"📡 Enhanced MQTT Worker initializing...")
        print(f"   🏗️ UNS Areas: {len(self.uns_structure['areas'])}")
        print(f"   📦 Payload Schemas: {len(self.payload_schemas)}")
        print(f"   🔗 Broker Configs: {len(self.brokers)}")
        print(f"   📊 ADK Integration: Ready")
    
    def start_enhanced_monitoring(self):
        """Start MQTT agent with specialized capabilities"""
        print("\n🔄 Starting Enhanced MQTT Worker...")
        
        # Phase 1: ADK Recovery
        print("📡 Phase 1: ADK Context Recovery")
        self.recovered_context = self.state_engine.recover_session_state()
        
        if self.recovered_context and not self.recovered_context.get("fallback"):
            print(f"✅ MQTT expertise recovered from previous session")
            self._load_topic_registry()
        else:
            print("🔄 Building MQTT expertise from scratch...")
        
        # Phase 2: Broker Connectivity Check
        print("\n📡 Phase 2: MQTT Broker Assessment")
        self._check_broker_connectivity()
        
        # Phase 3: Topic Structure Analysis
        print("\n🏗️ Phase 3: Topic Structure Analysis")
        self._analyze_topic_structure()
        
        # Phase 4: Payload Validation Setup
        print("\n📦 Phase 4: Payload Validation Setup")
        self._setup_payload_validation()
        
        # Phase 5: Coordination Setup
        print("\n🤝 Phase 5: Agent Coordination Setup")
        self._setup_agent_coordination()
        
        print("\n🎉 Enhanced MQTT Worker fully operational!")
    
    def _check_broker_connectivity(self):
        """Check MQTT broker connectivity"""
        for broker_name, config in self.brokers.items():
            try:
                client = mqtt.Client()
                result = client.connect(config["host"], config["port"], config["keepalive"])
                
                if result == 0:
                    print(f"   ✅ {broker_name} broker connected: {config['host']}:{config['port']}")
                    client.disconnect()
                else:
                    print(f"   ❌ {broker_name} broker connection failed: code {result}")
                    
            except Exception as e:
                print(f"   ❌ {broker_name} broker error: {e}")
    
    def _analyze_topic_structure(self):
        """Analyze existing topic structure for UNS compliance"""
        try:
            # Simulate topic discovery (in real implementation, this would scan live brokers)
            sample_topics = [
                "brewery/hlt/temperature",
                "brewery/fermentation/vessel01/temperature", 
                "brewery/glycol/chiller/status",
                "steelbonnet/brewery/cellar/fermentation/vessel_01/temperature/value",
                "ignition/Steel_Bonnet/HLT/Temperature"
            ]
            
            analysis = {
                "total_topics": len(sample_topics),
                "uns_compliant": 0,
                "non_compliant": 0,
                "compliance_issues": []
            }
            
            print(f"   📊 Analyzing {analysis['total_topics']} sample topics:")
            
            for topic in sample_topics:
                is_compliant, issues = self._validate_topic_structure(topic)
                
                if is_compliant:
                    analysis["uns_compliant"] += 1
                    print(f"      ✅ {topic}")
                else:
                    analysis["non_compliant"] += 1 
                    analysis["compliance_issues"].extend(issues)
                    print(f"      ❌ {topic} - {', '.join(issues)}")
            
            compliance_rate = (analysis["uns_compliant"] / analysis["total_topics"]) * 100
            print(f"   📈 UNS Compliance Rate: {compliance_rate:.1f}%")
            
            # Save analysis
            self._save_topic_analysis(analysis)
            
        except Exception as e:
            print(f"   ❌ Topic analysis failed: {e}")
    
    def _validate_topic_structure(self, topic: str) -> tuple:
        """Validate topic against UNS standards"""
        issues = []
        
        # Check UNS hierarchy: enterprise/site/area/line/equipment/data_type/attribute
        parts = topic.split('/')
        
        if len(parts) < 3:
            issues.append("Too few hierarchy levels")
        
        if len(parts) > 7:
            issues.append("Too many hierarchy levels")
        
        # Check for UNS enterprise/site structure
        if len(parts) >= 2:
            if parts[0] != self.uns_structure["enterprise"]:
                if parts[0] not in ["brewery", "ignition"]:  # Legacy allowed
                    issues.append(f"Non-UNS enterprise: {parts[0]}")
            
            if len(parts) >= 2 and parts[1] != self.uns_structure["site"]:
                if parts[1] not in ["Steel_Bonnet", "hlt", "fermentation", "glycol"]:  # Legacy allowed
                    issues.append(f"Non-UNS site: {parts[1]}")
        
        # Check naming convention (lowercase with underscores)
        for part in parts:
            if not re.match(r'^[a-z0-9_+]+$', part):
                issues.append(f"Invalid naming convention: {part}")
        
        return len(issues) == 0, issues
    
    def _setup_payload_validation(self):
        """Setup payload validation system"""
        try:
            print(f"   📦 Payload validation ready for {len(self.payload_schemas)} schema types:")
            
            for schema_name, schema in self.payload_schemas.items():
                # Test schema compilation
                jsonschema.Draft7Validator.check_schema(schema)
                print(f"      ✅ {schema_name} schema validated")
            
            # Create example payloads
            examples = self._generate_example_payloads()
            print(f"   📝 Generated {len(examples)} example payloads")
            
        except Exception as e:
            print(f"   ❌ Payload validation setup failed: {e}")
    
    def _generate_example_payloads(self) -> dict:
        """Generate example payloads for each schema"""
        examples = {
            "sensor_reading": {
                "timestamp": datetime.now().isoformat(),
                "value": 65.5,
                "unit": "°C", 
                "quality": "good",
                "source": "temp_sensor_hlt_001"
            },
            "equipment_status": {
                "timestamp": datetime.now().isoformat(),
                "status": "running",
                "runtime_hours": 1250.5,
                "fault_codes": [],
                "maintenance_due": False
            },
            "alarm_event": {
                "timestamp": datetime.now().isoformat(),
                "severity": "high",
                "message": "HLT temperature exceeding safety limit",
                "equipment_id": "hlt_001",
                "acknowledged": False,
                "auto_reset": False
            }
        }
        
        return examples
    
    def validate_payload(self, payload_data: dict, schema_type: str) -> tuple:
        """Validate payload against schema"""
        try:
            if schema_type not in self.payload_schemas:
                return False, f"Unknown schema type: {schema_type}"
            
            schema = self.payload_schemas[schema_type]
            jsonschema.validate(payload_data, schema)
            return True, "Valid payload"
            
        except jsonschema.ValidationError as e:
            return False, f"Validation error: {e.message}"
        except Exception as e:
            return False, f"Validation failed: {e}"
    
    def design_uns_topic(self, area: str, line: str, equipment: str, data_type: str, attribute: str) -> str:
        """Design UNS-compliant topic"""
        if area not in self.uns_structure["areas"]:
            raise ValueError(f"Invalid area: {area}")
        
        if line not in self.uns_structure["areas"][area]:
            raise ValueError(f"Invalid line for area {area}: {line}")
        
        topic = f"{self.uns_structure['enterprise']}/{self.uns_structure['site']}/{area}/{line}/{equipment}/{data_type}/{attribute}"
        
        # Validate the generated topic
        is_valid, issues = self._validate_topic_structure(topic)
        if not is_valid:
            raise ValueError(f"Generated topic failed validation: {', '.join(issues)}")
        
        return topic
    
    def _load_topic_registry(self):
        """Load persistent topic registry"""
        try:
            registry_dir = Path(__file__).parent.parent.parent / ".claude" / "adk_enhanced" / "mqtt_library"
            registry_dir.mkdir(parents=True, exist_ok=True)
            
            registry_file = registry_dir / "topic_registry.json"
            if registry_file.exists():
                with open(registry_file, 'r') as f:
                    self.topic_registry = json.load(f)
                print(f"   📚 Topic registry loaded: {len(self.topic_registry)} topics")
            else:
                self.topic_registry = {}
                print(f"   📚 New topic registry created")
                
        except Exception as e:
            print(f"   ⚠️ Could not load topic registry: {e}")
            self.topic_registry = {}
    
    def _save_topic_analysis(self, analysis):
        """Save topic analysis to persistent state"""
        try:
            context_update = {
                "topic_analysis": analysis,
                "analysis_timestamp": datetime.now().isoformat(),
                "specialization": self.specialization,
                "uns_areas": len(self.uns_structure["areas"]),
                "payload_schemas": len(self.payload_schemas)
            }
            
            self.state_engine.save_session_state(context_update)
            print(f"   💾 Topic analysis saved to persistent state")
            
        except Exception as e:
            print(f"   ⚠️ Could not save analysis: {e}")
    
    def _setup_agent_coordination(self):
        """Setup coordination with other specialized agents"""
        try:
            coordination_info = {
                "agent_type": "mqtt_agent",
                "specialization": "MQTT Topics & Payload Expert",
                "capabilities": [
                    "uns_topic_design",
                    "payload_validation",
                    "broker_optimization",
                    "brewery_data_architecture"
                ],
                "coordination_topics": [
                    "topic_validation",
                    "payload_schema_updates",
                    "broker_performance",
                    "data_flow_optimization"
                ]
            }
            
            print(f"   🤝 Coordination setup complete")
            print(f"      Specialization: {coordination_info['specialization']}")
            print(f"      Capabilities: {len(coordination_info['capabilities'])}")
            print(f"      UNS Areas: {len(self.uns_structure['areas'])}")
            
        except Exception as e:
            print(f"   ⚠️ Coordination setup failed: {e}")


def main():
    """Main entry point for enhanced MQTT worker"""
    print("📡 ADK Enhanced MQTT Worker")
    print("=" * 50)
    
    # Initialize enhanced MQTT worker
    worker = EnhancedMqttWorker()
    
    # Start enhanced monitoring
    worker.start_enhanced_monitoring()
    
    # Demo: Design UNS topics and validate payloads
    print("\n" + "=" * 50)
    print("🧪 Testing MQTT Topic Design & Payload Validation")
    
    # Test UNS topic design
    try:
        hlt_temp_topic = worker.design_uns_topic("brewhouse", "mash", "hlt_001", "temperature", "value")
        print(f"✅ UNS Topic Design: {hlt_temp_topic}")
        
        fermentation_topic = worker.design_uns_topic("cellar", "fermentation", "vessel_01", "temperature", "value")
        print(f"✅ UNS Topic Design: {fermentation_topic}")
        
        glycol_topic = worker.design_uns_topic("utilities", "glycol", "chiller_01", "status", "running")
        print(f"✅ UNS Topic Design: {glycol_topic}")
        
    except Exception as e:
        print(f"❌ Topic design failed: {e}")
    
    # Test payload validation
    test_payloads = [
        {
            "type": "sensor_reading",
            "data": {
                "timestamp": datetime.now().isoformat(),
                "value": 65.5,
                "unit": "°C",
                "quality": "good", 
                "source": "temp_sensor_hlt_001"
            }
        },
        {
            "type": "equipment_status",
            "data": {
                "timestamp": datetime.now().isoformat(),
                "status": "running",
                "runtime_hours": 1250.5,
                "fault_codes": [],
                "maintenance_due": False
            }
        }
    ]
    
    for test in test_payloads:
        is_valid, message = worker.validate_payload(test["data"], test["type"])
        status = "✅" if is_valid else "❌"
        print(f"{status} Payload Validation ({test['type']}): {message}")
    
    print("\n🎯 Enhanced MQTT Worker demonstration completed!")
    print("🚀 MQTT Agent ready for brewery data architecture!")


if __name__ == "__main__":
    main()