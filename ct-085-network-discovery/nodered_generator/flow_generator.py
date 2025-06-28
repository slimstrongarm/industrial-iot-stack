#!/usr/bin/env python3
"""
CT-085 Auto Node-RED Generator - Agent 3
Dynamic Node-RED flow creation from discovered devices and AI tag analysis
"""

import asyncio
import json
import logging
from typing import Dict, List, Any
from datetime import datetime
import uuid

logger = logging.getLogger(__name__)

class NodeREDFlowGenerator:
    """Auto-generates Node-RED flows from discovered industrial devices"""
    
    def __init__(self):
        """Initialize the Node-RED flow generator"""
        self.flow_templates = self._load_flow_templates()
        self.generated_flows = {}
        
    def _load_flow_templates(self) -> Dict[str, Any]:
        """Load Node-RED flow templates for different device types"""
        return {
            'modbus_read': {
                "id": "template_modbus_read",
                "type": "Modbus-Read",
                "name": "Read {device_name}",
                "topic": "",
                "showStatusActivities": False,
                "logIOActivities": False,
                "showErrors": False,
                "unitid": 1,
                "dataType": "HoldingRegister",
                "adr": "0",
                "quantity": "1",
                "server": "{server_id}",
                "useIOFile": False,
                "ioFile": "",
                "useIOForPayload": False,
                "emptyMsgOnFail": False,
                "x": 300,
                "y": 100
            },
            'opcua_read': {
                "id": "template_opcua_read",
                "type": "OpcUa-Item",
                "item": "ns=1;s={tag_name}",
                "datatype": "NodeId",
                "value": "",
                "name": "Read {device_name}",
                "topic": "{tag_name}",
                "x": 300,
                "y": 100
            },
            'mqtt_pub': {
                "id": "template_mqtt_pub",
                "type": "mqtt out",
                "name": "Publish {device_name}",
                "topic": "industrial/{device_type}/{device_id}",
                "qos": "1",
                "retain": "false",
                "broker": "{mqtt_broker}",
                "x": 600,
                "y": 100
            },
            'dashboard_gauge': {
                "id": "template_gauge",
                "type": "ui_gauge",
                "name": "{tag_name} Gauge",
                "label": "{tag_name}",
                "tooltip": "",
                "group": "{dashboard_group}",
                "order": 1,
                "width": "6",
                "height": "4",
                "gtype": "gage",
                "title": "{device_name}",
                "min": 0,
                "max": 100,
                "colors": ["#00b500","#e6e600","#ca3838"],
                "seg1": "33",
                "seg2": "66",
                "x": 800,
                "y": 100
            }
        }
    
    async def generate_flows_from_discovery(self, discovered_devices: Dict[str, List], tag_analysis: List) -> Dict[str, Any]:
        """Generate Node-RED flows from network discovery results"""
        flows = {
            "flows": [],
            "configs": [],
            "rev": str(uuid.uuid4())
        }
        
        y_position = 100
        
        # Process each protocol and its devices
        for protocol, devices in discovered_devices.items():
            for device in devices:
                device_flows = await self._generate_device_flows(device, tag_analysis, y_position)
                flows["flows"].extend(device_flows)
                y_position += 200
        
        # Add configuration nodes
        flows["configs"].extend(self._generate_config_nodes(discovered_devices))
        
        self.generated_flows[datetime.now().isoformat()] = flows
        return flows
    
    async def _generate_device_flows(self, device: Any, tag_analysis: List, y_pos: int) -> List[Dict]:
        """Generate flows for a specific device"""
        device_flows = []
        
        protocol = device.protocol
        device_name = f"{device.manufacturer}_{device.model}".replace(" ", "_")
        device_id = f"{device.ip_address}_{device.port}"
        
        if protocol == 'modbus':
            device_flows.extend(self._create_modbus_flows(device, device_name, device_id, y_pos))
        elif protocol == 'opcua':
            device_flows.extend(self._create_opcua_flows(device, device_name, device_id, y_pos))
        elif protocol == 'mqtt':
            device_flows.extend(self._create_mqtt_flows(device, device_name, device_id, y_pos))
        
        return device_flows
    
    def _create_modbus_flows(self, device: Any, device_name: str, device_id: str, y_pos: int) -> List[Dict]:
        """Create Modbus-specific flows"""
        flows = []
        x_pos = 100
        
        # Modbus read node
        read_node = self.flow_templates['modbus_read'].copy()
        read_node.update({
            "id": f"modbus_read_{device_id}",
            "name": f"Read {device_name}",
            "unitid": getattr(device, 'unit_id', 1),
            "server": f"modbus_server_{device_id}",
            "x": x_pos,
            "y": y_pos,
            "wires": [[f"mqtt_pub_{device_id}", f"gauge_{device_id}"]]
        })
        flows.append(read_node)
        
        # MQTT publish node
        mqtt_node = self.flow_templates['mqtt_pub'].copy()
        mqtt_node.update({
            "id": f"mqtt_pub_{device_id}",
            "name": f"Publish {device_name}",
            "topic": f"industrial/modbus/{device_id}",
            "broker": "mqtt_broker_local",
            "x": x_pos + 300,
            "y": y_pos
        })
        flows.append(mqtt_node)
        
        # Dashboard gauge
        gauge_node = self.flow_templates['dashboard_gauge'].copy()
        gauge_node.update({
            "id": f"gauge_{device_id}",
            "name": f"{device_name} Status",
            "label": f"{device_name}",
            "title": f"{device.manufacturer} {device.model}",
            "group": "dashboard_group_industrial",
            "x": x_pos + 300,
            "y": y_pos + 100
        })
        flows.append(gauge_node)
        
        # Inject node for periodic reading
        inject_node = {
            "id": f"inject_{device_id}",
            "type": "inject",
            "name": f"Poll {device_name}",
            "repeat": "5",
            "crontab": "",
            "once": True,
            "onceDelay": 0.1,
            "topic": "",
            "payload": "",
            "payloadType": "date",
            "x": x_pos - 150,
            "y": y_pos,
            "wires": [[f"modbus_read_{device_id}"]]
        }
        flows.append(inject_node)
        
        return flows
    
    def _create_opcua_flows(self, device: Any, device_name: str, device_id: str, y_pos: int) -> List[Dict]:
        """Create OPC-UA specific flows"""
        flows = []
        x_pos = 100
        
        # OPC-UA read node
        read_node = self.flow_templates['opcua_read'].copy()
        read_node.update({
            "id": f"opcua_read_{device_id}",
            "name": f"Read {device_name}",
            "item": f"ns=1;s=ServerStatus",
            "topic": f"{device_name}_status",
            "x": x_pos,
            "y": y_pos,
            "wires": [[f"mqtt_pub_{device_id}", f"gauge_{device_id}"]]
        })
        flows.append(read_node)
        
        # MQTT publish node
        mqtt_node = self.flow_templates['mqtt_pub'].copy()
        mqtt_node.update({
            "id": f"mqtt_pub_{device_id}",
            "topic": f"industrial/opcua/{device_id}",
            "x": x_pos + 300,
            "y": y_pos
        })
        flows.append(mqtt_node)
        
        return flows
    
    def _create_mqtt_flows(self, device: Any, device_name: str, device_id: str, y_pos: int) -> List[Dict]:
        """Create MQTT broker monitoring flows"""
        flows = []
        x_pos = 100
        
        # MQTT subscribe node
        subscribe_node = {
            "id": f"mqtt_sub_{device_id}",
            "type": "mqtt in",
            "name": f"Monitor {device_name}",
            "topic": "#",
            "qos": "1",
            "datatype": "auto",
            "broker": f"mqtt_broker_{device_id}",
            "x": x_pos,
            "y": y_pos,
            "wires": [[f"debug_{device_id}"]]
        }
        flows.append(subscribe_node)
        
        # Debug node
        debug_node = {
            "id": f"debug_{device_id}",
            "type": "debug",
            "name": f"Debug {device_name}",
            "active": True,
            "tosidebar": True,
            "console": False,
            "tostatus": False,
            "complete": "payload",
            "targetType": "msg",
            "x": x_pos + 300,
            "y": y_pos
        }
        flows.append(debug_node)
        
        return flows
    
    def _generate_config_nodes(self, discovered_devices: Dict[str, List]) -> List[Dict]:
        """Generate configuration nodes for servers and brokers"""
        configs = []
        
        # Modbus server configs
        modbus_devices = discovered_devices.get('modbus', [])
        for device in modbus_devices:
            device_id = f"{device.ip_address}_{device.port}"
            config = {
                "id": f"modbus_server_{device_id}",
                "type": "modbus-client",
                "name": f"Modbus {device.manufacturer}",
                "clienttype": "tcp",
                "bufferCommands": True,
                "stateLogEnabled": False,
                "queueLogEnabled": False,
                "tcpHost": device.ip_address,
                "tcpPort": str(device.port),
                "tcpType": "DEFAULT",
                "serialPort": "/dev/ttyUSB",
                "serialType": "RTU-BUFFERD",
                "serialBaudrate": "9600",
                "serialDatabits": "8",
                "serialStopbits": "1",
                "serialParity": "none",
                "serialConnectionDelay": "100",
                "unit_id": getattr(device, 'unit_id', 1),
                "commandDelay": "1",
                "clientTimeout": "5000",
                "reconnectOnTimeout": True,
                "reconnectTimeout": "2000",
                "parallelUnitIdsAllowed": True
            }
            configs.append(config)
        
        # MQTT broker config
        mqtt_config = {
            "id": "mqtt_broker_local",
            "type": "mqtt-broker",
            "name": "Local MQTT Broker",
            "broker": "localhost",
            "port": "1883",
            "clientid": "",
            "usetls": False,
            "compatmode": False,
            "keepalive": "60",
            "cleansession": True,
            "birthTopic": "",
            "birthQos": "0",
            "birthPayload": "",
            "closeTopic": "",
            "closeQos": "0",
            "closePayload": "",
            "willTopic": "",
            "willQos": "0",
            "willPayload": ""
        }
        configs.append(mqtt_config)
        
        # Dashboard group config
        dashboard_config = {
            "id": "dashboard_group_industrial",
            "type": "ui_group",
            "name": "Industrial Devices",
            "tab": "dashboard_tab_main",
            "order": 1,
            "disp": True,
            "width": "12",
            "collapse": False
        }
        configs.append(dashboard_config)
        
        return configs
    
    async def deploy_flows_to_nodered(self, flows: Dict[str, Any], nodered_url: str = "http://localhost:1880") -> bool:
        """Deploy generated flows to Node-RED instance"""
        try:
            import aiohttp
            
            async with aiohttp.ClientSession() as session:
                # Deploy flows
                async with session.post(
                    f"{nodered_url}/flows",
                    json=flows,
                    headers={"Content-Type": "application/json"}
                ) as response:
                    if response.status == 200:
                        logger.info("Flows deployed successfully to Node-RED")
                        return True
                    else:
                        logger.error(f"Failed to deploy flows: {response.status}")
                        return False
                        
        except Exception as e:
            logger.error(f"Error deploying flows: {e}")
            return False
    
    def export_flows_to_file(self, flows: Dict[str, Any], filename: str = None) -> str:
        """Export flows to JSON file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"/home/server/industrial-iot-stack/ct-085-network-discovery/nodered_generator/flows/ct085_flows_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(flows, f, indent=2)
        
        logger.info(f"Flows exported to {filename}")
        return filename

# Test functionality
if __name__ == "__main__":
    async def test_flow_generator():
        generator = NodeREDFlowGenerator()
        
        # Mock discovered devices
        from dataclasses import dataclass
        
        @dataclass
        class MockDevice:
            ip_address: str
            port: int
            protocol: str
            manufacturer: str
            model: str
            unit_id: int = 1
        
        devices = {
            'modbus': [
                MockDevice('192.168.1.100', 502, 'modbus', 'Allen-Bradley', 'CompactLogix', 1),
                MockDevice('192.168.1.101', 502, 'modbus', 'Schneider', 'M580', 2)
            ],
            'opcua': [
                MockDevice('192.168.1.102', 4840, 'opcua', 'Siemens', 'S7-1500', 1)
            ]
        }
        
        # Generate flows
        flows = await generator.generate_flows_from_discovery(devices, [])
        
        # Export to file
        filename = generator.export_flows_to_file(flows)
        print(f"Generated flows exported to: {filename}")
        print(f"Flow count: {len(flows['flows'])}")
        print(f"Config count: {len(flows['configs'])}")
    
    asyncio.run(test_flow_generator())