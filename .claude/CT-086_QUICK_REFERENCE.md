# CT-086 Quick Reference Guide

## 🚀 Instant Deployment
```bash
cd /home/server/industrial-iot-stack/ct-086-router-system
sudo python3 setup_ct086_system.py
```

## 📊 System Status Check
```bash
# Quick system health
python3 -c "from setup_ct086_system import CT086SystemOrchestrator; print(CT086SystemOrchestrator().get_system_status())"

# Agent status
ls -la ct-086-router-system/*/
```

## 🌐 Access Points
- **Router Management**: http://192.168.8.1
- **Traffic Dashboard**: http://localhost:8086  
- **Authentication**: http://localhost:8087
- **VPN Management**: http://localhost:8082

## 🔧 Quick Configuration
```bash
# Set external IP for VPN
export CT086_EXTERNAL_IP="YOUR_IP"

# Router admin password  
export CT086_ROUTER_PASSWORD="goodlife"
```

## 🔒 Default Credentials
- **Router**: admin / goodlife
- **System Admin**: admin / [see admin_credentials.json]
- **VPN Clients**: [see client_configs/ directory]

## 📱 Network Structure
- **VLAN 10**: Management (192.168.10.0/24)
- **VLAN 20**: Industrial (192.168.20.0/24)  
- **VLAN 30**: Monitoring (192.168.30.0/24)
- **VLAN 40**: Guest (192.168.40.0/24)

## 🧪 Quick Test
```bash
# Test network connectivity
ping 192.168.8.1

# Test VPN status
wg show

# Test firewall
iptables -L
```

## 🔄 Service Management
```bash
# Restart VPN
sudo systemctl restart wg-quick@wg0

# Check logs
tail -f /var/log/syslog | grep ct086
```

## 📋 Troubleshooting
| Issue | Quick Fix |
|-------|-----------|
| Router not accessible | Check network cable, ping 192.168.8.1 |
| VPN not connecting | Restart wg-quick@wg0 service |
| Dashboard not loading | Check port 8086, restart services |
| Authentication failed | Check auth_database.db exists |

## 🎯 Integration
- **CT-084 Compatible**: ✅ Pi image deployment
- **CT-085 Compatible**: ✅ Network discovery
- **Protocols Supported**: Modbus, OPC-UA, MQTT, EtherNet/IP

## 📞 Emergency Commands
```bash
# Reset router config
cd agent1_router_config && python3 glinet_router_manager.py

# Reset VPN
cd agent2_vpn_tunnel && python3 vpn_tunnel_manager.py

# Reset authentication
cd agent4_remote_access_security && python3 authentication_manager.py
```