#!/usr/bin/env python3
"""
CT-084 Parachute Drop System - Phidget Auto Sensor Configurator
Automatically detects, configures, and integrates Phidget sensors for parachute drop monitoring.

This module provides intelligent device recognition, automatic calibration,
and industrial protocol integration for CT-084 mission-critical applications.
"""

import os
import sys
import time
import json
import logging
import threading
import yaml
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from enum import Enum

# Import Phidget libraries (installed separately)
try:
    from Phidget22.Phidget import *
    from Phidget22.Devices.Hub import *
    from Phidget22.Devices.VoltageInput import *
    from Phidget22.Devices.VoltageRatioInput import *
    from Phidget22.Devices.TemperatureSensor import *
    from Phidget22.Devices.HumiditySensor import *
    from Phidget22.Devices.PressureSensor import *
    from Phidget22.Devices.Accelerometer import *
    from Phidget22.Devices.Gyroscope import *
    PHIDGET_AVAILABLE = True
except ImportError:
    PHIDGET_AVAILABLE = False
    logging.warning("Phidget22 library not available. Running in simulation mode.")

# Configure logging for CT-084 mission requirements
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | CT-084 | %(name)-20s | %(levelname)-8s | %(message)s',
    handlers=[
        logging.FileHandler('/var/log/ct-084/phidget_configurator.log', mode='a'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('PhidgetAutoConfigurator')

class SensorType(Enum):
    """Enumeration of supported sensor types for CT-084 parachute drop system."""
    TEMPERATURE = "temperature"
    PRESSURE = "pressure" 
    HUMIDITY = "humidity"
    ACCELERATION = "acceleration"
    GYROSCOPE = "gyroscope"
    VOLTAGE = "voltage"
    VOLTAGE_RATIO = "voltage_ratio"
    STRAIN_GAUGE = "strain_gauge"
    LOAD_CELL = "load_cell"
    UNKNOWN = "unknown"

class SensorConfig(Enum):
    """Pre-defined sensor configurations for parachute drop applications."""
    ALTITUDE_PRESSURE = "altitude_pressure"
    ENVIRONMENTAL_TEMP = "environmental_temp"
    VIBRATION_MONITOR = "vibration_monitor"
    LOAD_MONITORING = "load_monitoring"
    ORIENTATION_TRACKING = "orientation_tracking"

@dataclass
class SensorInfo:
    """Container for sensor information and metadata."""
    device_id: str
    sensor_type: SensorType
    hub_port: int
    serial_number: str
    device_name: str
    version: str
    channel_count: int
    calibration_status: str
    last_reading: Optional[float] = None
    timestamp: Optional[str] = None
    quality: str = "Unknown"
    configuration: Optional[Dict] = None
    opcua_namespace: Optional[str] = None

@dataclass
class PhidgetHubInfo:
    """Container for Phidget Hub information."""
    serial_number: str
    version: str
    port_count: int
    connected_sensors: List[SensorInfo]
    hub_status: str
    discovery_timestamp: str

class PhidgetAutoConfigurator:
    """
    Main auto-configurator class for CT-084 Phidget hub integration.
    
    Provides automatic device detection, sensor identification, calibration,
    and industrial protocol integration for mission-critical applications.
    """
    
    def __init__(self, config_file: str = "/etc/ct-084/phidget_config.yaml"):
        """Initialize the auto-configurator with configuration file."""
        self.config_file = config_file
        self.config = self._load_configuration()
        self.discovered_hubs: Dict[str, PhidgetHubInfo] = {}
        self.active_sensors: Dict[str, SensorInfo] = {}
        self.calibration_data: Dict[str, Dict] = {}
        self.running = False
        self.monitoring_thread = None
        
        # CT-084 specific configuration
        self.mission_config = {
            'altitude_thresholds': {
                'deployment_altitude': 1000,  # meters
                'critical_altitude': 500,     # meters
                'ground_level': 100          # meters
            },
            'sensor_priorities': {
                SensorType.PRESSURE: 1,      # Critical for altitude
                SensorType.ACCELERATION: 2,  # Critical for deployment detection
                SensorType.TEMPERATURE: 3,   # Environmental monitoring
                SensorType.HUMIDITY: 4       # Environmental monitoring
            },
            'data_rates': {
                'high_priority': 10,  # 10 Hz for critical sensors
                'normal': 1,          # 1 Hz for environmental
                'diagnostic': 0.1     # 0.1 Hz for diagnostics
            }
        }
        
        logger.info("CT-084 Phidget Auto-Configurator initialized")
        
    def _load_configuration(self) -> Dict:
        """Load configuration from YAML file with CT-084 defaults."""
        default_config = {
            'device_discovery': {
                'scan_interval': 5,
                'connection_timeout': 10,
                'retry_attempts': 3
            },
            'sensor_calibration': {
                'auto_calibrate': True,
                'calibration_samples': 100,
                'calibration_timeout': 30
            },
            'opcua_integration': {
                'enabled': True,
                'server_endpoint': 'opc.tcp://localhost:4840',
                'namespace': 'CT084_ParachuteDrop',
                'security_policy': 'None'
            },
            'data_logging': {
                'local_storage': True,
                'storage_path': '/var/log/ct-084/sensor_data',
                'retention_days': 30
            },
            'fault_tolerance': {
                'enable_redundancy': True,
                'sensor_timeout': 5,
                'max_consecutive_failures': 3
            }
        }
        
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    user_config = yaml.safe_load(f)
                    default_config.update(user_config)
                logger.info(f"Configuration loaded from {self.config_file}")
            except Exception as e:
                logger.error(f"Failed to load config file: {e}. Using defaults.")
        else:
            logger.info("Config file not found. Using default configuration.")
            
        return default_config
    
    def discover_phidget_hubs(self) -> List[PhidgetHubInfo]:
        """
        Automatically discover and enumerate Phidget VINT hubs.
        
        Returns:
            List of discovered Phidget hub information
        """
        logger.info("Starting Phidget hub discovery for CT-084 system...")
        discovered_hubs = []
        
        if not PHIDGET_AVAILABLE:
            logger.warning("Phidget library not available. Running discovery simulation.")
            # Return simulated hub for testing
            sim_hub = PhidgetHubInfo(
                serial_number="SIM123456",
                version="1.0.0",
                port_count=4,
                connected_sensors=[],
                hub_status="simulated",
                discovery_timestamp=datetime.now().isoformat()
            )
            discovered_hubs.append(sim_hub)
            self.discovered_hubs[sim_hub.serial_number] = sim_hub
            return discovered_hubs
        
        try:
            # Create hub instance for discovery
            hub = Hub()
            
            # Set up event handlers for hub discovery
            def on_attach(self):
                try:
                    hub_info = PhidgetHubInfo(
                        serial_number=str(hub.getDeviceSerialNumber()),
                        version=str(hub.getDeviceVersion()),
                        port_count=hub.getPortCount(),
                        connected_sensors=[],
                        hub_status="connected",
                        discovery_timestamp=datetime.now().isoformat()
                    )
                    
                    discovered_hubs.append(hub_info)
                    self.discovered_hubs[hub_info.serial_number] = hub_info
                    
                    logger.info(f"Discovered VINT Hub: {hub_info.serial_number} "
                              f"with {hub_info.port_count} ports")
                    
                except Exception as e:
                    logger.error(f"Error processing hub attachment: {e}")
            
            def on_detach(self):
                logger.warning(f"Hub {hub.getDeviceSerialNumber()} detached")
            
            def on_error(self, code, description):
                logger.error(f"Hub error {code}: {description}")
            
            # Set event handlers
            hub.setOnAttachHandler(on_attach)
            hub.setOnDetachHandler(on_detach)
            hub.setOnErrorHandler(on_error)
            
            # Open connection and wait for attachment
            hub.openWaitForAttachment(self.config['device_discovery']['connection_timeout'] * 1000)
            
            # Give time for discovery
            time.sleep(2)
            
            # Close the discovery connection
            hub.close()
            
        except Exception as e:
            logger.error(f"Hub discovery failed: {e}")
        
        logger.info(f"Hub discovery complete. Found {len(discovered_hubs)} hubs.")
        return discovered_hubs
    
    def identify_sensor_type(self, hub_port: int, hub_serial: str) -> Tuple[SensorType, Dict]:
        """
        Intelligently identify sensor type on a specific hub port.
        
        Args:
            hub_port: VINT hub port number
            hub_serial: Hub serial number
            
        Returns:
            Tuple of (sensor_type, device_info)
        """
        logger.info(f"Identifying sensor on hub {hub_serial} port {hub_port}")
        
        sensor_candidates = [
            (TemperatureSensor, SensorType.TEMPERATURE),
            (HumiditySensor, SensorType.HUMIDITY),
            (PressureSensor, SensorType.PRESSURE),
            (Accelerometer, SensorType.ACCELERATION),
            (Gyroscope, SensorType.GYROSCOPE),
            (VoltageInput, SensorType.VOLTAGE),
            (VoltageRatioInput, SensorType.VOLTAGE_RATIO)
        ]
        
        if not PHIDGET_AVAILABLE:
            # Simulation mode - return mock sensor for testing
            return SensorType.PRESSURE, {
                'device_name': 'Simulated Pressure Sensor',
                'serial_number': f'SIM{hub_port}001',
                'version': '1.0.0',
                'channel_count': 1
            }
        
        for sensor_class, sensor_type in sensor_candidates:
            try:
                sensor = sensor_class()
                sensor.setHubPort(hub_port)
                
                # Try to open connection
                sensor.openWaitForAttachment(3000)  # 3 second timeout
                
                # Successfully connected - gather device info
                device_info = {
                    'device_name': sensor.getDeviceName(),
                    'serial_number': str(sensor.getDeviceSerialNumber()),
                    'version': str(sensor.getDeviceVersion()),
                    'channel_count': getattr(sensor, 'getChannelCount', lambda: 1)()
                }
                
                sensor.close()
                
                logger.info(f"Identified {sensor_type.value} sensor: {device_info['device_name']}")
                return sensor_type, device_info
                
            except Exception as e:
                # This sensor type is not present on this port
                try:
                    sensor.close()
                except:
                    pass
                continue
        
        logger.warning(f"No recognized sensor found on port {hub_port}")
        return SensorType.UNKNOWN, {}
    
    def auto_configure_sensor(self, sensor_info: SensorInfo) -> bool:
        """
        Automatically configure a sensor based on its type and CT-084 requirements.
        
        Args:
            sensor_info: Sensor information object
            
        Returns:
            True if configuration successful, False otherwise
        """
        logger.info(f"Auto-configuring {sensor_info.sensor_type.value} sensor "
                   f"on port {sensor_info.hub_port}")
        
        try:
            # Get sensor-specific configuration
            config = self._get_sensor_configuration(sensor_info.sensor_type)
            
            if not PHIDGET_AVAILABLE:
                # Simulation mode
                sensor_info.configuration = config
                sensor_info.calibration_status = "simulated"
                logger.info(f"Simulated configuration for {sensor_info.sensor_type.value}")
                return True
            
            # Apply configuration based on sensor type
            if sensor_info.sensor_type == SensorType.PRESSURE:
                return self._configure_pressure_sensor(sensor_info, config)
            elif sensor_info.sensor_type == SensorType.TEMPERATURE:
                return self._configure_temperature_sensor(sensor_info, config)
            elif sensor_info.sensor_type == SensorType.ACCELERATION:
                return self._configure_acceleration_sensor(sensor_info, config)
            elif sensor_info.sensor_type == SensorType.HUMIDITY:
                return self._configure_humidity_sensor(sensor_info, config)
            else:
                logger.warning(f"No specific configuration for {sensor_info.sensor_type.value}")
                return False
                
        except Exception as e:
            logger.error(f"Failed to configure sensor: {e}")
            return False
    
    def _get_sensor_configuration(self, sensor_type: SensorType) -> Dict:
        """Get CT-084 specific sensor configuration."""
        configurations = {
            SensorType.PRESSURE: {
                'data_interval': 100,  # 10 Hz for critical altitude monitoring
                'change_trigger': 0.1,  # 0.1 kPa sensitivity
                'units': 'kPa',
                'range': 'auto',
                'calibration_type': 'barometric_altitude',
                'alerts': {
                    'low_pressure': 80.0,   # ~2000m altitude warning
                    'critical_pressure': 69.0  # ~3000m altitude critical
                }
            },
            SensorType.TEMPERATURE: {
                'data_interval': 1000,  # 1 Hz for environmental monitoring
                'change_trigger': 0.5,   # 0.5°C sensitivity
                'units': 'celsius',
                'range': [-40, 85],
                'calibration_type': 'environmental'
            },
            SensorType.ACCELERATION: {
                'data_interval': 100,   # 10 Hz for vibration/deployment detection
                'change_trigger': 0.1,  # 0.1g sensitivity
                'range': 8,             # ±8g range
                'calibration_type': 'deployment_detection',
                'alerts': {
                    'deployment_threshold': 2.0,  # 2g indicates deployment
                    'impact_threshold': 5.0       # 5g indicates impact
                }
            },
            SensorType.HUMIDITY: {
                'data_interval': 5000,  # 0.2 Hz for environmental monitoring
                'change_trigger': 2.0,   # 2% RH sensitivity
                'units': 'percent_rh',
                'calibration_type': 'environmental'
            }
        }
        
        return configurations.get(sensor_type, {})
    
    def _configure_pressure_sensor(self, sensor_info: SensorInfo, config: Dict) -> bool:
        """Configure pressure sensor for altitude monitoring."""
        try:
            pressure_sensor = PressureSensor()
            pressure_sensor.setHubPort(sensor_info.hub_port)
            pressure_sensor.openWaitForAttachment(5000)
            
            # Set data interval and change trigger
            pressure_sensor.setDataInterval(config.get('data_interval', 100))
            pressure_sensor.setPressureChangeTrigger(config.get('change_trigger', 0.1))
            
            # Perform calibration
            if self._calibrate_pressure_sensor(pressure_sensor, sensor_info):
                sensor_info.calibration_status = "calibrated"
                sensor_info.configuration = config
                logger.info(f"Pressure sensor configured for altitude monitoring")
                
                pressure_sensor.close()
                return True
            else:
                pressure_sensor.close()
                return False
                
        except Exception as e:
            logger.error(f"Failed to configure pressure sensor: {e}")
            return False
    
    def _configure_temperature_sensor(self, sensor_info: SensorInfo, config: Dict) -> bool:
        """Configure temperature sensor for environmental monitoring."""
        try:
            temp_sensor = TemperatureSensor()
            temp_sensor.setHubPort(sensor_info.hub_port)
            temp_sensor.openWaitForAttachment(5000)
            
            # Set data interval and change trigger
            temp_sensor.setDataInterval(config.get('data_interval', 1000))
            temp_sensor.setTemperatureChangeTrigger(config.get('change_trigger', 0.5))
            
            sensor_info.calibration_status = "factory_calibrated"
            sensor_info.configuration = config
            
            temp_sensor.close()
            logger.info("Temperature sensor configured for environmental monitoring")
            return True
            
        except Exception as e:
            logger.error(f"Failed to configure temperature sensor: {e}")
            return False
    
    def _configure_acceleration_sensor(self, sensor_info: SensorInfo, config: Dict) -> bool:
        """Configure accelerometer for deployment detection."""
        try:
            accel_sensor = Accelerometer()
            accel_sensor.setHubPort(sensor_info.hub_port)
            accel_sensor.openWaitForAttachment(5000)
            
            # Set data interval and acceleration range
            accel_sensor.setDataInterval(config.get('data_interval', 100))
            
            # Set acceleration range if supported
            try:
                accel_sensor.setAccelerationRange(config.get('range', 8))
            except:
                logger.warning("Acceleration range setting not supported")
            
            # Perform calibration
            if self._calibrate_acceleration_sensor(accel_sensor, sensor_info):
                sensor_info.calibration_status = "calibrated"
                sensor_info.configuration = config
                logger.info("Accelerometer configured for deployment detection")
                
                accel_sensor.close()
                return True
            else:
                accel_sensor.close()
                return False
                
        except Exception as e:
            logger.error(f"Failed to configure accelerometer: {e}")
            return False
    
    def _configure_humidity_sensor(self, sensor_info: SensorInfo, config: Dict) -> bool:
        """Configure humidity sensor for environmental monitoring."""
        try:
            humidity_sensor = HumiditySensor()
            humidity_sensor.setHubPort(sensor_info.hub_port)
            humidity_sensor.openWaitForAttachment(5000)
            
            # Set data interval and change trigger
            humidity_sensor.setDataInterval(config.get('data_interval', 5000))
            humidity_sensor.setHumidityChangeTrigger(config.get('change_trigger', 2.0))
            
            sensor_info.calibration_status = "factory_calibrated"
            sensor_info.configuration = config
            
            humidity_sensor.close()
            logger.info("Humidity sensor configured for environmental monitoring")
            return True
            
        except Exception as e:
            logger.error(f"Failed to configure humidity sensor: {e}")
            return False
    
    def _calibrate_pressure_sensor(self, pressure_sensor, sensor_info: SensorInfo) -> bool:
        """Calibrate pressure sensor for accurate altitude readings."""
        logger.info("Calibrating pressure sensor for altitude monitoring...")
        
        try:
            # Collect calibration samples
            samples = []
            sample_count = self.config['sensor_calibration']['calibration_samples']
            
            logger.info(f"Collecting {sample_count} calibration samples...")
            
            for i in range(sample_count):
                pressure = pressure_sensor.getPressure()
                samples.append(pressure)
                time.sleep(0.1)
                
                if i % 20 == 0:
                    logger.info(f"Calibration progress: {i}/{sample_count} samples")
            
            # Calculate calibration statistics
            avg_pressure = sum(samples) / len(samples)
            min_pressure = min(samples)
            max_pressure = max(samples)
            std_dev = (sum((x - avg_pressure) ** 2 for x in samples) / len(samples)) ** 0.5
            
            # Store calibration data
            calibration_data = {
                'timestamp': datetime.now().isoformat(),
                'sample_count': len(samples),
                'average_pressure': avg_pressure,
                'min_pressure': min_pressure,
                'max_pressure': max_pressure,
                'standard_deviation': std_dev,
                'sea_level_pressure': 101.325,  # Standard sea level pressure
                'calibration_altitude': 0  # Assume calibrating at known altitude
            }
            
            self.calibration_data[sensor_info.device_id] = calibration_data
            
            logger.info(f"Pressure sensor calibration complete. "
                       f"Average pressure: {avg_pressure:.2f} kPa, "
                       f"Std dev: {std_dev:.3f} kPa")
            
            return True
            
        except Exception as e:
            logger.error(f"Pressure sensor calibration failed: {e}")
            return False
    
    def _calibrate_acceleration_sensor(self, accel_sensor, sensor_info: SensorInfo) -> bool:
        """Calibrate accelerometer for deployment detection."""
        logger.info("Calibrating accelerometer for deployment detection...")
        
        try:
            # Collect static calibration samples (device at rest)
            samples_x, samples_y, samples_z = [], [], []
            sample_count = 50  # Smaller sample count for accelerometer
            
            logger.info(f"Collecting {sample_count} static calibration samples...")
            
            for i in range(sample_count):
                acceleration = accel_sensor.getAcceleration()
                samples_x.append(acceleration[0])
                samples_y.append(acceleration[1])
                samples_z.append(acceleration[2])
                time.sleep(0.02)  # 50 Hz sampling
            
            # Calculate static offsets
            offset_x = sum(samples_x) / len(samples_x)
            offset_y = sum(samples_y) / len(samples_y)
            offset_z = sum(samples_z) / len(samples_z) - 1.0  # Subtract 1g for gravity
            
            # Store calibration data
            calibration_data = {
                'timestamp': datetime.now().isoformat(),
                'sample_count': len(samples_x),
                'static_offsets': {
                    'x': offset_x,
                    'y': offset_y,
                    'z': offset_z
                },
                'gravity_reference': 1.0,
                'deployment_threshold': 2.0,
                'impact_threshold': 5.0
            }
            
            self.calibration_data[sensor_info.device_id] = calibration_data
            
            logger.info(f"Accelerometer calibration complete. "
                       f"Offsets: X={offset_x:.3f}g, Y={offset_y:.3f}g, Z={offset_z:.3f}g")
            
            return True
            
        except Exception as e:
            logger.error(f"Accelerometer calibration failed: {e}")
            return False
    
    def run_full_discovery_and_configuration(self) -> Dict[str, List[SensorInfo]]:
        """
        Run complete discovery and configuration process for CT-084 system.
        
        Returns:
            Dictionary mapping hub serial numbers to configured sensor lists
        """
        logger.info("Starting full CT-084 sensor discovery and configuration...")
        
        configured_sensors = {}
        
        # Step 1: Discover Phidget hubs
        discovered_hubs = self.discover_phidget_hubs()
        
        if not discovered_hubs:
            logger.error("No Phidget hubs discovered. Check USB connections.")
            return configured_sensors
        
        # Step 2: Scan each hub for sensors
        for hub_info in discovered_hubs:
            logger.info(f"Scanning hub {hub_info.serial_number} for sensors...")
            hub_sensors = []
            
            for port in range(hub_info.port_count):
                logger.info(f"Checking port {port} on hub {hub_info.serial_number}")
                
                # Identify sensor type
                sensor_type, device_info = self.identify_sensor_type(
                    port, hub_info.serial_number
                )
                
                if sensor_type != SensorType.UNKNOWN:
                    # Create sensor info object
                    sensor_info = SensorInfo(
                        device_id=f"{hub_info.serial_number}_port_{port}",
                        sensor_type=sensor_type,
                        hub_port=port,
                        serial_number=device_info.get('serial_number', 'unknown'),
                        device_name=device_info.get('device_name', 'unknown'),
                        version=device_info.get('version', 'unknown'),
                        channel_count=device_info.get('channel_count', 1),
                        calibration_status="uncalibrated",
                        timestamp=datetime.now().isoformat()
                    )
                    
                    # Auto-configure the sensor
                    if self.auto_configure_sensor(sensor_info):
                        hub_sensors.append(sensor_info)
                        self.active_sensors[sensor_info.device_id] = sensor_info
                        logger.info(f"Successfully configured {sensor_type.value} "
                                  f"sensor on port {port}")
                    else:
                        logger.warning(f"Failed to configure {sensor_type.value} "
                                     f"sensor on port {port}")
                else:
                    logger.info(f"No sensor detected on port {port}")
            
            # Update hub info with connected sensors
            hub_info.connected_sensors = hub_sensors
            configured_sensors[hub_info.serial_number] = hub_sensors
        
        # Step 3: Generate configuration summary
        self._generate_configuration_report(configured_sensors)
        
        logger.info(f"CT-084 sensor configuration complete. "
                   f"Configured {sum(len(sensors) for sensors in configured_sensors.values())} sensors.")
        
        return configured_sensors
    
    def _generate_configuration_report(self, configured_sensors: Dict[str, List[SensorInfo]]):
        """Generate comprehensive configuration report for CT-084 system."""
        report = {
            'timestamp': datetime.now().isoformat(),
            'system': 'CT-084 Parachute Drop System',
            'configuration_version': '1.0.0',
            'total_hubs': len(configured_sensors),
            'total_sensors': sum(len(sensors) for sensors in configured_sensors.values()),
            'hubs': {}
        }
        
        for hub_serial, sensors in configured_sensors.items():
            hub_report = {
                'hub_serial': hub_serial,
                'sensor_count': len(sensors),
                'sensors': []
            }
            
            for sensor in sensors:
                sensor_report = {
                    'device_id': sensor.device_id,
                    'type': sensor.sensor_type.value,
                    'port': sensor.hub_port,
                    'device_name': sensor.device_name,
                    'calibration_status': sensor.calibration_status,
                    'configuration': sensor.configuration,
                    'opcua_namespace': f"CT084_ParachuteDrop.{sensor.sensor_type.value}.Port_{sensor.hub_port}"
                }
                hub_report['sensors'].append(sensor_report)
            
            report['hubs'][hub_serial] = hub_report
        
        # Save report to file
        report_file = '/var/log/ct-084/configuration_report.json'
        os.makedirs(os.path.dirname(report_file), exist_ok=True)
        
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"Configuration report saved to {report_file}")
        
        # Print summary to console
        print("\n" + "="*60)
        print("CT-084 PARACHUTE DROP SYSTEM - SENSOR CONFIGURATION REPORT")
        print("="*60)
        print(f"Configuration Date: {report['timestamp']}")
        print(f"Total Hubs: {report['total_hubs']}")
        print(f"Total Sensors: {report['total_sensors']}")
        print()
        
        for hub_serial, hub_data in report['hubs'].items():
            print(f"Hub: {hub_serial}")
            print(f"  Sensors: {hub_data['sensor_count']}")
            for sensor in hub_data['sensors']:
                print(f"    Port {sensor['port']}: {sensor['type']} ({sensor['device_name']})")
                print(f"      Status: {sensor['calibration_status']}")
            print()
        
        print("Configuration complete. System ready for deployment.")
        print("="*60)

def main():
    """Main entry point for CT-084 Phidget Auto-Configurator."""
    print("CT-084 Parachute Drop System - Phidget Auto-Configurator")
    print("Starting automatic sensor detection and configuration...\n")
    
    # Initialize configurator
    configurator = PhidgetAutoConfigurator()
    
    # Run full discovery and configuration
    configured_sensors = configurator.run_full_discovery_and_configuration()
    
    if configured_sensors:
        print(f"\nConfiguration successful! {sum(len(sensors) for sensors in configured_sensors.values())} sensors configured.")
        print("See /var/log/ct-084/configuration_report.json for detailed report.")
    else:
        print("\nConfiguration failed! No sensors were configured.")
        print("Check hardware connections and Phidget library installation.")

if __name__ == "__main__":
    main()