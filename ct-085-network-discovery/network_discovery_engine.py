#!/usr/bin/env python3
"""
CT-085 Network Discovery Engine - Agent 1
Industrial network discovery system for Parachute Drop System

This module provides comprehensive network discovery capabilities for industrial automation systems,
including PLCs, MQTT brokers, Modbus devices, and OPC-UA servers with AI-powered device classification.
"""

import asyncio
import json
import logging
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Set
from concurrent.futures import ThreadPoolExecutor
import sqlite3
import ipaddress
from dataclasses import dataclass, asdict
import threading

from protocols.modbus_scanner import ModbusScanner
from protocols.opcua_scanner import OPCUAScanner
from protocols.mqtt_scanner import MQTTScanner
from protocols.ethernet_ip_scanner import EthernetIPScanner
from ai_classification.device_classifier import DeviceClassifier
from database.discovery_db import DiscoveryDatabase
from api.discovery_api import DiscoveryAPI

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/home/server/industrial-iot-stack/ct-085-network-discovery/logs/discovery.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class DiscoveredDevice:
    """Data class representing a discovered industrial device"""
    ip_address: str
    port: int
    protocol: str
    device_type: str
    manufacturer: str
    model: str
    firmware_version: str
    device_id: str
    confidence_score: float
    last_seen: datetime
    connection_status: str
    capabilities: List[str]
    security_level: str
    network_zone: str

@dataclass
class ScanConfiguration:
    """Configuration for network scanning parameters"""
    network_ranges: List[str]
    port_ranges: Dict[str, List[int]]
    scan_timeout: int
    max_concurrent_scans: int
    rate_limit_delay: float
    protocols_enabled: List[str]
    security_mode: str
    emergency_stop: bool

class NetworkDiscoveryEngine:
    """
    Main network discovery engine coordinating all protocol scanners
    and AI-powered device classification for industrial networks.
    """
    
    def __init__(self, config_path: str = None):
        """Initialize the discovery engine with configuration"""
        self.config = self._load_configuration(config_path)
        self.discovered_devices: Dict[str, DiscoveredDevice] = {}
        self.scanning_active = False
        self.emergency_stop = False
        self.scan_statistics = {
            'devices_discovered': 0,
            'scan_start_time': None,
            'scan_duration': 0,
            'protocols_scanned': [],
            'errors_encountered': 0
        }
        
        # Initialize components
        self.database = DiscoveryDatabase()
        self.device_classifier = DeviceClassifier()
        self.api_server = DiscoveryAPI(self)
        
        # Initialize protocol scanners
        self.scanners = {
            'modbus': ModbusScanner(self.config),
            'opcua': OPCUAScanner(self.config),
            'mqtt': MQTTScanner(self.config),
            'ethernet_ip': EthernetIPScanner(self.config)
        }
        
        # Thread pool for concurrent scanning
        self.executor = ThreadPoolExecutor(max_workers=self.config.max_concurrent_scans)
        
        logger.info("Network Discovery Engine initialized successfully")

    def _load_configuration(self, config_path: str) -> ScanConfiguration:
        """Load scanning configuration from JSON file"""
        default_config = {
            "network_ranges": ["192.168.1.0/24", "10.0.0.0/24"],
            "port_ranges": {
                "modbus": [502],
                "opcua": [4840, 48010],
                "mqtt": [1883, 8883],
                "ethernet_ip": [44818]
            },
            "scan_timeout": 30,
            "max_concurrent_scans": 10,
            "rate_limit_delay": 0.1,
            "protocols_enabled": ["modbus", "opcua", "mqtt", "ethernet_ip"],
            "security_mode": "passive",
            "emergency_stop": False
        }
        
        if config_path:
            try:
                with open(config_path, 'r') as f:
                    user_config = json.load(f)
                    default_config.update(user_config)
            except Exception as e:
                logger.warning(f"Could not load config from {config_path}: {e}")
        
        return ScanConfiguration(**default_config)

    async def discover_network(self, target_networks: List[str] = None) -> Dict[str, List[DiscoveredDevice]]:
        """
        Main discovery method that orchestrates network scanning across all protocols
        
        Args:
            target_networks: Optional list of network ranges to scan
            
        Returns:
            Dictionary organized by protocol containing discovered devices
        """
        if self.emergency_stop:
            logger.error("Discovery blocked - emergency stop active")
            return {}
            
        if self.scanning_active:
            logger.warning("Discovery already in progress")
            return self.get_discovered_devices()
            
        self.scanning_active = True
        self.scan_statistics['scan_start_time'] = datetime.now()
        self.scan_statistics['devices_discovered'] = 0
        self.scan_statistics['errors_encountered'] = 0
        
        logger.info("Starting comprehensive network discovery...")
        
        try:
            # Use provided networks or default from config
            networks = target_networks or self.config.network_ranges
            
            # Generate target IP addresses
            target_hosts = self._generate_target_hosts(networks)
            logger.info(f"Scanning {len(target_hosts)} potential hosts across {len(networks)} networks")
            
            # Scan each protocol concurrently
            scan_tasks = []
            for protocol in self.config.protocols_enabled:
                if protocol in self.scanners:
                    task = self._scan_protocol(protocol, target_hosts)
                    scan_tasks.append(task)
            
            # Execute all scans concurrently
            scan_results = await asyncio.gather(*scan_tasks, return_exceptions=True)
            
            # Process and classify discovered devices
            await self._process_scan_results(scan_results)
            
            # Update scan statistics
            self.scan_statistics['scan_duration'] = (datetime.now() - self.scan_statistics['scan_start_time']).total_seconds()
            self.scan_statistics['protocols_scanned'] = self.config.protocols_enabled
            
            logger.info(f"Discovery completed. Found {len(self.discovered_devices)} devices in {self.scan_statistics['scan_duration']:.2f} seconds")
            
            # Persist results to database
            await self._persist_discovery_results()
            
            return self.get_discovered_devices()
            
        except Exception as e:
            logger.error(f"Discovery failed: {e}")
            self.scan_statistics['errors_encountered'] += 1
            raise
        finally:
            self.scanning_active = False

    def _generate_target_hosts(self, networks: List[str]) -> List[str]:
        """Generate list of target IP addresses from network ranges"""
        target_hosts = []
        
        for network in networks:
            try:
                net = ipaddress.ip_network(network, strict=False)
                # Limit to first 254 hosts for large networks to prevent flooding
                host_count = min(254, net.num_addresses - 2)
                hosts = list(net.hosts())[:host_count]
                target_hosts.extend([str(host) for host in hosts])
                
            except Exception as e:
                logger.error(f"Invalid network range {network}: {e}")
                self.scan_statistics['errors_encountered'] += 1
                
        return target_hosts

    async def _scan_protocol(self, protocol: str, target_hosts: List[str]) -> Dict[str, List[DiscoveredDevice]]:
        """Scan a specific protocol across target hosts"""
        scanner = self.scanners[protocol]
        logger.info(f"Starting {protocol.upper()} protocol scan across {len(target_hosts)} hosts")
        
        discovered = []
        
        for host in target_hosts:
            if self.emergency_stop:
                logger.warning(f"{protocol.upper()} scan stopped - emergency stop activated")
                break
                
            try:
                # Rate limiting to prevent network flooding
                await asyncio.sleep(self.config.rate_limit_delay)
                
                # Scan this host for the current protocol
                device_info = await scanner.scan_host(host)
                
                if device_info:
                    # Apply AI classification
                    classified_device = await self._classify_device(device_info)
                    discovered.append(classified_device)
                    self.scan_statistics['devices_discovered'] += 1
                    
                    logger.info(f"Discovered {classified_device.manufacturer} {classified_device.model} at {host}")
                    
            except Exception as e:
                logger.debug(f"Error scanning {host} for {protocol}: {e}")
                
        logger.info(f"{protocol.upper()} scan completed. Found {len(discovered)} devices")
        return {protocol: discovered}

    async def _classify_device(self, device_info: Dict) -> DiscoveredDevice:
        """Apply AI classification to discovered device"""
        try:
            classification = await self.device_classifier.classify_device(device_info)
            
            device = DiscoveredDevice(
                ip_address=device_info['ip_address'],
                port=device_info['port'],
                protocol=device_info['protocol'],
                device_type=classification.get('device_type', 'Unknown'),
                manufacturer=classification.get('manufacturer', 'Unknown'),
                model=classification.get('model', 'Unknown'),
                firmware_version=device_info.get('firmware_version', 'Unknown'),
                device_id=device_info.get('device_id', f"{device_info['ip_address']}:{device_info['port']}"),
                confidence_score=classification.get('confidence_score', 0.0),
                last_seen=datetime.now(),
                connection_status='Active',
                capabilities=device_info.get('capabilities', []),
                security_level=self._assess_security_level(device_info),
                network_zone=self._determine_network_zone(device_info['ip_address'])
            )
            
            return device
            
        except Exception as e:
            logger.error(f"Device classification failed: {e}")
            raise

    def _assess_security_level(self, device_info: Dict) -> str:
        """Assess security level of discovered device"""
        # Simple security assessment based on protocol and capabilities
        protocol = device_info.get('protocol', '').lower()
        
        if protocol in ['opcua'] and device_info.get('security_enabled', False):
            return 'High'
        elif protocol in ['modbus', 'ethernet_ip']:
            return 'Medium'
        elif protocol == 'mqtt' and device_info.get('authentication_required', False):
            return 'Medium'
        else:
            return 'Low'

    def _determine_network_zone(self, ip_address: str) -> str:
        """Determine network security zone based on IP address"""
        try:
            ip = ipaddress.ip_address(ip_address)
            
            # Define common industrial network zones
            if ip in ipaddress.ip_network('192.168.1.0/24'):
                return 'Manufacturing'
            elif ip in ipaddress.ip_network('10.0.0.0/24'):
                return 'Process Control'
            elif ip in ipaddress.ip_network('172.16.0.0/16'):
                return 'Safety Systems'
            else:
                return 'General'
                
        except Exception:
            return 'Unknown'

    async def _process_scan_results(self, scan_results: List):
        """Process and merge scan results from all protocols"""
        for result in scan_results:
            if isinstance(result, Exception):
                logger.error(f"Scan error: {result}")
                self.scan_statistics['errors_encountered'] += 1
                continue
                
            if isinstance(result, dict):
                for protocol, devices in result.items():
                    for device in devices:
                        device_key = f"{device.ip_address}:{device.port}"
                        self.discovered_devices[device_key] = device

    async def _persist_discovery_results(self):
        """Persist discovery results to database"""
        try:
            for device in self.discovered_devices.values():
                await self.database.store_device(device)
            logger.info(f"Persisted {len(self.discovered_devices)} devices to database")
        except Exception as e:
            logger.error(f"Failed to persist results: {e}")

    def get_discovered_devices(self) -> Dict[str, List[DiscoveredDevice]]:
        """Get discovered devices organized by protocol"""
        devices_by_protocol = {}
        
        for device in self.discovered_devices.values():
            protocol = device.protocol
            if protocol not in devices_by_protocol:
                devices_by_protocol[protocol] = []
            devices_by_protocol[protocol].append(device)
            
        return devices_by_protocol

    def get_device_by_address(self, ip_address: str, port: int = None) -> Optional[DiscoveredDevice]:
        """Get specific device by IP address and optional port"""
        for device in self.discovered_devices.values():
            if device.ip_address == ip_address:
                if port is None or device.port == port:
                    return device
        return None

    def get_devices_by_manufacturer(self, manufacturer: str) -> List[DiscoveredDevice]:
        """Get all devices from specific manufacturer"""
        return [device for device in self.discovered_devices.values() 
                if device.manufacturer.lower() == manufacturer.lower()]

    def get_devices_by_protocol(self, protocol: str) -> List[DiscoveredDevice]:
        """Get all devices using specific protocol"""
        return [device for device in self.discovered_devices.values() 
                if device.protocol.lower() == protocol.lower()]

    def activate_emergency_stop(self):
        """Activate emergency stop to halt all scanning operations"""
        self.emergency_stop = True
        self.scanning_active = False
        logger.critical("EMERGENCY STOP ACTIVATED - All scanning operations halted")

    def deactivate_emergency_stop(self):
        """Deactivate emergency stop to resume normal operations"""
        self.emergency_stop = False
        logger.info("Emergency stop deactivated - Normal operations resumed")

    def get_scan_statistics(self) -> Dict:
        """Get current scan statistics"""
        return self.scan_statistics.copy()

    def export_discovery_data(self, format: str = 'json') -> str:
        """Export discovery data in specified format"""
        devices_data = []
        for device in self.discovered_devices.values():
            device_dict = asdict(device)
            device_dict['last_seen'] = device.last_seen.isoformat()
            devices_data.append(device_dict)
            
        if format.lower() == 'json':
            return json.dumps(devices_data, indent=2)
        else:
            raise ValueError(f"Unsupported export format: {format}")

    async def start_continuous_monitoring(self, interval_minutes: int = 15):
        """Start continuous monitoring mode with periodic rescans"""
        logger.info(f"Starting continuous monitoring with {interval_minutes} minute intervals")
        
        while not self.emergency_stop:
            try:
                await self.discover_network()
                await asyncio.sleep(interval_minutes * 60)
            except Exception as e:
                logger.error(f"Error in continuous monitoring: {e}")
                await asyncio.sleep(60)  # Wait 1 minute before retrying

    def start_api_server(self, host: str = '0.0.0.0', port: int = 8085):
        """Start REST API server for external integration"""
        self.api_server.start(host, port)

if __name__ == "__main__":
    # Example usage
    async def main():
        engine = NetworkDiscoveryEngine()
        
        try:
            # Start API server in background
            engine.start_api_server()
            
            # Perform initial discovery
            devices = await engine.discover_network()
            
            print(f"\nDiscovery completed! Found {sum(len(devs) for devs in devices.values())} devices:")
            for protocol, device_list in devices.items():
                print(f"\n{protocol.upper()} Devices ({len(device_list)}):")
                for device in device_list:
                    print(f"  - {device.manufacturer} {device.model} at {device.ip_address}:{device.port}")
            
            # Start continuous monitoring
            await engine.start_continuous_monitoring()
            
        except KeyboardInterrupt:
            logger.info("Discovery engine stopped by user")
        except Exception as e:
            logger.error(f"Discovery engine error: {e}")

    asyncio.run(main())