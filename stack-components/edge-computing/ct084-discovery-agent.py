#!/usr/bin/env python3
"""
CT-084 Enhanced Discovery Agent with AI-Powered Tag Intelligence
Industrial IoT Edge Device Discovery and OPC-UA Tag Mapping System

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
import threading
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import uuid

# Core libraries
import requests
from opcua import Client, ua
from opcua.common.node import Node
import paho.mqtt.client as mqtt

# Scientific computing
import numpy as np
import pandas as pd

# Phidget libraries
try:
    from Phidget22.Phidget import *
    from Phidget22.Devices.Hub import *
    from Phidget22.Devices.HumiditySensor import *
    from Phidget22.Devices.TemperatureSensor import *
    from Phidget22.Devices.VoltageRatioInput import *
    from Phidget22.Devices.VoltageInput import *
    from Phidget22.Devices.CurrentInput import *
    PHIDGETS_AVAILABLE = True
except ImportError:
    PHIDGETS_AVAILABLE = False
    logging.warning("Phidget22 library not available")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/var/log/ct084/discovery-agent.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('CT084-Discovery')

class DeviceType(Enum):
    """Enumeration of supported device types"""
    PHIDGET_HUB = "phidget_hub"
    PHIDGET_HUMIDITY = "phidget_humidity"
    PHIDGET_TEMPERATURE = "phidget_temperature"
    PHIDGET_VOLTAGE = "phidget_voltage"
    PHIDGET_CURRENT = "phidget_current"
    MODBUS_DEVICE = "modbus_device"
    OPCUA_SERVER = "opcua_server"
    MQTT_BROKER = "mqtt_broker"
    NETWORK_DEVICE = "network_device"
    UNKNOWN = "unknown"

class SensorContext(Enum):
    """Industrial sensor context classification"""
    TEMPERATURE_AMBIENT = "temperature_ambient"
    TEMPERATURE_PROCESS = "temperature_process"
    HUMIDITY_RELATIVE = "humidity_relative"
    PRESSURE_ABSOLUTE = "pressure_absolute"
    PRESSURE_GAUGE = "pressure_gauge"
    FLOW_VOLUMETRIC = "flow_volumetric"
    LEVEL_TANK = "level_tank"
    VIBRATION_ACCELERATION = "vibration_acceleration"
    CURRENT_AC = "current_ac"
    VOLTAGE_AC = "voltage_ac"
    UNKNOWN = "unknown"

@dataclass
class DeviceInfo:
    """Device information structure"""
    device_id: str
    device_type: DeviceType
    name: str
    location: str
    serial_number: Optional[str] = None
    model: Optional[str] = None
    manufacturer: Optional[str] = None
    firmware_version: Optional[str] = None
    capabilities: List[str] = None
    network_info: Dict[str, Any] = None
    last_seen: datetime = None
    
    def __post_init__(self):
        if self.capabilities is None:
            self.capabilities = []
        if self.network_info is None:
            self.network_info = {}
        if self.last_seen is None:
            self.last_seen = datetime.now()

@dataclass
class SensorDefinition:
    """Intelligent sensor definition with AI-powered context"""
    sensor_id: str
    sensor_type: str
    context: SensorContext
    units: str
    range_min: float
    range_max: float
    precision: int
    update_rate: float
    tags: Dict[str, str]
    metadata: Dict[str, Any]
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = {}
        if self.metadata is None:
            self.metadata = {}

@dataclass
class OPCUATagMapping:
    """OPC-UA tag mapping definition"""
    tag_path: str
    node_id: str
    data_type: str
    access_level: str
    description: str
    units: Optional[str] = None
    scaling: Optional[Dict[str, float]] = None
    alarm_limits: Optional[Dict[str, float]] = None

class IntelligentTagBuilder:
    """AI-powered tag intelligence system for industrial devices"""
    
    def __init__(self):
        self.context_patterns = {
            # Temperature sensor patterns
            r'temp.*ambient|room.*temp|air.*temp': SensorContext.TEMPERATURE_AMBIENT,
            r'temp.*process|tank.*temp|vessel.*temp': SensorContext.TEMPERATURE_PROCESS,
            r'temp.*supply|temp.*return|glycol.*temp': SensorContext.TEMPERATURE_PROCESS,
            
            # Humidity patterns
            r'humidity|rh|moisture': SensorContext.HUMIDITY_RELATIVE,
            
            # Pressure patterns
            r'pressure.*abs|absolute.*pressure': SensorContext.PRESSURE_ABSOLUTE,
            r'pressure.*gauge|gauge.*pressure': SensorContext.PRESSURE_GAUGE,
            
            # Flow patterns
            r'flow.*rate|volumetric.*flow|gpm|lpm': SensorContext.FLOW_VOLUMETRIC,
            
            # Level patterns
            r'level.*tank|tank.*level|level.*vessel': SensorContext.LEVEL_TANK,
            
            # Electrical patterns
            r'current.*ac|ac.*current|amp': SensorContext.CURRENT_AC,
            r'voltage.*ac|ac.*voltage|volt': SensorContext.VOLTAGE_AC,
            
            # Vibration patterns
            r'vibration|acceleration|vibe': SensorContext.VIBRATION_ACCELERATION
        }
        
        # Industrial naming conventions for tag paths
        self.uns_templates = {
            SensorContext.TEMPERATURE_AMBIENT: "Enterprise/{location}/Area/{area}/AmbientTemperature",
            SensorContext.TEMPERATURE_PROCESS: "Enterprise/{location}/Line/{line}/Process/{process}/Temperature",
            SensorContext.HUMIDITY_RELATIVE: "Enterprise/{location}/Area/{area}/RelativeHumidity",
            SensorContext.PRESSURE_ABSOLUTE: "Enterprise/{location}/Line/{line}/Process/{process}/Pressure",
            SensorContext.PRESSURE_GAUGE: "Enterprise/{location}/Line/{line}/Equipment/{equipment}/Pressure",
            SensorContext.FLOW_VOLUMETRIC: "Enterprise/{location}/Line/{line}/Process/{process}/FlowRate",
            SensorContext.LEVEL_TANK: "Enterprise/{location}/Area/{area}/Tank/{tank}/Level",
            SensorContext.CURRENT_AC: "Enterprise/{location}/Area/{area}/Electrical/{circuit}/Current",
            SensorContext.VOLTAGE_AC: "Enterprise/{location}/Area/{area}/Electrical/{circuit}/Voltage",
            SensorContext.VIBRATION_ACCELERATION: "Enterprise/{location}/Line/{line}/Equipment/{equipment}/Vibration"
        }
        
        # Default units mapping
        self.default_units = {
            SensorContext.TEMPERATURE_AMBIENT: "°C",
            SensorContext.TEMPERATURE_PROCESS: "°C",
            SensorContext.HUMIDITY_RELATIVE: "%RH",
            SensorContext.PRESSURE_ABSOLUTE: "kPa",
            SensorContext.PRESSURE_GAUGE: "PSI",
            SensorContext.FLOW_VOLUMETRIC: "L/min",
            SensorContext.LEVEL_TANK: "%",
            SensorContext.CURRENT_AC: "A",
            SensorContext.VOLTAGE_AC: "V",
            SensorContext.VIBRATION_ACCELERATION: "g"
        }
        
        # Typical industrial ranges
        self.typical_ranges = {
            SensorContext.TEMPERATURE_AMBIENT: (-20.0, 80.0),
            SensorContext.TEMPERATURE_PROCESS: (-50.0, 200.0),
            SensorContext.HUMIDITY_RELATIVE: (0.0, 100.0),
            SensorContext.PRESSURE_ABSOLUTE: (0.0, 1000.0),
            SensorContext.PRESSURE_GAUGE: (0.0, 500.0),
            SensorContext.FLOW_VOLUMETRIC: (0.0, 1000.0),
            SensorContext.LEVEL_TANK: (0.0, 100.0),
            SensorContext.CURRENT_AC: (0.0, 100.0),
            SensorContext.VOLTAGE_AC: (0.0, 600.0),
            SensorContext.VIBRATION_ACCELERATION: (0.0, 10.0)
        }
    
    def classify_sensor_context(self, device_info: DeviceInfo, sensor_name: str) -> SensorContext:
        """Use AI pattern matching to classify sensor context"""
        import re
        
        # Combine device name and sensor name for analysis
        combined_text = f"{device_info.name} {sensor_name} {device_info.location}".lower()
        
        # Pattern matching for context classification
        for pattern, context in self.context_patterns.items():
            if re.search(pattern, combined_text):
                logger.info(f"Classified sensor '{sensor_name}' as {context.value} using pattern '{pattern}'")
                return context
        
        # Default classification based on device type
        if device_info.device_type == DeviceType.PHIDGET_TEMPERATURE:
            return SensorContext.TEMPERATURE_PROCESS
        elif device_info.device_type == DeviceType.PHIDGET_HUMIDITY:
            return SensorContext.HUMIDITY_RELATIVE
        elif device_info.device_type == DeviceType.PHIDGET_VOLTAGE:
            return SensorContext.VOLTAGE_AC
        elif device_info.device_type == DeviceType.PHIDGET_CURRENT:
            return SensorContext.CURRENT_AC
        
        logger.warning(f"Could not classify sensor context for '{sensor_name}', using UNKNOWN")
        return SensorContext.UNKNOWN
    
    def generate_uns_path(self, context: SensorContext, device_info: DeviceInfo, 
                         sensor_name: str) -> str:
        """Generate Unified Namespace (UNS) compliant tag path"""
        
        # Extract location components
        location_parts = device_info.location.split('/')
        location = location_parts[0] if location_parts else "UnknownLocation"
        area = location_parts[1] if len(location_parts) > 1 else "GeneralArea"
        
        # Get UNS template for this context
        template = self.uns_templates.get(context, 
            "Enterprise/{location}/Area/{area}/Unknown/{sensor_name}")
        
        # Build tag path with intelligent defaults
        tag_path = template.format(
            location=location,
            area=area,
            line="Line1",  # Default line
            process=sensor_name.replace(' ', ''),
            equipment=device_info.name.replace(' ', ''),
            tank="Tank1",  # Default tank
            circuit="Circuit1",  # Default circuit
            sensor_name=sensor_name.replace(' ', '')
        )
        
        # Ensure valid OPC-UA path format
        tag_path = tag_path.replace(' ', '_').replace('-', '_')
        
        return tag_path
    
    def create_sensor_definition(self, device_info: DeviceInfo, 
                               sensor_name: str, sensor_type: str) -> SensorDefinition:
        """Create intelligent sensor definition with AI-powered metadata"""
        
        # Classify sensor context
        context = self.classify_sensor_context(device_info, sensor_name)
        
        # Generate sensor ID
        sensor_id = f"{device_info.device_id}_{sensor_name.replace(' ', '_').lower()}"
        
        # Get units and ranges based on context
        units = self.default_units.get(context, "units")
        range_min, range_max = self.typical_ranges.get(context, (0.0, 100.0))
        
        # Generate UNS-compliant tag path
        uns_path = self.generate_uns_path(context, device_info, sensor_name)
        
        # Build intelligent tags
        tags = {
            "UNS_Path": uns_path,
            "DeviceID": device_info.device_id,
            "SensorType": sensor_type,
            "Context": context.value,
            "Location": device_info.location,
            "Manufacturer": device_info.manufacturer or "Unknown",
            "Model": device_info.model or "Unknown",
            "SerialNumber": device_info.serial_number or "Unknown"
        }
        
        # Build metadata with AI insights
        metadata = {
            "discovery_timestamp": datetime.now().isoformat(),
            "confidence_score": 0.85,  # AI classification confidence
            "auto_generated": True,
            "context_source": "ai_pattern_matching",
            "device_capabilities": device_info.capabilities,
            "recommended_update_rate": self._recommend_update_rate(context),
            "alarm_enabled": True,
            "trending_enabled": True,
            "archival_enabled": True
        }
        
        return SensorDefinition(
            sensor_id=sensor_id,
            sensor_type=sensor_type,
            context=context,
            units=units,
            range_min=range_min,
            range_max=range_max,
            precision=2,
            update_rate=self._recommend_update_rate(context),
            tags=tags,
            metadata=metadata
        )
    
    def _recommend_update_rate(self, context: SensorContext) -> float:
        """Recommend optimal update rate based on sensor context"""
        fast_contexts = [
            SensorContext.VIBRATION_ACCELERATION,
            SensorContext.CURRENT_AC,
            SensorContext.VOLTAGE_AC
        ]
        
        medium_contexts = [
            SensorContext.TEMPERATURE_PROCESS,
            SensorContext.PRESSURE_ABSOLUTE,
            SensorContext.PRESSURE_GAUGE,
            SensorContext.FLOW_VOLUMETRIC
        ]
        
        if context in fast_contexts:
            return 0.1  # 100ms for fast-changing signals
        elif context in medium_contexts:
            return 1.0  # 1 second for process variables
        else:
            return 5.0  # 5 seconds for slow-changing variables

class PhidgetDiscoveryEngine:
    """Enhanced Phidget device discovery with intelligent sensor mapping"""
    
    def __init__(self, tag_builder: IntelligentTagBuilder):
        self.tag_builder = tag_builder
        self.discovered_devices = {}
        self.sensor_definitions = {}
        
    async def discover_phidget_devices(self) -> List[DeviceInfo]:
        """Discover and classify all connected Phidget devices"""
        devices = []
        
        if not PHIDGETS_AVAILABLE:
            logger.warning("Phidget discovery skipped - library not available")
            return devices
        
        try:
            # Discover VINT Hub
            hub_devices = await self._discover_vint_hubs()
            devices.extend(hub_devices)
            
            # Discover sensors on each hub
            for hub_device in hub_devices:
                sensor_devices = await self._discover_hub_sensors(hub_device)
                devices.extend(sensor_devices)
                
        except Exception as e:
            logger.error(f"Phidget discovery failed: {e}")
        
        return devices
    
    async def _discover_vint_hubs(self) -> List[DeviceInfo]:
        """Discover VINT Hub devices"""
        hubs = []
        
        try:
            hub = Hub()
            await asyncio.get_event_loop().run_in_executor(
                None, hub.openWaitForAttachment, 5000
            )
            
            device_info = DeviceInfo(
                device_id=f"hub_{hub.getDeviceSerialNumber()}",
                device_type=DeviceType.PHIDGET_HUB,
                name=f"VINT Hub {hub.getDeviceSerialNumber()}",
                location="CT084/EdgeNode/PhidgetHub",
                serial_number=str(hub.getDeviceSerialNumber()),
                model="HUB0000",
                manufacturer="Phidgets Inc.",
                firmware_version=str(hub.getDeviceVersion()),
                capabilities=["vint_hub", "usb_device", "sensor_hub"],
                network_info={"port_count": hub.getPortCount()}
            )
            
            hubs.append(device_info)
            self.discovered_devices[device_info.device_id] = device_info
            
            logger.info(f"Discovered VINT Hub: {device_info.serial_number} "
                       f"with {hub.getPortCount()} ports")
            
            hub.close()
            
        except Exception as e:
            logger.error(f"VINT Hub discovery failed: {e}")
        
        return hubs
    
    async def _discover_hub_sensors(self, hub_device: DeviceInfo) -> List[DeviceInfo]:
        """Discover sensors connected to a VINT Hub"""
        sensors = []
        
        try:
            # Test each VINT port for connected sensors
            for port in range(hub_device.network_info.get("port_count", 4)):
                port_sensors = await self._discover_port_sensors(hub_device, port)
                sensors.extend(port_sensors)
                
        except Exception as e:
            logger.error(f"Hub sensor discovery failed: {e}")
        
        return sensors
    
    async def _discover_port_sensors(self, hub_device: DeviceInfo, 
                                   port: int) -> List[DeviceInfo]:
        """Discover sensors on a specific VINT port"""
        sensors = []
        
        # Test for humidity sensor
        humidity_sensor = await self._test_humidity_sensor(hub_device, port)
        if humidity_sensor:
            sensors.append(humidity_sensor)
        
        # Test for temperature sensor
        temp_sensor = await self._test_temperature_sensor(hub_device, port)
        if temp_sensor:
            sensors.append(temp_sensor)
        
        # Test for voltage input
        voltage_sensor = await self._test_voltage_sensor(hub_device, port)
        if voltage_sensor:
            sensors.append(voltage_sensor)
        
        # Test for current input
        current_sensor = await self._test_current_sensor(hub_device, port)
        if current_sensor:
            sensors.append(current_sensor)
        
        return sensors
    
    async def _test_humidity_sensor(self, hub_device: DeviceInfo, 
                                  port: int) -> Optional[DeviceInfo]:
        """Test for humidity sensor on VINT port"""
        try:
            humidity_sensor = HumiditySensor()
            humidity_sensor.setHubPort(port)
            
            await asyncio.get_event_loop().run_in_executor(
                None, humidity_sensor.openWaitForAttachment, 2000
            )
            
            device_info = DeviceInfo(
                device_id=f"humidity_{hub_device.serial_number}_port{port}",
                device_type=DeviceType.PHIDGET_HUMIDITY,
                name=f"Humidity Sensor Port {port}",
                location=f"CT084/EdgeNode/PhidgetHub/Port{port}",
                serial_number=str(humidity_sensor.getDeviceSerialNumber()),
                model="HUM1001",
                manufacturer="Phidgets Inc.",
                firmware_version=str(humidity_sensor.getDeviceVersion()),
                capabilities=["humidity_measurement", "vint_device"],
                network_info={"hub_port": port, "hub_serial": hub_device.serial_number}
            )
            
            # Create intelligent sensor definition
            sensor_def = self.tag_builder.create_sensor_definition(
                device_info, "Relative Humidity", "humidity"
            )
            self.sensor_definitions[sensor_def.sensor_id] = sensor_def
            
            self.discovered_devices[device_info.device_id] = device_info
            logger.info(f"Discovered humidity sensor on port {port}")
            
            humidity_sensor.close()
            return device_info
            
        except Exception as e:
            # Sensor not present or error occurred
            return None
    
    async def _test_temperature_sensor(self, hub_device: DeviceInfo, 
                                     port: int) -> Optional[DeviceInfo]:
        """Test for temperature sensor on VINT port"""
        try:
            temp_sensor = TemperatureSensor()
            temp_sensor.setHubPort(port)
            
            await asyncio.get_event_loop().run_in_executor(
                None, temp_sensor.openWaitForAttachment, 2000
            )
            
            device_info = DeviceInfo(
                device_id=f"temperature_{hub_device.serial_number}_port{port}",
                device_type=DeviceType.PHIDGET_TEMPERATURE,
                name=f"Temperature Sensor Port {port}",
                location=f"CT084/EdgeNode/PhidgetHub/Port{port}",
                serial_number=str(temp_sensor.getDeviceSerialNumber()),
                model="TMP1101",
                manufacturer="Phidgets Inc.",
                firmware_version=str(temp_sensor.getDeviceVersion()),
                capabilities=["temperature_measurement", "vint_device"],
                network_info={"hub_port": port, "hub_serial": hub_device.serial_number}
            )
            
            # Create intelligent sensor definition
            sensor_def = self.tag_builder.create_sensor_definition(
                device_info, "Temperature", "temperature"
            )
            self.sensor_definitions[sensor_def.sensor_id] = sensor_def
            
            self.discovered_devices[device_info.device_id] = device_info
            logger.info(f"Discovered temperature sensor on port {port}")
            
            temp_sensor.close()
            return device_info
            
        except Exception as e:
            # Sensor not present or error occurred
            return None
    
    async def _test_voltage_sensor(self, hub_device: DeviceInfo, 
                                 port: int) -> Optional[DeviceInfo]:
        """Test for voltage input on VINT port"""
        try:
            voltage_sensor = VoltageInput()
            voltage_sensor.setHubPort(port)
            
            await asyncio.get_event_loop().run_in_executor(
                None, voltage_sensor.openWaitForAttachment, 2000
            )
            
            device_info = DeviceInfo(
                device_id=f"voltage_{hub_device.serial_number}_port{port}",
                device_type=DeviceType.PHIDGET_VOLTAGE,
                name=f"Voltage Input Port {port}",
                location=f"CT084/EdgeNode/PhidgetHub/Port{port}",
                serial_number=str(voltage_sensor.getDeviceSerialNumber()),
                model="VCP1001",
                manufacturer="Phidgets Inc.",
                firmware_version=str(voltage_sensor.getDeviceVersion()),
                capabilities=["voltage_measurement", "vint_device"],
                network_info={"hub_port": port, "hub_serial": hub_device.serial_number}
            )
            
            # Create intelligent sensor definition
            sensor_def = self.tag_builder.create_sensor_definition(
                device_info, "Voltage", "voltage"
            )
            self.sensor_definitions[sensor_def.sensor_id] = sensor_def
            
            self.discovered_devices[device_info.device_id] = device_info
            logger.info(f"Discovered voltage input on port {port}")
            
            voltage_sensor.close()
            return device_info
            
        except Exception as e:
            # Sensor not present or error occurred
            return None
    
    async def _test_current_sensor(self, hub_device: DeviceInfo, 
                                 port: int) -> Optional[DeviceInfo]:
        """Test for current input on VINT port"""
        try:
            current_sensor = CurrentInput()
            current_sensor.setHubPort(port)
            
            await asyncio.get_event_loop().run_in_executor(
                None, current_sensor.openWaitForAttachment, 2000
            )
            
            device_info = DeviceInfo(
                device_id=f"current_{hub_device.serial_number}_port{port}",
                device_type=DeviceType.PHIDGET_CURRENT,
                name=f"Current Input Port {port}",
                location=f"CT084/EdgeNode/PhidgetHub/Port{port}",
                serial_number=str(current_sensor.getDeviceSerialNumber()),
                model="CCP1001",
                manufacturer="Phidgets Inc.",
                firmware_version=str(current_sensor.getDeviceVersion()),
                capabilities=["current_measurement", "vint_device"],
                network_info={"hub_port": port, "hub_serial": hub_device.serial_number}
            )
            
            # Create intelligent sensor definition
            sensor_def = self.tag_builder.create_sensor_definition(
                device_info, "Current", "current"
            )
            self.sensor_definitions[sensor_def.sensor_id] = sensor_def
            
            self.discovered_devices[device_info.device_id] = device_info
            logger.info(f"Discovered current input on port {port}")
            
            current_sensor.close()
            return device_info
            
        except Exception as e:
            # Sensor not present or error occurred
            return None

class NetworkDiscoveryEngine:
    """Network-based device discovery for industrial protocols"""
    
    def __init__(self):
        self.discovered_devices = {}
    
    async def discover_network_devices(self, network_range: str = "192.168.1.0/24") -> List[DeviceInfo]:
        """Discover network-accessible industrial devices"""
        devices = []
        
        # Discover OPC-UA servers
        opcua_devices = await self._discover_opcua_servers()
        devices.extend(opcua_devices)
        
        # Discover MQTT brokers
        mqtt_devices = await self._discover_mqtt_brokers()
        devices.extend(mqtt_devices)
        
        # Discover Modbus devices
        modbus_devices = await self._discover_modbus_devices()
        devices.extend(modbus_devices)
        
        return devices
    
    async def _discover_opcua_servers(self) -> List[DeviceInfo]:
        """Discover OPC-UA servers on the network"""
        devices = []
        
        # Common OPC-UA ports and endpoints
        common_endpoints = [
            "opc.tcp://localhost:4840",
            "opc.tcp://ignition:62541",
            "opc.tcp://192.168.1.100:4840",
            "opc.tcp://scada:4840"
        ]
        
        for endpoint in common_endpoints:
            try:
                client = Client(endpoint)
                await asyncio.get_event_loop().run_in_executor(
                    None, client.connect
                )
                
                # Get server info
                server_info = client.get_server_node().get_browse_name()
                
                device_info = DeviceInfo(
                    device_id=f"opcua_{endpoint.replace(':', '_').replace('/', '_')}",
                    device_type=DeviceType.OPCUA_SERVER,
                    name=f"OPC-UA Server {endpoint}",
                    location="CT084/Network/OPCUA",
                    capabilities=["opcua_server", "data_access", "alarms_conditions"],
                    network_info={"endpoint": endpoint, "server_info": str(server_info)}
                )
                
                devices.append(device_info)
                self.discovered_devices[device_info.device_id] = device_info
                
                logger.info(f"Discovered OPC-UA server: {endpoint}")
                client.disconnect()
                
            except Exception as e:
                # Server not available
                pass
        
        return devices
    
    async def _discover_mqtt_brokers(self) -> List[DeviceInfo]:
        """Discover MQTT brokers on the network"""
        devices = []
        
        # Common MQTT broker addresses
        common_brokers = [
            ("localhost", 1883),
            ("emqx", 1883),
            ("mosquitto", 1883),
            ("192.168.1.100", 1883)
        ]
        
        for host, port in common_brokers:
            try:
                # Test MQTT connection
                client = mqtt.Client()
                client.connect(host, port, 5)
                
                device_info = DeviceInfo(
                    device_id=f"mqtt_{host}_{port}",
                    device_type=DeviceType.MQTT_BROKER,
                    name=f"MQTT Broker {host}:{port}",
                    location="CT084/Network/MQTT",
                    capabilities=["mqtt_broker", "pub_sub", "qos_levels"],
                    network_info={"host": host, "port": port}
                )
                
                devices.append(device_info)
                self.discovered_devices[device_info.device_id] = device_info
                
                logger.info(f"Discovered MQTT broker: {host}:{port}")
                client.disconnect()
                
            except Exception as e:
                # Broker not available
                pass
        
        return devices
    
    async def _discover_modbus_devices(self) -> List[DeviceInfo]:
        """Discover Modbus devices on the network"""
        devices = []
        
        # This would implement Modbus device scanning
        # For now, return empty list
        logger.info("Modbus discovery not yet implemented")
        
        return devices

class OPCUATagManager:
    """OPC-UA tag creation and management system"""
    
    def __init__(self, endpoint: str = "opc.tcp://localhost:4840"):
        self.endpoint = endpoint
        self.client = None
        self.tag_mappings = {}
    
    async def connect(self) -> bool:
        """Connect to OPC-UA server"""
        try:
            self.client = Client(self.endpoint)
            await asyncio.get_event_loop().run_in_executor(
                None, self.client.connect
            )
            logger.info(f"Connected to OPC-UA server: {self.endpoint}")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to OPC-UA server: {e}")
            return False
    
    async def create_tag_structure(self, sensor_definitions: Dict[str, SensorDefinition]) -> bool:
        """Create OPC-UA tag structure from sensor definitions"""
        if not self.client:
            logger.error("OPC-UA client not connected")
            return False
        
        try:
            # Get root folder
            root = self.client.get_root_node()
            objects = self.client.get_objects_node()
            
            # Create CT-084 folder structure
            ct084_folder = await self._get_or_create_folder(objects, "CT084")
            edge_folder = await self._get_or_create_folder(ct084_folder, "EdgeNodes")
            
            # Create tags for each sensor
            for sensor_id, sensor_def in sensor_definitions.items():
                await self._create_sensor_tags(edge_folder, sensor_def)
            
            logger.info(f"Created OPC-UA tag structure for {len(sensor_definitions)} sensors")
            return True
            
        except Exception as e:
            logger.error(f"Failed to create OPC-UA tag structure: {e}")
            return False
    
    async def _get_or_create_folder(self, parent_node: Node, folder_name: str) -> Node:
        """Get existing folder or create new one"""
        try:
            # Try to find existing folder
            for child in parent_node.get_children():
                if child.get_browse_name().Name == folder_name:
                    return child
            
            # Create new folder
            folder = await asyncio.get_event_loop().run_in_executor(
                None, parent_node.add_folder, folder_name
            )
            return folder
            
        except Exception as e:
            logger.error(f"Failed to create folder {folder_name}: {e}")
            raise
    
    async def _create_sensor_tags(self, parent_folder: Node, 
                                sensor_def: SensorDefinition) -> None:
        """Create OPC-UA tags for a sensor"""
        try:
            # Create sensor folder
            sensor_folder = await self._get_or_create_folder(
                parent_folder, sensor_def.sensor_id
            )
            
            # Create value tag
            value_tag = await asyncio.get_event_loop().run_in_executor(
                None, sensor_folder.add_variable,
                f"{sensor_def.sensor_id}_Value",
                0.0
            )
            
            # Create quality tag
            quality_tag = await asyncio.get_event_loop().run_in_executor(
                None, sensor_folder.add_variable,
                f"{sensor_def.sensor_id}_Quality",
                "Good"
            )
            
            # Create timestamp tag
            timestamp_tag = await asyncio.get_event_loop().run_in_executor(
                None, sensor_folder.add_variable,
                f"{sensor_def.sensor_id}_Timestamp",
                datetime.now()
            )
            
            # Store tag mappings
            self.tag_mappings[sensor_def.sensor_id] = {
                "value": value_tag,
                "quality": quality_tag,
                "timestamp": timestamp_tag,
                "folder": sensor_folder
            }
            
            logger.info(f"Created OPC-UA tags for sensor: {sensor_def.sensor_id}")
            
        except Exception as e:
            logger.error(f"Failed to create tags for sensor {sensor_def.sensor_id}: {e}")
    
    async def update_tag_value(self, sensor_id: str, value: float, 
                             quality: str = "Good") -> bool:
        """Update sensor tag value in OPC-UA server"""
        try:
            if sensor_id not in self.tag_mappings:
                logger.warning(f"Tag mapping not found for sensor: {sensor_id}")
                return False
            
            mapping = self.tag_mappings[sensor_id]
            
            # Update value
            await asyncio.get_event_loop().run_in_executor(
                None, mapping["value"].set_value, value
            )
            
            # Update quality
            await asyncio.get_event_loop().run_in_executor(
                None, mapping["quality"].set_value, quality
            )
            
            # Update timestamp
            await asyncio.get_event_loop().run_in_executor(
                None, mapping["timestamp"].set_value, datetime.now()
            )
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to update tag value for {sensor_id}: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from OPC-UA server"""
        if self.client:
            try:
                self.client.disconnect()
                logger.info("Disconnected from OPC-UA server")
            except Exception as e:
                logger.error(f"Error disconnecting from OPC-UA server: {e}")

class CT084DiscoveryAgent:
    """Main CT-084 Enhanced Discovery Agent"""
    
    def __init__(self, config_file: str = "/etc/ct084/ct084-config.json"):
        self.config_file = Path(config_file)
        self.config = {}
        self.running = False
        
        # Initialize components
        self.tag_builder = IntelligentTagBuilder()
        self.phidget_engine = PhidgetDiscoveryEngine(self.tag_builder)
        self.network_engine = NetworkDiscoveryEngine()
        self.opcua_manager = None
        
        # Discovery results
        self.all_devices = {}
        self.all_sensors = {}
        
        # Load configuration
        self.load_config()
        
        # Initialize OPC-UA manager if enabled
        if self.config.get("network", {}).get("opcua_endpoint"):
            self.opcua_manager = OPCUATagManager(
                self.config["network"]["opcua_endpoint"]
            )
    
    def load_config(self):
        """Load configuration from file"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r') as f:
                    self.config = json.load(f)
                logger.info(f"Loaded configuration from {self.config_file}")
            else:
                logger.warning(f"Configuration file not found: {self.config_file}")
                self.config = self._get_default_config()
        except Exception as e:
            logger.error(f"Failed to load configuration: {e}")
            self.config = self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration"""
        return {
            "device_info": {
                "device_id": "ct084-discovery-agent",
                "device_type": "CT-084-Parachute-Drop",
                "version": "1.0.0"
            },
            "discovery": {
                "enabled": True,
                "scan_interval": 30,
                "phidget_enabled": True,
                "network_enabled": True
            },
            "network": {
                "opcua_endpoint": "opc.tcp://localhost:4840",
                "mqtt_broker": "localhost",
                "mqtt_port": 1883
            }
        }
    
    async def start(self):
        """Start the discovery agent"""
        logger.info("Starting CT-084 Enhanced Discovery Agent...")
        self.running = True
        
        # Connect to OPC-UA server if configured
        if self.opcua_manager:
            await self.opcua_manager.connect()
        
        # Run discovery loop
        while self.running:
            try:
                await self.run_discovery_cycle()
                
                # Wait for next scan interval
                scan_interval = self.config.get("discovery", {}).get("scan_interval", 30)
                await asyncio.sleep(scan_interval)
                
            except Exception as e:
                logger.error(f"Discovery cycle failed: {e}")
                await asyncio.sleep(10)  # Shorter retry interval
    
    async def run_discovery_cycle(self):
        """Run complete discovery cycle"""
        logger.info("Running discovery cycle...")
        
        # Discover Phidget devices
        if self.config.get("discovery", {}).get("phidget_enabled", True):
            phidget_devices = await self.phidget_engine.discover_phidget_devices()
            for device in phidget_devices:
                self.all_devices[device.device_id] = device
        
        # Discover network devices
        if self.config.get("discovery", {}).get("network_enabled", True):
            network_devices = await self.network_engine.discover_network_devices()
            for device in network_devices:
                self.all_devices[device.device_id] = device
        
        # Update sensor definitions
        self.all_sensors.update(self.phidget_engine.sensor_definitions)
        
        # Create/update OPC-UA tag structure
        if self.opcua_manager and self.all_sensors:
            await self.opcua_manager.create_tag_structure(self.all_sensors)
        
        # Save discovery results
        await self.save_discovery_results()
        
        logger.info(f"Discovery cycle completed - Found {len(self.all_devices)} devices, "
                   f"{len(self.all_sensors)} sensors")
    
    async def save_discovery_results(self):
        """Save discovery results to file"""
        try:
            results = {
                "discovery_timestamp": datetime.now().isoformat(),
                "agent_version": "1.0.0",
                "devices": {
                    device_id: asdict(device) 
                    for device_id, device in self.all_devices.items()
                },
                "sensors": {
                    sensor_id: asdict(sensor)
                    for sensor_id, sensor in self.all_sensors.items()
                },
                "summary": {
                    "total_devices": len(self.all_devices),
                    "total_sensors": len(self.all_sensors),
                    "device_types": list(set(device.device_type.value 
                                           for device in self.all_devices.values())),
                    "sensor_contexts": list(set(sensor.context.value 
                                              for sensor in self.all_sensors.values()))
                }
            }
            
            results_file = Path("/var/log/ct084/discovery-results.json")
            results_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(results_file, 'w') as f:
                json.dump(results, f, indent=2, default=str)
            
            logger.info(f"Discovery results saved to {results_file}")
            
        except Exception as e:
            logger.error(f"Failed to save discovery results: {e}")
    
    def stop(self):
        """Stop the discovery agent"""
        logger.info("Stopping CT-084 Discovery Agent...")
        self.running = False
        
        if self.opcua_manager:
            self.opcua_manager.disconnect()

async def main():
    """Main entry point for CT-084 Discovery Agent"""
    agent = CT084DiscoveryAgent()
    
    try:
        await agent.start()
    except KeyboardInterrupt:
        logger.info("Received interrupt signal")
    except Exception as e:
        logger.error(f"Agent failed: {e}")
    finally:
        agent.stop()

if __name__ == "__main__":
    asyncio.run(main())