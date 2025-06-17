#!/usr/bin/env python3
"""
CT-084 Parachute Drop System - Setup and Installation Script
Automated setup for the complete Phidget auto-configurator system.

This script handles system installation, configuration, and deployment
for mission-critical parachute drop monitoring applications.
"""

import os
import sys
import subprocess
import logging
import platform
import shutil
import json
import yaml
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | CT-084-SETUP | %(levelname)-8s | %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('/tmp/ct084_setup.log')
    ]
)
logger = logging.getLogger('CT084Setup')

class CT084SystemSetup:
    """
    Complete system setup for CT-084 Parachute Drop System.
    
    Handles installation of dependencies, configuration of services,
    and deployment of the Phidget auto-configurator system.
    """
    
    def __init__(self):
        """Initialize the setup system."""
        self.system_name = "CT-084 Parachute Drop System"
        self.version = "1.0.0"
        self.base_dir = Path(__file__).parent
        self.install_dir = Path("/opt/ct-084")
        self.config_dir = Path("/etc/ct-084")
        self.log_dir = Path("/var/log/ct-084")
        self.data_dir = Path("/var/lib/ct-084")
        self.backup_dir = Path("/var/backups/ct-084")
        
        # Service configuration
        self.service_user = "ct084"
        self.service_group = "ct084"
        
        logger.info(f"Initializing {self.system_name} v{self.version} setup")
    
    def check_system_requirements(self) -> bool:
        """Check system requirements and compatibility."""
        logger.info("Checking system requirements...")
        
        # Check operating system
        if platform.system() not in ['Linux', 'Darwin']:
            logger.error(f"Unsupported operating system: {platform.system()}")
            return False
        
        # Check Python version
        python_version = sys.version_info
        if python_version < (3, 8):
            logger.error(f"Python 3.8+ required, found {python_version.major}.{python_version.minor}")
            return False
        
        # Check for required system packages
        required_packages = ['udev', 'libusb-1.0-0']
        missing_packages = []
        
        for package in required_packages:
            if not self._check_package_installed(package):
                missing_packages.append(package)
        
        if missing_packages:
            logger.warning(f"Missing system packages: {missing_packages}")
            logger.info("Install with: sudo apt-get install " + " ".join(missing_packages))
        
        # Check for USB access permissions
        if not self._check_usb_permissions():
            logger.warning("USB device access may require additional permissions")
            logger.info("Consider adding user to 'plugdev' group")
        
        logger.info("System requirements check completed")
        return True
    
    def _check_package_installed(self, package: str) -> bool:
        """Check if a system package is installed."""
        try:
            if platform.system() == 'Linux':
                result = subprocess.run(['dpkg', '-l', package], 
                                      capture_output=True, text=True)
                return result.returncode == 0
            elif platform.system() == 'Darwin':
                result = subprocess.run(['brew', 'list', package], 
                                      capture_output=True, text=True)
                return result.returncode == 0
        except FileNotFoundError:
            pass
        return False
    
    def _check_usb_permissions(self) -> bool:
        """Check USB device access permissions."""
        try:
            # Check if /dev/bus/usb exists and is accessible
            usb_path = Path('/dev/bus/usb')
            if usb_path.exists():
                return os.access(usb_path, os.R_OK)
        except:
            pass
        return False
    
    def install_python_dependencies(self) -> bool:
        """Install Python dependencies."""
        logger.info("Installing Python dependencies...")
        
        requirements_file = self.base_dir / "requirements.txt"
        
        if not requirements_file.exists():
            logger.error("requirements.txt not found")
            return False
        
        try:
            # Upgrade pip first
            subprocess.run([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'], 
                         check=True)
            
            # Install requirements
            subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', str(requirements_file)], 
                         check=True)
            
            logger.info("Python dependencies installed successfully")
            return True
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to install Python dependencies: {e}")
            return False
    
    def create_system_directories(self) -> bool:
        """Create system directories with proper permissions."""
        logger.info("Creating system directories...")
        
        directories = [
            self.install_dir,
            self.config_dir,
            self.log_dir,
            self.data_dir,
            self.backup_dir
        ]
        
        try:
            for directory in directories:
                directory.mkdir(parents=True, exist_ok=True)
                logger.info(f"Created directory: {directory}")
                
                # Set permissions (readable by service user)
                try:
                    os.chmod(directory, 0o755)
                except PermissionError:
                    logger.warning(f"Could not set permissions for {directory}")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to create directories: {e}")
            return False
    
    def create_service_user(self) -> bool:
        """Create dedicated service user for CT-084 system."""
        logger.info("Creating service user...")
        
        try:
            # Check if user already exists
            result = subprocess.run(['id', self.service_user], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info(f"Service user '{self.service_user}' already exists")
                return True
            
            # Create system user
            subprocess.run([
                'sudo', 'useradd', '--system', '--no-create-home',
                '--shell', '/bin/false', '--group', self.service_group,
                self.service_user
            ], check=True)
            
            # Add user to required groups
            subprocess.run([
                'sudo', 'usermod', '-a', '-G', 'plugdev,dialout', self.service_user
            ], check=True)
            
            logger.info(f"Service user '{self.service_user}' created")
            return True
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to create service user: {e}")
            return False
        except FileNotFoundError:
            logger.warning("Cannot create service user - sudo not available")
            return True  # Continue without dedicated user
    
    def install_system_files(self) -> bool:
        """Install system files to target directories."""
        logger.info("Installing system files...")
        
        try:
            # Copy Python modules
            module_dirs = [
                "phidget-auto-configurator",
                "device-detection", 
                "opcua-integration",
                "config-management"
            ]
            
            for module_dir in module_dirs:
                src_dir = self.base_dir / module_dir
                dst_dir = self.install_dir / module_dir
                
                if src_dir.exists():
                    shutil.copytree(src_dir, dst_dir, dirs_exist_ok=True)
                    logger.info(f"Installed module: {module_dir}")
                else:
                    logger.warning(f"Module directory not found: {module_dir}")
            
            # Copy additional files
            additional_files = [
                "requirements.txt",
                "README.md"
            ]
            
            for filename in additional_files:
                src_file = self.base_dir / filename
                dst_file = self.install_dir / filename
                
                if src_file.exists():
                    shutil.copy2(src_file, dst_file)
                    logger.info(f"Installed file: {filename}")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to install system files: {e}")
            return False
    
    def create_default_configurations(self) -> bool:
        """Create default configuration files."""
        logger.info("Creating default configuration files...")
        
        try:
            # Main system configuration
            system_config = {
                'system_id': 'CT-084-001',
                'configuration_version': '1.0.0',
                'created_timestamp': datetime.now().isoformat(),
                'last_modified': datetime.now().isoformat(),
                'devices': {},
                'opcua_settings': {
                    'endpoint': 'opc.tcp://localhost:4840/freeopcua/server/',
                    'namespace': 'CT084_ParachuteDrop',
                    'security_policy': 'None',
                    'auto_reconnect': True
                },
                'monitoring_settings': {
                    'scan_interval': 5.0,
                    'data_retention_days': 30,
                    'alert_enabled': True
                },
                'fault_tolerance': {
                    'enable_redundancy': True,
                    'max_connection_failures': 3,
                    'auto_recovery': True,
                    'store_and_forward': True
                },
                'mission_parameters': {
                    'deployment_altitude': 1000,
                    'critical_altitude': 500,
                    'max_descent_rate': 10,
                    'parachute_deployment_time': 30
                }
            }
            
            with open(self.config_dir / "system_configuration.yaml", 'w') as f:
                yaml.dump(system_config, f, default_flow_style=False, indent=2)
            
            # Phidget configuration
            phidget_config = {
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
                    'storage_path': str(self.log_dir / 'sensor_data'),
                    'retention_days': 30
                },
                'fault_tolerance': {
                    'enable_redundancy': True,
                    'sensor_timeout': 5,
                    'max_consecutive_failures': 3
                }
            }
            
            with open(self.config_dir / "phidget_config.yaml", 'w') as f:
                yaml.dump(phidget_config, f, default_flow_style=False, indent=2)
            
            # OPC-UA configuration
            opcua_config = {
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
                }
            }
            
            with open(self.config_dir / "opcua_config.yaml", 'w') as f:
                yaml.dump(opcua_config, f, default_flow_style=False, indent=2)
            
            logger.info("Default configuration files created")
            return True
            
        except Exception as e:
            logger.error(f"Failed to create configuration files: {e}")
            return False
    
    def create_systemd_service(self) -> bool:
        """Create systemd service for CT-084 system."""
        logger.info("Creating systemd service...")
        
        service_content = f"""[Unit]
Description=CT-084 Parachute Drop System - Phidget Auto Configurator
Documentation=https://github.com/your-org/ct-084-parachute-drop-system
After=network.target
Wants=network.target

[Service]
Type=simple
User={self.service_user}
Group={self.service_group}
WorkingDirectory={self.install_dir}
Environment=PYTHONPATH={self.install_dir}
ExecStart={sys.executable} -m phidget-auto-configurator.phidget_auto_configurator
ExecReload=/bin/kill -HUP $MAINPID
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal
SyslogIdentifier=ct084-system

# Security settings
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths={self.config_dir} {self.log_dir} {self.data_dir} {self.backup_dir}

[Install]
WantedBy=multi-user.target
"""
        
        try:
            service_file = Path("/etc/systemd/system/ct084-system.service")
            
            with open(service_file, 'w') as f:
                f.write(service_content)
            
            # Reload systemd
            subprocess.run(['sudo', 'systemctl', 'daemon-reload'], check=True)
            
            logger.info("Systemd service created: ct084-system.service")
            return True
            
        except Exception as e:
            logger.error(f"Failed to create systemd service: {e}")
            return False
    
    def setup_udev_rules(self) -> bool:
        """Setup udev rules for Phidget devices."""
        logger.info("Setting up udev rules...")
        
        udev_rules = """# CT-084 Parachute Drop System - Phidget Device Rules
# Phidgets Inc. devices
SUBSYSTEM=="usb", ATTRS{idVendor}=="06c2", MODE="0666", GROUP="plugdev"
SUBSYSTEM=="usb", ATTRS{idVendor}=="0925", MODE="0666", GROUP="plugdev"

# Phidget USB devices - specific handling
SUBSYSTEM=="usb", ATTRS{idVendor}=="06c2", ATTRS{idProduct}=="0030", SYMLINK+="phidget_vint_hub_%n"
SUBSYSTEM=="usb", ATTRS{idVendor}=="06c2", ATTRS{idProduct}=="0031", SYMLINK+="phidget_vint_hub_%n"

# Set environment variables for CT-084 system
ACTION=="add", SUBSYSTEM=="usb", ATTRS{idVendor}=="06c2", ENV{CT084_PHIDGET}="1"
"""
        
        try:
            rules_file = Path("/etc/udev/rules.d/99-ct084-phidgets.rules")
            
            with open(rules_file, 'w') as f:
                f.write(udev_rules)
            
            # Reload udev rules
            subprocess.run(['sudo', 'udevadm', 'control', '--reload-rules'], check=True)
            subprocess.run(['sudo', 'udevadm', 'trigger'], check=True)
            
            logger.info("Udev rules installed and reloaded")
            return True
            
        except Exception as e:
            logger.error(f"Failed to setup udev rules: {e}")
            return False
    
    def create_launcher_scripts(self) -> bool:
        """Create launcher scripts for easy system management."""
        logger.info("Creating launcher scripts...")
        
        try:
            # Main launcher script
            launcher_content = f"""#!/bin/bash
# CT-084 Parachute Drop System Launcher

export PYTHONPATH="{self.install_dir}:$PYTHONPATH"
export CT084_CONFIG_DIR="{self.config_dir}"
export CT084_LOG_DIR="{self.log_dir}"
export CT084_DATA_DIR="{self.data_dir}"

cd {self.install_dir}

case "$1" in
    start)
        echo "Starting CT-084 Parachute Drop System..."
        python3 -m phidget-auto-configurator.phidget_auto_configurator
        ;;
    discovery)
        echo "Running device discovery..."
        python3 -m device-detection.usb_device_manager
        ;;
    opcua-test)
        echo "Testing OPC-UA connection..."
        python3 -m opcua-integration.opcua_bridge
        ;;
    config)
        echo "Configuration management..."
        python3 -m config-management.configuration_manager
        ;;
    status)
        systemctl status ct084-system
        ;;
    logs)
        journalctl -u ct084-system -f
        ;;
    *)
        echo "Usage: $0 {{start|discovery|opcua-test|config|status|logs}}"
        exit 1
        ;;
esac
"""
            
            launcher_file = Path("/usr/local/bin/ct084")
            with open(launcher_file, 'w') as f:
                f.write(launcher_content)
            
            os.chmod(launcher_file, 0o755)
            
            logger.info("Launcher script created: /usr/local/bin/ct084")
            return True
            
        except Exception as e:
            logger.error(f"Failed to create launcher scripts: {e}")
            return False
    
    def run_initial_tests(self) -> bool:
        """Run initial system tests."""
        logger.info("Running initial system tests...")
        
        try:
            # Test Python module imports
            test_modules = [
                "phidget-auto-configurator.phidget_auto_configurator",
                "device-detection.usb_device_manager",
                "opcua-integration.opcua_bridge",
                "config-management.configuration_manager"
            ]
            
            for module in test_modules:
                try:
                    result = subprocess.run([
                        sys.executable, '-c', f'import sys; sys.path.insert(0, "{self.install_dir}"); import {module.replace("-", "_")}'
                    ], capture_output=True, text=True, timeout=10)
                    
                    if result.returncode == 0:
                        logger.info(f"Module test passed: {module}")
                    else:
                        logger.error(f"Module test failed: {module} - {result.stderr}")
                        return False
                        
                except subprocess.TimeoutExpired:
                    logger.error(f"Module test timeout: {module}")
                    return False
            
            # Test configuration loading
            config_manager_path = self.install_dir / "config-management" / "configuration_manager.py"
            if config_manager_path.exists():
                result = subprocess.run([
                    sys.executable, str(config_manager_path)
                ], capture_output=True, text=True, timeout=30)
                
                if result.returncode == 0:
                    logger.info("Configuration manager test passed")
                else:
                    logger.warning(f"Configuration manager test warning: {result.stderr}")
            
            logger.info("Initial system tests completed")
            return True
            
        except Exception as e:
            logger.error(f"System tests failed: {e}")
            return False
    
    def print_installation_summary(self):
        """Print installation summary and next steps."""
        print("\n" + "="*60)
        print("CT-084 PARACHUTE DROP SYSTEM - INSTALLATION COMPLETE")
        print("="*60)
        print(f"Version: {self.version}")
        print(f"Installation Directory: {self.install_dir}")
        print(f"Configuration Directory: {self.config_dir}")
        print(f"Log Directory: {self.log_dir}")
        print()
        print("NEXT STEPS:")
        print("1. Start the system:")
        print("   sudo systemctl start ct084-system")
        print()
        print("2. Enable auto-start:")
        print("   sudo systemctl enable ct084-system")
        print()
        print("3. Check system status:")
        print("   ct084 status")
        print()
        print("4. Run device discovery:")
        print("   ct084 discovery")
        print()
        print("5. View logs:")
        print("   ct084 logs")
        print()
        print("DOCUMENTATION:")
        print(f"- Configuration files: {self.config_dir}")
        print(f"- Log files: {self.log_dir}")
        print(f"- Setup log: /tmp/ct084_setup.log")
        print()
        print("For support and documentation:")
        print("https://github.com/your-org/ct-084-parachute-drop-system")
        print("="*60)
    
    def run_complete_setup(self) -> bool:
        """Run complete system setup."""
        logger.info(f"Starting {self.system_name} installation...")
        
        steps = [
            ("Checking system requirements", self.check_system_requirements),
            ("Installing Python dependencies", self.install_python_dependencies),
            ("Creating system directories", self.create_system_directories),
            ("Creating service user", self.create_service_user),
            ("Installing system files", self.install_system_files),
            ("Creating default configurations", self.create_default_configurations),
            ("Creating systemd service", self.create_systemd_service),
            ("Setting up udev rules", self.setup_udev_rules),
            ("Creating launcher scripts", self.create_launcher_scripts),
            ("Running initial tests", self.run_initial_tests)
        ]
        
        for step_name, step_function in steps:
            logger.info(f"Step: {step_name}")
            try:
                if not step_function():
                    logger.error(f"Setup failed at step: {step_name}")
                    return False
            except Exception as e:
                logger.error(f"Setup failed at step '{step_name}': {e}")
                return False
        
        self.print_installation_summary()
        logger.info("CT-084 system installation completed successfully")
        return True

def main():
    """Main entry point for setup script."""
    if os.geteuid() != 0:
        print("ERROR: This script must be run as root (use sudo)")
        print("sudo python3 setup_ct084_system.py")
        sys.exit(1)
    
    print("CT-084 Parachute Drop System - Setup and Installation")
    print("="*60)
    
    setup = CT084SystemSetup()
    
    try:
        success = setup.run_complete_setup()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\nSetup interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Setup failed with unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()