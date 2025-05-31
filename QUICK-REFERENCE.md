# Steel Bonnet IIoT Quick Reference

## Critical Information

### Jython 2.7 Constraints in Ignition
```python
# ❌ DON'T use f-strings
wrong = f"Temperature: {temp}"

# ✅ DO use .format() or %
right = "Temperature: {}".format(temp)
right = "Temperature: %s" % temp

# ❌ DON'T use Python 3 features
# ✅ DO test everything in Script Console first
```

### UNS Topic Structure
```
SteelBonnet/Brewery/{Area}/{Equipment}/{Measurement}

Examples:
SteelBonnet/Brewery/ColdSide/FV1/Temperature
SteelBonnet/Brewery/Utilities/AirCompressor/Pressure
SteelBonnet/Brewery/HotSide/Boiler/Status
```

### Key Integration Points

1. **PLC → Ignition Edge**
   - Protocol: Modbus TCP
   - Already configured and working

2. **MQTT → Node-RED → OPC-UA → Ignition**
   - Legacy devices publish to MQTT
   - Node-RED subscribes and transforms
   - Creates OPC-UA tags in Ignition
   - Acts as quarantine/validation layer

3. **Pi + Phidget → OPC-UA → Ignition**
   - Direct OPC-UA publishing (cleaner)
   - No MQTT middleman needed
   - Each Pi is an OPC-UA client

### Common Commands

```bash
# Test Phidget sensors on Pi
ssh pi@raspberrypi.local
python3 /home/pi/edge-node/phidget_device_test.py

# Monitor MQTT traffic
mosquitto_sub -h localhost -t "SteelBonnet/#" -v

# Check Node-RED flows
http://[node-red-host]:1880

# Ignition Edge Gateway
http://[ignition-host]:8088
```

### Testing Workflow

1. **Before deploying to field:**
   ```python
   # In Ignition Script Console
   udtFactory_unified.test_udt_creation("Test_Pump_001")
   ```

2. **Validate MQTT flow:**
   ```bash
   # Publish test message
   mosquitto_pub -t "SteelBonnet/Brewery/Test/Pump/Status" -m "1"
   # Check if OPC tag created in Ignition
   ```

3. **Pi deployment checklist:**
   - [ ] Install OS and updates
   - [ ] Run pi-initial-setup.sh
   - [ ] Install Phidget libraries
   - [ ] Deploy Node-RED
   - [ ] Test sensor connectivity
   - [ ] Configure OPC-UA endpoint

### Architecture Decision Log

1. **Why MQTT quarantine?**
   - Legacy devices with non-standard data
   - Need validation before OPC tags
   - Easier to modify Node-RED than Jython

2. **Why direct OPC-UA for Pi?**
   - Cleaner data path
   - Better performance
   - Native Ignition integration

3. **Why Jython 2.7 still?**
   - Ignition legacy compatibility
   - Can't upgrade without breaking changes
   - Must test everything thoroughly

### Next Actions Priority

1. **Deploy first Pi unit** in fermentation area
2. **Test end-to-end data flow**
3. **Create Ignition screens** for operators
4. **Document standard procedures**
5. **Train operations team**