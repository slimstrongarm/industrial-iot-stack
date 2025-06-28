#!/usr/bin/env python3
"""
CT-086 Agent 4: Security Hardening System
Comprehensive security hardening for Parachute Drop router system

This module implements enterprise-grade security hardening including
firewall configuration, intrusion detection, and security monitoring.
"""

import os
import json
import subprocess
import logging
import time
import threading
from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from enum import Enum
import ipaddress
import re


class ThreatLevel(Enum):
    """Security threat levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class SecurityRule(Enum):
    """Security rule types"""
    FIREWALL = "firewall"
    INTRUSION_DETECTION = "intrusion_detection"
    ACCESS_CONTROL = "access_control"
    RATE_LIMITING = "rate_limiting"
    MALWARE_DETECTION = "malware_detection"


@dataclass
class SecurityEvent:
    """Security event record"""
    timestamp: datetime
    event_type: str
    threat_level: ThreatLevel
    source_ip: str
    target_ip: str
    protocol: str
    port: int
    description: str
    action_taken: str
    raw_data: Dict[str, Any]


@dataclass
class FirewallRule:
    """Firewall rule configuration"""
    rule_id: str
    chain: str  # INPUT, OUTPUT, FORWARD
    action: str  # ACCEPT, DROP, REJECT
    protocol: str
    source_ip: str
    destination_ip: str
    source_port: Optional[int]
    destination_port: Optional[int]
    description: str
    enabled: bool = True


@dataclass
class IntrusionSignature:
    """Intrusion detection signature"""
    signature_id: str
    name: str
    pattern: str
    protocol: str
    severity: ThreatLevel
    description: str
    action: str  # log, block, alert
    enabled: bool = True


class SecurityHardeningManager:
    """
    Comprehensive security hardening system
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.config_dir = "/home/server/industrial-iot-stack/ct-086-router-system/agent4_remote_access_security"
        
        # Security state
        self.firewall_rules: List[FirewallRule] = []
        self.intrusion_signatures: List[IntrusionSignature] = []
        self.security_events: List[SecurityEvent] = []
        self.blocked_ips: Set[str] = set()
        self.rate_limits: Dict[str, List[datetime]] = {}
        
        # Monitoring state
        self.monitoring_active = False
        self.monitor_thread = None
        
        # Industrial security policies
        self.industrial_policies = {
            "allowed_industrial_protocols": [502, 4840, 1883, 44818, 47808],  # Modbus, OPC-UA, MQTT, EtherNet/IP, BACnet
            "management_networks": ["192.168.10.0/24"],
            "industrial_networks": ["192.168.20.0/24"],
            "monitoring_networks": ["192.168.30.0/24"],
            "guest_networks": ["192.168.40.0/24"],
            "max_connections_per_ip": 50,
            "rate_limit_threshold": 100,  # requests per minute
            "suspicious_port_scan_threshold": 10
        }
        
        # Initialize security components
        self._initialize_firewall_rules()
        self._initialize_intrusion_signatures()
    
    def _initialize_firewall_rules(self):
        """Initialize default firewall rules"""
        default_rules = [
            # Allow loopback
            FirewallRule(
                rule_id="fw_001",
                chain="INPUT",
                action="ACCEPT",
                protocol="all",
                source_ip="127.0.0.1",
                destination_ip="127.0.0.1",
                source_port=None,
                destination_port=None,
                description="Allow loopback traffic"
            ),
            
            # Allow established connections
            FirewallRule(
                rule_id="fw_002",
                chain="INPUT",
                action="ACCEPT",
                protocol="all",
                source_ip="0.0.0.0/0",
                destination_ip="0.0.0.0/0",
                source_port=None,
                destination_port=None,
                description="Allow established connections"
            ),
            
            # Allow SSH from management network
            FirewallRule(
                rule_id="fw_003",
                chain="INPUT",
                action="ACCEPT",
                protocol="tcp",
                source_ip="192.168.10.0/24",
                destination_ip="0.0.0.0/0",
                source_port=None,
                destination_port=22,
                description="Allow SSH from management network"
            ),
            
            # Allow HTTPS from management network
            FirewallRule(
                rule_id="fw_004",
                chain="INPUT",
                action="ACCEPT",
                protocol="tcp",
                source_ip="192.168.10.0/24",
                destination_ip="0.0.0.0/0",
                source_port=None,
                destination_port=443,
                description="Allow HTTPS from management network"
            ),
            
            # Allow VPN traffic
            FirewallRule(
                rule_id="fw_005",
                chain="INPUT",
                action="ACCEPT",
                protocol="udp",
                source_ip="0.0.0.0/0",
                destination_ip="0.0.0.0/0",
                source_port=None,
                destination_port=51820,
                description="Allow WireGuard VPN"
            ),
            
            # Allow industrial protocols within industrial network
            FirewallRule(
                rule_id="fw_006",
                chain="FORWARD",
                action="ACCEPT",
                protocol="tcp",
                source_ip="192.168.20.0/24",
                destination_ip="192.168.20.0/24",
                source_port=None,
                destination_port=502,
                description="Allow Modbus within industrial network"
            ),
            
            # Block all other traffic by default
            FirewallRule(
                rule_id="fw_999",
                chain="INPUT",
                action="DROP",
                protocol="all",
                source_ip="0.0.0.0/0",
                destination_ip="0.0.0.0/0",
                source_port=None,
                destination_port=None,
                description="Default drop rule"
            )
        ]
        
        self.firewall_rules = default_rules
    
    def _initialize_intrusion_signatures(self):
        """Initialize intrusion detection signatures"""
        default_signatures = [
            IntrusionSignature(
                signature_id="ids_001",
                name="Port Scan Detection",
                pattern="multiple_ports_same_source",
                protocol="tcp",
                severity=ThreatLevel.MEDIUM,
                description="Detect port scanning attempts",
                action="log"
            ),
            
            IntrusionSignature(
                signature_id="ids_002",
                name="Brute Force SSH",
                pattern="multiple_ssh_failures",
                protocol="tcp",
                severity=ThreatLevel.HIGH,
                description="Detect SSH brute force attacks",
                action="block"
            ),
            
            IntrusionSignature(
                signature_id="ids_003",
                name="Suspicious Modbus Traffic",
                pattern="modbus_write_commands",
                protocol="tcp",
                severity=ThreatLevel.HIGH,
                description="Detect suspicious Modbus write operations",
                action="alert"
            ),
            
            IntrusionSignature(
                signature_id="ids_004",
                name="Unauthorized Network Access",
                pattern="cross_vlan_traffic",
                protocol="all",
                severity=ThreatLevel.MEDIUM,
                description="Detect unauthorized cross-VLAN traffic",
                action="log"
            ),
            
            IntrusionSignature(
                signature_id="ids_005",
                name="DDoS Attack",
                pattern="high_connection_rate",
                protocol="all",
                severity=ThreatLevel.CRITICAL,
                description="Detect DDoS attacks",
                action="block"
            )
        ]
        
        self.intrusion_signatures = default_signatures
    
    def apply_firewall_rules(self) -> bool:
        """Apply firewall rules using iptables"""
        try:
            self.logger.info("Applying firewall rules...")
            
            # Flush existing rules
            subprocess.run(["iptables", "-F"], check=True)
            subprocess.run(["iptables", "-X"], check=True)
            
            # Set default policies
            subprocess.run(["iptables", "-P", "INPUT", "DROP"], check=True)
            subprocess.run(["iptables", "-P", "FORWARD", "DROP"], check=True)
            subprocess.run(["iptables", "-P", "OUTPUT", "ACCEPT"], check=True)
            
            # Apply rules
            for rule in self.firewall_rules:
                if not rule.enabled:
                    continue
                
                cmd = ["iptables", "-A", rule.chain]
                
                # Protocol
                if rule.protocol != "all":
                    cmd.extend(["-p", rule.protocol])
                
                # Source IP
                if rule.source_ip != "0.0.0.0/0":
                    cmd.extend(["-s", rule.source_ip])
                
                # Destination IP
                if rule.destination_ip != "0.0.0.0/0":
                    cmd.extend(["-d", rule.destination_ip])
                
                # Source port
                if rule.source_port:
                    cmd.extend(["--sport", str(rule.source_port)])
                
                # Destination port
                if rule.destination_port:
                    cmd.extend(["--dport", str(rule.destination_port)])
                
                # Special handling for established connections
                if "established" in rule.description.lower():
                    cmd.extend(["-m", "state", "--state", "ESTABLISHED,RELATED"])
                
                # Action
                cmd.extend(["-j", rule.action])
                
                # Apply rule
                subprocess.run(cmd, check=True)
                self.logger.debug(f"Applied firewall rule: {rule.rule_id}")
            
            # Save rules
            subprocess.run(["iptables-save"], check=True)
            
            self.logger.info(f"Applied {len(self.firewall_rules)} firewall rules")
            return True
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to apply firewall rules: {e}")
            return False
        except Exception as e:
            self.logger.error(f"Firewall configuration error: {e}")
            return False
    
    def add_firewall_rule(self, rule: FirewallRule) -> bool:
        """Add a new firewall rule"""
        try:
            # Check for duplicate rule IDs
            if any(r.rule_id == rule.rule_id for r in self.firewall_rules):
                raise ValueError(f"Rule ID {rule.rule_id} already exists")
            
            self.firewall_rules.append(rule)
            self.logger.info(f"Added firewall rule: {rule.rule_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to add firewall rule: {e}")
            return False
    
    def block_ip_address(self, ip_address: str, reason: str = "Security threat") -> bool:
        """Block an IP address"""
        try:
            # Validate IP address
            ipaddress.ip_address(ip_address)
            
            # Add to blocked set
            self.blocked_ips.add(ip_address)
            
            # Add iptables rule
            subprocess.run([
                "iptables", "-I", "INPUT", "1",
                "-s", ip_address,
                "-j", "DROP",
                "-m", "comment", "--comment", f"Blocked: {reason}"
            ], check=True)
            
            # Log security event
            self._log_security_event(
                event_type="ip_blocked",
                threat_level=ThreatLevel.HIGH,
                source_ip=ip_address,
                target_ip="",
                protocol="",
                port=0,
                description=f"IP address blocked: {reason}",
                action_taken="blocked"
            )
            
            self.logger.warning(f"Blocked IP address {ip_address}: {reason}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to block IP {ip_address}: {e}")
            return False
    
    def unblock_ip_address(self, ip_address: str) -> bool:
        """Unblock an IP address"""
        try:
            # Remove from blocked set
            self.blocked_ips.discard(ip_address)
            
            # Remove iptables rule
            subprocess.run([
                "iptables", "-D", "INPUT",
                "-s", ip_address,
                "-j", "DROP"
            ], check=False)  # Don't fail if rule doesn't exist
            
            self.logger.info(f"Unblocked IP address: {ip_address}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to unblock IP {ip_address}: {e}")
            return False
    
    def start_intrusion_monitoring(self):
        """Start intrusion detection monitoring"""
        if self.monitoring_active:
            self.logger.warning("Intrusion monitoring already active")
            return
        
        self.monitoring_active = True
        self.monitor_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
        self.monitor_thread.start()
        
        self.logger.info("Started intrusion detection monitoring")
    
    def stop_intrusion_monitoring(self):
        """Stop intrusion detection monitoring"""
        self.monitoring_active = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=10)
        
        self.logger.info("Stopped intrusion detection monitoring")
    
    def _monitoring_loop(self):
        """Main intrusion detection monitoring loop"""
        while self.monitoring_active:
            try:
                # Monitor system logs for suspicious activity
                self._analyze_system_logs()
                
                # Monitor network connections
                self._analyze_network_connections()
                
                # Check rate limits
                self._check_rate_limits()
                
                # Clean up old events
                self._cleanup_old_events()
                
                time.sleep(30)  # Check every 30 seconds
                
            except Exception as e:
                self.logger.error(f"Intrusion monitoring error: {e}")
                time.sleep(60)  # Wait longer on error
    
    def _analyze_system_logs(self):
        """Analyze system logs for security events"""
        try:
            # Analyze auth.log for failed login attempts
            auth_log_path = "/var/log/auth.log"
            if os.path.exists(auth_log_path):
                self._analyze_auth_log(auth_log_path)
            
            # Analyze syslog for network events
            syslog_path = "/var/log/syslog"
            if os.path.exists(syslog_path):
                self._analyze_syslog(syslog_path)
                
        except Exception as e:
            self.logger.error(f"Failed to analyze system logs: {e}")
    
    def _analyze_auth_log(self, log_path: str):
        """Analyze authentication log for suspicious activity"""
        try:
            # Read recent entries (last 100 lines)
            result = subprocess.run(["tail", "-n", "100", log_path], 
                                  capture_output=True, text=True)
            
            failed_attempts = {}
            ssh_patterns = [
                r"Failed password for .* from (\d+\.\d+\.\d+\.\d+)",
                r"Invalid user .* from (\d+\.\d+\.\d+\.\d+)",
                r"Connection closed by (\d+\.\d+\.\d+\.\d+)"
            ]
            
            for line in result.stdout.split('\n'):
                for pattern in ssh_patterns:
                    match = re.search(pattern, line)
                    if match:
                        ip = match.group(1)
                        failed_attempts[ip] = failed_attempts.get(ip, 0) + 1
            
            # Check for brute force attempts
            for ip, count in failed_attempts.items():
                if count >= 5:  # 5 or more failed attempts
                    self._handle_brute_force_attempt(ip, count)
                    
        except Exception as e:
            self.logger.error(f"Failed to analyze auth log: {e}")
    
    def _analyze_syslog(self, log_path: str):
        """Analyze system log for network events"""
        try:
            # Read recent entries
            result = subprocess.run(["tail", "-n", "50", log_path], 
                                  capture_output=True, text=True)
            
            # Look for network-related security events
            for line in result.stdout.split('\n'):
                if "kernel:" in line and "DROP" in line:
                    # Parse dropped packet information
                    self._parse_dropped_packet(line)
                    
        except Exception as e:
            self.logger.error(f"Failed to analyze syslog: {e}")
    
    def _analyze_network_connections(self):
        """Analyze current network connections"""
        try:
            # Get current connections
            result = subprocess.run(["netstat", "-tuln"], capture_output=True, text=True)
            
            connection_counts = {}
            for line in result.stdout.split('\n'):
                if 'ESTABLISHED' in line:
                    parts = line.split()
                    if len(parts) >= 5:
                        foreign_addr = parts[4]
                        if ':' in foreign_addr:
                            ip = foreign_addr.split(':')[0]
                            connection_counts[ip] = connection_counts.get(ip, 0) + 1
            
            # Check for excessive connections
            for ip, count in connection_counts.items():
                if count > self.industrial_policies["max_connections_per_ip"]:
                    self._handle_excessive_connections(ip, count)
                    
        except Exception as e:
            self.logger.error(f"Failed to analyze network connections: {e}")
    
    def _check_rate_limits(self):
        """Check and enforce rate limits"""
        current_time = datetime.now()
        cutoff_time = current_time - timedelta(minutes=1)
        
        # Clean old entries
        for ip in list(self.rate_limits.keys()):
            self.rate_limits[ip] = [
                timestamp for timestamp in self.rate_limits[ip]
                if timestamp > cutoff_time
            ]
            
            # Check for rate limit violations
            if len(self.rate_limits[ip]) > self.industrial_policies["rate_limit_threshold"]:
                self._handle_rate_limit_violation(ip, len(self.rate_limits[ip]))
    
    def _handle_brute_force_attempt(self, ip_address: str, attempt_count: int):
        """Handle detected brute force attempt"""
        self.block_ip_address(ip_address, f"Brute force attack: {attempt_count} attempts")
        
        self._log_security_event(
            event_type="brute_force_attack",
            threat_level=ThreatLevel.HIGH,
            source_ip=ip_address,
            target_ip="",
            protocol="ssh",
            port=22,
            description=f"Brute force attack detected: {attempt_count} failed attempts",
            action_taken="ip_blocked"
        )
    
    def _handle_excessive_connections(self, ip_address: str, connection_count: int):
        """Handle excessive connection attempts"""
        if connection_count > self.industrial_policies["max_connections_per_ip"] * 2:
            self.block_ip_address(ip_address, f"Excessive connections: {connection_count}")
        
        self._log_security_event(
            event_type="excessive_connections",
            threat_level=ThreatLevel.MEDIUM,
            source_ip=ip_address,
            target_ip="",
            protocol="",
            port=0,
            description=f"Excessive connections detected: {connection_count}",
            action_taken="monitored" if connection_count <= self.industrial_policies["max_connections_per_ip"] * 2 else "blocked"
        )
    
    def _handle_rate_limit_violation(self, ip_address: str, request_count: int):
        """Handle rate limit violations"""
        self._log_security_event(
            event_type="rate_limit_violation",
            threat_level=ThreatLevel.MEDIUM,
            source_ip=ip_address,
            target_ip="",
            protocol="",
            port=0,
            description=f"Rate limit violation: {request_count} requests per minute",
            action_taken="rate_limited"
        )
    
    def _parse_dropped_packet(self, log_line: str):
        """Parse dropped packet log entry"""
        try:
            # Extract IP addresses and ports from kernel log
            src_match = re.search(r"SRC=(\d+\.\d+\.\d+\.\d+)", log_line)
            dst_match = re.search(r"DST=(\d+\.\d+\.\d+\.\d+)", log_line)
            dpt_match = re.search(r"DPT=(\d+)", log_line)
            proto_match = re.search(r"PROTO=(\w+)", log_line)
            
            if src_match and dst_match:
                src_ip = src_match.group(1)
                dst_ip = dst_match.group(1)
                port = int(dpt_match.group(1)) if dpt_match else 0
                protocol = proto_match.group(1).lower() if proto_match else "unknown"
                
                self._log_security_event(
                    event_type="packet_dropped",
                    threat_level=ThreatLevel.LOW,
                    source_ip=src_ip,
                    target_ip=dst_ip,
                    protocol=protocol,
                    port=port,
                    description="Packet dropped by firewall",
                    action_taken="dropped"
                )
                
        except Exception as e:
            self.logger.debug(f"Failed to parse dropped packet log: {e}")
    
    def _log_security_event(self, event_type: str, threat_level: ThreatLevel,
                           source_ip: str, target_ip: str, protocol: str,
                           port: int, description: str, action_taken: str):
        """Log a security event"""
        event = SecurityEvent(
            timestamp=datetime.now(),
            event_type=event_type,
            threat_level=threat_level,
            source_ip=source_ip,
            target_ip=target_ip,
            protocol=protocol,
            port=port,
            description=description,
            action_taken=action_taken,
            raw_data={}
        )
        
        self.security_events.append(event)
        
        # Log based on threat level
        if threat_level == ThreatLevel.CRITICAL:
            self.logger.critical(f"SECURITY: {event_type} - {description}")
        elif threat_level == ThreatLevel.HIGH:
            self.logger.error(f"SECURITY: {event_type} - {description}")
        elif threat_level == ThreatLevel.MEDIUM:
            self.logger.warning(f"SECURITY: {event_type} - {description}")
        else:
            self.logger.info(f"SECURITY: {event_type} - {description}")
    
    def _cleanup_old_events(self):
        """Clean up old security events"""
        cutoff_time = datetime.now() - timedelta(days=7)
        self.security_events = [
            event for event in self.security_events
            if event.timestamp > cutoff_time
        ]
    
    def get_security_status(self) -> Dict[str, Any]:
        """Get comprehensive security status"""
        recent_events = [
            event for event in self.security_events
            if (datetime.now() - event.timestamp).total_seconds() < 3600
        ]
        
        threat_counts = {}
        for threat in ThreatLevel:
            threat_counts[threat.value] = sum(
                1 for event in recent_events
                if event.threat_level == threat
            )
        
        return {
            "monitoring_active": self.monitoring_active,
            "firewall_rules_count": len(self.firewall_rules),
            "intrusion_signatures_count": len(self.intrusion_signatures),
            "blocked_ips_count": len(self.blocked_ips),
            "recent_events_count": len(recent_events),
            "threat_distribution": threat_counts,
            "policies": self.industrial_policies,
            "timestamp": datetime.now().isoformat()
        }
    
    def deploy_parachute_drop_security(self) -> Dict[str, Any]:
        """Deploy complete security hardening for Parachute Drop system"""
        try:
            self.logger.info("Deploying Parachute Drop security hardening...")
            
            # Apply firewall rules
            if not self.apply_firewall_rules():
                raise Exception("Failed to apply firewall rules")
            
            # Start intrusion monitoring
            self.start_intrusion_monitoring()
            
            # Save configuration
            config = {
                "deployment_time": datetime.now().isoformat(),
                "firewall_rules": [asdict(rule) for rule in self.firewall_rules],
                "intrusion_signatures": [asdict(sig) for sig in self.intrusion_signatures],
                "industrial_policies": self.industrial_policies,
                "monitoring_active": self.monitoring_active,
                "security_features": [
                    "Firewall protection",
                    "Intrusion detection",
                    "Rate limiting",
                    "IP blocking",
                    "Security event logging"
                ]
            }
            
            config_path = f"{self.config_dir}/security_deployment.json"
            with open(config_path, 'w') as f:
                json.dump(config, f, indent=2)
            
            self.logger.info("Parachute Drop security hardening deployed successfully")
            return config
            
        except Exception as e:
            self.logger.error(f"Security deployment failed: {e}")
            raise


def main():
    """Test security hardening system"""
    logging.basicConfig(level=logging.INFO)
    
    security_manager = SecurityHardeningManager()
    
    print("🛡️ Security Hardening for Parachute Drop System")
    print("=" * 55)
    
    try:
        # Deploy security hardening
        config = security_manager.deploy_parachute_drop_security()
        print("✅ Security hardening deployed successfully!")
        
        print(f"\n🔥 Firewall Rules: {len(config['firewall_rules'])}")
        print(f"🔍 Intrusion Signatures: {len(config['intrusion_signatures'])}")
        print(f"📊 Monitoring Active: {config['monitoring_active']}")
        print(f"🏭 Industrial Policies: {len(config['industrial_policies'])}")
        
        # Get security status
        status = security_manager.get_security_status()
        print(f"\n📈 Security Status:")
        print(f"  Blocked IPs: {status['blocked_ips_count']}")
        print(f"  Recent Events: {status['recent_events_count']}")
        print(f"  Threat Distribution: {status['threat_distribution']}")
        
        # Run for a short time to demonstrate
        print(f"\n🔍 Running security monitoring...")
        time.sleep(10)
        
        # Stop monitoring
        security_manager.stop_intrusion_monitoring()
        print("🛑 Security monitoring stopped")
        
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()