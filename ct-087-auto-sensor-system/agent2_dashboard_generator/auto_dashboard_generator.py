#!/usr/bin/env python3
"""
CT-087 Agent 2: Auto Dashboard Generator
Professional dashboard creation from detected sensors

Consumes Agent 1 sensor profiles and generates:
- Real-time sensor dashboards
- Professional industrial UI layouts
- Interactive controls and displays
- Mobile-responsive designs
- Node-RED dashboard flows

Author: Server Claude Agent 2
Project: CT-087 Auto Sensor Detection System
ADK Coordination: Receives input from Agent 1, provides to Agent 3/4
"""

import json
import time
import asyncio
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import uuid
import jinja2
import yaml

# Dashboard generation libraries
try:
    import plotly.graph_objects as go
    import plotly.express as px
    from plotly.subplots import make_subplots
    import dash
    from dash import dcc, html, Input, Output, State
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
    logging.warning("Plotly/Dash not available - generating static configs")

# Configure logging for CT-087 Agent 2
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | CT-087-A2 | %(name)-25s | %(levelname)-8s | %(message)s',
    handlers=[
        logging.FileHandler('/tmp/ct-087-logs/agent2_dashboard_generator.log', mode='a'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('AutoDashboardGenerator')

class DashboardType(Enum):
    """Types of dashboards to generate."""
    OVERVIEW = "overview"
    DETAILED = "detailed"
    MOBILE = "mobile"
    PROCESS = "process"
    ALARM = "alarm"
    TREND = "trend"

class WidgetType(Enum):
    """Dashboard widget types."""
    GAUGE = "gauge"
    LINE_CHART = "line_chart"
    BAR_CHART = "bar_chart"
    THERMOMETER = "thermometer"
    BOOLEAN_INDICATOR = "boolean_indicator"
    NUMERIC_DISPLAY = "numeric_display"
    TREND_INDICATOR = "trend_indicator"
    ALARM_PANEL = "alarm_panel"
    TABLE = "table"
    HISTOGRAM = "histogram"

@dataclass
class DashboardWidget:
    """Dashboard widget configuration."""
    widget_id: str
    widget_type: WidgetType
    sensor_id: str
    title: str
    position: Dict[str, int]  # x, y, width, height
    config: Dict[str, Any]
    style: Dict[str, str]
    data_source: str
    update_interval: int
    thresholds: Dict[str, float]
    created_at: datetime

@dataclass
class DashboardLayout:
    """Complete dashboard layout."""
    dashboard_id: str
    dashboard_type: DashboardType
    title: str
    description: str
    widgets: List[DashboardWidget]
    layout_config: Dict[str, Any]
    responsive_config: Dict[str, Any]
    theme: str
    created_at: datetime
    sensor_count: int
    auto_generated: bool

class AutoDashboardGenerator:
    """
    Automatic dashboard generator for CT-087 detected sensors.
    
    Features:
    - Consumes Agent 1 sensor profiles
    - Generates multiple dashboard types
    - Creates Node-RED flows
    - Responsive design support
    - Professional industrial themes
    """
    
    def __init__(self, config_path: str = "/etc/ct-087/dashboard_config.json"):
        self.config_path = config_path
        self.sensor_profiles: Dict[str, Dict] = {}
        self.generated_dashboards: Dict[str, DashboardLayout] = {}
        self.dashboard_templates = self.load_dashboard_templates()
        
        # ADK Coordination
        self.agent_id = "ct-087-agent-2"
        self.coordination_state = {
            "status": "initializing",
            "input_agents": ["ct-087-agent-1"],
            "output_agents": ["ct-087-agent-3", "ct-087-agent-4"],
            "resources_locked": [],
            "dependencies_met": False
        }
        
        self.load_configuration()
        logger.info(f"🎨 CT-087 Agent 2 initialized - Auto Dashboard Generator")
    
    def load_configuration(self):
        """Load dashboard generation configuration."""
        try:
            if Path(self.config_path).exists():
                with open(self.config_path, 'r') as f:
                    self.config = json.load(f)
            else:
                self.config = self.create_default_dashboard_config()
                self.save_configuration()
            
            logger.info(f"✅ Dashboard configuration loaded")
        except Exception as e:
            logger.error(f"❌ Failed to load dashboard configuration: {e}")
            self.config = self.create_default_dashboard_config()
    
    def create_default_dashboard_config(self) -> Dict:
        """Create default dashboard configuration."""
        return {
            "themes": {
                "industrial": {
                    "primary_color": "#1f2937",
                    "secondary_color": "#374151",
                    "accent_color": "#3b82f6",
                    "warning_color": "#f59e0b",
                    "danger_color": "#ef4444",
                    "success_color": "#10b981",
                    "background_color": "#f9fafb",
                    "text_color": "#111827",
                    "font_family": "Arial, sans-serif"
                },
                "dark": {
                    "primary_color": "#0f172a",
                    "secondary_color": "#1e293b",
                    "accent_color": "#0ea5e9",
                    "warning_color": "#f97316",
                    "danger_color": "#dc2626",
                    "success_color": "#059669",
                    "background_color": "#020617",
                    "text_color": "#f8fafc",
                    "font_family": "Arial, sans-serif"
                }
            },
            "layouts": {
                "overview": {
                    "grid_columns": 12,
                    "grid_rows": 8,
                    "widget_margin": 10,
                    "responsive_breakpoints": {
                        "mobile": 768,
                        "tablet": 1024,
                        "desktop": 1440
                    }
                }
            },
            "widgets": {
                "default_sizes": {
                    "gauge": {"width": 3, "height": 2},
                    "line_chart": {"width": 6, "height": 3},
                    "thermometer": {"width": 2, "height": 4},
                    "boolean_indicator": {"width": 2, "height": 1},
                    "table": {"width": 12, "height": 4}
                }
            },
            "update_intervals": {
                "real_time": 1000,
                "fast": 5000,
                "normal": 10000,
                "slow": 30000
            },
            "data_retention": {
                "real_time_buffer": 1000,
                "historical_days": 30
            }
        }
    
    def save_configuration(self):
        """Save dashboard configuration."""
        try:
            Path(self.config_path).parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_path, 'w') as f:
                json.dump(self.config, f, indent=2)
            logger.info(f"✅ Dashboard configuration saved")
        except Exception as e:
            logger.error(f"❌ Failed to save dashboard configuration: {e}")
    
    def load_dashboard_templates(self) -> Dict:
        """Load dashboard templates for different sensor types."""
        return {
            "current_4_20ma": {
                "primary_widget": WidgetType.GAUGE,
                "secondary_widgets": [WidgetType.LINE_CHART, WidgetType.TREND_INDICATOR],
                "layout_priority": "high",
                "color_scheme": "blue"
            },
            "temperature_rtd": {
                "primary_widget": WidgetType.THERMOMETER,
                "secondary_widgets": [WidgetType.LINE_CHART, WidgetType.ALARM_PANEL],
                "layout_priority": "high",
                "color_scheme": "red"
            },
            "pressure_gauge": {
                "primary_widget": WidgetType.GAUGE,
                "secondary_widgets": [WidgetType.LINE_CHART, WidgetType.NUMERIC_DISPLAY],
                "layout_priority": "high",
                "color_scheme": "green"
            },
            "digital_input": {
                "primary_widget": WidgetType.BOOLEAN_INDICATOR,
                "secondary_widgets": [WidgetType.ALARM_PANEL],
                "layout_priority": "medium",
                "color_scheme": "purple"
            },
            "voltage_0_10v": {
                "primary_widget": WidgetType.GAUGE,
                "secondary_widgets": [WidgetType.LINE_CHART],
                "layout_priority": "medium",
                "color_scheme": "orange"
            }
        }
    
    async def load_sensor_profiles(self) -> bool:
        """Load sensor profiles from Agent 1."""
        try:
            # Check for Agent 1 completion
            agent1_completion_path = "/tmp/ct-087-agent1-completion.json"
            if not Path(agent1_completion_path).exists():
                logger.warning("⏳ Waiting for Agent 1 to complete sensor detection...")
                return False
            
            # Load Agent 1 results
            with open(agent1_completion_path, 'r') as f:
                agent1_results = json.load(f)
            
            sensor_profiles_path = agent1_results.get("output_file")
            if not sensor_profiles_path or not Path(sensor_profiles_path).exists():
                logger.error("❌ Agent 1 sensor profiles file not found")
                return False
            
            # Load sensor profiles
            with open(sensor_profiles_path, 'r') as f:
                profiles_data = json.load(f)
            
            self.sensor_profiles = {
                sensor['sensor_id']: sensor 
                for sensor in profiles_data['sensors']
            }
            
            logger.info(f"✅ Loaded {len(self.sensor_profiles)} sensor profiles from Agent 1")
            self.coordination_state["dependencies_met"] = True
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to load sensor profiles: {e}")
            return False
    
    async def generate_all_dashboards(self) -> List[DashboardLayout]:
        """Generate all dashboard types for detected sensors."""
        if not await self.load_sensor_profiles():
            logger.error("❌ Cannot generate dashboards without sensor profiles")
            return []
        
        logger.info(f"🎨 Generating dashboards for {len(self.sensor_profiles)} sensors...")
        
        generated_dashboards = []
        
        # Generate different dashboard types
        dashboard_types = [
            DashboardType.OVERVIEW,
            DashboardType.DETAILED,
            DashboardType.MOBILE,
            DashboardType.PROCESS,
            DashboardType.ALARM
        ]
        
        for dashboard_type in dashboard_types:
            try:
                dashboard = await self.generate_dashboard(dashboard_type)
                if dashboard:
                    generated_dashboards.append(dashboard)
                    self.generated_dashboards[dashboard.dashboard_id] = dashboard
                    logger.info(f"✅ Generated {dashboard_type.value} dashboard: {dashboard.dashboard_id}")
            except Exception as e:
                logger.error(f"❌ Failed to generate {dashboard_type.value} dashboard: {e}")
        
        # Save all generated dashboards
        await self.save_dashboards(generated_dashboards)
        
        logger.info(f"🎯 Dashboard generation complete: {len(generated_dashboards)} dashboards created")
        return generated_dashboards
    
    async def generate_dashboard(self, dashboard_type: DashboardType) -> Optional[DashboardLayout]:
        """Generate a specific type of dashboard."""
        try:
            dashboard_id = f"ct087_{dashboard_type.value}_{int(time.time())}"
            
            # Create widgets based on dashboard type
            widgets = await self.create_widgets_for_dashboard(dashboard_type)
            
            # Configure layout
            layout_config = self.create_layout_config(dashboard_type, len(widgets))
            
            # Configure responsive behavior
            responsive_config = self.create_responsive_config(dashboard_type)
            
            # Select theme
            theme = "industrial" if dashboard_type in [DashboardType.PROCESS, DashboardType.OVERVIEW] else "dark"
            
            dashboard = DashboardLayout(
                dashboard_id=dashboard_id,
                dashboard_type=dashboard_type,
                title=self.get_dashboard_title(dashboard_type),
                description=self.get_dashboard_description(dashboard_type),
                widgets=widgets,
                layout_config=layout_config,
                responsive_config=responsive_config,
                theme=theme,
                created_at=datetime.now(),
                sensor_count=len(self.sensor_profiles),
                auto_generated=True
            )
            
            return dashboard
            
        except Exception as e:
            logger.error(f"❌ Failed to generate {dashboard_type.value} dashboard: {e}")
            return None
    
    async def create_widgets_for_dashboard(self, dashboard_type: DashboardType) -> List[DashboardWidget]:
        """Create widgets for a specific dashboard type."""
        widgets = []
        
        # Grid position tracking
        current_x = 0
        current_y = 0
        grid_columns = self.config["layouts"]["overview"]["grid_columns"]
        
        for sensor_id, sensor_profile in self.sensor_profiles.items():
            try:
                sensor_type = sensor_profile.get("sensor_type", "unknown")
                template = self.dashboard_templates.get(sensor_type, self.dashboard_templates["current_4_20ma"])
                
                # Create primary widget
                primary_widget = await self.create_sensor_widget(
                    sensor_profile, 
                    template["primary_widget"], 
                    dashboard_type,
                    position={"x": current_x, "y": current_y}
                )
                
                if primary_widget:
                    widgets.append(primary_widget)
                    
                    # Update position for next widget
                    widget_width = primary_widget.position["width"]
                    current_x += widget_width
                    
                    if current_x >= grid_columns:
                        current_x = 0
                        current_y += primary_widget.position["height"]
                
                # Add secondary widgets for detailed dashboards
                if dashboard_type == DashboardType.DETAILED:
                    for secondary_type in template["secondary_widgets"]:
                        secondary_widget = await self.create_sensor_widget(
                            sensor_profile,
                            secondary_type,
                            dashboard_type,
                            position={"x": current_x, "y": current_y},
                            is_secondary=True
                        )
                        
                        if secondary_widget:
                            widgets.append(secondary_widget)
                            current_x += secondary_widget.position["width"]
                            
                            if current_x >= grid_columns:
                                current_x = 0
                                current_y += secondary_widget.position["height"]
                
            except Exception as e:
                logger.error(f"❌ Failed to create widget for sensor {sensor_id}: {e}")
        
        return widgets
    
    async def create_sensor_widget(self, sensor_profile: Dict, widget_type: WidgetType, 
                                 dashboard_type: DashboardType, position: Dict[str, int],
                                 is_secondary: bool = False) -> Optional[DashboardWidget]:
        """Create a widget for a specific sensor."""
        try:
            sensor_id = sensor_profile["sensor_id"]
            sensor_name = sensor_profile["name"]
            sensor_units = sensor_profile["units"]
            dashboard_config = sensor_profile.get("dashboard_config", {})
            safety_limits = sensor_profile.get("safety_limits", {})
            
            # Generate widget ID
            widget_id = f"widget_{sensor_id}_{widget_type.value}"
            if is_secondary:
                widget_id += "_secondary"
            
            # Get default widget size
            default_sizes = self.config["widgets"]["default_sizes"]
            widget_size = default_sizes.get(widget_type.value, {"width": 3, "height": 2})
            
            # Adjust size for dashboard type
            if dashboard_type == DashboardType.MOBILE:
                widget_size = {"width": min(widget_size["width"], 6), "height": widget_size["height"]}
            elif dashboard_type == DashboardType.OVERVIEW and is_secondary:
                widget_size = {"width": widget_size["width"] // 2, "height": widget_size["height"] // 2}
            
            # Create widget configuration
            widget_config = await self.create_widget_config(widget_type, sensor_profile, dashboard_config)
            
            # Create widget style
            widget_style = self.create_widget_style(widget_type, sensor_profile, dashboard_type)
            
            # Determine update interval
            update_interval = self.get_update_interval(sensor_profile, dashboard_type)
            
            # Create thresholds
            thresholds = self.create_widget_thresholds(safety_limits)
            
            widget = DashboardWidget(
                widget_id=widget_id,
                widget_type=widget_type,
                sensor_id=sensor_id,
                title=f"{sensor_name}" + (f" ({widget_type.value.replace('_', ' ').title()})" if is_secondary else ""),
                position={
                    "x": position["x"],
                    "y": position["y"],
                    "width": widget_size["width"],
                    "height": widget_size["height"]
                },
                config=widget_config,
                style=widget_style,
                data_source=f"sensor_data/{sensor_id}",
                update_interval=update_interval,
                thresholds=thresholds,
                created_at=datetime.now()
            )
            
            return widget
            
        except Exception as e:
            logger.error(f"❌ Failed to create widget: {e}")
            return None
    
    async def create_widget_config(self, widget_type: WidgetType, sensor_profile: Dict, 
                                 dashboard_config: Dict) -> Dict[str, Any]:
        """Create configuration for a specific widget type."""
        base_config = {
            "sensor_id": sensor_profile["sensor_id"],
            "units": sensor_profile["units"],
            "precision": dashboard_config.get("precision", 2),
            "show_timestamp": True,
            "show_quality": True
        }
        
        # Widget-specific configurations
        if widget_type == WidgetType.GAUGE:
            base_config.update({
                "min_value": dashboard_config.get("min_value", sensor_profile.get("range_min", 0)),
                "max_value": dashboard_config.get("max_value", sensor_profile.get("range_max", 100)),
                "segments": [
                    {"from": 0, "to": 70, "color": "#10b981"},
                    {"from": 70, "to": 85, "color": "#f59e0b"},
                    {"from": 85, "to": 100, "color": "#ef4444"}
                ],
                "needle_color": "#1f2937",
                "show_value": True,
                "show_units": True
            })
        
        elif widget_type == WidgetType.LINE_CHART:
            base_config.update({
                "time_window": dashboard_config.get("trend_window", 300),
                "show_points": False,
                "line_width": 2,
                "fill_area": False,
                "show_grid": True,
                "show_legend": True,
                "y_axis_title": f"{sensor_profile['name']} ({sensor_profile['units']})"
            })
        
        elif widget_type == WidgetType.THERMOMETER:
            base_config.update({
                "min_temp": dashboard_config.get("min_value", -50),
                "max_temp": dashboard_config.get("max_value", 200),
                "scale": "celsius",
                "show_scale": True,
                "bulb_color": "#ef4444",
                "mercury_color": "#dc2626"
            })
        
        elif widget_type == WidgetType.BOOLEAN_INDICATOR:
            base_config.update({
                "true_label": "ON",
                "false_label": "OFF",
                "true_color": "#10b981",
                "false_color": "#6b7280",
                "blink_on_change": True,
                "show_timestamp": True
            })
        
        elif widget_type == WidgetType.NUMERIC_DISPLAY:
            base_config.update({
                "font_size": "large",
                "show_trend_arrow": True,
                "show_change_percent": True,
                "format": "decimal"
            })
        
        elif widget_type == WidgetType.ALARM_PANEL:
            base_config.update({
                "show_active_alarms": True,
                "show_alarm_history": True,
                "max_history_items": 10,
                "enable_acknowledgment": True,
                "alarm_colors": {
                    "normal": "#10b981",
                    "warning": "#f59e0b",
                    "alarm": "#ef4444"
                }
            })
        
        return base_config
    
    def create_widget_style(self, widget_type: WidgetType, sensor_profile: Dict, 
                          dashboard_type: DashboardType) -> Dict[str, str]:
        """Create style configuration for widget."""
        theme = self.config["themes"]["industrial" if dashboard_type != DashboardType.ALARM else "dark"]
        
        base_style = {
            "background_color": theme["background_color"],
            "text_color": theme["text_color"],
            "border_color": theme["secondary_color"],
            "border_width": "1px",
            "border_radius": "8px",
            "font_family": theme["font_family"],
            "padding": "10px"
        }
        
        # Widget-specific styling
        sensor_type = sensor_profile.get("sensor_type", "unknown")
        dashboard_config = sensor_profile.get("dashboard_config", {})
        
        if "color" in dashboard_config:
            base_style["accent_color"] = dashboard_config["color"]
        elif sensor_type == "current_4_20ma":
            base_style["accent_color"] = "#3b82f6"
        elif sensor_type == "temperature_rtd":
            base_style["accent_color"] = "#ef4444"
        elif sensor_type == "pressure_gauge":
            base_style["accent_color"] = "#10b981"
        else:
            base_style["accent_color"] = theme["accent_color"]
        
        return base_style
    
    def get_update_interval(self, sensor_profile: Dict, dashboard_type: DashboardType) -> int:
        """Determine update interval for widget."""
        sensor_sample_rate = sensor_profile.get("sample_rate", 1)
        
        # Base interval from sensor sample rate
        base_interval = max(1000 // sensor_sample_rate, 1000)  # At least 1 second
        
        # Adjust for dashboard type
        if dashboard_type == DashboardType.OVERVIEW:
            return base_interval * 2  # Slower for overview
        elif dashboard_type == DashboardType.ALARM:
            return base_interval // 2  # Faster for alarms
        elif dashboard_type == DashboardType.MOBILE:
            return base_interval * 3  # Slower for mobile to save battery
        else:
            return base_interval
    
    def create_widget_thresholds(self, safety_limits: Dict) -> Dict[str, float]:
        """Create widget thresholds from safety limits."""
        return {
            "warning_low": safety_limits.get("warning_low", float('-inf')),
            "warning_high": safety_limits.get("warning_high", float('inf')),
            "alarm_low": safety_limits.get("alarm_low", float('-inf')),
            "alarm_high": safety_limits.get("alarm_high", float('inf'))
        }
    
    def create_layout_config(self, dashboard_type: DashboardType, widget_count: int) -> Dict[str, Any]:
        """Create layout configuration for dashboard."""
        base_layout = self.config["layouts"]["overview"].copy()
        
        # Adjust layout based on dashboard type
        if dashboard_type == DashboardType.MOBILE:
            base_layout.update({
                "grid_columns": 6,
                "grid_rows": widget_count * 2,
                "widget_margin": 5,
                "compact_mode": True
            })
        elif dashboard_type == DashboardType.DETAILED:
            base_layout.update({
                "grid_columns": 12,
                "grid_rows": widget_count * 3,
                "widget_margin": 15,
                "show_toolbar": True
            })
        elif dashboard_type == DashboardType.ALARM:
            base_layout.update({
                "grid_columns": 8,
                "grid_rows": 6,
                "widget_margin": 5,
                "auto_refresh": True,
                "refresh_interval": 5000
            })
        
        return base_layout
    
    def create_responsive_config(self, dashboard_type: DashboardType) -> Dict[str, Any]:
        """Create responsive configuration for dashboard."""
        return {
            "enable_responsive": True,
            "breakpoints": self.config["layouts"]["overview"]["responsive_breakpoints"],
            "mobile_adjustments": {
                "stack_widgets": dashboard_type != DashboardType.MOBILE,
                "hide_secondary_widgets": dashboard_type == DashboardType.OVERVIEW,
                "reduce_widget_size": True
            },
            "tablet_adjustments": {
                "reduce_margins": True,
                "compact_titles": True
            }
        }
    
    def get_dashboard_title(self, dashboard_type: DashboardType) -> str:
        """Get title for dashboard type."""
        titles = {
            DashboardType.OVERVIEW: "CT-087 Sensor Overview",
            DashboardType.DETAILED: "CT-087 Detailed Monitoring",
            DashboardType.MOBILE: "CT-087 Mobile View",
            DashboardType.PROCESS: "CT-087 Process Dashboard",
            DashboardType.ALARM: "CT-087 Alarm Panel",
            DashboardType.TREND: "CT-087 Trend Analysis"
        }
        return titles.get(dashboard_type, "CT-087 Dashboard")
    
    def get_dashboard_description(self, dashboard_type: DashboardType) -> str:
        """Get description for dashboard type."""
        descriptions = {
            DashboardType.OVERVIEW: "High-level view of all detected sensors with key metrics",
            DashboardType.DETAILED: "Comprehensive monitoring with detailed charts and controls",
            DashboardType.MOBILE: "Mobile-optimized view for field operations",
            DashboardType.PROCESS: "Process-focused dashboard for operations",
            DashboardType.ALARM: "Real-time alarm monitoring and management",
            DashboardType.TREND: "Historical trends and predictive analytics"
        }
        return descriptions.get(dashboard_type, "Auto-generated sensor dashboard")
    
    async def generate_node_red_flows(self) -> List[Dict]:
        """Generate Node-RED flows for the dashboards."""
        logger.info("🔄 Generating Node-RED flows for dashboards...")
        
        flows = []
        
        for dashboard_id, dashboard in self.generated_dashboards.items():
            try:
                flow = await self.create_node_red_flow(dashboard)
                if flow:
                    flows.append(flow)
                    logger.info(f"✅ Generated Node-RED flow for {dashboard_id}")
            except Exception as e:
                logger.error(f"❌ Failed to generate Node-RED flow for {dashboard_id}: {e}")
        
        # Save flows
        await self.save_node_red_flows(flows)
        
        return flows
    
    async def create_node_red_flow(self, dashboard: DashboardLayout) -> Optional[Dict]:
        """Create Node-RED flow for a dashboard."""
        try:
            flow_id = f"flow_{dashboard.dashboard_id}"
            
            flow = {
                "id": flow_id,
                "label": dashboard.title,
                "disabled": False,
                "info": dashboard.description,
                "nodes": [],
                "configs": []
            }
            
            # Create nodes for each widget
            node_y = 100
            
            for widget in dashboard.widgets:
                # Input node (sensor data)
                input_node = {
                    "id": f"input_{widget.widget_id}",
                    "type": "inject",
                    "z": flow_id,
                    "name": f"Sensor {widget.sensor_id}",
                    "props": [
                        {"p": "payload", "v": "0", "vt": "num"},
                        {"p": "topic", "v": widget.sensor_id, "vt": "str"}
                    ],
                    "repeat": str(widget.update_interval / 1000),
                    "crontab": "",
                    "once": True,
                    "x": 100,
                    "y": node_y,
                    "wires": [[f"ui_{widget.widget_id}"]]
                }
                
                # UI node (dashboard widget)
                ui_node = self.create_ui_node(widget, flow_id, node_y)
                
                flow["nodes"].extend([input_node, ui_node])
                node_y += 80
            
            return flow
            
        except Exception as e:
            logger.error(f"❌ Failed to create Node-RED flow: {e}")
            return None
    
    def create_ui_node(self, widget: DashboardWidget, flow_id: str, y_position: int) -> Dict:
        """Create Node-RED UI node for widget."""
        base_node = {
            "id": f"ui_{widget.widget_id}",
            "type": "ui_gauge",  # Default, will be overridden
            "z": flow_id,
            "name": widget.title,
            "group": "default_group",
            "order": 0,
            "width": widget.position["width"],
            "height": widget.position["height"],
            "x": 300,
            "y": y_position,
            "wires": []
        }
        
        # Configure based on widget type
        if widget.widget_type == WidgetType.GAUGE:
            base_node.update({
                "type": "ui_gauge",
                "min": widget.config.get("min_value", 0),
                "max": widget.config.get("max_value", 100),
                "seg1": widget.thresholds.get("warning_low", 70),
                "seg2": widget.thresholds.get("alarm_low", 85),
                "unit": widget.config.get("units", ""),
                "format": "{{value}}",
                "gtype": "gage"
            })
        
        elif widget.widget_type == WidgetType.LINE_CHART:
            base_node.update({
                "type": "ui_chart",
                "interpolate": "linear",
                "nodata": "No Data",
                "dot": False,
                "ymin": "",
                "ymax": "",
                "removeOlder": widget.config.get("time_window", 300),
                "removeOlderPoints": "",
                "removeOlderUnit": "1",
                "cutout": 0,
                "useOneColor": False,
                "useUTC": False,
                "colors": ["#1f77b4", "#ff7f0e", "#2ca02c"],
                "outputs": 1,
                "useDifferentColor": False
            })
        
        elif widget.widget_type == WidgetType.BOOLEAN_INDICATOR:
            base_node.update({
                "type": "ui_led",
                "colorForValue": [
                    {"color": widget.style.get("accent_color", "#10b981"), "value": "true", "valueType": "bool"},
                    {"color": "#6b7280", "value": "false", "valueType": "bool"}
                ],
                "allowColorForValueInMessage": False
            })
        
        elif widget.widget_type == WidgetType.NUMERIC_DISPLAY:
            base_node.update({
                "type": "ui_text",
                "format": "{{msg.payload}} " + widget.config.get("units", ""),
                "layout": "row-spread",
                "style": False,
                "font": "",
                "fontSize": widget.config.get("font_size", "large"),
                "color": widget.style.get("text_color", "#000000"),
                "className": ""
            })
        
        return base_node
    
    async def save_dashboards(self, dashboards: List[DashboardLayout]):
        """Save generated dashboards for other agents."""
        try:
            # Prepare dashboard data
            dashboard_data = {
                "dashboards": [asdict(dashboard) for dashboard in dashboards],
                "generated_by": "ct-087-agent-2",
                "generated_at": datetime.now().isoformat(),
                "total_dashboards": len(dashboards),
                "sensor_count": len(self.sensor_profiles)
            }
            
            # Save to JSON file for Agent 3/4
            output_path = "/tmp/ct-087-dashboard-layouts.json"
            with open(output_path, 'w') as f:
                json.dump(dashboard_data, f, indent=2, default=str)
            
            logger.info(f"✅ Dashboard layouts saved to {output_path}")
            
            # Save coordination completion
            coordination_path = "/tmp/ct-087-agent2-completion.json"
            with open(coordination_path, 'w') as f:
                json.dump({
                    "agent": "ct-087-agent-2",
                    "status": "completed",
                    "output_file": output_path,
                    "dashboards_generated": len(dashboards),
                    "completion_time": datetime.now().isoformat()
                }, f, indent=2)
            
        except Exception as e:
            logger.error(f"❌ Failed to save dashboards: {e}")
    
    async def save_node_red_flows(self, flows: List[Dict]):
        """Save Node-RED flows."""
        try:
            output_path = "/tmp/ct-087-node-red-flows.json"
            with open(output_path, 'w') as f:
                json.dump(flows, f, indent=2)
            
            logger.info(f"✅ Node-RED flows saved to {output_path}")
            
        except Exception as e:
            logger.error(f"❌ Failed to save Node-RED flows: {e}")

# ADK Coordination
async def main():
    """Main execution for CT-087 Agent 2."""
    logger.info("🎨 CT-087 Agent 2 Auto Dashboard Generator Starting...")
    
    # Initialize generator
    generator = AutoDashboardGenerator()
    
    # Generate all dashboards
    dashboards = await generator.generate_all_dashboards()
    
    if dashboards:
        # Generate Node-RED flows
        flows = await generator.generate_node_red_flows()
        
        logger.info(f"✅ Agent 2 Complete: {len(dashboards)} dashboards and {len(flows)} Node-RED flows generated")
        logger.info("🔄 Ready for Agent 3 (Multi-Sensor Integration) and Agent 4 (Professional Dashboard)")
    else:
        logger.warning("⚠️  No dashboards generated")
    
    return dashboards

if __name__ == "__main__":
    asyncio.run(main())