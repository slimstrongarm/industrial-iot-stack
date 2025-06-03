#!/bin/bash
# Automated Docker Setup for Industrial IoT Stack
# Run this after SSHing into the server

echo "🚀 Industrial IoT Stack - Docker Setup"
echo "====================================="
echo "This script will set up your Docker environment"
echo ""

# Function to check Docker
check_docker() {
    echo "🔍 Checking Docker installation..."
    if command -v docker &> /dev/null; then
        echo "✅ Docker found: $(docker --version)"
        return 0
    else
        echo "❌ Docker not found in current environment"
        return 1
    fi
}

# Function to check if we're in WSL
check_environment() {
    echo ""
    echo "🌍 Checking environment..."
    if grep -qi microsoft /proc/version 2>/dev/null; then
        echo "✅ Running in WSL"
        echo "Distribution: $(lsb_release -d 2>/dev/null | cut -f2 || cat /etc/os-release | grep PRETTY_NAME | cut -d'"' -f2)"
    elif [[ "$OS" == "Windows_NT" ]]; then
        echo "📍 Running in Windows SSH"
        echo "💡 Entering WSL..."
        wsl
    else
        echo "❓ Unknown environment"
    fi
}

# Main setup function
main_setup() {
    check_environment
    
    if ! check_docker; then
        echo ""
        echo "🔧 Docker not accessible. Trying WSL..."
        echo "Enter your default WSL distro with: wsl"
        echo "Then run this script again"
        exit 1
    fi
    
    echo ""
    echo "📁 Creating project structure..."
    mkdir -p ~/industrial-iot-stack/{data,configs,scripts,logs}
    cd ~/industrial-iot-stack
    
    echo ""
    echo "📥 Creating docker-compose.yml..."
    cat > docker-compose.yml << 'EOF'
version: '3.8'

# Industrial IoT Stack - Core Services
# Phase 1: Essential Services Only

services:
  # PostgreSQL Database
  postgres:
    image: postgres:15-alpine
    container_name: iiot-postgres
    environment:
      POSTGRES_USER: ${POSTGRES_USER:-ignition}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-ignition}
      POSTGRES_DB: ${POSTGRES_DB:-ignition}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ignition"]
      interval: 10s
      timeout: 5s
      retries: 5

  # MQTT Broker
  mqtt:
    image: eclipse-mosquitto:2
    container_name: iiot-mqtt
    ports:
      - "1883:1883"
      - "9001:9001"
    volumes:
      - ./configs/mosquitto:/mosquitto/config
      - mqtt_data:/mosquitto/data
      - mqtt_logs:/mosquitto/log
    restart: unless-stopped

  # Node-RED
  node-red:
    image: nodered/node-red:3.1
    container_name: iiot-node-red
    environment:
      - TZ=America/Chicago
    ports:
      - "1880:1880"
    volumes:
      - node_red_data:/data
    depends_on:
      - mqtt
      - postgres
    restart: unless-stopped

volumes:
  postgres_data:
  mqtt_data:
  mqtt_logs:
  node_red_data:

networks:
  default:
    name: iiot-network
EOF

    echo ""
    echo "🔧 Creating Mosquitto config..."
    mkdir -p configs/mosquitto
    cat > configs/mosquitto/mosquitto.conf << 'EOF'
listener 1883
allow_anonymous true

listener 9001
protocol websockets
allow_anonymous true

persistence true
persistence_location /mosquitto/data/

log_dest file /mosquitto/log/mosquitto.log
log_type all
EOF

    echo ""
    echo "🌐 Creating .env file..."
    cat > .env << 'EOF'
# PostgreSQL Configuration
POSTGRES_USER=ignition
POSTGRES_PASSWORD=SecurePassword123!
POSTGRES_DB=ignition

# MQTT Configuration
MQTT_USER=iiot
MQTT_PASSWORD=SecurePassword123!

# Domain Configuration
DOMAIN=localhost
EOF

    echo ""
    echo "✅ Setup complete! Ready to deploy."
    echo ""
    echo "📋 Next steps:"
    echo "1. Review docker-compose.yml"
    echo "2. Update .env with secure passwords"
    echo "3. Run: docker-compose up -d"
    echo "4. Check status: docker-compose ps"
    echo ""
    echo "🎯 Services will be available at:"
    echo "   - PostgreSQL: localhost:5432"
    echo "   - MQTT: localhost:1883"
    echo "   - Node-RED: http://localhost:1880"
}

# Run main setup
main_setup