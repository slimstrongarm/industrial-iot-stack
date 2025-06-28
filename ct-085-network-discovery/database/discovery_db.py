#!/usr/bin/env python3
"""
Database management for network discovery system
Handles device storage, classification results, and scan history
"""

import sqlite3
import json
import logging
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from contextlib import contextmanager
import threading

class DiscoveryDatabase:
    def __init__(self, db_path: str = "database/discovery.db"):
        self.db_path = db_path
        self.lock = threading.Lock()
        self.init_database()
        
    def init_database(self):
        """Initialize database with required tables"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Devices table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS devices (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ip_address TEXT NOT NULL,
                    mac_address TEXT,
                    hostname TEXT,
                    device_type TEXT,
                    vendor TEXT,
                    model TEXT,
                    firmware_version TEXT,
                    protocols TEXT,  -- JSON array of supported protocols
                    first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    status TEXT DEFAULT 'active',
                    confidence_score REAL,
                    classification_data TEXT,  -- JSON classification details
                    custom_tags TEXT,  -- JSON array of custom tags
                    UNIQUE(ip_address)
                )
            ''')
            
            # Protocol endpoints table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS protocol_endpoints (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    device_id INTEGER,
                    protocol TEXT NOT NULL,
                    port INTEGER NOT NULL,
                    endpoint_data TEXT,  -- JSON protocol-specific data
                    last_response TEXT,
                    response_time REAL,
                    is_active BOOLEAN DEFAULT 1,
                    discovered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (device_id) REFERENCES devices (id)
                )
            ''')
            
            # Scan history table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS scan_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    scan_id TEXT NOT NULL,
                    scan_type TEXT NOT NULL,
                    target_range TEXT,
                    start_time TIMESTAMP,
                    end_time TIMESTAMP,
                    devices_found INTEGER DEFAULT 0,
                    scan_config TEXT,  -- JSON scan configuration
                    results_summary TEXT,  -- JSON summary
                    status TEXT DEFAULT 'running'
                )
            ''')
            
            # Device capabilities table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS device_capabilities (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    device_id INTEGER,
                    capability_type TEXT NOT NULL,
                    capability_data TEXT,  -- JSON capability details
                    verified BOOLEAN DEFAULT 0,
                    last_verified TIMESTAMP,
                    FOREIGN KEY (device_id) REFERENCES devices (id)
                )
            ''')
            
            # Network topology table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS network_topology (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    device_id INTEGER,
                    connected_device_id INTEGER,
                    connection_type TEXT,
                    connection_data TEXT,  -- JSON connection details
                    discovered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (device_id) REFERENCES devices (id),
                    FOREIGN KEY (connected_device_id) REFERENCES devices (id)
                )
            ''')
            
            # Create indexes for better performance
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_devices_ip ON devices(ip_address)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_devices_type ON devices(device_type)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_devices_last_seen ON devices(last_seen)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_endpoints_device ON protocol_endpoints(device_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_endpoints_protocol ON protocol_endpoints(protocol)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_scan_history_time ON scan_history(start_time)')
            
            conn.commit()
            logging.info("Database initialized successfully")
    
    @contextmanager
    def get_connection(self):
        """Get database connection with proper error handling"""
        conn = None
        try:
            conn = sqlite3.connect(self.db_path, timeout=30)
            conn.row_factory = sqlite3.Row
            yield conn
        except Exception as e:
            if conn:
                conn.rollback()
            logging.error(f"Database error: {e}")
            raise
        finally:
            if conn:
                conn.close()
    
    def add_device(self, device_data: Dict[str, Any]) -> int:
        """Add or update device in database"""
        with self.lock:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Check if device exists
                cursor.execute('SELECT id FROM devices WHERE ip_address = ?', (device_data['ip_address'],))
                existing = cursor.fetchone()
                
                if existing:
                    # Update existing device
                    device_id = existing['id']
                    update_fields = []
                    update_values = []
                    
                    for field in ['hostname', 'device_type', 'vendor', 'model', 'firmware_version', 
                                'protocols', 'confidence_score', 'classification_data', 'custom_tags']:
                        if field in device_data:
                            update_fields.append(f"{field} = ?")
                            if field in ['protocols', 'classification_data', 'custom_tags']:
                                update_values.append(json.dumps(device_data[field]))
                            else:
                                update_values.append(device_data[field])
                    
                    update_fields.append("last_seen = CURRENT_TIMESTAMP")
                    update_values.append(device_data['ip_address'])
                    
                    query = f"UPDATE devices SET {', '.join(update_fields)} WHERE ip_address = ?"
                    cursor.execute(query, update_values)
                    
                else:
                    # Insert new device
                    protocols_json = json.dumps(device_data.get('protocols', []))
                    classification_json = json.dumps(device_data.get('classification_data', {}))
                    tags_json = json.dumps(device_data.get('custom_tags', []))
                    
                    cursor.execute('''
                        INSERT INTO devices (ip_address, mac_address, hostname, device_type, vendor, 
                                           model, firmware_version, protocols, confidence_score, 
                                           classification_data, custom_tags)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        device_data['ip_address'],
                        device_data.get('mac_address'),
                        device_data.get('hostname'),
                        device_data.get('device_type'),
                        device_data.get('vendor'),
                        device_data.get('model'),
                        device_data.get('firmware_version'),
                        protocols_json,
                        device_data.get('confidence_score'),
                        classification_json,
                        tags_json
                    ))
                    device_id = cursor.lastrowid
                
                conn.commit()
                return device_id
    
    def add_protocol_endpoint(self, device_id: int, protocol_data: Dict[str, Any]):
        """Add protocol endpoint for a device"""
        with self.lock:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                endpoint_json = json.dumps(protocol_data.get('endpoint_data', {}))
                
                cursor.execute('''
                    INSERT OR REPLACE INTO protocol_endpoints 
                    (device_id, protocol, port, endpoint_data, last_response, response_time, is_active)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    device_id,
                    protocol_data['protocol'],
                    protocol_data['port'],
                    endpoint_json,
                    protocol_data.get('last_response'),
                    protocol_data.get('response_time'),
                    protocol_data.get('is_active', True)
                ))
                
                conn.commit()
    
    def start_scan(self, scan_id: str, scan_type: str, target_range: str, config: Dict[str, Any]) -> int:
        """Record scan start"""
        with self.lock:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                config_json = json.dumps(config)
                
                cursor.execute('''
                    INSERT INTO scan_history (scan_id, scan_type, target_range, start_time, scan_config, status)
                    VALUES (?, ?, ?, CURRENT_TIMESTAMP, ?, 'running')
                ''', (scan_id, scan_type, target_range, config_json))
                
                scan_record_id = cursor.lastrowid
                conn.commit()
                return scan_record_id
    
    def complete_scan(self, scan_id: str, devices_found: int, results_summary: Dict[str, Any]):
        """Mark scan as complete"""
        with self.lock:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                summary_json = json.dumps(results_summary)
                
                cursor.execute('''
                    UPDATE scan_history 
                    SET end_time = CURRENT_TIMESTAMP, devices_found = ?, results_summary = ?, status = 'completed'
                    WHERE scan_id = ?
                ''', (devices_found, summary_json, scan_id))
                
                conn.commit()
    
    def get_devices(self, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Get devices with optional filters"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            query = "SELECT * FROM devices"
            params = []
            
            if filters:
                conditions = []
                
                if 'device_type' in filters:
                    conditions.append("device_type = ?")
                    params.append(filters['device_type'])
                
                if 'vendor' in filters:
                    conditions.append("vendor = ?")
                    params.append(filters['vendor'])
                
                if 'active_since' in filters:
                    conditions.append("last_seen >= ?")
                    params.append(filters['active_since'])
                
                if 'ip_range' in filters:
                    # Simple IP range filtering - could be enhanced
                    conditions.append("ip_address LIKE ?")
                    params.append(f"{filters['ip_range']}%")
                
                if conditions:
                    query += " WHERE " + " AND ".join(conditions)
            
            query += " ORDER BY last_seen DESC"
            
            cursor.execute(query, params)
            devices = []
            
            for row in cursor.fetchall():
                device = dict(row)
                # Parse JSON fields
                if device['protocols']:
                    device['protocols'] = json.loads(device['protocols'])
                if device['classification_data']:
                    device['classification_data'] = json.loads(device['classification_data'])
                if device['custom_tags']:
                    device['custom_tags'] = json.loads(device['custom_tags'])
                
                devices.append(device)
            
            return devices
    
    def get_device_endpoints(self, device_id: int) -> List[Dict[str, Any]]:
        """Get protocol endpoints for a device"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM protocol_endpoints 
                WHERE device_id = ? AND is_active = 1
                ORDER BY protocol, port
            ''', (device_id,))
            
            endpoints = []
            for row in cursor.fetchall():
                endpoint = dict(row)
                if endpoint['endpoint_data']:
                    endpoint['endpoint_data'] = json.loads(endpoint['endpoint_data'])
                endpoints.append(endpoint)
            
            return endpoints
    
    def get_scan_history(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get recent scan history"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM scan_history 
                ORDER BY start_time DESC 
                LIMIT ?
            ''', (limit,))
            
            scans = []
            for row in cursor.fetchall():
                scan = dict(row)
                if scan['scan_config']:
                    scan['scan_config'] = json.loads(scan['scan_config'])
                if scan['results_summary']:
                    scan['results_summary'] = json.loads(scan['results_summary'])
                scans.append(scan)
            
            return scans
    
    def cleanup_old_data(self, days_old: int = 30):
        """Clean up old scan history and inactive devices"""
        cutoff_date = datetime.now() - timedelta(days=days_old)
        
        with self.lock:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Remove old scan history
                cursor.execute('''
                    DELETE FROM scan_history 
                    WHERE start_time < ? AND status = 'completed'
                ''', (cutoff_date,))
                
                # Mark devices as inactive if not seen recently
                cursor.execute('''
                    UPDATE devices 
                    SET status = 'inactive' 
                    WHERE last_seen < ? AND status = 'active'
                ''', (cutoff_date,))
                
                conn.commit()
                logging.info(f"Cleaned up data older than {days_old} days")
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get database statistics"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            stats = {}
            
            # Device counts
            cursor.execute("SELECT COUNT(*) FROM devices WHERE status = 'active'")
            stats['active_devices'] = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM devices")
            stats['total_devices'] = cursor.fetchone()[0]
            
            # Device types
            cursor.execute('''
                SELECT device_type, COUNT(*) as count 
                FROM devices 
                WHERE status = 'active' AND device_type IS NOT NULL
                GROUP BY device_type
            ''')
            stats['device_types'] = dict(cursor.fetchall())
            
            # Protocol counts
            cursor.execute('''
                SELECT protocol, COUNT(*) as count 
                FROM protocol_endpoints 
                WHERE is_active = 1
                GROUP BY protocol
            ''')
            stats['protocols'] = dict(cursor.fetchall())
            
            # Recent scan count
            cursor.execute('''
                SELECT COUNT(*) FROM scan_history 
                WHERE start_time >= datetime('now', '-24 hours')
            ''')
            stats['recent_scans'] = cursor.fetchone()[0]
            
            return stats

if __name__ == "__main__":
    # Test database functionality
    logging.basicConfig(level=logging.INFO)
    
    db = DiscoveryDatabase("test_discovery.db")
    
    # Test device addition
    test_device = {
        'ip_address': '192.168.1.100',
        'hostname': 'test-plc',
        'device_type': 'PLC',
        'vendor': 'Siemens',
        'model': 'S7-1200',
        'protocols': ['modbus', 'opcua'],
        'confidence_score': 0.95
    }
    
    device_id = db.add_device(test_device)
    print(f"Added device with ID: {device_id}")
    
    # Test endpoint addition
    endpoint = {
        'protocol': 'modbus',
        'port': 502,
        'endpoint_data': {'slave_id': 1, 'function_codes': [3, 4]},
        'response_time': 0.1,
        'is_active': True
    }
    
    db.add_protocol_endpoint(device_id, endpoint)
    
    # Test retrieval
    devices = db.get_devices()
    print(f"Found {len(devices)} devices")
    
    stats = db.get_statistics()
    print(f"Database statistics: {stats}")