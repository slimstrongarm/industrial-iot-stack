#!/usr/bin/env python3
"""
CT-086 Agent 2: Secure Tunnel Controller
Advanced tunnel management with security monitoring and automatic failover

This module provides enterprise-grade VPN tunnel management with
security monitoring, automatic failover, and threat detection.
"""

import os
import json
import time
import threading
import subprocess
import psutil
import logging
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from enum import Enum
import hashlib
import hmac
import socket
import ssl


class TunnelState(Enum):
    """Tunnel connection states"""
    DISCONNECTED = "disconnected"
    CONNECTING = "connecting"
    CONNECTED = "connected"
    RECONNECTING = "reconnecting"
    FAILED = "failed"
    DISABLED = "disabled"


class SecurityThreat(Enum):
    """Security threat levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class TunnelMetrics:
    """Tunnel performance metrics"""
    bytes_sent: int
    bytes_received: int
    packets_sent: int
    packets_received: int
    latency_ms: float
    packet_loss_percent: float
    connection_uptime: timedelta
    last_handshake: datetime
    throughput_mbps: float


@dataclass
class SecurityEvent:
    """Security event logging"""
    timestamp: datetime
    event_type: str
    threat_level: SecurityThreat
    source_ip: str
    description: str
    action_taken: str
    tunnel_name: str


@dataclass
class TunnelConnection:
    """Tunnel connection information"""
    name: str
    protocol: str
    state: TunnelState
    local_endpoint: str
    remote_endpoint: str
    metrics: TunnelMetrics
    last_update: datetime
    config_hash: str
    is_primary: bool = False
    failover_priority: int = 0


class TunnelHealthMonitor:
    """Monitor tunnel health and performance"""
    
    def __init__(self, tunnel_name: str):
        self.tunnel_name = tunnel_name
        self.logger = logging.getLogger(__name__)
        self.health_checks = []
        self.monitoring = False
        self.monitor_thread = None
        
    def add_health_check(self, check_func: Callable[[], bool], interval: int = 30):
        """Add a health check function"""
        self.health_checks.append({
            "function": check_func,
            "interval": interval,
            "last_run": datetime.min,
            "last_result": False
        })
    
    def ping_test(self, target_ip: str, timeout: int = 5) -> bool:
        """Ping connectivity test"""
        try:
            result = subprocess.run(
                ["ping", "-c", "1", "-W", str(timeout), target_ip],
                capture_output=True,
                text=True
            )
            return result.returncode == 0
        except:
            return False
    
    def bandwidth_test(self, target_ip: str, port: int = 80) -> float:
        """Simple bandwidth test"""
        try:
            start_time = time.time()
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            result = sock.connect_ex((target_ip, port))
            end_time = time.time()
            sock.close()
            
            if result == 0:
                return (end_time - start_time) * 1000  # Return latency in ms
            return float('inf')
        except:
            return float('inf')
    
    def start_monitoring(self):
        """Start health monitoring"""
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
        self.logger.info(f"Health monitoring started for {self.tunnel_name}")
    
    def stop_monitoring(self):
        """Stop health monitoring"""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=10)
        self.logger.info(f"Health monitoring stopped for {self.tunnel_name}")
    
    def _monitor_loop(self):
        """Main monitoring loop"""
        while self.monitoring:
            current_time = datetime.now()
            
            for check in self.health_checks:
                if (current_time - check["last_run"]).seconds >= check["interval"]:
                    try:
                        result = check["function"]()
                        check["last_result"] = result
                        check["last_run"] = current_time
                        
                        if not result:
                            self.logger.warning(f"Health check failed for {self.tunnel_name}")
                    except Exception as e:
                        self.logger.error(f"Health check error for {self.tunnel_name}: {e}")
                        check["last_result"] = False
            
            time.sleep(10)  # Check every 10 seconds
    
    def get_health_status(self) -> Dict[str, Any]:
        """Get current health status"""
        all_healthy = all(check["last_result"] for check in self.health_checks)
        
        return {
            "tunnel_name": self.tunnel_name,
            "overall_health": "healthy" if all_healthy else "unhealthy",
            "checks": [
                {
                    "last_run": check["last_run"].isoformat(),
                    "result": check["last_result"],
                    "interval": check["interval"]
                }
                for check in self.health_checks
            ],
            "timestamp": datetime.now().isoformat()
        }


class SecurityMonitor:
    """Monitor tunnel security and detect threats"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.security_events: List[SecurityEvent] = []
        self.blocked_ips: set = set()
        self.rate_limits: Dict[str, List[datetime]] = {}
        self.monitoring = False
        
    def detect_brute_force(self, source_ip: str, max_attempts: int = 5, window_minutes: int = 15) -> bool:
        """Detect brute force authentication attempts"""
        current_time = datetime.now()
        
        if source_ip not in self.rate_limits:
            self.rate_limits[source_ip] = []
        
        # Clean old attempts
        cutoff_time = current_time - timedelta(minutes=window_minutes)
        self.rate_limits[source_ip] = [
            attempt for attempt in self.rate_limits[source_ip] 
            if attempt > cutoff_time
        ]
        
        # Add current attempt
        self.rate_limits[source_ip].append(current_time)
        
        # Check if threshold exceeded
        if len(self.rate_limits[source_ip]) > max_attempts:
            self.log_security_event(
                event_type="brute_force_detected",
                threat_level=SecurityThreat.HIGH,
                source_ip=source_ip,
                description=f"Brute force detected: {len(self.rate_limits[source_ip])} attempts in {window_minutes} minutes"
            )
            return True
        
        return False
    
    def check_ip_reputation(self, ip_address: str) -> SecurityThreat:
        """Check IP address reputation (simplified)"""
        # In production, this would integrate with threat intelligence feeds
        suspicious_ranges = [
            "10.0.0.0/8",    # Private networks (if unexpected)
            "172.16.0.0/12", # Private networks (if unexpected)
            "192.168.0.0/16" # Private networks (if unexpected)
        ]
        
        # Simple reputation check based on known bad patterns
        if any(char in ip_address for char in [".", ":", "/"]):
            # Placeholder for real reputation checks
            return SecurityThreat.LOW
        
        return SecurityThreat.LOW
    
    def analyze_traffic_patterns(self, tunnel_metrics: TunnelMetrics) -> List[SecurityEvent]:
        """Analyze traffic patterns for anomalies"""
        events = []
        
        # Detect unusual traffic volume
        if tunnel_metrics.throughput_mbps > 100:  # Threshold for suspicious activity
            events.append(SecurityEvent(
                timestamp=datetime.now(),
                event_type="high_traffic_volume",
                threat_level=SecurityThreat.MEDIUM,
                source_ip="tunnel",
                description=f"High traffic volume detected: {tunnel_metrics.throughput_mbps} Mbps",
                action_taken="monitoring",
                tunnel_name="unknown"
            ))
        
        # Detect high packet loss (possible attack)
        if tunnel_metrics.packet_loss_percent > 10:
            events.append(SecurityEvent(
                timestamp=datetime.now(),
                event_type="high_packet_loss",
                threat_level=SecurityThreat.MEDIUM,
                source_ip="tunnel",
                description=f"High packet loss detected: {tunnel_metrics.packet_loss_percent}%",
                action_taken="investigating",
                tunnel_name="unknown"
            ))
        
        return events
    
    def log_security_event(self, event_type: str, threat_level: SecurityThreat, 
                          source_ip: str, description: str, tunnel_name: str = "unknown",
                          action_taken: str = "logged"):
        """Log a security event"""
        event = SecurityEvent(
            timestamp=datetime.now(),
            event_type=event_type,
            threat_level=threat_level,
            source_ip=source_ip,
            description=description,
            action_taken=action_taken,
            tunnel_name=tunnel_name
        )
        
        self.security_events.append(event)
        self.logger.warning(f"Security event: {event_type} from {source_ip} - {description}")
        
        # Auto-block on critical threats
        if threat_level == SecurityThreat.CRITICAL:
            self.block_ip(source_ip)
    
    def block_ip(self, ip_address: str):
        """Block an IP address"""
        self.blocked_ips.add(ip_address)
        self.logger.critical(f"Blocked IP address: {ip_address}")
        
        # Add iptables rule
        try:
            subprocess.run([
                "iptables", "-A", "INPUT", "-s", ip_address, "-j", "DROP"
            ], check=True)
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to block IP {ip_address}: {e}")
    
    def get_security_summary(self) -> Dict[str, Any]:
        """Get security monitoring summary"""
        recent_events = [
            event for event in self.security_events
            if (datetime.now() - event.timestamp).days < 7
        ]
        
        threat_counts = {}
        for threat in SecurityThreat:
            threat_counts[threat.value] = sum(
                1 for event in recent_events 
                if event.threat_level == threat
            )
        
        return {
            "total_events": len(recent_events),
            "threat_distribution": threat_counts,
            "blocked_ips": list(self.blocked_ips),
            "active_rate_limits": len(self.rate_limits),
            "last_updated": datetime.now().isoformat()
        }


class SecureTunnelController:
    """
    Advanced secure tunnel controller with monitoring and failover
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.tunnels: Dict[str, TunnelConnection] = {}
        self.health_monitors: Dict[str, TunnelHealthMonitor] = {}
        self.security_monitor = SecurityMonitor()
        self.config_dir = "/home/server/industrial-iot-stack/ct-086-router-system/agent2_vpn_tunnel"
        self.failover_enabled = True
        self.monitoring_active = False
        
    def register_tunnel(self, tunnel_config: Dict[str, Any]) -> bool:
        """Register a new tunnel for monitoring"""
        try:
            tunnel_name = tunnel_config["name"]
            
            # Create tunnel connection object
            tunnel = TunnelConnection(
                name=tunnel_name,
                protocol=tunnel_config["protocol"],
                state=TunnelState.DISCONNECTED,
                local_endpoint=tunnel_config.get("local_endpoint", ""),
                remote_endpoint=tunnel_config.get("remote_endpoint", ""),
                metrics=TunnelMetrics(
                    bytes_sent=0,
                    bytes_received=0,
                    packets_sent=0,
                    packets_received=0,
                    latency_ms=0.0,
                    packet_loss_percent=0.0,
                    connection_uptime=timedelta(),
                    last_handshake=datetime.now(),
                    throughput_mbps=0.0
                ),
                last_update=datetime.now(),
                config_hash=hashlib.md5(json.dumps(tunnel_config, sort_keys=True).encode()).hexdigest(),
                is_primary=tunnel_config.get("is_primary", False),
                failover_priority=tunnel_config.get("failover_priority", 0)
            )
            
            self.tunnels[tunnel_name] = tunnel
            
            # Create health monitor
            monitor = TunnelHealthMonitor(tunnel_name)
            
            # Add default health checks
            if "remote_endpoint" in tunnel_config:
                remote_ip = tunnel_config["remote_endpoint"].split(":")[0]
                monitor.add_health_check(lambda: monitor.ping_test(remote_ip), interval=30)
                monitor.add_health_check(lambda: monitor.bandwidth_test(remote_ip) < 1000, interval=60)
            
            self.health_monitors[tunnel_name] = monitor
            
            self.logger.info(f"Registered tunnel: {tunnel_name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to register tunnel: {e}")
            return False
    
    def start_tunnel_monitoring(self, tunnel_name: str) -> bool:
        """Start monitoring for a specific tunnel"""
        try:
            if tunnel_name in self.health_monitors:
                self.health_monitors[tunnel_name].start_monitoring()
                self.tunnels[tunnel_name].state = TunnelState.CONNECTING
                return True
            return False
        except Exception as e:
            self.logger.error(f"Failed to start monitoring for {tunnel_name}: {e}")
            return False
    
    def stop_tunnel_monitoring(self, tunnel_name: str) -> bool:
        """Stop monitoring for a specific tunnel"""
        try:
            if tunnel_name in self.health_monitors:
                self.health_monitors[tunnel_name].stop_monitoring()
                self.tunnels[tunnel_name].state = TunnelState.DISCONNECTED
                return True
            return False
        except Exception as e:
            self.logger.error(f"Failed to stop monitoring for {tunnel_name}: {e}")
            return False
    
    def trigger_failover(self, failed_tunnel: str) -> bool:
        """Trigger failover to backup tunnel"""
        if not self.failover_enabled:
            return False
        
        try:
            # Find backup tunnel with highest priority
            backup_tunnels = [
                (name, tunnel) for name, tunnel in self.tunnels.items()
                if (name != failed_tunnel and 
                    tunnel.state in [TunnelState.CONNECTED, TunnelState.DISCONNECTED] and
                    not tunnel.is_primary)
            ]
            
            if not backup_tunnels:
                self.logger.error("No backup tunnels available for failover")
                return False
            
            # Sort by failover priority
            backup_tunnels.sort(key=lambda x: x[1].failover_priority, reverse=True)
            backup_name, backup_tunnel = backup_tunnels[0]
            
            # Activate backup tunnel
            self.logger.info(f"Failing over from {failed_tunnel} to {backup_name}")
            backup_tunnel.is_primary = True
            backup_tunnel.state = TunnelState.CONNECTING
            
            # Deactivate failed tunnel
            if failed_tunnel in self.tunnels:
                self.tunnels[failed_tunnel].is_primary = False
                self.tunnels[failed_tunnel].state = TunnelState.FAILED
            
            # Log security event
            self.security_monitor.log_security_event(
                event_type="tunnel_failover",
                threat_level=SecurityThreat.MEDIUM,
                source_ip="system",
                description=f"Failover triggered: {failed_tunnel} -> {backup_name}",
                tunnel_name=failed_tunnel,
                action_taken="failover_completed"
            )
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failover failed: {e}")
            return False
    
    def update_tunnel_metrics(self, tunnel_name: str, metrics_data: Dict[str, Any]):
        """Update tunnel performance metrics"""
        if tunnel_name not in self.tunnels:
            return
        
        tunnel = self.tunnels[tunnel_name]
        
        # Update metrics
        tunnel.metrics.bytes_sent = metrics_data.get("bytes_sent", 0)
        tunnel.metrics.bytes_received = metrics_data.get("bytes_received", 0)
        tunnel.metrics.latency_ms = metrics_data.get("latency_ms", 0.0)
        tunnel.metrics.packet_loss_percent = metrics_data.get("packet_loss_percent", 0.0)
        tunnel.metrics.throughput_mbps = metrics_data.get("throughput_mbps", 0.0)
        tunnel.last_update = datetime.now()
        
        # Analyze for security threats
        security_events = self.security_monitor.analyze_traffic_patterns(tunnel.metrics)
        for event in security_events:
            event.tunnel_name = tunnel_name
    
    def get_tunnel_status(self) -> Dict[str, Any]:
        """Get comprehensive tunnel status"""
        status = {
            "tunnels": {},
            "security_summary": self.security_monitor.get_security_summary(),
            "failover_enabled": self.failover_enabled,
            "monitoring_active": self.monitoring_active,
            "timestamp": datetime.now().isoformat()
        }
        
        for tunnel_name, tunnel in self.tunnels.items():
            health_status = {}
            if tunnel_name in self.health_monitors:
                health_status = self.health_monitors[tunnel_name].get_health_status()
            
            status["tunnels"][tunnel_name] = {
                "state": tunnel.state.value,
                "protocol": tunnel.protocol,
                "is_primary": tunnel.is_primary,
                "failover_priority": tunnel.failover_priority,
                "metrics": asdict(tunnel.metrics),
                "health": health_status,
                "last_update": tunnel.last_update.isoformat()
            }
        
        return status
    
    def deploy_parachute_drop_tunnels(self, config: Dict[str, Any]) -> bool:
        """Deploy complete tunnel infrastructure for Parachute Drop system"""
        try:
            self.logger.info("Deploying Parachute Drop tunnel infrastructure...")
            
            # Primary WireGuard tunnel
            primary_config = {
                "name": "primary-wireguard",
                "protocol": "wireguard",
                "local_endpoint": "0.0.0.0:51820",
                "remote_endpoint": f"{config['external_ip']}:51820",
                "is_primary": True,
                "failover_priority": 100
            }
            
            # Backup OpenVPN tunnel
            backup_config = {
                "name": "backup-openvpn",
                "protocol": "openvpn",
                "local_endpoint": "0.0.0.0:1194",
                "remote_endpoint": f"{config['external_ip']}:1194",
                "is_primary": False,
                "failover_priority": 50
            }
            
            # Register tunnels
            success = True
            for tunnel_config in [primary_config, backup_config]:
                if not self.register_tunnel(tunnel_config):
                    success = False
            
            # Start monitoring
            if success:
                for tunnel_name in self.tunnels:
                    self.start_tunnel_monitoring(tunnel_name)
                
                self.monitoring_active = True
                
                # Save deployment configuration
                deployment_info = {
                    "deployment_time": datetime.now().isoformat(),
                    "tunnels_deployed": list(self.tunnels.keys()),
                    "external_ip": config['external_ip'],
                    "monitoring_active": True,
                    "failover_enabled": True
                }
                
                with open(f"{self.config_dir}/tunnel_deployment.json", "w") as f:
                    json.dump(deployment_info, f, indent=2)
                
                self.logger.info("Parachute Drop tunnel infrastructure deployed successfully")
            
            return success
            
        except Exception as e:
            self.logger.error(f"Tunnel deployment failed: {e}")
            return False


def main():
    """Test secure tunnel controller"""
    logging.basicConfig(level=logging.INFO)
    
    controller = SecureTunnelController()
    
    print("🔐 Secure Tunnel Controller for Parachute Drop System")
    print("=" * 65)
    
    # Example deployment
    config = {
        "external_ip": "203.0.113.10"  # Replace with actual external IP
    }
    
    try:
        if controller.deploy_parachute_drop_tunnels(config):
            print("✅ Tunnel infrastructure deployed successfully!")
            
            # Wait a moment for monitoring to start
            time.sleep(2)
            
            # Get status
            status = controller.get_tunnel_status()
            print(f"\n📊 Tunnel Status:")
            print(f"  Active Tunnels: {len(status['tunnels'])}")
            print(f"  Failover Enabled: {status['failover_enabled']}")
            print(f"  Monitoring Active: {status['monitoring_active']}")
            
            for tunnel_name, tunnel_info in status['tunnels'].items():
                print(f"\n🔗 {tunnel_name}:")
                print(f"  State: {tunnel_info['state']}")
                print(f"  Protocol: {tunnel_info['protocol']}")
                print(f"  Primary: {tunnel_info['is_primary']}")
        
        else:
            print("❌ Tunnel deployment failed!")
    
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()