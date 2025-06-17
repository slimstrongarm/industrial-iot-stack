# 🪂 CT-084 Quick Reference Guide

## ⚡ Fast Facts
- **System**: CT-084 Parachute Drop Industrial IoT Edge Computing
- **Status**: ✅ Production Ready  
- **Components**: 3 integrated subsystems (Pi Builder + Phidget Hub + Node-RED)
- **Deployment**: One-command installation
- **Access**: Mobile-responsive dashboards + professional UIs

---

## 🚀 Quick Commands

### **Installation & Setup**
```bash
# System validation (30 seconds)
./ct084-quick-validate.sh

# Pi image building (15 minutes)  
sudo ./ct084-pi-image-builder.sh

# System installation on Pi (5 minutes)
sudo ./setup_ct084_system.py

# Service verification
sudo systemctl status ct084-discovery ct084-health nodered
```

### **Status Checks**
```bash
# System health
curl http://localhost:8084/health

# Discovery logs
sudo journalctl -u ct084-discovery -f

# Sensor detection
python3 ct084-device-detector.py

# Dashboard access
curl http://localhost:1880/ui
```

### **Troubleshooting**
```bash
# Restart services
sudo systemctl restart ct084-discovery ct084-health nodered

# Check logs
grep -i error /var/log/ct084/*.log

# USB devices
lsusb | grep Phidgets

# Network test
ping -c 3 8.8.8.8
```

---

## 📂 File Locations

### **Agent 1: Pi Image & Discovery**
```
/stack-components/edge-computing/
├── ct084-pi-image-builder.sh      # Main Pi image builder
├── ct084-discovery-agent.py       # AI-powered discovery
├── ct084-device-detector.py       # Hardware detection
├── ct084-sensor-identifier.py     # Sensor identification
├── ct084-system-tester.py         # Testing framework
└── ct084-quick-validate.sh        # Fast validation
```

### **Agent 2: Phidget Hub System**
```
/ct-084-parachute-drop-system/
├── phidget_auto_configurator.py   # Main configurator (1,344 lines)
├── usb_device_manager.py          # USB handling (847 lines)  
├── opcua_bridge.py                # OPC-UA integration (756 lines)
├── configuration_manager.py       # Config management (1,073 lines)
├── setup_ct084_system.py          # Installation (644 lines)
└── test_ct084_system.py           # Testing (643 lines)
```

### **Agent 3: Dashboard & Production**
```
/stack-components/node-red/
├── dashboard-generator.js          # Auto-dashboard creation
├── sensor-discovery.js            # Multi-protocol discovery
├── production-deployment.js       # Production package
├── mobile-responsive-layouts.js   # Mobile interfaces  
├── alert-integration.js           # Multi-channel alerts
├── ct084-complete-integration.js  # Unified package
└── templates/
    └── industrial-dashboard-templates.json # Professional themes
```

---

## 🎯 Mission-Critical Features

### **Parachute Drop Specific**
| Feature | Function | Status |
|---------|----------|--------|
| Altitude Monitoring | Pressure sensor calibration | ✅ Ready |
| Deployment Detection | Accelerometer-based sensing | ✅ Ready |  
| Environmental Tracking | Temperature/humidity logging | ✅ Ready |
| Mission Parameters | Configurable thresholds | ✅ Ready |

### **Industrial Integration**
| Protocol | Function | Endpoint |
|----------|----------|----------|
| OPC-UA | Industrial connectivity | `opc.tcp://localhost:4840` |
| MQTT | Real-time messaging | `localhost:1883` |
| Modbus | Legacy device support | Auto-discovery |
| HTTP/REST | API access | `localhost:8084` |

### **Operational Interfaces**  
| Interface | Purpose | URL |
|-----------|---------|-----|
| Node-RED Dashboard | Primary operations | `http://localhost:1880/ui` |
| Health Check API | System status | `http://localhost:8084/health` |
| Mobile Interface | Field operations | Responsive design |
| Admin Interface | Configuration | SSH access |

---

## ⚙️ Configuration Quick Reference

### **Main Config File**
`/etc/ct084/ct084-config.json`
```json
{
    "device_info": {
        "device_id": "ct084-parachute-drop-001",
        "device_type": "CT-084-Parachute-Drop",
        "location": "CT084/ParachuteDrop/EdgeNode001"
    },
    "discovery": {
        "scan_interval": 30,
        "ai_classification": true
    },
    "network": {
        "opcua_endpoint": "opc.tcp://ignition:62541",
        "mqtt_broker": "emqx"
    }
}
```

### **Service Management**
```bash
# Main services
sudo systemctl [start|stop|restart|status] ct084-discovery
sudo systemctl [start|stop|restart|status] ct084-health  
sudo systemctl [start|stop|restart|status] nodered

# Enable auto-start
sudo systemctl enable ct084-discovery ct084-health nodered
```

### **Log Files**
```bash
/var/log/ct084/discovery-agent.log      # Device discovery
/var/log/ct084/device-detector.log      # Hardware detection
/var/log/ct084/sensor-identifier.log    # Sensor identification
/var/log/ct084/health-monitor.log       # System health
```

---

## 🚨 Emergency Procedures

### **Critical System Failure**
1. **Immediate Response**
   ```bash
   # Check system status
   curl http://localhost:8084/health
   
   # Restart all services
   sudo systemctl restart ct084-discovery ct084-health nodered
   
   # Check for errors
   grep -i "error\|failed\|critical" /var/log/ct084/*.log
   ```

2. **Network Connectivity Loss**
   ```bash
   # Test basic connectivity
   ping -c 3 8.8.8.8
   
   # Check local services
   curl http://localhost:1880/ui
   curl http://localhost:8084/health
   
   # Restart network services
   sudo systemctl restart networking
   ```

3. **Sensor Detection Failure**
   ```bash
   # Check USB connections
   lsusb | grep Phidgets
   
   # Test Phidget library
   python3 -c "from Phidget22.Devices.Hub import *; h=Hub(); h.openWaitForAttachment(5000)"
   
   # Manual device detection
   python3 ct084-device-detector.py
   ```

### **Recovery Procedures**
```bash
# Full system reset
sudo systemctl stop ct084-discovery ct084-health nodered
sudo rm -rf /var/log/ct084/*.log
sudo systemctl start ct084-discovery ct084-health nodered

# Configuration reset
sudo cp /etc/ct084/ct084-config.json.backup /etc/ct084/ct084-config.json
sudo systemctl restart ct084-discovery

# Factory reset
cd /ct-084-parachute-drop-system
sudo ./setup_ct084_system.py --reset
```

---

## 📱 Mobile Interface Access

### **Field Operations Screens**
- **Critical Sensors**: Priority sensor data with large displays
- **Equipment Quick View**: Single equipment focus with essentials
- **Emergency Response**: Emergency procedures and alerts
- **Mission Overview**: Parachute-specific mission monitoring

### **Mobile URLs**
```bash
# Primary mobile dashboard
http://<pi-ip>:1880/ui/#!/0?socketid=<id>

# Emergency response screen  
http://<pi-ip>:1880/ui/#!/emergency

# Mission monitoring
http://<pi-ip>:1880/ui/#!/mission
```

### **Touch Optimizations**
- Large tap targets (minimum 44px)
- Swipe gestures for navigation
- Pinch-to-zoom for detailed views
- Haptic feedback where supported

---

## 🔗 Integration Points

### **Agent Integration Architecture**
```
Agent 1 (Foundation) ──▶ Agent 2 (Sensors) ──▶ Agent 3 (Operations)
    │                        │                       │
    ├─ Pi Image              ├─ USB Manager          ├─ Dashboards
    ├─ Discovery             ├─ OPC-UA Bridge        ├─ Mobile UI
    ├─ Device Detection      ├─ Configuration        ├─ Alerts
    └─ Testing               └─ Installation         └─ Production
```

### **Data Flow**
```
Phidget Sensors ──▶ USB Manager ──▶ OPC-UA Bridge ──▶ Node-RED Dashboard
       │                 │               │                    │
       └─ Discovery ──────┼─ Config Mgmt ─┼─ MQTT Broker ─────┤
                          │               │                    │
                          └─ Health Mon ──┴─ Alert System ─────┘
```

### **Network Topology**
```
Pi Edge Node (CT-084)
├─ eth0: 192.168.1.x (Primary)
├─ wlan0: WiFi backup
├─ OPC-UA Server: :4840
├─ MQTT Broker: :1883  
├─ Node-RED: :1880
├─ Health API: :8084
└─ SSH: :22
```

---

## 🎖️ Production Readiness Checklist

### **Pre-Deployment** ☑️
- [ ] Hardware setup complete (Pi, Phidget hub, sensors)
- [ ] Network connectivity verified (Ethernet + WiFi backup)
- [ ] System validation passed (`./ct084-quick-validate.sh`)
- [ ] Pi image built and flashed (`./ct084-pi-image-builder.sh`)
- [ ] Installation completed (`sudo ./setup_ct084_system.py`)

### **Operational Verification** ☑️  
- [ ] All services running (`systemctl status ct084-*`)
- [ ] Sensors discovered and operational
- [ ] Dashboard accessible (`http://localhost:1880/ui`)
- [ ] Mobile interface tested on field devices
- [ ] Alert channels configured (email, SMS, webhooks)

### **Mission Ready** ☑️
- [ ] Emergency procedures tested
- [ ] Parachute-specific thresholds configured
- [ ] Backup and recovery procedures established
- [ ] Operators trained on interfaces
- [ ] Full system health check passed

---

## 📞 Quick Support

### **Documentation Links**
- **[Complete Guide](CT-084_COMPLETE_GUIDE.md)** - Full documentation
- **[Technical Implementation](../stack-components/edge-computing/CT084-COMPLETE-SYSTEM-GUIDE.md)** - Technical details
- **[Index Navigation](INDEX.md)** - All system documentation

### **Key Contact Points**
- **System Status**: `curl http://localhost:8084/health`
- **Discovery Logs**: `sudo journalctl -u ct084-discovery -f`  
- **Node-RED Dashboard**: `http://localhost:1880/ui`
- **SSH Access**: `ssh pi@<pi-ip>`

### **Performance Targets**
- **Discovery Time**: < 30 seconds
- **Sensor Response**: < 100ms
- **Dashboard Load**: < 5 seconds
- **Mobile Interface**: < 3 seconds
- **Alert Delivery**: < 30 seconds

---

**System Status**: ✅ Production Ready  
**Last Validated**: June 12, 2025  
**Next Review**: Deployment-dependent  

*For detailed technical documentation, see [CT-084_COMPLETE_GUIDE.md](CT-084_COMPLETE_GUIDE.md)*