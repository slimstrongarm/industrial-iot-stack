#!/usr/bin/env python3
"""
Modbus Protocol Scanner for CT-085 Network Discovery
Provides comprehensive Modbus TCP/RTU scanning capabilities for industrial devices
"""

import asyncio
import socket
import struct
import logging
from typing import Dict, Optional, List
from datetime import datetime

logger = logging.getLogger(__name__)

class ModbusScanner:
    """
    Modbus TCP/RTU scanner for discovering and identifying Modbus devices
    Supports Allen-Bradley, Schneider, Siemens, and other industrial PLCs
    """
    
    # Modbus Function Codes
    READ_COILS = 0x01
    READ_DISCRETE_INPUTS = 0x02
    READ_HOLDING_REGISTERS = 0x03
    READ_INPUT_REGISTERS = 0x04
    
    # Device identification registers (common addresses)
    DEVICE_ID_REGISTERS = [0x0000, 0x0001, 0x0002, 0x1000, 0x1001, 0x2000]
    
    # Manufacturer identification patterns
    MANUFACTURER_PATTERNS = {
        'Allen-Bradley': [b'ALLEN-BRADLEY', b'AB', b'ROCKWELL'],
        'Schneider Electric': [b'SCHNEIDER', b'MODICON', b'TELEMECANIQUE'],
        'Siemens': [b'SIEMENS', b'SIMATIC', b'S7'],
        'Omron': [b'OMRON', b'CJ', b'CP'],
        'Mitsubishi': [b'MITSUBISHI', b'MELSEC', b'FX'],
        'Phoenix Contact': [b'PHOENIX', b'ILC'],
        'Beckhoff': [b'BECKHOFF', b'CX', b'BK'],
        'ABB': [b'ABB', b'AC800M'],
        'Emerson': [b'EMERSON', b'DELTAV'],
        'Honeywell': [b'HONEYWELL', b'EXPERION']
    }
    
    def __init__(self, config):
        """Initialize Modbus scanner with configuration"""
        self.config = config
        self.timeout = 3.0
        self.transaction_id = 1
        
    async def scan_host(self, ip_address: str) -> Optional[Dict]:
        """
        Scan a single host for Modbus services
        
        Args:
            ip_address: Target IP address to scan
            
        Returns:
            Device information dictionary if Modbus device found, None otherwise
        """
        # Check standard Modbus TCP port
        for port in self.config.port_ranges.get('modbus', [502]):
            device_info = await self._scan_modbus_port(ip_address, port)
            if device_info:
                return device_info
                
        return None
    
    async def _scan_modbus_port(self, ip_address: str, port: int) -> Optional[Dict]:
        """Scan specific IP:port for Modbus service"""
        try:
            # Attempt TCP connection
            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(ip_address, port),
                timeout=self.timeout
            )
            
            logger.debug(f"Connected to {ip_address}:{port} for Modbus scan")
            
            # Perform Modbus device identification
            device_info = await self._identify_modbus_device(reader, writer, ip_address, port)
            
            writer.close()
            await writer.wait_closed()
            
            return device_info
            
        except Exception as e:
            logger.debug(f"Modbus scan failed for {ip_address}:{port}: {e}")
            return None
    
    async def _identify_modbus_device(self, reader, writer, ip_address: str, port: int) -> Dict:
        """Identify Modbus device through register reads and analysis"""
        device_info = {
            'ip_address': ip_address,
            'port': port,
            'protocol': 'modbus',
            'capabilities': [],
            'registers_found': [],
            'device_signature': None,
            'scan_timestamp': datetime.now().isoformat()
        }
        
        # Test multiple unit IDs (slave addresses)
        for unit_id in [1, 2, 3, 247, 255]:  # Common unit IDs
            try:
                # Test device responsiveness with Read Holding Registers
                response = await self._read_holding_registers(reader, writer, unit_id, 0x0000, 1)
                
                if response:
                    device_info['unit_id'] = unit_id
                    device_info['capabilities'].append('holding_registers')
                    logger.debug(f"Modbus device responds on unit ID {unit_id}")
                    break
                    
            except Exception as e:
                logger.debug(f"Unit ID {unit_id} failed: {e}")
                continue
        
        if 'unit_id' not in device_info:
            logger.debug(f"No responsive unit ID found for {ip_address}:{port}")
            return None
        
        unit_id = device_info['unit_id']
        
        # Test different function codes to determine capabilities
        await self._test_function_codes(reader, writer, unit_id, device_info)
        
        # Read device identification registers
        await self._read_device_identification(reader, writer, unit_id, device_info)
        
        # Perform manufacturer identification
        await self._identify_manufacturer(reader, writer, unit_id, device_info)
        
        # Read device diagnostic information
        await self._read_diagnostics(reader, writer, unit_id, device_info)
        
        return device_info
    
    async def _test_function_codes(self, reader, writer, unit_id: int, device_info: Dict):
        """Test supported Modbus function codes"""
        function_tests = [
            (self.READ_COILS, 'coils'),
            (self.READ_DISCRETE_INPUTS, 'discrete_inputs'),
            (self.READ_HOLDING_REGISTERS, 'holding_registers'),
            (self.READ_INPUT_REGISTERS, 'input_registers')
        ]
        
        for func_code, capability in function_tests:
            try:
                if func_code == self.READ_COILS:
                    response = await self._read_coils(reader, writer, unit_id, 0x0000, 1)
                elif func_code == self.READ_DISCRETE_INPUTS:
                    response = await self._read_discrete_inputs(reader, writer, unit_id, 0x0000, 1)
                elif func_code == self.READ_HOLDING_REGISTERS:
                    response = await self._read_holding_registers(reader, writer, unit_id, 0x0000, 1)
                elif func_code == self.READ_INPUT_REGISTERS:
                    response = await self._read_input_registers(reader, writer, unit_id, 0x0000, 1)
                
                if response:
                    device_info['capabilities'].append(capability)
                    logger.debug(f"Function code {func_code:02X} supported")
                    
            except Exception as e:
                logger.debug(f"Function code {func_code:02X} not supported: {e}")
    
    async def _read_device_identification(self, reader, writer, unit_id: int, device_info: Dict):
        """Read device identification registers"""
        for register in self.DEVICE_ID_REGISTERS:
            try:
                response = await self._read_holding_registers(reader, writer, unit_id, register, 4)
                if response and len(response) >= 8:
                    # Convert register values to string
                    device_info['registers_found'].append({
                        'address': register,
                        'values': response,
                        'ascii': self._registers_to_ascii(response)
                    })
                    
            except Exception as e:
                logger.debug(f"Failed to read register {register:04X}: {e}")
    
    async def _identify_manufacturer(self, reader, writer, unit_id: int, device_info: Dict):
        """Identify device manufacturer based on register content"""
        manufacturer_scores = {}
        
        # Scan common manufacturer identification registers
        for register in range(0x0000, 0x0100, 0x10):  # Sample every 16th register
            try:
                response = await self._read_holding_registers(reader, writer, unit_id, register, 8)
                if response:
                    ascii_data = self._registers_to_ascii(response).upper()
                    
                    # Check against manufacturer patterns
                    for manufacturer, patterns in self.MANUFACTURER_PATTERNS.items():
                        score = 0
                        for pattern in patterns:
                            if pattern.decode('utf-8', errors='ignore').upper() in ascii_data:
                                score += len(pattern)
                        
                        if score > 0:
                            if manufacturer not in manufacturer_scores:
                                manufacturer_scores[manufacturer] = 0
                            manufacturer_scores[manufacturer] += score
                            
            except Exception:
                continue
        
        # Determine most likely manufacturer
        if manufacturer_scores:
            likely_manufacturer = max(manufacturer_scores, key=manufacturer_scores.get)
            confidence = manufacturer_scores[likely_manufacturer] / sum(manufacturer_scores.values())
            
            device_info['manufacturer_detection'] = {
                'manufacturer': likely_manufacturer,
                'confidence': confidence,
                'all_scores': manufacturer_scores
            }
            
            logger.debug(f"Identified manufacturer: {likely_manufacturer} (confidence: {confidence:.2f})")
    
    async def _read_diagnostics(self, reader, writer, unit_id: int, device_info: Dict):
        """Read device diagnostic information"""
        try:
            # Try reading some common diagnostic registers
            diagnostic_registers = [0x1000, 0x2000, 0x3000, 0x4000]
            
            for reg in diagnostic_registers:
                try:
                    response = await self._read_holding_registers(reader, writer, unit_id, reg, 2)
                    if response:
                        device_info['diagnostics'] = device_info.get('diagnostics', {})
                        device_info['diagnostics'][f'reg_{reg:04X}'] = response
                        
                except Exception:
                    continue
                    
        except Exception as e:
            logger.debug(f"Diagnostic read failed: {e}")
    
    async def _read_holding_registers(self, reader, writer, unit_id: int, address: int, count: int) -> Optional[List[int]]:
        """Read Modbus holding registers"""
        return await self._modbus_request(reader, writer, unit_id, self.READ_HOLDING_REGISTERS, address, count)
    
    async def _read_input_registers(self, reader, writer, unit_id: int, address: int, count: int) -> Optional[List[int]]:
        """Read Modbus input registers"""
        return await self._modbus_request(reader, writer, unit_id, self.READ_INPUT_REGISTERS, address, count)
    
    async def _read_coils(self, reader, writer, unit_id: int, address: int, count: int) -> Optional[List[bool]]:
        """Read Modbus coils"""
        response = await self._modbus_request(reader, writer, unit_id, self.READ_COILS, address, count)
        if response:
            # Convert byte response to boolean list
            coils = []
            for byte_val in response:
                for bit in range(8):
                    if len(coils) < count:
                        coils.append(bool(byte_val & (1 << bit)))
            return coils[:count]
        return None
    
    async def _read_discrete_inputs(self, reader, writer, unit_id: int, address: int, count: int) -> Optional[List[bool]]:
        """Read Modbus discrete inputs"""
        response = await self._modbus_request(reader, writer, unit_id, self.READ_DISCRETE_INPUTS, address, count)
        if response:
            # Convert byte response to boolean list
            inputs = []
            for byte_val in response:
                for bit in range(8):
                    if len(inputs) < count:
                        inputs.append(bool(byte_val & (1 << bit)))
            return inputs[:count]
        return None
    
    async def _modbus_request(self, reader, writer, unit_id: int, function_code: int, address: int, count: int) -> Optional[List]:
        """Send Modbus request and parse response"""
        try:
            # Build Modbus TCP request
            self.transaction_id += 1
            if self.transaction_id > 65535:
                self.transaction_id = 1
            
            # MBAP Header (7 bytes) + PDU
            request = struct.pack(
                '>HHHBB HH',
                self.transaction_id,  # Transaction ID
                0x0000,              # Protocol ID
                0x0006,              # Length
                unit_id,             # Unit ID
                function_code,       # Function Code
                address,             # Starting Address
                count                # Quantity
            )
            
            # Send request
            writer.write(request)
            await writer.drain()
            
            # Read response header
            header = await asyncio.wait_for(reader.read(7), timeout=2.0)
            if len(header) != 7:
                return None
            
            trans_id, proto_id, length, unit, func = struct.unpack('>HHHBB', header)
            
            # Validate response header
            if trans_id != self.transaction_id or func != function_code:
                return None
            
            # Read response data
            data_length = length - 2  # Subtract unit ID and function code
            data = await asyncio.wait_for(reader.read(data_length), timeout=2.0)
            
            if len(data) != data_length:
                return None
            
            # Parse response based on function code
            if function_code in [self.READ_HOLDING_REGISTERS, self.READ_INPUT_REGISTERS]:
                byte_count = data[0]
                if len(data) < byte_count + 1:
                    return None
                
                # Convert bytes to 16-bit registers
                registers = []
                for i in range(1, byte_count + 1, 2):
                    if i + 1 < len(data):
                        reg_value = struct.unpack('>H', data[i:i+2])[0]
                        registers.append(reg_value)
                
                return registers
                
            elif function_code in [self.READ_COILS, self.READ_DISCRETE_INPUTS]:
                byte_count = data[0]
                return list(data[1:byte_count+1])
            
            return None
            
        except Exception as e:
            logger.debug(f"Modbus request failed: {e}")
            return None
    
    def _registers_to_ascii(self, registers: List[int]) -> str:
        """Convert register values to ASCII string"""
        ascii_chars = []
        for reg in registers:
            # Each register is 2 bytes (big-endian)
            high_byte = (reg >> 8) & 0xFF
            low_byte = reg & 0xFF
            
            # Only include printable ASCII characters
            if 32 <= high_byte <= 126:
                ascii_chars.append(chr(high_byte))
            if 32 <= low_byte <= 126:
                ascii_chars.append(chr(low_byte))
        
        return ''.join(ascii_chars).strip()

# Test functionality
if __name__ == "__main__":
    async def test_modbus_scanner():
        class MockConfig:
            port_ranges = {'modbus': [502]}
        
        scanner = ModbusScanner(MockConfig())
        
        # Test with known Modbus device (adjust IP as needed)
        test_ip = "192.168.1.100"
        result = await scanner.scan_host(test_ip)
        
        if result:
            print(f"Modbus device found at {test_ip}:")
            print(json.dumps(result, indent=2, default=str))
        else:
            print(f"No Modbus device found at {test_ip}")
    
    import json
    asyncio.run(test_modbus_scanner())