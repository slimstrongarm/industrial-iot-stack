#!/bin/bash
# Pi 7" Touchscreen Setup for Brewery Demo
# Sets up Node-RED with dashboard optimized for 7" display

echo "🪂 Setting up Pi Touchscreen for Brewery Demo"
echo "=============================================="

# Update system
echo "📦 Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install Node-RED dashboard if not already installed
echo "📊 Installing Node-RED Dashboard..."
cd ~/.node-red
npm install node-red-dashboard
npm install node-red-contrib-phidget22

# Install additional useful nodes
npm install node-red-contrib-ui-led
npm install node-red-contrib-ui-level
npm install node-red-contrib-moment

# Create custom CSS for 7" display
echo "🎨 Creating custom dashboard CSS..."
mkdir -p ~/.node-red/static/css
cat > ~/.node-red/static/css/brewery-dashboard.css << 'EOF'
/* Custom CSS for 7" Touchscreen Dashboard */

/* Make everything bigger for touch */
.nr-dashboard-text {
    font-size: 18px !important;
}

.nr-dashboard-button {
    height: 60px !important;
    font-size: 20px !important;
}

/* Big gauges for easy viewing */
.big-gauge .nr-dashboard-gauge {
    min-height: 300px !important;
}

/* Large displays */
.big-display .nr-dashboard-text {
    font-size: 48px !important;
    font-weight: bold !important;
}

/* Header styling */
.header-status {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    color: white !important;
    border-radius: 10px !important;
    margin: 5px !important;
}

/* Status indicators */
.status-normal { color: #48BB78 !important; }
.status-warning { color: #ED8936 !important; }
.status-alarm { color: #F56565 !important; }

/* Chart styling */
.live-chart {
    border-radius: 8px !important;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
}

/* Remove unnecessary padding for 7" screen */
.nr-dashboard-cardpanel {
    padding: 8px !important;
}

.nr-dashboard-cardcontainer {
    margin: 4px !important;
}

/* Make tabs bigger for touch */
.md-tab {
    min-height: 60px !important;
    font-size: 18px !important;
}

/* Optimize for landscape 7" (800x480) */
@media (max-width: 800px) {
    .nr-dashboard-template {
        font-size: 16px !important;
    }
    
    .nr-dashboard-gauge svg {
        height: 200px !important;
    }
}

/* Full screen mode optimizations */
body.nr-dashboard-fullscreen {
    overflow: hidden !important;
}

/* Touch-friendly buttons */
.nr-dashboard-button:hover {
    transform: scale(1.05) !important;
    transition: transform 0.1s !important;
}
EOF

# Configure Node-RED settings for dashboard
echo "⚙️ Configuring Node-RED settings..."
cat >> ~/.node-red/settings.js << 'EOF'

// Dashboard optimizations for Pi touchscreen
module.exports.ui = module.exports.ui || {};
module.exports.ui.path = "ui";
module.exports.ui.middleware = function(req, res, next) { 
    // Add custom CSS
    if (req.url === '/ui') {
        res.setHeader('Cache-Control', 'no-cache');
    }
    next(); 
};

// Serve custom CSS
module.exports.httpStatic = [
    '/home/pi/.node-red/static/',
    '/usr/lib/node_modules/node-red-dashboard/dist/'
];

// Performance optimizations for Pi
module.exports.debugMaxLength = 100;
module.exports.maxNodeRedLogs = 50;

// Function global context for brewery monitoring
module.exports.functionGlobalContext = {
    brewery: {
        location: "Demo Tank",
        alarmThresholds: {
            temperature: { min: 15, max: 30 },
            humidity: { min: 30, max: 80 }
        }
    }
};
EOF

# Set up auto-launch dashboard in fullscreen
echo "🖥️ Setting up auto-launch..."
mkdir -p ~/.config/autostart

cat > ~/.config/autostart/brewery-dashboard.desktop << 'EOF'
[Desktop Entry]
Type=Application
Name=Brewery Dashboard
Comment=Launch brewery monitoring dashboard
Exec=chromium-browser --start-fullscreen --disable-infobars --disable-session-crashed-bubble --disable-translate --kiosk http://localhost:1880/ui
Icon=chromium-browser
Terminal=false
Categories=Network;
StartupNotify=false
EOF

# Configure Pi for optimal touchscreen performance
echo "🎯 Optimizing Pi for touchscreen..."

# Disable screen blanking
sudo sh -c 'echo "xserver-command=X -s 0 -dpms" >> /etc/lightdm/lightdm.conf'

# Hide cursor after 5 seconds of inactivity
sudo apt install -y unclutter
echo "@unclutter -idle 5" >> ~/.config/lxsession/LXDE-pi/autostart

# Install Chromium if not present
sudo apt install -y chromium-browser

# Create startup script for the demo
cat > ~/start-brewery-demo.sh << 'EOF'
#!/bin/bash
echo "🪂 Starting Brewery Demo..."

# Start Node-RED if not running
if ! pgrep -f "node-red" > /dev/null; then
    echo "Starting Node-RED..."
    node-red &
    sleep 10
fi

# Wait for Node-RED to be ready
while ! curl -s http://localhost:1880 > /dev/null; do
    echo "Waiting for Node-RED..."
    sleep 2
done

echo "✅ Node-RED is ready"

# Import the dashboard flow
if [ -f ~/pi-touchscreen-flow.json ]; then
    echo "📊 Importing dashboard flow..."
    curl -X POST -H "Content-Type: application/json" \
         -d @~/pi-touchscreen-flow.json \
         http://localhost:1880/flows
    echo "Dashboard imported!"
fi

# Launch browser in fullscreen
echo "🚀 Launching dashboard..."
chromium-browser --start-fullscreen \
                 --disable-infobars \
                 --disable-session-crashed-bubble \
                 --disable-translate \
                 --kiosk \
                 http://localhost:1880/ui &

echo "🍺 Brewery Demo Ready!"
echo "Dashboard: http://localhost:1880/ui"
echo "Node-RED Editor: http://localhost:1880"
EOF

chmod +x ~/start-brewery-demo.sh

# Enable auto-login (optional)
read -p "Enable auto-login to desktop? (y/n): " auto_login
if [[ $auto_login =~ ^[Yy]$ ]]; then
    sudo raspi-config nonint do_boot_behaviour B4
    echo "Auto-login enabled"
fi

echo ""
echo "✅ Pi Touchscreen Setup Complete!"
echo "=================================="
echo ""
echo "🎯 Next Steps:"
echo "1. Copy pi-touchscreen-flow.json to your Pi home directory"
echo "2. Restart your Pi: sudo reboot"
echo "3. The dashboard will auto-launch in fullscreen"
echo ""
echo "📊 Manual Launch:"
echo "   ~/start-brewery-demo.sh"
echo ""
echo "🌐 Access URLs:"
echo "   Dashboard: http://$(hostname -I | cut -d' ' -f1):1880/ui"
echo "   Node-RED:  http://$(hostname -I | cut -d' ' -f1):1880"
echo ""
echo "📱 The dashboard is optimized for:"
echo "   - 7\" touchscreen (800x480)"
echo "   - Touch-friendly buttons and gauges"
echo "   - Real-time temperature and humidity"
echo "   - Live trend charts"
echo "   - Professional brewery branding"
echo ""
echo "🪂 Ready for Parachute Drop demo!"