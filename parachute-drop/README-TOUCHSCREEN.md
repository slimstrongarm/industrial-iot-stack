# 🍺 Pi 7" Touchscreen Dashboard for Brewery Demo

## 🎯 Overview

This creates a beautiful, professional touchscreen dashboard for your Raspberry Pi that displays real-time Phidget sensor data. Perfect for brewery demos with a "wow factor" presentation.

## 📦 What's Included

- **Professional brewery-themed dashboard** with custom CSS
- **Large, touch-friendly gauges** for temperature and humidity
- **Real-time trend charts** showing live data
- **Alarm thresholds** with visual indicators
- **Auto-launch in fullscreen** for demo mode
- **Test data generator** when sensors aren't connected

## 🚀 Quick Setup

### 1. Copy Files to Pi
```bash
# Copy the flow and setup script to your Pi
scp pi-touchscreen-flow.json pi@your-pi-ip:~/
scp pi-touchscreen-setup.sh pi@your-pi-ip:~/
```

### 2. Run Setup Script
```bash
ssh pi@your-pi-ip
chmod +x pi-touchscreen-setup.sh
./pi-touchscreen-setup.sh
```

### 3. Import Dashboard Flow
```bash
# Import the touchscreen dashboard
curl -X POST -H "Content-Type: application/json" \
     -d @pi-touchscreen-flow.json \
     http://localhost:1880/flows
```

### 4. Restart Pi
```bash
sudo reboot
```

## 📱 Dashboard Features

### Main Display Elements:
- **🌡️ Temperature Gauge**: Large circular gauge (0-40°C)
- **💧 Humidity Gauge**: Wave-style gauge (0-100%RH)
- **📊 Live Charts**: Real-time trending for both sensors
- **🚨 Status Header**: System status with alarm indicators
- **📈 Data History**: Keeps last 100 data points

### Visual Indicators:
- **🟢 Green**: Normal operation
- **🟡 Yellow**: Warning thresholds
- **🔴 Red**: Alarm conditions

### Alarm Thresholds:
- **Temperature**: 15-30°C (normal), outside = warning/alarm
- **Humidity**: 30-80%RH (normal), outside = warning/alarm

## 🔧 Customization

### Change Location/Branding:
Edit the flow's function nodes to change:
- Location name (currently "Demo Tank")
- Company branding
- Alarm thresholds
- Color scheme

### Modify CSS Styling:
Edit `~/.node-red/static/css/brewery-dashboard.css` for:
- Colors and fonts
- Gauge sizes
- Layout adjustments
- Touch button sizes

### Add More Sensors:
The flow is designed to easily add:
- Current sensors (for motor monitoring)
- Pressure sensors
- Digital inputs
- Additional temperature zones

## 📊 Using with Real Phidget Sensors

### Replace Test Data:
1. Remove or disable the "Generate Test Data" function
2. Connect your Phidget temperature/humidity sensor
3. Update the Phidget node configuration with your device serial number
4. Deploy the flow

### Sensor Configuration:
- **Hub Port**: Set to match your Phidget VINT hub port
- **Data Interval**: Currently 1000ms (1 second updates)
- **Change Triggers**: Temperature 0.1°C, Humidity 0.5%RH

## 🎪 Demo Mode Features

### Auto-Launch:
- Dashboard automatically launches in fullscreen after Pi boot
- No mouse cursor visible (hides after 5 seconds)
- Professional kiosk-style presentation

### Test Data:
- Generates realistic brewery data when sensors not connected
- Temperature varies around 22.5°C
- Humidity varies around 65%RH
- Updates every 5 seconds

### Manual Control:
```bash
# Start demo manually
~/start-brewery-demo.sh

# Access Node-RED editor
# Open browser to: http://pi-ip:1880

# Access dashboard
# Open browser to: http://pi-ip:1880/ui
```

## 🔍 Troubleshooting

### Dashboard Not Loading:
```bash
# Check Node-RED status
sudo systemctl status nodered

# Restart Node-RED
sudo systemctl restart nodered

# Check logs
journalctl -u nodered -f
```

### Phidget Not Connecting:
```bash
# Check Phidget libraries
sudo apt install libphidget22

# List connected Phidgets
sudo phidget22admin

# Check hub status in Node-RED debug panel
```

### Touch Not Working:
```bash
# Install touchscreen drivers
sudo apt install xserver-xorg-input-evdev

# Calibrate if needed
sudo apt install xinput-calibrator
```

## 📏 Display Specifications

**Optimized for:**
- **Screen Size**: 7" (800x480 resolution)
- **Orientation**: Landscape
- **Touch**: Capacitive or resistive
- **Viewing Distance**: 2-3 feet (demo table setup)

**Layout:**
- **Header**: System status (full width)
- **Left Side**: Temperature gauge and display
- **Right Side**: Humidity gauge and display  
- **Bottom**: Live trend charts (dual charts)

## 🎯 Demo Script

### For Client Presentation:

1. **"Let me show you our instant monitoring system"**
   - Point to professional dashboard
   - Show real-time temperature updating

2. **"This is live sensor data from your equipment"**
   - Touch the screen to show interactivity
   - Point out trend charts

3. **"Watch what happens when conditions go out of range"**
   - Demonstrate alarm states (if using test data)
   - Show color changes and status updates

4. **"This is running on a $50 Raspberry Pi"**
   - Point out the small device
   - Emphasize cost-effectiveness

5. **"Imagine this data feeding into your main control system"**
   - Discuss integration possibilities
   - Show the bigger picture

## 🚀 Next Steps

This touchscreen interface can be:
- **Connected to MQTT** for data sharing
- **Integrated with Ignition** for SCADA systems
- **Enhanced with more sensors** for complete monitoring
- **Networked with other Pi units** for multi-zone monitoring
- **Connected to cloud platforms** for remote access

Perfect foundation for scaling up to a complete industrial IoT solution!

---

*🪂 Ready for your brewery parachute drop demo!*