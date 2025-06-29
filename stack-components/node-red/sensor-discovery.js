/**
 * Sensor Discovery System for CT-084 Parachute Drop System
 * Auto-discovers and configures sensors from multiple sources including Phidget, OPC-UA, MQTT, and Modbus
 * Author: Agent 3 - Dashboard Generator and Production Deployment
 */

const EventEmitter = require('events');
const fs = require('fs').promises;
const path = require('path');

class SensorDiscoverySystem extends EventEmitter {
    constructor(options = {}) {
        super();
        
        this.options = {
            discoveryInterval: options.discoveryInterval || 60000, // 1 minute
            enablePhidget: options.enablePhidget !== false,
            enableOPCUA: options.enableOPCUA !== false,
            enableMQTT: options.enableMQTT !== false,
            enableModbus: options.enableModbus !== false,
            configPath: options.configPath || './config/sensors.json',
            ...options
        };
        
        this.discoveredSensors = new Map();
        this.sensorConfig = new Map();
        this.discoveryRunning = false;
        this.discoveryTimer = null;
        
        // Protocol-specific configurations
        this.protocolConfigs = {
            phidget: {
                hubSearchTimeout: 5000,
                sensorTimeout: 3000,
                maxRetries: 3
            },
            opcua: {
                connectionTimeout: 10000,
                browseTimeout: 5000,
                endpoints: [
                    'opc.tcp://localhost:62541',
                    'opc.tcp://ignition:62541'
                ]
            },
            mqtt: {
                brokers: [
                    'mqtt://localhost:1883',
                    'mqtt://emqx:1883'
                ],
                discoveryTopics: [
                    'parachute/+',
                    'sensors/+/+',
                    'equipment/+/+',
                    'industrial/+/+'
                ]
            },
            modbus: {
                deviceScanRange: { start: 1, end: 10 },
                timeout: 2000,
                baudRate: 9600,
                dataBits: 8,
                stopBits: 1,
                parity: 'none'
            }
        };
    }

    /**
     * Start the discovery system
     */
    async start() {
        console.log('🔍 Starting Sensor Discovery System...');
        
        try {
            // Load existing sensor configuration
            await this.loadSensorConfig();
            
            // Perform initial discovery
            await this.performDiscovery();
            
            // Set up periodic discovery
            this.discoveryTimer = setInterval(() => {
                this.performDiscovery().catch(error => {
                    console.error('Discovery error:', error);
                    this.emit('error', error);
                });
            }, this.options.discoveryInterval);
            
            this.discoveryRunning = true;
            this.emit('started');
            
            console.log('✅ Sensor Discovery System started successfully');
            
        } catch (error) {
            console.error('❌ Failed to start discovery system:', error);
            this.emit('error', error);
            throw error;
        }
    }

    /**
     * Stop the discovery system
     */
    async stop() {
        console.log('🛑 Stopping Sensor Discovery System...');
        
        if (this.discoveryTimer) {
            clearInterval(this.discoveryTimer);
            this.discoveryTimer = null;
        }
        
        this.discoveryRunning = false;
        
        // Save current configuration
        await this.saveSensorConfig();
        
        this.emit('stopped');
        console.log('✅ Sensor Discovery System stopped');
    }

    /**
     * Perform comprehensive sensor discovery
     */
    async performDiscovery() {
        console.log('🔍 Performing sensor discovery...');
        
        const startTime = Date.now();
        const discoveryResults = [];
        
        // Parallel discovery from all enabled sources
        const discoveryPromises = [];
        
        if (this.options.enablePhidget) {
            discoveryPromises.push(this.discoverPhidgetSensors());
        }
        
        if (this.options.enableOPCUA) {
            discoveryPromises.push(this.discoverOPCUATags());
        }
        
        if (this.options.enableMQTT) {
            discoveryPromises.push(this.discoverMQTTTopics());
        }
        
        if (this.options.enableModbus) {
            discoveryPromises.push(this.discoverModbusDevices());
        }
        
        // Execute all discoveries
        const results = await Promise.allSettled(discoveryPromises);
        
        // Process results
        results.forEach((result, index) => {
            const sources = ['Phidget', 'OPC-UA', 'MQTT', 'Modbus'];
            if (result.status === 'fulfilled') {
                discoveryResults.push(...result.value);
                console.log(`✅ ${sources[index]} discovery: ${result.value.length} sensors found`);
            } else {
                console.log(`⚠️ ${sources[index]} discovery failed: ${result.reason.message}`);
            }
        });
        
        // Update sensor registry
        await this.updateSensorRegistry(discoveryResults);
        
        const duration = Date.now() - startTime;
        console.log(`🔍 Discovery completed in ${duration}ms - Total sensors: ${this.discoveredSensors.size}`);
        
        // Emit discovery event
        this.emit('discovery_complete', {
            duration,
            sensorsFound: discoveryResults.length,
            totalSensors: this.discoveredSensors.size,
            sensors: Array.from(this.discoveredSensors.values())
        });
        
        return discoveryResults;
    }

    /**
     * Discover Phidget sensors
     */
    async discoverPhidgetSensors() {
        const sensors = [];
        
        try {
            // Try to import Phidget22 library
            let phidget22;
            try {
                phidget22 = require('phidget22');
            } catch (err) {
                console.log('📦 Phidget22 library not available, using simulation mode');
                return this.simulatePhidgetDiscovery();
            }
            
            const { Hub, HumiditySensor, TemperatureSensor, PressureSensor } = phidget22;
            
            // Discover VINT Hubs
            const hub = new Hub();
            
            try {
                await hub.open(this.protocolConfigs.phidget.hubSearchTimeout);
                
                const hubSerial = hub.getDeviceSerialNumber();
                const portCount = hub.getPortCount();
                
                console.log(`🔌 Found VINT Hub: Serial ${hubSerial}, Ports: ${portCount}`);
                
                // Scan each VINT port for sensors
                for (let port = 0; port < portCount; port++) {
                    try {
                        const portMode = hub.getPortMode(port);
                        
                        if (portMode !== 0) { // Port has a device
                            // Try different sensor types
                            const sensorPromises = [
                                this.detectPhidgetSensorType(HumiditySensor, port, 'humidity'),
                                this.detectPhidgetSensorType(TemperatureSensor, port, 'temperature'),
                                this.detectPhidgetSensorType(PressureSensor, port, 'pressure')
                            ];
                            
                            const sensorResults = await Promise.allSettled(sensorPromises);
                            
                            sensorResults.forEach(result => {
                                if (result.status === 'fulfilled' && result.value) {
                                    sensors.push(result.value);
                                }
                            });
                        }
                    } catch (portError) {
                        console.log(`⚠️ Error scanning VINT port ${port}:`, portError.message);
                    }
                }
                
                await hub.close();
                
            } catch (hubError) {
                console.log('⚠️ No VINT Hub found or connection failed:', hubError.message);
            }
            
        } catch (error) {
            console.error('❌ Phidget discovery error:', error);
        }
        
        return sensors;
    }

    /**
     * Detect specific Phidget sensor type on a port
     */
    async detectPhidgetSensorType(SensorClass, port, sensorType) {
        try {
            const sensor = new SensorClass();
            sensor.setHubPort(port);
            
            await sensor.open(this.protocolConfigs.phidget.sensorTimeout);
            
            const deviceSerial = sensor.getDeviceSerialNumber();
            const deviceName = sensor.getDeviceName();
            
            await sensor.close();
            
            return this.createPhidgetSensorDefinition({
                port,
                sensorType,
                deviceSerial,
                deviceName
            });
            
        } catch (error) {
            // Sensor not present on this port
            return null;
        }
    }

    /**
     * Create Phidget sensor definition
     */
    createPhidgetSensorDefinition({ port, sensorType, deviceSerial, deviceName }) {
        const baseId = `phidget_hub0_port${port}_${sensorType}`;
        
        const sensorDef = {
            id: baseId,
            name: `VINT Port ${port} ${sensorType.charAt(0).toUpperCase() + sensorType.slice(1)}`,
            type: sensorType,
            source: 'phidget',
            protocol: 'VINT',
            location: `VINT Hub Port ${port}`,
            equipment: 'Environmental Monitoring',
            category: 'environment',
            
            // Phidget-specific properties
            hubPort: port,
            deviceSerial,
            deviceName,
            
            // Sensor properties based on type
            ...this.getPhidgetSensorProperties(sensorType),
            
            // Discovery metadata
            discovered: new Date().toISOString(),
            lastSeen: new Date().toISOString(),
            status: 'active'
        };
        
        return sensorDef;
    }

    /**
     * Get sensor properties based on Phidget sensor type
     */
    getPhidgetSensorProperties(sensorType) {
        const properties = {
            humidity: {
                unit: '%RH',
                min: 0,
                max: 100,
                precision: 2,
                thresholds: { warning: { low: 30, high: 70 }, critical: { low: 20, high: 80 } }
            },
            temperature: {
                unit: '°C',
                min: -40,
                max: 85,
                precision: 1,
                thresholds: { warning: { low: 5, high: 35 }, critical: { low: 0, high: 40 } }
            },
            pressure: {
                unit: 'kPa',
                min: 0,
                max: 700,
                precision: 1,
                thresholds: { warning: { low: 50, high: 650 }, critical: { low: 10, high: 690 } }
            }
        };
        
        return properties[sensorType] || {
            unit: '',
            min: 0,
            max: 100,
            precision: 2,
            thresholds: { warning: { low: 10, high: 90 }, critical: { low: 0, high: 100 } }
        };
    }

    /**
     * Simulate Phidget discovery when library is not available
     */
    simulatePhidgetDiscovery() {
        const simulatedSensors = [];
        
        // Simulate typical parachute drop sensors
        const sensorTypes = [
            { port: 0, type: 'humidity', name: 'Environmental Humidity' },
            { port: 0, type: 'temperature', name: 'Environmental Temperature' },
            { port: 1, type: 'pressure', name: 'Barometric Pressure' },
            { port: 2, type: 'temperature', name: 'Equipment Temperature' }
        ];
        
        sensorTypes.forEach(({ port, type, name }) => {
            simulatedSensors.push(this.createPhidgetSensorDefinition({
                port,
                sensorType: type,
                deviceSerial: 123456 + port,
                deviceName: `Simulated ${name} Sensor`
            }));
        });
        
        console.log('🎭 Using simulated Phidget sensors');
        return simulatedSensors;
    }

    /**
     * Discover OPC-UA tags
     */
    async discoverOPCUATags() {
        const tags = [];
        
        try {
            // Try to import OPC-UA library
            let opcua;
            try {
                opcua = require('node-opcua-client');
            } catch (err) {
                console.log('📦 OPC-UA library not available, using simulation mode');
                return this.simulateOPCUADiscovery();
            }
            
            const { OPCUAClient } = opcua;
            
            // Try each configured endpoint
            for (const endpoint of this.protocolConfigs.opcua.endpoints) {
                try {
                    console.log(`🔗 Connecting to OPC-UA server: ${endpoint}`);
                    
                    const client = OPCUAClient.create({
                        connectionStrategy: {
                            maxRetry: 1,
                            initialDelay: 1000,
                            maxDelay: 2000
                        }
                    });
                    
                    await client.connect(endpoint);
                    const session = await client.createSession();
                    
                    // Browse for tags starting from root
                    const browseResult = await session.browse('i=85'); // Objects folder
                    
                    for (const reference of browseResult.references) {
                        if (reference.browseName.name) {
                            const tag = await this.createOPCUATagDefinition(session, reference, endpoint);
                            if (tag) {
                                tags.push(tag);
                            }
                        }
                    }
                    
                    await session.close();
                    await client.disconnect();
                    
                    console.log(`✅ OPC-UA discovery from ${endpoint}: ${tags.length} tags found`);
                    
                } catch (endpointError) {
                    console.log(`⚠️ Failed to connect to ${endpoint}:`, endpointError.message);
                }
            }
            
        } catch (error) {
            console.error('❌ OPC-UA discovery error:', error);
        }
        
        return tags;
    }

    /**
     * Create OPC-UA tag definition
     */
    async createOPCUATagDefinition(session, reference, endpoint) {
        try {
            const nodeId = reference.nodeId.toString();
            const browseName = reference.browseName.name;
            
            // Read node attributes
            const dataValue = await session.read({ nodeId, attributeId: 13 }); // Value attribute
            
            return {
                id: `opcua_${browseName.toLowerCase().replace(/[^a-z0-9]/g, '_')}`,
                name: browseName,
                type: this.inferTypeFromOPCUA(dataValue),
                source: 'opcua',
                protocol: 'OPC-UA',
                location: endpoint,
                equipment: 'Industrial Equipment',
                category: 'process',
                
                // OPC-UA specific properties
                nodeId,
                endpoint,
                dataType: dataValue.value ? dataValue.value.dataType : 'Unknown',
                
                // Discovery metadata
                discovered: new Date().toISOString(),
                lastSeen: new Date().toISOString(),
                status: 'active',
                
                // Default properties
                unit: this.inferUnitFromName(browseName),
                min: 0,
                max: 100,
                precision: 2
            };
            
        } catch (error) {
            console.log(`⚠️ Error creating OPC-UA tag definition for ${reference.browseName.name}:`, error.message);
            return null;
        }
    }

    /**
     * Simulate OPC-UA discovery
     */
    simulateOPCUADiscovery() {
        const simulatedTags = [
            { name: 'Conveyor_Speed', type: 'speed', unit: 'm/min', equipment: 'Conveyor_01' },
            { name: 'Tank_Level', type: 'level', unit: '%', equipment: 'Tank_A01' },
            { name: 'Pump_Flow', type: 'flow', unit: 'L/min', equipment: 'Pump_P01' },
            { name: 'Motor_Current', type: 'current', unit: 'A', equipment: 'Motor_M01' },
            { name: 'System_Pressure', type: 'pressure', unit: 'bar', equipment: 'System' }
        ];
        
        return simulatedTags.map(tag => ({
            id: `opcua_${tag.name.toLowerCase()}`,
            name: tag.name.replace('_', ' '),
            type: tag.type,
            source: 'opcua',
            protocol: 'OPC-UA',
            location: 'opc.tcp://localhost:62541',
            equipment: tag.equipment,
            category: 'process',
            nodeId: `ns=2;s=${tag.name}`,
            endpoint: 'opc.tcp://localhost:62541',
            unit: tag.unit,
            min: 0,
            max: tag.type === 'level' ? 100 : 1000,
            precision: 2,
            discovered: new Date().toISOString(),
            lastSeen: new Date().toISOString(),
            status: 'simulated'
        }));
    }

    /**
     * Discover MQTT topics
     */
    async discoverMQTTTopics() {
        const topics = [];
        
        try {
            // Try to import MQTT library
            let mqtt;
            try {
                mqtt = require('mqtt');
            } catch (err) {
                console.log('📦 MQTT library not available, using simulation mode');
                return this.simulateMQTTDiscovery();
            }
            
            // Try each configured broker
            for (const brokerUrl of this.protocolConfigs.mqtt.brokers) {
                try {
                    console.log(`🔗 Connecting to MQTT broker: ${brokerUrl}`);
                    
                    const client = mqtt.connect(brokerUrl, {
                        connectTimeout: 5000,
                        reconnectPeriod: 0
                    });
                    
                    await new Promise((resolve, reject) => {
                        client.on('connect', resolve);
                        client.on('error', reject);
                        setTimeout(() => reject(new Error('Connection timeout')), 5000);
                    });
                    
                    // Subscribe to discovery topics
                    const discoveryTopics = this.protocolConfigs.mqtt.discoveryTopics;
                    client.subscribe(discoveryTopics);
                    
                    // Collect topics for a short period
                    const discoveredTopics = new Set();
                    
                    client.on('message', (topic, message) => {
                        discoveredTopics.add(topic);
                    });
                    
                    // Wait for topic discovery
                    await new Promise(resolve => setTimeout(resolve, 3000));
                    
                    // Create topic definitions
                    for (const topic of discoveredTopics) {
                        const topicDef = this.createMQTTTopicDefinition(topic, brokerUrl);
                        if (topicDef) {
                            topics.push(topicDef);
                        }
                    }
                    
                    client.end();
                    
                    console.log(`✅ MQTT discovery from ${brokerUrl}: ${topics.length} topics found`);
                    
                } catch (brokerError) {
                    console.log(`⚠️ Failed to connect to ${brokerUrl}:`, brokerError.message);
                }
            }
            
        } catch (error) {
            console.error('❌ MQTT discovery error:', error);
        }
        
        return topics;
    }

    /**
     * Create MQTT topic definition
     */
    createMQTTTopicDefinition(topic, brokerUrl) {
        const topicParts = topic.split('/');
        const measurement = topicParts[topicParts.length - 1];
        
        return {
            id: `mqtt_${measurement.toLowerCase().replace(/[^a-z0-9]/g, '_')}`,
            name: measurement.replace('_', ' ').toUpperCase(),
            type: this.inferTypeFromTopicName(measurement),
            source: 'mqtt',
            protocol: 'MQTT',
            location: brokerUrl,
            equipment: topicParts[0] || 'Unknown Equipment',
            category: 'telemetry',
            
            // MQTT specific properties
            topic,
            broker: brokerUrl,
            qos: 1,
            
            // Inferred properties
            unit: this.inferUnitFromName(measurement),
            min: 0,
            max: this.getDefaultMaxForType(this.inferTypeFromTopicName(measurement)),
            precision: 2,
            
            // Discovery metadata
            discovered: new Date().toISOString(),
            lastSeen: new Date().toISOString(),
            status: 'active'
        };
    }

    /**
     * Simulate MQTT discovery
     */
    simulateMQTTDiscovery() {
        const simulatedTopics = [
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
        
        return simulatedTopics.map(topic => 
            this.createMQTTTopicDefinition(topic, 'mqtt://localhost:1883')
        );
    }

    /**
     * Discover Modbus devices
     */
    async discoverModbusDevices() {
        const devices = [];
        
        try {
            // Try to import Modbus library
            let modbus;
            try {
                modbus = require('modbus-serial');
            } catch (err) {
                console.log('📦 Modbus library not available, using simulation mode');
                return this.simulateModbusDiscovery();
            }
            
            const client = new modbus();
            
            // Scan device address range
            for (let address = this.protocolConfigs.modbus.deviceScanRange.start; 
                 address <= this.protocolConfigs.modbus.deviceScanRange.end; 
                 address++) {
                
                try {
                    // Try to connect to device
                    await client.connectTCP('localhost', { port: 502 });
                    client.setID(address);
                    
                    // Try to read holding registers to detect device
                    const data = await client.readHoldingRegisters(0, 1);
                    
                    if (data && data.data) {
                        // Device responded, create device definition
                        const deviceDef = this.createModbusDeviceDefinition(address);
                        devices.push(deviceDef);
                        
                        console.log(`✅ Found Modbus device at address ${address}`);
                    }
                    
                    client.close();
                    
                } catch (deviceError) {
                    // Device not responding at this address
                }
            }
            
        } catch (error) {
            console.error('❌ Modbus discovery error:', error);
        }
        
        return devices;
    }

    /**
     * Create Modbus device definition
     */
    createModbusDeviceDefinition(address) {
        return {
            id: `modbus_device_${address}`,
            name: `Modbus Device ${address}`,
            type: 'device',
            source: 'modbus',
            protocol: 'Modbus TCP',
            location: 'localhost:502',
            equipment: `Modbus Device ${address}`,
            category: 'electrical',
            
            // Modbus specific properties
            address,
            registerType: 'holding',
            registerAddress: 0,
            quantity: 1,
            
            // Default properties
            unit: '',
            min: 0,
            max: 65535,
            precision: 0,
            
            // Discovery metadata
            discovered: new Date().toISOString(),
            lastSeen: new Date().toISOString(),
            status: 'active'
        };
    }

    /**
     * Simulate Modbus discovery
     */
    simulateModbusDiscovery() {
        const simulatedDevices = [
            { address: 1, name: 'Power_Meter', registers: ['Voltage', 'Current', 'Power'] },
            { address: 2, name: 'Weather_Station', registers: ['Wind_Speed', 'Temperature', 'Humidity'] }
        ];
        
        const devices = [];
        
        simulatedDevices.forEach(device => {
            device.registers.forEach((register, index) => {
                devices.push({
                    id: `modbus_${device.address}_${register.toLowerCase()}`,
                    name: `${device.name} ${register}`,
                    type: this.inferTypeFromName(register),
                    source: 'modbus',
                    protocol: 'Modbus TCP',
                    location: 'localhost:502',
                    equipment: device.name,
                    category: 'electrical',
                    address: device.address,
                    registerType: 'holding',
                    registerAddress: index,
                    quantity: 1,
                    unit: this.inferUnitFromName(register),
                    min: 0,
                    max: this.getDefaultMaxForType(this.inferTypeFromName(register)),
                    precision: 2,
                    discovered: new Date().toISOString(),
                    lastSeen: new Date().toISOString(),
                    status: 'simulated'
                });
            });
        });
        
        return devices;
    }

    /**
     * Update sensor registry with discovered sensors
     */
    async updateSensorRegistry(discoveredSensors) {
        let newSensors = 0;
        let updatedSensors = 0;
        
        discoveredSensors.forEach(sensor => {
            if (this.discoveredSensors.has(sensor.id)) {
                // Update existing sensor
                const existing = this.discoveredSensors.get(sensor.id);
                existing.lastSeen = sensor.lastSeen;
                existing.status = sensor.status;
                updatedSensors++;
            } else {
                // Add new sensor
                this.discoveredSensors.set(sensor.id, sensor);
                newSensors++;
            }
        });
        
        // Mark sensors as offline if not seen recently
        const now = Date.now();
        const offlineThreshold = 5 * 60 * 1000; // 5 minutes
        
        this.discoveredSensors.forEach(sensor => {
            const lastSeen = new Date(sensor.lastSeen).getTime();
            if (now - lastSeen > offlineThreshold) {
                sensor.status = 'offline';
            }
        });
        
        if (newSensors > 0 || updatedSensors > 0) {
            console.log(`📊 Sensor registry updated: ${newSensors} new, ${updatedSensors} updated`);
            this.emit('sensors_updated', {
                newSensors,
                updatedSensors,
                totalSensors: this.discoveredSensors.size
            });
        }
        
        // Save updated configuration
        await this.saveSensorConfig();
    }

    /**
     * Get all discovered sensors
     */
    getAllSensors() {
        return Array.from(this.discoveredSensors.values());
    }

    /**
     * Get sensors by source
     */
    getSensorsBySource(source) {
        return this.getAllSensors().filter(sensor => sensor.source === source);
    }

    /**
     * Get sensors by category
     */
    getSensorsByCategory(category) {
        return this.getAllSensors().filter(sensor => sensor.category === category);
    }

    /**
     * Get active sensors
     */
    getActiveSensors() {
        return this.getAllSensors().filter(sensor => sensor.status === 'active');
    }

    /**
     * Load sensor configuration from file
     */
    async loadSensorConfig() {
        try {
            const configData = await fs.readFile(this.options.configPath, 'utf8');
            const config = JSON.parse(configData);
            
            if (config.sensors) {
                config.sensors.forEach(sensor => {
                    this.discoveredSensors.set(sensor.id, sensor);
                });
                console.log(`📄 Loaded ${config.sensors.length} sensors from configuration`);
            }
            
        } catch (error) {
            console.log('📄 No existing sensor configuration found, starting fresh');
        }
    }

    /**
     * Save sensor configuration to file
     */
    async saveSensorConfig() {
        try {
            const config = {
                version: '1.0.0',
                updated: new Date().toISOString(),
                sensorCount: this.discoveredSensors.size,
                sensors: Array.from(this.discoveredSensors.values())
            };
            
            const configDir = path.dirname(this.options.configPath);
            await fs.mkdir(configDir, { recursive: true });
            await fs.writeFile(this.options.configPath, JSON.stringify(config, null, 2));
            
            console.log(`💾 Saved ${config.sensorCount} sensors to configuration`);
            
        } catch (error) {
            console.error('❌ Failed to save sensor configuration:', error);
        }
    }

    /**
     * Helper methods for type and unit inference
     */
    inferTypeFromOPCUA(dataValue) {
        if (!dataValue || !dataValue.value) return 'value';
        
        const dataType = dataValue.value.dataType;
        if (dataType === 'Boolean') return 'status';
        if (dataType === 'Double' || dataType === 'Float') return 'analog';
        return 'value';
    }

    inferTypeFromTopicName(name) {
        const lowerName = name.toLowerCase();
        if (lowerName.includes('temp')) return 'temperature';
        if (lowerName.includes('humid')) return 'humidity';
        if (lowerName.includes('press')) return 'pressure';
        if (lowerName.includes('level')) return 'level';
        if (lowerName.includes('flow')) return 'flow';
        if (lowerName.includes('speed')) return 'speed';
        if (lowerName.includes('voltage')) return 'voltage';
        if (lowerName.includes('current')) return 'current';
        if (lowerName.includes('power')) return 'power';
        if (lowerName.includes('altitude')) return 'altitude';
        if (lowerName.includes('velocity')) return 'velocity';
        if (lowerName.includes('accel')) return 'acceleration';
        if (lowerName.includes('gps') || lowerName.includes('lat') || lowerName.includes('lon')) return 'position';
        if (lowerName.includes('status')) return 'status';
        return 'value';
    }

    inferTypeFromName(name) {
        return this.inferTypeFromTopicName(name);
    }

    inferUnitFromName(name) {
        const lowerName = name.toLowerCase();
        if (lowerName.includes('temp')) return '°C';
        if (lowerName.includes('humid')) return '%RH';
        if (lowerName.includes('press')) return 'bar';
        if (lowerName.includes('level')) return '%';
        if (lowerName.includes('flow')) return 'L/min';
        if (lowerName.includes('speed') || lowerName.includes('velocity')) return 'm/s';
        if (lowerName.includes('voltage')) return 'V';
        if (lowerName.includes('current')) return 'A';
        if (lowerName.includes('power')) return 'kW';
        if (lowerName.includes('altitude')) return 'm';
        if (lowerName.includes('accel')) return 'g';
        if (lowerName.includes('gps') || lowerName.includes('lat') || lowerName.includes('lon')) return '°';
        if (lowerName.includes('signal')) return 'dBm';
        return '';
    }

    getDefaultMaxForType(type) {
        const maxValues = {
            temperature: 100,
            humidity: 100,
            pressure: 1000,
            level: 100,
            flow: 1000,
            speed: 100,
            voltage: 500,
            current: 100,
            power: 10000,
            altitude: 10000,
            velocity: 100,
            acceleration: 10,
            position: 180,
            signal: 0
        };
        return maxValues[type] || 100;
    }
}

module.exports = SensorDiscoverySystem;