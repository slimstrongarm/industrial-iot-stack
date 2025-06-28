#!/usr/bin/env python3
"""
CT-086 Agent 3: Network Traffic Analyzer
Advanced traffic monitoring and analysis for Parachute Drop system

This agent provides real-time network traffic analysis, protocol detection,
and security monitoring for industrial network deployments.
"""

import os
import json
import time
import threading
import logging
import socket
import struct
import subprocess
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from collections import defaultdict, deque
import ipaddress
import asyncio
import sqlite3


@dataclass
class NetworkFlow:
    """Network traffic flow information"""
    src_ip: str
    dst_ip: str
    src_port: int
    dst_port: int
    protocol: str
    bytes_sent: int
    bytes_received: int
    packets_sent: int
    packets_received: int
    start_time: datetime
    last_seen: datetime
    duration: timedelta
    flow_state: str  # 'active', 'closed', 'timeout'


@dataclass
class ProtocolStats:
    """Protocol-specific statistics"""
    protocol_name: str
    total_bytes: int
    total_packets: int
    flow_count: int
    average_packet_size: float
    bandwidth_mbps: float
    top_talkers: List[Tuple[str, int]]  # (IP, bytes)


@dataclass
class SecurityAlert:
    """Security monitoring alert"""
    timestamp: datetime
    alert_type: str
    severity: str  # 'low', 'medium', 'high', 'critical'
    source_ip: str
    target_ip: str
    protocol: str
    description: str
    raw_data: Dict[str, Any]


@dataclass
class BandwidthMetrics:
    """Bandwidth utilization metrics"""
    interface: str
    timestamp: datetime
    rx_bytes: int
    tx_bytes: int
    rx_packets: int
    tx_packets: int
    rx_mbps: float
    tx_mbps: float
    utilization_percent: float


class IndustrialProtocolDetector:
    """Detect and analyze industrial protocols"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Industrial protocol signatures
        self.protocol_signatures = {
            'modbus_tcp': {
                'port': 502,
                'signature': b'\x00\x00\x00\x00\x00\x06',  # MBAP header pattern
                'name': 'Modbus TCP'
            },
            'opcua': {
                'port': 4840,
                'signature': b'OPC',
                'name': 'OPC-UA'
            },
            'ethernet_ip': {
                'port': 44818,
                'signature': b'\x65\x00',  # EtherNet/IP header
                'name': 'EtherNet/IP'
            },
            'mqtt': {
                'port': 1883,
                'signature': b'\x10',  # MQTT CONNECT packet
                'name': 'MQTT'
            },
            'bacnet': {
                'port': 47808,
                'signature': b'\x81',  # BACnet/IP header
                'name': 'BACnet/IP'
            },
            'dnp3': {
                'port': 20000,
                'signature': b'\x05\x64',  # DNP3 header
                'name': 'DNP3'
            }
        }
    
    def detect_protocol(self, src_port: int, dst_port: int, payload: bytes) -> Optional[str]:
        """Detect industrial protocol from packet data"""
        for protocol_key, protocol_info in self.protocol_signatures.items():
            # Check port-based detection
            if dst_port == protocol_info['port'] or src_port == protocol_info['port']:
                # Verify with signature if payload available
                if payload and protocol_info['signature'] in payload[:50]:
                    return protocol_info['name']
                elif not payload:  # Port-only detection for encrypted/truncated packets
                    return f"{protocol_info['name']} (port-based)"
        
        # Standard protocols
        standard_protocols = {
            80: 'HTTP',
            443: 'HTTPS',
            22: 'SSH',
            23: 'Telnet',
            53: 'DNS',
            67: 'DHCP',
            161: 'SNMP',
            443: 'HTTPS'
        }
        
        if dst_port in standard_protocols:
            return standard_protocols[dst_port]
        if src_port in standard_protocols:
            return standard_protocols[src_port]
        
        return f"Unknown (port {dst_port})"
    
    def analyze_modbus_packet(self, payload: bytes) -> Dict[str, Any]:
        """Analyze Modbus TCP packet details"""
        if len(payload) < 8:
            return {}
        
        try:
            # Modbus TCP/IP header: Transaction ID (2) + Protocol ID (2) + Length (2) + Unit ID (1) + Function Code (1)
            transaction_id = struct.unpack('>H', payload[0:2])[0]
            protocol_id = struct.unpack('>H', payload[2:4])[0]
            length = struct.unpack('>H', payload[4:6])[0]
            unit_id = payload[6]
            function_code = payload[7]
            
            function_names = {
                1: 'Read Coils',
                2: 'Read Discrete Inputs',
                3: 'Read Holding Registers',
                4: 'Read Input Registers',
                5: 'Write Single Coil',
                6: 'Write Single Register',
                15: 'Write Multiple Coils',
                16: 'Write Multiple Registers'
            }
            
            return {
                'transaction_id': transaction_id,
                'protocol_id': protocol_id,
                'length': length,
                'unit_id': unit_id,
                'function_code': function_code,
                'function_name': function_names.get(function_code, f'Unknown ({function_code})')
            }
        except:
            return {}
    
    def analyze_opcua_packet(self, payload: bytes) -> Dict[str, Any]:
        """Analyze OPC-UA packet details"""
        if len(payload) < 8:
            return {}
        
        try:
            # OPC-UA message header analysis (simplified)
            message_type = payload[0:3].decode('ascii', errors='ignore')
            message_size = struct.unpack('<I', payload[4:8])[0]
            
            return {
                'message_type': message_type,
                'message_size': message_size,
                'is_opcua': message_type in ['HEL', 'ACK', 'ERR', 'MSG']
            }
        except:
            return {}


class NetworkTrafficAnalyzer:
    """
    Comprehensive network traffic analysis system
    """
    
    def __init__(self, interface: str = "eth0"):
        self.interface = interface
        self.logger = logging.getLogger(__name__)
        self.protocol_detector = IndustrialProtocolDetector()
        
        # Data storage
        self.active_flows: Dict[str, NetworkFlow] = {}
        self.protocol_stats: Dict[str, ProtocolStats] = {}
        self.security_alerts: List[SecurityAlert] = []
        self.bandwidth_history: deque = deque(maxlen=1000)  # Keep last 1000 measurements
        
        # Monitoring configuration
        self.monitoring_active = False
        self.monitor_thread = None
        self.database_path = "/home/server/industrial-iot-stack/ct-086-router-system/agent3_traffic_monitoring/traffic_analysis.db"
        
        # Security thresholds
        self.security_thresholds = {
            'max_connections_per_ip': 100,
            'max_bandwidth_mbps': 500,
            'suspicious_port_scan_threshold': 20,
            'modbus_write_threshold': 10  # per minute
        }
        
        # Initialize database
        self._initialize_database()
    
    def _initialize_database(self):
        """Initialize SQLite database for storing traffic data"""
        os.makedirs(os.path.dirname(self.database_path), exist_ok=True)
        
        with sqlite3.connect(self.database_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS network_flows (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    src_ip TEXT,
                    dst_ip TEXT,
                    src_port INTEGER,
                    dst_port INTEGER,
                    protocol TEXT,
                    bytes_sent INTEGER,
                    bytes_received INTEGER,
                    packets_sent INTEGER,
                    packets_received INTEGER,
                    start_time TEXT,
                    duration_seconds REAL,
                    flow_state TEXT
                )
            ''')
            
            conn.execute('''
                CREATE TABLE IF NOT EXISTS protocol_statistics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    protocol_name TEXT,
                    total_bytes INTEGER,
                    total_packets INTEGER,
                    flow_count INTEGER,
                    bandwidth_mbps REAL
                )
            ''')
            
            conn.execute('''
                CREATE TABLE IF NOT EXISTS security_alerts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    alert_type TEXT,
                    severity TEXT,
                    source_ip TEXT,
                    target_ip TEXT,
                    protocol TEXT,
                    description TEXT,
                    raw_data TEXT
                )
            ''')
            
            conn.execute('''
                CREATE TABLE IF NOT EXISTS bandwidth_metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    interface TEXT,
                    rx_bytes INTEGER,
                    tx_bytes INTEGER,
                    rx_packets INTEGER,
                    tx_packets INTEGER,
                    rx_mbps REAL,
                    tx_mbps REAL,
                    utilization_percent REAL
                )
            ''')
    
    def start_monitoring(self):
        """Start network traffic monitoring"""
        if self.monitoring_active:
            self.logger.warning("Monitoring already active")
            return
        
        self.monitoring_active = True
        self.monitor_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
        self.monitor_thread.start()
        
        self.logger.info(f"Started traffic monitoring on interface {self.interface}")
    
    def stop_monitoring(self):
        """Stop network traffic monitoring"""
        self.monitoring_active = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=10)
        
        self.logger.info("Stopped traffic monitoring")
    
    def _monitoring_loop(self):
        """Main monitoring loop"""
        while self.monitoring_active:
            try:
                # Collect interface statistics
                self._collect_interface_stats()
                
                # Collect netstat data for active connections
                self._collect_netstat_data()
                
                # Analyze traffic patterns
                self._analyze_traffic_patterns()
                
                # Clean up old flows
                self._cleanup_old_flows()
                
                # Store data to database
                self._store_periodic_data()
                
                time.sleep(30)  # Monitor every 30 seconds
                
            except Exception as e:
                self.logger.error(f"Error in monitoring loop: {e}")
                time.sleep(60)  # Wait longer on error
    
    def _collect_interface_stats(self):
        """Collect network interface statistics"""
        try:
            # Read interface statistics from /proc/net/dev
            with open('/proc/net/dev', 'r') as f:
                lines = f.readlines()
            
            for line in lines:
                if self.interface in line:
                    parts = line.split()
                    if len(parts) >= 17:
                        timestamp = datetime.now()
                        
                        rx_bytes = int(parts[1])
                        rx_packets = int(parts[2])
                        tx_bytes = int(parts[9])
                        tx_packets = int(parts[10])
                        
                        # Calculate bandwidth if we have previous measurement
                        rx_mbps = 0.0
                        tx_mbps = 0.0
                        utilization = 0.0
                        
                        if self.bandwidth_history:
                            prev_metric = self.bandwidth_history[-1]
                            time_diff = (timestamp - prev_metric.timestamp).total_seconds()
                            
                            if time_diff > 0:
                                rx_mbps = ((rx_bytes - prev_metric.rx_bytes) * 8) / (time_diff * 1_000_000)
                                tx_mbps = ((tx_bytes - prev_metric.tx_bytes) * 8) / (time_diff * 1_000_000)
                                utilization = min(100, ((rx_mbps + tx_mbps) / 1000) * 100)  # Assume 1Gbps interface
                        
                        metric = BandwidthMetrics(
                            interface=self.interface,
                            timestamp=timestamp,
                            rx_bytes=rx_bytes,
                            tx_bytes=tx_bytes,
                            rx_packets=rx_packets,
                            tx_packets=tx_packets,
                            rx_mbps=rx_mbps,
                            tx_mbps=tx_mbps,
                            utilization_percent=utilization
                        )
                        
                        self.bandwidth_history.append(metric)
                        break
                        
        except Exception as e:
            self.logger.error(f"Failed to collect interface stats: {e}")
    
    def _collect_netstat_data(self):
        """Collect active network connections using netstat"""
        try:
            result = subprocess.run(['netstat', '-tuln'], capture_output=True, text=True)
            lines = result.stdout.split('\n')
            
            current_flows = {}
            
            for line in lines:
                if 'LISTEN' in line or 'ESTABLISHED' in line:
                    parts = line.split()
                    if len(parts) >= 4:
                        proto = parts[0]
                        local_addr = parts[3]
                        
                        if ':' in local_addr:
                            local_ip, local_port = local_addr.rsplit(':', 1)
                            
                            # Create flow key
                            flow_key = f"{local_ip}:{local_port}:{proto}"
                            
                            # Detect protocol
                            detected_protocol = self.protocol_detector.detect_protocol(
                                int(local_port), int(local_port), b''
                            )
                            
                            # Update or create flow
                            if flow_key not in self.active_flows:
                                flow = NetworkFlow(
                                    src_ip=local_ip,
                                    dst_ip="",
                                    src_port=int(local_port),
                                    dst_port=0,
                                    protocol=detected_protocol or proto,
                                    bytes_sent=0,
                                    bytes_received=0,
                                    packets_sent=0,
                                    packets_received=0,
                                    start_time=datetime.now(),
                                    last_seen=datetime.now(),
                                    duration=timedelta(),
                                    flow_state='active'
                                )
                                self.active_flows[flow_key] = flow
                            else:
                                self.active_flows[flow_key].last_seen = datetime.now()
                            
                            current_flows[flow_key] = True
            
            # Mark flows as closed if not seen
            for flow_key, flow in self.active_flows.items():
                if flow_key not in current_flows:
                    if flow.flow_state == 'active':
                        flow.flow_state = 'closed'
                        flow.duration = flow.last_seen - flow.start_time
                        
        except Exception as e:
            self.logger.error(f"Failed to collect netstat data: {e}")
    
    def _analyze_traffic_patterns(self):
        """Analyze traffic patterns for security threats"""
        current_time = datetime.now()
        
        # Analyze connection patterns
        ip_connections = defaultdict(int)
        protocol_counts = defaultdict(int)
        
        for flow in self.active_flows.values():
            if flow.flow_state == 'active':
                ip_connections[flow.src_ip] += 1
                protocol_counts[flow.protocol] += 1
        
        # Check for suspicious connection counts
        for ip, count in ip_connections.items():
            if count > self.security_thresholds['max_connections_per_ip']:
                self._create_security_alert(
                    alert_type="high_connection_count",
                    severity="medium",
                    source_ip=ip,
                    target_ip="",
                    protocol="",
                    description=f"High connection count from {ip}: {count} connections"
                )
        
        # Check bandwidth utilization
        if self.bandwidth_history:
            latest_metric = self.bandwidth_history[-1]
            total_bandwidth = latest_metric.rx_mbps + latest_metric.tx_mbps
            
            if total_bandwidth > self.security_thresholds['max_bandwidth_mbps']:
                self._create_security_alert(
                    alert_type="high_bandwidth_usage",
                    severity="high",
                    source_ip="system",
                    target_ip="",
                    protocol="",
                    description=f"High bandwidth usage: {total_bandwidth:.2f} Mbps"
                )
        
        # Update protocol statistics
        self._update_protocol_statistics(protocol_counts)
    
    def _update_protocol_statistics(self, protocol_counts: Dict[str, int]):
        """Update protocol statistics"""
        for protocol, count in protocol_counts.items():
            if protocol not in self.protocol_stats:
                self.protocol_stats[protocol] = ProtocolStats(
                    protocol_name=protocol,
                    total_bytes=0,
                    total_packets=0,
                    flow_count=count,
                    average_packet_size=0.0,
                    bandwidth_mbps=0.0,
                    top_talkers=[]
                )
            else:
                self.protocol_stats[protocol].flow_count = count
    
    def _create_security_alert(self, alert_type: str, severity: str, source_ip: str,
                              target_ip: str, protocol: str, description: str,
                              raw_data: Dict[str, Any] = None):
        """Create a security alert"""
        alert = SecurityAlert(
            timestamp=datetime.now(),
            alert_type=alert_type,
            severity=severity,
            source_ip=source_ip,
            target_ip=target_ip,
            protocol=protocol,
            description=description,
            raw_data=raw_data or {}
        )
        
        self.security_alerts.append(alert)
        self.logger.warning(f"Security Alert [{severity}]: {alert_type} - {description}")
        
        # Store in database
        with sqlite3.connect(self.database_path) as conn:
            conn.execute('''
                INSERT INTO security_alerts 
                (timestamp, alert_type, severity, source_ip, target_ip, protocol, description, raw_data)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                alert.timestamp.isoformat(),
                alert.alert_type,
                alert.severity,
                alert.source_ip,
                alert.target_ip,
                alert.protocol,
                alert.description,
                json.dumps(alert.raw_data)
            ))
    
    def _cleanup_old_flows(self):
        """Clean up old inactive flows"""
        current_time = datetime.now()
        timeout_threshold = timedelta(minutes=30)
        
        expired_flows = []
        for flow_key, flow in self.active_flows.items():
            if current_time - flow.last_seen > timeout_threshold:
                flow.flow_state = 'timeout'
                flow.duration = flow.last_seen - flow.start_time
                expired_flows.append(flow_key)
        
        # Store expired flows in database
        for flow_key in expired_flows:
            flow = self.active_flows[flow_key]
            self._store_flow_to_database(flow)
            del self.active_flows[flow_key]
    
    def _store_flow_to_database(self, flow: NetworkFlow):
        """Store network flow to database"""
        with sqlite3.connect(self.database_path) as conn:
            conn.execute('''
                INSERT INTO network_flows 
                (src_ip, dst_ip, src_port, dst_port, protocol, bytes_sent, bytes_received,
                 packets_sent, packets_received, start_time, duration_seconds, flow_state)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                flow.src_ip,
                flow.dst_ip,
                flow.src_port,
                flow.dst_port,
                flow.protocol,
                flow.bytes_sent,
                flow.bytes_received,
                flow.packets_sent,
                flow.packets_received,
                flow.start_time.isoformat(),
                flow.duration.total_seconds(),
                flow.flow_state
            ))
    
    def _store_periodic_data(self):
        """Store periodic statistics to database"""
        current_time = datetime.now()
        
        # Store protocol statistics
        with sqlite3.connect(self.database_path) as conn:
            for protocol, stats in self.protocol_stats.items():
                conn.execute('''
                    INSERT INTO protocol_statistics 
                    (timestamp, protocol_name, total_bytes, total_packets, flow_count, bandwidth_mbps)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    current_time.isoformat(),
                    stats.protocol_name,
                    stats.total_bytes,
                    stats.total_packets,
                    stats.flow_count,
                    stats.bandwidth_mbps
                ))
            
            # Store bandwidth metrics
            if self.bandwidth_history:
                latest_metric = self.bandwidth_history[-1]
                conn.execute('''
                    INSERT INTO bandwidth_metrics 
                    (timestamp, interface, rx_bytes, tx_bytes, rx_packets, tx_packets,
                     rx_mbps, tx_mbps, utilization_percent)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    latest_metric.timestamp.isoformat(),
                    latest_metric.interface,
                    latest_metric.rx_bytes,
                    latest_metric.tx_bytes,
                    latest_metric.rx_packets,
                    latest_metric.tx_packets,
                    latest_metric.rx_mbps,
                    latest_metric.tx_mbps,
                    latest_metric.utilization_percent
                ))
    
    def get_monitoring_summary(self) -> Dict[str, Any]:
        """Get comprehensive monitoring summary"""
        current_time = datetime.now()
        
        # Calculate summary statistics
        active_flow_count = sum(1 for flow in self.active_flows.values() if flow.flow_state == 'active')
        protocol_distribution = {}
        
        for flow in self.active_flows.values():
            if flow.flow_state == 'active':
                protocol_distribution[flow.protocol] = protocol_distribution.get(flow.protocol, 0) + 1
        
        # Recent security alerts (last hour)
        recent_alerts = [
            alert for alert in self.security_alerts
            if (current_time - alert.timestamp).total_seconds() < 3600
        ]
        
        # Current bandwidth
        current_bandwidth = {"rx_mbps": 0.0, "tx_mbps": 0.0, "utilization": 0.0}
        if self.bandwidth_history:
            latest = self.bandwidth_history[-1]
            current_bandwidth = {
                "rx_mbps": latest.rx_mbps,
                "tx_mbps": latest.tx_mbps,
                "utilization": latest.utilization_percent
            }
        
        return {
            "monitoring_status": "active" if self.monitoring_active else "stopped",
            "interface": self.interface,
            "timestamp": current_time.isoformat(),
            "active_flows": active_flow_count,
            "protocol_distribution": protocol_distribution,
            "recent_alerts": len(recent_alerts),
            "current_bandwidth": current_bandwidth,
            "database_path": self.database_path,
            "security_thresholds": self.security_thresholds,
            "total_protocols_detected": len(self.protocol_stats)
        }
    
    def deploy_parachute_drop_monitoring(self) -> Dict[str, Any]:
        """Deploy monitoring for Parachute Drop system"""
        try:
            self.logger.info("Deploying Parachute Drop traffic monitoring...")
            
            # Configure monitoring for industrial protocols
            self.security_thresholds.update({
                'modbus_connections_per_ip': 10,
                'opcua_sessions_per_ip': 5,
                'mqtt_connections_per_ip': 50,
                'industrial_bandwidth_threshold': 100  # Mbps
            })
            
            # Start monitoring
            self.start_monitoring()
            
            # Create initial configuration
            config = {
                "deployment_time": datetime.now().isoformat(),
                "interface": self.interface,
                "monitoring_active": True,
                "industrial_protocol_monitoring": True,
                "security_monitoring": True,
                "database_enabled": True,
                "thresholds": self.security_thresholds
            }
            
            # Save configuration
            config_path = "/home/server/industrial-iot-stack/ct-086-router-system/agent3_traffic_monitoring/monitoring_config.json"
            with open(config_path, 'w') as f:
                json.dump(config, f, indent=2)
            
            self.logger.info("Parachute Drop traffic monitoring deployed successfully")
            return config
            
        except Exception as e:
            self.logger.error(f"Failed to deploy traffic monitoring: {e}")
            raise


def main():
    """Test network traffic analyzer"""
    logging.basicConfig(level=logging.INFO)
    
    analyzer = NetworkTrafficAnalyzer(interface="eth0")
    
    print("📊 Network Traffic Analyzer for Parachute Drop System")
    print("=" * 60)
    
    try:
        # Deploy monitoring
        config = analyzer.deploy_parachute_drop_monitoring()
        print("✅ Traffic monitoring deployed successfully!")
        
        # Wait for some data collection
        print("📡 Collecting traffic data...")
        time.sleep(30)
        
        # Get monitoring summary
        summary = analyzer.get_monitoring_summary()
        print(f"\n📈 Monitoring Summary:")
        print(f"  Status: {summary['monitoring_status']}")
        print(f"  Interface: {summary['interface']}")
        print(f"  Active Flows: {summary['active_flows']}")
        print(f"  Protocols Detected: {summary['total_protocols_detected']}")
        print(f"  Recent Alerts: {summary['recent_alerts']}")
        print(f"  Bandwidth: {summary['current_bandwidth']['rx_mbps']:.2f} Mbps RX, {summary['current_bandwidth']['tx_mbps']:.2f} Mbps TX")
        
        # Stop monitoring
        analyzer.stop_monitoring()
        print("\n🛑 Monitoring stopped")
        
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()