#!/usr/bin/env python3
"""
CT-084 Parachute Drop System - OPC-UA Integration Bridge
Provides industrial-grade OPC-UA connectivity for Phidget sensor data integration.

This module bridges Phidget sensor data to OPC-UA servers with full industrial
protocol compliance, security, and fault tolerance for mission-critical applications.
"""

import os
import sys
import time
import json
import logging
import threading
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union, Callable
from dataclasses import dataclass, asdict
from enum import Enum
import yaml

# OPC-UA libraries
try:
    from asyncua import Client, Server, ua
    from asyncua.common.node import Node
    from asyncua.common.subscription import SubHandler
    from asyncua.crypto.security_policies import SecurityPolicyBasic256Sha256
    from asyncua.crypto.cert_gen import setup_self_signed_certificate
    OPCUA_AVAILABLE = True
except ImportError:
    OPCUA_AVAILABLE = False
    logging.warning("asyncua library not available. OPC-UA functionality disabled.")

# Import local modules
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
try:
    from phidget_auto_configurator.phidget_auto_configurator import SensorInfo, SensorType
except ImportError:
    # Define minimal types for standalone operation
    from enum import Enum
    
    class SensorType(Enum):
        TEMPERATURE = "temperature"
        PRESSURE = "pressure"
        HUMIDITY = "humidity"
        ACCELERATION = "acceleration"
        GYROSCOPE = "gyroscope"
        VOLTAGE = "voltage"
        VOLTAGE_RATIO = "voltage_ratio"

# Configure logging
logger = logging.getLogger('OPCUABridge')

class ConnectionState(Enum):
    """OPC-UA connection states."""
    DISCONNECTED = "disconnected"
    CONNECTING = "connecting"
    CONNECTED = "connected"
    RECONNECTING = "reconnecting"
    ERROR = "error"

class DataQuality(Enum):
    """Data quality indicators."""
    GOOD = "Good"
    UNCERTAIN = "Uncertain"
    BAD = "Bad"

@dataclass
class OPCUANodeInfo:
    """Information about an OPC-UA node."""
    node_id: str
    browse_name: str
    display_name: str
    data_type: str
    access_level: str
    sensor_id: str
    sensor_type: SensorType
    namespace_index: int
    value: Any = None
    timestamp: Optional[str] = None
    quality: DataQuality = DataQuality.GOOD

@dataclass
class OPCUAServerConfig:
    """OPC-UA server configuration."""
    endpoint: str
    namespace: str
    security_policy: str = "None"
    security_mode: str = "None"
    username: Optional[str] = None
    password: Optional[str] = None
    certificate_path: Optional[str] = None
    private_key_path: Optional[str] = None
    trust_store_path: Optional[str] = None

class CT084OPCUABridge:
    """
    OPC-UA bridge for CT-084 Parachute Drop System sensor integration.
    
    Provides bidirectional OPC-UA communication with automatic node creation,
    data publishing, and industrial-grade reliability features.
    """
    
    def __init__(self, config_file: str = "/etc/ct-084/opcua_config.yaml"):
        """Initialize OPC-UA bridge with configuration."""
        self.config_file = config_file
        self.config = self._load_configuration()
        
        # Connection management
        self.client = None
        self.server = None
        self.connection_state = ConnectionState.DISCONNECTED
        self.last_connection_attempt = None
        self.reconnect_interval = 5.0
        
        # Node management
        self.namespace_index = None
        self.sensor_nodes: Dict[str, OPCUANodeInfo] = {}
        self.subscription = None
        self.subscription_handler = None
        
        # Data management
        self.data_buffer: Dict[str, List] = {}
        self.max_buffer_size = 1000
        self.publish_interval = 1.0  # seconds
        
        # Threading
        self.running = False
        self.publish_thread = None
        self.reconnect_thread = None
        
        # Callbacks
        self.data_callbacks: List[Callable] = []
        self.connection_callbacks: List[Callable] = []
        
        logger.info("CT-084 OPC-UA Bridge initialized")
    
    def _load_configuration(self) -> Dict:
        """Load OPC-UA configuration from YAML file."""
        default_config = {
            'client': {
                'endpoint': 'opc.tcp://localhost:4840/freeopcua/server/',
                'namespace': 'CT084_ParachuteDrop',
                'security_policy': 'None',
                'security_mode': 'None',
                'timeout': 10,
                'session_timeout': 60000
            },
            'server': {
                'enabled': False,
                'endpoint': 'opc.tcp://0.0.0.0:4841/ct084/server/',
                'namespace': 'CT084_ParachuteDrop',
                'security_policy': 'None',
                'security_mode': 'None'
            },
            'data_publishing': {
                'publish_interval': 1.0,
                'buffer_size': 1000,
                'quality_monitoring': True,
                'timestamp_source': 'server'
            },
            'fault_tolerance': {
                'auto_reconnect': True,
                'reconnect_interval': 5.0,
                'max_reconnect_attempts': 10,
                'store_and_forward': True
            },
            'node_structure': {
                'base_path': 'CT084/ParachuteDrop',
                'sensor_groups': {
                    'Environment': ['temperature', 'humidity', 'pressure'],
                    'Motion': ['acceleration', 'gyroscope'],
                    'Analog': ['voltage', 'voltage_ratio']
                }
            }
        }
        
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    user_config = yaml.safe_load(f)
                    # Deep merge configuration
                    self._deep_merge_config(default_config, user_config)
                logger.info(f"OPC-UA configuration loaded from {self.config_file}")
            except Exception as e:
                logger.error(f"Failed to load OPC-UA config: {e}. Using defaults.")
        
        return default_config
    
    def _deep_merge_config(self, default: Dict, user: Dict):
        """Deep merge user configuration into defaults."""
        for key, value in user.items():
            if key in default and isinstance(default[key], dict) and isinstance(value, dict):
                self._deep_merge_config(default[key], value)
            else:
                default[key] = value
    
    async def connect_client(self, server_config: Optional[OPCUAServerConfig] = None) -> bool:
        """
        Connect to OPC-UA server as client.
        
        Args:
            server_config: Optional server configuration override
            
        Returns:
            True if connection successful, False otherwise
        """
        if not OPCUA_AVAILABLE:
            logger.error("OPC-UA library not available")
            return False
        
        try:
            self.connection_state = ConnectionState.CONNECTING
            
            # Use provided config or default from file
            config = server_config or self._get_client_config()
            
            logger.info(f"Connecting to OPC-UA server: {config.endpoint}")
            
            # Create client
            self.client = Client(url=config.endpoint)
            
            # Configure security if specified
            if config.security_policy != "None":
                await self._configure_security(config)
            
            # Set session timeout
            self.client.session_timeout = self.config['client']['session_timeout']
            
            # Connect
            await self.client.connect()
            
            # Get namespace index
            namespace_array = await self.client.get_namespace_array()
            if config.namespace in namespace_array:
                self.namespace_index = namespace_array.index(config.namespace)
            else:
                # Create new namespace
                namespace_index = await self.client.get_namespace_index(config.namespace)
                self.namespace_index = namespace_index
            
            self.connection_state = ConnectionState.CONNECTED
            self.last_connection_attempt = datetime.now()
            
            logger.info(f"Connected to OPC-UA server. Namespace index: {self.namespace_index}")
            
            # Trigger connection callbacks
            for callback in self.connection_callbacks:
                try:
                    callback(True, config.endpoint)
                except Exception as e:
                    logger.error(f"Error in connection callback: {e}")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to connect to OPC-UA server: {e}")
            self.connection_state = ConnectionState.ERROR
            
            # Trigger connection callbacks
            for callback in self.connection_callbacks:
                try:
                    callback(False, str(e))
                except Exception as e:
                    logger.error(f"Error in connection callback: {e}")
            
            return False
    
    def _get_client_config(self) -> OPCUAServerConfig:
        """Get client configuration from config file."""
        client_config = self.config['client']
        return OPCUAServerConfig(
            endpoint=client_config['endpoint'],
            namespace=client_config['namespace'],
            security_policy=client_config['security_policy'],
            security_mode=client_config['security_mode']
        )
    
    async def _configure_security(self, config: OPCUAServerConfig):
        """Configure OPC-UA security settings."""
        logger.info(f"Configuring OPC-UA security: {config.security_policy}")
        
        # Set security policy
        if config.security_policy == "Basic256Sha256":
            self.client.set_security(SecurityPolicyBasic256Sha256)
        
        # Load certificates if provided
        if config.certificate_path and config.private_key_path:
            self.client.load_client_certificate(config.certificate_path)
            self.client.load_private_key(config.private_key_path)
        
        # Set user authentication
        if config.username and config.password:
            self.client.set_user(config.username)
            self.client.set_password(config.password)
    
    async def disconnect_client(self):
        """Disconnect from OPC-UA server."""
        if self.client and self.connection_state == ConnectionState.CONNECTED:
            try:
                await self.client.disconnect()
                logger.info("Disconnected from OPC-UA server")
            except Exception as e:
                logger.error(f"Error during disconnect: {e}")
        
        self.connection_state = ConnectionState.DISCONNECTED
        self.client = None
    
    async def create_sensor_nodes(self, sensors: List[SensorInfo]) -> bool:
        """
        Create OPC-UA nodes for sensors with proper namespace organization.
        
        Args:
            sensors: List of sensor information objects
            
        Returns:
            True if nodes created successfully, False otherwise
        """
        if not self.client or self.connection_state != ConnectionState.CONNECTED:
            logger.error("Not connected to OPC-UA server")
            return False
        
        try:
            logger.info(f"Creating OPC-UA nodes for {len(sensors)} sensors")
            
            # Get root node
            root = self.client.get_root_node()
            objects = await root.get_child(["0:Objects"])
            
            # Create base structure
            base_path = self.config['node_structure']['base_path']
            ct084_folder = await self._ensure_folder_exists(objects, "CT084")
            parachute_folder = await self._ensure_folder_exists(ct084_folder, "ParachuteDrop")
            
            # Group sensors by type
            sensor_groups = self.config['node_structure']['sensor_groups']
            
            for sensor in sensors:
                try:
                    # Determine sensor group
                    group_name = self._get_sensor_group(sensor.sensor_type, sensor_groups)
                    group_folder = await self._ensure_folder_exists(parachute_folder, group_name)
                    
                    # Create sensor folder
                    sensor_name = f"Sensor_{sensor.hub_port}"
                    sensor_folder = await self._ensure_folder_exists(group_folder, sensor_name)
                    
                    # Create data nodes for sensor
                    await self._create_sensor_data_nodes(sensor_folder, sensor)
                    
                    logger.info(f"Created OPC-UA nodes for {sensor.sensor_type.value} sensor "
                              f"on port {sensor.hub_port}")
                
                except Exception as e:
                    logger.error(f"Failed to create nodes for sensor {sensor.device_id}: {e}")
                    continue
            
            logger.info("OPC-UA node creation complete")
            return True
            
        except Exception as e:
            logger.error(f"Failed to create sensor nodes: {e}")
            return False
    
    async def _ensure_folder_exists(self, parent_node: Node, folder_name: str) -> Node:
        """Ensure a folder exists, create if necessary."""
        try:
            # Try to get existing folder
            folder = await parent_node.get_child([f"{self.namespace_index}:{folder_name}"])
            return folder
        except:
            # Create new folder
            folder = await parent_node.add_folder(self.namespace_index, folder_name)
            return folder
    
    def _get_sensor_group(self, sensor_type: SensorType, groups: Dict) -> str:
        """Determine which group a sensor belongs to."""
        for group_name, sensor_types in groups.items():
            if sensor_type.value in sensor_types:
                return group_name
        return "Other"
    
    async def _create_sensor_data_nodes(self, sensor_folder: Node, sensor: SensorInfo):
        """Create data nodes for a specific sensor."""
        # Create value node
        value_node = await sensor_folder.add_variable(
            self.namespace_index,
            "Value",
            0.0,
            ua.VariantType.Double
        )
        await value_node.set_writable(False)
        
        # Create quality node
        quality_node = await sensor_folder.add_variable(
            self.namespace_index,
            "Quality",
            "Good",
            ua.VariantType.String
        )
        await quality_node.set_writable(False)
        
        # Create timestamp node
        timestamp_node = await sensor_folder.add_variable(
            self.namespace_index,
            "Timestamp",
            datetime.now(),
            ua.VariantType.DateTime
        )
        await timestamp_node.set_writable(False)
        
        # Create configuration node
        config_node = await sensor_folder.add_variable(
            self.namespace_index,
            "Configuration",
            json.dumps(sensor.configuration or {}),
            ua.VariantType.String
        )
        await config_node.set_writable(False)
        
        # Store node information
        node_info = OPCUANodeInfo(
            node_id=str(value_node.nodeid),
            browse_name=f"Sensor_{sensor.hub_port}_Value",
            display_name=f"{sensor.sensor_type.value} Value",
            data_type="Double",
            access_level="Read",
            sensor_id=sensor.device_id,
            sensor_type=sensor.sensor_type,
            namespace_index=self.namespace_index
        )
        
        self.sensor_nodes[sensor.device_id] = node_info
    
    async def publish_sensor_data(self, sensor_id: str, value: float, 
                                quality: DataQuality = DataQuality.GOOD,
                                timestamp: Optional[datetime] = None) -> bool:
        """
        Publish sensor data to OPC-UA server.
        
        Args:
            sensor_id: Sensor identifier
            value: Sensor value to publish
            quality: Data quality indicator
            timestamp: Optional timestamp (uses current time if None)
            
        Returns:
            True if published successfully, False otherwise
        """
        if not self.client or self.connection_state != ConnectionState.CONNECTED:
            # Store data for later if store-and-forward is enabled
            if self.config['fault_tolerance']['store_and_forward']:
                self._buffer_data(sensor_id, value, quality, timestamp)
            return False
        
        if sensor_id not in self.sensor_nodes:
            logger.warning(f"No OPC-UA node found for sensor {sensor_id}")
            return False
        
        try:
            node_info = self.sensor_nodes[sensor_id]
            
            # Get the value node
            value_node = self.client.get_node(node_info.node_id)
            
            # Update value
            await value_node.write_value(value)
            
            # Update quality and timestamp if nodes exist
            parent_node = await value_node.get_parent()
            
            try:
                quality_node = await parent_node.get_child([f"{self.namespace_index}:Quality"])
                await quality_node.write_value(quality.value)
            except:
                pass  # Quality node may not exist
            
            try:
                timestamp_node = await parent_node.get_child([f"{self.namespace_index}:Timestamp"])
                await timestamp_node.write_value(timestamp or datetime.now())
            except:
                pass  # Timestamp node may not exist
            
            # Update local node info
            node_info.value = value
            node_info.quality = quality
            node_info.timestamp = (timestamp or datetime.now()).isoformat()
            
            logger.debug(f"Published data for sensor {sensor_id}: {value} ({quality.value})")
            return True
            
        except Exception as e:
            logger.error(f"Failed to publish data for sensor {sensor_id}: {e}")
            
            # Store data for later if store-and-forward is enabled
            if self.config['fault_tolerance']['store_and_forward']:
                self._buffer_data(sensor_id, value, quality, timestamp)
            
            return False
    
    def _buffer_data(self, sensor_id: str, value: float, 
                    quality: DataQuality, timestamp: Optional[datetime]):
        """Buffer data for store-and-forward functionality."""
        if sensor_id not in self.data_buffer:
            self.data_buffer[sensor_id] = []
        
        data_point = {
            'value': value,
            'quality': quality.value,
            'timestamp': (timestamp or datetime.now()).isoformat()
        }
        
        self.data_buffer[sensor_id].append(data_point)
        
        # Limit buffer size
        if len(self.data_buffer[sensor_id]) > self.max_buffer_size:
            self.data_buffer[sensor_id].pop(0)
        
        logger.debug(f"Buffered data for sensor {sensor_id}: {value}")
    
    async def flush_buffered_data(self) -> int:
        """
        Flush all buffered data to OPC-UA server.
        
        Returns:
            Number of data points successfully published
        """
        if not self.data_buffer:
            return 0
        
        published_count = 0
        
        for sensor_id, data_points in list(self.data_buffer.items()):
            for data_point in data_points[:]:  # Copy list to avoid modification during iteration
                try:
                    timestamp = datetime.fromisoformat(data_point['timestamp'])
                    quality = DataQuality(data_point['quality'])
                    
                    if await self.publish_sensor_data(sensor_id, data_point['value'], 
                                                    quality, timestamp):
                        self.data_buffer[sensor_id].remove(data_point)
                        published_count += 1
                        
                except Exception as e:
                    logger.error(f"Failed to flush buffered data: {e}")
                    break  # Stop trying to flush this sensor's data
        
        # Clean up empty buffers
        self.data_buffer = {k: v for k, v in self.data_buffer.items() if v}
        
        if published_count > 0:
            logger.info(f"Flushed {published_count} buffered data points")
        
        return published_count
    
    def start_auto_reconnect(self):
        """Start automatic reconnection thread."""
        if self.reconnect_thread and self.reconnect_thread.is_alive():
            return
        
        self.reconnect_thread = threading.Thread(target=self._reconnect_loop, daemon=True)
        self.reconnect_thread.start()
        logger.info("Auto-reconnect thread started")
    
    def _reconnect_loop(self):
        """Automatic reconnection loop."""
        while self.running and self.config['fault_tolerance']['auto_reconnect']:
            if self.connection_state in [ConnectionState.DISCONNECTED, ConnectionState.ERROR]:
                try:
                    logger.info("Attempting to reconnect to OPC-UA server...")
                    self.connection_state = ConnectionState.RECONNECTING
                    
                    # Run async reconnection
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    success = loop.run_until_complete(self.connect_client())
                    loop.close()
                    
                    if success:
                        logger.info("Reconnection successful")
                        # Flush buffered data
                        if self.data_buffer:
                            loop = asyncio.new_event_loop()
                            asyncio.set_event_loop(loop)
                            flushed = loop.run_until_complete(self.flush_buffered_data())
                            loop.close()
                            
                            if flushed > 0:
                                logger.info(f"Restored {flushed} buffered data points")
                    else:
                        logger.warning("Reconnection failed, will retry")
                        
                except Exception as e:
                    logger.error(f"Error during reconnection: {e}")
            
            time.sleep(self.reconnect_interval)
    
    def register_data_callback(self, callback: Callable):
        """Register callback for data events."""
        self.data_callbacks.append(callback)
    
    def register_connection_callback(self, callback: Callable):
        """Register callback for connection events."""
        self.connection_callbacks.append(callback)
    
    def get_node_info(self, sensor_id: str) -> Optional[OPCUANodeInfo]:
        """Get OPC-UA node information for a sensor."""
        return self.sensor_nodes.get(sensor_id)
    
    def get_connection_status(self) -> Dict:
        """Get current connection status."""
        return {
            'state': self.connection_state.value,
            'last_connection_attempt': self.last_connection_attempt.isoformat() if self.last_connection_attempt else None,
            'namespace_index': self.namespace_index,
            'node_count': len(self.sensor_nodes),
            'buffered_data_points': sum(len(data) for data in self.data_buffer.values())
        }
    
    def start(self):
        """Start the OPC-UA bridge."""
        self.running = True
        if self.config['fault_tolerance']['auto_reconnect']:
            self.start_auto_reconnect()
        logger.info("OPC-UA Bridge started")
    
    def stop(self):
        """Stop the OPC-UA bridge."""
        self.running = False
        
        # Disconnect client
        if self.client:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self.disconnect_client())
            loop.close()
        
        # Wait for threads to finish
        if self.reconnect_thread:
            self.reconnect_thread.join(timeout=5)
        
        logger.info("OPC-UA Bridge stopped")

async def main():
    """Main entry point for OPC-UA bridge testing."""
    print("CT-084 OPC-UA Bridge - Testing")
    print("Initializing OPC-UA connection...\n")
    
    # Create bridge
    bridge = CT084OPCUABridge()
    
    # Register callbacks
    def on_connection_change(connected: bool, info: str):
        status = "Connected" if connected else "Disconnected"
        print(f"OPC-UA Connection: {status} - {info}")
    
    bridge.register_connection_callback(on_connection_change)
    
    try:
        # Start bridge
        bridge.start()
        
        # Attempt connection
        success = await bridge.connect_client()
        
        if success:
            print("OPC-UA connection established")
            
            # Create sample sensor nodes
            from datetime import datetime
            sample_sensor = SensorInfo(
                device_id="test_sensor_001",
                sensor_type=SensorType.PRESSURE,
                hub_port=0,
                serial_number="TEST001",
                device_name="Test Pressure Sensor",
                version="1.0.0",
                channel_count=1,
                calibration_status="calibrated",
                timestamp=datetime.now().isoformat()
            )
            
            await bridge.create_sensor_nodes([sample_sensor])
            
            # Publish test data
            for i in range(10):
                test_value = 101.325 - (i * 0.1)  # Simulated pressure drop
                await bridge.publish_sensor_data(
                    "test_sensor_001", 
                    test_value, 
                    DataQuality.GOOD
                )
                print(f"Published test data: {test_value} kPa")
                await asyncio.sleep(1)
        
        else:
            print("Failed to connect to OPC-UA server")
            print("Check server configuration and availability")
    
    except KeyboardInterrupt:
        print("\nShutting down...")
    
    finally:
        bridge.stop()
        print("OPC-UA Bridge testing complete")

if __name__ == "__main__":
    asyncio.run(main())