# TODO: Pi Edge Node Deployment

## Current Status
- ✅ Pi + Phidget documentation complete
- ✅ Started working with Pi units
- ⏳ Need to standardize deployment
- ⏳ OPC-UA client configuration needed

## Phase 1: First Pi Setup (Fermentation Area)

### 1.1 Hardware Setup
- [ ] Select Pi location (near FV1?)
- [ ] Mount Pi in enclosure
- [ ] Connect VINT Hub via USB
- [ ] Install Phidget sensors:
  - [ ] Port 0: FV1 Temperature/Humidity (HUM1001)
  - [ ] Port 1: FV2 Temperature/Humidity (HUM1001)
  - [ ] Port 2: Glycol Supply Temp
  - [ ] Port 3: Glycol Return Temp
- [ ] Connect to network (Ethernet preferred)
- [ ] Power up and verify LEDs

### 1.2 Software Installation
- [ ] Flash SD card with Raspberry Pi OS Lite
- [ ] Run initial setup script:
  ```bash
  curl -sSL https://raw.githubusercontent.com/.../pi-initial-setup.sh | bash
  ```
- [ ] Install Phidget libraries
- [ ] Install Node-RED
- [ ] Configure auto-start services
- [ ] Set up Tailscale for remote access

### 1.3 Phidget Testing
- [ ] Run device discovery test
- [ ] Verify all sensors detected
- [ ] Test data quality and update rates
- [ ] Log 1-hour of test data
- [ ] Validate temperature ranges

## Phase 2: OPC-UA Integration

### 2.1 Direct OPC-UA Publishing
- [ ] Install OPC-UA client library
- [ ] Configure Ignition endpoint
- [ ] Set up certificate exchange
- [ ] Create node namespace
- [ ] Test single tag write

### 2.2 Data Structure
- [ ] Implement UNS path building:
  ```
  SteelBonnet/Brewery/ColdSide/FV1/Temperature
  SteelBonnet/Brewery/ColdSide/FV1/Humidity
  ```
- [ ] Add metadata tags (quality, timestamp)
- [ ] Implement buffering for network outages
- [ ] Add diagnostics tags (Pi health)

### 2.3 Self-Registration
- [ ] Pi announces itself on startup
- [ ] Publishes capability list
- [ ] Creates tag structure in Ignition
- [ ] Maintains heartbeat

## Phase 3: Production Deployment

### 3.1 Reliability Features
- [ ] Implement store-and-forward
- [ ] Add watchdog timer
- [ ] Configure log rotation
- [ ] Set up automatic updates
- [ ] Create backup scripts

### 3.2 Monitoring
- [ ] CPU/Memory/Temperature monitoring
- [ ] Network connectivity checks
- [ ] Sensor health validation
- [ ] SD card health monitoring
- [ ] Alert on failures

### 3.3 Deployment Tools
- [ ] Create golden image for SD cards
- [ ] Ansible playbook for updates
- [ ] Remote deployment script
- [ ] Health check dashboard
- [ ] Documentation for ops team

## Success Criteria
- [ ] Pi runs 7 days without intervention
- [ ] Automatic recovery from power loss
- [ ] Data gaps < 1 minute during network issues
- [ ] Remote management via Tailscale
- [ ] Sensor data accurate within ±0.5°C

## Scale-Out Plan
1. Pi-Edge-001: Fermentation (This TODO)
2. Pi-Edge-002: Hot Side
3. Pi-Edge-003: Utilities
4. Pi-Edge-004: Packaging

## Server Integration Notes
- Tailscale mesh network for secure access
- Central logging to your new server
- Backup sensor data to server
- Grafana dashboards for Pi fleet health