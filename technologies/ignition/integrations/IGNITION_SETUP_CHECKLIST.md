# Ignition Integration Setup Checklist
> Step-by-step guide to complete the Node-RED → Ignition integration

## 🎯 Current Status
✅ Node-RED running with test data flowing (662 MQTT msgs, 178 OPC msgs)  
✅ Ignition Gateway running (http://localhost:8088)  
✅ OPC-UA Server active on port 62541  
⚠️ Tags not appearing in Ignition Tag Browser  

## 🔧 Required Setup Steps

### **Step 1: Check Ignition Modules**
📍 **Location**: http://localhost:8088/web/config/modules

**Required Modules:**
- [ ] **MQTT Engine** - Receives MQTT data from Node-RED
- [ ] **MQTT Transmission** - Bidirectional MQTT communication  
- [ ] **OPC-UA Server** - ✅ Already confirmed active
- [ ] **Tag Historian** (optional) - For data storage

### **Step 2: Configure MQTT Engine**
📍 **Location**: Gateway → Configure → MQTT Engine → Settings

**Connection Settings:**
```
Broker URL: tcp://localhost:1883
Client ID: IgnitionMQTTEngine
Username: (blank for anonymous)
Password: (blank for anonymous) 
Auto-connect: Enabled
```

**Tag Group Configuration:**
```
Group Name: NodeRED_Data
Subscription Topic: UNS/+/+/+/+
Tag Provider: [default]
Base Tag Path: SteelBonnet
```

### **Step 3: Create Tag Structure**
📍 **Location**: Designer → Tag Browser

**Expected Node-RED Topics → Ignition Tags:**
```
brewery/fermenter/1/temp          → [default]SteelBonnet/Brewery/Fermenter1/Temperature
brewery/fermenter/1/pH            → [default]SteelBonnet/Brewery/Fermenter1/pH  
VFD_1/Current                     → [default]SteelBonnet/Utilities/VFD_1/Current
Ambient_Temp                      → [default]SteelBonnet/Environment/Ambient_Temp
```

### **Step 4: Verify Data Flow**
📍 **Location**: Designer → Tag Browser

**Verification Steps:**
1. Open Ignition Designer
2. Navigate to Tag Browser  
3. Look for `[default]` → `SteelBonnet` folder
4. Check if folders/tags are auto-created
5. Verify tag values are updating

### **Step 5: Install Keith Gamble's Module (Optional)**
📍 **Repository**: github.com/slimstrongarm/ignition-project-scan-endpoint

**Build Steps:**
```bash
git clone https://github.com/slimstrongarm/ignition-project-scan-endpoint.git
cd ignition-project-scan-endpoint
cp gradle.properties.template gradle.properties
# Edit gradle.properties with signing info
./gradlew build
```

**Install Steps:**
1. Copy built .modl file to Gateway
2. Install via Gateway → Configure → Modules
3. Test endpoint: `GET /data/project-scan-endpoint/confirm-support`

## 🔍 Debugging Issues

### **Issue: No Tags Appearing**
**Cause**: MQTT Engine not configured or not connecting  
**Solution**:
1. Check MQTT Engine status in Gateway
2. Verify broker connection to localhost:1883
3. Check MQTT topic subscriptions
4. Review Gateway logs for errors

### **Issue: Tags Created But No Data**
**Cause**: Topic mapping or data format issues  
**Solution**:
1. Check Node-RED MQTT topic format
2. Verify tag group subscription patterns
3. Check data type mapping
4. Monitor MQTT traffic with `mosquitto_sub -t "#"`

### **Issue: OPC-UA Connection Errors**
**Cause**: Security policy or endpoint configuration  
**Solution**:
1. Set OPC-UA server to allow anonymous connections
2. Use `None` security policy for testing
3. Check endpoint URL: `opc.tcp://localhost:62541/discovery`

## 🚀 Quick Test Commands

### **Check MQTT Traffic:**
```bash
# Monitor all MQTT topics
mosquitto_sub -h localhost -t "#" -v

# Monitor specific Node-RED topics  
mosquitto_sub -h localhost -t "brewery/#" -v
mosquitto_sub -h localhost -t "UNS/#" -v
```

### **Check Ignition Connectivity:**
```bash
# Basic connection test
curl -I http://localhost:8088

# OPC-UA server test (if client available)
# opcua-client opc.tcp://localhost:62541/discovery
```

## ✅ Success Criteria

### **Integration Working When:**
- [ ] MQTT Engine shows "Connected" status in Gateway
- [ ] SteelBonnet folder appears in Tag Browser
- [ ] Tags auto-created with live data from Node-RED
- [ ] Tag values updating in real-time (68.1°F, pH 4.39, etc.)
- [ ] No errors in Gateway logs
- [ ] VSCode can interact with Ignition (if module installed)

### **Expected Tag Values (from Node-RED):**
- `Fermenter1/Temperature`: ~68.1°F
- `Fermenter1/pH`: ~4.39  
- `VFD_1/Current`: ~12.7A
- `Ambient_Temp`: ~81°F

---
**Next Action**: Check Ignition Gateway modules and configure MQTT Engine