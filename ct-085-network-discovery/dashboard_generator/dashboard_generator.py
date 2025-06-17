#!/usr/bin/env python3
"""
CT-085 Professional Dashboard Generator - Agent 4
Creates industrial monitoring interfaces for discovered systems
"""

import asyncio
import json
import logging
from typing import Dict, List, Any
from datetime import datetime
import uuid

logger = logging.getLogger(__name__)

class DashboardGenerator:
    """Professional dashboard generator for industrial monitoring interfaces"""
    
    def __init__(self):
        """Initialize dashboard generator"""
        self.dashboard_templates = self._load_dashboard_templates()
        self.generated_dashboards = {}
        
    def _load_dashboard_templates(self) -> Dict[str, Any]:
        """Load dashboard templates for different industrial scenarios"""
        return {
            'industrial_overview': {
                'title': 'Industrial Network Overview',
                'layout': 'grid',
                'widgets': ['device_summary', 'protocol_distribution', 'network_topology', 'alert_panel'],
                'refresh_rate': 5000,
                'theme': 'industrial_dark'
            },
            'device_detail': {
                'title': 'Device Detail Monitor',
                'layout': 'tabs',
                'widgets': ['device_info', 'tag_values', 'diagnostics', 'trending'],
                'refresh_rate': 1000,
                'theme': 'industrial_light'
            },
            'process_control': {
                'title': 'Process Control Dashboard',
                'layout': 'responsive',
                'widgets': ['process_variables', 'setpoints', 'control_outputs', 'alarms'],
                'refresh_rate': 500,
                'theme': 'process_blue'
            }
        }
    
    async def generate_dashboards(self, discovered_devices: Dict, tag_analysis: List) -> Dict[str, Any]:
        """Generate professional dashboards from discovery data"""
        dashboards = {
            'overview': await self._create_overview_dashboard(discovered_devices),
            'devices': await self._create_device_dashboards(discovered_devices, tag_analysis),
            'process': await self._create_process_dashboard(tag_analysis),
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'device_count': sum(len(devices) for devices in discovered_devices.values()),
                'tag_count': len(tag_analysis)
            }
        }
        
        self.generated_dashboards[datetime.now().isoformat()] = dashboards
        return dashboards
    
    async def _create_overview_dashboard(self, discovered_devices: Dict) -> Dict[str, Any]:
        """Create industrial network overview dashboard"""
        return {
            'id': 'industrial_overview',
            'title': 'Industrial Network Overview',
            'layout': {
                'type': 'grid',
                'columns': 12,
                'rows': 8,
                'gap': 10
            },
            'widgets': [
                {
                    'id': 'device_summary',
                    'type': 'summary_card',
                    'title': 'Discovered Devices',
                    'position': {'x': 0, 'y': 0, 'w': 3, 'h': 2},
                    'data_source': 'device_count',
                    'value': sum(len(devices) for devices in discovered_devices.values()),
                    'icon': 'industrial',
                    'color': 'blue'
                },
                {
                    'id': 'protocol_chart',
                    'type': 'pie_chart',
                    'title': 'Protocol Distribution',
                    'position': {'x': 3, 'y': 0, 'w': 4, 'h': 4},
                    'data': [
                        {'protocol': protocol, 'count': len(devices)} 
                        for protocol, devices in discovered_devices.items()
                    ]
                },
                {
                    'id': 'network_topology',
                    'type': 'network_diagram',
                    'title': 'Network Topology',
                    'position': {'x': 7, 'y': 0, 'w': 5, 'h': 6},
                    'devices': discovered_devices
                },
                {
                    'id': 'device_list',
                    'type': 'data_table',
                    'title': 'Device List',
                    'position': {'x': 0, 'y': 4, 'w': 7, 'h': 4},
                    'columns': ['IP Address', 'Protocol', 'Manufacturer', 'Model', 'Status'],
                    'data': self._format_device_table_data(discovered_devices)
                }
            ],
            'refresh_rate': 5000,
            'theme': 'industrial_dark'
        }
    
    async def _create_device_dashboards(self, discovered_devices: Dict, tag_analysis: List) -> List[Dict[str, Any]]:
        """Create individual device monitoring dashboards"""
        device_dashboards = []
        
        for protocol, devices in discovered_devices.items():
            for device in devices:
                dashboard = await self._create_single_device_dashboard(device, tag_analysis)
                device_dashboards.append(dashboard)
        
        return device_dashboards
    
    async def _create_single_device_dashboard(self, device: Any, tag_analysis: List) -> Dict[str, Any]:
        """Create dashboard for a single device"""
        device_id = f"{device.ip_address}_{device.port}"
        device_tags = [tag for tag in tag_analysis if device_id in tag.tag_name]
        
        return {
            'id': f'device_{device_id}',
            'title': f'{device.manufacturer} {device.model} Monitor',
            'layout': {
                'type': 'tabs',
                'tabs': ['overview', 'tags', 'diagnostics', 'trends']
            },
            'tabs': {
                'overview': {
                    'widgets': [
                        {
                            'id': 'device_info',
                            'type': 'info_panel',
                            'title': 'Device Information',
                            'data': {
                                'ip_address': device.ip_address,
                                'port': device.port,
                                'protocol': device.protocol,
                                'manufacturer': device.manufacturer,
                                'model': device.model,
                                'last_seen': getattr(device, 'last_seen', datetime.now()).isoformat()
                            }
                        },
                        {
                            'id': 'connection_status',
                            'type': 'status_indicator',
                            'title': 'Connection Status',
                            'value': getattr(device, 'connection_status', 'Active'),
                            'color_mapping': {
                                'Active': 'green',
                                'Inactive': 'red',
                                'Warning': 'yellow'
                            }
                        }
                    ]
                },
                'tags': {
                    'widgets': [
                        {
                            'id': f'tag_table_{device_id}',
                            'type': 'tag_table',
                            'title': 'Device Tags',
                            'data': [
                                {
                                    'name': tag.tag_name,
                                    'purpose': tag.purpose,
                                    'data_type': tag.data_type,
                                    'units': tag.units,
                                    'criticality': tag.criticality
                                }
                                for tag in device_tags
                            ]
                        }
                    ]
                }
            },
            'refresh_rate': 2000
        }
    
    async def _create_process_dashboard(self, tag_analysis: List) -> Dict[str, Any]:
        """Create process control dashboard"""
        process_variables = [tag for tag in tag_analysis if tag.purpose == 'Process Variable']
        setpoints = [tag for tag in tag_analysis if tag.purpose == 'Setpoint']
        control_outputs = [tag for tag in tag_analysis if tag.purpose == 'Control Output']
        alarms = [tag for tag in tag_analysis if tag.purpose == 'Alarm']
        
        return {
            'id': 'process_control',
            'title': 'Process Control Dashboard',
            'layout': {
                'type': 'responsive',
                'breakpoints': {'lg': 1200, 'md': 996, 'sm': 768, 'xs': 480}
            },
            'widgets': [
                {
                    'id': 'pv_panel',
                    'type': 'gauge_panel',
                    'title': 'Process Variables',
                    'position': {'x': 0, 'y': 0, 'w': 6, 'h': 4},
                    'gauges': [
                        {
                            'tag': tag.tag_name,
                            'label': tag.description,
                            'units': tag.units,
                            'min': 0,
                            'max': 100,
                            'ranges': [
                                {'from': 0, 'to': 33, 'color': 'green'},
                                {'from': 33, 'to': 66, 'color': 'yellow'},
                                {'from': 66, 'to': 100, 'color': 'red'}
                            ]
                        }
                        for tag in process_variables[:6]
                    ]
                },
                {
                    'id': 'setpoint_panel',
                    'type': 'input_panel',
                    'title': 'Setpoints',
                    'position': {'x': 6, 'y': 0, 'w': 3, 'h': 4},
                    'inputs': [
                        {
                            'tag': tag.tag_name,
                            'label': tag.description,
                            'units': tag.units,
                            'min': 0,
                            'max': 100,
                            'step': 0.1
                        }
                        for tag in setpoints[:8]
                    ]
                },
                {
                    'id': 'alarm_panel',
                    'type': 'alarm_list',
                    'title': 'Active Alarms',
                    'position': {'x': 9, 'y': 0, 'w': 3, 'h': 8},
                    'alarms': [
                        {
                            'tag': tag.tag_name,
                            'description': tag.description,
                            'criticality': tag.criticality,
                            'timestamp': datetime.now().isoformat(),
                            'acknowledged': False
                        }
                        for tag in alarms
                    ]
                },
                {
                    'id': 'trend_chart',
                    'type': 'time_series_chart',
                    'title': 'Process Trends',
                    'position': {'x': 0, 'y': 4, 'w': 9, 'h': 4},
                    'series': [
                        {
                            'tag': tag.tag_name,
                            'label': tag.description,
                            'color': self._get_tag_color(tag.category),
                            'units': tag.units
                        }
                        for tag in process_variables[:4]
                    ],
                    'time_range': '1h',
                    'update_interval': 1000
                }
            ],
            'refresh_rate': 500,
            'theme': 'process_blue'
        }
    
    def _format_device_table_data(self, discovered_devices: Dict) -> List[Dict[str, str]]:
        """Format device data for table display"""
        table_data = []
        
        for protocol, devices in discovered_devices.items():
            for device in devices:
                table_data.append({
                    'ip_address': device.ip_address,
                    'protocol': protocol.upper(),
                    'manufacturer': device.manufacturer,
                    'model': device.model,
                    'status': getattr(device, 'connection_status', 'Active')
                })
        
        return table_data
    
    def _get_tag_color(self, category: str) -> str:
        """Get color for tag category"""
        color_map = {
            'Temperature Control': '#ff6b6b',
            'Pressure Control': '#4ecdc4',
            'Flow Control': '#45b7d1',
            'Level Control': '#96ceb4',
            'Process Control': '#ffeaa7',
            'Monitoring': '#dda0dd',
            'Production Tracking': '#98d8c8',
            'System Configuration': '#a8e6cf'
        }
        return color_map.get(category, '#95a5a6')
    
    def export_dashboards(self, dashboards: Dict[str, Any], export_format: str = 'json') -> str:
        """Export dashboards to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if export_format == 'json':
            filename = f"/home/server/industrial-iot-stack/ct-085-network-discovery/dashboard_generator/ct085_dashboards_{timestamp}.json"
            with open(filename, 'w') as f:
                json.dump(dashboards, f, indent=2)
        elif export_format == 'html':
            filename = f"/home/server/industrial-iot-stack/ct-085-network-discovery/dashboard_generator/ct085_dashboards_{timestamp}.html"
            html_content = self._generate_html_dashboard(dashboards)
            with open(filename, 'w') as f:
                f.write(html_content)
        
        logger.info(f"Dashboards exported to {filename}")
        return filename
    
    def _generate_html_dashboard(self, dashboards: Dict[str, Any]) -> str:
        """Generate HTML dashboard for web deployment"""
        html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CT-085 Industrial Dashboard</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #2c3e50; color: white; }
        .dashboard { display: grid; grid-template-columns: repeat(12, 1fr); gap: 20px; }
        .widget { background: #34495e; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.3); }
        .widget h3 { margin-top: 0; color: #3498db; }
        .device-table { width: 100%; border-collapse: collapse; }
        .device-table th, .device-table td { padding: 12px; text-align: left; border-bottom: 1px solid #7f8c8d; }
        .device-table th { background: #3498db; color: white; }
        .status-active { color: #2ecc71; font-weight: bold; }
    </style>
</head>
<body>
    <h1>CT-085 Industrial Network Dashboard</h1>
    <div class="dashboard">
        <div class="widget" style="grid-column: span 4;">
            <h3>Network Overview</h3>
            <p>Total Devices: {device_count}</p>
            <p>Protocols: {protocol_list}</p>
            <p>Generated: {timestamp}</p>
        </div>
        <div class="widget" style="grid-column: span 8;">
            <h3>Discovered Devices</h3>
            <table class="device-table">
                <thead>
                    <tr><th>IP Address</th><th>Protocol</th><th>Manufacturer</th><th>Model</th><th>Status</th></tr>
                </thead>
                <tbody>
                    {device_rows}
                </tbody>
            </table>
        </div>
    </div>
</body>
</html>"""
        
        # Extract data for HTML template
        device_count = dashboards['metadata']['device_count']
        protocols = list(dashboards.get('overview', {}).get('widgets', [{}])[1].get('data', []))
        protocol_list = ', '.join([p.get('protocol', '') for p in protocols])
        timestamp = dashboards['metadata']['generated_at']
        
        # Generate device table rows
        device_data = dashboards.get('overview', {}).get('widgets', [{}])[-1].get('data', [])
        device_rows = '\n'.join([
            f"<tr><td>{row['ip_address']}</td><td>{row['protocol']}</td><td>{row['manufacturer']}</td><td>{row['model']}</td><td class='status-active'>{row['status']}</td></tr>"
            for row in device_data
        ])
        
        return html_template.format(
            device_count=device_count,
            protocol_list=protocol_list,
            timestamp=timestamp,
            device_rows=device_rows
        )

# Test functionality  
if __name__ == "__main__":
    async def test_dashboard_generator():
        generator = DashboardGenerator()
        
        # Mock data
        from dataclasses import dataclass
        
        @dataclass
        class MockDevice:
            ip_address: str
            port: int
            protocol: str
            manufacturer: str
            model: str
            connection_status: str = 'Active'
        
        @dataclass
        class MockTag:
            tag_name: str
            purpose: str
            data_type: str
            units: str
            description: str
            category: str
            criticality: str
        
        devices = {
            'modbus': [MockDevice('192.168.1.100', 502, 'modbus', 'Allen-Bradley', 'CompactLogix')],
            'opcua': [MockDevice('192.168.1.101', 4840, 'opcua', 'Siemens', 'S7-1500')]
        }
        
        tags = [
            MockTag('TEMP_01_PV', 'Process Variable', 'REAL', 'degC', 'Temperature 1', 'Temperature Control', 'Medium'),
            MockTag('PRESS_01_SP', 'Setpoint', 'REAL', 'bar', 'Pressure Setpoint', 'Pressure Control', 'High')
        ]
        
        # Generate dashboards
        dashboards = await generator.generate_dashboards(devices, tags)
        
        # Export
        json_file = generator.export_dashboards(dashboards, 'json')
        html_file = generator.export_dashboards(dashboards, 'html')
        
        print(f"Dashboards generated:")
        print(f"JSON: {json_file}")
        print(f"HTML: {html_file}")
    
    asyncio.run(test_dashboard_generator())