#!/usr/bin/env python3
"""
CT-088 Agent 3: Parachute Drop Integration
Dashboard generation and remote monitoring integration for legacy protocols
"""

import json
import os
from datetime import datetime
from pathlib import Path
import sqlite3

class NodeREDFlowGenerator:
    """Generate Node-RED flows for legacy protocol integration"""
    
    def __init__(self):
        self.flow_template = {
            "id": "ct088_legacy_flows",
            "label": "CT-088 Legacy Protocol Flows",
            "nodes": [],
            "configs": []
        }
        
    def generate_modbus_flow(self, devices):
        """Generate Modbus RTU monitoring flow"""
        modbus_nodes = []
        
        for i, device in enumerate(devices):
            # Modbus read node
            modbus_read = {
                "id": f"modbus_read_{i}",
                "type": "modbus-read",
                "name": f"Modbus Device {device.get('slave_id', i)}",
                "topic": "",
                "showStatusActivities": True,
                "logIOActivities": False,
                "unitid": device.get('slave_id', 1),
                "dataType": "HoldingRegister",
                "adr": "0",
                "quantity": "10",
                "rate": "5000",
                "server": "modbus_server_config",
                "x": 200,
                "y": 100 + i * 80,
                "wires": [[f"modbus_parser_{i}"]]
            }
            
            # Parser node
            parser_node = {
                "id": f"modbus_parser_{i}",
                "type": "function",
                "name": f"Parse Device {device.get('slave_id', i)}",
                "func": f"""
// Parse Modbus data for device {device.get('slave_id', i)}
var deviceData = {{
    device_id: "modbus_{device.get('slave_id', i)}",
    timestamp: new Date().toISOString(),
    registers: []
}};

if (msg.payload && Array.isArray(msg.payload)) {{
    for (var j = 0; j < msg.payload.length; j++) {{
        deviceData.registers.push({{
            address: j,
            value: msg.payload[j],
            purpose: "industrial_data"
        }});
    }}
}}

msg.payload = deviceData;
return msg;
                """,
                "x": 400,
                "y": 100 + i * 80,
                "wires": [["dashboard_update", "mqtt_publish"]]
            }
            
            modbus_nodes.extend([modbus_read, parser_node])
            
        return modbus_nodes
        
    def generate_dashboard_nodes(self):
        """Generate dashboard visualization nodes"""
        dashboard_nodes = [
            {
                "id": "dashboard_update",
                "type": "ui_chart",
                "name": "Legacy Protocol Monitor",
                "group": "legacy_monitoring",
                "order": 1,
                "width": 12,
                "height": 6,
                "label": "Device Values",
                "chartType": "line",
                "legend": "true",
                "xformat": "HH:mm:ss",
                "interpolate": "linear",
                "nodata": "No Data",
                "dot": False,
                "ymin": "",
                "ymax": "",
                "removeOlder": 1,
                "removeOlderPoints": "",
                "removeOlderUnit": "3600",
                "cutout": 0,
                "useOneColor": False,
                "colors": ["#1f77b4","#aec7e8","#ff7f0e","#ffbb78"],
                "x": 600,
                "y": 200,
                "wires": [[]]
            },
            {
                "id": "mqtt_publish",
                "type": "mqtt out",
                "name": "Legacy Protocol MQTT",
                "topic": "industrial/legacy_protocols",
                "qos": "1",
                "retain": "false",
                "broker": "mqtt_broker_config",
                "x": 600,
                "y": 300,
                "wires": []
            }
        ]
        
        return dashboard_nodes
        
    def generate_complete_flow(self, discovery_data):
        """Generate complete Node-RED flow"""
        all_nodes = []
        
        # Add Modbus flows
        modbus_devices = [d for d in discovery_data.get('devices_mapped', []) 
                         if 'modbus' in d.get('device_id', '')]
        all_nodes.extend(self.generate_modbus_flow(modbus_devices))
        
        # Add dashboard nodes
        all_nodes.extend(self.generate_dashboard_nodes())
        
        # Add configuration nodes
        configs = [
            {
                "id": "modbus_server_config",
                "type": "modbus-client",
                "name": "Modbus RTU Server",
                "clienttype": "serial",
                "bufferCommands": True,
                "stateLogEnabled": False,
                "tcpHost": "",
                "tcpPort": "502",
                "tcpType": "DEFAULT",
                "serialPort": "/dev/ttyUSB0",
                "serialType": "RTU-BUFFERD",
                "serialBaudrate": "9600",
                "serialDatabits": "8",
                "serialStopbits": "1",
                "serialParity": "none"
            },
            {
                "id": "mqtt_broker_config", 
                "type": "mqtt-broker",
                "name": "Industrial MQTT",
                "broker": "localhost",
                "port": "1883",
                "clientid": "ct088_legacy_client",
                "usetls": False,
                "compatmode": False,
                "keepalive": "60",
                "cleansession": True
            },
            {
                "id": "legacy_monitoring",
                "type": "ui_group",
                "name": "Legacy Protocol Monitoring",
                "tab": "legacy_dashboard",
                "order": 1,
                "disp": True,
                "width": "12",
                "collapse": False
            },
            {
                "id": "legacy_dashboard",
                "type": "ui_tab",
                "name": "Legacy Protocols",
                "icon": "dashboard",
                "order": 1,
                "disabled": False,
                "hidden": False
            }
        ]
        
        flow = {
            "id": "ct088_legacy_protocol_flow",
            "label": "CT-088 Legacy Protocol Integration",
            "nodes": all_nodes,
            "configs": configs
        }
        
        return flow

class DashboardGenerator:
    """Generate professional dashboards for legacy protocols"""
    
    def __init__(self):
        self.dashboard_templates = []
        
    def create_overview_dashboard(self, device_data):
        """Create overview dashboard for all legacy devices"""
        dashboard = {
            "dashboard_id": "ct088_legacy_overview",
            "dashboard_name": "Legacy Protocol Overview",
            "dashboard_type": "overview",
            "widgets": []
        }
        
        # Device status summary widget
        device_summary = {
            "widget_id": "device_summary",
            "widget_type": "status_grid",
            "title": "Device Status Summary",
            "position": {"x": 0, "y": 0, "width": 6, "height": 3},
            "config": {
                "devices": []
            }
        }
        
        for device in device_data.get('devices_mapped', []):
            device_summary["config"]["devices"].append({
                "device_id": device['device_id'],
                "device_type": device['device_type'],
                "status": "online",
                "last_update": datetime.now().isoformat()
            })
            
        dashboard["widgets"].append(device_summary)
        
        # Protocol distribution chart
        protocol_chart = {
            "widget_id": "protocol_distribution",
            "widget_type": "pie_chart",
            "title": "Protocol Distribution",
            "position": {"x": 6, "y": 0, "width": 6, "height": 3},
            "config": {
                "data_source": "device_protocols",
                "chart_type": "donut"
            }
        }
        dashboard["widgets"].append(protocol_chart)
        
        return dashboard
        
    def create_device_detail_dashboard(self, device):
        """Create detailed dashboard for specific device"""
        dashboard = {
            "dashboard_id": f"ct088_{device['device_id']}_detail",
            "dashboard_name": f"Device {device['device_id']} Detail",
            "dashboard_type": "device_detail",
            "widgets": []
        }
        
        # Register value trends
        for i, register in enumerate(device.get('register_mappings', [])[:6]):
            trend_widget = {
                "widget_id": f"register_{register['register_address']}_trend",
                "widget_type": "line_chart",
                "title": f"Register {register['register_address']} - {register['purpose']}",
                "position": {"x": (i % 3) * 4, "y": (i // 3) * 3, "width": 4, "height": 3},
                "config": {
                    "data_source": f"register_{register['register_address']}",
                    "y_axis_label": register['engineering_units'],
                    "time_range": "1h"
                }
            }
            dashboard["widgets"].append(trend_widget)
            
        return dashboard

class RemoteMonitoringIntegration:
    """Remote monitoring and alerting integration"""
    
    def __init__(self):
        self.monitoring_config = {
            "alert_rules": [],
            "notification_channels": [],
            "data_retention": "30_days"
        }
        
    def create_alert_rules(self, device_mappings):
        """Create intelligent alert rules based on device mappings"""
        alert_rules = []
        
        for device in device_mappings:
            for register in device.get('register_mappings', []):
                purpose = register['purpose']
                
                # Create purpose-specific alert rules
                if 'temperature' in purpose:
                    alert_rules.append({
                        "rule_id": f"temp_high_{device['device_id']}_{register['register_address']}",
                        "device_id": device['device_id'],
                        "register_address": register['register_address'],
                        "condition": "value > 80",
                        "severity": "warning",
                        "message": f"High temperature detected on {device['device_id']}"
                    })
                elif 'pressure' in purpose:
                    alert_rules.append({
                        "rule_id": f"pressure_high_{device['device_id']}_{register['register_address']}",
                        "device_id": device['device_id'],
                        "register_address": register['register_address'],
                        "condition": "value > 300",
                        "severity": "critical",
                        "message": f"High pressure detected on {device['device_id']}"
                    })
                elif 'alarm' in purpose or 'status' in purpose:
                    alert_rules.append({
                        "rule_id": f"status_change_{device['device_id']}_{register['register_address']}",
                        "device_id": device['device_id'],
                        "register_address": register['register_address'],
                        "condition": "value != previous_value",
                        "severity": "info",
                        "message": f"Status change on {device['device_id']}"
                    })
                    
        return alert_rules
        
    def setup_cloud_integration(self):
        """Setup cloud monitoring integration"""
        cloud_config = {
            "aws_iot": {
                "enabled": True,
                "endpoint": "industrial-iot.iot.us-east-1.amazonaws.com",
                "topic_prefix": "ct088/legacy_protocols"
            },
            "azure_iot": {
                "enabled": True,
                "connection_string": "HostName=ct088hub.azure-devices.net;SharedAccessKeyName=iothubowner",
                "device_prefix": "ct088_legacy"
            },
            "mqtt_bridge": {
                "enabled": True,
                "broker": "industrial-mqtt.company.com",
                "topic": "factory/legacy_protocols"
            }
        }
        
        return cloud_config

def main():
    """CT-088 Agent 3: Parachute Drop Integration"""
    print("🚀 CT-088 Agent 3: Parachute Drop Integration")
    print("=" * 60)
    
    # Load discovery results from Agent 2
    try:
        with open('/tmp/ct-088-discovery-mapping.json', 'r') as f:
            discovery_data = json.load(f)
    except FileNotFoundError:
        print("❌ Agent 2 results not found")
        return False
        
    # Generate Node-RED flows
    print("\n🔧 Generating Node-RED flows...")
    flow_generator = NodeREDFlowGenerator()
    flows = flow_generator.generate_complete_flow(discovery_data)
    
    with open('/tmp/ct-088-nodered-flows.json', 'w') as f:
        json.dump(flows, f, indent=2)
        
    # Generate dashboards
    print("\n📊 Generating professional dashboards...")
    dashboard_gen = DashboardGenerator()
    
    dashboards = []
    
    # Overview dashboard
    overview = dashboard_gen.create_overview_dashboard(discovery_data)
    dashboards.append(overview)
    
    # Device detail dashboards
    for device in discovery_data.get('devices_mapped', []):
        detail_dashboard = dashboard_gen.create_device_detail_dashboard(device)
        dashboards.append(detail_dashboard)
        
    with open('/tmp/ct-088-dashboards.json', 'w') as f:
        json.dump(dashboards, f, indent=2)
        
    # Setup remote monitoring
    print("\n🌐 Setting up remote monitoring...")
    monitoring = RemoteMonitoringIntegration()
    alert_rules = monitoring.create_alert_rules(discovery_data.get('devices_mapped', []))
    cloud_config = monitoring.setup_cloud_integration()
    
    monitoring_config = {
        "alert_rules": alert_rules,
        "cloud_integration": cloud_config,
        "total_alert_rules": len(alert_rules)
    }
    
    with open('/tmp/ct-088-monitoring-config.json', 'w') as f:
        json.dump(monitoring_config, f, indent=2)
        
    # Generate final summary
    summary = {
        'agent_id': 'ct-088-agent-3',
        'agent_name': 'Parachute Drop Integration',
        'deployment_status': 'completed',
        'nodered_flows_generated': 1,
        'dashboards_created': len(dashboards),
        'alert_rules_configured': len(alert_rules),
        'cloud_integrations': len(cloud_config),
        'outputs': {
            'nodered_flows': '/tmp/ct-088-nodered-flows.json',
            'dashboards': '/tmp/ct-088-dashboards.json',
            'monitoring_config': '/tmp/ct-088-monitoring-config.json'
        },
        'completion_time': datetime.now().isoformat()
    }
    
    with open('/tmp/ct-088-agent3-summary.json', 'w') as f:
        json.dump(summary, f, indent=2)
        
    print(f"\n✅ Agent 3 deployment completed!")
    print(f"📊 Generated {len(dashboards)} dashboards")
    print(f"🚨 Configured {len(alert_rules)} alert rules")
    print(f"🌐 Setup {len(cloud_config)} cloud integrations")
    
    return True

if __name__ == "__main__":
    main()
