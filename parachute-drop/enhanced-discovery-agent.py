#!/usr/bin/env python3
"""
🪂 PARACHUTE DROP - Enhanced Industrial Discovery Agent
CT-084 Implementation: Advanced network discovery with AI-powered tag intelligence
"""

import socket
import threading
import time
import json
import struct
import serial
import subprocess
import re
import asyncio
from datetime import datetime
from pathlib import Path

# Industrial protocol libraries
try:
    import modbus_tk.defines as cst
    from modbus_tk import modbus_rtu
    from pymodbus.client.sync import ModbusSerialClient, ModbusTcpClient
    import paho.mqtt.client as mqtt
    from scapy.all import *
    import nmap
except ImportError as e:
    print(f"Installing required package: {e}")
    subprocess.check_call([sys.executable, "-m", "pip", "install", str(e).split("'")[1]])

class EnhancedDiscoveryAgent:
    def __init__(self):
        self.discovered_devices = {}
        self.mqtt_traffic = []
        self.tag_intelligence = {}
        self.network_topology = {}
        self.device_signatures = {}
        self.running = True
        
        # AI-powered tag classification patterns
        self.tag_patterns = {
            'temperature': {
                'keywords': ['temp', 'temperature', 'deg', 'celsius', 'fahrenheit', 'thermal'],
                'value_ranges': [(0, 200), (32, 400), (-50, 150)],
                'units': ['°C', '°F', 'C', 'F'],
                'confidence': 0.9
            },
            'pressure': {
                'keywords': ['press', 'pressure', 'psi', 'bar', 'pascal', 'kpa'],
                'value_ranges': [(0, 1000), (0, 100), (0, 10)],
                'units': ['PSI', 'Bar', 'kPa', 'Pa'],
                'confidence': 0.85
            },
            'level': {
                'keywords': ['level', 'tank', 'height', 'depth', 'volume'],
                'value_ranges': [(0, 100), (0, 1000)],
                'units': ['%', 'ft', 'm', 'gal', 'L'],
                'confidence': 0.8
            },
            'motor': {
                'keywords': ['motor', 'pump', 'fan', 'drive', 'run', 'start', 'stop'],
                'value_ranges': [(0, 1), (0, 100)],
                'units': ['', '%', 'RPM'],
                'confidence': 0.75
            },
            'valve': {
                'keywords': ['valve', 'actuator', 'position', 'open', 'close'],
                'value_ranges': [(0, 1), (0, 100)],
                'units': ['', '%'],
                'confidence': 0.75
            },
            'flow': {
                'keywords': ['flow', 'rate', 'gpm', 'lpm', 'velocity'],
                'value_ranges': [(0, 1000), (0, 100)],
                'units': ['GPM', 'LPM', 'm/s', 'ft/s'],
                'confidence': 0.8
            }
        }
        
    def enhanced_network_scan(self, network_range="192.168.1.0/24"):
        """Enhanced network discovery with protocol fingerprinting"""
        print(f"🔍 Enhanced Network Scan: {network_range}")
        
        nm = nmap.PortScanner()
        
        # Comprehensive industrial port scan
        industrial_ports = "102,502,4840,1883,8883,44818,2222,9600,20000,21,22,23,80,443,161,502,5094"
        
        try:
            result = nm.scan(network_range, industrial_ports, arguments='-sS -O --version-all')
            
            for host in nm.all_hosts():
                if nm[host].state() == 'up':
                    device_info = self.enhanced_device_identification(host, nm[host])
                    if device_info:
                        self.discovered_devices[host] = device_info
                        print(f"✅ Discovered: {host} - {device_info['type']} ({device_info['confidence']}% confidence)")
                        
        except Exception as e:
            print(f"❌ Network scan error: {e}")
            
        return self.discovered_devices
    
    def enhanced_device_identification(self, ip, scan_result):
        """Advanced device identification with confidence scoring"""
        device = {
            "ip": ip,
            "type": "Unknown Device",
            "vendor": "Unknown",
            "protocols": [],
            "services": {},
            "tags": [],
            "confidence": 0,
            "signature": "",
            "capabilities": []
        }
        
        ports = scan_result.get('tcp', {})
        
        # Protocol detection with confidence scoring
        confidence_score = 0
        
        # Siemens S7 Detection
        if 102 in ports and ports[102]['state'] == 'open':
            device["type"] = "Siemens S7 PLC"
            device["vendor"] = "Siemens"
            device["protocols"].append("S7")
            device["capabilities"].extend(["Process Control", "HMI Communication", "Data Blocks"])
            confidence_score += 40
            device["tags"] = self.discover_s7_tags_enhanced(ip)
            
        # Modbus TCP Detection
        if 502 in ports and ports[502]['state'] == 'open':
            device_type = "Modbus TCP Device"
            if device["type"] == "Unknown Device":
                device["type"] = device_type
            device["protocols"].append("Modbus TCP")
            device["capabilities"].extend(["Industrial I/O", "Register Access"])
            confidence_score += 30
            device["tags"].extend(self.discover_modbus_tags_enhanced(ip))
            
        # OPC-UA Detection
        if 4840 in ports and ports[4840]['state'] == 'open':
            device["type"] = "OPC-UA Server"
            device["protocols"].append("OPC-UA")
            device["capabilities"].extend(["Secure Communication", "Information Modeling"])
            confidence_score += 35
            
        # EtherNet/IP Detection
        if 44818 in ports and ports[44818]['state'] == 'open':
            device["type"] = "Allen-Bradley PLC"
            device["vendor"] = "Rockwell Automation"
            device["protocols"].append("EtherNet/IP")
            device["capabilities"].extend(["CIP Messaging", "Real-time I/O"])
            confidence_score += 40
            
        # MQTT Broker Detection
        if 1883 in ports and ports[1883]['state'] == 'open':
            device["type"] = "MQTT Broker"
            device["protocols"].append("MQTT")
            device["capabilities"].extend(["Message Brokering", "Topic Management"])
            confidence_score += 20
            self.discover_mqtt_topics(ip)
            
        # Web Interface Detection
        if 80 in ports and ports[80]['state'] == 'open':
            device["capabilities"].append("Web Interface")
            confidence_score += 10
            web_info = self.probe_web_interface(ip)
            device["services"]["http"] = web_info
            
        # Additional fingerprinting
        device["signature"] = self.generate_device_signature(ports)
        device["confidence"] = min(confidence_score, 95)  # Cap at 95%
        
        return device if confidence_score > 15 else None
    
    def discover_s7_tags_enhanced(self, ip):
        """Enhanced S7 tag discovery with pattern recognition"""
        tags = []
        
        try:
            # Simulate S7 connection (would use snap7 in production)
            common_s7_patterns = [
                {"db": 1, "offset": 0, "name": "HLT_Temperature", "type": "REAL", "purpose": "Hot Liquor Tank Temperature"},
                {"db": 1, "offset": 4, "name": "MLT_Temperature", "type": "REAL", "purpose": "Mash Lauter Tun Temperature"},
                {"db": 1, "offset": 8, "name": "Kettle_Temperature", "type": "REAL", "purpose": "Boil Kettle Temperature"},
                {"db": 2, "offset": 0, "name": "Pump_1_Run", "type": "BOOL", "purpose": "Pump 1 Running Status"},
                {"db": 2, "offset": 1, "name": "Pump_2_Run", "type": "BOOL", "purpose": "Pump 2 Running Status"},
                {"db": 3, "offset": 0, "name": "Flow_Rate_GPM", "type": "REAL", "purpose": "Flow Rate in GPM"},
            ]
            
            for pattern in common_s7_patterns:
                tag = {
                    "name": pattern["name"],
                    "address": f"DB{pattern['db']}.DB{pattern['offset']}",
                    "type": pattern["type"],
                    "purpose": pattern["purpose"],
                    "confidence": self.calculate_tag_confidence(pattern["name"], None)
                }
                tags.append(tag)
                
        except Exception as e:
            print(f"S7 discovery error for {ip}: {e}")
            
        return tags
    
    def discover_modbus_tags_enhanced(self, ip, port=502):
        """Enhanced Modbus tag discovery with intelligent register mapping"""
        tags = []
        
        try:
            client = ModbusTcpClient(ip, port=port, timeout=2)
            if client.connect():
                
                # Intelligent register scanning
                register_ranges = [
                    {"start": 1, "count": 50, "type": "Holding", "purpose": "Process Variables"},
                    {"start": 30001, "count": 20, "type": "Input", "purpose": "Sensor Readings"},
                    {"start": 1, "count": 20, "type": "Coil", "purpose": "Digital Outputs"},
                    {"start": 10001, "count": 20, "type": "Discrete", "purpose": "Digital Inputs"}
                ]
                
                for reg_range in register_ranges:
                    try:
                        if reg_range["type"] == "Holding":
                            result = client.read_holding_registers(reg_range["start"], reg_range["count"])
                        elif reg_range["type"] == "Input":
                            result = client.read_input_registers(reg_range["start"], reg_range["count"])
                        
                        if not result.isError():
                            for i, value in enumerate(result.registers):
                                address = reg_range["start"] + i
                                tag_name = f"HR_{address}" if reg_range["type"] == "Holding" else f"IR_{address}"
                                purpose = self.intelligent_modbus_purpose_detection(address, value, reg_range["type"])
                                
                                tag = {
                                    "name": tag_name,
                                    "address": address,
                                    "type": "UINT16",
                                    "value": value,
                                    "purpose": purpose,
                                    "confidence": self.calculate_tag_confidence(tag_name, value)
                                }
                                tags.append(tag)
                                
                    except Exception:
                        continue
                        
                client.close()
                
        except Exception as e:
            print(f"Modbus discovery error for {ip}: {e}")
            
        return tags[:20]  # Limit to first 20 meaningful tags
    
    def intelligent_modbus_purpose_detection(self, address, value, reg_type):
        """AI-powered Modbus register purpose detection"""
        
        # Address-based pattern recognition
        if 1 <= address <= 100:
            if 0 <= value <= 100:
                return "Process Variable (%)"
            elif 0 <= value <= 1000:
                return "Temperature or Pressure Reading"
            elif value in [0, 1]:
                return "Status Flag"
                
        elif 101 <= address <= 200:
            return "Setpoint or Configuration Parameter"
            
        elif 201 <= address <= 300:
            return "Control Output Signal"
            
        # Value-based pattern recognition
        if 15 <= value <= 85:
            return "Temperature (°C)"
        elif 60 <= value <= 185:
            return "Temperature (°F)" 
        elif 0 <= value <= 300:
            return "Pressure (PSI)"
        elif value in [0, 1]:
            return "Digital Status"
        elif 0 <= value <= 4095:
            return "Analog Input (0-10V scaled)"
            
        return "Unknown Process Variable"
    
    def discover_mqtt_topics(self, broker_ip, duration=30):
        """Discover and analyze MQTT topics with pattern recognition"""
        
        def on_connect(client, userdata, flags, rc):
            print(f"📡 Connected to MQTT broker at {broker_ip}")
            client.subscribe("#")
            
        def on_message(client, userdata, msg):
            try:
                payload_str = msg.payload.decode('utf-8', errors='ignore')
                
                traffic = {
                    "timestamp": time.time(),
                    "topic": msg.topic,
                    "payload": payload_str,
                    "qos": msg.qos,
                    "purpose": self.analyze_mqtt_topic_purpose(msg.topic, payload_str)
                }
                
                self.mqtt_traffic.append(traffic)
                self.update_topic_intelligence(msg.topic, payload_str)
                
            except Exception as e:
                print(f"MQTT message processing error: {e}")
                
        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_message = on_message
        
        try:
            client.connect(broker_ip, 1883, 60)
            client.loop_start()
            time.sleep(duration)
            client.loop_stop()
            client.disconnect()
            
            print(f"📊 Analyzed {len(self.mqtt_traffic)} MQTT messages")
            
        except Exception as e:
            print(f"MQTT discovery error: {e}")
    
    def analyze_mqtt_topic_purpose(self, topic, payload):
        """AI-powered MQTT topic purpose analysis"""
        
        topic_lower = topic.lower()
        
        # Industrial automation patterns
        if any(word in topic_lower for word in ['brewery', 'hlt', 'mlt', 'kettle']):
            if 'temp' in topic_lower:
                return "Brewery Temperature Control"
            elif 'level' in topic_lower:
                return "Brewery Tank Level"
            elif 'pump' in topic_lower:
                return "Brewery Pump Control"
                
        # General industrial patterns
        pattern_map = {
            'temperature': ['temp', 'thermal', 'deg'],
            'pressure': ['pressure', 'psi', 'bar'],
            'flow': ['flow', 'gpm', 'lpm'],
            'level': ['level', 'tank', 'height'],
            'motor': ['motor', 'pump', 'fan', 'drive'],
            'valve': ['valve', 'actuator'],
            'alarm': ['alarm', 'alert', 'fault', 'error']
        }
        
        for purpose, keywords in pattern_map.items():
            if any(keyword in topic_lower for keyword in keywords):
                return f"Industrial {purpose.title()} Monitoring"
                
        # Sparkplug B / UNS pattern detection
        if 'spBv1.0' in topic:
            return "Sparkplug B Industrial Data"
        elif topic.count('/') >= 3:
            return "Hierarchical Process Data"
            
        return "Industrial Telemetry Data"
    
    def calculate_tag_confidence(self, tag_name, value):
        """Calculate confidence score for tag purpose identification"""
        
        if not tag_name:
            return 0
            
        confidence = 20  # Base confidence
        name_lower = tag_name.lower()
        
        # Check against known patterns
        for category, patterns in self.tag_patterns.items():
            keyword_matches = sum(1 for keyword in patterns['keywords'] if keyword in name_lower)
            if keyword_matches > 0:
                confidence += keyword_matches * 20
                
                # Value range validation if value provided
                if value is not None:
                    for min_val, max_val in patterns['value_ranges']:
                        if min_val <= value <= max_val:
                            confidence += 15
                            break
                            
        return min(confidence, 95)
    
    def generate_node_red_flows(self):
        """Generate Node-RED flows based on discovered devices"""
        
        flows = []
        y_position = 100
        
        for ip, device in self.discovered_devices.items():
            if not device['tags']:
                continue
                
            # Create device-specific flows
            if 'Modbus' in device['protocols']:
                modbus_flow = self.create_modbus_flow(ip, device, y_position)
                flows.extend(modbus_flow)
                y_position += 200
                
            elif 'S7' in device['protocols']:
                s7_flow = self.create_s7_flow(ip, device, y_position)
                flows.extend(s7_flow)
                y_position += 200
                
        return flows
    
    def create_modbus_flow(self, ip, device, y_pos):
        """Create Node-RED flow for Modbus device"""
        
        flows = []
        
        # Modbus read node
        modbus_node = {
            "id": f"modbus_{ip.replace('.', '_')}",
            "type": "modbus-read",
            "name": f"{device['type']} - {ip}",
            "topic": "",
            "showStatusActivities": True,
            "unitid": "1",
            "dataType": "HoldingRegister",
            "adr": "1",
            "quantity": str(len(device['tags'])),
            "rate": "5",
            "rateUnit": "s",
            "server": "modbus_server",
            "x": 200,
            "y": y_pos,
            "wires": [[f"process_{ip.replace('.', '_')}"]]
        }
        
        # Processing node
        process_node = {
            "id": f"process_{ip.replace('.', '_')}",
            "type": "function",
            "name": "Process & Scale",
            "func": self.generate_processing_function(device['tags']),
            "outputs": 1,
            "x": 450,
            "y": y_pos,
            "wires": [[f"mqtt_{ip.replace('.', '_')}"]]
        }
        
        # MQTT output node
        mqtt_node = {
            "id": f"mqtt_{ip.replace('.', '_')}",
            "type": "mqtt out",
            "name": f"Publish {device['type']}",
            "topic": f"parachute/devices/{ip.replace('.', '_')}/data",
            "qos": "1",
            "retain": "true",
            "broker": "mqtt_broker",
            "x": 700,
            "y": y_pos,
            "wires": []
        }
        
        flows.extend([modbus_node, process_node, mqtt_node])
        return flows
    
    def generate_processing_function(self, tags):
        """Generate JavaScript function for tag processing"""
        
        func_lines = ["// Auto-generated tag processing", "const processed = {};", ""]
        
        for i, tag in enumerate(tags):
            if 'temperature' in tag['purpose'].lower():
                func_lines.append(f"processed.{tag['name']} = {{")
                func_lines.append(f"    value: msg.payload[{i}],")
                func_lines.append(f"    unit: '°C',")
                func_lines.append(f"    purpose: '{tag['purpose']}',")
                func_lines.append(f"    timestamp: new Date().toISOString()")
                func_lines.append("};")
            else:
                func_lines.append(f"processed.{tag['name']} = msg.payload[{i}];")
        
        func_lines.extend(["", "msg.payload = processed;", "return msg;"])
        
        return "\n".join(func_lines)
    
    def generate_comprehensive_report(self):
        """Generate comprehensive discovery report"""
        
        report = {
            "discovery_metadata": {
                "timestamp": datetime.now().isoformat(),
                "agent_version": "Enhanced Discovery Agent v2.0",
                "scan_duration": "Network scan + 30s MQTT analysis",
                "total_devices": len(self.discovered_devices)
            },
            "network_summary": {
                "devices_by_type": self.categorize_devices(),
                "protocols_detected": self.get_unique_protocols(),
                "confidence_distribution": self.analyze_confidence_levels()
            },
            "detailed_devices": self.discovered_devices,
            "mqtt_analysis": {
                "total_messages": len(self.mqtt_traffic),
                "unique_topics": len(self.tag_intelligence),
                "topic_patterns": self.analyze_topic_patterns(),
                "data_flows": self.mqtt_traffic[-10:]  # Last 10 messages
            },
            "recommendations": self.generate_enhanced_recommendations(),
            "integration_options": self.suggest_integration_approaches(),
            "node_red_flows": self.generate_node_red_flows()
        }
        
        return report
    
    def categorize_devices(self):
        """Categorize discovered devices by type"""
        categories = {}
        for device in self.discovered_devices.values():
            device_type = device['type']
            categories[device_type] = categories.get(device_type, 0) + 1
        return categories
    
    def get_unique_protocols(self):
        """Get list of unique protocols discovered"""
        protocols = set()
        for device in self.discovered_devices.values():
            protocols.update(device['protocols'])
        return list(protocols)
    
    def generate_enhanced_recommendations(self):
        """Generate actionable recommendations based on discoveries"""
        
        recommendations = []
        
        device_types = self.categorize_devices()
        protocols = self.get_unique_protocols()
        
        # Protocol-specific recommendations
        if 'S7' in protocols:
            recommendations.append({
                "priority": "High",
                "category": "Integration",
                "recommendation": "Deploy Ignition with Siemens S7 driver for optimal S7 PLC integration",
                "benefit": "Native protocol support with real-time data exchange"
            })
            
        if 'Modbus TCP' in protocols or 'Modbus RTU' in protocols:
            recommendations.append({
                "priority": "Medium", 
                "category": "Data Collection",
                "recommendation": "Implement Node-RED Modbus flows for flexible data processing",
                "benefit": "Cost-effective data collection with custom processing logic"
            })
            
        if len(self.mqtt_traffic) > 50:
            recommendations.append({
                "priority": "High",
                "category": "Analytics",
                "recommendation": "Deploy MQTT analytics dashboard for topic intelligence",
                "benefit": "Real-time visibility into existing data flows and patterns"
            })
            
        # Device count recommendations
        total_devices = len(self.discovered_devices)
        if total_devices > 5:
            recommendations.append({
                "priority": "High",
                "category": "Architecture",
                "recommendation": "Consider centralized HMI/SCADA system for unified monitoring",
                "benefit": "Consolidated operations with improved efficiency"
            })
            
        return recommendations

async def main():
    """Main execution with async support"""
    print("🪂 PARACHUTE DROP - Enhanced Discovery Agent Starting...")
    print("CT-084: Industrial Discovery Agent Implementation")
    print("==================================================")
    
    agent = EnhancedDiscoveryAgent()
    
    # Phase 1: Network Discovery
    print("\n🔍 Phase 1: Enhanced Network Discovery")
    devices = agent.enhanced_network_scan()
    print(f"📊 Discovered {len(devices)} industrial devices")
    
    # Phase 2: MQTT Analysis (if broker found)
    mqtt_brokers = [ip for ip, device in devices.items() if 'MQTT' in device.get('protocols', [])]
    if mqtt_brokers:
        print(f"\n📡 Phase 2: MQTT Traffic Analysis")
        for broker in mqtt_brokers[:1]:  # Analyze first broker found
            agent.discover_mqtt_topics(broker)
    
    # Phase 3: Generate Comprehensive Report
    print("\n📋 Phase 3: Generating Comprehensive Report")
    report = agent.generate_comprehensive_report()
    
    # Save reports
    output_dir = Path("/home/pi/parachute_drop")
    output_dir.mkdir(exist_ok=True)
    
    # Save JSON report
    with open(output_dir / "discovery_report.json", "w") as f:
        json.dump(report, f, indent=2)
    
    # Save Node-RED flows
    if report['node_red_flows']:
        with open(output_dir / "auto_generated_flows.json", "w") as f:
            json.dump(report['node_red_flows'], f, indent=2)
    
    # Generate summary
    print("\n✅ DISCOVERY COMPLETE!")
    print(f"📊 Summary:")
    print(f"   • {len(devices)} industrial devices discovered")
    print(f"   • {len(agent.get_unique_protocols())} protocols detected")
    print(f"   • {len(agent.mqtt_traffic)} MQTT messages analyzed")
    print(f"   • {len(report['recommendations'])} recommendations generated")
    print(f"   • Reports saved to: {output_dir}")
    
    return report

if __name__ == "__main__":
    asyncio.run(main())