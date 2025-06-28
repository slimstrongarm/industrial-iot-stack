#!/bin/bash
# 🪂 Parachute Drop - Portable Router Configuration
# Creates isolated network for safe industrial deployment

echo "🌐 Configuring Portable Router for Parachute Drop..."
echo "=================================================="

# Router: GL.iNet GL-MT1300 (Beryl) or similar travel router
# Creates: Isolated network for Pi and discovered devices
# Provides: WiFi hotspot, ethernet bridge, VPN tunnel home

# Default configuration for GL.iNet routers
ROUTER_IP="192.168.8.1"
ROUTER_SSID="ParachuteDrop"
ROUTER_PASSWORD="Industrial2024!"

echo "📡 Setting up isolated network..."

# Create network configuration
cat > parachute_network_config.json << 'EOF'
{
  "network_config": {
    "router_ip": "192.168.8.1",
    "subnet": "192.168.8.0/24",
    "dhcp_range": "192.168.8.10-192.168.8.50",
    "wifi_ssid": "ParachuteDrop",
    "wifi_password": "Industrial2024!",
    "security": "WPA2-PSK"
  },
  "device_assignments": {
    "raspberry_pi": "192.168.8.10",
    "facility_laptop": "192.168.8.20",
    "discovered_plc": "192.168.8.30-50"
  },
  "port_forwarding": {
    "node_red": {
      "internal": "192.168.8.10:1880",
      "external": "1880"
    },
    "mqtt": {
      "internal": "192.168.8.10:1883", 
      "external": "1883"
    },
    "ssh": {
      "internal": "192.168.8.10:22",
      "external": "2222"
    }
  },
  "firewall_rules": {
    "allow_internal": "192.168.8.0/24",
    "block_internet": "unless_vpn",
    "log_all_traffic": true
  }
}
EOF

echo "🔧 Configuring router via API..."

# GL.iNet router API configuration (adjust for your router model)
ROUTER_API="http://${ROUTER_IP}/cgi-bin/luci"

# Set WiFi configuration
curl -X POST "${ROUTER_API}/admin/wireless" \
  -d "ssid=${ROUTER_SSID}" \
  -d "encryption=psk2" \
  -d "key=${ROUTER_PASSWORD}" \
  -d "channel=6"

# Set DHCP reservations
curl -X POST "${ROUTER_API}/admin/network/dhcp" \
  -d "start=10" \
  -d "limit=40" \
  -d "leasetime=24h"

# Create static IP for Pi
curl -X POST "${ROUTER_API}/admin/network/dhcp/static" \
  -d "mac=b8:27:eb:xx:xx:xx" \
  -d "ip=192.168.8.10" \
  -d "name=parachute-pi"

echo "🔒 Setting up VPN tunnel for remote access..."

# OpenVPN configuration for secure tunnel home
cat > parachute_vpn.ovpn << 'EOF'
# Parachute Drop VPN Configuration
# Allows secure remote access to deployed Pi
client
dev tun
proto udp
remote your-vpn-server.com 1194
resolv-retry infinite
nobind
persist-key
persist-tun
ca ca.crt
cert client.crt
key client.key
cipher AES-256-CBC
auth SHA256
comp-lzo
verb 3

# Route Pi subnet through VPN
route 192.168.8.0 255.255.255.0
EOF

echo "📊 Setting up traffic monitoring..."

# Create traffic monitoring script
cat > monitor_network_traffic.py << 'EOF'
#!/usr/bin/env python3
"""
Monitor network traffic for industrial protocol detection
"""
import scapy.all as scapy
import json
import time
from collections import defaultdict

class TrafficAnalyzer:
    def __init__(self):
        self.protocols = defaultdict(int)
        self.devices = defaultdict(dict)
        
    def packet_handler(self, packet):
        if packet.haslayer(scapy.IP):
            src_ip = packet[scapy.IP].src
            dst_ip = packet[scapy.IP].dst
            
            # Detect industrial protocols
            if packet.haslayer(scapy.TCP):
                dst_port = packet[scapy.TCP].dport
                
                # Common industrial ports
                protocol_map = {
                    102: "Siemens S7",
                    502: "Modbus TCP", 
                    44818: "EtherNet/IP",
                    4840: "OPC-UA",
                    1883: "MQTT",
                    8883: "MQTT/TLS"
                }
                
                if dst_port in protocol_map:
                    protocol = protocol_map[dst_port]
                    self.protocols[protocol] += 1
                    self.devices[src_ip]['protocols'] = self.devices[src_ip].get('protocols', [])
                    if protocol not in self.devices[src_ip]['protocols']:
                        self.devices[src_ip]['protocols'].append(protocol)
                    
                    print(f"📡 {protocol} traffic: {src_ip} -> {dst_ip}")
    
    def start_monitoring(self, duration=300):  # 5 minutes
        print("🔍 Starting network traffic analysis...")
        scapy.sniff(prn=self.packet_handler, timeout=duration, filter="ip")
        
        # Save results
        results = {
            "timestamp": time.time(),
            "protocols_detected": dict(self.protocols),
            "devices_discovered": dict(self.devices)
        }
        
        with open('/tmp/traffic_analysis.json', 'w') as f:
            json.dump(results, f, indent=2)
            
        return results

if __name__ == "__main__":
    analyzer = TrafficAnalyzer()
    analyzer.start_monitoring()
EOF

chmod +x monitor_network_traffic.py

echo "🚀 Creating deployment checklist..."

cat > deployment_checklist.md << 'EOF'
# 🪂 Parachute Drop Deployment Checklist

## Pre-Deployment (Office)
- [ ] Charge all devices (Pi, router, tablet)
- [ ] Load sensor configurations
- [ ] Test VPN connection
- [ ] Backup current flows

## On-Site Setup (5 minutes)
- [ ] Power on portable router
- [ ] Connect Pi via ethernet
- [ ] Connect facility laptop to WiFi "ParachuteDrop"
- [ ] Access Pi dashboard at 192.168.8.10:1880/ui

## Discovery Phase (15 minutes)
- [ ] Run network discovery scan
- [ ] Connect RJ45 to PLC if available
- [ ] Deploy Phidget sensors at key points
- [ ] Start MQTT traffic monitoring

## Data Collection (Ongoing)
- [ ] Verify sensor readings on dashboard
- [ ] Check data logging to local files
- [ ] Monitor for industrial protocol traffic
- [ ] Document facility-specific findings

## Before Leaving
- [ ] Ensure Pi is logging data
- [ ] Test VPN remote access
- [ ] Leave contact info for facility
- [ ] Schedule follow-up in 1 week
EOF

echo "✅ Portable router configuration complete!"
echo ""
echo "📋 Next Steps:"
echo "1. Flash router with custom firmware if needed"
echo "2. Test isolated network with Pi"
echo "3. Configure VPN server for remote access"
echo "4. Load deployment checklist on tablet"

echo ""
echo "🌐 Network Details:"
echo "Router IP: ${ROUTER_IP}"
echo "WiFi: ${ROUTER_SSID} / ${ROUTER_PASSWORD}"
echo "Pi Dashboard: http://192.168.8.10:1880/ui"
echo "Remote Access: VPN tunnel + SSH to 192.168.8.10:22"