# MQTT Technology Stack Documentation
*Quick reference for Claude instances working on MQTT implementations*

## 🎯 Quick Start for New Claude Instances

**Working on MQTT?** Start here:
1. **Architecture**: `reference/MQTT_BROKER_ARCHITECTURE.md` - Core design patterns
2. **Setup**: `setup-guides/` - Step-by-step implementation guides  
3. **Troubleshooting**: `troubleshooting/` - Common issues and solutions
4. **Real Implementations**: `implementations/` - Live brewery and project examples

## 📂 File Organization

### Setup Guides
- **EMQX Broker Setup** - Complete EMQX configuration and auth
- **MQTT Integration** - Connect MQTT to other stack components
- **Security & Auth** - Authentication, credentials, and access control

### Implementations  
- **Steel Bonnet Brewery** - Production MQTT topic mapping and flows
- **Parachute Drop CT-084** - Edge device MQTT communication
- **Network Discovery CT-085** - MQTT device discovery patterns

### Troubleshooting
- **Authentication Issues** - User, client ID, and permission problems
- **Network Configuration** - Connection, firewall, and routing issues
- **Integration Debugging** - MQTT ↔ Node-RED ↔ Ignition troubleshooting

## 🔗 Related Technologies

- **Node-RED**: `../node-red/` - MQTT flow processing and automation
- **Ignition**: `../ignition/` - MQTT ↔ OPC UA bridging
- **n8n**: `../n8n/` - MQTT workflow automation
- **Docker**: `../docker/` - Containerized MQTT broker deployment

## 📊 Current Projects Using MQTT

- **CT-084**: Parachute Drop System - Edge device telemetry
- **CT-085**: Network Discovery - MQTT device scanning  
- **Steel Bonnet**: Brewery automation - Equipment monitoring
- **WhatsApp Integration**: MQTT → Alert notifications

## 🎯 Common MQTT Patterns in This Stack

1. **Equipment Monitoring**: Sensors → MQTT → Node-RED → Ignition
2. **Alert Systems**: MQTT triggers → n8n → WhatsApp/Discord notifications  
3. **Edge Computing**: Pi devices → MQTT → Central processing
4. **Cross-System Integration**: MQTT as universal message bus

---
*Last Updated: 2025-06-28 | Files: 19 | Status: Active Development*