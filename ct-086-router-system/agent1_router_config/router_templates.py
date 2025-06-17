#!/usr/bin/env python3
"""
CT-086 Agent 1: Router Configuration Templates
Pre-built configurations for common industrial deployment scenarios

This module provides configuration templates for different GL.iNet router
models and deployment scenarios in industrial environments.
"""

import json
import yaml
from typing import Dict, Any, List
from dataclasses import dataclass, asdict
from enum import Enum


class RouterModel(Enum):
    """Supported GL.iNet router models"""
    FLINT = "GL-AX1800"      # High-performance WiFi 6
    BERYL = "GL-MT1300"      # Portable travel router
    SLATE = "GL-AR750S"      # Dual-band gigabit
    MANGO = "GL-MT300N-V2"   # Mini pocket router
    BRUME = "GL-MV1000"      # Gigabit VPN gateway


class DeploymentScenario(Enum):
    """Industrial deployment scenarios"""
    MANUFACTURING_FLOOR = "manufacturing_floor"
    PROCESS_CONTROL = "process_control"
    REMOTE_MONITORING = "remote_monitoring"
    MAINTENANCE_ACCESS = "maintenance_access"
    TEMPORARY_DEPLOYMENT = "temporary_deployment"
    EDGE_GATEWAY = "edge_gateway"


@dataclass
class RouterTemplate:
    """Router configuration template"""
    name: str
    model: RouterModel
    scenario: DeploymentScenario
    description: str
    network_config: Dict[str, Any]
    wifi_config: Dict[str, Any]
    firewall_config: Dict[str, Any]
    additional_features: List[str]


class RouterConfigurationTemplates:
    """
    Router configuration templates for industrial deployments
    """
    
    def __init__(self):
        self.templates: Dict[str, RouterTemplate] = {}
        self._initialize_templates()
    
    def _initialize_templates(self):
        """Initialize all configuration templates"""
        
        # Manufacturing Floor Template
        self.templates["manufacturing_floor_flint"] = RouterTemplate(
            name="Manufacturing Floor - High Performance",
            model=RouterModel.FLINT,
            scenario=DeploymentScenario.MANUFACTURING_FLOOR,
            description="High-density industrial network for manufacturing floor with multiple production lines",
            network_config={
                "vlans": [
                    {"id": 10, "name": "management", "subnet": "192.168.10.0/24", "priority": "critical"},
                    {"id": 20, "name": "production", "subnet": "192.168.20.0/24", "priority": "critical"},
                    {"id": 21, "name": "quality", "subnet": "192.168.21.0/24", "priority": "high"},
                    {"id": 30, "name": "data_collection", "subnet": "192.168.30.0/24", "priority": "medium"},
                    {"id": 40, "name": "maintenance", "subnet": "192.168.40.0/24", "priority": "medium"}
                ],
                "dhcp_ranges": {
                    "management": {"start": 10, "end": 50},
                    "production": {"start": 10, "end": 200},
                    "quality": {"start": 10, "end": 100},
                    "data_collection": {"start": 10, "end": 150},
                    "maintenance": {"start": 10, "end": 50}
                }
            },
            wifi_config={
                "networks": [
                    {
                        "ssid": "ManufacturingFloor-Mgmt",
                        "vlan": 10,
                        "security": "wpa3",
                        "hidden": True,
                        "band": "both"
                    },
                    {
                        "ssid": "ManufacturingFloor-Prod",
                        "vlan": 20,
                        "security": "wpa3",
                        "hidden": True,
                        "band": "5ghz"
                    },
                    {
                        "ssid": "ManufacturingFloor-Data",
                        "vlan": 30,
                        "security": "wpa2",
                        "hidden": False,
                        "band": "2.4ghz"
                    }
                ]
            },
            firewall_config={
                "default_policy": "drop",
                "rules": [
                    {
                        "name": "mgmt_full_access",
                        "src": "vlan10",
                        "dest": "*",
                        "action": "accept"
                    },
                    {
                        "name": "production_to_data",
                        "src": "vlan20",
                        "dest": "vlan30",
                        "ports": [502, 4840, 1883],
                        "action": "accept"
                    },
                    {
                        "name": "quality_restricted",
                        "src": "vlan21",
                        "dest": "vlan20,vlan30",
                        "ports": [80, 443, 4840],
                        "action": "accept"
                    }
                ]
            },
            additional_features=[
                "load_balancing",
                "bandwidth_monitoring",
                "device_discovery",
                "alert_notifications"
            ]
        )
        
        # Process Control Template
        self.templates["process_control_brume"] = RouterTemplate(
            name="Process Control - Secure Gateway",
            model=RouterModel.BRUME,
            scenario=DeploymentScenario.PROCESS_CONTROL,
            description="Ultra-secure process control network with strict isolation and VPN access",
            network_config={
                "vlans": [
                    {"id": 10, "name": "control_mgmt", "subnet": "10.1.10.0/24", "priority": "critical"},
                    {"id": 20, "name": "safety_systems", "subnet": "10.1.20.0/24", "priority": "critical"},
                    {"id": 21, "name": "process_control", "subnet": "10.1.21.0/24", "priority": "critical"},
                    {"id": 30, "name": "hmi_stations", "subnet": "10.1.30.0/24", "priority": "high"},
                    {"id": 40, "name": "engineering", "subnet": "10.1.40.0/24", "priority": "medium"}
                ],
                "dhcp_ranges": {
                    "control_mgmt": {"start": 10, "end": 30},
                    "safety_systems": {"start": 10, "end": 50},
                    "process_control": {"start": 10, "end": 100},
                    "hmi_stations": {"start": 10, "end": 50},
                    "engineering": {"start": 10, "end": 30}
                }
            },
            wifi_config={
                "networks": [
                    {
                        "ssid": "ProcessControl-Secure",
                        "vlan": 30,
                        "security": "wpa3",
                        "hidden": True,
                        "band": "5ghz",
                        "isolation": True
                    }
                ]
            },
            firewall_config={
                "default_policy": "drop",
                "strict_mode": True,
                "rules": [
                    {
                        "name": "safety_isolation",
                        "src": "vlan20",
                        "dest": "!vlan20",
                        "action": "drop",
                        "log": True
                    },
                    {
                        "name": "control_to_safety",
                        "src": "vlan21",
                        "dest": "vlan20",
                        "ports": [502],
                        "action": "accept",
                        "log": True
                    },
                    {
                        "name": "hmi_to_control",
                        "src": "vlan30",
                        "dest": "vlan21",
                        "ports": [4840, 502],
                        "action": "accept"
                    }
                ]
            },
            additional_features=[
                "vpn_server",
                "intrusion_detection",
                "activity_logging",
                "fail_safe_mode"
            ]
        )
        
        # Remote Monitoring Template
        self.templates["remote_monitoring_slate"] = RouterTemplate(
            name="Remote Monitoring - Edge Gateway",
            model=RouterModel.SLATE,
            scenario=DeploymentScenario.REMOTE_MONITORING,
            description="Remote site monitoring with cellular backup and cloud connectivity",
            network_config={
                "vlans": [
                    {"id": 10, "name": "monitoring", "subnet": "172.16.10.0/24", "priority": "high"},
                    {"id": 20, "name": "sensors", "subnet": "172.16.20.0/24", "priority": "medium"},
                    {"id": 30, "name": "maintenance", "subnet": "172.16.30.0/24", "priority": "low"}
                ],
                "dhcp_ranges": {
                    "monitoring": {"start": 10, "end": 50},
                    "sensors": {"start": 10, "end": 200},
                    "maintenance": {"start": 10, "end": 30}
                }
            },
            wifi_config={
                "networks": [
                    {
                        "ssid": "RemoteMonitoring",
                        "vlan": 10,
                        "security": "wpa2",
                        "hidden": False,
                        "band": "both"
                    },
                    {
                        "ssid": "RemoteMaintenance",
                        "vlan": 30,
                        "security": "wpa2",
                        "hidden": True,
                        "band": "2.4ghz"
                    }
                ]
            },
            firewall_config={
                "default_policy": "accept",
                "rules": [
                    {
                        "name": "sensor_data_flow",
                        "src": "vlan20",
                        "dest": "vlan10",
                        "ports": [1883, 8086],
                        "action": "accept"
                    },
                    {
                        "name": "remote_access",
                        "src": "wan",
                        "dest": "vlan10",
                        "ports": [443, 8080],
                        "action": "accept"
                    }
                ]
            },
            additional_features=[
                "cellular_backup",
                "cloud_sync",
                "data_buffering",
                "alert_forwarding"
            ]
        )
        
        # Temporary Deployment Template
        self.templates["temporary_deployment_beryl"] = RouterTemplate(
            name="Temporary Deployment - Portable Setup",
            model=RouterModel.BERYL,
            scenario=DeploymentScenario.TEMPORARY_DEPLOYMENT,
            description="Quick setup for temporary installations and testing",
            network_config={
                "vlans": [
                    {"id": 10, "name": "temp_mgmt", "subnet": "192.168.100.0/24", "priority": "medium"},
                    {"id": 20, "name": "temp_devices", "subnet": "192.168.101.0/24", "priority": "medium"},
                    {"id": 30, "name": "temp_guest", "subnet": "192.168.102.0/24", "priority": "low"}
                ],
                "dhcp_ranges": {
                    "temp_mgmt": {"start": 10, "end": 50},
                    "temp_devices": {"start": 10, "end": 100},
                    "temp_guest": {"start": 10, "end": 100}
                }
            },
            wifi_config={
                "networks": [
                    {
                        "ssid": "TempSetup-Devices",
                        "vlan": 20,
                        "security": "wpa2",
                        "hidden": False,
                        "band": "both"
                    },
                    {
                        "ssid": "TempSetup-Guest",
                        "vlan": 30,
                        "security": "wpa2",
                        "hidden": False,
                        "band": "2.4ghz"
                    }
                ]
            },
            firewall_config={
                "default_policy": "accept",
                "rules": [
                    {
                        "name": "allow_all_local",
                        "src": "lan",
                        "dest": "lan",
                        "action": "accept"
                    }
                ]
            },
            additional_features=[
                "easy_setup",
                "auto_configuration",
                "status_dashboard"
            ]
        )
    
    def get_template(self, template_name: str) -> Optional[RouterTemplate]:
        """Get a specific template"""
        return self.templates.get(template_name)
    
    def list_templates(self) -> List[str]:
        """List all available templates"""
        return list(self.templates.keys())
    
    def get_templates_by_model(self, model: RouterModel) -> List[RouterTemplate]:
        """Get templates for a specific router model"""
        return [template for template in self.templates.values() 
                if template.model == model]
    
    def get_templates_by_scenario(self, scenario: DeploymentScenario) -> List[RouterTemplate]:
        """Get templates for a specific deployment scenario"""
        return [template for template in self.templates.values() 
                if template.scenario == scenario]
    
    def generate_router_config(self, template_name: str, custom_params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Generate complete router configuration from template"""
        template = self.get_template(template_name)
        if not template:
            raise ValueError(f"Template '{template_name}' not found")
        
        # Base configuration
        config = {
            "system": {
                "hostname": f"parachute-drop-{template.scenario.value.replace('_', '-')}",
                "timezone": "UTC",
                "model": template.model.value,
                "deployment_scenario": template.scenario.value
            },
            "network": {
                "interfaces": {},
                "vlans": template.network_config["vlans"]
            },
            "wireless": {
                "networks": template.wifi_config["networks"]
            },
            "firewall": {
                "default_policy": template.firewall_config.get("default_policy", "drop"),
                "rules": template.firewall_config["rules"]
            },
            "dhcp": {
                "pools": []
            },
            "features": template.additional_features
        }
        
        # Generate network interfaces
        for vlan in template.network_config["vlans"]:
            interface_name = f"vlan{vlan['id']}"
            config["network"]["interfaces"][interface_name] = {
                "type": "bridge",
                "proto": "static",
                "ipaddr": vlan["subnet"].split('/')[0],
                "netmask": "255.255.255.0",
                "vlan_id": vlan["id"],
                "description": vlan["name"],
                "priority": vlan["priority"]
            }
            
            # Add DHCP pool
            dhcp_range = template.network_config["dhcp_ranges"].get(vlan["name"], {"start": 10, "end": 100})
            config["dhcp"]["pools"].append({
                "interface": interface_name,
                "start": dhcp_range["start"],
                "limit": dhcp_range["end"] - dhcp_range["start"],
                "leasetime": "12h"
            })
        
        # Apply custom parameters
        if custom_params:
            self._apply_custom_params(config, custom_params)
        
        return config
    
    def _apply_custom_params(self, config: Dict[str, Any], custom_params: Dict[str, Any]):
        """Apply custom parameters to configuration"""
        if "hostname" in custom_params:
            config["system"]["hostname"] = custom_params["hostname"]
        
        if "wifi_passwords" in custom_params:
            for i, network in enumerate(config["wireless"]["networks"]):
                if i < len(custom_params["wifi_passwords"]):
                    network["password"] = custom_params["wifi_passwords"][i]
        
        if "additional_vlans" in custom_params:
            for vlan in custom_params["additional_vlans"]:
                config["network"]["vlans"].append(vlan)
    
    def export_template(self, template_name: str, format_type: str = "json") -> str:
        """Export template configuration"""
        template = self.get_template(template_name)
        if not template:
            raise ValueError(f"Template '{template_name}' not found")
        
        config = self.generate_router_config(template_name)
        
        if format_type.lower() == "yaml":
            return yaml.dump(config, default_flow_style=False, indent=2)
        else:
            return json.dumps(config, indent=2, default=str)
    
    def export_all_templates(self, output_dir: str = "/home/server/industrial-iot-stack/ct-086-router-system/agent1_router_config/templates/"):
        """Export all templates to files"""
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        for template_name in self.templates:
            # Export JSON
            json_config = self.export_template(template_name, "json")
            with open(f"{output_dir}{template_name}.json", "w") as f:
                f.write(json_config)
            
            # Export YAML
            yaml_config = self.export_template(template_name, "yaml")
            with open(f"{output_dir}{template_name}.yaml", "w") as f:
                f.write(yaml_config)
        
        # Create template index
        index = {
            "templates": {
                name: {
                    "name": template.name,
                    "model": template.model.value,
                    "scenario": template.scenario.value,
                    "description": template.description,
                    "features": template.additional_features
                }
                for name, template in self.templates.items()
            },
            "models": {model.value: model.name for model in RouterModel},
            "scenarios": {scenario.value: scenario.name for scenario in DeploymentScenario}
        }
        
        with open(f"{output_dir}template_index.json", "w") as f:
            json.dump(index, f, indent=2)


def main():
    """Test router templates"""
    templates = RouterConfigurationTemplates()
    
    print("🔧 Router Configuration Templates")
    print("=" * 50)
    print(f"Available Templates: {len(templates.list_templates())}")
    
    # List all templates
    for template_name in templates.list_templates():
        template = templates.get_template(template_name)
        print(f"\n📋 {template.name}")
        print(f"   Model: {template.model.value}")
        print(f"   Scenario: {template.scenario.value}")
        print(f"   VLANs: {len(template.network_config['vlans'])}")
        print(f"   Features: {', '.join(template.additional_features[:3])}...")
    
    # Export all templates
    templates.export_all_templates()
    print("\n✅ All templates exported to templates/ directory")
    
    # Generate example configuration
    config = templates.generate_router_config("manufacturing_floor_flint")
    print(f"\n🔧 Generated config for manufacturing floor:")
    print(f"   Hostname: {config['system']['hostname']}")
    print(f"   VLANs: {len(config['network']['vlans'])}")
    print(f"   WiFi Networks: {len(config['wireless']['networks'])}")
    print(f"   Firewall Rules: {len(config['firewall']['rules'])}")


if __name__ == "__main__":
    main()