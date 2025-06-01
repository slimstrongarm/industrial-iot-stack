#!/bin/bash
# Server Docker Audit Script
# Run this on your server to understand existing Docker setup before deployment

echo "=== Docker Environment Audit ==="
echo "Generated: $(date)"
echo "================================"

echo -e "\n📋 Docker Version & Info:"
docker --version
docker compose version 2>/dev/null || docker-compose --version

echo -e "\n🏃 Running Containers:"
docker ps --format "table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}"

echo -e "\n💾 All Containers (including stopped):"
docker ps -a --format "table {{.Names}}\t{{.Image}}\t{{.Status}}"

echo -e "\n🖼️ Docker Images:"
docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}"

echo -e "\n📁 Docker Volumes:"
docker volume ls

echo -e "\n🌐 Docker Networks:"
docker network ls

echo -e "\n💽 Disk Usage:"
docker system df

echo -e "\n📂 Docker Compose Projects (if any):"
find / -name "docker-compose.yml" -o -name "docker-compose.yaml" 2>/dev/null | head -20

echo -e "\n🔍 Port Usage (potential conflicts):"
echo "Checking common IoT stack ports..."
for port in 8088 1880 1883 62541 3000 9090; do
    if lsof -i :$port >/dev/null 2>&1; then
        echo "⚠️  Port $port is in use:"
        lsof -i :$port | grep LISTEN
    else
        echo "✅ Port $port is available"
    fi
done

echo -e "\n📊 System Resources:"
echo "CPU: $(nproc) cores"
echo "Memory: $(free -h | grep Mem | awk '{print $2}') total, $(free -h | grep Mem | awk '{print $3}') used"
echo "Disk: $(df -h /var/lib/docker | tail -1 | awk '{print $4}') available in /var/lib/docker"

echo -e "\n🔐 Docker Permissions:"
groups | grep -q docker && echo "✅ Current user is in docker group" || echo "⚠️  Current user NOT in docker group"

echo -e "\n📍 Suggested deployment directory:"
if [ -d "/opt/industrial-iot-stack" ]; then
    echo "⚠️  /opt/industrial-iot-stack already exists:"
    ls -la /opt/industrial-iot-stack
else
    echo "✅ /opt/industrial-iot-stack is available for deployment"
fi

echo -e "\n=== End of Audit ==="