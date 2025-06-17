#!/usr/bin/env python3
"""
CT-084 Parachute Drop System - USB Device Manager
Handles automatic USB device detection, enumeration, and management for Phidget sensors.

This module provides robust USB device handling with hot-plug support,
device failure recovery, and comprehensive device state monitoring.
"""

import os
import sys
import time
import json
import logging
import threading
import subprocess
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from enum import Enum
import platform

# USB detection libraries
try:
    import usb.core
    import usb.util
    USB_AVAILABLE = True
except ImportError:
    USB_AVAILABLE = False
    logging.warning("pyusb library not available. USB detection limited.")

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False
    logging.warning("psutil library not available. System monitoring limited.")

# Configure logging
logger = logging.getLogger('USBDeviceManager')

class DeviceState(Enum):
    """USB device connection states."""
    DISCONNECTED = "disconnected"
    CONNECTING = "connecting"
    CONNECTED = "connected"
    ERROR = "error"
    UNKNOWN = "unknown"

class PhidgetDeviceType(Enum):
    """Known Phidget device types by USB VID/PID."""
    VINT_HUB = "vint_hub"
    INTERFACEKIT = "interfacekit"
    TEMPERATURE_SENSOR = "temperature_sensor"
    PRESSURE_SENSOR = "pressure_sensor"
    UNKNOWN_PHIDGET = "unknown_phidget"
    NON_PHIDGET = "non_phidget"

@dataclass
class USBDeviceInfo:
    """Container for USB device information."""
    vendor_id: str
    product_id: str
    device_path: str
    manufacturer: str
    product_name: str
    serial_number: str
    device_type: PhidgetDeviceType
    connection_state: DeviceState
    first_seen: str
    last_seen: str
    connection_count: int = 0
    error_count: int = 0
    last_error: Optional[str] = None

class USBDeviceManager:
    """
    Manages USB device detection and monitoring for CT-084 Phidget integration.
    
    Provides automatic device discovery, hot-plug support, and device state management
    with robust error handling and recovery mechanisms.
    """
    
    # Known Phidget USB vendor IDs
    PHIDGET_VENDOR_IDS = {
        0x06C2: "Phidgets Inc.",
        0x0925: "Phidgets Inc. (Legacy)"
    }
    
    # Known Phidget device product IDs
    PHIDGET_PRODUCT_IDS = {
        0x0030: PhidgetDeviceType.VINT_HUB,
        0x0031: PhidgetDeviceType.VINT_HUB,
        0x0032: PhidgetDeviceType.VINT_HUB,
        0x0040: PhidgetDeviceType.INTERFACEKIT,
        0x0041: PhidgetDeviceType.INTERFACEKIT,
        0x0051: PhidgetDeviceType.TEMPERATURE_SENSOR,
        0x0052: PhidgetDeviceType.PRESSURE_SENSOR
    }
    
    def __init__(self, monitoring_interval: float = 2.0):
        """
        Initialize USB device manager.
        
        Args:
            monitoring_interval: Time between device scans in seconds
        """
        self.monitoring_interval = monitoring_interval
        self.detected_devices: Dict[str, USBDeviceInfo] = {}
        self.monitoring_active = False
        self.monitoring_thread = None
        self.device_callbacks: Dict[str, List] = {
            'on_device_connected': [],
            'on_device_disconnected': [],
            'on_device_error': []
        }
        
        logger.info("USB Device Manager initialized for CT-084 system")
    
    def scan_usb_devices(self) -> List[USBDeviceInfo]:
        """
        Scan for all USB devices and identify Phidget devices.
        
        Returns:
            List of detected USB device information
        """
        logger.debug("Scanning USB devices...")
        detected_devices = []
        
        if not USB_AVAILABLE:
            # Fallback to system commands
            return self._scan_devices_fallback()
        
        try:
            # Find all USB devices
            devices = usb.core.find(find_all=True)
            
            for device in devices:
                try:
                    device_info = self._extract_device_info(device)
                    if device_info:
                        detected_devices.append(device_info)
                        
                except Exception as e:
                    logger.warning(f"Failed to process USB device: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"USB scan failed: {e}")
            # Try fallback method
            return self._scan_devices_fallback()
        
        logger.info(f"USB scan complete. Found {len(detected_devices)} devices, "
                   f"{len([d for d in detected_devices if d.device_type != PhidgetDeviceType.NON_PHIDGET])} Phidgets")
        
        return detected_devices
    
    def _extract_device_info(self, usb_device) -> Optional[USBDeviceInfo]:
        """Extract information from a USB device object."""
        try:
            vendor_id = usb_device.idVendor
            product_id = usb_device.idProduct
            
            # Get device strings (may require device access)
            try:
                manufacturer = usb.util.get_string(usb_device, usb_device.iManufacturer) or "Unknown"
                product_name = usb.util.get_string(usb_device, usb_device.iProduct) or "Unknown"
                serial_number = usb.util.get_string(usb_device, usb_device.iSerialNumber) or "Unknown"
            except:
                # Device access may be restricted
                manufacturer = self.PHIDGET_VENDOR_IDS.get(vendor_id, "Unknown")
                product_name = f"USB Device {product_id:04X}"
                serial_number = f"{vendor_id:04X}:{product_id:04X}"
            
            # Determine device type
            device_type = self._identify_device_type(vendor_id, product_id)
            
            # Skip non-Phidget devices unless debugging
            if device_type == PhidgetDeviceType.NON_PHIDGET:
                return None
            
            device_path = f"/dev/bus/usb/{usb_device.bus:03d}/{usb_device.address:03d}"
            device_id = f"{vendor_id:04X}:{product_id:04X}:{serial_number}"
            
            return USBDeviceInfo(
                vendor_id=f"{vendor_id:04X}",
                product_id=f"{product_id:04X}",
                device_path=device_path,
                manufacturer=manufacturer,
                product_name=product_name,
                serial_number=serial_number,
                device_type=device_type,
                connection_state=DeviceState.CONNECTED,
                first_seen=datetime.now().isoformat(),
                last_seen=datetime.now().isoformat()
            )
            
        except Exception as e:
            logger.error(f"Failed to extract device info: {e}")
            return None
    
    def _identify_device_type(self, vendor_id: int, product_id: int) -> PhidgetDeviceType:
        """Identify Phidget device type based on VID/PID."""
        if vendor_id not in self.PHIDGET_VENDOR_IDS:
            return PhidgetDeviceType.NON_PHIDGET
        
        return self.PHIDGET_PRODUCT_IDS.get(product_id, PhidgetDeviceType.UNKNOWN_PHIDGET)
    
    def _scan_devices_fallback(self) -> List[USBDeviceInfo]:
        """Fallback USB device scanning using system commands."""
        logger.info("Using fallback USB device scanning")
        detected_devices = []
        
        try:
            if platform.system() == "Linux":
                # Use lsusb command
                result = subprocess.run(['lsusb'], capture_output=True, text=True)
                
                if result.returncode == 0:
                    for line in result.stdout.strip().split('\n'):
                        device_info = self._parse_lsusb_line(line)
                        if device_info:
                            detected_devices.append(device_info)
                            
        except Exception as e:
            logger.error(f"Fallback USB scan failed: {e}")
            
            # Create simulated devices for testing
            detected_devices = self._create_simulated_devices()
        
        return detected_devices
    
    def _parse_lsusb_line(self, line: str) -> Optional[USBDeviceInfo]:
        """Parse lsusb output line to extract device information."""
        try:
            # Example line: "Bus 001 Device 004: ID 06c2:0030 Phidgets Inc. VINT Hub"
            parts = line.split()
            if len(parts) < 6:
                return None
            
            id_part = parts[5]  # "06c2:0030"
            if ':' not in id_part:
                return None
            
            vendor_id_str, product_id_str = id_part.split(':')
            vendor_id = int(vendor_id_str, 16)
            product_id = int(product_id_str, 16)
            
            # Extract device name from remaining parts
            device_name = ' '.join(parts[6:]) if len(parts) > 6 else "Unknown"
            
            # Check if this is a Phidget device
            device_type = self._identify_device_type(vendor_id, product_id)
            if device_type == PhidgetDeviceType.NON_PHIDGET:
                return None
            
            bus = parts[1]
            device = parts[3].rstrip(':')
            device_path = f"/dev/bus/usb/{bus}/{device}"
            
            return USBDeviceInfo(
                vendor_id=f"{vendor_id:04X}",
                product_id=f"{product_id:04X}",
                device_path=device_path,
                manufacturer=self.PHIDGET_VENDOR_IDS.get(vendor_id, "Unknown"),
                product_name=device_name,
                serial_number=f"{vendor_id:04X}:{product_id:04X}",
                device_type=device_type,
                connection_state=DeviceState.CONNECTED,
                first_seen=datetime.now().isoformat(),
                last_seen=datetime.now().isoformat()
            )
            
        except Exception as e:
            logger.warning(f"Failed to parse lsusb line '{line}': {e}")
            return None
    
    def _create_simulated_devices(self) -> List[USBDeviceInfo]:
        """Create simulated Phidget devices for testing."""
        logger.info("Creating simulated Phidget devices for testing")
        
        simulated_devices = [
            USBDeviceInfo(
                vendor_id="06C2",
                product_id="0030",
                device_path="/dev/usb/sim001",
                manufacturer="Phidgets Inc.",
                product_name="VINT Hub (Simulated)",
                serial_number="SIM123456",
                device_type=PhidgetDeviceType.VINT_HUB,
                connection_state=DeviceState.CONNECTED,
                first_seen=datetime.now().isoformat(),
                last_seen=datetime.now().isoformat()
            ),
            USBDeviceInfo(
                vendor_id="06C2",
                product_id="0051",
                device_path="/dev/usb/sim002",
                manufacturer="Phidgets Inc.",
                product_name="Temperature Sensor (Simulated)",
                serial_number="SIM123457",
                device_type=PhidgetDeviceType.TEMPERATURE_SENSOR,
                connection_state=DeviceState.CONNECTED,
                first_seen=datetime.now().isoformat(),
                last_seen=datetime.now().isoformat()
            )
        ]
        
        return simulated_devices
    
    def start_monitoring(self):
        """Start continuous USB device monitoring."""
        if self.monitoring_active:
            logger.warning("USB monitoring already active")
            return
        
        self.monitoring_active = True
        self.monitoring_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
        self.monitoring_thread.start()
        
        logger.info("USB device monitoring started")
    
    def stop_monitoring(self):
        """Stop USB device monitoring."""
        if not self.monitoring_active:
            return
        
        self.monitoring_active = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=5)
        
        logger.info("USB device monitoring stopped")
    
    def _monitoring_loop(self):
        """Main monitoring loop for USB device changes."""
        logger.info("USB monitoring loop started")
        
        while self.monitoring_active:
            try:
                # Scan for current devices
                current_devices = self.scan_usb_devices()
                current_device_ids = set()
                
                # Process currently connected devices
                for device in current_devices:
                    device_id = f"{device.vendor_id}:{device.product_id}:{device.serial_number}"
                    current_device_ids.add(device_id)
                    
                    if device_id in self.detected_devices:
                        # Update existing device
                        existing_device = self.detected_devices[device_id]
                        existing_device.last_seen = datetime.now().isoformat()
                        existing_device.connection_state = DeviceState.CONNECTED
                    else:
                        # New device detected
                        device.connection_count = 1
                        self.detected_devices[device_id] = device
                        logger.info(f"New Phidget device detected: {device.product_name} ({device_id})")
                        self._trigger_callbacks('on_device_connected', device)
                
                # Check for disconnected devices
                for device_id, device in list(self.detected_devices.items()):
                    if device_id not in current_device_ids:
                        if device.connection_state == DeviceState.CONNECTED:
                            device.connection_state = DeviceState.DISCONNECTED
                            logger.warning(f"Phidget device disconnected: {device.product_name} ({device_id})")
                            self._trigger_callbacks('on_device_disconnected', device)
                
                time.sleep(self.monitoring_interval)
                
            except Exception as e:
                logger.error(f"Error in USB monitoring loop: {e}")
                time.sleep(self.monitoring_interval * 2)  # Back off on error
    
    def _trigger_callbacks(self, event_type: str, device: USBDeviceInfo):
        """Trigger registered callbacks for device events."""
        for callback in self.device_callbacks.get(event_type, []):
            try:
                callback(device)
            except Exception as e:
                logger.error(f"Error in {event_type} callback: {e}")
    
    def register_callback(self, event_type: str, callback):
        """
        Register a callback for device events.
        
        Args:
            event_type: Type of event ('on_device_connected', 'on_device_disconnected', 'on_device_error')
            callback: Function to call when event occurs
        """
        if event_type not in self.device_callbacks:
            logger.error(f"Unknown event type: {event_type}")
            return
        
        self.device_callbacks[event_type].append(callback)
        logger.info(f"Registered callback for {event_type}")
    
    def get_phidget_devices(self) -> List[USBDeviceInfo]:
        """Get list of all detected Phidget devices."""
        return [device for device in self.detected_devices.values() 
                if device.device_type != PhidgetDeviceType.NON_PHIDGET]
    
    def get_vint_hubs(self) -> List[USBDeviceInfo]:
        """Get list of detected VINT Hub devices."""
        return [device for device in self.detected_devices.values() 
                if device.device_type == PhidgetDeviceType.VINT_HUB]
    
    def get_device_by_serial(self, serial_number: str) -> Optional[USBDeviceInfo]:
        """Get device information by serial number."""
        for device in self.detected_devices.values():
            if device.serial_number == serial_number:
                return device
        return None
    
    def generate_device_report(self) -> Dict:
        """Generate comprehensive device status report."""
        report = {
            'timestamp': datetime.now().isoformat(),
            'total_devices': len(self.detected_devices),
            'connected_devices': len([d for d in self.detected_devices.values() 
                                    if d.connection_state == DeviceState.CONNECTED]),
            'phidget_devices': len(self.get_phidget_devices()),
            'vint_hubs': len(self.get_vint_hubs()),
            'devices': []
        }
        
        for device in self.detected_devices.values():
            device_report = {
                'vendor_id': device.vendor_id,
                'product_id': device.product_id,
                'manufacturer': device.manufacturer,
                'product_name': device.product_name,
                'serial_number': device.serial_number,
                'device_type': device.device_type.value,
                'connection_state': device.connection_state.value,
                'device_path': device.device_path,
                'first_seen': device.first_seen,
                'last_seen': device.last_seen,
                'connection_count': device.connection_count,
                'error_count': device.error_count,
                'last_error': device.last_error
            }
            report['devices'].append(device_report)
        
        return report
    
    def save_device_report(self, filepath: str = '/var/log/ct-084/usb_devices.json'):
        """Save device report to file."""
        try:
            report = self.generate_device_report()
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            with open(filepath, 'w') as f:
                json.dump(report, f, indent=2)
            
            logger.info(f"Device report saved to {filepath}")
            
        except Exception as e:
            logger.error(f"Failed to save device report: {e}")

def main():
    """Main entry point for USB device manager testing."""
    print("CT-084 USB Device Manager - Testing")
    print("Scanning for Phidget devices...\n")
    
    # Create device manager
    manager = USBDeviceManager()
    
    # Register event callbacks
    def on_device_connected(device):
        print(f"✓ Device Connected: {device.product_name} ({device.serial_number})")
    
    def on_device_disconnected(device):
        print(f"✗ Device Disconnected: {device.product_name} ({device.serial_number})")
    
    manager.register_callback('on_device_connected', on_device_connected)
    manager.register_callback('on_device_disconnected', on_device_disconnected)
    
    # Initial scan
    devices = manager.scan_usb_devices()
    
    print(f"Initial scan found {len(devices)} Phidget devices:")
    for device in devices:
        print(f"  - {device.product_name} ({device.device_type.value})")
        print(f"    Serial: {device.serial_number}")
        print(f"    Path: {device.device_path}")
        print()
    
    # Start monitoring
    manager.start_monitoring()
    
    try:
        print("Monitoring for device changes... (Press Ctrl+C to stop)")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping monitoring...")
        manager.stop_monitoring()
    
    # Generate final report
    print("\nFinal device report:")
    report = manager.generate_device_report()
    print(f"Total devices tracked: {report['total_devices']}")
    print(f"Currently connected: {report['connected_devices']}")

if __name__ == "__main__":
    main()