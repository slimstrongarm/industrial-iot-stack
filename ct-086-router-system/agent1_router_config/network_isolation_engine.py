#!/usr/bin/env python3
"""
CT-086 Agent 1: Network Isolation Engine
Advanced VLAN and subnet isolation for industrial environments

This module provides sophisticated network segmentation and traffic control
for the Parachute Drop system router configuration.
"""

import json
import logging
import ipaddress
from typing import Dict, List, Optional, Set, Tuple, Any
from dataclasses import dataclass, asdict
from enum import Enum
import yaml


class SecurityLevel(Enum):
    """Network security levels"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    GUEST = "guest"


class ProtocolType(Enum):
    """Industrial protocol types"""
    MODBUS_TCP = "modbus_tcp"
    MODBUS_RTU = "modbus_rtu"
    OPC_UA = "opc_ua"
    ETHERNET_IP = "ethernet_ip"
    MQTT = "mqtt"
    HTTP = "http"
    HTTPS = "https"
    SSH = "ssh"
    SNMP = "snmp"
    DHCP = "dhcp"
    DNS = "dns"


@dataclass
class NetworkInterface:
    """Network interface configuration"""
    name: str
    vlan_id: int
    ip_address: str
    subnet_mask: str
    gateway: str
    description: str
    security_level: SecurityLevel
    enabled: bool = True


@dataclass
class FirewallRule:
    """Firewall rule configuration"""
    name: str
    source_zone: str
    dest_zone: str
    source_ip: str
    dest_ip: str
    protocol: str
    port: int
    action: str  # ACCEPT, DROP, REJECT
    description: str
    enabled: bool = True


@dataclass
class TrafficPolicy:
    """Traffic control policy"""
    name: str
    source_networks: List[str]
    dest_networks: List[str]
    allowed_protocols: List[ProtocolType]
    denied_protocols: List[ProtocolType]
    bandwidth_limit: Optional[int] = None  # In Mbps
    time_restrictions: Optional[Dict[str, str]] = None


class NetworkIsolationEngine:
    """
    Advanced network isolation engine for industrial environments
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.network_interfaces: Dict[str, NetworkInterface] = {}
        self.firewall_rules: List[FirewallRule] = []
        self.traffic_policies: List[TrafficPolicy] = []
        
        # Initialize default industrial network zones
        self._initialize_default_zones()
        self._initialize_default_policies()
    
    def _initialize_default_zones(self):
        """Initialize default network zones for industrial environments"""
        default_zones = [
            NetworkInterface(
                name="management",
                vlan_id=10,
                ip_address="192.168.10.1",
                subnet_mask="255.255.255.0",
                gateway="192.168.10.1",
                description="Network management and monitoring",
                security_level=SecurityLevel.CRITICAL
            ),
            NetworkInterface(
                name="control_network",
                vlan_id=20,
                ip_address="192.168.20.1",
                subnet_mask="255.255.255.0",
                gateway="192.168.20.1",
                description="PLC and control system network",
                security_level=SecurityLevel.CRITICAL
            ),
            NetworkInterface(
                name="hmi_network",
                vlan_id=21,
                ip_address="192.168.21.1",
                subnet_mask="255.255.255.0",
                gateway="192.168.21.1",
                description="HMI and operator interfaces",
                security_level=SecurityLevel.HIGH
            ),
            NetworkInterface(
                name="data_collection",
                vlan_id=30,
                ip_address="192.168.30.1",
                subnet_mask="255.255.255.0",
                gateway="192.168.30.1",
                description="Data historians and analytics",
                security_level=SecurityLevel.MEDIUM
            ),
            NetworkInterface(
                name="maintenance",
                vlan_id=40,
                ip_address="192.168.40.1",
                subnet_mask="255.255.255.0",
                gateway="192.168.40.1",
                description="Maintenance and diagnostics",
                security_level=SecurityLevel.MEDIUM
            ),
            NetworkInterface(
                name="guest_network",
                vlan_id=50,
                ip_address="192.168.50.1",
                subnet_mask="255.255.255.0",
                gateway="192.168.50.1",
                description="Guest and temporary access",
                security_level=SecurityLevel.GUEST
            )
        ]
        
        for zone in default_zones:
            self.network_interfaces[zone.name] = zone
    
    def _initialize_default_policies(self):
        """Initialize default traffic policies"""
        self.traffic_policies = [
            TrafficPolicy(
                name="management_full_access",
                source_networks=["192.168.10.0/24"],
                dest_networks=["0.0.0.0/0"],
                allowed_protocols=[p for p in ProtocolType],
                denied_protocols=[]
            ),
            TrafficPolicy(
                name="control_network_isolation",
                source_networks=["192.168.20.0/24"],
                dest_networks=["192.168.30.0/24"],  # Only to data collection
                allowed_protocols=[
                    ProtocolType.MODBUS_TCP,
                    ProtocolType.OPC_UA,
                    ProtocolType.ETHERNET_IP,
                    ProtocolType.MQTT
                ],
                denied_protocols=[
                    ProtocolType.HTTP,
                    ProtocolType.HTTPS
                ]
            ),
            TrafficPolicy(
                name="hmi_restricted_access",
                source_networks=["192.168.21.0/24"],
                dest_networks=["192.168.20.0/24", "192.168.30.0/24"],
                allowed_protocols=[
                    ProtocolType.OPC_UA,
                    ProtocolType.HTTPS,
                    ProtocolType.MQTT
                ],
                denied_protocols=[
                    ProtocolType.SSH,
                    ProtocolType.SNMP
                ]
            ),
            TrafficPolicy(
                name="guest_internet_only",
                source_networks=["192.168.50.0/24"],
                dest_networks=["0.0.0.0/0"],
                allowed_protocols=[
                    ProtocolType.HTTP,
                    ProtocolType.HTTPS,
                    ProtocolType.DNS,
                    ProtocolType.DHCP
                ],
                denied_protocols=[
                    ProtocolType.SSH,
                    ProtocolType.SNMP,
                    ProtocolType.MODBUS_TCP,
                    ProtocolType.OPC_UA
                ]
            )
        ]
    
    def add_network_interface(self, interface: NetworkInterface) -> bool:
        """Add a new network interface"""
        try:
            # Validate IP configuration
            ip_net = ipaddress.IPv4Network(f"{interface.ip_address}/{interface.subnet_mask}", strict=False)
            
            # Check for VLAN conflicts
            for existing_name, existing_interface in self.network_interfaces.items():
                if existing_interface.vlan_id == interface.vlan_id and existing_name != interface.name:
                    raise ValueError(f"VLAN ID {interface.vlan_id} already in use by {existing_name}")
            
            self.network_interfaces[interface.name] = interface
            self.logger.info(f"Added network interface: {interface.name} (VLAN {interface.vlan_id})")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to add network interface {interface.name}: {e}")
            return False
    
    def generate_firewall_rules(self) -> List[FirewallRule]:
        """Generate firewall rules based on traffic policies"""
        rules = []
        rule_id = 1
        
        # Default deny rule between VLANs
        rules.append(FirewallRule(
            name=f"rule_{rule_id:03d}_default_deny",
            source_zone="*",
            dest_zone="*",
            source_ip="0.0.0.0/0",
            dest_ip="0.0.0.0/0",
            protocol="all",
            port=0,
            action="DROP",
            description="Default deny between VLANs"
        ))
        rule_id += 1
        
        # Generate rules from policies
        for policy in self.traffic_policies:
            for src_net in policy.source_networks:
                for dest_net in policy.dest_networks:
                    for protocol in policy.allowed_protocols:
                        port = self._get_protocol_port(protocol)
                        
                        rules.append(FirewallRule(
                            name=f"rule_{rule_id:03d}_{policy.name}_{protocol.value}",
                            source_zone=self._get_zone_by_network(src_net),
                            dest_zone=self._get_zone_by_network(dest_net),
                            source_ip=src_net,
                            dest_ip=dest_net,
                            protocol=protocol.value,
                            port=port,
                            action="ACCEPT",
                            description=f"Allow {protocol.value} from {policy.name}"
                        ))
                        rule_id += 1
        
        # Add explicit deny rules for denied protocols
        for policy in self.traffic_policies:
            for src_net in policy.source_networks:
                for protocol in policy.denied_protocols:
                    port = self._get_protocol_port(protocol)
                    
                    rules.append(FirewallRule(
                        name=f"rule_{rule_id:03d}_{policy.name}_deny_{protocol.value}",
                        source_zone=self._get_zone_by_network(src_net),
                        dest_zone="*",
                        source_ip=src_net,
                        dest_ip="0.0.0.0/0",
                        protocol=protocol.value,
                        port=port,
                        action="DROP",
                        description=f"Deny {protocol.value} from {policy.name}"
                    ))
                    rule_id += 1
        
        self.firewall_rules = rules
        return rules
    
    def _get_protocol_port(self, protocol: ProtocolType) -> int:
        """Get default port for protocol"""
        port_map = {
            ProtocolType.MODBUS_TCP: 502,
            ProtocolType.OPC_UA: 4840,
            ProtocolType.ETHERNET_IP: 44818,
            ProtocolType.MQTT: 1883,
            ProtocolType.HTTP: 80,
            ProtocolType.HTTPS: 443,
            ProtocolType.SSH: 22,
            ProtocolType.SNMP: 161,
            ProtocolType.DHCP: 67,
            ProtocolType.DNS: 53
        }
        return port_map.get(protocol, 0)
    
    def _get_zone_by_network(self, network: str) -> str:
        """Get zone name by network address"""
        try:
            target_net = ipaddress.IPv4Network(network, strict=False)
            
            for zone_name, interface in self.network_interfaces.items():
                zone_net = ipaddress.IPv4Network(
                    f"{interface.ip_address}/{interface.subnet_mask}", 
                    strict=False
                )
                if target_net.subnet_of(zone_net) or target_net == zone_net:
                    return zone_name
            
            return "external"
            
        except:
            return "unknown"
    
    def validate_network_configuration(self) -> Dict[str, List[str]]:
        """Validate network configuration for security and conflicts"""
        issues = {
            "errors": [],
            "warnings": [],
            "recommendations": []
        }
        
        # Check for VLAN conflicts
        vlan_usage = {}
        for name, interface in self.network_interfaces.items():
            if interface.vlan_id in vlan_usage:
                issues["errors"].append(
                    f"VLAN {interface.vlan_id} used by both {name} and {vlan_usage[interface.vlan_id]}"
                )
            else:
                vlan_usage[interface.vlan_id] = name
        
        # Check for IP overlaps
        networks = []
        for name, interface in self.network_interfaces.items():
            try:
                net = ipaddress.IPv4Network(f"{interface.ip_address}/{interface.subnet_mask}", strict=False)
                for existing_net, existing_name in networks:
                    if net.overlaps(existing_net):
                        issues["errors"].append(
                            f"Network overlap between {name} and {existing_name}"
                        )
                networks.append((net, name))
            except:
                issues["errors"].append(f"Invalid IP configuration for {name}")
        
        # Security recommendations
        for name, interface in self.network_interfaces.items():
            if interface.security_level == SecurityLevel.CRITICAL:
                if not interface.name.startswith(('control', 'management')):
                    issues["warnings"].append(
                        f"Critical security level for non-control network: {name}"
                    )
        
        # Check isolation policies
        critical_zones = [name for name, iface in self.network_interfaces.items() 
                         if iface.security_level == SecurityLevel.CRITICAL]
        
        for policy in self.traffic_policies:
            for src_net in policy.source_networks:
                src_zone = self._get_zone_by_network(src_net)
                if src_zone in critical_zones:
                    if ProtocolType.HTTP in policy.allowed_protocols:
                        issues["warnings"].append(
                            f"HTTP allowed from critical zone in policy: {policy.name}"
                        )
        
        return issues
    
    def export_configuration(self, format_type: str = "json") -> str:
        """Export network configuration"""
        config_data = {
            "network_interfaces": {name: asdict(interface) 
                                 for name, interface in self.network_interfaces.items()},
            "firewall_rules": [asdict(rule) for rule in self.firewall_rules],
            "traffic_policies": [asdict(policy) for policy in self.traffic_policies],
            "validation_results": self.validate_network_configuration()
        }
        
        if format_type.lower() == "yaml":
            return yaml.dump(config_data, default_flow_style=False, indent=2)
        else:
            return json.dumps(config_data, indent=2, default=str)
    
    def generate_router_config(self) -> Dict[str, Any]:
        """Generate router-specific configuration"""
        # Generate firewall rules
        self.generate_firewall_rules()
        
        # Create router configuration
        router_config = {
            "system": {
                "hostname": "parachute-drop-router",
                "timezone": "UTC"
            },
            "network": {
                "interfaces": {}
            },
            "wireless": {
                "networks": []
            },
            "firewall": {
                "rules": [],
                "zones": []
            },
            "dhcp": {
                "pools": []
            }
        }
        
        # Add network interfaces
        for name, interface in self.network_interfaces.items():
            router_config["network"]["interfaces"][f"vlan{interface.vlan_id}"] = {
                "type": "bridge",
                "proto": "static",
                "ipaddr": interface.ip_address,
                "netmask": interface.subnet_mask,
                "description": interface.description,
                "enabled": interface.enabled
            }
            
            # Add WiFi network
            router_config["wireless"]["networks"].append({
                "ssid": f"ParachuteDrop-{name.title()}",
                "password": f"PDrop-{name[:3].upper()}-2025!",
                "encryption": "psk2",
                "network": f"vlan{interface.vlan_id}",
                "hidden": interface.security_level in [SecurityLevel.CRITICAL, SecurityLevel.HIGH]
            })
            
            # Add DHCP pool
            router_config["dhcp"]["pools"].append({
                "interface": f"vlan{interface.vlan_id}",
                "start": 10,
                "limit": 200,
                "leasetime": "12h"
            })
        
        # Add firewall rules
        for rule in self.firewall_rules:
            router_config["firewall"]["rules"].append({
                "name": rule.name,
                "src": rule.source_zone,
                "dest": rule.dest_zone,
                "src_ip": rule.source_ip,
                "dest_ip": rule.dest_ip,
                "proto": rule.protocol,
                "dest_port": str(rule.port) if rule.port > 0 else None,
                "target": rule.action,
                "enabled": rule.enabled
            })
        
        return router_config


def main():
    """Test network isolation engine"""
    engine = NetworkIsolationEngine()
    
    # Generate configuration
    config = engine.generate_router_config()
    
    # Validate configuration
    validation = engine.validate_network_configuration()
    
    print("🔧 Network Isolation Engine Configuration")
    print("=" * 50)
    print(f"Network Interfaces: {len(engine.network_interfaces)}")
    print(f"Firewall Rules: {len(engine.firewall_rules)}")
    print(f"Traffic Policies: {len(engine.traffic_policies)}")
    
    print("\n📋 Validation Results:")
    for category, issues in validation.items():
        if issues:
            print(f"  {category.title()}: {len(issues)}")
            for issue in issues[:3]:  # Show first 3
                print(f"    - {issue}")
    
    # Export configuration
    config_json = engine.export_configuration("json")
    with open("/home/server/industrial-iot-stack/ct-086-router-system/agent1_router_config/network_isolation_config.json", "w") as f:
        f.write(config_json)
    
    print("\n✅ Configuration exported to network_isolation_config.json")


if __name__ == "__main__":
    main()