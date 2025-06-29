/**
 * Node-RED Dashboard Generator for CT-084 Parachute Drop System
 * Automatically generates professional industrial dashboards based on discovered sensors
 * Author: Agent 3 - Dashboard Generator and Production Deployment
 */

const path = require('path');
const fs = require('fs').promises;

class DashboardGenerator {
    constructor(options = {}) {
        this.options = {
            templatePath: options.templatePath || './templates',
            outputPath: options.outputPath || './generated-dashboards',
            siteName: options.siteName || 'Industrial IoT System',
            theme: options.theme || 'dark',
            enableSecurity: options.enableSecurity !== false,
            ...options
        };
        
        this.discoveredSensors = new Map();
        this.equipmentGroups = new Map();
        this.dashboardLayout = null;
        this.generatedFlows = [];
    }

    /**
     * Auto-discover sensors and equipment from various sources
     */
    async discoverSensors() {
        console.log('🔍 Starting sensor discovery...');
        
        // Discovery sources
        const discoveries = await Promise.allSettled([
            this.discoverPhidgetSensors(),
            this.discoverOPCUATags(),
            this.discoverMQTTTopics(),
            this.discoverModbusDevices()
        ]);
        
        discoveries.forEach((result, index) => {
            const sources = ['Phidget', 'OPC-UA', 'MQTT', 'Modbus'];
            if (result.status === 'fulfilled') {
                console.log(`✅ ${sources[index]} discovery completed: ${result.value.length} devices found`);
            } else {
                console.log(`⚠️ ${sources[index]} discovery failed:`, result.reason.message);
            }
        });
        
        // Group sensors by equipment type for better dashboard organization
        this.groupSensorsByEquipment();
        
        console.log(`📊 Total sensors discovered: ${this.discoveredSensors.size}`);
        console.log(`🏭 Equipment groups: ${this.equipmentGroups.size}`);
        
        return {
            sensors: Array.from(this.discoveredSensors.values()),
            equipment: Array.from(this.equipmentGroups.values())
        };
    }

    /**
     * Discover Phidget sensors connected to VINT hubs
     */
    async discoverPhidgetSensors() {
        const sensors = [];
        
        try {
            // Simulate Phidget discovery - in real implementation, use Phidget22 library
            const phidgetTypes = [
                { type: 'HUM1001', name: 'Humidity/Temperature Sensor', ports: [0, 1, 2] },
                { type: 'PRE1000', name: 'Pressure Sensor', ports: [3] },
                { type: 'TMP1200', name: 'Thermocouple', ports: [4, 5] }
            ];
            
            phidgetTypes.forEach(device => {
                device.ports.forEach(port => {
                    const baseId = `phidget_hub0_port${port}`;
                    
                    if (device.type === 'HUM1001') {
                        sensors.push(this.createSensorDefinition({
                            id: `${baseId}_humidity`,
                            name: `Hub 0 Port ${port} Humidity`,
                            type: 'humidity',
                            unit: '%RH',
                            min: 0,
                            max: 100,
                            source: 'phidget',
                            location: `VINT Hub 0 Port ${port}`,
                            equipment: 'Environmental Monitoring',
                            category: 'environment'
                        }));
                        
                        sensors.push(this.createSensorDefinition({
                            id: `${baseId}_temperature`,
                            name: `Hub 0 Port ${port} Temperature`,
                            type: 'temperature',
                            unit: '°C',
                            min: -40,
                            max: 85,
                            source: 'phidget',
                            location: `VINT Hub 0 Port ${port}`,
                            equipment: 'Environmental Monitoring',
                            category: 'environment'
                        }));
                    } else if (device.type === 'PRE1000') {
                        sensors.push(this.createSensorDefinition({
                            id: `${baseId}_pressure`,
                            name: `Hub 0 Port ${port} Pressure`,
                            type: 'pressure',
                            unit: 'kPa',
                            min: 0,
                            max: 700,
                            source: 'phidget',
                            location: `VINT Hub 0 Port ${port}`,
                            equipment: 'Pressure Systems',
                            category: 'process'
                        }));
                    } else if (device.type === 'TMP1200') {
                        sensors.push(this.createSensorDefinition({
                            id: `${baseId}_thermocouple`,
                            name: `Hub 0 Port ${port} Thermocouple`,
                            type: 'temperature',
                            unit: '°C',
                            min: -200,
                            max: 1200,
                            source: 'phidget',
                            location: `VINT Hub 0 Port ${port}`,
                            equipment: 'Temperature Monitoring',
                            category: 'process'
                        }));
                    }
                });
            });
            
        } catch (error) {
            console.error('Phidget discovery error:', error);
        }
        
        sensors.forEach(sensor => this.discoveredSensors.set(sensor.id, sensor));
        return sensors;
    }

    /**
     * Discover OPC-UA tags from Ignition or other OPC-UA servers
     */
    async discoverOPCUATags() {
        const tags = [];
        
        try {
            // Simulate OPC-UA tag discovery - typical industrial equipment
            const equipmentTypes = [
                {
                    name: 'Conveyor_01',
                    tags: [
                        { name: 'Speed', type: 'speed', unit: 'm/min', min: 0, max: 100 },
                        { name: 'Motor_Current', type: 'current', unit: 'A', min: 0, max: 50 },
                        { name: 'Running', type: 'status', unit: 'bool' }
                    ]
                },
                {
                    name: 'Tank_A01',
                    tags: [
                        { name: 'Level', type: 'level', unit: '%', min: 0, max: 100 },
                        { name: 'Temperature', type: 'temperature', unit: '°C', min: 0, max: 100 },
                        { name: 'Pressure', type: 'pressure', unit: 'bar', min: 0, max: 10 }
                    ]
                },
                {
                    name: 'Pump_P01',
                    tags: [
                        { name: 'Flow_Rate', type: 'flow', unit: 'L/min', min: 0, max: 1000 },
                        { name: 'Discharge_Pressure', type: 'pressure', unit: 'bar', min: 0, max: 20 },
                        { name: 'Running_Hours', type: 'hours', unit: 'h', min: 0, max: 99999 }
                    ]
                }
            ];
            
            equipmentTypes.forEach(equipment => {
                equipment.tags.forEach(tag => {
                    const tagId = `opcua_${equipment.name}_${tag.name}`;
                    tags.push(this.createSensorDefinition({
                        id: tagId,
                        name: `${equipment.name} ${tag.name}`,
                        type: tag.type,
                        unit: tag.unit,
                        min: tag.min,
                        max: tag.max,
                        source: 'opcua',
                        location: `OPC-UA Server`,
                        equipment: equipment.name,
                        category: 'process',
                        opcPath: `ns=2;s=${equipment.name}.${tag.name}`
                    }));
                });
            });
            
        } catch (error) {
            console.error('OPC-UA discovery error:', error);
        }
        
        tags.forEach(tag => this.discoveredSensors.set(tag.id, tag));
        return tags;
    }

    /**
     * Discover MQTT topics by scanning the broker
     */
    async discoverMQTTTopics() {
        const topics = [];
        
        try {
            // Simulate MQTT topic discovery
            const topicPatterns = [
                'parachute/drop/altitude',
                'parachute/drop/velocity',
                'parachute/drop/gps_lat',
                'parachute/drop/gps_lon',
                'parachute/drop/accelerometer_x',
                'parachute/drop/accelerometer_y',
                'parachute/drop/accelerometer_z',
                'parachute/drop/battery_voltage',
                'parachute/drop/signal_strength',
                'parachute/drop/deployment_status'
            ];
            
            topicPatterns.forEach(topic => {
                const parts = topic.split('/');
                const measurement = parts[parts.length - 1];
                
                let type, unit, min, max;
                switch (measurement) {
                    case 'altitude':
                        type = 'altitude'; unit = 'm'; min = 0; max = 10000;
                        break;
                    case 'velocity':
                        type = 'velocity'; unit = 'm/s'; min = 0; max = 100;
                        break;
                    case 'gps_lat':
                        type = 'latitude'; unit = '°'; min = -90; max = 90;
                        break;
                    case 'gps_lon':
                        type = 'longitude'; unit = '°'; min = -180; max = 180;
                        break;
                    case 'accelerometer_x':
                    case 'accelerometer_y':
                    case 'accelerometer_z':
                        type = 'acceleration'; unit = 'g'; min = -10; max = 10;
                        break;
                    case 'battery_voltage':
                        type = 'voltage'; unit = 'V'; min = 0; max = 12;
                        break;
                    case 'signal_strength':
                        type = 'signal'; unit = 'dBm'; min = -120; max = 0;
                        break;
                    case 'deployment_status':
                        type = 'status'; unit = 'bool';
                        break;
                    default:
                        type = 'value'; unit = ''; min = 0; max = 100;
                }
                
                topics.push(this.createSensorDefinition({
                    id: `mqtt_${measurement}`,
                    name: `Parachute ${measurement.replace('_', ' ').toUpperCase()}`,
                    type: type,
                    unit: unit,
                    min: min,
                    max: max,
                    source: 'mqtt',
                    location: 'Drop Zone',
                    equipment: 'Parachute Drop System',
                    category: 'telemetry',
                    mqttTopic: topic
                }));
            });
            
        } catch (error) {
            console.error('MQTT discovery error:', error);
        }
        
        topics.forEach(topic => this.discoveredSensors.set(topic.id, topic));
        return topics;
    }

    /**
     * Discover Modbus devices
     */
    async discoverModbusDevices() {
        const devices = [];
        
        try {
            // Simulate Modbus device discovery
            const modbusDevices = [
                {
                    address: 1,
                    name: 'Power_Meter_01',
                    registers: [
                        { address: 0, name: 'Voltage_L1', type: 'voltage', unit: 'V' },
                        { address: 2, name: 'Current_L1', type: 'current', unit: 'A' },
                        { address: 4, name: 'Power_Total', type: 'power', unit: 'kW' },
                        { address: 6, name: 'Energy_Total', type: 'energy', unit: 'kWh' }
                    ]
                },
                {
                    address: 2,
                    name: 'Weather_Station',
                    registers: [
                        { address: 0, name: 'Wind_Speed', type: 'wind_speed', unit: 'm/s' },
                        { address: 1, name: 'Wind_Direction', type: 'wind_direction', unit: '°' },
                        { address: 2, name: 'Ambient_Temperature', type: 'temperature', unit: '°C' },
                        { address: 3, name: 'Humidity', type: 'humidity', unit: '%RH' },
                        { address: 4, name: 'Barometric_Pressure', type: 'pressure', unit: 'mbar' }
                    ]
                }
            ];
            
            modbusDevices.forEach(device => {
                device.registers.forEach(register => {
                    const deviceId = `modbus_${device.address}_${register.address}`;
                    devices.push(this.createSensorDefinition({
                        id: deviceId,
                        name: `${device.name} ${register.name}`,
                        type: register.type,
                        unit: register.unit,
                        min: 0,
                        max: this.getDefaultMaxForType(register.type),
                        source: 'modbus',
                        location: `Modbus Device ${device.address}`,
                        equipment: device.name,
                        category: 'electrical',
                        modbusAddress: device.address,
                        modbusRegister: register.address
                    }));
                });
            });
            
        } catch (error) {
            console.error('Modbus discovery error:', error);
        }
        
        devices.forEach(device => this.discoveredSensors.set(device.id, device));
        return devices;
    }

    /**
     * Create standardized sensor definition
     */
    createSensorDefinition(config) {
        return {
            id: config.id,
            name: config.name,
            type: config.type,
            unit: config.unit || '',
            min: config.min !== undefined ? config.min : 0,
            max: config.max !== undefined ? config.max : 100,
            source: config.source,
            location: config.location,
            equipment: config.equipment,
            category: config.category || 'general',
            
            // Source-specific properties
            ...(config.opcPath && { opcPath: config.opcPath }),
            ...(config.mqttTopic && { mqttTopic: config.mqttTopic }),
            ...(config.modbusAddress && { modbusAddress: config.modbusAddress }),
            ...(config.modbusRegister && { modbusRegister: config.modbusRegister }),
            
            // Display properties
            displayOrder: this.getDisplayOrderForType(config.type),
            color: this.getColorForType(config.type),
            icon: this.getIconForType(config.type),
            
            // Alert thresholds
            thresholds: this.getDefaultThresholds(config.type, config.min, config.max)
        };
    }

    /**
     * Group sensors by equipment for dashboard organization
     */
    groupSensorsByEquipment() {
        const groups = new Map();
        
        this.discoveredSensors.forEach(sensor => {
            const equipmentName = sensor.equipment;
            
            if (!groups.has(equipmentName)) {
                groups.set(equipmentName, {
                    name: equipmentName,
                    category: sensor.category,
                    sensors: [],
                    location: sensor.location,
                    hasAlarms: false,
                    hasStatus: false
                });
            }
            
            const group = groups.get(equipmentName);
            group.sensors.push(sensor);
            
            // Check for alarm-capable sensors
            if (sensor.thresholds && (sensor.thresholds.warning || sensor.thresholds.critical)) {
                group.hasAlarms = true;
            }
            
            // Check for status sensors
            if (sensor.type === 'status' || sensor.unit === 'bool') {
                group.hasStatus = true;
            }
        });
        
        this.equipmentGroups = groups;
    }

    /**
     * Generate complete dashboard flows
     */
    async generateDashboard() {
        console.log('🎯 Generating dashboard flows...');
        
        // Generate main dashboard layout
        const layoutFlow = this.generateLayoutFlow();
        
        // Generate equipment-specific flows
        const equipmentFlows = Array.from(this.equipmentGroups.values()).map(equipment => 
            this.generateEquipmentFlow(equipment)
        );
        
        // Generate overview flow
        const overviewFlow = this.generateOverviewFlow();
        
        // Generate alarm management flow
        const alarmFlow = this.generateAlarmFlow();
        
        // Combine all flows
        this.generatedFlows = [
            layoutFlow,
            overviewFlow,
            alarmFlow,
            ...equipmentFlows
        ].flat();
        
        console.log(`✅ Generated ${this.generatedFlows.length} dashboard nodes`);
        return this.generatedFlows;
    }

    /**
     * Generate main dashboard layout
     */
    generateLayoutFlow() {
        const layoutNodes = [];
        
        // Dashboard configuration node
        layoutNodes.push({
            id: "dashboard_config",
            type: "ui_base",
            theme: {
                name: "theme-dark",
                lightTheme: {
                    default: "#0094CE",
                    baseColor: "#0094CE",
                    baseFont: "-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,Oxygen-Sans,Ubuntu,Cantarell,Helvetica Neue,sans-serif"
                },
                darkTheme: {
                    default: "#097479",
                    baseColor: "#097479",
                    baseFont: "-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,Oxygen-Sans,Ubuntu,Cantarell,Helvetica Neue,sans-serif"
                },
                customTheme: {
                    name: "Industrial",
                    default: "#4B7C59",
                    baseColor: "#4B7C59",
                    baseFont: "-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,Oxygen-Sans,Ubuntu,Cantarell,Helvetica Neue,sans-serif"
                }
            },
            site: {
                name: this.options.siteName,
                hideToolbar: "false",
                allowSwipe: "false",
                lockMenu: "false",
                allowTempTheme: "true",
                dateFormat: "DD/MM/YYYY",
                sizes: {
                    sx: 48,
                    sy: 48,
                    gx: 6,
                    gy: 6,
                    cx: 6,
                    cy: 6
                }
            }
        });
        
        return layoutNodes;
    }

    /**
     * Generate overview dashboard flow
     */
    generateOverviewFlow() {
        const overviewNodes = [];
        let yPos = 60;
        
        // Overview tab
        overviewNodes.push({
            id: "overview_tab",
            type: "ui_tab",
            name: "Overview",
            icon: "dashboard",
            order: 1,
            disabled: false,
            hidden: false
        });
        
        // Overview group
        overviewNodes.push({
            id: "overview_group",
            type: "ui_group",
            name: "System Overview",
            tab: "overview_tab",
            order: 1,
            disp: true,
            width: "24",
            collapse: false
        });
        
        // System status summary
        overviewNodes.push({
            id: "system_status_summary",
            type: "ui_template",
            group: "overview_group",
            name: "System Status",
            order: 1,
            width: "24",
            height: "4",
            format: this.generateSystemStatusTemplate(),
            storeOutMessages: true,
            fwdInMessages: true,
            resendOnRefresh: true,
            templateScope: "local",
            x: 200,
            y: yPos,
            wires: [[]]
        });
        
        yPos += 80;
        
        // Key metrics cards
        const keyMetrics = [
            { name: "Active Equipment", icon: "fa-cogs", color: "#4CAF50" },
            { name: "Active Alarms", icon: "fa-exclamation-triangle", color: "#FF9800" },
            { name: "Data Points", icon: "fa-database", color: "#2196F3" },
            { name: "System Uptime", icon: "fa-clock-o", color: "#9C27B0" }
        ];
        
        keyMetrics.forEach((metric, index) => {
            overviewNodes.push({
                id: `metric_${metric.name.toLowerCase().replace(' ', '_')}`,
                type: "ui_gauge",
                group: "overview_group",
                name: metric.name,
                order: index + 2,
                width: "6",
                height: "4",
                gtype: "gage",
                title: metric.name,
                label: "units",
                format: "{{value}}",
                min: 0,
                max: 100,
                colors: ["#00b500", "#e6e600", "#ca3838"],
                seg1: "70",
                seg2: "90",
                className: "",
                x: 200 + (index * 120),
                y: yPos,
                wires: []
            });
        });
        
        return overviewNodes;
    }

    /**
     * Generate equipment-specific dashboard flow
     */
    generateEquipmentFlow(equipment) {
        const equipmentNodes = [];
        const tabId = `tab_${equipment.name.toLowerCase().replace(/[^a-z0-9]/g, '_')}`;
        const groupId = `group_${equipment.name.toLowerCase().replace(/[^a-z0-9]/g, '_')}`;
        
        // Equipment tab
        equipmentNodes.push({
            id: tabId,
            type: "ui_tab",
            name: equipment.name,
            icon: this.getEquipmentIcon(equipment.category),
            order: this.getTabOrder(equipment.category),
            disabled: false,
            hidden: false
        });
        
        // Equipment main group
        equipmentNodes.push({
            id: groupId,
            type: "ui_group",
            name: `${equipment.name} Monitoring`,
            tab: tabId,
            order: 1,
            disp: true,
            width: "24",
            collapse: false
        });
        
        // Generate widgets for each sensor
        equipment.sensors.forEach((sensor, index) => {
            const sensorNodes = this.generateSensorWidgets(sensor, groupId, index + 1);
            equipmentNodes.push(...sensorNodes);
        });
        
        // Add equipment summary if multiple sensors
        if (equipment.sensors.length > 1) {
            equipmentNodes.push({
                id: `${groupId}_summary`,
                type: "ui_template",
                group: groupId,
                name: `${equipment.name} Summary`,
                order: 999,
                width: "24",
                height: "6",
                format: this.generateEquipmentSummaryTemplate(equipment),
                storeOutMessages: true,
                fwdInMessages: true,
                resendOnRefresh: true,
                templateScope: "local",
                x: 400,
                y: 300,
                wires: [[]]
            });
        }
        
        return equipmentNodes;
    }

    /**
     * Generate sensor widgets
     */
    generateSensorWidgets(sensor, groupId, order) {
        const widgets = [];
        
        // Choose appropriate widget type based on sensor type
        let widgetType, widgetConfig;
        
        switch (sensor.type) {
            case 'status':
                widgetType = 'ui_led';
                widgetConfig = {
                    label: "",
                    labelPlacement: "left",
                    labelAlignment: "left",
                    colorForValue: [
                        { color: "#ff0000", value: "false", valueType: "str" },
                        { color: "#008000", value: "true", valueType: "str" }
                    ],
                    allowColorForValueInMessage: false
                };
                break;
                
            case 'temperature':
            case 'pressure':
            case 'level':
                widgetType = 'ui_gauge';
                widgetConfig = {
                    gtype: "gage",
                    title: sensor.name,
                    label: sensor.unit,
                    format: "{{value}}",
                    min: sensor.min,
                    max: sensor.max,
                    colors: ["#00b500", "#e6e600", "#ca3838"],
                    seg1: Math.round(sensor.max * 0.7),
                    seg2: Math.round(sensor.max * 0.9)
                };
                break;
                
            case 'flow':
            case 'speed':
            case 'current':
                widgetType = 'ui_chart';
                widgetConfig = {
                    group: groupId,
                    order: order,
                    width: 12,
                    height: 6,
                    label: sensor.name,
                    chartType: "line",
                    legend: "false",
                    xformat: "HH:mm:ss",
                    interpolate: "linear",
                    nodata: "",
                    dot: false,
                    ymin: sensor.min,
                    ymax: sensor.max,
                    removeOlder: 1,
                    removeOlderPoints: "",
                    removeOlderUnit: "3600",
                    cutout: 0,
                    useOneColor: false,
                    useUTC: false,
                    colors: ["#1f77b4", "#aec7e8", "#ff7f0e", "#2ca02c", "#98df8a", "#d62728", "#ff9896", "#9467bd", "#c5b0d5"]
                };
                break;
                
            default:
                widgetType = 'ui_text';
                widgetConfig = {
                    label: sensor.name,
                    format: `{{msg.payload}} ${sensor.unit}`,
                    layout: "row-spread"
                };
                break;
        }
        
        // Create the widget node
        widgets.push({
            id: `widget_${sensor.id}`,
            type: widgetType,
            group: groupId,
            name: sensor.name,
            order: order,
            width: widgetType === 'ui_chart' ? 12 : 6,
            height: widgetType === 'ui_chart' ? 6 : 3,
            ...widgetConfig,
            x: 200 + ((order - 1) % 4) * 150,
            y: 100 + Math.floor((order - 1) / 4) * 100,
            wires: []
        });
        
        // Add data input node for the sensor
        widgets.push({
            id: `input_${sensor.id}`,
            type: this.getSensorInputNodeType(sensor),
            name: `${sensor.name} Input`,
            ...this.getSensorInputConfig(sensor),
            x: 50,
            y: 100 + Math.floor((order - 1) / 4) * 100,
            wires: [[`widget_${sensor.id}`]]
        });
        
        return widgets;
    }

    /**
     * Generate alarm management flow
     */
    generateAlarmFlow() {
        const alarmNodes = [];
        
        // Alarms tab
        alarmNodes.push({
            id: "alarms_tab",
            type: "ui_tab",
            name: "Alarms",
            icon: "warning",
            order: 999,
            disabled: false,
            hidden: false
        });
        
        // Active alarms group
        alarmNodes.push({
            id: "active_alarms_group",
            type: "ui_group",
            name: "Active Alarms",
            tab: "alarms_tab",
            order: 1,
            disp: true,
            width: "24",
            collapse: false
        });
        
        // Alarm table
        alarmNodes.push({
            id: "alarm_table",
            type: "ui_table",
            group: "active_alarms_group",
            name: "Active Alarms",
            order: 1,
            width: "24",
            height: "10",
            columns: [
                { field: "timestamp", title: "Time", width: "150", align: "left" },
                { field: "equipment", title: "Equipment", width: "200", align: "left" },
                { field: "sensor", title: "Sensor", width: "200", align: "left" },
                { field: "severity", title: "Severity", width: "100", align: "center" },
                { field: "value", title: "Value", width: "100", align: "right" },
                { field: "message", title: "Message", width: "", align: "left" }
            ],
            outputs: 1,
            cts: false,
            x: 400,
            y: 200,
            wires: [[]]
        });
        
        // Alarm statistics
        alarmNodes.push({
            id: "alarm_stats",
            type: "ui_template",
            group: "active_alarms_group",
            name: "Alarm Statistics",
            order: 2,
            width: "24",
            height: "4",
            format: this.generateAlarmStatsTemplate(),
            storeOutMessages: true,
            fwdInMessages: true,
            resendOnRefresh: true,
            templateScope: "local",
            x: 400,
            y: 300,
            wires: [[]]
        });
        
        return alarmNodes;
    }

    /**
     * Helper methods for sensor configuration
     */
    getSensorInputNodeType(sensor) {
        switch (sensor.source) {
            case 'phidget': return 'phidget-humidity-sensor';
            case 'opcua': return 'OpcUa-Client';
            case 'mqtt': return 'mqtt in';
            case 'modbus': return 'modbus-read';
            default: return 'inject';
        }
    }

    getSensorInputConfig(sensor) {
        switch (sensor.source) {
            case 'phidget':
                return {
                    sensorName: sensor.name,
                    hubPort: "0",
                    updateRate: "1000"
                };
            case 'opcua':
                return {
                    endpoint: "opc.tcp://localhost:62541",
                    action: "subscribe",
                    deadbandtype: "a",
                    deadbandvalue: 1,
                    time: 10,
                    timeUnit: "s"
                };
            case 'mqtt':
                return {
                    topic: sensor.mqttTopic,
                    qos: "1",
                    datatype: "auto",
                    broker: "mqtt_broker"
                };
            case 'modbus':
                return {
                    name: sensor.name,
                    showStatusActivities: false,
                    showErrors: false,
                    unitid: sensor.modbusAddress,
                    dataType: "HoldingRegister",
                    adr: sensor.modbusRegister,
                    quantity: "1"
                };
            default:
                return {
                    repeat: "5",
                    crontab: "",
                    once: false,
                    onceDelay: 0.1,
                    topic: sensor.id,
                    payload: Math.floor(Math.random() * (sensor.max - sensor.min)) + sensor.min
                };
        }
    }

    /**
     * Template generation methods
     */
    generateSystemStatusTemplate() {
        return `
<div style="padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px; color: white;">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
        <h2 style="margin: 0; font-size: 24px;"><i class="fa fa-dashboard"></i> System Overview</h2>
        <div style="font-size: 14px; opacity: 0.9;">
            Last Updated: {{msg.timestamp || new Date().toLocaleString()}}
        </div>
    </div>
    
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px;">
        <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 8px; text-align: center;">
            <div style="font-size: 32px; font-weight: bold; color: #4CAF50;">{{msg.payload.equipmentOnline || 0}}</div>
            <div style="opacity: 0.9;">Equipment Online</div>
        </div>
        
        <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 8px; text-align: center;">
            <div style="font-size: 32px; font-weight: bold; color: #FF9800;">{{msg.payload.activeAlarms || 0}}</div>
            <div style="opacity: 0.9;">Active Alarms</div>
        </div>
        
        <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 8px; text-align: center;">
            <div style="font-size: 32px; font-weight: bold; color: #2196F3;">{{msg.payload.dataPoints || 0}}</div>
            <div style="opacity: 0.9;">Data Points/Min</div>
        </div>
        
        <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 8px; text-align: center;">
            <div style="font-size: 32px; font-weight: bold; color: #9C27B0;">{{msg.payload.uptime || '0h'}}</div>
            <div style="opacity: 0.9;">System Uptime</div>
        </div>
    </div>
</div>
        `;
    }

    generateEquipmentSummaryTemplate(equipment) {
        return `
<div style="padding: 15px; background: #f5f5f5; border-radius: 8px; border-left: 4px solid #2196F3;">
    <h3 style="margin: 0 0 15px 0; color: #333;"><i class="fa ${this.getEquipmentIcon(equipment.category)}"></i> ${equipment.name} Summary</h3>
    
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 10px;">
        ${equipment.sensors.map(sensor => `
        <div style="background: white; padding: 10px; border-radius: 4px; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
            <div style="font-size: 18px; font-weight: bold; color: ${sensor.color};">{{msg.${sensor.id} || '--'}}</div>
            <div style="font-size: 12px; color: #666;">${sensor.name}</div>
            <div style="font-size: 11px; color: #999;">${sensor.unit}</div>
        </div>
        `).join('')}
    </div>
    
    <div style="margin-top: 15px; padding: 10px; background: #e8f5e8; border-radius: 4px; font-size: 12px; color: #2e7d32;">
        <i class="fa fa-info-circle"></i> Location: ${equipment.location} | Sensors: ${equipment.sensors.length} | Status: Online
    </div>
</div>
        `;
    }

    generateAlarmStatsTemplate() {
        return `
<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: 10px; padding: 10px;">
    <div style="text-align: center; padding: 10px; background: #ffebee; border-radius: 4px;">
        <div style="font-size: 24px; font-weight: bold; color: #d32f2f;">{{msg.payload.critical || 0}}</div>
        <div style="font-size: 12px; color: #666;">Critical</div>
    </div>
    
    <div style="text-align: center; padding: 10px; background: #fff3e0; border-radius: 4px;">
        <div style="font-size: 24px; font-weight: bold; color: #f57c00;">{{msg.payload.warning || 0}}</div>
        <div style="font-size: 12px; color: #666;">Warning</div>
    </div>
    
    <div style="text-align: center; padding: 10px; background: #e3f2fd; border-radius: 4px;">
        <div style="font-size: 24px; font-weight: bold; color: #1976d2;">{{msg.payload.info || 0}}</div>
        <div style="font-size: 12px; color: #666;">Info</div>
    </div>
    
    <div style="text-align: center; padding: 10px; background: #e8f5e8; border-radius: 4px;">
        <div style="font-size: 24px; font-weight: bold; color: #388e3c;">{{msg.payload.acknowledged || 0}}</div>
        <div style="font-size: 12px; color: #666;">Acknowledged</div>
    </div>
</div>
        `;
    }

    /**
     * Utility methods
     */
    getDefaultMaxForType(type) {
        const maxValues = {
            temperature: 100,
            humidity: 100,
            pressure: 1000,
            voltage: 500,
            current: 100,
            power: 10000,
            energy: 999999,
            flow: 1000,
            level: 100,
            speed: 100,
            wind_speed: 50,
            wind_direction: 360
        };
        return maxValues[type] || 100;
    }

    getDisplayOrderForType(type) {
        const order = {
            status: 1,
            temperature: 2,
            pressure: 3,
            level: 4,
            flow: 5,
            speed: 6,
            current: 7,
            voltage: 8,
            power: 9,
            energy: 10
        };
        return order[type] || 99;
    }

    getColorForType(type) {
        const colors = {
            temperature: "#FF6B6B",
            humidity: "#4ECDC4",
            pressure: "#45B7D1",
            level: "#96CEB4",
            flow: "#FFEAA7",
            speed: "#DDA0DD",
            current: "#F39C12",
            voltage: "#E74C3C",
            power: "#9B59B6",
            energy: "#1ABC9C",
            status: "#95A5A6"
        };
        return colors[type] || "#95A5A6";
    }

    getIconForType(type) {
        const icons = {
            temperature: "fa-thermometer-half",
            humidity: "fa-tint",
            pressure: "fa-gauge",
            level: "fa-signal",
            flow: "fa-exchange",
            speed: "fa-tachometer",
            current: "fa-bolt",
            voltage: "fa-flash",
            power: "fa-plug",
            energy: "fa-battery-full",
            status: "fa-circle"
        };
        return icons[type] || "fa-circle-o";
    }

    getEquipmentIcon(category) {
        const icons = {
            environment: "fa-tree",
            process: "fa-cogs",
            electrical: "fa-bolt",
            telemetry: "fa-satellite",
            general: "fa-cube"
        };
        return icons[category] || "fa-cube";
    }

    getTabOrder(category) {
        const order = {
            telemetry: 2,
            process: 3,
            environment: 4,
            electrical: 5,
            general: 6
        };
        return order[category] || 10;
    }

    getDefaultThresholds(type, min, max) {
        const range = max - min;
        return {
            warning: {
                low: min + (range * 0.1),
                high: min + (range * 0.9)
            },
            critical: {
                low: min,
                high: max
            }
        };
    }

    /**
     * Export dashboard to file
     */
    async exportDashboard(outputPath) {
        if (!this.generatedFlows.length) {
            throw new Error('No dashboard flows generated. Call generateDashboard() first.');
        }
        
        const dashboardData = {
            flows: this.generatedFlows,
            sensors: Array.from(this.discoveredSensors.values()),
            equipment: Array.from(this.equipmentGroups.values()),
            metadata: {
                generated: new Date().toISOString(),
                version: "1.0.0",
                generator: "CT-084 Dashboard Generator",
                siteName: this.options.siteName,
                sensorCount: this.discoveredSensors.size,
                equipmentCount: this.equipmentGroups.size
            }
        };
        
        await fs.writeFile(outputPath, JSON.stringify(dashboardData, null, 2));
        console.log(`📁 Dashboard exported to: ${outputPath}`);
        
        return dashboardData;
    }

    /**
     * Generate production deployment package
     */
    async generateDeploymentPackage() {
        console.log('📦 Creating production deployment package...');
        
        const deploymentConfig = {
            version: "1.0.0",
            name: "CT-084 Parachute Drop Dashboard",
            description: "Industrial IoT dashboard for parachute drop system monitoring",
            
            // Node-RED configuration
            nodeRed: {
                flows: this.generatedFlows,
                settings: this.generateProductionSettings(),
                customNodes: await this.getCustomNodesList()
            },
            
            // Infrastructure requirements
            infrastructure: {
                hardware: {
                    cpu: "ARM64 (Raspberry Pi 4 recommended)",
                    memory: "4GB RAM minimum",
                    storage: "32GB SD card (industrial grade)",
                    network: "Ethernet + WiFi capabilities"
                },
                software: {
                    os: "Raspberry Pi OS Lite",
                    nodeJs: "16.x or higher",
                    nodeRed: "3.x or higher",
                    python: "3.9+ (for Phidget integration)"
                }
            },
            
            // Security configuration
            security: {
                authentication: this.options.enableSecurity,
                encryption: true,
                certificates: this.options.enableSecurity,
                firewall: {
                    inbound: [1880, 22, 1883, 502],
                    outbound: ["all"]
                }
            },
            
            // Monitoring and maintenance
            monitoring: {
                healthChecks: true,
                logRotation: true,
                backupSchedule: "daily",
                updateSchedule: "weekly"
            },
            
            // Deployment scripts
            deployment: {
                install: "./scripts/install.sh",
                configure: "./scripts/configure.sh",
                start: "./scripts/start.sh",
                monitor: "./scripts/monitor.sh"
            }
        };
        
        return deploymentConfig;
    }

    generateProductionSettings() {
        return {
            uiPort: process.env.PORT || 1880,
            uiHost: "0.0.0.0",
            
            httpAdminRoot: this.options.enableSecurity ? '/admin' : false,
            httpNodeRoot: '/api',
            
            adminAuth: this.options.enableSecurity ? {
                type: "credentials",
                users: [{
                    username: "admin",
                    password: "$2b$08$BHbVOp3DaIhO8QQQZ8E6aOUxn8QjB.v5Ml5pTa4dNjG5r5tGJQFpu",
                    permissions: "*"
                }]
            } : false,
            
            functionGlobalContext: {
                site: {
                    name: this.options.siteName,
                    location: "Industrial Site",
                    timezone: process.env.TZ || "UTC"
                },
                monitoring: {
                    enabled: true,
                    interval: 60000,
                    retention: 86400000
                }
            },
            
            logging: {
                console: {
                    level: "info",
                    metrics: false,
                    audit: true
                },
                file: {
                    level: "info",
                    filename: "/var/log/node-red/node-red.log",
                    maxFiles: 10,
                    maxSize: "10MB"
                }
            }
        };
    }

    async getCustomNodesList() {
        return [
            "node-red-dashboard",
            "node-red-contrib-opcua",
            "node-red-contrib-modbus",
            "node-red-contrib-phidget22",
            "node-red-contrib-mqtt-broker",
            "node-red-contrib-influxdb",
            "node-red-contrib-buffer-parser",
            "node-red-contrib-cron-plus"
        ];
    }
}

module.exports = DashboardGenerator;