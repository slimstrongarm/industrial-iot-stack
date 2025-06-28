# CT-084 Parachute Drop System - Quick Reference

## System Overview
**CT-084** is an AI-powered industrial IoT edge computing system for rapid deployment with intelligent device discovery and sensor identification.

## Core Components
- **Pi Image Builder**: Automated Pi image creation
- **Discovery Agent**: AI-powered device/sensor discovery  
- **Device Detector**: Hardware detection engine
- **Sensor Identifier**: AI sensor classification
- **System Tester**: Comprehensive validation suite
- **Quick Validator**: Fast deployment checks

## Quick Commands

### Build Pi Image
```bash
sudo ./ct084-pi-image-builder.sh
```

### Validate System
```bash
./ct084-quick-validate.sh
```

### Run Tests
```bash
python3 ct084-system-tester.py
```

### Check Services
```bash
sudo systemctl status ct084-discovery
sudo systemctl status ct084-health
sudo systemctl status nodered
```

### View Logs
```bash
sudo journalctl -u ct084-discovery -f
tail -f /var/log/ct084/discovery-agent.log
```

### Health Check
```bash
curl http://localhost:8084/health
```

## Service URLs
- **Node-RED**: http://\<pi-ip\>:1880
- **Health Monitor**: http://\<pi-ip\>:8084/health
- **Discovery API**: http://\<pi-ip\>:8084/discovery

## Key File Locations
- **Config**: `/etc/ct084/ct084-config.json`
- **Logs**: `/var/log/ct084/`
- **Data**: `/opt/ct084/`
- **Results**: `/var/log/ct084/*-results.json`

## Network Configuration
- **OPC-UA**: `opc.tcp://ignition:62541`
- **MQTT**: `emqx:1883`
- **Discovery Port**: `8084`
- **Node-RED**: `1880`

## Troubleshooting

### Service Issues
```bash
# Restart services
sudo systemctl restart ct084-discovery
sudo systemctl restart ct084-health

# Check status
sudo systemctl status ct084-*

# View errors
sudo journalctl -u ct084-discovery -xe
```

### Phidget Issues
```bash
# Check USB devices
lsusb | grep Phidgets

# Test Phidget library
python3 -c "from Phidget22.Devices.Hub import *"

# Run detection
python3 ct084-device-detector.py
```

### Network Issues
```bash
# Test connectivity
ping 8.8.8.8
telnet ignition 62541
mosquitto_pub -h emqx -t test -m "hello"

# Check network services
nmap -sT localhost -p 1880,8084
```

## Common Tasks

### Add New Sensor
1. Connect to VINT Hub port
2. Restart discovery: `sudo systemctl restart ct084-discovery`
3. Check logs: `journalctl -u ct084-discovery -f`
4. Verify in Node-RED dashboard

### Update Configuration
1. Edit: `sudo nano /etc/ct084/ct084-config.json`
2. Validate: `python3 -m json.tool /etc/ct084/ct084-config.json`
3. Restart: `sudo systemctl restart ct084-discovery`

### Backup System
```bash
# Backup configuration
sudo cp /etc/ct084/ct084-config.json /backup/

# Backup logs
sudo tar -czf /backup/ct084-logs-$(date +%Y%m%d).tar.gz /var/log/ct084/

# Backup Node-RED flows
sudo cp /root/.node-red/flows.json /backup/
```

### Factory Reset
1. Hold GPIO pin 18 during boot, OR
2. Run: `sudo /opt/ct084/factory-reset.sh`

## Performance Targets
- **Discovery Time**: < 30 seconds
- **Sensor ID Time**: < 5 seconds per sensor
- **Memory Usage**: < 512MB
- **CPU Usage**: < 25% average
- **Update Rate**: 1-10 Hz per sensor

## Support Files
- **Full Guide**: `CT084-COMPLETE-SYSTEM-GUIDE.md`
- **Build Manifest**: `build/images/ct084-build-manifest.json`
- **Test Results**: `/var/log/ct084/test_report_*.json`
- **Discovery Results**: `/var/log/ct084/discovery-results.json`

## Emergency Contacts
- **Technical Issues**: Check logs first
- **Hardware Issues**: Verify connections
- **Network Issues**: Check firewall/routing
- **Performance Issues**: Monitor system resources

---
**Version**: 1.0.0 | **Built**: December 2025 | **Agent**: Claude Agent 1