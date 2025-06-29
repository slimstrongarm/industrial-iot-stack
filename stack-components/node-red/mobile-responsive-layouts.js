/**
 * Mobile-Responsive Dashboard Layouts for CT-084 Parachute Drop System
 * Optimized layouts for field operations and mobile devices
 * Author: Agent 3 - Dashboard Generator and Production Deployment
 */

class MobileResponsiveLayoutGenerator {
    constructor(options = {}) {
        this.options = {
            breakpoints: {
                mobile: 768,
                tablet: 1024,
                desktop: 1440
            },
            priorityOrder: ['critical', 'warning', 'info'],
            maxMobileGroups: 3,
            enableOfflineMode: options.enableOfflineMode !== false,
            ...options
        };
        
        this.mobileLayouts = new Map();
        this.responsiveTemplates = new Map();
    }

    /**
     * Generate mobile-optimized dashboard layouts
     */
    generateMobileLayouts(sensors, equipment) {
        console.log('📱 Generating mobile-responsive layouts...');
        
        // Field Operations Layout - Critical sensors only
        const fieldLayout = this.generateFieldOperationsLayout(sensors, equipment);
        
        // Equipment Quick View - Single equipment focus
        const equipmentLayout = this.generateEquipmentQuickView(equipment);
        
        // Emergency Response Layout - Alarms and critical status
        const emergencyLayout = this.generateEmergencyResponseLayout(sensors);
        
        // Mission Overview - Parachute drop specific
        const missionLayout = this.generateMissionOverviewLayout(sensors);
        
        return {
            field: fieldLayout,
            equipment: equipmentLayout,
            emergency: emergencyLayout,
            mission: missionLayout
        };
    }

    /**
     * Generate field operations layout for mobile
     */
    generateFieldOperationsLayout(sensors, equipment) {
        const criticalSensors = sensors.filter(s => 
            s.type === 'status' || 
            s.category === 'telemetry' ||
            (s.thresholds && s.thresholds.critical)
        ).slice(0, 6); // Limit to 6 most critical

        return {
            id: "field_operations_mobile",
            name: "Field Operations",
            description: "Mobile-optimized layout for field personnel",
            viewport: "mobile",
            flows: [
                {
                    id: "field_tab",
                    type: "ui_tab",
                    name: "Field Ops",
                    icon: "assignment_ind",
                    order: 1
                },
                {
                    id: "status_group",
                    type: "ui_group",
                    name: "System Status",
                    tab: "field_tab",
                    order: 1,
                    width: "12", // Full width for mobile
                    collapse: false
                },
                ...this.generateMobileStatusCard(criticalSensors),
                {
                    id: "quick_actions_group",
                    type: "ui_group",
                    name: "Quick Actions",
                    tab: "field_tab",
                    order: 2,
                    width: "12",
                    collapse: false
                },
                ...this.generateMobileActionButtons(),
                {
                    id: "alerts_group",
                    type: "ui_group",
                    name: "Active Alerts",
                    tab: "field_tab",
                    order: 3,
                    width: "12",
                    collapse: false
                },
                ...this.generateMobileAlertsList()
            ],
            customCSS: this.getMobileFieldCSS()
        };
    }

    /**
     * Generate equipment quick view for mobile
     */
    generateEquipmentQuickView(equipment) {
        return {
            id: "equipment_mobile",
            name: "Equipment View",
            description: "Single equipment focus for mobile",
            viewport: "mobile",
            flows: equipment.slice(0, 3).map((eq, index) => ({
                id: `eq_tab_${eq.name.toLowerCase().replace(/[^a-z0-9]/g, '_')}`,
                type: "ui_tab",
                name: eq.name.substring(0, 8), // Truncate for mobile
                icon: this.getEquipmentMobileIcon(eq.category),
                order: index + 1,
                flows: [
                    {
                        id: `eq_overview_${eq.name.toLowerCase().replace(/[^a-z0-9]/g, '_')}`,
                        type: "ui_group",
                        name: "Overview",
                        tab: `eq_tab_${eq.name.toLowerCase().replace(/[^a-z0-9]/g, '_')}`,
                        order: 1,
                        width: "12"
                    },
                    ...this.generateMobileEquipmentWidgets(eq.sensors.slice(0, 4)) // Max 4 sensors
                ]
            })),
            customCSS: this.getMobileEquipmentCSS()
        };
    }

    /**
     * Generate emergency response layout
     */
    generateEmergencyResponseLayout(sensors) {
        return {
            id: "emergency_mobile",
            name: "Emergency Response",
            description: "Emergency response interface for mobile",
            viewport: "mobile",
            flows: [
                {
                    id: "emergency_tab",
                    type: "ui_tab",
                    name: "Emergency",
                    icon: "warning",
                    order: 1
                },
                {
                    id: "emergency_status",
                    type: "ui_template",
                    group: "emergency_main",
                    name: "Emergency Status",
                    order: 1,
                    width: "12",
                    height: "4",
                    format: this.getEmergencyStatusTemplate(),
                    x: 60,
                    y: 60
                },
                {
                    id: "emergency_main",
                    type: "ui_group",
                    name: "Emergency Control",
                    tab: "emergency_tab",
                    order: 1,
                    width: "12"
                },
                {
                    id: "emergency_abort",
                    type: "ui_button",
                    group: "emergency_main",
                    name: "EMERGENCY ABORT",
                    order: 2,
                    width: "12",
                    height: "3",
                    color: "red",
                    bgcolor: "#FF0000",
                    className: "emergency-button",
                    x: 60,
                    y: 140
                },
                {
                    id: "emergency_comms",
                    type: "ui_group",
                    name: "Communications",
                    tab: "emergency_tab",
                    order: 2,
                    width: "12"
                },
                {
                    id: "radio_check",
                    type: "ui_button",
                    group: "emergency_comms",
                    name: "Radio Check",
                    order: 1,
                    width: "6",
                    height: "2",
                    x: 60,
                    y: 220
                },
                {
                    id: "alert_all",
                    type: "ui_button",
                    group: "emergency_comms",
                    name: "Alert All",
                    order: 2,
                    width: "6",
                    height: "2",
                    x: 180,
                    y: 220
                }
            ],
            customCSS: this.getEmergencyCSS()
        };
    }

    /**
     * Generate mission overview layout for parachute drop
     */
    generateMissionOverviewLayout(sensors) {
        const telemetrySensors = sensors.filter(s => s.category === 'telemetry');
        
        return {
            id: "mission_mobile",
            name: "Mission Overview",
            description: "Parachute drop mission overview for mobile",
            viewport: "mobile",
            flows: [
                {
                    id: "mission_tab",
                    type: "ui_tab",
                    name: "Mission",
                    icon: "flight_takeoff",
                    order: 1
                },
                {
                    id: "mission_phase",
                    type: "ui_group",
                    name: "Mission Phase",
                    tab: "mission_tab",
                    order: 1,
                    width: "12"
                },
                {
                    id: "phase_indicator",
                    type: "ui_template",
                    group: "mission_phase",
                    name: "Current Phase",
                    order: 1,
                    width: "12",
                    height: "3",
                    format: this.getMissionPhaseTemplate(),
                    x: 60,
                    y: 60
                },
                {
                    id: "telemetry_group",
                    type: "ui_group",
                    name: "Key Telemetry",
                    tab: "mission_tab",
                    order: 2,
                    width: "12"
                },
                ...this.generateMobileTelemetryWidgets(telemetrySensors),
                {
                    id: "mission_map",
                    type: "ui_group",
                    name: "Position",
                    tab: "mission_tab",
                    order: 3,
                    width: "12"
                },
                {
                    id: "position_map",
                    type: "ui_worldmap",
                    group: "mission_map",
                    name: "Drop Position",
                    order: 1,
                    width: "12",
                    height: "8",
                    zoom: "15",
                    x: 60,
                    y: 300
                }
            ],
            customCSS: this.getMissionCSS()
        };
    }

    /**
     * Generate mobile status card
     */
    generateMobileStatusCard(sensors) {
        return [{
            id: "mobile_status_card",
            type: "ui_template",
            group: "status_group",
            name: "System Status Card",
            order: 1,
            width: "12",
            height: "6",
            format: this.generateMobileStatusTemplate(sensors),
            x: 60,
            y: 60
        }];
    }

    /**
     * Generate mobile action buttons
     */
    generateMobileActionButtons() {
        const actions = [
            { name: "Refresh", icon: "refresh", color: "blue" },
            { name: "Test Comms", icon: "wifi", color: "green" },
            { name: "View Logs", icon: "list", color: "gray" },
            { name: "Emergency", icon: "warning", color: "red" }
        ];

        return actions.map((action, index) => ({
            id: `action_${action.name.toLowerCase().replace(' ', '_')}`,
            type: "ui_button",
            group: "quick_actions_group",
            name: action.name,
            order: index + 1,
            width: "6",
            height: "2",
            color: action.color,
            icon: `fa-${action.icon}`,
            x: 60 + (index % 2) * 120,
            y: 180 + Math.floor(index / 2) * 80
        }));
    }

    /**
     * Generate mobile alerts list
     */
    generateMobileAlertsList() {
        return [{
            id: "mobile_alerts",
            type: "ui_template",
            group: "alerts_group",
            name: "Active Alerts",
            order: 1,
            width: "12",
            height: "8",
            format: this.getMobileAlertsTemplate(),
            x: 60,
            y: 340
        }];
    }

    /**
     * Generate mobile equipment widgets
     */
    generateMobileEquipmentWidgets(sensors) {
        return sensors.map((sensor, index) => {
            const yPos = 140 + (index * 80);
            
            if (sensor.type === 'status') {
                return {
                    id: `mobile_${sensor.id}`,
                    type: "ui_led",
                    group: `eq_overview_${sensor.equipment.toLowerCase().replace(/[^a-z0-9]/g, '_')}`,
                    name: sensor.name,
                    order: index + 1,
                    width: "12",
                    height: "2",
                    x: 60,
                    y: yPos
                };
            } else {
                return {
                    id: `mobile_${sensor.id}`,
                    type: "ui_gauge",
                    group: `eq_overview_${sensor.equipment.toLowerCase().replace(/[^a-z0-9]/g, '_')}`,
                    name: sensor.name,
                    order: index + 1,
                    width: "12",
                    height: "4",
                    gtype: "donut",
                    min: sensor.min,
                    max: sensor.max,
                    x: 60,
                    y: yPos
                };
            }
        });
    }

    /**
     * Generate mobile telemetry widgets
     */
    generateMobileTelemetryWidgets(telemetrySensors) {
        const keyTelemetry = ['altitude', 'velocity', 'battery_voltage', 'signal_strength'];
        const filteredSensors = telemetrySensors.filter(s => 
            keyTelemetry.some(key => s.id.includes(key))
        ).slice(0, 4);

        return filteredSensors.map((sensor, index) => ({
            id: `mobile_telemetry_${sensor.id}`,
            type: "ui_text",
            group: "telemetry_group",
            name: sensor.name,
            order: index + 1,
            width: "6",
            height: "2",
            format: `{{msg.payload}} ${sensor.unit}`,
            layout: "row-spread",
            className: "mobile-telemetry",
            x: 60 + (index % 2) * 120,
            y: 140 + Math.floor(index / 2) * 60
        }));
    }

    /**
     * CSS Templates for Mobile Layouts
     */
    getMobileFieldCSS() {
        return `
/* Mobile Field Operations CSS */
@media screen and (max-width: 768px) {
    .nr-dashboard-template {
        padding: 8px !important;
    }
    
    .status-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 12px;
        padding: 16px;
        margin: 8px 0;
        color: white;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    .status-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 12px;
        margin-top: 12px;
    }
    
    .status-item {
        background: rgba(255,255,255,0.1);
        border-radius: 8px;
        padding: 12px;
        text-align: center;
    }
    
    .status-value {
        font-size: 20px;
        font-weight: bold;
        margin-bottom: 4px;
    }
    
    .status-label {
        font-size: 12px;
        opacity: 0.9;
    }
    
    .quick-action-btn {
        margin: 4px;
        border-radius: 8px;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .alert-list {
        max-height: 300px;
        overflow-y: auto;
    }
    
    .alert-item {
        background: white;
        border-left: 4px solid #ff9800;
        margin: 8px 0;
        padding: 12px;
        border-radius: 4px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .alert-critical {
        border-left-color: #f44336;
    }
    
    .alert-warning {
        border-left-color: #ff9800;
    }
    
    .alert-info {
        border-left-color: #2196f3;
    }
}
        `;
    }

    getMobileEquipmentCSS() {
        return `
/* Mobile Equipment CSS */
@media screen and (max-width: 768px) {
    .equipment-header {
        background: #f5f5f5;
        padding: 12px;
        border-radius: 8px;
        margin-bottom: 16px;
        text-align: center;
    }
    
    .equipment-name {
        font-size: 18px;
        font-weight: bold;
        color: #333;
        margin-bottom: 4px;
    }
    
    .equipment-status {
        font-size: 14px;
        color: #666;
    }
    
    .sensor-card {
        background: white;
        border-radius: 8px;
        padding: 16px;
        margin: 8px 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .sensor-name {
        font-size: 14px;
        font-weight: bold;
        color: #333;
        margin-bottom: 8px;
    }
    
    .sensor-value {
        font-size: 24px;
        font-weight: bold;
        text-align: center;
        margin: 12px 0;
    }
    
    .sensor-unit {
        font-size: 12px;
        color: #666;
        text-align: center;
    }
    
    .gauge-mobile {
        width: 100% !important;
        height: auto !important;
    }
}
        `;
    }

    getEmergencyCSS() {
        return `
/* Emergency Response CSS */
@media screen and (max-width: 768px) {
    .emergency-status {
        background: linear-gradient(135deg, #ff4444 0%, #cc0000 100%);
        color: white;
        padding: 20px;
        text-align: center;
        border-radius: 12px;
        margin-bottom: 16px;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(255, 68, 68, 0.7); }
        70% { box-shadow: 0 0 0 10px rgba(255, 68, 68, 0); }
        100% { box-shadow: 0 0 0 0 rgba(255, 68, 68, 0); }
    }
    
    .emergency-button {
        background: #ff0000 !important;
        color: white !important;
        font-size: 18px !important;
        font-weight: bold !important;
        padding: 20px !important;
        border-radius: 12px !important;
        border: 3px solid #ffffff !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        box-shadow: 0 4px 16px rgba(255, 0, 0, 0.4) !important;
    }
    
    .emergency-button:active {
        transform: scale(0.95);
        box-shadow: 0 2px 8px rgba(255, 0, 0, 0.6) !important;
    }
    
    .comms-button {
        background: #2196f3;
        color: white;
        margin: 4px;
        border-radius: 8px;
        font-weight: bold;
        padding: 12px;
    }
    
    .emergency-info {
        background: #fff3cd;
        border: 1px solid #ffeaa7;
        color: #856404;
        padding: 12px;
        border-radius: 8px;
        margin: 8px 0;
        font-size: 14px;
    }
}
        `;
    }

    getMissionCSS() {
        return `
/* Mission Overview CSS */
@media screen and (max-width: 768px) {
    .mission-phase {
        background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
        color: white;
        padding: 20px;
        text-align: center;
        border-radius: 12px;
        margin-bottom: 16px;
    }
    
    .phase-name {
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 8px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .phase-description {
        font-size: 14px;
        opacity: 0.9;
    }
    
    .phase-timer {
        font-size: 16px;
        font-weight: bold;
        margin-top: 8px;
        font-family: monospace;
    }
    
    .telemetry-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 8px;
        margin: 16px 0;
    }
    
    .mobile-telemetry {
        background: white;
        border-radius: 8px;
        padding: 12px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 4px;
    }
    
    .telemetry-value {
        font-size: 18px;
        font-weight: bold;
        color: #333;
        margin-bottom: 4px;
    }
    
    .telemetry-label {
        font-size: 11px;
        color: #666;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .map-container {
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
}
        `;
    }

    /**
     * Template generators
     */
    generateMobileStatusTemplate(sensors) {
        return `
<div class="status-card">
    <div style="text-align: center; margin-bottom: 16px;">
        <div style="font-size: 20px; font-weight: bold;">System Status</div>
        <div style="font-size: 12px; opacity: 0.8;">{{msg.timestamp || new Date().toLocaleString()}}</div>
    </div>
    
    <div class="status-grid">
        <div class="status-item">
            <div class="status-value" style="color: #4CAF50;">{{msg.payload.onlineSensors || 0}}</div>
            <div class="status-label">Online</div>
        </div>
        
        <div class="status-item">
            <div class="status-value" style="color: #FF9800;">{{msg.payload.alerts || 0}}</div>
            <div class="status-label">Alerts</div>
        </div>
        
        <div class="status-item">
            <div class="status-value" style="color: #2196F3;">{{msg.payload.dataRate || 0}}</div>
            <div class="status-label">Data/min</div>
        </div>
        
        <div class="status-item">
            <div class="status-value" style="color: #9C27B0;">{{msg.payload.uptime || '0h'}}</div>
            <div class="status-label">Uptime</div>
        </div>
    </div>
</div>
        `;
    }

    getEmergencyStatusTemplate() {
        return `
<div class="emergency-status">
    <div style="font-size: 24px; font-weight: bold; margin-bottom: 8px;">
        <i class="fa fa-exclamation-triangle"></i> EMERGENCY MODE
    </div>
    <div style="font-size: 14px; opacity: 0.9;">
        Status: {{msg.payload.emergencyStatus || 'STANDBY'}}
    </div>
    <div style="font-size: 12px; margin-top: 8px;">
        Last Update: {{msg.timestamp || new Date().toLocaleString()}}
    </div>
</div>
        `;
    }

    getMissionPhaseTemplate() {
        return `
<div class="mission-phase">
    <div class="phase-name">{{msg.payload.phase || 'STANDBY'}}</div>
    <div class="phase-description">{{msg.payload.description || 'System Ready'}}</div>
    <div class="phase-timer">{{msg.payload.missionTime || '00:00:00'}}</div>
</div>
        `;
    }

    getMobileAlertsTemplate() {
        return `
<div class="alert-list">
    <div ng-repeat="alert in msg.payload.alerts" class="alert-item alert-{{alert.severity.toLowerCase()}}">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <div style="font-weight: bold; color: #333; margin-bottom: 4px;">
                    {{alert.equipment}} - {{alert.sensor}}
                </div>
                <div style="font-size: 12px; color: #666;">
                    {{alert.message}}
                </div>
            </div>
            <div style="text-align: right;">
                <div style="background: #ff9800; color: white; padding: 2px 8px; border-radius: 12px; font-size: 10px; font-weight: bold;">
                    {{alert.severity}}
                </div>
                <div style="font-size: 10px; color: #999; margin-top: 2px;">
                    {{alert.timestamp | date:'HH:mm'}}
                </div>
            </div>
        </div>
    </div>
    
    <div ng-if="!msg.payload.alerts || msg.payload.alerts.length === 0" style="text-align: center; padding: 20px; color: #666;">
        <i class="fa fa-check-circle" style="font-size: 24px; color: #4CAF50; margin-bottom: 8px;"></i>
        <div>No Active Alerts</div>
    </div>
</div>
        `;
    }

    /**
     * Helper methods
     */
    getEquipmentMobileIcon(category) {
        const icons = {
            environment: "eco",
            process: "settings",
            electrical: "flash_on",
            telemetry: "satellite",
            general: "devices"
        };
        return icons[category] || "devices";
    }

    /**
     * Generate responsive breakpoint configurations
     */
    generateResponsiveConfig() {
        return {
            mobile: {
                maxWidth: this.options.breakpoints.mobile,
                columns: 12,
                groupWidth: 12,
                widgetHeight: 2,
                spacing: 4
            },
            tablet: {
                maxWidth: this.options.breakpoints.tablet,
                columns: 24,
                groupWidth: 12,
                widgetHeight: 3,
                spacing: 6
            },
            desktop: {
                maxWidth: this.options.breakpoints.desktop,
                columns: 24,
                groupWidth: 6,
                widgetHeight: 4,
                spacing: 6
            }
        };
    }

    /**
     * Export mobile layouts package
     */
    async exportMobileLayouts(outputPath) {
        const layouts = this.generateMobileLayouts([], []); // Would receive actual sensor data
        
        const mobilePackage = {
            version: "1.0.0",
            name: "CT-084 Mobile Dashboard Layouts",
            description: "Mobile-responsive layouts for field operations",
            generated: new Date().toISOString(),
            
            layouts,
            
            responsive: this.generateResponsiveConfig(),
            
            features: {
                offline: this.options.enableOfflineMode,
                touch: true,
                swipe: true,
                orientation: "both"
            },
            
            customCSS: {
                field: this.getMobileFieldCSS(),
                equipment: this.getMobileEquipmentCSS(),
                emergency: this.getEmergencyCSS(),
                mission: this.getMissionCSS()
            }
        };
        
        if (outputPath) {
            const fs = require('fs').promises;
            await fs.writeFile(outputPath, JSON.stringify(mobilePackage, null, 2));
            console.log(`📱 Mobile layouts exported to: ${outputPath}`);
        }
        
        return mobilePackage;
    }
}

module.exports = MobileResponsiveLayoutGenerator;