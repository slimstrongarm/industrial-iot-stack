#!/bin/bash
# 🪂 PARACHUTE DROP - Complete Pi Image Builder
# CT-084: Industrial Discovery Agent Implementation
# Creates production-ready Pi image for rapid deployment

echo "🪂 PARACHUTE DROP - Building Complete Pi Image..."
echo "=================================================="
echo "CT-084: Industrial Discovery Agent Implementation"
echo "Creating production-ready deployment image..."
echo ""

# Configuration
PI_IMAGE_NAME="parachute-drop-v1"
BUILD_DIR="/tmp/parachute-build"
MOUNT_POINT="/tmp/pi-mount"

# Create build directory
mkdir -p $BUILD_DIR
cd $BUILD_DIR

echo "📥 Downloading base Raspberry Pi OS..."
# Download latest Raspberry Pi OS Lite
wget -O raspios-lite.img.xz https://downloads.raspberrypi.org/raspios_lite_armhf/images/raspios_lite_armhf-2024-03-15/2024-03-15-raspios-lite-armhf.img.xz

echo "📦 Extracting image..."
unxz raspios-lite.img.xz

echo "🔧 Mounting image for customization..."
# Create loop device and mount
sudo losetup -P /dev/loop0 raspios-lite.img
sudo mkdir -p $MOUNT_POINT
sudo mount /dev/loop0p2 $MOUNT_POINT
sudo mount /dev/loop0p1 $MOUNT_POINT/boot

echo "⚙️ Configuring system basics..."
# Enable SSH
sudo touch $MOUNT_POINT/boot/ssh

# Configure WiFi (will be overridden by portable router)
cat > wifi_config.txt << 'EOF'
country=US
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1

network={
    ssid="ParachuteDrop-Setup"
    psk="Industrial2024!"
}
EOF
sudo cp wifi_config.txt $MOUNT_POINT/boot/wpa_supplicant.conf

# Set hostname
echo "parachute-drop" | sudo tee $MOUNT_POINT/etc/hostname

echo "🐍 Installing Python dependencies..."
# Prepare package installation script
cat > install_packages.sh << 'EOF'
#!/bin/bash
# Run this script in chroot environment

# Update package lists
apt-get update

# Install base packages
apt-get install -y python3-pip nodejs npm git curl wget

# Install Node-RED
bash <(curl -sL https://raw.githubusercontent.com/node-red/linux-installers/master/deb/update-nodejs-and-nodered) --confirm-install

# Enable Node-RED service
systemctl enable nodered.service

# Install EMQX
wget https://www.emqx.io/downloads/broker/v5.0.0/emqx-5.0.0-ubuntu20.04-arm64.deb
dpkg -i emqx-5.0.0-ubuntu20.04-arm64.deb || apt-get install -f -y
systemctl enable emqx

# Install Phidget libraries
wget -qO- https://www.phidgets.com/downloads/setup_linux | bash
apt-get install -y libphidget22

# Install Python packages for discovery
pip3 install paho-mqtt requests scapy nmap python-nmap pymodbus minimalmodbus

# Install touchscreen packages
apt-get install -y xinit chromium-browser unclutter

# Clean up
apt-get autoremove -y
apt-get clean
EOF

# Copy and execute in chroot
sudo cp install_packages.sh $MOUNT_POINT/tmp/
sudo chmod +x $MOUNT_POINT/tmp/install_packages.sh
sudo chroot $MOUNT_POINT /tmp/install_packages.sh

echo "🔍 Installing discovery agents..."
# Copy discovery agent files
sudo mkdir -p $MOUNT_POINT/home/pi/parachute_drop
sudo cp ../parachute-drop/discovery-agent.py $MOUNT_POINT/home/pi/parachute_drop/
sudo cp ../parachute-drop/serial-modbus-interface.py $MOUNT_POINT/home/pi/parachute_drop/
sudo cp ../parachute-drop/phidget-sensor-config.json $MOUNT_POINT/home/pi/parachute_drop/

echo "📊 Installing Node-RED flows..."
# Copy Node-RED flows
sudo mkdir -p $MOUNT_POINT/home/pi/.node-red
sudo cp ../parachute-drop/node-red-touchscreen-flow.json $MOUNT_POINT/home/pi/.node-red/flows.json

# Install Node-RED packages
cat > node_red_packages.sh << 'EOF'
#!/bin/bash
cd /home/pi/.node-red
npm install node-red-dashboard
npm install node-red-contrib-ui-svg
npm install node-red-contrib-phidget22
npm install node-red-contrib-modbus
npm install node-red-node-serialport
EOF

sudo cp node_red_packages.sh $MOUNT_POINT/tmp/
sudo chmod +x $MOUNT_POINT/tmp/node_red_packages.sh
sudo chroot $MOUNT_POINT /tmp/node_red_packages.sh

echo "🚀 Setting up auto-start services..."
# Create discovery service
cat > discovery_service.txt << 'EOF'
[Unit]
Description=Parachute Drop Discovery Agent
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/parachute_drop
ExecStart=/usr/bin/python3 /home/pi/parachute_drop/discovery-agent.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

sudo cp discovery_service.txt $MOUNT_POINT/etc/systemd/system/parachute-discovery.service

# Create touchscreen dashboard service
cat > dashboard_service.txt << 'EOF'
[Unit]
Description=Parachute Drop Dashboard
After=graphical.target

[Service]
Type=simple
User=pi
Environment=DISPLAY=:0
ExecStart=/bin/bash -c "sleep 30 && unclutter -idle 0.5 -root & chromium-browser --noerrdialogs --disable-infobars --kiosk http://localhost:1880/ui"
Restart=always
RestartSec=30

[Install]
WantedBy=graphical.target
EOF

sudo cp dashboard_service.txt $MOUNT_POINT/etc/systemd/system/parachute-dashboard.service

echo "⚡ Enabling services..."
sudo chroot $MOUNT_POINT systemctl enable parachute-discovery.service
sudo chroot $MOUNT_POINT systemctl enable parachute-dashboard.service

echo "🔧 Final configuration..."
# Set permissions
sudo chown -R 1000:1000 $MOUNT_POINT/home/pi/parachute_drop
sudo chown -R 1000:1000 $MOUNT_POINT/home/pi/.node-red

# Create startup script
cat > startup_script.txt << 'EOF'
#!/bin/bash
# Parachute Drop startup script

echo "🪂 PARACHUTE DROP INITIALIZING..."

# Wait for network
sleep 10

# Start discovery agent if not running
systemctl is-active --quiet parachute-discovery || systemctl start parachute-discovery

# Ensure Node-RED is running
systemctl is-active --quiet nodered || systemctl start nodered

# Ensure EMQX is running  
systemctl is-active --quiet emqx || systemctl start emqx

# Wait for services to be ready
sleep 20

# Start dashboard if display available
if [ "$DISPLAY" != "" ]; then
    systemctl is-active --quiet parachute-dashboard || systemctl start parachute-dashboard
fi

echo "✅ PARACHUTE DROP READY!"
echo "Dashboard: http://localhost:1880/ui"
echo "Discovery: Running in background"
echo "MQTT: localhost:1883"
EOF

sudo cp startup_script.txt $MOUNT_POINT/home/pi/parachute_startup.sh
sudo chmod +x $MOUNT_POINT/home/pi/parachute_startup.sh

# Add to .bashrc for auto-start
echo "/home/pi/parachute_startup.sh" | sudo tee -a $MOUNT_POINT/home/pi/.bashrc

echo "💾 Creating final image..."
# Unmount and clean up
sudo umount $MOUNT_POINT/boot
sudo umount $MOUNT_POINT
sudo losetup -d /dev/loop0

# Compress final image
echo "🗜️ Compressing image..."
xz -z -9 raspios-lite.img
mv raspios-lite.img.xz ${PI_IMAGE_NAME}.img.xz

echo "✅ PARACHUTE DROP PI IMAGE COMPLETE!"
echo ""
echo "📋 Image Details:"
echo "   File: ${PI_IMAGE_NAME}.img.xz"
echo "   Size: $(du -h ${PI_IMAGE_NAME}.img.xz | cut -f1)"
echo "   Location: $(pwd)/${PI_IMAGE_NAME}.img.xz"
echo ""
echo "🚀 Flash Instructions:"
echo "   sudo dd if=${PI_IMAGE_NAME}.img.xz | unxz | dd of=/dev/sdX bs=4M status=progress"
echo ""
echo "🎯 First Boot:"
echo "   1. Pi auto-starts discovery and dashboard"
echo "   2. Connect to WiFi 'ParachuteDrop-Setup'"
echo "   3. Access dashboard at http://parachute-drop.local:1880/ui"
echo "   4. Deploy sensors and watch magic happen!"
echo ""
echo "📊 What's Included:"
echo "   ✅ Node-RED with industrial dashboard"
echo "   ✅ EMQX MQTT broker"
echo "   ✅ Phidget sensor support"
echo "   ✅ Network discovery agent"
echo "   ✅ Serial/Modbus interface"
echo "   ✅ Auto-start touchscreen UI"
echo "   ✅ All Python dependencies"
echo ""
echo "🪂 Ready for industrial deployment!"