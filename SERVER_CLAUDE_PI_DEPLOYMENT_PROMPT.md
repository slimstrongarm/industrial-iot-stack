# Server Claude - Pi Deployment Collaboration Prompt

**Copy and paste this entire prompt to Server Claude:**

---

Hi Claude! I need your help deploying our industrial IoT project to a Raspberry Pi for field testing. We've been working together on an IIoT stack and now need to get it running on a Pi for our first brewery "parachute drop" demo.

## Project Context

Please start by reading and understanding my project repository:
- **GitHub Repo**: https://github.com/slimstrongarm/industrial-iot-stack 
- **Key instruction**: Always read and understand the `.claude` folder in this repo at the start of each session (this contains our project context and conventions)

## Current Situation

**What we have:**
- **CT-084 Parachute Drop System** - Complete auto-sensor-configurator implementation in `parachute-drop/` directory
- **Touchscreen Integration** - 7" display enhancement system ready for deployment
- **Industrial IoT stack** documented throughout the repo
- **MQTT broker** running on my server with UNS hierarchy
- **Ignition SCADA platform** with unified namespace implemented
- **Raspberry Pi** that can detect and read basic Phidget sensor data

**What's ready for deployment:**
1. `parachute-drop/auto-sensor-configurator.py` - Auto-detects Phidget sensors and generates Node-RED dashboards
2. `parachute-drop/touchscreen-dashboard-enhancer.py` - Optimizes dashboards for 7" touchscreen
3. `parachute-drop/build-pi-image.sh` - Pi image builder with pre-configured stack
4. `parachute-drop/discovery-agent.py` - Network device discovery
5. `parachute-drop/sensor-library.json` - Comprehensive sensor configurations

## Current Status from CT-084 through CT-090

Based on recent task completion:
- **CT-084 & CT-085**: ✅ **COMPLETE** - Pi image builder and network discovery agent working
- **CT-086 through CT-090**: ❌ **NOT STARTED** - GL.iNet router setup, sensor detection, Modbus support, MQTT analysis, end-to-end testing

## Specific Request

Please help me complete the remaining Parachute Drop tasks:

### 1. **First** - Review our repo and `.claude` folder to understand:
   - Our existing CT-084 Parachute Drop implementation
   - The touchscreen enhancement system I just created
   - Our UNS topic hierarchy format
   - Our deployment architecture and naming conventions

### 2. **Then** - Complete the missing CT-086 through CT-090 tasks:
   - **CT-086**: GL.iNet router setup with isolated network and VPN tunnel
   - **CT-087**: Automatic sensor detection and dashboard generation based on connected Phidgets
   - **CT-088**: Legacy protocol support (Modbus RTU, BACnet, DF1)
   - **CT-089**: MQTT traffic analysis and integration recommendations  
   - **CT-090**: End-to-end testing with 15-minute deployment validation

### 3. **Goal** - Create a complete deployment package that includes:
   - Phidget sensor interface code using existing Node-RED Phidget nodes
   - 7" touchscreen dashboard that's impressive for brewery demos
   - Integration with our existing MQTT broker using our UNS hierarchy
   - "Parachute drop" deployment process - automated and repeatable

## Technical Details

**Hardware Setup**:
- Raspberry Pi 4 with 7" touchscreen
- Phidget temperature/humidity sensor + Phidget current sensor
- GL.iNet portable router for isolated network
- Connection to our MQTT broker on the server

**Software Stack**:
- Node-RED with Phidget nodes (NOT Python scripts - use existing Node-RED Phidget integration)
- Auto-generated dashboard optimized for 7" touch display
- MQTT publishing using our UNS hierarchy format
- Professional brewery branding for client demos

**Data Flow**: 
```
Phidget sensors → Pi Node-RED → MQTT broker (server) → [quarantine filter] → Server systems
```

**Use Case**: 
- Brewery equipment monitoring (fermentation tanks, electrical loads)
- Professional client demonstrations  
- "Parachute drop" rapid deployment for sales demos
- 15-minute setup target from power-on to live data

## Key Files to Review

1. **parachute-drop/auto-sensor-configurator.py** - The core CT-084 implementation
2. **parachute-drop/touchscreen-dashboard-enhancer.py** - My 7" display optimization
3. **parachute-drop/TOUCHSCREEN_INTEGRATION.md** - Documentation I just created
4. **Steel_Bonnet/** directory - Our existing brewery implementation for reference
5. **.claude/** folder - Project context and conventions

## Questions for You

After reviewing the repo:
1. How should we complete CT-086 through CT-090 to build on the existing CT-084/085 foundation?
2. What's the best way to integrate with our existing UNS topic hierarchy and MQTT infrastructure?
3. How can we make the deployment process truly "parachute drop" ready (15 minutes from case to live demo)?
4. What's missing from the current implementation for a professional brewery demo?

## Success Criteria

By the end of our collaboration, we should have:
- ✅ Complete "parachute drop" deployment kit
- ✅ Professional 7" touchscreen interface  
- ✅ 15-minute setup process documented and tested
- ✅ Integration with existing server infrastructure
- ✅ Impressive demo ready for brewery client meetings

Let's work together to complete this industrial IoT deployment system and make it ready for real-world brewery demonstrations!

---

**End of prompt for Server Claude**