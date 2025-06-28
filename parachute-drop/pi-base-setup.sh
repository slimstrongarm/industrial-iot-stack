#!/bin/bash
# 🪂 PARACHUTE DROP - Raspberry Pi Base Setup
# Industrial IoT Rapid Deployment Kit
# Version 1.0 - Foundation Build

echo "🪂 PARACHUTE DROP - Pi Configuration Starting..."
echo "================================================"

# Update system
echo "📦 Updating Raspberry Pi OS..."
sudo apt-get update && sudo apt-get upgrade -y

# Install Node-RED
echo "🔴 Installing Node-RED..."
bash <(curl -sL https://raw.githubusercontent.com/node-red/linux-installers/master/deb/update-nodejs-and-nodered)

# Enable Node-RED service
sudo systemctl enable nodered.service
sudo systemctl start nodered.service

# Install EMQX (Lightweight MQTT Broker)
echo "📡 Installing EMQX..."
wget https://www.emqx.io/downloads/broker/v5.0.0/emqx-5.0.0-ubuntu20.04-arm64.deb
sudo dpkg -i emqx-5.0.0-ubuntu20.04-arm64.deb
sudo systemctl enable emqx
sudo systemctl start emqx

# Install Node-RED Dashboard
echo "📊 Installing Node-RED Dashboard..."
cd ~/.node-red
npm install node-red-dashboard
npm install node-red-contrib-ui-svg
npm install node-red-contrib-phidget22

# Install Phidget drivers
echo "🔌 Installing Phidget22 Libraries..."
wget -qO- https://www.phidgets.com/downloads/setup_linux | sudo bash
sudo apt-get install -y libphidget22

# Configure touchscreen
echo "📱 Configuring Pi Touchscreen..."
sudo apt-get install -y xinit chromium-browser unclutter

# Create auto-start script for touchscreen
cat > ~/start-dashboard.sh << 'EOF'
#!/bin/bash
# Start Node-RED Dashboard on touchscreen
unclutter -idle 0.5 -root &
chromium-browser --noerrdialogs --disable-infobars --kiosk http://localhost:1880/ui &
EOF

chmod +x ~/start-dashboard.sh

# Create EMQX config for secure remote connection
echo "🔐 Configuring EMQX for secure remote access..."
sudo tee /etc/emqx/emqx.conf > /dev/null << 'EOF'
node {
  name = "parachute-drop@127.0.0.1"
}

listeners.tcp.default {
  bind = "0.0.0.0:1883"
}

listeners.ssl.default {
  bind = "0.0.0.0:8883"
  ssl_options {
    certfile = "/etc/emqx/certs/cert.pem"
    keyfile = "/etc/emqx/certs/key.pem"
  }
}

# Authentication
authentication = [
  {
    mechanism = password_based
    backend = built_in_database
  }
]
EOF

echo "✅ Base Pi configuration complete!"
echo ""
echo "📋 Next Steps:"
echo "1. Configure Phidget Hub at http://localhost:8080"
echo "2. Access Node-RED at http://localhost:1880"
echo "3. EMQX Dashboard at http://localhost:18083"
echo "4. Import parachute-drop flows"