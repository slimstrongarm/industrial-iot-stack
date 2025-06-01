# Ignition Integration Setup Guide
> Complete setup for VSCode Flint + Ignition Gateway integration

## 🎯 Current Status

### ✅ **Working Now**
- Node-RED flowing simulated data (MQTT: 662 msgs, Modbus: 586 msgs, OPC-UA: 178 msgs)
- Test infrastructure passing (7/19 flows active)
- Equipment registration working (54 devices managed)

### ⚠️ **Missing Link**
- Tags not appearing in Ignition Tag Browser
- Need Flint VSCode extension + Ignition gateway module

## 🔧 Setup Required

### **Step 1: Install Flint for Ignition VSCode Extension**
```bash
# In VSCode:
# 1. Open Extensions (Cmd+Shift+X)
# 2. Search "Flint for Ignition" 
# 3. Install by Keith Gamble
# 4. Reload VSCode
```

### **Step 2: Check Ignition Gateway Modules**
Access: http://localhost:8088/web/config/modules

**Required Modules for Integration:**
- **MQTT Engine** - For MQTT → Ignition bridge
- **MQTT Transmission** - For Node-RED ↔ Ignition communication  
- **OPC-UA Server** - Already confirmed running on port 62541
- **Web Services** - For REST API integration (if needed)

### **Step 3: Configure MQTT Integration**
In Ignition Gateway Config:
1. **MQTT Engine Settings**:
   - Broker URL: `tcp://localhost:1883`
   - Client ID: `IgnitionMQTTEngine`
   - Auto-connect: Enabled

2. **Create MQTT Tag Groups**:
   - Group Name: `NodeRED_Data`
   - Topic: `UNS/+/+/+/+`
   - Tag Path: `[default]SteelBonnet`

### **Step 4: Verify Tag Creation Path**
**Expected Flow:**
```
Node-RED MQTT Publish → MQTT Broker → MQTT Engine → Ignition Tags
```

**Debug Steps:**
1. Check MQTT Engine status in Gateway
2. Verify MQTT topics being published
3. Check tag provider configuration
4. Look for errors in Gateway logs

## 🔍 Debugging Current Issue

### **Check MQTT Topics Being Published**
```bash
# Monitor MQTT traffic
mosquitto_sub -h localhost -t "UNS/#" -v
```

### **Check Ignition Gateway Logs**
Access: http://localhost:8088/web/status/diagnostics/logs

**Look for:**
- MQTT Engine connection status
- Tag creation attempts  
- OPC-UA server activity
- Any error messages

### **Verify OPC-UA Endpoint**
The Node-RED logs show OPC-UA connection errors:
```
Error: End point must exist opc.tcp://localhost:62541/discovery
securityMode = None  securityPolicy = None
```

**Fix Required:**
1. Check Ignition OPC-UA server settings
2. Verify security policy configuration
3. Ensure anonymous connections allowed

## 📚 Documentation Strategy for Agent Army

### **Technology-Specific Documentation**

#### **Node-RED Agents**
```
docs/node-red/
├── api-reference.pdf          # Node-RED API documentation
├── flow-patterns.md           # Common flow patterns
├── mqtt-integration.md        # MQTT best practices
└── troubleshooting.md         # Common issues & fixes
```

#### **Ignition Agents**  
```
docs/ignition/
├── scripting-api.pdf          # Ignition scripting reference
├── udt-patterns.md            # UDT design patterns
├── mqtt-engine-config.md      # MQTT Engine setup
└── flint-integration.md       # VSCode Flint usage
```

#### **Protocol Documentation**
```
docs/protocols/
├── mqtt-specifications.pdf    # MQTT 3.1.1 & 5.0 specs
├── opcua-reference.pdf        # OPC-UA specification
├── modbus-tcp-guide.pdf       # Modbus TCP reference
└── isa95-standard.pdf         # ISA-95 hierarchy standard
```

### **Agent-Accessible Documentation**
```python
# In agents, reference docs like:
def get_mqtt_spec():
    return read_file("docs/protocols/mqtt-specifications.pdf")

def get_ignition_api():
    return read_file("docs/ignition/scripting-api.pdf")
```

## 🚀 Immediate Next Steps

### **1. Install Flint Extension**
- Install Keith Gamble's Flint for Ignition in VSCode
- Check for any configuration prompts

### **2. Check Gateway Modules** 
- Access http://localhost:8088/web/config/modules
- Verify MQTT Engine installed
- Install missing modules if needed

### **3. Fix OPC-UA Connection**
- Check OPC-UA server security settings
- Allow anonymous connections for testing
- Verify endpoint configuration

### **4. Monitor Tag Creation**
- Use Gateway diagnostics to watch tag creation
- Check for MQTT Engine activity
- Verify tag provider setup

## 🎖️ Success Criteria

### **When Integration is Working:**
- ✅ Tags appear in Ignition Tag Browser under `[default]/SteelBonnet/`
- ✅ Live data from Node-RED visible in Ignition
- ✅ VSCode can read/write Ignition scripts via Flint
- ✅ Bidirectional communication working

### **Expected Tag Structure:**
```
[default]
├── SteelBonnet/
│   ├── Brewery/
│   │   ├── Fermenter1/
│   │   │   ├── Temperature: 68.1°F
│   │   │   ├── Pressure: 1.2 bar  
│   │   │   └── pH: 4.39
│   │   └── Utilities/
│   │       └── VFD_1/
│   │           └── Current: 12.7A
│   └── NodeRED/
│       ├── TestResults/
│       └── EquipmentRegistry/
```

---
**Ready to complete the missing link and see those tags in Ignition! 🔗**