# MQTT Broker Architecture - CRITICAL

## 🚨 Important: Two Different MQTT Brokers

### Mac Instance (Green TMUX)
- **Broker**: Mosquitto
- **Port**: 1883 (default)
- **Purpose**: Local development, testing
- **Topics**: Development/test topics

### Server Instance (Blue TMUX)
- **Broker**: EMQX
- **Port**: 1883 (default) - CHECK IF DIFFERENT
- **Purpose**: Production, POC demo
- **Dashboard**: Usually on port 18083
- **Topics**: Production brewery topics

## Key Differences

### Mosquitto (Mac)
- Lightweight, simple configuration
- Config file: mosquitto.conf
- Basic authentication
- No built-in dashboard
- Command line tools: mosquitto_pub, mosquitto_sub

### EMQX (Server)
- Enterprise-grade features
- Web dashboard for monitoring
- Advanced authentication (built-in)
- Clustering support
- REST API for management
- Better performance monitoring

## Testing Commands

### For Mosquitto (Mac):
```bash
# Subscribe
mosquitto_sub -h localhost -t "test/#" -v

# Publish
mosquitto_pub -h localhost -t "test/message" -m "Hello from Mac"
```

### For EMQX (Server):
```bash
# Subscribe (might need auth)
mosquitto_sub -h localhost -p 1883 -t "iiot/#" -v

# Or use EMQX's own CLI
emqx_ctl topics list
emqx_ctl stats

# Check dashboard
http://server-ip:18083
# Default login often: admin/public
```

## Inter-Broker Communication

### Option 1: MQTT Bridge
Configure Mosquitto to bridge to EMQX:
```conf
# In mosquitto.conf
connection emqx-bridge
address server-ip:1883
topic # out 0
topic # in 0
```

### Option 2: Node-RED Bridge
Use Node-RED to subscribe to one broker and publish to another

### Option 3: Direct Client Connections
Have clients connect to both brokers as needed

## For Friday Demo

### Data Flow:
```
Field Devices → EMQX (Server) → Processing → Visualization
                     ↓
              Test Bridge
                     ↓
            Mosquitto (Mac) → Development Testing
```

## ✅ Completed Tasks (Server Claude CT-001 to CT-004)
1. ✅ Server audit completed - Docker services documented
2. ✅ EMQX broker deployed and operational on port 1883
3. ✅ EMQX dashboard confirmed running on port 18083
4. ✅ MQTT connectivity tested between Mac Mosquitto and Server EMQX
5. ✅ Docker Compose configuration created for full stack

## Status Update (June 3, 2025)
- **EMQX Deployment**: Fully operational on server
- **Cross-Platform Testing**: Mac ↔ Server MQTT communication verified  
- **Docker Integration**: Complete stack ready for n8n addition
- **Friday Demo Ready**: MQTT infrastructure prepared for demonstration

## Remaining Tasks
- Configure production topic namespace strategy
- Implement MQTT bridge for permanent sync (if needed)
- Add n8n to the Docker stack for workflow automation