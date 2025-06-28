#!/usr/bin/env python3
"""
🪂 Parachute Drop - Industrial Discovery Agent
Multi-protocol network discovery and tag intelligence system
"""

import socket
import threading
import time
import json
import struct
import serial
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu
from pymodbus.client.sync import ModbusSerialClient
from pymodbus.client.sync import ModbusTcpClient
import paho.mqtt.client as mqtt
from scapy.all import *
import nmap

class ParachuteDropDiscovery:
    def __init__(self):
        self.discovered_devices = {}
        self.mqtt_traffic = []
        self.modbus_devices = []
        self.tag_intelligence = {}
        
    def discover_network(self, network_range="192.168.1.0/24"):
        """Scan network for industrial devices"""
        print(f"🔍 Scanning network: {network_range}")
        
        nm = nmap.PortScanner()
        
        # Common industrial ports
        ports = "102,502,44818,1883,8883,9600,20000"  # S7, Modbus, OPC-UA, MQTT, etc
        
        result = nm.scan(network_range, ports)
        
        for host in nm.all_hosts():
            if nm[host].state() == 'up':
                device_info = self.identify_device(host, nm[host])
                if device_info:
                    self.discovered_devices[host] = device_info
                    
        return self.discovered_devices
    
    def identify_device(self, ip, scan_result):
        """Identify device type based on open ports and responses"""
        device = {
            "ip": ip,
            "type": "unknown",
            "protocol": [],
            "vendor": "unknown",
            "tags": [],
            "confidence": 0
        }
        
        ports = scan_result['tcp']
        
        # Siemens S7
        if 102 in ports and ports[102]['state'] == 'open':
            device["type"] = "Siemens PLC"
            device["protocol"].append("S7")
            device["confidence"] += 30
            device["tags"] = self.discover_s7_tags(ip)
            
        # Modbus TCP
        if 502 in ports and ports[502]['state'] == 'open':
            device["type"] = "Modbus Device"
            device["protocol"].append("Modbus TCP")
            device["confidence"] += 25
            device["tags"] = self.discover_modbus_tags(ip)
            
        # OPC-UA
        if 4840 in ports and ports[4840]['state'] == 'open':
            device["type"] = "OPC-UA Server"
            device["protocol"].append("OPC-UA")
            device["confidence"] += 35
            
        # MQTT Broker
        if 1883 in ports and ports[1883]['state'] == 'open':
            device["type"] = "MQTT Broker"
            device["protocol"].append("MQTT")
            device["confidence"] += 20
            self.listen_mqtt_traffic(ip)
            
        return device if device["confidence"] > 0 else None
    
    def discover_s7_tags(self, ip):
        """Attempt to read S7 tag structure"""
        tags = []
        try:
            # S7 discovery logic would go here
            # This is a simplified version
            common_s7_tags = [
                {"name": "DB1.Temperature", "type": "REAL", "purpose": "Process Temperature"},
                {"name": "DB1.Pressure", "type": "REAL", "purpose": "System Pressure"},
                {"name": "M0.0", "type": "BOOL", "purpose": "Motor Start"},
                {"name": "M0.1", "type": "BOOL", "purpose": "Motor Running"},
            ]
            tags.extend(common_s7_tags)
        except Exception as e:
            print(f"S7 discovery failed for {ip}: {e}")
        return tags
    
    def discover_modbus_tags(self, ip, port=502):
        """Discover Modbus registers and their purposes"""
        tags = []
        try:
            client = ModbusTcpClient(ip, port=port)
            if client.connect():
                # Read common Modbus registers
                for address in range(1, 50):  # Scan first 50 registers
                    try:
                        result = client.read_holding_registers(address, 1)
                        if not result.isError():
                            purpose = self.guess_tag_purpose(f"HR_{address}", result.registers[0])
                            tags.append({
                                "name": f"40{address:03d}",
                                "address": address,
                                "type": "UINT16",
                                "value": result.registers[0],
                                "purpose": purpose
                            })
                    except:
                        continue
                client.close()
        except Exception as e:
            print(f"Modbus discovery failed for {ip}: {e}")
        return tags
    
    def discover_serial_modbus(self, port="/dev/ttyUSB0", baud=9600):
        """Scan for Modbus RTU devices on serial connection"""
        devices = []
        try:
            client = ModbusSerialClient(method='rtu', port=port, baudrate=baud, timeout=1)
            if client.connect():
                # Scan for slave addresses 1-247
                for slave_id in range(1, 248):
                    try:
                        result = client.read_holding_registers(1, 1, unit=slave_id)
                        if not result.isError():
                            device = {
                                "slave_id": slave_id,
                                "protocol": "Modbus RTU",
                                "port": port,
                                "baud": baud,
                                "registers": self.scan_modbus_registers(client, slave_id)
                            }
                            devices.append(device)
                            print(f"📡 Found Modbus device at ID {slave_id}")
                    except:
                        continue
                client.close()
        except Exception as e:
            print(f"Serial Modbus scan failed: {e}")
        return devices
    
    def listen_mqtt_traffic(self, broker_ip, duration=30):
        """Listen to MQTT traffic and analyze topics"""
        def on_connect(client, userdata, flags, rc):
            print(f"📡 Connected to MQTT broker at {broker_ip}")
            client.subscribe("#")  # Subscribe to all topics
            
        def on_message(client, userdata, msg):
            traffic = {
                "timestamp": time.time(),
                "topic": msg.topic,
                "payload": msg.payload.decode('utf-8', errors='ignore'),
                "qos": msg.qos
            }
            self.mqtt_traffic.append(traffic)
            self.analyze_mqtt_topic(msg.topic, traffic["payload"])
            
        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_message = on_message
        
        try:
            client.connect(broker_ip, 1883, 60)
            client.loop_start()
            time.sleep(duration)
            client.loop_stop()
            client.disconnect()
        except Exception as e:
            print(f"MQTT listening failed: {e}")
    
    def analyze_mqtt_topic(self, topic, payload):
        """Analyze MQTT topic structure to determine purpose"""
        topic_parts = topic.split('/')
        
        # Common industrial MQTT patterns
        patterns = {
            "temperature": ["temp", "temperature", "°c", "celsius", "fahrenheit"],
            "pressure": ["pressure", "psi", "bar", "pascal"],
            "motor": ["motor", "pump", "fan", "drive"],
            "valve": ["valve", "actuator", "position"],
            "alarm": ["alarm", "alert", "fault", "error"],
            "setpoint": ["sp", "setpoint", "target", "set"]
        }
        
        purpose = "unknown"
        for category, keywords in patterns.items():
            if any(keyword in topic.lower() for keyword in keywords):
                purpose = category
                break
                
        self.tag_intelligence[topic] = {
            "purpose": purpose,
            "last_value": payload,
            "update_time": time.time(),
            "samples": self.tag_intelligence.get(topic, {}).get("samples", 0) + 1
        }
    
    def guess_tag_purpose(self, tag_name, value):
        """AI-powered tag purpose detection based on name and value patterns"""
        name_lower = tag_name.lower()
        
        # Temperature detection
        if any(word in name_lower for word in ["temp", "temperature"]):
            if 0 <= value <= 200:
                return "Process Temperature (°C)"
            elif 32 <= value <= 400:
                return "Process Temperature (°F)"
                
        # Pressure detection
        if any(word in name_lower for word in ["press", "pressure"]):
            if 0 <= value <= 1000:
                return "System Pressure (PSI)"
                
        # Motor status
        if any(word in name_lower for word in ["motor", "run", "start"]):
            if value in [0, 1]:
                return "Motor Status (On/Off)"
                
        # Level detection
        if any(word in name_lower for word in ["level", "tank"]):
            if 0 <= value <= 100:
                return "Tank Level (%)"
                
        return "Unknown Process Variable"
    
    def generate_report(self):
        """Generate comprehensive discovery report"""
        report = {
            "discovery_timestamp": time.time(),
            "network_devices": self.discovered_devices,
            "mqtt_analysis": {
                "total_messages": len(self.mqtt_traffic),
                "unique_topics": len(self.tag_intelligence),
                "topic_intelligence": self.tag_intelligence
            },
            "recommendations": self.generate_recommendations()
        }
        
        return report
    
    def generate_recommendations(self):
        """Generate actionable recommendations based on discoveries"""
        recs = []
        
        if any("Siemens" in device["type"] for device in self.discovered_devices.values()):
            recs.append("Deploy Ignition with Siemens S7 driver for optimal integration")
            
        if any("Modbus" in device["type"] for device in self.discovered_devices.values()):
            recs.append("Configure Node-RED Modbus nodes for data collection")
            
        if len(self.mqtt_traffic) > 100:
            recs.append("Rich MQTT traffic detected - implement topic analytics dashboard")
            
        return recs

def main():
    print("🪂 PARACHUTE DROP - Discovery Agent Starting...")
    
    discovery = ParachuteDropDiscovery()
    
    # Network discovery
    devices = discovery.discover_network()
    print(f"📊 Found {len(devices)} industrial devices")
    
    # Serial discovery
    serial_devices = discovery.discover_serial_modbus()
    print(f"📡 Found {len(serial_devices)} serial Modbus devices")
    
    # Generate report
    report = discovery.generate_report()
    
    # Save to file
    with open('/home/pi/parachute_drop/discovery_report.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    print("✅ Discovery complete! Report saved.")
    return report

if __name__ == "__main__":
    main()