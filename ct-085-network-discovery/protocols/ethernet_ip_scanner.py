"""
EtherNet/IP Protocol Scanner
Discovers EtherNet/IP devices using CIP (Common Industrial Protocol)
Supports Allen-Bradley, Rockwell Automation, and other CIP-compatible devices
"""

import asyncio
import logging
import socket
import struct
from typing import Dict, Optional, List, Tuple
from dataclasses import dataclass
from enum import IntEnum

class CIPServiceCode(IntEnum):
    """CIP Service Codes"""
    GET_ATTRIBUTE_ALL = 0x01
    GET_ATTRIBUTE_SINGLE = 0x0E
    LIST_IDENTITY = 0x63
    LIST_SERVICES = 0x04

class CIPClass(IntEnum):
    """CIP Object Class Codes"""
    IDENTITY = 0x01
    MESSAGE_ROUTER = 0x02
    DEVICE_NET = 0x03
    ASSEMBLY = 0x04
    CONNECTION_MANAGER = 0x06

@dataclass
class EtherNetIPDevice:
    """EtherNet/IP device information"""
    vendor_id: Optional[int] = None
    device_type: Optional[int] = None
    product_code: Optional[int] = None
    revision: Optional[str] = None
    serial_number: Optional[int] = None
    product_name: Optional[str] = None
    state: Optional[int] = None
    ip_address: Optional[str] = None
    subnet_mask: Optional[str] = None
    gateway: Optional[str] = None
    name_server: Optional[str] = None
    domain_name: Optional[str] = None
    host_name: Optional[str] = None
    device_status: Optional[int] = None
    config_capability: Optional[int] = None
    config_control: Optional[int] = None

class EthernetIPScanner:
    """
    EtherNet/IP (CIP) protocol scanner for industrial device discovery
    Implements safe discovery using List Identity and List Services commands
    """
    
    def __init__(self):
        self.logger = logging.getLogger('EthernetIPScanner')
        self.default_ports = [44818, 2222]  # EtherNet/IP ports (TCP and UDP)
        self.timeout = 5.0
        
        # EtherNet/IP Encapsulation Commands
        self.EIP_CMD_NOP = 0x0000
        self.EIP_CMD_LIST_SERVICES = 0x0004
        self.EIP_CMD_LIST_IDENTITY = 0x0063
        self.EIP_CMD_LIST_INTERFACES = 0x0064
        self.EIP_CMD_REGISTER_SESSION = 0x0065
        self.EIP_CMD_UNREGISTER_SESSION = 0x0066
        self.EIP_CMD_SEND_RR_DATA = 0x006F
        self.EIP_CMD_SEND_UNIT_DATA = 0x0070
        
        # EtherNet/IP Status Codes
        self.EIP_STATUS_SUCCESS = 0x0000
        self.EIP_STATUS_INVALID_CMD = 0x0001
        self.EIP_STATUS_NO_MEMORY = 0x0002
        self.EIP_STATUS_INCORRECT_DATA = 0x0003
        self.EIP_STATUS_INVALID_SESSION = 0x0064
        self.EIP_STATUS_INVALID_LENGTH = 0x0065
        self.EIP_STATUS_UNSUPPORTED_PROTOCOL = 0x0069
        
        # Vendor ID mappings
        self.VENDOR_IDS = {
            1: "Rockwell Automation/Allen-Bradley",
            2: "Namco Controls",
            3: "Honeywell",
            4: "Parker Hannifin",
            5: "Rockwell Automation/Reliance Electric",
            6: "AMCI",
            7: "Hitachi America",
            8: "Furnas Electric",
            9: "Schneider Electric",
            10: "Omron",
            11: "Mitsubishi",
            12: "Oriental Motor",
            13: "A-B Quality",
            14: "Molex",
            15: "Yaskawa Electric",
            16: "Modicon",
            17: "AEG",
            18: "Siemens Energy & Automation",
            19: "ICS Triplex",
            20: "Kawasaki Robotics",
            21: "Kollmorgen",
            22: "API Motion",
            23: "Quicksilver Controls",
            24: "Bosch Rexroth",
            25: "Nachi Fujikoshi",
            26: "FANUC",
            27: "Eaton Corporation",
            28: "Apex Tool Group",
            29: "Hilscher",
            30: "Unico",
            31: "Infranor",
            32: "Camozzi",
            33: "S-S Technologies",
            34: "Sensor Partners",
            35: "Rotork",
            36: "WATLOW",
            37: "EUROTHERM",
            38: "Gems Sensors",
            39: "Rotork Instruments",
            40: "Loadstar Sensors",
            41: "Sensor Solutions Corp",
            42: "Bay Networks",
            43: "Cutler-Hammer",
            44: "Lantronix",
            45: "Phillips Petroleum",
            46: "Eaton E-NET",
            47: "Yokogawa",
            48: "Koyo Electronics",
            49: "Omron STI",
            50: "Trouble Shooting",
            51: "Weidmuller",
            52: "SST",
            53: "Northwire",
            54: "Woodhead",
            55: "Turck",
            56: "David Brown",
            57: "Barber Colman",
            58: "Schneider Electric",
            59: "Toshiba International",
            60: "Control Techniques",
            61: "Unidrive",
            62: "Numatics",
            63: "Bosch Rexroth",
            64: "Rexroth",
            65: "Eaton",
            66: "Vickers",
            67: "Eaton Hydraulics",
            68: "Hydraforce",
            69: "AMCI",
            70: "Eaton Electrical",
            71: "Wago",
            72: "Hilscher",
            73: "Jetter",
            74: "SSD Drives",
            75: "Lufkin",
            76: "Gefran",
            77: "IFM Electronic",
            78: "Leuze Electronic",
            79: "Datalogic",
            80: "Red Lion Controls",
            81: "SICK",
            82: "Stegmann",
            83: "Pepperl+Fuchs",
            84: "Balluff",
            85: "Banner Engineering",
            86: "Leuze Lumiflex",
            87: "Balluff Inc.",
            88: "Automation Direct",
            89: "Heidenhain",
            90: "Burr-Brown",
            91: "Moeller",
            92: "Tr-Electronic",
            93: "Weiss Klimatech",
            94: "Dunkermotoren",
            95: "Elau",
            96: "Kawasaki",
            97: "Kollmorgen",
            98: "Dunkermotoren GmbH",
            99: "Elau AG",
            100: "Rexroth Indramat",
            101: "AMK",
            102: "Kollmorgen Electro-Optical",
            103: "Nikon",
            104: "Autotrol",
            105: "Festo",
            106: "SMC",
            107: "Bimba",
            108: "Parker Hannifin",
            109: "Festo Corporation",
            110: "SMC Corporation",
            111: "Bimba Manufacturing",
            112: "Norgren",
            113: "Vickers",
            114: "Numatics",
            115: "Air Logic",
            116: "Camozzi",
            117: "Aventics",
            118: "Norgren Inc.",
            119: "Aro",
            120: "Camozzi Automation",
            121: "Metal Work",
            122: "Mindman",
            123: "Airtac",
            124: "Chelic",
            125: "Shako",
            126: "Ningbo Sanmin",
            127: "Aignep",
            128: "Camozzi USA",
            129: "Comatrol",
            130: "Wandfluh",
            131: "Atos",
            132: "Bosch Rexroth AG",
            133: "Hydac",
            134: "Hawe Hydraulik",
            135: "Parker Hannifin Corporation",
            136: "Eaton Corporation",
            137: "Danfoss",
            138: "Moog",
            139: "Bosch Rexroth Corporation",
            140: "Hydac Inc.",
            141: "Hawe Hydraulics",
            142: "Wandfluh AG",
            143: "Atos S.p.A.",
            144: "Comatrol",
            145: "Danfoss A/S",
            146: "Moog Inc.",
            147: "Sun Hydraulics"
        }
        
        # Device Type mappings
        self.DEVICE_TYPES = {
            0x00: "Generic Device",
            0x02: "AC Drive",
            0x03: "Motor Overload",
            0x04: "Limit Switch",
            0x05: "Inductive Proximity Switch",
            0x06: "Photoelectric Sensor",
            0x07: "General Purpose Discrete I/O",
            0x08: "Resolver",
            0x09: "General Purpose Analog I/O",
            0x0A: "Generic Rotating Shaft Encoder",
            0x0B: "General Purpose Encoder",
            0x0C: "Pneumatic Valve",
            0x0D: "Hydraulic Valve",
            0x0E: "Electric Valve",
            0x0F: "Analog Current Sensor",
            0x10: "Analog Voltage Sensor",
            0x11: "Pneumatic Pressure Switch",
            0x12: "Pneumatic Flow Switch",
            0x13: "Pneumatic Temperature Switch",
            0x14: "Vacuum Pressure Switch",
            0x15: "Process Control Sensor",
            0x16: "Process Control I/O",
            0x17: "Pneumatic Pressure Sensor",
            0x18: "Pneumatic Flow Sensor",
            0x19: "Pneumatic Temperature Sensor",
            0x1A: "Vacuum Pressure Sensor",
            0x1B: "Vacuum Flow Sensor",
            0x1C: "Pneumatic Pressure Switch",
            0x1D: "Pneumatic Flow Switch",
            0x1E: "Mass Flow Controller",
            0x1F: "Pneumatic Pressure Controller",
            0x20: "Pneumatic Flow Controller",
            0x21: "Pneumatic Temperature Controller",
            0x22: "Turbine Flow Meter",
            0x23: "Vortex Flow Meter",
            0x24: "Magnetic Flow Meter",
            0x25: "Ultrasonic Flow Meter",
            0x2A: "DC Drive",
            0x2B: "Contactor",
            0x2C: "Motor Starter",
            0x2D: "Soft Start",
            0x2E: "Human Machine Interface",
            0x32: "Pneumatic Valve",
            0x33: "Hydraulic Valve"
        }
    
    async def scan_device(self, ip_address: str, port: int = None) -> Optional[Dict]:
        """
        Scan for EtherNet/IP device on specified IP address
        
        Args:
            ip_address: Target IP address
            port: EtherNet/IP port (will try common ports if not specified)
            
        Returns:
            Dictionary with device information or None if not found
        """
        ports_to_scan = [port] if port else self.default_ports
        
        for scan_port in ports_to_scan:
            try:
                device_info = await self._discover_ethernet_ip_device(ip_address, scan_port)
                if device_info:
                    return {
                        'port': scan_port,
                        'device_type': self._get_device_type_name(device_info.device_type),
                        'manufacturer': self._get_vendor_name(device_info.vendor_id),
                        'model': device_info.product_name,
                        'firmware_version': device_info.revision,
                        'capabilities': self._get_device_capabilities(device_info),
                        'protocol_specific': {
                            'vendor_id': device_info.vendor_id,
                            'device_type_id': device_info.device_type,
                            'product_code': device_info.product_code,
                            'serial_number': device_info.serial_number,
                            'state': device_info.state,
                            'device_status': device_info.device_status,
                            'config_capability': device_info.config_capability,
                            'config_control': device_info.config_control,
                            'network_info': {
                                'ip_address': device_info.ip_address,
                                'subnet_mask': device_info.subnet_mask,
                                'gateway': device_info.gateway,
                                'name_server': device_info.name_server,
                                'domain_name': device_info.domain_name,
                                'host_name': device_info.host_name
                            }
                        }
                    }
            except Exception as e:
                self.logger.debug(f"EtherNet/IP scan failed for {ip_address}:{scan_port} - {e}")
        
        return None
    
    async def _discover_ethernet_ip_device(self, ip_address: str, port: int) -> Optional[EtherNetIPDevice]:
        """Discover EtherNet/IP device using List Identity command"""
        try:
            # First check if port is open
            if not await self._check_port_open(ip_address, port):
                return None
            
            # Try List Identity command
            device_info = await self._send_list_identity(ip_address, port)
            
            if device_info:
                # Try to get additional information
                await self._get_additional_device_info(ip_address, port, device_info)
            
            return device_info
            
        except Exception as e:
            self.logger.debug(f"EtherNet/IP discovery failed for {ip_address}:{port}: {e}")
            return None
    
    async def _check_port_open(self, ip_address: str, port: int) -> bool:
        """Check if EtherNet/IP port is open"""
        try:
            future = asyncio.open_connection(ip_address, port)
            reader, writer = await asyncio.wait_for(future, timeout=self.timeout)
            writer.close()
            await writer.wait_closed()
            return True
        except:
            return False
    
    async def _send_list_identity(self, ip_address: str, port: int) -> Optional[EtherNetIPDevice]:
        """Send List Identity command to EtherNet/IP device"""
        try:
            # Connect to device
            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(ip_address, port),
                timeout=self.timeout
            )
            
            try:
                # Build List Identity request
                request = self._build_list_identity_request()
                
                writer.write(request)
                await writer.drain()
                
                # Read response
                response = await asyncio.wait_for(reader.read(1024), timeout=self.timeout)
                
                if len(response) < 24:  # Minimum EtherNet/IP header size
                    return None
                
                # Parse response
                device_info = self._parse_list_identity_response(response)
                
                return device_info
                
            finally:
                writer.close()
                await writer.wait_closed()
                
        except Exception as e:
            self.logger.debug(f"List Identity command failed: {e}")
            return None
    
    def _build_list_identity_request(self) -> bytes:
        """Build EtherNet/IP List Identity request"""
        # EtherNet/IP Encapsulation Header
        # Command (2 bytes) + Length (2 bytes) + Session Handle (4 bytes) + 
        # Status (4 bytes) + Sender Context (8 bytes) + Options (4 bytes)
        
        command = self.EIP_CMD_LIST_IDENTITY
        length = 0  # No data for List Identity
        session_handle = 0x00000000
        status = 0x00000000
        sender_context = b'\x00\x00\x00\x00\x00\x00\x00\x00'
        options = 0x00000000
        
        request = struct.pack('<HHII8sI',
            command,
            length,
            session_handle,
            status,
            sender_context,
            options
        )
        
        return request
    
    def _parse_list_identity_response(self, response: bytes) -> Optional[EtherNetIPDevice]:
        """Parse List Identity response"""
        try:
            if len(response) < 24:
                return None
            
            # Parse encapsulation header
            command, length, session_handle, status = struct.unpack('<HHII', response[:12])
            
            if command != self.EIP_CMD_LIST_IDENTITY or status != self.EIP_STATUS_SUCCESS:
                return None
            
            if length == 0:  # No identity data
                return None
            
            # Skip sender context and options
            offset = 24
            
            if len(response) < offset + 2:
                return None
            
            # Parse item count
            item_count = struct.unpack('<H', response[offset:offset + 2])[0]
            offset += 2
            
            if item_count == 0:
                return None
            
            # Parse first item (should be identity item)
            if len(response) < offset + 4:
                return None
            
            item_type_code, item_length = struct.unpack('<HH', response[offset:offset + 4])
            offset += 4
            
            if item_type_code != 0x000C:  # Identity Item Type Code
                return None
            
            if len(response) < offset + item_length:
                return None
            
            # Parse identity data
            identity_data = response[offset:offset + item_length]
            device_info = self._parse_identity_data(identity_data)
            
            return device_info
            
        except Exception as e:
            self.logger.debug(f"Error parsing List Identity response: {e}")
            return None
    
    def _parse_identity_data(self, data: bytes) -> EtherNetIPDevice:
        """Parse identity data from List Identity response"""
        device_info = EtherNetIPDevice()
        
        try:
            if len(data) < 24:  # Minimum identity data size
                return device_info
            
            # Parse fixed portion of identity data
            protocol_version, sin_family, sin_port, sin_addr, sin_zero = struct.unpack('<HHH4s8s', data[:20])
            
            # Extract IP address
            device_info.ip_address = '.'.join(str(b) for b in sin_addr)
            
            offset = 20
            
            if len(data) < offset + 24:
                return device_info
            
            # Parse device identity
            vendor_id, device_type, product_code, revision_major, revision_minor, \
            status, serial_number, product_name_length = struct.unpack('<HHHHBBIH', data[offset:offset + 16])
            
            device_info.vendor_id = vendor_id
            device_info.device_type = device_type
            device_info.product_code = product_code
            device_info.revision = f"{revision_major}.{revision_minor}"
            device_info.state = status
            device_info.serial_number = serial_number
            
            offset += 16
            
            # Parse product name
            if len(data) >= offset + product_name_length:
                product_name = data[offset:offset + product_name_length].decode('utf-8', errors='ignore')
                device_info.product_name = product_name
                offset += product_name_length
            
            # Parse state (if available)
            if len(data) >= offset + 1:
                device_info.device_status = data[offset]
                
        except Exception as e:
            self.logger.debug(f"Error parsing identity data: {e}")
        
        return device_info
    
    async def _get_additional_device_info(self, ip_address: str, port: int, device_info: EtherNetIPDevice):
        """Get additional device information using other CIP services"""
        try:
            # This would typically involve registering a session and sending
            # additional CIP requests, but for simplicity we'll skip this
            # in the basic implementation
            pass
        except Exception as e:
            self.logger.debug(f"Failed to get additional device info: {e}")
    
    def _get_vendor_name(self, vendor_id: int) -> str:
        """Get vendor name from vendor ID"""
        return self.VENDOR_IDS.get(vendor_id, f"Unknown Vendor (ID: {vendor_id})")
    
    def _get_device_type_name(self, device_type: int) -> str:
        """Get device type name from device type ID"""
        return self.DEVICE_TYPES.get(device_type, f"Unknown Device Type (ID: {device_type})")
    
    def _get_device_capabilities(self, device_info: EtherNetIPDevice) -> List[str]:
        """Get device capabilities based on device information"""
        capabilities = ['ethernet_ip', 'cip_protocol', 'industrial_automation']
        
        # Add vendor-specific capabilities
        if device_info.vendor_id == 1:  # Rockwell Automation
            capabilities.extend(['allen_bradley_compatible', 'rslogix_compatible'])
        elif device_info.vendor_id == 9:  # Schneider Electric
            capabilities.extend(['modicon_compatible', 'unity_pro_compatible'])
        elif device_info.vendor_id == 18:  # Siemens
            capabilities.extend(['siemens_compatible', 'step7_compatible'])
        elif device_info.vendor_id == 10:  # Omron
            capabilities.extend(['omron_compatible', 'cx_programmer_compatible'])
        
        # Add device type specific capabilities
        if device_info.device_type in [0x02, 0x2A]:  # AC Drive, DC Drive
            capabilities.extend(['variable_frequency_drive', 'motor_control'])
        elif device_info.device_type in [0x07, 0x09]:  # Discrete I/O, Analog I/O
            capabilities.extend(['digital_io', 'process_control'])
        elif device_info.device_type == 0x2E:  # HMI
            capabilities.extend(['human_machine_interface', 'operator_interface'])
        elif device_info.device_type in [0x0C, 0x0D, 0x0E]:  # Valves
            capabilities.extend(['valve_control', 'pneumatic_hydraulic'])
        
        # Add network capabilities
        capabilities.append('tcp_ip_networking')
        
        if device_info.config_capability:
            capabilities.append('remote_configuration')
        
        return capabilities
    
    async def check_device_status(self, ip_address: str, port: int = None) -> bool:
        """Check if EtherNet/IP device is still online"""
        ports_to_check = [port] if port else [44818]  # Default port
        
        for check_port in ports_to_check:
            try:
                future = asyncio.open_connection(ip_address, check_port)
                reader, writer = await asyncio.wait_for(future, timeout=2.0)
                writer.close()
                await writer.wait_closed()
                return True
            except:
                continue
        
        return False
    
    def get_common_ethernet_ip_ports(self) -> List[int]:
        """Get list of common EtherNet/IP ports"""
        return self.default_ports