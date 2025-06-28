# CT-084 Parachute Drop System - Phidget Auto Configurator

## Mission-Critical Sensor Integration for Parachute Drop Operations

The CT-084 Parachute Drop System provides comprehensive automatic sensor configuration, monitoring, and industrial protocol integration for mission-critical parachute drop operations. This system ensures reliable altitude monitoring, deployment detection, and environmental data collection throughout the entire drop sequence.

### 🎯 Key Features

- **Automatic Device Detection**: Intelligent USB device discovery and Phidget sensor enumeration
- **Smart Sensor Configuration**: Automatic sensor type identification and mission-specific calibration
- **Industrial Integration**: Full OPC-UA connectivity with fault tolerance and store-and-forward capability
- **Mission-Critical Reliability**: Comprehensive error handling, automatic recovery, and configuration backup
- **Real-Time Monitoring**: Continuous sensor monitoring with deployment detection and altitude tracking

### 📊 System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   USB Devices   │    │  Phidget VINT   │    │    Sensors      │
│   Detection     │────│      Hub        │────│   (Multiple)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                        │                        │
         │              ┌─────────▼─────────┐              │
         │              │  Auto Configurator │              │
         │              │     System         │              │
         │              └─────────┬─────────┘              │
         │                        │                        │
         ▼                        ▼                        ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Configuration  │    │    OPC-UA       │    │   Data Logging  │
│   Management    │    │  Integration    │    │  & Monitoring   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### 🚀 Quick Start

#### Prerequisites

- Linux system (Ubuntu 20.04+ recommended)
- Python 3.8+
- USB access permissions
- Phidget VINT Hub and sensors

#### Installation

1. **Clone and Setup**:
   ```bash
   git clone <repository-url>
   cd ct-084-parachute-drop-system
   chmod +x setup_ct084_system.py
   sudo ./setup_ct084_system.py
   ```

2. **Start the System**:
   ```bash
   sudo systemctl start ct084-system
   sudo systemctl enable ct084-system
   ```

3. **Verify Installation**:
   ```bash
   ct084 status
   ct084 discovery
   ```

#### Basic Usage

1. **Connect Hardware**:
   - Connect Phidget VINT Hub to USB port
   - Attach sensors to VINT ports (0-3)
   - Ensure proper power supply

2. **Run Discovery**:
   ```bash
   ct084 discovery
   ```

3. **Check Sensor Configuration**:
   ```bash
   ct084 config
   ```

4. **Monitor System Logs**:
   ```bash
   ct084 logs
   ```

### 📋 Supported Sensors

#### Mission-Critical Sensors
- **Pressure Sensors**: Altitude monitoring and deployment detection
- **Accelerometers**: Vibration monitoring and impact detection
- **Temperature Sensors**: Environmental monitoring
- **Humidity Sensors**: Environmental conditions

#### Industrial Sensors
- **Voltage Inputs**: Analog signal monitoring
- **Voltage Ratio Inputs**: Bridge sensor support
- **Load Cells**: Weight and force measurement
- **Strain Gauges**: Structural monitoring

### 🔧 Configuration

#### System Configuration (`/etc/ct-084/system_configuration.yaml`)

```yaml
system_id: "CT-084-001"
configuration_version: "1.0.0"

mission_parameters:
  deployment_altitude: 1000      # meters
  critical_altitude: 500         # meters
  max_descent_rate: 10          # m/s
  parachute_deployment_time: 30  # seconds

opcua_settings:
  endpoint: "opc.tcp://localhost:4840/freeopcua/server/"
  namespace: "CT084_ParachuteDrop"
  auto_reconnect: true

monitoring_settings:
  scan_interval: 5.0            # seconds
  data_retention_days: 30
  alert_enabled: true

fault_tolerance:
  enable_redundancy: true
  max_connection_failures: 3
  auto_recovery: true
  store_and_forward: true
```

#### Sensor-Specific Configuration

Each sensor type has optimized configuration for parachute drop operations:

- **Pressure Sensors**: 10 Hz sampling for altitude monitoring
- **Accelerometers**: High-frequency sampling for deployment detection
- **Environmental Sensors**: Lower frequency for long-term monitoring

### 🏭 Industrial Integration

#### OPC-UA Node Structure

```
CT084/
├── ParachuteDrop/
│   ├── Environment/
│   │   ├── Sensor_0/
│   │   │   ├── Value
│   │   │   ├── Quality
│   │   │   ├── Timestamp
│   │   │   └── Configuration
│   │   └── Sensor_1/...
│   ├── Motion/
│   │   ├── Sensor_2/...
│   │   └── Sensor_3/...
│   └── Analog/
│       └── Sensor_4/...
```

#### Data Publishing

- **Real-time Data**: Published at sensor-specific intervals
- **Quality Monitoring**: Good/Uncertain/Bad quality indicators
- **Buffering**: Store-and-forward for network interruptions
- **Timestamps**: Synchronized timestamps for correlation

### 📊 Monitoring and Alerts

#### System Health Monitoring

- **Device Status**: USB connection and sensor health
- **Data Quality**: Validation and range checking
- **Network Status**: OPC-UA connection monitoring
- **Performance**: CPU, memory, and disk usage

#### Mission-Critical Alerts

- **Altitude Warnings**: Deployment and critical altitude thresholds
- **Sensor Failures**: Automatic detection and notification
- **Communication Loss**: Network and device disconnect alerts
- **System Errors**: Hardware and software fault detection

### 🔒 Fault Tolerance and Recovery

#### Automatic Recovery

- **USB Hot-Plug**: Automatic sensor reconnection
- **Network Recovery**: OPC-UA reconnection with buffering
- **Configuration Backup**: Automatic configuration snapshots
- **Graceful Degradation**: Continued operation with reduced sensors

#### Data Integrity

- **Store-and-Forward**: Buffer data during network outages
- **Checksum Validation**: Configuration integrity checking
- **Backup Management**: Automated backup rotation
- **Recovery Procedures**: Automatic and manual recovery options

### 🛠️ API Reference

#### Phidget Auto Configurator

```python
from phidget_auto_configurator import PhidgetAutoConfigurator

# Initialize configurator
configurator = PhidgetAutoConfigurator()

# Run full discovery and configuration
sensors = configurator.run_full_discovery_and_configuration()

# Get configuration status
status = configurator.get_configuration_status()
```

#### Device Detection

```python
from device_detection import USBDeviceManager

# Create device manager
manager = USBDeviceManager()

# Start monitoring
manager.start_monitoring()

# Get Phidget devices
devices = manager.get_phidget_devices()
```

#### OPC-UA Integration

```python
from opcua_integration import CT084OPCUABridge

# Create bridge
bridge = CT084OPCUABridge()

# Connect to server
await bridge.connect_client()

# Create sensor nodes
await bridge.create_sensor_nodes(sensors)

# Publish data
await bridge.publish_sensor_data(sensor_id, value, quality)
```

#### Configuration Management

```python
from config_management import ConfigurationManager

# Create manager
manager = ConfigurationManager()

# Load configuration
config = manager.load_system_configuration()

# Create backup
backup_id = manager.create_backup("Manual backup")

# Restore from backup
manager.restore_backup(backup_id)
```

### 📁 File Structure

```
ct-084-parachute-drop-system/
├── phidget-auto-configurator/
│   └── phidget_auto_configurator.py
├── device-detection/
│   └── usb_device_manager.py
├── opcua-integration/
│   └── opcua_bridge.py
├── config-management/
│   └── configuration_manager.py
├── requirements.txt
├── setup_ct084_system.py
└── README.md
```

### 📊 System Directories

- **Installation**: `/opt/ct-084/`
- **Configuration**: `/etc/ct-084/`
- **Logs**: `/var/log/ct-084/`
- **Data**: `/var/lib/ct-084/`
- **Backups**: `/var/backups/ct-084/`

### 🔧 Troubleshooting

#### Common Issues

1. **USB Permission Denied**:
   ```bash
   sudo usermod -a -G plugdev $USER
   # Log out and back in
   ```

2. **Phidget Library Missing**:
   ```bash
   pip install Phidget22
   ```

3. **OPC-UA Connection Failed**:
   - Check server endpoint configuration
   - Verify network connectivity
   - Check firewall settings

4. **Service Won't Start**:
   ```bash
   systemctl status ct084-system
   journalctl -u ct084-system -f
   ```

#### Log Files

- **System Logs**: `/var/log/ct-084/phidget_configurator.log`
- **Setup Logs**: `/tmp/ct084_setup.log`
- **Service Logs**: `journalctl -u ct084-system`

#### Configuration Validation

```bash
ct084 config
```

### 🚀 Advanced Configuration

#### Custom Sensor Calibration

Sensors can be calibrated for specific mission requirements:

```yaml
calibration_data:
  pressure_sensor:
    sea_level_pressure: 101.325
    altitude_offset: 0
    calibration_temperature: 20.0
  
  accelerometer:
    static_offsets:
      x: 0.002
      y: -0.001
      z: 0.005
    sensitivity: 1.0
```

#### OPC-UA Security

For secure environments:

```yaml
opcua_settings:
  security_policy: "Basic256Sha256"
  security_mode: "SignAndEncrypt"
  certificate_path: "/etc/ct-084/certs/client.pem"
  private_key_path: "/etc/ct-084/certs/client.key"
```

### 📈 Performance Monitoring

#### System Metrics

- **Sensor Update Rates**: Monitor actual vs. configured rates
- **Data Throughput**: OPC-UA publish statistics
- **Error Rates**: Failed connections and data quality issues
- **Resource Usage**: CPU, memory, and disk utilization

#### Mission Metrics

- **Altitude Tracking**: Real-time altitude monitoring
- **Deployment Detection**: Accelerometer-based deployment sensing
- **Environmental Conditions**: Temperature and humidity tracking
- **System Reliability**: Uptime and fault statistics

### 🔄 Maintenance

#### Regular Maintenance

1. **Configuration Backups**: Automatic and manual backup creation
2. **Log Rotation**: Automated log cleanup and archival
3. **System Updates**: Software and configuration updates
4. **Sensor Calibration**: Periodic calibration verification

#### Backup and Recovery

- **Automatic Backups**: Scheduled configuration snapshots
- **Manual Backups**: On-demand backup creation
- **Recovery Procedures**: Restore from backup with validation
- **Disaster Recovery**: Complete system restoration

### 🤝 Contributing

#### Development Setup

1. Clone the repository
2. Install development dependencies: `pip install -r requirements-dev.txt`
3. Run tests: `pytest`
4. Follow coding standards: PEP 8 compliance

#### Testing

- **Unit Tests**: Individual component testing
- **Integration Tests**: End-to-end system testing
- **Hardware Tests**: Physical sensor validation
- **Performance Tests**: Load and stress testing

### 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

### 🆘 Support

- **Documentation**: Comprehensive inline documentation
- **Examples**: Working code examples and configurations
- **Issue Tracking**: GitHub issues for bug reports and feature requests
- **Community**: Discussion forums and user community

### 🔗 Related Projects

- **Phidgets Library**: Official Phidget sensor support
- **OPC-UA Foundation**: Industrial communication standards
- **Industrial IoT Stack**: Broader industrial integration platform

---

**CT-084 Parachute Drop System - Mission-Critical Sensor Integration**

*Built for reliability, designed for performance, tested for mission-critical operations.*