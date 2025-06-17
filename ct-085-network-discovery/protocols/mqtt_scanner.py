"""
MQTT Protocol Scanner
Discovers MQTT brokers in industrial IoT networks
"""

import asyncio
import logging
import socket
import struct
import json
from typing import Dict, Optional, List, Tuple
from dataclasses import dataclass
from enum import IntEnum

class MQTTMessageType(IntEnum):
    """MQTT message types"""
    CONNECT = 1
    CONNACK = 2
    PUBLISH = 3
    PUBACK = 4
    PUBREC = 5
    PUBREL = 6
    PUBCOMP = 7
    SUBSCRIBE = 8
    SUBACK = 9
    UNSUBSCRIBE = 10
    UNSUBACK = 11
    PINGREQ = 12
    PINGRESP = 13
    DISCONNECT = 14

@dataclass
class MQTTBrokerInfo:
    """Information about discovered MQTT broker"""
    broker_version: Optional[str] = None
    max_keepalive: Optional[int] = None
    session_present: bool = False
    return_code: int = 0
    server_keep_alive: Optional[int] = None
    assigned_client_identifier: Optional[str] = None
    maximum_packet_size: Optional[int] = None
    topic_alias_maximum: Optional[int] = None
    reason_string: Optional[str] = None
    wildcard_subscription_available: bool = True
    subscription_identifier_available: bool = True
    shared_subscription_available: bool = True
    server_reference: Optional[str] = None
    authentication_method: Optional[str] = None
    supports_retained_messages: bool = True
    max_qos: int = 2
    receive_maximum: Optional[int] = None

class MQTTScanner:
    """
    MQTT protocol scanner for broker discovery in IoT networks
    Implements safe discovery using CONNECT/CONNACK handshake
    """
    
    def __init__(self):
        self.logger = logging.getLogger('MQTTScanner')
        self.default_ports = [1883, 8883, 1884, 8884, 9001, 9883]  # Common MQTT ports
        self.timeout = 5.0
        
        # MQTT protocol constants
        self.MQTT_PROTOCOL_NAME_V3 = b"MQIsdp"
        self.MQTT_PROTOCOL_NAME_V311 = b"MQTT"
        self.MQTT_PROTOCOL_VERSION_V3 = 3
        self.MQTT_PROTOCOL_VERSION_V311 = 4
        self.MQTT_PROTOCOL_VERSION_V5 = 5
        
        # Connection return codes
        self.CONNACK_CODES = {
            0: "Connection Accepted",
            1: "Connection Refused - Unacceptable Protocol Version",
            2: "Connection Refused - Identifier Rejected",
            3: "Connection Refused - Server Unavailable",
            4: "Connection Refused - Bad User Name or Password",
            5: "Connection Refused - Not Authorized"
        }
    
    async def scan_device(self, ip_address: str, port: int = None) -> Optional[Dict]:
        """
        Scan for MQTT broker on specified IP address
        
        Args:
            ip_address: Target IP address
            port: MQTT port (will try common ports if not specified)
            
        Returns:
            Dictionary with broker information or None if not found
        """
        ports_to_scan = [port] if port else self.default_ports
        
        for scan_port in ports_to_scan:
            try:
                broker_info = await self._discover_mqtt_broker(ip_address, scan_port)
                if broker_info:
                    return {
                        'port': scan_port,
                        'device_type': 'MQTT Broker',
                        'manufacturer': self._identify_broker_manufacturer(broker_info, ip_address),
                        'model': self._identify_broker_model(broker_info),
                        'firmware_version': broker_info.broker_version,
                        'capabilities': self._get_broker_capabilities(broker_info, scan_port),
                        'protocol_specific': {
                            'return_code': broker_info.return_code,
                            'return_code_description': self.CONNACK_CODES.get(broker_info.return_code, "Unknown"),
                            'session_present': broker_info.session_present,
                            'max_keepalive': broker_info.max_keepalive,
                            'server_keep_alive': broker_info.server_keep_alive,
                            'max_qos': broker_info.max_qos,
                            'supports_retained_messages': broker_info.supports_retained_messages,
                            'wildcard_subscription_available': broker_info.wildcard_subscription_available,
                            'subscription_identifier_available': broker_info.subscription_identifier_available,
                            'shared_subscription_available': broker_info.shared_subscription_available,
                            'maximum_packet_size': broker_info.maximum_packet_size,
                            'topic_alias_maximum': broker_info.topic_alias_maximum,
                            'receive_maximum': broker_info.receive_maximum,
                            'assigned_client_identifier': broker_info.assigned_client_identifier,
                            'server_reference': broker_info.server_reference,
                            'authentication_method': broker_info.authentication_method,
                            'reason_string': broker_info.reason_string
                        }
                    }
            except Exception as e:
                self.logger.debug(f"MQTT scan failed for {ip_address}:{scan_port} - {e}")
        
        return None
    
    async def _discover_mqtt_broker(self, ip_address: str, port: int) -> Optional[MQTTBrokerInfo]:
        """Discover MQTT broker using CONNECT/CONNACK handshake"""
        try:
            # First check if port is open
            if not await self._check_port_open(ip_address, port):
                return None
            
            # Try different MQTT protocol versions
            for protocol_version in [self.MQTT_PROTOCOL_VERSION_V5, 
                                   self.MQTT_PROTOCOL_VERSION_V311, 
                                   self.MQTT_PROTOCOL_VERSION_V3]:
                
                broker_info = await self._test_mqtt_connection(ip_address, port, protocol_version)
                if broker_info and broker_info.return_code == 0:
                    return broker_info
            
            return None
            
        except Exception as e:
            self.logger.debug(f"MQTT discovery failed for {ip_address}:{port}: {e}")
            return None
    
    async def _check_port_open(self, ip_address: str, port: int) -> bool:
        """Check if MQTT port is open"""
        try:
            future = asyncio.open_connection(ip_address, port)
            reader, writer = await asyncio.wait_for(future, timeout=self.timeout)
            writer.close()
            await writer.wait_closed()
            return True
        except:
            return False
    
    async def _test_mqtt_connection(self, ip_address: str, port: int, protocol_version: int) -> Optional[MQTTBrokerInfo]:
        """Test MQTT connection with specific protocol version"""
        try:
            # Connect to broker
            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(ip_address, port),
                timeout=self.timeout
            )
            
            try:
                # Send CONNECT packet
                connect_packet = self._build_connect_packet(protocol_version, f"scanner_{ip_address.replace('.', '_')}")
                writer.write(connect_packet)
                await writer.drain()
                
                # Read CONNACK response
                response = await asyncio.wait_for(reader.read(1024), timeout=self.timeout)
                
                if len(response) < 4:
                    return None
                
                # Parse CONNACK
                broker_info = self._parse_connack_response(response, protocol_version)
                
                # Send DISCONNECT to be polite
                disconnect_packet = self._build_disconnect_packet(protocol_version)
                writer.write(disconnect_packet)
                await writer.drain()
                
                return broker_info
                
            finally:
                writer.close()
                await writer.wait_closed()
                
        except Exception as e:
            self.logger.debug(f"MQTT connection test failed: {e}")
            return None
    
    def _build_connect_packet(self, protocol_version: int, client_id: str) -> bytes:
        """Build MQTT CONNECT packet"""
        # Variable header
        if protocol_version == self.MQTT_PROTOCOL_VERSION_V5:
            protocol_name = self.MQTT_PROTOCOL_NAME_V311
        elif protocol_version == self.MQTT_PROTOCOL_VERSION_V311:
            protocol_name = self.MQTT_PROTOCOL_NAME_V311
        else:  # V3
            protocol_name = self.MQTT_PROTOCOL_NAME_V3
        
        # Protocol name length + protocol name + protocol version
        variable_header = struct.pack('>H', len(protocol_name)) + protocol_name + struct.pack('>B', protocol_version)
        
        # Connect flags: Clean Session = 1, others = 0
        connect_flags = 0x02  # Clean Session
        variable_header += struct.pack('>B', connect_flags)
        
        # Keep Alive (60 seconds)
        keep_alive = 60
        variable_header += struct.pack('>H', keep_alive)
        
        # Properties (MQTT v5 only)
        properties = b''
        if protocol_version == self.MQTT_PROTOCOL_VERSION_V5:
            properties = struct.pack('>B', 0)  # Property Length = 0
            variable_header += properties
        
        # Payload: Client ID
        client_id_bytes = client_id.encode('utf-8')
        payload = struct.pack('>H', len(client_id_bytes)) + client_id_bytes
        
        # Calculate remaining length
        remaining_length = len(variable_header) + len(payload)
        
        # Fixed header: Message Type (CONNECT = 1) + Flags (0) + Remaining Length
        fixed_header = struct.pack('>B', (MQTTMessageType.CONNECT << 4)) + self._encode_remaining_length(remaining_length)
        
        return fixed_header + variable_header + payload
    
    def _build_disconnect_packet(self, protocol_version: int) -> bytes:
        """Build MQTT DISCONNECT packet"""
        if protocol_version == self.MQTT_PROTOCOL_VERSION_V5:
            # MQTT v5 DISCONNECT with reason code 0 (Normal disconnection)
            fixed_header = struct.pack('>B', (MQTTMessageType.DISCONNECT << 4))
            remaining_length = 2  # Reason code + property length
            fixed_header += self._encode_remaining_length(remaining_length)
            variable_header = struct.pack('>BB', 0, 0)  # Reason code 0, property length 0
            return fixed_header + variable_header
        else:
            # MQTT v3/v3.1.1 DISCONNECT (no variable header/payload)
            fixed_header = struct.pack('>B', (MQTTMessageType.DISCONNECT << 4))
            remaining_length = 0
            fixed_header += self._encode_remaining_length(remaining_length)
            return fixed_header
    
    def _encode_remaining_length(self, length: int) -> bytes:
        """Encode remaining length using MQTT variable length encoding"""
        encoded = bytearray()
        while length > 0:
            byte = length % 128
            length = length // 128
            if length > 0:
                byte |= 0x80
            encoded.append(byte)
        return bytes(encoded) if encoded else b'\x00'
    
    def _parse_connack_response(self, response: bytes, protocol_version: int) -> MQTTBrokerInfo:
        """Parse CONNACK response packet"""
        broker_info = MQTTBrokerInfo()
        
        try:
            # Check message type
            if len(response) < 2:
                return broker_info
            
            message_type = (response[0] & 0xF0) >> 4
            if message_type != MQTTMessageType.CONNACK:
                return broker_info
            
            # Decode remaining length
            remaining_length, offset = self._decode_remaining_length(response[1:])
            offset += 1  # Adjust for fixed header
            
            if len(response) < offset + 2:
                return broker_info
            
            # Parse variable header
            if protocol_version == self.MQTT_PROTOCOL_VERSION_V5:
                # MQTT v5 CONNACK
                connect_acknowledge_flags = response[offset]
                broker_info.session_present = (connect_acknowledge_flags & 0x01) != 0
                
                reason_code = response[offset + 1]
                broker_info.return_code = reason_code
                
                offset += 2
                
                # Properties
                if offset < len(response):
                    properties_length, prop_offset = self._decode_remaining_length(response[offset:])
                    offset += prop_offset
                    
                    # Parse properties
                    self._parse_mqtt5_properties(response[offset:offset + properties_length], broker_info)
                    
            else:
                # MQTT v3/v3.1.1 CONNACK
                connect_acknowledge_flags = response[offset]
                broker_info.session_present = (connect_acknowledge_flags & 0x01) != 0
                
                return_code = response[offset + 1]
                broker_info.return_code = return_code
        
        except Exception as e:
            self.logger.debug(f"Error parsing CONNACK: {e}")
        
        return broker_info
    
    def _decode_remaining_length(self, data: bytes) -> Tuple[int, int]:
        """Decode MQTT variable length encoding"""
        length = 0
        multiplier = 1
        offset = 0
        
        while offset < len(data):
            byte = data[offset]
            length += (byte & 0x7F) * multiplier
            offset += 1
            
            if (byte & 0x80) == 0:
                break
                
            multiplier *= 128
            if multiplier > 128 * 128 * 128:
                break
        
        return length, offset
    
    def _parse_mqtt5_properties(self, properties_data: bytes, broker_info: MQTTBrokerInfo):
        """Parse MQTT v5 properties"""
        try:
            offset = 0
            while offset < len(properties_data):
                if offset >= len(properties_data):
                    break
                
                property_id = properties_data[offset]
                offset += 1
                
                # Parse based on property ID
                if property_id == 0x11:  # Session Expiry Interval
                    if offset + 4 <= len(properties_data):
                        broker_info.max_keepalive = struct.unpack('>I', properties_data[offset:offset + 4])[0]
                        offset += 4
                elif property_id == 0x13:  # Server Keep Alive
                    if offset + 2 <= len(properties_data):
                        broker_info.server_keep_alive = struct.unpack('>H', properties_data[offset:offset + 2])[0]
                        offset += 2
                elif property_id == 0x12:  # Assigned Client Identifier
                    if offset + 2 <= len(properties_data):
                        str_len = struct.unpack('>H', properties_data[offset:offset + 2])[0]
                        offset += 2
                        if offset + str_len <= len(properties_data):
                            broker_info.assigned_client_identifier = properties_data[offset:offset + str_len].decode('utf-8')
                            offset += str_len
                elif property_id == 0x27:  # Maximum Packet Size
                    if offset + 4 <= len(properties_data):
                        broker_info.maximum_packet_size = struct.unpack('>I', properties_data[offset:offset + 4])[0]
                        offset += 4
                elif property_id == 0x22:  # Topic Alias Maximum
                    if offset + 2 <= len(properties_data):
                        broker_info.topic_alias_maximum = struct.unpack('>H', properties_data[offset:offset + 2])[0]
                        offset += 2
                elif property_id == 0x1F:  # Reason String
                    if offset + 2 <= len(properties_data):
                        str_len = struct.unpack('>H', properties_data[offset:offset + 2])[0]
                        offset += 2
                        if offset + str_len <= len(properties_data):
                            broker_info.reason_string = properties_data[offset:offset + str_len].decode('utf-8')
                            offset += str_len
                elif property_id == 0x28:  # Wildcard Subscription Available
                    if offset + 1 <= len(properties_data):
                        broker_info.wildcard_subscription_available = properties_data[offset] != 0
                        offset += 1
                elif property_id == 0x29:  # Subscription Identifier Available
                    if offset + 1 <= len(properties_data):
                        broker_info.subscription_identifier_available = properties_data[offset] != 0
                        offset += 1
                elif property_id == 0x2A:  # Shared Subscription Available
                    if offset + 1 <= len(properties_data):
                        broker_info.shared_subscription_available = properties_data[offset] != 0
                        offset += 1
                elif property_id == 0x1C:  # Server Reference
                    if offset + 2 <= len(properties_data):
                        str_len = struct.unpack('>H', properties_data[offset:offset + 2])[0]
                        offset += 2
                        if offset + str_len <= len(properties_data):
                            broker_info.server_reference = properties_data[offset:offset + str_len].decode('utf-8')
                            offset += str_len
                elif property_id == 0x15:  # Authentication Method
                    if offset + 2 <= len(properties_data):
                        str_len = struct.unpack('>H', properties_data[offset:offset + 2])[0]
                        offset += 2
                        if offset + str_len <= len(properties_data):
                            broker_info.authentication_method = properties_data[offset:offset + str_len].decode('utf-8')
                            offset += str_len
                elif property_id == 0x21:  # Receive Maximum
                    if offset + 2 <= len(properties_data):
                        broker_info.receive_maximum = struct.unpack('>H', properties_data[offset:offset + 2])[0]
                        offset += 2
                else:
                    # Unknown property, skip
                    break
                    
        except Exception as e:
            self.logger.debug(f"Error parsing MQTT v5 properties: {e}")
    
    def _identify_broker_manufacturer(self, broker_info: MQTTBrokerInfo, ip_address: str) -> Optional[str]:
        """Identify MQTT broker manufacturer"""
        # Check server reference or assigned client ID for clues
        if broker_info.server_reference:
            ref_lower = broker_info.server_reference.lower()
            if 'mosquitto' in ref_lower:
                return 'Eclipse Mosquitto'
            elif 'hivemq' in ref_lower:
                return 'HiveMQ'
            elif 'emqx' in ref_lower:
                return 'EMQX'
            elif 'rabbitmq' in ref_lower:
                return 'RabbitMQ'
            elif 'aws' in ref_lower or 'amazon' in ref_lower:
                return 'Amazon AWS IoT'
            elif 'azure' in ref_lower or 'microsoft' in ref_lower:
                return 'Microsoft Azure IoT'
            elif 'google' in ref_lower or 'gcp' in ref_lower:
                return 'Google Cloud IoT'
        
        # Check authentication method
        if broker_info.authentication_method:
            auth_lower = broker_info.authentication_method.lower()
            if 'aws' in auth_lower:
                return 'Amazon AWS IoT'
            elif 'azure' in auth_lower:
                return 'Microsoft Azure IoT'
        
        # Default based on common patterns
        if broker_info.topic_alias_maximum and broker_info.topic_alias_maximum > 0:
            return 'HiveMQ'  # HiveMQ commonly supports topic aliases
        
        return 'Unknown MQTT Broker'
    
    def _identify_broker_model(self, broker_info: MQTTBrokerInfo) -> str:
        """Identify specific broker model/type"""
        if broker_info.server_reference:
            if 'mosquitto' in broker_info.server_reference.lower():
                return 'Eclipse Mosquitto'
            elif 'hivemq' in broker_info.server_reference.lower():
                return 'HiveMQ Broker'
            elif 'emqx' in broker_info.server_reference.lower():
                return 'EMQX Broker'
            elif 'rabbitmq' in broker_info.server_reference.lower():
                return 'RabbitMQ MQTT Plugin'
        
        # Determine model based on capabilities
        capabilities = []
        if broker_info.wildcard_subscription_available:
            capabilities.append('wildcard')
        if broker_info.shared_subscription_available:
            capabilities.append('shared_subs')
        if broker_info.subscription_identifier_available:
            capabilities.append('sub_ids')
        
        if len(capabilities) > 2:
            return 'Advanced MQTT Broker'
        elif len(capabilities) > 0:
            return 'Standard MQTT Broker'
        else:
            return 'Basic MQTT Broker'
    
    def _get_broker_capabilities(self, broker_info: MQTTBrokerInfo, port: int) -> List[str]:
        """Get MQTT broker capabilities"""
        capabilities = ['mqtt_broker', 'message_queuing', 'publish_subscribe']
        
        # Add security capability if using secure port
        if port in [8883, 8884, 9883]:
            capabilities.append('tls_security')
        elif port == 9001:
            capabilities.append('websocket_support')
        
        # Add feature-based capabilities
        if broker_info.wildcard_subscription_available:
            capabilities.append('wildcard_subscriptions')
        
        if broker_info.shared_subscription_available:
            capabilities.append('shared_subscriptions')
        
        if broker_info.subscription_identifier_available:
            capabilities.append('subscription_identifiers')
        
        if broker_info.supports_retained_messages:
            capabilities.append('retained_messages')
        
        if broker_info.max_qos >= 2:
            capabilities.append('qos_2_support')
        elif broker_info.max_qos >= 1:
            capabilities.append('qos_1_support')
        
        if broker_info.authentication_method:
            capabilities.append('authentication_required')
        
        return capabilities
    
    async def check_device_status(self, ip_address: str, port: int = None) -> bool:
        """Check if MQTT broker is still online"""
        ports_to_check = [port] if port else [1883, 8883]  # Common ports
        
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
    
    def get_common_mqtt_ports(self) -> List[int]:
        """Get list of common MQTT ports"""
        return self.default_ports