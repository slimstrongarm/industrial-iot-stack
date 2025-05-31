# Ignition Edge

## Description
Ignition Edge is a lightweight, edge-computing solution that brings Ignition's data collection, visualization, and system management capabilities directly to edge devices at the plant floor.

## Core Capabilities
- **Edge Computing**: Process data locally before sending to central systems
- **Protocol Translation**: Convert between industrial protocols (Modbus, OPC-UA, etc.)
- **Local HMI**: Provide operator interfaces without cloud connectivity
- **Store & Forward**: Buffer data during network outages
- **Tag Historian**: Local data logging and trending

## Current Implementation Status
### ✅ Implemented
- Basic Modbus device connections
- Local SQLite historian
- Simple HMI screens for operator interface

### 🚧 In Progress
- MQTT transmission to central Ignition Gateway
- Advanced alarming configuration

### 📋 Planned
- OPC-UA server functionality
- Enhanced edge analytics
- Integration with ML models

## Integration Points
### Inputs
- Modbus TCP/RTU from PLCs
- OPC-UA from compatible devices
- MQTT subscriptions from Node-RED

### Outputs
- MQTT publications to broker
- REST API for Node-RED consumption
- SQL database for reporting

### Dependencies
- Java Runtime Environment
- SQLite for local storage
- Network connectivity for remote synchronization

## Configuration
- Gateway Configuration: `/usr/local/ignition-edge/data/`
- Device connections: Configured through web interface
- MQTT settings: In gateway network settings

## Performance Metrics
- Tag throughput: 10,000 tags @ 1 second scan rate
- Memory usage: 512MB - 2GB depending on project size
- CPU usage: 10-30% on edge hardware

## Known Limitations
- Limited to 500 tags without license
- No redundancy options in Edge edition
- Reduced driver set compared to full Ignition

## Related Steel Bonnet Scripts
- Device configuration scripts: [Link to Steel Bonnet repo]
- Backup/restore utilities: [Link to Steel Bonnet repo]
- Performance monitoring: [Link to Steel Bonnet repo]

## Maintenance Notes
- Weekly gateway backups recommended
- Monitor wrapper.log for errors
- Check store & forward queues regularly