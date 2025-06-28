#!/usr/bin/env python3
"""
CT-084 Automatic Device Detection System
Advanced Industrial Device Detection with Pattern Recognition

Author: Claude Agent 1 - Edge Computing Specialist  
Version: 1.0.0
Project: CT-084 Parachute Drop System
"""

import json
import time
import asyncio
import logging
import socket
import struct
import subprocess
import threading
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple, Set
from dataclasses import dataclass, asdict
from enum import Enum
import uuid
import re

# Network scanning
import ipaddress
from concurrent.futures import ThreadPoolExecutor, as_completed

# USB device detection
try:
    import pyudev
    USB_DETECTION_AVAILABLE = True
except ImportError:
    USB_DETECTION_AVAILABLE = False
    logging.warning("pyudev not available - USB detection limited")

# Serial port detection  
try:
    import serial.tools.list_ports
    SERIAL_DETECTION_AVAILABLE = True
except ImportError:
    SERIAL_DETECTION_AVAILABLE = False
    logging.warning("pyserial not available - Serial detection disabled")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/var/log/ct084/device-detector.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('CT084-DeviceDetector')

class DeviceInterface(Enum):
    """Device interface types"""
    USB = "usb"
    SERIAL = "serial"
    ETHERNET = "ethernet"
    WIRELESS = "wireless"
    I2C = "i2c"
    SPI = "spi"
    MODBUS_RTU = "modbus_rtu"
    MODBUS_TCP = "modbus_tcp"
    OPCUA = "opcua"
    MQTT = "mqtt"
    UNKNOWN = "unknown"

class DeviceCategory(Enum):
    """Industrial device categories"""
    SENSOR_HUB = "sensor_hub"
    TEMPERATURE_SENSOR = "temperature_sensor"
    HUMIDITY_SENSOR = "humidity_sensor" 
    PRESSURE_SENSOR = "pressure_sensor"
    FLOW_SENSOR = "flow_sensor"
    LEVEL_SENSOR = "level_sensor"
    VIBRATION_SENSOR = "vibration_sensor"
    ELECTRICAL_METER = "electrical_meter"
    VALVE_ACTUATOR = "valve_actuator"
    MOTOR_DRIVE = "motor_drive"
    PLC = "plc"
    HMI = "hmi"
    GATEWAY = "gateway"
    NETWORK_SWITCH = "network_switch"
    POWER_SUPPLY = "power_supply"
    UNKNOWN = "unknown"

@dataclass
class DeviceSignature:
    """Device identification signature"""
    vendor_id: Optional[str] = None
    product_id: Optional[str] = None
    manufacturer: Optional[str] = None
    product_name: Optional[str] = None
    serial_number: Optional[str] = None
    mac_address: Optional[str] = None
    ip_address: Optional[str] = None
    port_responses: Dict[int, str] = None
    service_names: List[str] = None
    device_strings: List[str] = None
    
    def __post_init__(self):
        if self.port_responses is None:
            self.port_responses = {}
        if self.service_names is None:
            self.service_names = []
        if self.device_strings is None:
            self.device_strings = []

@dataclass
class DetectedDevice:
    """Detected device information"""
    device_id: str
    category: DeviceCategory
    interface: DeviceInterface
    name: str
    manufacturer: str
    model: str
    signature: DeviceSignature
    capabilities: List[str]
    location: str
    confidence: float
    detection_timestamp: datetime
    metadata: Dict[str, Any]
    
    def __post_init__(self):
        if self.capabilities is None:
            self.capabilities = []
        if self.metadata is None:
            self.metadata = {}

class DeviceDatabase:
    """Device signature database for pattern matching"""
    
    def __init__(self):
        self.device_patterns = self._load_device_patterns()
    
    def _load_device_patterns(self) -> Dict[str, Dict[str, Any]]:
        """Load device identification patterns"""
        return {
            # Phidgets devices
            "phidgets_hub": {
                "vendor_id": "06c2",
                "manufacturer": ["Phidgets Inc.", "phidgets"],
                "product_names": ["VINT Hub", "PhidgetHub"],
                "category": DeviceCategory.SENSOR_HUB,
                "interface": DeviceInterface.USB,
                "capabilities": ["vint_hub", "sensor_hub", "usb_device"],
                "confidence": 0.95
            },
            "phidgets_humidity": {
                "vendor_id": "06c2", 
                "manufacturer": ["Phidgets Inc.", "phidgets"],
                "product_names": ["Humidity", "HUM1001"],
                "category": DeviceCategory.HUMIDITY_SENSOR,
                "interface": DeviceInterface.USB,
                "capabilities": ["humidity_measurement", "vint_device"],
                "confidence": 0.90
            },
            "phidgets_temperature": {
                "vendor_id": "06c2",
                "manufacturer": ["Phidgets Inc.", "phidgets"], 
                "product_names": ["Temperature", "TMP1101", "Thermocouple"],
                "category": DeviceCategory.TEMPERATURE_SENSOR,
                "interface": DeviceInterface.USB,
                "capabilities": ["temperature_measurement", "vint_device"],
                "confidence": 0.90
            },
            
            # Industrial PLCs
            "allen_bradley_plc": {
                "manufacturer": ["Allen-Bradley", "Rockwell", "A-B"],
                "product_names": ["ControlLogix", "CompactLogix", "MicroLogix"],
                "port_responses": {44818: "EtherNet/IP"},
                "category": DeviceCategory.PLC,
                "interface": DeviceInterface.ETHERNET,
                "capabilities": ["ethernet_ip", "plc", "automation"],
                "confidence": 0.85
            },
            "siemens_plc": {
                "manufacturer": ["Siemens", "SIMATIC"],
                "product_names": ["S7-1200", "S7-1500", "S7-300", "S7-400"],
                "port_responses": {102: "ISO-TSAP"},
                "category": DeviceCategory.PLC,
                "interface": DeviceInterface.ETHERNET,
                "capabilities": ["profinet", "s7_comm", "plc"],
                "confidence": 0.85
            },
            
            # OPC-UA Servers
            "opcua_server": {
                "port_responses": {4840: "OPC-UA", 62541: "OPC-UA"},
                "service_names": ["opcua", "opc-ua"],
                "category": DeviceCategory.GATEWAY,
                "interface": DeviceInterface.ETHERNET,
                "capabilities": ["opcua_server", "data_access"],
                "confidence": 0.80
            },
            
            # MQTT Brokers
            "mqtt_broker": {
                "port_responses": {1883: "MQTT", 8883: "MQTT-TLS"},
                "service_names": ["mqtt", "mosquitto", "emqx"],
                "category": DeviceCategory.GATEWAY,
                "interface": DeviceInterface.ETHERNET,
                "capabilities": ["mqtt_broker", "pub_sub"],
                "confidence": 0.75
            },
            
            # Modbus devices
            "modbus_device": {
                "port_responses": {502: "Modbus-TCP"},
                "service_names": ["modbus"],
                "category": DeviceCategory.GATEWAY,
                "interface": DeviceInterface.ETHERNET,
                "capabilities": ["modbus_tcp", "industrial_protocol"],
                "confidence": 0.70
            },
            
            # Network infrastructure
            "cisco_switch": {
                "manufacturer": ["Cisco", "cisco"],
                "product_names": ["Catalyst", "Nexus"],
                "port_responses": {23: "telnet", 22: "ssh", 80: "http"},
                "category": DeviceCategory.NETWORK_SWITCH,
                "interface": DeviceInterface.ETHERNET,
                "capabilities": ["network_switch", "managed"],
                "confidence": 0.75
            },
            
            # Power supplies
            "phoenix_power": {
                "manufacturer": ["Phoenix Contact", "PHOENIX"],
                "product_names": ["QUINT", "STEP"],
                "category": DeviceCategory.POWER_SUPPLY,
                "interface": DeviceInterface.ETHERNET,
                "capabilities": ["power_supply", "din_rail"],
                "confidence": 0.70
            }
        }
    
    def match_device(self, signature: DeviceSignature) -> Tuple[Optional[str], float]:
        """Match device signature against database"""
        best_match = None
        best_confidence = 0.0
        
        for pattern_name, pattern in self.device_patterns.items():
            confidence = self._calculate_match_confidence(signature, pattern)
            
            if confidence > best_confidence:
                best_confidence = confidence
                best_match = pattern_name
        
        # Only return matches above minimum confidence threshold
        if best_confidence > 0.6:
            return best_match, best_confidence
        
        return None, 0.0
    
    def _calculate_match_confidence(self, signature: DeviceSignature, 
                                  pattern: Dict[str, Any]) -> float:
        """Calculate confidence score for device pattern match"""
        score = 0.0
        total_weight = 0.0
        
        # Vendor ID match (high weight)
        if pattern.get("vendor_id") and signature.vendor_id:
            total_weight += 3.0
            if pattern["vendor_id"].lower() == signature.vendor_id.lower():
                score += 3.0
        
        # Manufacturer match (high weight)
        if pattern.get("manufacturer") and signature.manufacturer:
            total_weight += 2.5
            for mfg in pattern["manufacturer"]:
                if mfg.lower() in signature.manufacturer.lower():
                    score += 2.5
                    break
        
        # Product name match (medium weight)
        if pattern.get("product_names") and signature.product_name:
            total_weight += 2.0
            for product in pattern["product_names"]:
                if product.lower() in signature.product_name.lower():
                    score += 2.0
                    break
        
        # Port response match (medium weight)
        if pattern.get("port_responses") and signature.port_responses:
            total_weight += 1.5
            for port, response in pattern["port_responses"].items():
                if port in signature.port_responses:
                    if response.lower() in signature.port_responses[port].lower():
                        score += 1.5
                        break
        
        # Service name match (low weight)
        if pattern.get("service_names") and signature.service_names:
            total_weight += 1.0
            for service in pattern["service_names"]:
                if service in signature.service_names:
                    score += 1.0
                    break
        
        # Calculate final confidence
        if total_weight > 0:
            confidence = score / total_weight
            return min(confidence, 1.0)
        
        return 0.0

class USBDeviceDetector:
    """USB device detection system"""
    
    def __init__(self):
        self.context = None
        if USB_DETECTION_AVAILABLE:
            self.context = pyudev.Context()
    
    async def detect_usb_devices(self) -> List[DeviceSignature]:
        """Detect USB devices and extract signatures"""
        signatures = []
        
        if not USB_DETECTION_AVAILABLE:
            logger.warning("USB detection not available")
            return signatures
        
        try:
            # Get USB devices
            for device in self.context.list_devices(subsystem='usb'):
                if device.device_type == 'usb_device':
                    signature = self._extract_usb_signature(device)
                    if signature:
                        signatures.append(signature)
            
            logger.info(f"Detected {len(signatures)} USB devices")
            
        except Exception as e:
            logger.error(f"USB detection failed: {e}")
        
        return signatures
    
    def _extract_usb_signature(self, device) -> Optional[DeviceSignature]:
        """Extract signature from USB device"""
        try:
            vendor_id = device.get('ID_VENDOR_ID')
            product_id = device.get('ID_MODEL_ID') 
            manufacturer = device.get('ID_VENDOR')
            product_name = device.get('ID_MODEL')
            serial = device.get('ID_SERIAL_SHORT')
            
            # Get additional device strings
            device_strings = []
            for attr in ['ID_VENDOR_FROM_DATABASE', 'ID_MODEL_FROM_DATABASE']:
                value = device.get(attr)
                if value:
                    device_strings.append(value)
            
            if vendor_id or manufacturer or product_name:
                return DeviceSignature(
                    vendor_id=vendor_id,
                    product_id=product_id,
                    manufacturer=manufacturer,
                    product_name=product_name,
                    serial_number=serial,
                    device_strings=device_strings
                )
        
        except Exception as e:
            logger.debug(f"Error extracting USB signature: {e}")
        
        return None

class SerialDeviceDetector:
    """Serial device detection system"""
    
    def __init__(self):
        pass
    
    async def detect_serial_devices(self) -> List[DeviceSignature]:
        """Detect serial devices and extract signatures"""
        signatures = []
        
        if not SERIAL_DETECTION_AVAILABLE:
            logger.warning("Serial detection not available")
            return signatures
        
        try:
            ports = serial.tools.list_ports.comports()
            
            for port in ports:
                signature = self._extract_serial_signature(port)
                if signature:
                    signatures.append(signature)
            
            logger.info(f"Detected {len(signatures)} serial devices")
            
        except Exception as e:
            logger.error(f"Serial detection failed: {e}")
        
        return signatures
    
    def _extract_serial_signature(self, port) -> Optional[DeviceSignature]:
        """Extract signature from serial port"""
        try:
            # Extract vendor/product IDs from hardware ID
            vendor_id = None
            product_id = None
            
            if hasattr(port, 'vid') and port.vid:
                vendor_id = f"{port.vid:04x}"
            if hasattr(port, 'pid') and port.pid:
                product_id = f"{port.pid:04x}"
            
            return DeviceSignature(
                vendor_id=vendor_id,
                product_id=product_id,
                manufacturer=port.manufacturer,
                product_name=port.product,
                serial_number=port.serial_number,
                device_strings=[port.description] if port.description else []
            )
        
        except Exception as e:
            logger.debug(f"Error extracting serial signature: {e}")
        
        return None

class NetworkDeviceDetector:
    """Network device detection system"""
    
    def __init__(self):
        self.common_ports = [
            22,    # SSH
            23,    # Telnet
            80,    # HTTP
            443,   # HTTPS
            502,   # Modbus TCP
            1883,  # MQTT
            4840,  # OPC-UA
            8883,  # MQTT TLS
            44818, # EtherNet/IP
            62541  # Ignition OPC-UA
        ]
    
    async def detect_network_devices(self, network_range: str = "192.168.1.0/24") -> List[DeviceSignature]:
        """Detect network devices and extract signatures"""
        signatures = []
        
        try:
            # Get network to scan
            network = ipaddress.IPv4Network(network_range, strict=False)
            
            # Scan hosts in parallel
            with ThreadPoolExecutor(max_workers=50) as executor:
                futures = {
                    executor.submit(self._scan_host, str(ip)): ip 
                    for ip in network.hosts()
                }
                
                for future in as_completed(futures):
                    ip = futures[future]
                    try:
                        signature = future.result(timeout=5)
                        if signature:
                            signatures.append(signature)
                    except Exception as e:
                        logger.debug(f"Error scanning {ip}: {e}")
            
            logger.info(f"Detected {len(signatures)} network devices")
            
        except Exception as e:
            logger.error(f"Network detection failed: {e}")
        
        return signatures
    
    def _scan_host(self, ip: str) -> Optional[DeviceSignature]:
        """Scan individual host for services"""
        try:
            # Check if host is reachable
            if not self._ping_host(ip):
                return None
            
            # Port scan
            port_responses = {}
            service_names = []
            
            for port in self.common_ports:
                response = self._test_port(ip, port)
                if response:
                    port_responses[port] = response
                    
                    # Identify known services
                    if port == 22:
                        service_names.append("ssh")
                    elif port == 23:
                        service_names.append("telnet")
                    elif port == 80:
                        service_names.append("http")
                    elif port == 443:
                        service_names.append("https")
                    elif port == 502:
                        service_names.append("modbus")
                    elif port == 1883:
                        service_names.append("mqtt")
                    elif port == 4840 or port == 62541:
                        service_names.append("opcua")
            
            if port_responses:
                # Try to get MAC address
                mac_address = self._get_mac_address(ip)
                
                return DeviceSignature(
                    ip_address=ip,
                    mac_address=mac_address,
                    port_responses=port_responses,
                    service_names=service_names
                )
        
        except Exception as e:
            logger.debug(f"Error scanning host {ip}: {e}")
        
        return None
    
    def _ping_host(self, ip: str) -> bool:
        """Check if host is reachable"""
        try:
            result = subprocess.run(
                ['ping', '-c', '1', '-W', '1', ip],
                capture_output=True,
                timeout=2
            )
            return result.returncode == 0
        except:
            return False
    
    def _test_port(self, ip: str, port: int) -> Optional[str]:
        """Test if port is open and get service info"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((ip, port))
            
            if result == 0:
                # Try to get banner
                try:
                    banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
                    sock.close()
                    return banner if banner else "open"
                except:
                    sock.close()
                    return "open"
            
            sock.close()
            return None
            
        except Exception as e:
            return None
    
    def _get_mac_address(self, ip: str) -> Optional[str]:
        """Get MAC address for IP using ARP"""
        try:
            result = subprocess.run(
                ['arp', '-n', ip],
                capture_output=True,
                text=True,
                timeout=2
            )
            
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                for line in lines:
                    if ip in line:
                        parts = line.split()
                        for part in parts:
                            if ':' in part and len(part) == 17:
                                return part
            
        except Exception as e:
            logger.debug(f"Error getting MAC for {ip}: {e}")
        
        return None

class CT084DeviceDetector:
    """Main CT-084 device detection system"""
    
    def __init__(self, config_file: str = "/etc/ct084/ct084-config.json"):
        self.config_file = Path(config_file)
        self.config = {}
        self.load_config()
        
        # Initialize components
        self.device_db = DeviceDatabase()
        self.usb_detector = USBDeviceDetector()
        self.serial_detector = SerialDeviceDetector()
        self.network_detector = NetworkDeviceDetector()
        
        # Detection results
        self.detected_devices = {}
        self.device_signatures = {}
    
    def load_config(self):
        """Load configuration"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r') as f:
                    self.config = json.load(f)
            else:
                self.config = {"detection": {"enabled": True}}
        except Exception as e:
            logger.error(f"Failed to load config: {e}")
            self.config = {"detection": {"enabled": True}}
    
    async def run_detection_cycle(self) -> Dict[str, DetectedDevice]:
        """Run complete device detection cycle"""
        logger.info("Starting CT-084 device detection cycle...")
        
        all_signatures = []
        
        # USB device detection
        try:
            usb_signatures = await self.usb_detector.detect_usb_devices()
            all_signatures.extend(usb_signatures)
        except Exception as e:
            logger.error(f"USB detection failed: {e}")
        
        # Serial device detection
        try:
            serial_signatures = await self.serial_detector.detect_serial_devices()
            all_signatures.extend(serial_signatures)
        except Exception as e:
            logger.error(f"Serial detection failed: {e}")
        
        # Network device detection
        try:
            network_signatures = await self.network_detector.detect_network_devices()
            all_signatures.extend(network_signatures)
        except Exception as e:
            logger.error(f"Network detection failed: {e}")
        
        # Process signatures and classify devices
        detected_devices = {}
        for signature in all_signatures:
            device = self._classify_device(signature)
            if device:
                detected_devices[device.device_id] = device
        
        self.detected_devices = detected_devices
        
        # Save detection results
        await self.save_detection_results()
        
        logger.info(f"Detection cycle completed - Found {len(detected_devices)} devices")
        return detected_devices
    
    def _classify_device(self, signature: DeviceSignature) -> Optional[DetectedDevice]:
        """Classify device based on signature"""
        try:
            # Match against device database
            pattern_name, confidence = self.device_db.match_device(signature)
            
            if pattern_name:
                pattern = self.device_db.device_patterns[pattern_name]
                
                # Generate device ID
                device_id = self._generate_device_id(signature, pattern_name)
                
                # Build device name
                name = self._build_device_name(signature, pattern)
                
                # Extract manufacturer and model
                manufacturer = signature.manufacturer or pattern.get("manufacturer", ["Unknown"])[0]
                model = signature.product_name or "Unknown Model"
                
                # Determine interface
                interface = pattern.get("interface", DeviceInterface.UNKNOWN)
                
                # Build location path
                location = self._build_location_path(signature, interface)
                
                # Build metadata
                metadata = {
                    "pattern_matched": pattern_name,
                    "signature": asdict(signature),
                    "detection_method": self._get_detection_method(signature),
                    "last_updated": datetime.now().isoformat()
                }
                
                return DetectedDevice(
                    device_id=device_id,
                    category=pattern["category"],
                    interface=interface,
                    name=name,
                    manufacturer=manufacturer,
                    model=model,
                    signature=signature,
                    capabilities=pattern.get("capabilities", []),
                    location=location,
                    confidence=confidence,
                    detection_timestamp=datetime.now(),
                    metadata=metadata
                )
        
        except Exception as e:
            logger.error(f"Error classifying device: {e}")
        
        return None
    
    def _generate_device_id(self, signature: DeviceSignature, pattern_name: str) -> str:
        """Generate unique device ID"""
        # Use serial number if available
        if signature.serial_number:
            return f"{pattern_name}_{signature.serial_number}"
        
        # Use vendor/product ID combination
        if signature.vendor_id and signature.product_id:
            return f"{pattern_name}_{signature.vendor_id}_{signature.product_id}"
        
        # Use IP address for network devices
        if signature.ip_address:
            return f"{pattern_name}_{signature.ip_address.replace('.', '_')}"
        
        # Use MAC address if available
        if signature.mac_address:
            return f"{pattern_name}_{signature.mac_address.replace(':', '_')}"
        
        # Generate random ID as fallback
        return f"{pattern_name}_{uuid.uuid4().hex[:8]}"
    
    def _build_device_name(self, signature: DeviceSignature, pattern: Dict[str, Any]) -> str:
        """Build human-readable device name"""
        # Use product name if available
        if signature.product_name:
            return signature.product_name
        
        # Use manufacturer + pattern name
        manufacturer = signature.manufacturer or pattern.get("manufacturer", ["Unknown"])[0]
        category = pattern["category"].value.replace('_', ' ').title()
        
        return f"{manufacturer} {category}"
    
    def _build_location_path(self, signature: DeviceSignature, interface: DeviceInterface) -> str:
        """Build UNS-compliant location path"""
        base_path = "CT084/ParachuteDrop/EdgeNode"
        
        if interface == DeviceInterface.USB:
            return f"{base_path}/USB"
        elif interface == DeviceInterface.SERIAL:
            return f"{base_path}/Serial"
        elif interface == DeviceInterface.ETHERNET:
            if signature.ip_address:
                return f"{base_path}/Network/{signature.ip_address}"
            return f"{base_path}/Network"
        else:
            return f"{base_path}/Unknown"
    
    def _get_detection_method(self, signature: DeviceSignature) -> str:
        """Determine detection method used"""
        if signature.vendor_id or signature.product_id:
            return "usb_enumeration"
        elif signature.ip_address:
            return "network_scan"
        elif signature.manufacturer and not signature.ip_address:
            return "serial_enumeration"
        else:
            return "unknown"
    
    async def save_detection_results(self):
        """Save detection results to file"""
        try:
            results = {
                "detection_timestamp": datetime.now().isoformat(),
                "detector_version": "1.0.0",
                "total_devices": len(self.detected_devices),
                "devices": {
                    device_id: asdict(device)
                    for device_id, device in self.detected_devices.items()
                },
                "summary": {
                    "categories": {},
                    "interfaces": {},
                    "manufacturers": {}
                }
            }
            
            # Build summary statistics
            for device in self.detected_devices.values():
                # Categories
                cat = device.category.value
                results["summary"]["categories"][cat] = results["summary"]["categories"].get(cat, 0) + 1
                
                # Interfaces
                iface = device.interface.value
                results["summary"]["interfaces"][iface] = results["summary"]["interfaces"].get(iface, 0) + 1
                
                # Manufacturers
                mfg = device.manufacturer
                results["summary"]["manufacturers"][mfg] = results["summary"]["manufacturers"].get(mfg, 0) + 1
            
            results_file = Path("/var/log/ct084/device-detection-results.json")
            results_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(results_file, 'w') as f:
                json.dump(results, f, indent=2, default=str)
            
            logger.info(f"Detection results saved to {results_file}")
            
        except Exception as e:
            logger.error(f"Failed to save detection results: {e}")

async def main():
    """Main entry point for device detector"""
    detector = CT084DeviceDetector()
    
    try:
        # Run detection cycle
        devices = await detector.run_detection_cycle()
        
        print(f"\nCT-084 Device Detection Results:")
        print(f"================================")
        print(f"Total devices detected: {len(devices)}")
        
        for device_id, device in devices.items():
            print(f"\nDevice: {device.name}")
            print(f"  ID: {device_id}")
            print(f"  Category: {device.category.value}")
            print(f"  Interface: {device.interface.value}")
            print(f"  Manufacturer: {device.manufacturer}")
            print(f"  Confidence: {device.confidence:.2f}")
            print(f"  Location: {device.location}")
            
    except KeyboardInterrupt:
        logger.info("Detection interrupted by user")
    except Exception as e:
        logger.error(f"Detection failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())