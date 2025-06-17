#!/usr/bin/env python3
"""
CT-084 Parachute Drop System - Configuration Manager
Handles configuration persistence, recovery, and device failure management.

This module provides comprehensive configuration management with automatic
backup, recovery, validation, and synchronization capabilities for mission-critical operations.
"""

import os
import sys
import time
import json
import yaml
import logging
import shutil
import threading
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, asdict, field
from enum import Enum
from pathlib import Path
import sqlite3

# Configuration validation
try:
    import jsonschema
    JSONSCHEMA_AVAILABLE = True
except ImportError:
    JSONSCHEMA_AVAILABLE = False
    logging.warning("jsonschema library not available. Configuration validation limited.")

# Import local modules
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Configure logging
logger = logging.getLogger('ConfigurationManager')

class ConfigStatus(Enum):
    """Configuration status indicators."""
    VALID = "valid"
    INVALID = "invalid"
    PENDING = "pending"
    CORRUPTED = "corrupted"
    MISSING = "missing"

class BackupType(Enum):
    """Backup type indicators."""
    AUTOMATIC = "automatic"
    MANUAL = "manual"
    EMERGENCY = "emergency"
    SCHEDULED = "scheduled"

@dataclass
class ConfigurationBackup:
    """Information about a configuration backup."""
    backup_id: str
    timestamp: str
    backup_type: BackupType
    file_path: str
    file_size: int
    checksum: str
    description: str
    valid: bool = True
    restored_count: int = 0

@dataclass
class DeviceConfiguration:
    """Device-specific configuration data."""
    device_id: str
    device_type: str
    serial_number: str
    hub_port: int
    sensor_type: str
    calibration_data: Dict = field(default_factory=dict)
    operational_parameters: Dict = field(default_factory=dict)
    alarm_thresholds: Dict = field(default_factory=dict)
    opcua_mapping: Dict = field(default_factory=dict)
    last_updated: str = field(default_factory=lambda: datetime.now().isoformat())
    configuration_version: str = "1.0.0"
    status: ConfigStatus = ConfigStatus.VALID

@dataclass
class SystemConfiguration:
    """Complete system configuration."""
    system_id: str
    configuration_version: str
    created_timestamp: str
    last_modified: str
    devices: Dict[str, DeviceConfiguration] = field(default_factory=dict)
    opcua_settings: Dict = field(default_factory=dict)
    monitoring_settings: Dict = field(default_factory=dict)
    fault_tolerance: Dict = field(default_factory=dict)
    mission_parameters: Dict = field(default_factory=dict)
    checksum: Optional[str] = None

class ConfigurationManager:
    """
    Comprehensive configuration management for CT-084 Parachute Drop System.
    
    Provides configuration persistence, validation, backup/restore,
    and automatic recovery capabilities for mission-critical reliability.
    """
    
    def __init__(self, config_dir: str = "/etc/ct-084", 
                 backup_dir: str = "/var/backups/ct-084",
                 database_path: str = "/var/lib/ct-084/config.db"):
        """
        Initialize configuration manager.
        
        Args:
            config_dir: Primary configuration directory
            backup_dir: Backup storage directory
            database_path: SQLite database for configuration tracking
        """
        self.config_dir = Path(config_dir)
        self.backup_dir = Path(backup_dir)
        self.database_path = Path(database_path)
        
        # Ensure directories exist
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Configuration files
        self.system_config_file = self.config_dir / "system_configuration.yaml"
        self.device_config_file = self.config_dir / "device_configurations.yaml"
        self.schema_file = self.config_dir / "configuration_schema.json"
        
        # Current configuration
        self.system_config: Optional[SystemConfiguration] = None
        self.device_configs: Dict[str, DeviceConfiguration] = {}
        
        # Backup management
        self.max_backups = 50
        self.auto_backup_interval = 300  # 5 minutes
        self.backup_thread = None
        self.monitoring_active = False
        
        # Initialize database
        self._initialize_database()
        
        # Load configuration schema
        self.config_schema = self._load_configuration_schema()
        
        logger.info("Configuration Manager initialized")
    
    def _initialize_database(self):
        """Initialize SQLite database for configuration tracking."""
        try:
            with sqlite3.connect(self.database_path) as conn:
                cursor = conn.cursor()
                
                # Create backups table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS backups (
                        backup_id TEXT PRIMARY KEY,
                        timestamp TEXT NOT NULL,
                        backup_type TEXT NOT NULL,
                        file_path TEXT NOT NULL,
                        file_size INTEGER NOT NULL,
                        checksum TEXT NOT NULL,
                        description TEXT,
                        valid INTEGER DEFAULT 1,
                        restored_count INTEGER DEFAULT 0
                    )
                ''')
                
                # Create configuration changes table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS config_changes (
                        change_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp TEXT NOT NULL,
                        change_type TEXT NOT NULL,
                        device_id TEXT,
                        field_name TEXT,
                        old_value TEXT,
                        new_value TEXT,
                        user_id TEXT,
                        description TEXT
                    )
                ''')
                
                # Create device status table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS device_status (
                        device_id TEXT PRIMARY KEY,
                        last_seen TEXT NOT NULL,
                        configuration_status TEXT NOT NULL,
                        error_count INTEGER DEFAULT 0,
                        last_error TEXT,
                        configuration_checksum TEXT
                    )
                ''')
                
                conn.commit()
                logger.info("Configuration database initialized")
                
        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")
    
    def _load_configuration_schema(self) -> Optional[Dict]:
        """Load JSON schema for configuration validation."""
        if not JSONSCHEMA_AVAILABLE:
            logger.warning("Configuration validation unavailable - jsonschema not installed")
            return None
        
        schema_file = self.schema_file
        
        # Create default schema if it doesn't exist
        if not schema_file.exists():
            self._create_default_schema()
        
        try:
            with open(schema_file, 'r') as f:
                schema = json.load(f)
            logger.info("Configuration schema loaded")
            return schema
        except Exception as e:
            logger.error(f"Failed to load configuration schema: {e}")
            return None
    
    def _create_default_schema(self):
        """Create default JSON schema for configuration validation."""
        default_schema = {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "title": "CT-084 Parachute Drop System Configuration",
            "type": "object",
            "properties": {
                "system_id": {"type": "string", "minLength": 1},
                "configuration_version": {"type": "string", "pattern": "^\\d+\\.\\d+\\.\\d+$"},
                "created_timestamp": {"type": "string", "format": "date-time"},
                "last_modified": {"type": "string", "format": "date-time"},
                "devices": {
                    "type": "object",
                    "additionalProperties": {
                        "type": "object",
                        "properties": {
                            "device_id": {"type": "string", "minLength": 1},
                            "device_type": {"type": "string", "enum": ["phidget_hub", "sensor", "actuator"]},
                            "serial_number": {"type": "string", "minLength": 1},
                            "hub_port": {"type": "integer", "minimum": 0, "maximum": 15},
                            "sensor_type": {
                                "type": "string", 
                                "enum": ["temperature", "pressure", "humidity", "acceleration", "gyroscope", "voltage", "voltage_ratio"]
                            },
                            "calibration_data": {"type": "object"},
                            "operational_parameters": {"type": "object"},
                            "alarm_thresholds": {"type": "object"},
                            "opcua_mapping": {"type": "object"},
                            "configuration_version": {"type": "string"},
                            "status": {"type": "string", "enum": ["valid", "invalid", "pending", "corrupted", "missing"]}
                        },
                        "required": ["device_id", "device_type", "serial_number", "sensor_type"]
                    }
                },
                "opcua_settings": {"type": "object"},
                "monitoring_settings": {"type": "object"},
                "fault_tolerance": {"type": "object"},
                "mission_parameters": {"type": "object"}
            },
            "required": ["system_id", "configuration_version", "created_timestamp", "devices"]
        }
        
        try:
            with open(self.schema_file, 'w') as f:
                json.dump(default_schema, f, indent=2)
            logger.info("Default configuration schema created")
        except Exception as e:
            logger.error(f"Failed to create default schema: {e}")
    
    def load_system_configuration(self) -> Optional[SystemConfiguration]:
        """
        Load system configuration from file.
        
        Returns:
            SystemConfiguration object if successful, None otherwise
        """
        try:
            if not self.system_config_file.exists():
                logger.warning("System configuration file does not exist")
                return self._create_default_system_configuration()
            
            with open(self.system_config_file, 'r') as f:
                config_data = yaml.safe_load(f)
            
            # Validate configuration
            if not self._validate_configuration(config_data):
                logger.error("System configuration validation failed")
                return None
            
            # Convert to SystemConfiguration object
            system_config = SystemConfiguration(
                system_id=config_data['system_id'],
                configuration_version=config_data['configuration_version'],
                created_timestamp=config_data['created_timestamp'],
                last_modified=config_data['last_modified'],
                devices={},
                opcua_settings=config_data.get('opcua_settings', {}),
                monitoring_settings=config_data.get('monitoring_settings', {}),
                fault_tolerance=config_data.get('fault_tolerance', {}),
                mission_parameters=config_data.get('mission_parameters', {})
            )
            
            # Load device configurations
            if 'devices' in config_data:
                for device_id, device_data in config_data['devices'].items():
                    device_config = DeviceConfiguration(**device_data)
                    system_config.devices[device_id] = device_config
            
            # Calculate checksum
            system_config.checksum = self._calculate_configuration_checksum(system_config)
            
            self.system_config = system_config
            logger.info(f"System configuration loaded: {system_config.system_id}")
            
            return system_config
            
        except Exception as e:
            logger.error(f"Failed to load system configuration: {e}")
            return None
    
    def _create_default_system_configuration(self) -> SystemConfiguration:
        """Create default system configuration."""
        logger.info("Creating default system configuration")
        
        default_config = SystemConfiguration(
            system_id="CT-084-001",
            configuration_version="1.0.0",
            created_timestamp=datetime.now().isoformat(),
            last_modified=datetime.now().isoformat(),
            opcua_settings={
                'endpoint': 'opc.tcp://localhost:4840/freeopcua/server/',
                'namespace': 'CT084_ParachuteDrop',
                'security_policy': 'None',
                'auto_reconnect': True
            },
            monitoring_settings={
                'scan_interval': 5.0,
                'data_retention_days': 30,
                'alert_enabled': True
            },
            fault_tolerance={
                'enable_redundancy': True,
                'max_connection_failures': 3,
                'auto_recovery': True,
                'store_and_forward': True
            },
            mission_parameters={
                'deployment_altitude': 1000,  # meters
                'critical_altitude': 500,     # meters
                'max_descent_rate': 10,       # m/s
                'parachute_deployment_time': 30  # seconds
            }
        )
        
        # Calculate checksum
        default_config.checksum = self._calculate_configuration_checksum(default_config)
        
        # Save default configuration
        self.save_system_configuration(default_config)
        
        return default_config
    
    def save_system_configuration(self, config: SystemConfiguration, 
                                create_backup: bool = True) -> bool:
        """
        Save system configuration to file.
        
        Args:
            config: SystemConfiguration object to save
            create_backup: Whether to create backup before saving
            
        Returns:
            True if saved successfully, False otherwise
        """
        try:
            # Create backup if requested
            if create_backup and self.system_config_file.exists():
                self.create_backup("Automatic backup before configuration save", 
                                 BackupType.AUTOMATIC)
            
            # Update timestamps
            config.last_modified = datetime.now().isoformat()
            config.checksum = self._calculate_configuration_checksum(config)
            
            # Convert to dictionary for serialization
            config_dict = {
                'system_id': config.system_id,
                'configuration_version': config.configuration_version,
                'created_timestamp': config.created_timestamp,
                'last_modified': config.last_modified,
                'devices': {},
                'opcua_settings': config.opcua_settings,
                'monitoring_settings': config.monitoring_settings,
                'fault_tolerance': config.fault_tolerance,
                'mission_parameters': config.mission_parameters,
                'checksum': config.checksum
            }
            
            # Add device configurations
            for device_id, device_config in config.devices.items():
                config_dict['devices'][device_id] = asdict(device_config)
            
            # Validate before saving
            if not self._validate_configuration(config_dict):
                logger.error("Configuration validation failed, not saving")
                return False
            
            # Write to file
            with open(self.system_config_file, 'w') as f:
                yaml.dump(config_dict, f, default_flow_style=False, indent=2)
            
            # Update internal reference
            self.system_config = config
            
            # Log configuration change
            self._log_configuration_change("system_save", None, "system", 
                                         None, config.checksum, "System configuration saved")
            
            logger.info(f"System configuration saved: {config.system_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save system configuration: {e}")
            return False
    
    def add_device_configuration(self, device_config: DeviceConfiguration) -> bool:
        """
        Add or update device configuration.
        
        Args:
            device_config: DeviceConfiguration object to add/update
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if not self.system_config:
                logger.error("No system configuration loaded")
                return False
            
            # Update device timestamp
            device_config.last_updated = datetime.now().isoformat()
            device_config.status = ConfigStatus.VALID
            
            # Store old configuration for change tracking
            old_config = self.system_config.devices.get(device_config.device_id)
            
            # Add/update device
            self.system_config.devices[device_config.device_id] = device_config
            
            # Save system configuration
            if self.save_system_configuration(self.system_config):
                # Log device configuration change
                self._log_configuration_change(
                    "device_update" if old_config else "device_add",
                    device_config.device_id,
                    "device_configuration",
                    asdict(old_config) if old_config else None,
                    asdict(device_config),
                    f"Device {device_config.device_id} configuration updated"
                )
                
                logger.info(f"Device configuration saved: {device_config.device_id}")
                return True
            else:
                return False
                
        except Exception as e:
            logger.error(f"Failed to add device configuration: {e}")
            return False
    
    def remove_device_configuration(self, device_id: str) -> bool:
        """
        Remove device configuration.
        
        Args:
            device_id: ID of device to remove
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if not self.system_config:
                logger.error("No system configuration loaded")
                return False
            
            if device_id not in self.system_config.devices:
                logger.warning(f"Device {device_id} not found in configuration")
                return False
            
            # Store old configuration for change tracking
            old_config = self.system_config.devices[device_id]
            
            # Remove device
            del self.system_config.devices[device_id]
            
            # Save system configuration
            if self.save_system_configuration(self.system_config):
                # Log device removal
                self._log_configuration_change(
                    "device_remove",
                    device_id,
                    "device_configuration",
                    asdict(old_config),
                    None,
                    f"Device {device_id} configuration removed"
                )
                
                logger.info(f"Device configuration removed: {device_id}")
                return True
            else:
                return False
                
        except Exception as e:
            logger.error(f"Failed to remove device configuration: {e}")
            return False
    
    def _validate_configuration(self, config_data: Dict) -> bool:
        """
        Validate configuration against schema.
        
        Args:
            config_data: Configuration data to validate
            
        Returns:
            True if valid, False otherwise
        """
        if not JSONSCHEMA_AVAILABLE or not self.config_schema:
            logger.warning("Configuration validation skipped - schema unavailable")
            return True
        
        try:
            jsonschema.validate(config_data, self.config_schema)
            logger.debug("Configuration validation passed")
            return True
        except jsonschema.ValidationError as e:
            logger.error(f"Configuration validation failed: {e.message}")
            return False
        except Exception as e:
            logger.error(f"Configuration validation error: {e}")
            return False
    
    def _calculate_configuration_checksum(self, config: SystemConfiguration) -> str:
        """Calculate SHA256 checksum of configuration."""
        try:
            # Convert to JSON string for consistent hashing
            config_dict = asdict(config)
            config_dict.pop('checksum', None)  # Remove checksum field itself
            config_str = json.dumps(config_dict, sort_keys=True)
            
            # Calculate SHA256 hash
            return hashlib.sha256(config_str.encode()).hexdigest()
        except Exception as e:
            logger.error(f"Failed to calculate configuration checksum: {e}")
            return ""
    
    def create_backup(self, description: str, backup_type: BackupType = BackupType.MANUAL) -> Optional[str]:
        """
        Create configuration backup.
        
        Args:
            description: Description of the backup
            backup_type: Type of backup being created
            
        Returns:
            Backup ID if successful, None otherwise
        """
        try:
            # Generate backup ID
            backup_id = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{backup_type.value}"
            backup_timestamp = datetime.now().isoformat()
            
            # Create backup file path
            backup_filename = f"{backup_id}.yaml"
            backup_filepath = self.backup_dir / backup_filename
            
            # Copy configuration file
            if self.system_config_file.exists():
                shutil.copy2(self.system_config_file, backup_filepath)
                
                # Calculate file size and checksum
                file_size = backup_filepath.stat().st_size
                with open(backup_filepath, 'rb') as f:
                    file_checksum = hashlib.sha256(f.read()).hexdigest()
                
                # Store backup information in database
                backup_info = ConfigurationBackup(
                    backup_id=backup_id,
                    timestamp=backup_timestamp,
                    backup_type=backup_type,
                    file_path=str(backup_filepath),
                    file_size=file_size,
                    checksum=file_checksum,
                    description=description
                )
                
                self._store_backup_info(backup_info)
                
                # Clean up old backups
                self._cleanup_old_backups()
                
                logger.info(f"Configuration backup created: {backup_id}")
                return backup_id
            else:
                logger.error("No configuration file exists to backup")
                return None
                
        except Exception as e:
            logger.error(f"Failed to create backup: {e}")
            return None
    
    def restore_backup(self, backup_id: str) -> bool:
        """
        Restore configuration from backup.
        
        Args:
            backup_id: ID of backup to restore
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Get backup information
            backup_info = self._get_backup_info(backup_id)
            if not backup_info:
                logger.error(f"Backup {backup_id} not found")
                return False
            
            backup_file = Path(backup_info.file_path)
            if not backup_file.exists():
                logger.error(f"Backup file {backup_file} does not exist")
                return False
            
            # Validate backup file checksum
            with open(backup_file, 'rb') as f:
                current_checksum = hashlib.sha256(f.read()).hexdigest()
            
            if current_checksum != backup_info.checksum:
                logger.error(f"Backup file checksum mismatch - file may be corrupted")
                return False
            
            # Create current configuration backup before restore
            restore_backup_id = self.create_backup(
                f"Pre-restore backup before restoring {backup_id}",
                BackupType.EMERGENCY
            )
            
            # Restore configuration
            shutil.copy2(backup_file, self.system_config_file)
            
            # Reload configuration
            restored_config = self.load_system_configuration()
            if restored_config:
                # Update restore count
                self._update_backup_restore_count(backup_id)
                
                # Log restoration
                self._log_configuration_change(
                    "restore",
                    None,
                    "system",
                    None,
                    backup_id,
                    f"Configuration restored from backup {backup_id}"
                )
                
                logger.info(f"Configuration restored from backup: {backup_id}")
                return True
            else:
                # Restore failed, try to restore pre-restore backup
                if restore_backup_id:
                    logger.error("Restore failed, attempting to restore pre-restore backup")
                    return self.restore_backup(restore_backup_id)
                return False
                
        except Exception as e:
            logger.error(f"Failed to restore backup {backup_id}: {e}")
            return False
    
    def _store_backup_info(self, backup_info: ConfigurationBackup):
        """Store backup information in database."""
        try:
            with sqlite3.connect(self.database_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO backups 
                    (backup_id, timestamp, backup_type, file_path, file_size, 
                     checksum, description, valid, restored_count)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    backup_info.backup_id,
                    backup_info.timestamp,
                    backup_info.backup_type.value,
                    backup_info.file_path,
                    backup_info.file_size,
                    backup_info.checksum,
                    backup_info.description,
                    int(backup_info.valid),
                    backup_info.restored_count
                ))
                conn.commit()
        except Exception as e:
            logger.error(f"Failed to store backup info: {e}")
    
    def _get_backup_info(self, backup_id: str) -> Optional[ConfigurationBackup]:
        """Get backup information from database."""
        try:
            with sqlite3.connect(self.database_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT backup_id, timestamp, backup_type, file_path, file_size,
                           checksum, description, valid, restored_count
                    FROM backups WHERE backup_id = ?
                ''', (backup_id,))
                
                row = cursor.fetchone()
                if row:
                    return ConfigurationBackup(
                        backup_id=row[0],
                        timestamp=row[1],
                        backup_type=BackupType(row[2]),
                        file_path=row[3],
                        file_size=row[4],
                        checksum=row[5],
                        description=row[6],
                        valid=bool(row[7]),
                        restored_count=row[8]
                    )
                return None
        except Exception as e:
            logger.error(f"Failed to get backup info: {e}")
            return None
    
    def _update_backup_restore_count(self, backup_id: str):
        """Update backup restore count."""
        try:
            with sqlite3.connect(self.database_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE backups SET restored_count = restored_count + 1
                    WHERE backup_id = ?
                ''', (backup_id,))
                conn.commit()
        except Exception as e:
            logger.error(f"Failed to update backup restore count: {e}")
    
    def _cleanup_old_backups(self):
        """Clean up old backups to maintain storage limits."""
        try:
            with sqlite3.connect(self.database_path) as conn:
                cursor = conn.cursor()
                
                # Get backup count
                cursor.execute('SELECT COUNT(*) FROM backups')
                backup_count = cursor.fetchone()[0]
                
                if backup_count > self.max_backups:
                    # Delete oldest backups
                    excess_count = backup_count - self.max_backups
                    cursor.execute('''
                        SELECT backup_id, file_path FROM backups 
                        ORDER BY timestamp ASC LIMIT ?
                    ''', (excess_count,))
                    
                    old_backups = cursor.fetchall()
                    
                    for backup_id, file_path in old_backups:
                        # Delete file
                        try:
                            Path(file_path).unlink(missing_ok=True)
                        except Exception as e:
                            logger.warning(f"Failed to delete backup file {file_path}: {e}")
                        
                        # Remove from database
                        cursor.execute('DELETE FROM backups WHERE backup_id = ?', (backup_id,))
                    
                    conn.commit()
                    logger.info(f"Cleaned up {len(old_backups)} old backups")
                    
        except Exception as e:
            logger.error(f"Failed to cleanup old backups: {e}")
    
    def _log_configuration_change(self, change_type: str, device_id: Optional[str],
                                field_name: str, old_value: Any, new_value: Any,
                                description: str, user_id: str = "system"):
        """Log configuration change to database."""
        try:
            with sqlite3.connect(self.database_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO config_changes 
                    (timestamp, change_type, device_id, field_name, old_value, 
                     new_value, user_id, description)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    datetime.now().isoformat(),
                    change_type,
                    device_id,
                    field_name,
                    json.dumps(old_value) if old_value is not None else None,
                    json.dumps(new_value) if new_value is not None else None,
                    user_id,
                    description
                ))
                conn.commit()
        except Exception as e:
            logger.error(f"Failed to log configuration change: {e}")
    
    def get_backup_list(self) -> List[ConfigurationBackup]:
        """Get list of all available backups."""
        backups = []
        try:
            with sqlite3.connect(self.database_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT backup_id, timestamp, backup_type, file_path, file_size,
                           checksum, description, valid, restored_count
                    FROM backups ORDER BY timestamp DESC
                ''')
                
                for row in cursor.fetchall():
                    backup = ConfigurationBackup(
                        backup_id=row[0],
                        timestamp=row[1],
                        backup_type=BackupType(row[2]),
                        file_path=row[3],
                        file_size=row[4],
                        checksum=row[5],
                        description=row[6],
                        valid=bool(row[7]),
                        restored_count=row[8]
                    )
                    backups.append(backup)
                    
        except Exception as e:
            logger.error(f"Failed to get backup list: {e}")
        
        return backups
    
    def start_automatic_backup(self):
        """Start automatic backup monitoring."""
        if self.backup_thread and self.backup_thread.is_alive():
            logger.warning("Automatic backup already running")
            return
        
        self.monitoring_active = True
        self.backup_thread = threading.Thread(target=self._backup_monitoring_loop, daemon=True)
        self.backup_thread.start()
        logger.info("Automatic backup monitoring started")
    
    def stop_automatic_backup(self):
        """Stop automatic backup monitoring."""
        self.monitoring_active = False
        if self.backup_thread:
            self.backup_thread.join(timeout=5)
        logger.info("Automatic backup monitoring stopped")
    
    def _backup_monitoring_loop(self):
        """Automatic backup monitoring loop."""
        last_backup_time = datetime.now()
        
        while self.monitoring_active:
            try:
                current_time = datetime.now()
                
                # Check if backup interval has elapsed
                if (current_time - last_backup_time).total_seconds() >= self.auto_backup_interval:
                    # Check if configuration has changed
                    if self.system_config and self.system_config_file.exists():
                        file_modified = datetime.fromtimestamp(
                            self.system_config_file.stat().st_mtime
                        )
                        
                        if file_modified > last_backup_time:
                            backup_id = self.create_backup(
                                "Automatic scheduled backup",
                                BackupType.SCHEDULED
                            )
                            
                            if backup_id:
                                last_backup_time = current_time
                                logger.info("Automatic backup completed")
                
                time.sleep(60)  # Check every minute
                
            except Exception as e:
                logger.error(f"Error in backup monitoring loop: {e}")
                time.sleep(60)
    
    def get_configuration_status(self) -> Dict:
        """Get comprehensive configuration status."""
        status = {
            'timestamp': datetime.now().isoformat(),
            'system_config_loaded': self.system_config is not None,
            'config_file_exists': self.system_config_file.exists(),
            'schema_available': self.config_schema is not None,
            'total_devices': len(self.system_config.devices) if self.system_config else 0,
            'backup_count': 0,
            'automatic_backup_active': self.monitoring_active,
            'last_modification': None,
            'configuration_valid': False
        }
        
        try:
            # Get backup count
            with sqlite3.connect(self.database_path) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT COUNT(*) FROM backups')
                status['backup_count'] = cursor.fetchone()[0]
            
            # Check file modification time
            if self.system_config_file.exists():
                status['last_modification'] = datetime.fromtimestamp(
                    self.system_config_file.stat().st_mtime
                ).isoformat()
            
            # Validate current configuration
            if self.system_config:
                config_dict = asdict(self.system_config)
                status['configuration_valid'] = self._validate_configuration(config_dict)
                
        except Exception as e:
            logger.error(f"Failed to get configuration status: {e}")
        
        return status

def main():
    """Main entry point for configuration manager testing."""
    print("CT-084 Configuration Manager - Testing")
    print("Initializing configuration management...\n")
    
    # Create configuration manager
    manager = ConfigurationManager()
    
    # Load or create system configuration
    config = manager.load_system_configuration()
    
    if config:
        print(f"System Configuration: {config.system_id}")
        print(f"Version: {config.configuration_version}")
        print(f"Devices: {len(config.devices)}")
        print(f"Checksum: {config.checksum[:16]}...")
    
    # Create test backup
    backup_id = manager.create_backup("Test backup", BackupType.MANUAL)
    print(f"Created backup: {backup_id}")
    
    # Get status
    status = manager.get_configuration_status()
    print(f"\nConfiguration Status:")
    print(f"  System config loaded: {status['system_config_loaded']}")
    print(f"  Total devices: {status['total_devices']}")
    print(f"  Backup count: {status['backup_count']}")
    print(f"  Configuration valid: {status['configuration_valid']}")
    
    # List backups
    backups = manager.get_backup_list()
    print(f"\nAvailable Backups ({len(backups)}):")
    for backup in backups[:5]:  # Show first 5
        print(f"  {backup.backup_id} - {backup.backup_type.value} - {backup.timestamp}")

if __name__ == "__main__":
    main()