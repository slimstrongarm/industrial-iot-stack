#!/usr/bin/env python3
"""
CT-086 Agent 2: VPN Tunnel Implementation
Secure remote access tunneling for Parachute Drop system

This agent specializes in WireGuard and OpenVPN tunnel setup for secure
remote access to industrial networks deployed via GL.iNet routers.
"""

import os
import json
import subprocess
import ipaddress
import logging
import time
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
import qrcode
import base64
import secrets
import cryptography.hazmat.primitives.asymmetric.ed25519 as ed25519
from cryptography.hazmat.primitives import serialization
import yaml


@dataclass
class VPNClient:
    """VPN client configuration"""
    name: str
    public_key: str
    private_key: str
    ip_address: str
    allowed_ips: List[str]
    dns_servers: List[str]
    endpoint: str
    persistent_keepalive: int
    created_at: datetime
    last_handshake: Optional[datetime] = None
    bytes_sent: int = 0
    bytes_received: int = 0
    is_active: bool = True


@dataclass
class VPNServer:
    """VPN server configuration"""
    name: str
    protocol: str  # 'wireguard' or 'openvpn'
    listen_port: int
    public_key: str
    private_key: str
    network: str
    dns_servers: List[str]
    allowed_networks: List[str]
    clients: List[VPNClient]
    is_running: bool = False


class WireGuardManager:
    """WireGuard VPN tunnel management"""
    
    def __init__(self, interface_name: str = "wg0"):
        self.interface_name = interface_name
        self.config_dir = "/etc/wireguard"
        self.logger = logging.getLogger(__name__)
        
    def generate_keypair(self) -> Tuple[str, str]:
        """Generate WireGuard key pair"""
        try:
            # Generate private key
            private_key_result = subprocess.run(
                ["wg", "genkey"],
                capture_output=True,
                text=True,
                check=True
            )
            private_key = private_key_result.stdout.strip()
            
            # Generate public key from private key
            public_key_result = subprocess.run(
                ["wg", "pubkey"],
                input=private_key,
                capture_output=True,
                text=True,
                check=True
            )
            public_key = public_key_result.stdout.strip()
            
            return private_key, public_key
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to generate WireGuard keys: {e}")
            raise
    
    def create_server_config(self, server: VPNServer) -> str:
        """Create WireGuard server configuration"""
        config_lines = [
            "[Interface]",
            f"PrivateKey = {server.private_key}",
            f"Address = {server.network}",
            f"ListenPort = {server.listen_port}",
            f"DNS = {', '.join(server.dns_servers)}",
            "",
            "# Firewall rules",
            "PostUp = iptables -A FORWARD -i %i -j ACCEPT",
            "PostUp = iptables -A FORWARD -o %i -j ACCEPT", 
            "PostUp = iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE",
            "PreDown = iptables -D FORWARD -i %i -j ACCEPT",
            "PreDown = iptables -D FORWARD -o %i -j ACCEPT",
            "PreDown = iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE",
            ""
        ]
        
        # Add client configurations
        for client in server.clients:
            config_lines.extend([
                "[Peer]",
                f"# {client.name}",
                f"PublicKey = {client.public_key}",
                f"AllowedIPs = {', '.join(client.allowed_ips)}",
                f"PersistentKeepalive = {client.persistent_keepalive}",
                ""
            ])
        
        return "\n".join(config_lines)
    
    def create_client_config(self, client: VPNClient, server: VPNServer) -> str:
        """Create WireGuard client configuration"""
        config_lines = [
            "[Interface]",
            f"PrivateKey = {client.private_key}",
            f"Address = {client.ip_address}",
            f"DNS = {', '.join(client.dns_servers)}",
            "",
            "[Peer]",
            f"PublicKey = {server.public_key}",
            f"Endpoint = {client.endpoint}:{server.listen_port}",
            f"AllowedIPs = {', '.join(client.allowed_ips)}",
            f"PersistentKeepalive = {client.persistent_keepalive}"
        ]
        
        return "\n".join(config_lines)
    
    def generate_client_qr_code(self, client_config: str) -> str:
        """Generate QR code for mobile client setup"""
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(client_config)
        qr.make(fit=True)
        
        # Save QR code as image
        img = qr.make_image(fill_color="black", back_color="white")
        qr_path = f"/home/server/industrial-iot-stack/ct-086-router-system/agent2_vpn_tunnel/qr_codes/{client.name}_qr.png"
        os.makedirs(os.path.dirname(qr_path), exist_ok=True)
        img.save(qr_path)
        
        return qr_path
    
    def start_server(self, server: VPNServer) -> bool:
        """Start WireGuard server"""
        try:
            # Create configuration file
            config_content = self.create_server_config(server)
            config_path = f"{self.config_dir}/{self.interface_name}.conf"
            
            os.makedirs(self.config_dir, exist_ok=True)
            with open(config_path, 'w') as f:
                f.write(config_content)
            
            # Start WireGuard interface
            subprocess.run(["wg-quick", "up", self.interface_name], check=True)
            
            self.logger.info(f"WireGuard server started on {self.interface_name}")
            return True
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to start WireGuard server: {e}")
            return False
    
    def stop_server(self) -> bool:
        """Stop WireGuard server"""
        try:
            subprocess.run(["wg-quick", "down", self.interface_name], check=True)
            self.logger.info(f"WireGuard server stopped on {self.interface_name}")
            return True
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to stop WireGuard server: {e}")
            return False
    
    def get_server_status(self) -> Dict[str, Any]:
        """Get WireGuard server status"""
        try:
            result = subprocess.run(
                ["wg", "show", self.interface_name],
                capture_output=True,
                text=True,
                check=True
            )
            
            return {
                "interface": self.interface_name,
                "status": "running",
                "output": result.stdout,
                "timestamp": datetime.now().isoformat()
            }
            
        except subprocess.CalledProcessError:
            return {
                "interface": self.interface_name,
                "status": "stopped",
                "timestamp": datetime.now().isoformat()
            }


class OpenVPNManager:
    """OpenVPN tunnel management for legacy support"""
    
    def __init__(self, config_dir: str = "/etc/openvpn"):
        self.config_dir = config_dir
        self.logger = logging.getLogger(__name__)
    
    def generate_ca_certificate(self, ca_name: str = "parachute-drop-ca") -> Dict[str, str]:
        """Generate Certificate Authority for OpenVPN"""
        ca_dir = f"{self.config_dir}/ca"
        os.makedirs(ca_dir, exist_ok=True)
        
        # Generate CA key and certificate using easy-rsa
        commands = [
            f"cd {ca_dir} && easyrsa init-pki",
            f"cd {ca_dir} && easyrsa --batch build-ca nopass",
            f"cd {ca_dir} && easyrsa gen-dh"
        ]
        
        for cmd in commands:
            subprocess.run(cmd, shell=True, check=True)
        
        return {
            "ca_cert": f"{ca_dir}/pki/ca.crt",
            "ca_key": f"{ca_dir}/pki/private/ca.key",
            "dh_params": f"{ca_dir}/pki/dh.pem"
        }
    
    def create_server_config(self, server_name: str, port: int = 1194) -> str:
        """Create OpenVPN server configuration"""
        config = f"""
port {port}
proto udp
dev tun
ca /etc/openvpn/ca/pki/ca.crt
cert /etc/openvpn/ca/pki/issued/{server_name}.crt
key /etc/openvpn/ca/pki/private/{server_name}.key
dh /etc/openvpn/ca/pki/dh.pem
server 10.8.0.0 255.255.255.0
ifconfig-pool-persist ipp.txt
push "route 192.168.10.0 255.255.255.0"
push "route 192.168.20.0 255.255.255.0"
push "route 192.168.30.0 255.255.255.0"
push "dhcp-option DNS 8.8.8.8"
push "dhcp-option DNS 8.8.4.4"
keepalive 10 120
tls-auth ta.key 0
cipher AES-256-CBC
user nobody
group nogroup
persist-key
persist-tun
status openvpn-status.log
verb 3
"""
        return config.strip()


class VPNTunnelManager:
    """
    Comprehensive VPN tunnel management for Parachute Drop system
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.wireguard = WireGuardManager()
        self.openvpn = OpenVPNManager()
        self.servers: Dict[str, VPNServer] = {}
        self.config_file = "/home/server/industrial-iot-stack/ct-086-router-system/agent2_vpn_tunnel/vpn_config.json"
        
        # Load existing configuration
        self.load_configuration()
    
    def create_wireguard_server(self, 
                               name: str,
                               network: str = "10.0.0.1/24",
                               port: int = 51820,
                               dns_servers: List[str] = None) -> VPNServer:
        """Create a new WireGuard server"""
        if dns_servers is None:
            dns_servers = ["8.8.8.8", "8.8.4.4"]
        
        # Generate server keys
        private_key, public_key = self.wireguard.generate_keypair()
        
        server = VPNServer(
            name=name,
            protocol="wireguard",
            listen_port=port,
            public_key=public_key,
            private_key=private_key,
            network=network,
            dns_servers=dns_servers,
            allowed_networks=["192.168.10.0/24", "192.168.20.0/24", "192.168.30.0/24"],
            clients=[]
        )
        
        self.servers[name] = server
        self.save_configuration()
        
        self.logger.info(f"Created WireGuard server: {name}")
        return server
    
    def add_wireguard_client(self, 
                            server_name: str,
                            client_name: str,
                            endpoint: str,
                            allowed_networks: List[str] = None) -> VPNClient:
        """Add a client to WireGuard server"""
        if server_name not in self.servers:
            raise ValueError(f"Server {server_name} not found")
        
        server = self.servers[server_name]
        
        if allowed_networks is None:
            allowed_networks = ["192.168.10.0/24", "192.168.20.0/24", "192.168.30.0/24"]
        
        # Generate client keys
        private_key, public_key = self.wireguard.generate_keypair()
        
        # Assign IP address
        base_network = ipaddress.IPv4Network(server.network, strict=False)
        client_ip = str(base_network.network_address + len(server.clients) + 2)
        
        client = VPNClient(
            name=client_name,
            public_key=public_key,
            private_key=private_key,
            ip_address=f"{client_ip}/24",
            allowed_ips=allowed_networks,
            dns_servers=server.dns_servers,
            endpoint=endpoint,
            persistent_keepalive=25,
            created_at=datetime.now()
        )
        
        server.clients.append(client)
        self.save_configuration()
        
        # Generate client configuration and QR code
        client_config = self.wireguard.create_client_config(client, server)
        qr_path = self.wireguard.generate_client_qr_code(client_config)
        
        # Save client configuration file
        client_config_path = f"/home/server/industrial-iot-stack/ct-086-router-system/agent2_vpn_tunnel/client_configs/{client_name}.conf"
        os.makedirs(os.path.dirname(client_config_path), exist_ok=True)
        with open(client_config_path, 'w') as f:
            f.write(client_config)
        
        self.logger.info(f"Added WireGuard client: {client_name} to server {server_name}")
        self.logger.info(f"Client config saved to: {client_config_path}")
        self.logger.info(f"QR code saved to: {qr_path}")
        
        return client
    
    def deploy_parachute_drop_vpn(self, external_ip: str) -> Dict[str, Any]:
        """Deploy complete VPN setup for Parachute Drop system"""
        try:
            self.logger.info("Deploying Parachute Drop VPN system...")
            
            # Create main WireGuard server
            server = self.create_wireguard_server(
                name="parachute-drop-main",
                network="10.0.0.1/24",
                port=51820,
                dns_servers=["192.168.10.1", "8.8.8.8"]
            )
            
            # Create default clients
            clients = [
                {"name": "admin-laptop", "networks": ["192.168.10.0/24", "192.168.20.0/24", "192.168.30.0/24"]},
                {"name": "engineer-mobile", "networks": ["192.168.20.0/24", "192.168.30.0/24"]},
                {"name": "technician-tablet", "networks": ["192.168.30.0/24"]},
                {"name": "monitoring-system", "networks": ["192.168.30.0/24"]}
            ]
            
            created_clients = []
            for client_info in clients:
                client = self.add_wireguard_client(
                    server_name="parachute-drop-main",
                    client_name=client_info["name"],
                    endpoint=external_ip,
                    allowed_networks=client_info["networks"]
                )
                created_clients.append(client)
            
            # Start the server
            if self.wireguard.start_server(server):
                server.is_running = True
                self.save_configuration()
            
            deployment_info = {
                "server": {
                    "name": server.name,
                    "protocol": server.protocol,
                    "port": server.listen_port,
                    "network": server.network,
                    "public_key": server.public_key,
                    "status": "running" if server.is_running else "stopped"
                },
                "clients": [
                    {
                        "name": client.name,
                        "ip_address": client.ip_address,
                        "config_file": f"client_configs/{client.name}.conf",
                        "qr_code": f"qr_codes/{client.name}_qr.png"
                    }
                    for client in created_clients
                ],
                "deployment_time": datetime.now().isoformat(),
                "external_endpoint": external_ip,
                "access_instructions": {
                    "admin_access": "Full network access - use admin-laptop config",
                    "engineer_access": "Industrial networks only - use engineer-mobile config", 
                    "technician_access": "Monitoring network only - use technician-tablet config",
                    "monitoring_access": "Data collection only - use monitoring-system config"
                }
            }
            
            # Save deployment info
            with open("/home/server/industrial-iot-stack/ct-086-router-system/agent2_vpn_tunnel/deployment_info.json", "w") as f:
                json.dump(deployment_info, f, indent=2)
            
            self.logger.info("Parachute Drop VPN deployment completed successfully")
            return deployment_info
            
        except Exception as e:
            self.logger.error(f"VPN deployment failed: {e}")
            raise
    
    def get_connection_status(self) -> Dict[str, Any]:
        """Get VPN connection status"""
        status = {
            "servers": {},
            "total_clients": 0,
            "active_connections": 0,
            "last_updated": datetime.now().isoformat()
        }
        
        for server_name, server in self.servers.items():
            if server.protocol == "wireguard":
                server_status = self.wireguard.get_server_status()
                status["servers"][server_name] = {
                    "protocol": server.protocol,
                    "status": server_status.get("status", "unknown"),
                    "clients": len(server.clients),
                    "network": server.network,
                    "port": server.listen_port
                }
                status["total_clients"] += len(server.clients)
        
        return status
    
    def save_configuration(self):
        """Save VPN configuration to file"""
        config_data = {
            "servers": {
                name: {
                    "name": server.name,
                    "protocol": server.protocol,
                    "listen_port": server.listen_port,
                    "public_key": server.public_key,
                    "private_key": server.private_key,
                    "network": server.network,
                    "dns_servers": server.dns_servers,
                    "allowed_networks": server.allowed_networks,
                    "is_running": server.is_running,
                    "clients": [
                        {
                            "name": client.name,
                            "public_key": client.public_key,
                            "private_key": client.private_key,
                            "ip_address": client.ip_address,
                            "allowed_ips": client.allowed_ips,
                            "dns_servers": client.dns_servers,
                            "endpoint": client.endpoint,
                            "persistent_keepalive": client.persistent_keepalive,
                            "created_at": client.created_at.isoformat(),
                            "is_active": client.is_active
                        }
                        for client in server.clients
                    ]
                }
                for name, server in self.servers.items()
            },
            "last_updated": datetime.now().isoformat()
        }
        
        os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
        with open(self.config_file, 'w') as f:
            json.dump(config_data, f, indent=2)
    
    def load_configuration(self):
        """Load VPN configuration from file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    config_data = json.load(f)
                
                for server_name, server_data in config_data.get("servers", {}).items():
                    clients = []
                    for client_data in server_data.get("clients", []):
                        client = VPNClient(
                            name=client_data["name"],
                            public_key=client_data["public_key"],
                            private_key=client_data["private_key"],
                            ip_address=client_data["ip_address"],
                            allowed_ips=client_data["allowed_ips"],
                            dns_servers=client_data["dns_servers"],
                            endpoint=client_data["endpoint"],
                            persistent_keepalive=client_data["persistent_keepalive"],
                            created_at=datetime.fromisoformat(client_data["created_at"]),
                            is_active=client_data.get("is_active", True)
                        )
                        clients.append(client)
                    
                    server = VPNServer(
                        name=server_data["name"],
                        protocol=server_data["protocol"],
                        listen_port=server_data["listen_port"],
                        public_key=server_data["public_key"],
                        private_key=server_data["private_key"],
                        network=server_data["network"],
                        dns_servers=server_data["dns_servers"],
                        allowed_networks=server_data["allowed_networks"],
                        clients=clients,
                        is_running=server_data.get("is_running", False)
                    )
                    
                    self.servers[server_name] = server
                
                self.logger.info(f"Loaded configuration with {len(self.servers)} servers")
                
        except Exception as e:
            self.logger.warning(f"Could not load existing configuration: {e}")


def main():
    """Test VPN tunnel manager"""
    # Setup logging
    logging.basicConfig(level=logging.INFO)
    
    vpn_manager = VPNTunnelManager()
    
    print("🔐 VPN Tunnel Manager for Parachute Drop System")
    print("=" * 60)
    
    # Example deployment (change IP to actual external IP)
    external_ip = "203.0.113.10"  # Example IP - replace with actual
    
    try:
        deployment_info = vpn_manager.deploy_parachute_drop_vpn(external_ip)
        
        print(f"✅ VPN Deployment Successful!")
        print(f"📊 Server: {deployment_info['server']['name']}")
        print(f"🌐 Protocol: {deployment_info['server']['protocol']}")
        print(f"🔌 Port: {deployment_info['server']['port']}")
        print(f"📱 Clients Created: {len(deployment_info['clients'])}")
        
        print("\n📱 Client Access:")
        for client in deployment_info['clients']:
            print(f"  - {client['name']}: {client['config_file']}")
        
        # Get connection status
        status = vpn_manager.get_connection_status()
        print(f"\n📊 Connection Status:")
        print(f"  Total Servers: {len(status['servers'])}")
        print(f"  Total Clients: {status['total_clients']}")
        
    except Exception as e:
        print(f"❌ VPN deployment failed: {e}")


if __name__ == "__main__":
    main()