# CT-058: Monitoring Dashboard Design Draft

## 🎯 **Purpose**
Create a unified "Monitoring Dashboard" tab in Google Sheets that provides real-time visibility into the entire Industrial IoT stack health and performance.

## 📊 **Dashboard Layout Design**

### **Section A: System Overview (Rows 1-8)**
```
┌─────────────────────────────────────────────────────────────────┐
│  🏭 INDUSTRIAL IOT STACK - MONITORING DASHBOARD                 │
├─────────────────────────────────────────────────────────────────┤
│  Overall Status: ● HEALTHY        Last Updated: 2025-06-07 15:30│
│  Active Alerts: 0                 Uptime: 99.2%                 │
└─────────────────────────────────────────────────────────────────┘
```

### **Section B: Container Health (Rows 10-20)**
```
🐳 DOCKER CONTAINERS
┌──────────────────────┬────────────┬─────────┬──────────┬─────────┐
│ Container            │ Status     │ CPU %   │ Memory   │ Uptime  │
├──────────────────────┼────────────┼─────────┼──────────┼─────────┤
│ discord-claude-bot   │ ● RUNNING  │ 2.1%    │ 45MB     │ 2d 14h  │
│ mac-claude-worker    │ ● RUNNING  │ 1.8%    │ 32MB     │ 2d 14h  │
│ iiot-emqx           │ ● RUNNING  │ 3.2%    │ 128MB    │ 5d 2h   │
│ iiot-node-red       │ ● RUNNING  │ 4.1%    │ 89MB     │ 5d 2h   │
│ iiot-n8n            │ ● RUNNING  │ 2.9%    │ 156MB    │ 5d 2h   │
│ iiot-ignition       │ ● RUNNING  │ 8.5%    │ 512MB    │ 5d 2h   │
│ iiot-timescaledb    │ ● RUNNING  │ 1.2%    │ 234MB    │ 5d 2h   │
└──────────────────────┴────────────┴─────────┴──────────┴─────────┘
```

### **Section C: Industrial Systems (Rows 22-32)**
```
🏭 INDUSTRIAL SYSTEMS
┌──────────────────────┬────────────┬─────────────────┬─────────────┐
│ System               │ Status     │ Response Time   │ Last Check  │
├──────────────────────┼────────────┼─────────────────┼─────────────┤
│ MQTT Broker (EMQX)   │ ● HEALTHY  │ 12ms            │ 15:29       │
│ Node-RED Flows       │ ● HEALTHY  │ 45ms            │ 15:29       │
│ Ignition Gateway     │ ● HEALTHY  │ 89ms            │ 15:29       │
│ OPC UA Server        │ ● HEALTHY  │ 23ms            │ 15:29       │
│ Steel Bonnet MQTT    │ ● HEALTHY  │ 8ms             │ 15:29       │
│ WhatsApp Integration │ ● HEALTHY  │ 156ms           │ 15:28       │
│ Google Sheets API    │ ● HEALTHY  │ 234ms           │ 15:29       │
└──────────────────────┴────────────┴─────────────────┴─────────────┘
```

### **Section D: Equipment Monitoring (Rows 34-44)**
```
🏭 STEEL BONNET EQUIPMENT
┌──────────────────────┬────────────┬─────────────────┬─────────────┐
│ Equipment            │ Status     │ Current Value   │ Last Update │
├──────────────────────┼────────────┼─────────────────┼─────────────┤
│ Boiler 001          │ ● RUNNING  │ 165°F           │ 15:29       │
│ Pump 001            │ ● RUNNING  │ 245 GPM         │ 15:29       │
│ Chiller 001         │ ● RUNNING  │ 2.1°F           │ 15:29       │
│ Air Compressor       │ ● RUNNING  │ 87 PSI          │ 15:29       │
│ Walk-in Chiller      │ ● RUNNING  │ 38°F            │ 15:29       │
└──────────────────────┴────────────┴─────────────────┴─────────────┘
```

### **Section E: System Resources (Rows 46-54)**
```
💻 SYSTEM RESOURCES
┌──────────────────────┬────────────┬─────────────────┬─────────────┐
│ Resource             │ Current    │ Threshold       │ Status      │
├──────────────────────┼────────────┼─────────────────┼─────────────┤
│ CPU Usage            │ 23.4%      │ <80%            │ ● NORMAL    │
│ Memory Usage         │ 67.2%      │ <85%            │ ● NORMAL    │
│ Disk Usage           │ 45.8%      │ <90%            │ ● NORMAL    │
│ Network I/O          │ 12.3 MB/s  │ <100 MB/s       │ ● NORMAL    │
│ MQTT Messages/sec    │ 847        │ <5000           │ ● NORMAL    │
└──────────────────────┴────────────┴─────────────────┴─────────────┘
```

### **Section F: Recent Alerts & Activity (Rows 56-66)**
```
🚨 RECENT ALERTS & ACTIVITY
┌─────────────┬─────────┬──────────────────────────────────────┬────────────┐
│ Time        │ Type    │ Description                          │ Status     │
├─────────────┼─────────┼──────────────────────────────────────┼────────────┤
│ 15:25       │ INFO    │ Discord bot restarted successfully   │ RESOLVED   │
│ 14:45       │ WARNING │ High CPU usage detected (82%)        │ RESOLVED   │
│ 13:12       │ INFO    │ Steel Bonnet equipment data updated  │ NORMAL     │
│ 12:55       │ SUCCESS │ CT-058 monitoring dashboard created  │ COMPLETE   │
└─────────────┴─────────┴──────────────────────────────────────┴────────────┘
```

### **Section G: Quick Actions (Rows 68-75)**
```
⚡ QUICK ACTIONS
┌─────────────────────────────────────────────────────────────────┐
│ [Refresh All Data]  [Run Health Check]  [Export Report]        │
│ [Restart Services]  [View Logs]        [Create Alert]          │
└─────────────────────────────────────────────────────────────────┘
```

## 🎨 **Visual Design Elements**

### **Status Indicators**
- **🟢 ● HEALTHY/RUNNING/NORMAL** - Green background
- **🟡 ● WARNING/DEGRADED** - Yellow background  
- **🔴 ● CRITICAL/ERROR/DOWN** - Red background
- **⚪ ● UNKNOWN/PENDING** - Gray background

### **Color Coding**
- **Headers**: Dark blue background (#1a73e8), white text
- **Status Good**: Light green background (#d4f3d0)
- **Status Warning**: Light yellow background (#fff4c4)
- **Status Critical**: Light red background (#fce8e6)
- **System Resources**: Progress bar formatting based on thresholds

### **Conditional Formatting Rules**
1. **CPU/Memory/Disk** - Green <70%, Yellow 70-85%, Red >85%
2. **Response Times** - Green <100ms, Yellow 100-500ms, Red >500ms
3. **Container Status** - Green "RUNNING", Red anything else
4. **Equipment Status** - Green "RUNNING", Yellow "WARNING", Red "ERROR"

## 🔌 **Integration Points**

### **Data Sources**
1. **`unified_industrial_monitor.py`** - Primary data collector
2. **Docker API** - Container health and resource usage
3. **MQTT Broker** - Real-time equipment data
4. **Node-RED API** - Flow status and performance
5. **Ignition Gateway API** - System health and OPC data
6. **Google Sheets API** - Task status and activity logs

### **Update Mechanisms**
1. **Real-time Updates** - Every 30 seconds via monitoring script
2. **Manual Refresh** - Button to force immediate update
3. **Scheduled Reports** - Hourly snapshots for trending
4. **Alert Triggers** - Immediate updates when thresholds exceeded

### **Script Integration**
```python
# Main update function called by unified_industrial_monitor.py
def update_monitoring_dashboard(monitoring_data):
    # Update Container Health section
    update_container_status(monitoring_data['docker_containers'])
    
    # Update Industrial Systems section  
    update_industrial_systems(monitoring_data['mqtt_brokers'], 
                             monitoring_data['node_red'],
                             monitoring_data['ignition'])
    
    # Update Equipment section
    update_equipment_status(monitoring_data['steel_bonnet_equipment'])
    
    # Update System Resources
    update_system_resources(monitoring_data['system_metrics'])
    
    # Update Activity Log
    add_activity_log_entry("Dashboard updated", "INFO")
```

## 📱 **Mobile Optimization**

### **Discord Integration**
- **Status commands**: `!status` returns dashboard summary
- **Alert integration**: Critical alerts posted to Discord channels
- **Mobile viewing**: Dashboard optimized for mobile Google Sheets app

### **WhatsApp Integration**  
- **Critical alerts**: Automatic WhatsApp messages for system failures
- **Daily summaries**: End-of-day status reports via WhatsApp

## 🎯 **Success Metrics**

### **Operational Goals**
1. **<30 second** dashboard load time
2. **99%+ uptime** visibility across all systems
3. **<2 minute** mean time to alert (MTTA)
4. **Mobile-first** accessibility from anywhere

### **User Experience**
1. **Single pane of glass** - no need to check multiple systems
2. **Actionable insights** - clear next steps for any issues
3. **Trend visibility** - easy to spot patterns over time
4. **Alert fatigue prevention** - intelligent thresholding

## 🚀 **Implementation Plan**

### **Phase 1: Core Dashboard (This Week)**
1. Create Google Sheets tab with basic layout
2. Implement container health monitoring
3. Add system status indicators
4. Basic conditional formatting

### **Phase 2: Enhanced Features (Next Week)**  
1. Equipment monitoring integration
2. Real-time data updates
3. Alert history and trending
4. Mobile optimization

### **Phase 3: Advanced Intelligence (Future)**
1. Predictive analytics
2. Automated remediation suggestions
3. Performance trending and forecasting
4. Integration with maintenance schedules

---

**This dashboard will transform operations from reactive monitoring to proactive management, providing complete Industrial IoT stack visibility in a single, mobile-accessible interface.** 🏭📊