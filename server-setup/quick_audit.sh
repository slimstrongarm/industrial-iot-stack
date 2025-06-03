#!/bin/bash
# Quick Server Audit Script

echo "🔍 ================================"
echo "   Server Services Audit"
echo "   $(date)"
echo "================================"
echo ""

echo "📊 EXISTING SERVICES CHECK:"
echo "---------------------------"

# Check for running Docker containers
echo "🐳 Docker Containers:"
docker ps -a --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" 2>/dev/null || echo "Docker not accessible"
echo ""

# Check for Node-RED
echo "🔴 Node-RED Status:"
if docker ps | grep -i node-red > /dev/null 2>&1; then
    echo "✅ Node-RED container found running"
    docker ps | grep -i node-red
else
    echo "📍 Checking for Node-RED on host..."
    ps aux | grep -i node-red | grep -v grep || echo "No Node-RED process found"
fi
curl -s http://localhost:1880 > /dev/null 2>&1 && echo "✅ Node-RED responding on :1880" || echo "❌ No response on :1880"
echo ""

# Check for Ignition
echo "🔥 Ignition Status:"
if docker ps | grep -i ignition > /dev/null 2>&1; then
    echo "✅ Ignition container found running"
    docker ps | grep -i ignition
else
    echo "📍 Checking for Ignition on host..."
    ps aux | grep -i ignition | grep -v grep || echo "No Ignition process found"
fi
curl -s http://localhost:8088/StatusPing > /dev/null 2>&1 && echo "✅ Ignition responding on :8088" || echo "❌ No response on :8088"
curl -s http://localhost:8043/StatusPing > /dev/null 2>&1 && echo "✅ Ignition Edge responding on :8043" || echo "❌ No response on :8043"
echo ""

# Check for databases
echo "🗄️ Database Status:"
echo "PostgreSQL:"
netstat -an | grep :5432 > /dev/null 2>&1 && echo "✅ PostgreSQL listening on :5432" || echo "❌ PostgreSQL not found on :5432"
echo "MySQL:"
netstat -an | grep :3306 > /dev/null 2>&1 && echo "✅ MySQL listening on :3306" || echo "❌ MySQL not found on :3306"
echo ""

# Check all listening ports
echo "🌐 All Listening Services:"
netstat -tlnp 2>/dev/null | grep LISTEN | head -20 || ss -tlnp 2>/dev/null | head -20 || echo "Cannot list ports"
echo ""

# Check Docker images available
echo "💾 Docker Images Available:"
docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}" 2>/dev/null | head -15 || echo "Cannot list images"
echo ""

# Check for Ignition installation
echo "📁 Ignition Installation Check:"
if [ -d "/usr/local/bin/ignition" ]; then
    echo "✅ Found Ignition in /usr/local/bin/ignition"
    ls -la /usr/local/bin/ignition/
elif [ -d "/opt/ignition" ]; then
    echo "✅ Found Ignition in /opt/ignition"
    ls -la /opt/ignition/
else
    echo "❌ No standard Ignition installation found"
fi
echo ""

echo "🎯 RECOMMENDATIONS FOR DEMO:"
echo "1. Use existing services if available"
echo "2. Configure Ignition Edge for POC"
echo "3. Ensure MQTT broker is running"
echo "4. Set up data flow: Edge → MQTT → Gateway"
echo ""