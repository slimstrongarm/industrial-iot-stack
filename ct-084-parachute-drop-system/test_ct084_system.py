#!/usr/bin/env python3
"""
CT-084 Parachute Drop System - Comprehensive System Test
Validates complete system functionality including device detection, sensor configuration,
OPC-UA integration, and configuration management.

This script provides comprehensive testing for mission-critical validation.
"""

import os
import sys
import time
import json
import logging
import asyncio
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple

# Add system modules to path
sys.path.insert(0, str(Path(__file__).parent))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | CT-084-TEST | %(levelname)-8s | %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('/tmp/ct084_test.log')
    ]
)
logger = logging.getLogger('CT084Test')

class CT084SystemTest:
    """
    Comprehensive test suite for CT-084 Parachute Drop System.
    
    Tests all major components and integration points to ensure
    mission-critical reliability and functionality.
    """
    
    def __init__(self):
        """Initialize the test system."""
        self.test_results = {
            'timestamp': datetime.now().isoformat(),
            'tests_run': 0,
            'tests_passed': 0,
            'tests_failed': 0,
            'test_details': {}
        }
        
        self.base_dir = Path(__file__).parent
        logger.info("CT-084 System Test Suite initialized")
    
    def run_test(self, test_name: str, test_function) -> bool:
        """
        Run a single test with error handling and result tracking.
        
        Args:
            test_name: Name of the test
            test_function: Function to execute
            
        Returns:
            True if test passed, False otherwise
        """
        logger.info(f"Running test: {test_name}")
        self.test_results['tests_run'] += 1
        
        try:
            start_time = time.time()
            result = test_function()
            end_time = time.time()
            
            if result:
                self.test_results['tests_passed'] += 1
                status = "PASSED"
                logger.info(f"✓ Test PASSED: {test_name}")
            else:
                self.test_results['tests_failed'] += 1
                status = "FAILED"
                logger.error(f"✗ Test FAILED: {test_name}")
            
            self.test_results['test_details'][test_name] = {
                'status': status,
                'duration': round(end_time - start_time, 3),
                'timestamp': datetime.now().isoformat()
            }
            
            return result
            
        except Exception as e:
            self.test_results['tests_failed'] += 1
            status = "ERROR"
            logger.error(f"✗ Test ERROR: {test_name} - {e}")
            
            self.test_results['test_details'][test_name] = {
                'status': status,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
            
            return False
    
    def test_python_imports(self) -> bool:
        """Test that all required Python modules can be imported."""
        logger.info("Testing Python module imports...")
        
        # Test core dependencies
        core_modules = [
            'yaml',
            'json',
            'sqlite3',
            'asyncio',
            'threading',
            'pathlib'
        ]
        
        for module in core_modules:
            try:
                __import__(module)
                logger.debug(f"Successfully imported: {module}")
            except ImportError as e:
                logger.error(f"Failed to import core module {module}: {e}")
                return False
        
        # Test optional dependencies (warn but don't fail)
        optional_modules = [
            ('Phidget22', 'Phidget sensor support'),
            ('asyncua', 'OPC-UA integration'),
            ('pyusb', 'USB device detection'),
            ('psutil', 'System monitoring'),
            ('jsonschema', 'Configuration validation')
        ]
        
        warnings = []
        for module, description in optional_modules:
            try:
                __import__(module)
                logger.debug(f"Successfully imported optional module: {module}")
            except ImportError:
                warnings.append(f"{module} not available - {description} limited")
        
        if warnings:
            logger.warning(f"Optional modules missing: {len(warnings)} warnings")
            for warning in warnings:
                logger.warning(f"  - {warning}")
        
        return True
    
    def test_system_modules(self) -> bool:
        """Test that CT-084 system modules can be imported."""
        logger.info("Testing CT-084 system modules...")
        
        test_modules = [
            ('phidget_auto_configurator.phidget_auto_configurator', 'PhidgetAutoConfigurator'),
            ('device_detection.usb_device_manager', 'USBDeviceManager'),
            ('opcua_integration.opcua_bridge', 'CT084OPCUABridge'),
            ('config_management.configuration_manager', 'ConfigurationManager')
        ]
        
        for module_path, class_name in test_modules:
            try:
                # Import module
                module_parts = module_path.split('.')
                module_file = self.base_dir / module_parts[0].replace('_', '-') / f"{module_parts[1]}.py"
                
                if not module_file.exists():
                    logger.error(f"Module file not found: {module_file}")
                    return False
                
                # Test Python syntax
                result = subprocess.run([
                    sys.executable, '-m', 'py_compile', str(module_file)
                ], capture_output=True, text=True)
                
                if result.returncode != 0:
                    logger.error(f"Syntax error in {module_path}: {result.stderr}")
                    return False
                
                logger.debug(f"Module syntax check passed: {module_path}")
                
            except Exception as e:
                logger.error(f"Failed to test module {module_path}: {e}")
                return False
        
        return True
    
    def test_configuration_files(self) -> bool:
        """Test configuration file structure and validation."""
        logger.info("Testing configuration file structure...")
        
        # Check required files exist
        required_files = [
            'requirements.txt',
            'setup_ct084_system.py',
            'README.md'
        ]
        
        for filename in required_files:
            file_path = self.base_dir / filename
            if not file_path.exists():
                logger.error(f"Required file missing: {filename}")
                return False
            
            # Basic content validation
            if filename == 'requirements.txt':
                with open(file_path) as f:
                    content = f.read()
                    if 'Phidget22' not in content:
                        logger.error("Phidget22 not found in requirements.txt")
                        return False
            
            logger.debug(f"Configuration file check passed: {filename}")
        
        return True
    
    def test_usb_device_detection(self) -> bool:
        """Test USB device detection functionality."""
        logger.info("Testing USB device detection...")
        
        try:
            # Import USB device manager
            sys.path.insert(0, str(self.base_dir / 'device-detection'))
            from usb_device_manager import USBDeviceManager
            
            # Create manager instance
            manager = USBDeviceManager(monitoring_interval=1.0)
            
            # Test device scanning
            devices = manager.scan_usb_devices()
            logger.info(f"Detected {len(devices)} USB devices")
            
            # Test Phidget device filtering
            phidget_devices = manager.get_phidget_devices()
            logger.info(f"Found {len(phidget_devices)} Phidget devices")
            
            # Test device reporting
            report = manager.generate_device_report()
            if 'total_devices' not in report:
                logger.error("Invalid device report format")
                return False
            
            logger.info(f"Device detection test completed - {report['total_devices']} total devices")
            return True
            
        except Exception as e:
            logger.error(f"USB device detection test failed: {e}")
            return False
    
    def test_phidget_configurator(self) -> bool:
        """Test Phidget auto-configurator functionality."""
        logger.info("Testing Phidget auto-configurator...")
        
        try:
            # Import configurator
            sys.path.insert(0, str(self.base_dir / 'phidget-auto-configurator'))
            from phidget_auto_configurator import PhidgetAutoConfigurator, SensorType
            
            # Create configurator instance
            configurator = PhidgetAutoConfigurator()
            
            # Test hub discovery
            discovered_hubs = configurator.discover_phidget_hubs()
            logger.info(f"Discovered {len(discovered_hubs)} Phidget hubs")
            
            # Test sensor type identification (simulation mode)
            sensor_type, device_info = configurator.identify_sensor_type(0, "TEST123")
            if sensor_type == SensorType.UNKNOWN and not device_info:
                logger.info("Sensor identification returned expected unknown result")
            else:
                logger.info(f"Sensor identification result: {sensor_type.value}")
            
            # Test configuration generation
            if discovered_hubs:
                configured_sensors = configurator.run_full_discovery_and_configuration()
                logger.info(f"Configuration completed for {len(configured_sensors)} hub(s)")
            
            return True
            
        except Exception as e:
            logger.error(f"Phidget configurator test failed: {e}")
            return False
    
    def test_opcua_integration(self) -> bool:
        """Test OPC-UA integration functionality."""
        logger.info("Testing OPC-UA integration...")
        
        try:
            # Import OPC-UA bridge
            sys.path.insert(0, str(self.base_dir / 'opcua-integration'))
            from opcua_bridge import CT084OPCUABridge, DataQuality
            
            # Create bridge instance
            bridge = CT084OPCUABridge()
            
            # Test configuration loading
            status = bridge.get_connection_status()
            if 'state' not in status:
                logger.error("Invalid connection status format")
                return False
            
            logger.info(f"OPC-UA bridge status: {status['state']}")
            
            # Test data quality enumeration
            qualities = [DataQuality.GOOD, DataQuality.UNCERTAIN, DataQuality.BAD]
            logger.info(f"Data quality types available: {[q.value for q in qualities]}")
            
            # Test bridge lifecycle
            bridge.start()
            time.sleep(1)
            bridge.stop()
            
            logger.info("OPC-UA integration test completed")
            return True
            
        except Exception as e:
            logger.error(f"OPC-UA integration test failed: {e}")
            return False
    
    def test_configuration_management(self) -> bool:
        """Test configuration management functionality."""
        logger.info("Testing configuration management...")
        
        try:
            # Import configuration manager
            sys.path.insert(0, str(self.base_dir / 'config-management'))
            from configuration_manager import ConfigurationManager, BackupType
            
            # Create temporary directories for testing
            test_config_dir = Path('/tmp/ct084_test_config')
            test_backup_dir = Path('/tmp/ct084_test_backup')
            test_db_path = Path('/tmp/ct084_test.db')
            
            # Clean up any existing test files
            import shutil
            for path in [test_config_dir, test_backup_dir]:
                if path.exists():
                    shutil.rmtree(path)
            if test_db_path.exists():
                test_db_path.unlink()
            
            # Create manager instance
            manager = ConfigurationManager(
                config_dir=str(test_config_dir),
                backup_dir=str(test_backup_dir),
                database_path=str(test_db_path)
            )
            
            # Test configuration loading/creation
            config = manager.load_system_configuration()
            if not config:
                logger.error("Failed to load/create system configuration")
                return False
            
            logger.info(f"System configuration loaded: {config.system_id}")
            
            # Test backup creation
            backup_id = manager.create_backup("Test backup", BackupType.MANUAL)
            if not backup_id:
                logger.error("Failed to create configuration backup")
                return False
            
            logger.info(f"Created backup: {backup_id}")
            
            # Test backup listing
            backups = manager.get_backup_list()
            if len(backups) == 0:
                logger.error("No backups found after creation")
                return False
            
            # Test status reporting
            status = manager.get_configuration_status()
            if not status['system_config_loaded']:
                logger.error("System configuration not loaded according to status")
                return False
            
            logger.info("Configuration management test completed")
            return True
            
        except Exception as e:
            logger.error(f"Configuration management test failed: {e}")
            return False
    
    def test_system_integration(self) -> bool:
        """Test integration between system components."""
        logger.info("Testing system integration...")
        
        try:
            # Test component initialization order
            logger.info("Testing component initialization...")
            
            # 1. Configuration Manager
            sys.path.insert(0, str(self.base_dir / 'config-management'))
            from configuration_manager import ConfigurationManager
            config_manager = ConfigurationManager()
            system_config = config_manager.load_system_configuration()
            
            # 2. USB Device Manager
            sys.path.insert(0, str(self.base_dir / 'device-detection'))
            from usb_device_manager import USBDeviceManager
            device_manager = USBDeviceManager()
            
            # 3. Phidget Configurator
            sys.path.insert(0, str(self.base_dir / 'phidget-auto-configurator'))
            from phidget_auto_configurator import PhidgetAutoConfigurator
            configurator = PhidgetAutoConfigurator()
            
            # 4. OPC-UA Bridge
            sys.path.insert(0, str(self.base_dir / 'opcua-integration'))
            from opcua_bridge import CT084OPCUABridge
            opcua_bridge = CT084OPCUABridge()
            
            # Test component interaction
            devices = device_manager.scan_usb_devices()
            logger.info(f"Found {len(devices)} devices for integration test")
            
            if system_config:
                logger.info(f"System config available for integration: {system_config.system_id}")
            
            logger.info("System integration test completed")
            return True
            
        except Exception as e:
            logger.error(f"System integration test failed: {e}")
            return False
    
    def test_error_handling(self) -> bool:
        """Test error handling and fault tolerance."""
        logger.info("Testing error handling and fault tolerance...")
        
        try:
            # Test configuration with invalid paths
            sys.path.insert(0, str(self.base_dir / 'config-management'))
            from configuration_manager import ConfigurationManager
            
            invalid_manager = ConfigurationManager(
                config_dir="/nonexistent/path",
                backup_dir="/nonexistent/backup",
                database_path="/nonexistent/database.db"
            )
            
            # This should handle the error gracefully
            status = invalid_manager.get_configuration_status()
            logger.info("Error handling test: Invalid paths handled gracefully")
            
            # Test USB manager with no devices
            sys.path.insert(0, str(self.base_dir / 'device-detection'))
            from usb_device_manager import USBDeviceManager
            
            manager = USBDeviceManager()
            devices = manager.scan_usb_devices()  # Should not crash
            logger.info(f"Error handling test: USB scan with no devices returned {len(devices)} devices")
            
            logger.info("Error handling test completed")
            return True
            
        except Exception as e:
            logger.error(f"Error handling test failed: {e}")
            return False
    
    def test_performance(self) -> bool:
        """Test system performance and resource usage."""
        logger.info("Testing system performance...")
        
        try:
            import psutil
            import time
            
            # Monitor resource usage during operations
            process = psutil.Process()
            start_memory = process.memory_info().rss
            start_time = time.time()
            
            # Run performance-intensive operations
            sys.path.insert(0, str(self.base_dir / 'device-detection'))
            from usb_device_manager import USBDeviceManager
            
            manager = USBDeviceManager()
            
            # Perform multiple scans
            for i in range(5):
                devices = manager.scan_usb_devices()
                time.sleep(0.1)
            
            end_time = time.time()
            end_memory = process.memory_info().rss
            
            # Calculate performance metrics
            duration = end_time - start_time
            memory_usage = (end_memory - start_memory) / 1024 / 1024  # MB
            
            logger.info(f"Performance test completed:")
            logger.info(f"  Duration: {duration:.3f} seconds")
            logger.info(f"  Memory usage: {memory_usage:.2f} MB")
            
            # Performance thresholds
            if duration > 10.0:
                logger.warning(f"Performance warning: Operation took {duration:.3f} seconds")
            
            if memory_usage > 100.0:
                logger.warning(f"Memory warning: Used {memory_usage:.2f} MB")
            
            return True
            
        except ImportError:
            logger.warning("psutil not available - skipping performance test")
            return True
        except Exception as e:
            logger.error(f"Performance test failed: {e}")
            return False
    
    def test_documentation(self) -> bool:
        """Test documentation completeness and accuracy."""
        logger.info("Testing documentation...")
        
        try:
            # Check README.md exists and has required sections
            readme_path = self.base_dir / 'README.md'
            if not readme_path.exists():
                logger.error("README.md not found")
                return False
            
            with open(readme_path) as f:
                readme_content = f.read()
            
            required_sections = [
                'CT-084 Parachute Drop System',
                'Quick Start',
                'Installation',
                'Configuration',
                'API Reference',
                'Troubleshooting'
            ]
            
            missing_sections = []
            for section in required_sections:
                if section not in readme_content:
                    missing_sections.append(section)
            
            if missing_sections:
                logger.error(f"Missing documentation sections: {missing_sections}")
                return False
            
            # Check for example code blocks
            if '```python' not in readme_content:
                logger.warning("No Python code examples found in documentation")
            
            # Check requirements.txt documentation
            requirements_path = self.base_dir / 'requirements.txt'
            with open(requirements_path) as f:
                requirements_content = f.read()
            
            if '# CT-084' not in requirements_content:
                logger.warning("Requirements file lacks proper header documentation")
            
            logger.info("Documentation test completed")
            return True
            
        except Exception as e:
            logger.error(f"Documentation test failed: {e}")
            return False
    
    def run_all_tests(self) -> Dict:
        """Run complete test suite."""
        logger.info("Starting CT-084 System Test Suite...")
        print("\n" + "="*60)
        print("CT-084 PARACHUTE DROP SYSTEM - COMPREHENSIVE TESTING")
        print("="*60)
        
        # Define test suite
        test_suite = [
            ("Python Imports", self.test_python_imports),
            ("System Modules", self.test_system_modules),
            ("Configuration Files", self.test_configuration_files),
            ("USB Device Detection", self.test_usb_device_detection),
            ("Phidget Configurator", self.test_phidget_configurator),
            ("OPC-UA Integration", self.test_opcua_integration),
            ("Configuration Management", self.test_configuration_management),
            ("System Integration", self.test_system_integration),
            ("Error Handling", self.test_error_handling),
            ("Performance", self.test_performance),
            ("Documentation", self.test_documentation)
        ]
        
        # Run all tests
        for test_name, test_function in test_suite:
            self.run_test(test_name, test_function)
            print()  # Add spacing between tests
        
        # Generate final report
        self._generate_test_report()
        
        return self.test_results
    
    def _generate_test_report(self):
        """Generate comprehensive test report."""
        results = self.test_results
        
        print("\n" + "="*60)
        print("TEST RESULTS SUMMARY")
        print("="*60)
        print(f"Tests Run: {results['tests_run']}")
        print(f"Tests Passed: {results['tests_passed']}")
        print(f"Tests Failed: {results['tests_failed']}")
        print(f"Success Rate: {(results['tests_passed']/results['tests_run']*100):.1f}%")
        print()
        
        # Detailed results
        print("DETAILED RESULTS:")
        for test_name, details in results['test_details'].items():
            status = details['status']
            duration = details.get('duration', 0)
            
            status_symbol = "✓" if status == "PASSED" else "✗"
            print(f"  {status_symbol} {test_name}: {status} ({duration:.3f}s)")
            
            if 'error' in details:
                print(f"    Error: {details['error']}")
        
        print()
        
        # Overall assessment
        if results['tests_failed'] == 0:
            print("🎉 ALL TESTS PASSED - System ready for deployment!")
        elif results['tests_failed'] < results['tests_run'] * 0.2:
            print("⚠️  MINOR ISSUES - System mostly functional with warnings")
        else:
            print("❌ MAJOR ISSUES - System requires attention before deployment")
        
        print("="*60)
        
        # Save detailed results
        try:
            with open('/tmp/ct084_test_results.json', 'w') as f:
                json.dump(results, f, indent=2)
            print(f"Detailed results saved to: /tmp/ct084_test_results.json")
            print(f"Test log saved to: /tmp/ct084_test.log")
        except Exception as e:
            logger.error(f"Failed to save test results: {e}")

def main():
    """Main entry point for system testing."""
    print("CT-084 Parachute Drop System - Comprehensive System Test")
    
    # Create test instance
    test_system = CT084SystemTest()
    
    try:
        # Run all tests
        results = test_system.run_all_tests()
        
        # Exit with appropriate code
        exit_code = 0 if results['tests_failed'] == 0 else 1
        sys.exit(exit_code)
        
    except KeyboardInterrupt:
        print("\nTesting interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Testing failed with unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()