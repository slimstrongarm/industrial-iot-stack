# 🍺 Actual Brewery MQTT Topic Analysis - FOUND!
**Date**: 2025-06-06  
**Source**: dcramb/zymnist-sbbc-scmc GitHub repository  
**Status**: ✅ COMPLETE - Found actual MQTT structure!

## 🔍 **ACTUAL Topic Structure Discovered**

### **Command Topics** (Incoming)
```
cmd/zymnist/sbbc/zym-017556/#
cmd/zymnist/sbbc/zym-017556/hlt_heat_pid
```

### **Status Topics** (Outgoing)  
```
sta/zymnist/sbbc/zym-017556/{botlet_id}
```

### **ZymBoard Topics** (ThingsBoard Integration)
```
v1/devices/me/telemetry
v1/devices/me/attributes
```

## 📊 **Topic Breakdown**

### **Command Structure:**
```
cmd/{app}/{account}/{bot_id}/{botlet_id}
```
Where:
- **app**: `zymnist` (company name)
- **account**: `sbbc` (Santa Barbara Brewing Company)
- **bot_id**: `zym-017556` (hardware device ID)
- **botlet_id**: `hlt_heat_pid` (specific controller/function)

### **Status Structure:**
```
sta/{app}/{account}/{bot_id}/{botlet_id}
```

## 🏭 **Equipment Identified**

### **Bot ID**: `zym-017556`
- **Type**: Controller/Gateway device
- **Functions**:
  - `hlt_heat_pid` - Hot Liquor Tank heating PID controller
  - Other relay controls and sensors

### **Parameters Monitored**:
- `analog_input_1` - Temperature sensor 1
- `analog_input_error_1` - Sensor 1 error status
- `analog_input_2` - Temperature sensor 2  
- `analog_input_error_2` - Sensor 2 error status
- `heat_power` - Heating element power output
- `set_point` - Temperature setpoint
- `control_loop_mode` - PID control mode (auto/manual/off)

## 💾 **Actual Payload Examples**

### **Command Payload:**
```json
{
  "msgType": "cmd",
  "app": "zymnist",
  "accnt": "sbbc",
  "bot": "zym-017556",
  "botlet": "hlt_heat_pid",
  "cmd": "read",
  "properties": {
    "parameter": {
      "name": "analog_input_1"
    },
    "change_only": true
  }
}
```

### **Status Payload:**
```json
{
  "msgType": "sta",
  "app": "zymnist", 
  "accnt": "sbbc",
  "bot": "zym-017556",
  "botlet": "hlt_heat_pid",
  "properties": {
    "parameter": {
      "name": "analog_input_1",
      "value": 152.5
    }
  }
}
```

## 🔗 **MQTT Brokers Used**

### **Primary IoT Broker:**
- **Host**: `mqtts://r77c68a0.ala.us-east-1.emqxsl.com`
- **Port**: `8883` (TLS)
- **Type**: Cloud EMQX broker

### **Local ZymBoard:**
- **Host**: `192.168.0.22`
- **Port**: `1993`
- **Type**: Local ThingsBoard integration

## 🔄 **Translation to Our UNS Structure**

### **Their Topics → Our UNS Topics:**
```
cmd/zymnist/sbbc/zym-017556/hlt_heat_pid
    ↓ TRANSLATE TO ↓
salinas/brewery/brew_house/hlt/temperature/command

sta/zymnist/sbbc/zym-017556/hlt_heat_pid  
    ↓ TRANSLATE TO ↓
salinas/brewery/brew_house/hlt/temperature/telemetry
```

## 🎯 **Node-RED Translation Design**

### **Input Topics to Monitor:**
```
sta/zymnist/sbbc/+/+           # All status messages
cmd/zymnist/sbbc/+/+           # All command messages  
v1/devices/me/telemetry        # ThingsBoard telemetry
v1/devices/me/attributes       # ThingsBoard attributes
```

### **Output UNS Topics:**
```
salinas/brewery/brew_house/hlt/temperature/telemetry
salinas/brewery/brew_house/hlt/temperature/command
salinas/brewery/brew_house/hlt/heating/telemetry
salinas/brewery/brew_house/hlt/heating/command
```

## 🏗️ **Equipment Type Mapping**

| Botlet ID | Equipment Type | UNS Location | Function |
|-----------|----------------|--------------|----------|
| hlt_heat_pid | Hot Liquor Tank | brew_house/hlt | Temperature control |
| (others TBD) | Fermentation | production/fermentation | Temperature monitoring |
| (others TBD) | Utilities | utilities/compressed_air | Support systems |

## 🚀 **Implementation Ready**

✅ **Found actual MQTT topics**  
✅ **Discovered payload structure**  
✅ **Identified equipment types**  
✅ **Mapped to UNS structure**  
✅ **Ready for Node-RED translation**  

## 📝 **Next Steps**
1. Create Node-RED translation flow using actual topic patterns
2. Map all botlet types to UNS equipment categories
3. Handle both command and status message translation
4. Test with simulated brewery data
5. Deploy for Friday demo

---
**🎉 SUCCESS**: Found real brewery MQTT structure - no more guessing!