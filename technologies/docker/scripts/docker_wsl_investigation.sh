#!/bin/bash
# Docker and WSL Investigation Script

echo "🔍 ============================================"
echo "   Docker & WSL Investigation Report"
echo "   $(date)"
echo "============================================"
echo ""

echo "📊 WSL Status:"
echo "-------------------"
wsl -l -v 2>/dev/null || echo "WSL command not accessible from SSH"
echo ""

echo "🐳 Docker Desktop Status:"
echo "------------------------"
# Check if Docker Desktop is running
tasklist /FI "IMAGENAME eq Docker Desktop.exe" 2>NUL | find /I /N "Docker Desktop.exe" >NUL
if [ $? -eq 0 ]; then
    echo "✅ Docker Desktop is running"
else
    echo "❌ Docker Desktop is not running"
fi

echo ""
echo "🔧 Docker CLI Check:"
echo "-------------------"
# Check if docker CLI is available
if command -v docker &> /dev/null; then
    echo "✅ Docker CLI found"
    docker --version
    echo ""
    echo "Docker Info:"
    docker info 2>&1 | grep -E "Server Version:|Operating System:|Total Memory:|CPUs:" || echo "Docker daemon might not be running"
else
    echo "❌ Docker CLI not found in PATH"
fi

echo ""
echo "🌐 Docker Service Status:"
echo "------------------------"
# Check Windows Docker service
sc query docker 2>/dev/null || echo "Docker service not found as Windows service"

echo ""
echo "📁 WSL Distros Available:"
echo "------------------------"
# List WSL distros from Windows side
wsl --list --verbose 2>/dev/null || powershell.exe -Command "wsl --list --verbose" 2>/dev/null || echo "Cannot list WSL distros"

echo ""
echo "🔌 Docker Contexts:"
echo "------------------"
docker context ls 2>/dev/null || echo "Cannot list Docker contexts"

echo ""
echo "💾 Docker Storage:"
echo "-----------------"
docker system df 2>/dev/null || echo "Cannot check Docker storage"

echo ""
echo "🏃 Running Containers:"
echo "---------------------"
docker ps 2>/dev/null || echo "No containers running or Docker not accessible"

echo ""
echo "📍 Docker Installation Paths:"
echo "----------------------------"
echo "Checking common Docker locations..."
ls -la "/mnt/c/Program Files/Docker/Docker" 2>/dev/null | head -5 || echo "Docker Desktop not found in Program Files"
ls -la "$HOME/.docker" 2>/dev/null | head -5 || echo "No .docker directory in home"

echo ""
echo "🔧 Recommendations:"
echo "------------------"
if ! command -v docker &> /dev/null; then
    echo "1. Docker CLI not accessible from this SSH session"
    echo "2. You may need to:"
    echo "   - Enable WSL integration in Docker Desktop"
    echo "   - OR install Docker directly in WSL"
    echo "   - OR use Docker Desktop from Windows side"
else
    echo "1. Docker is accessible!"
    echo "2. Ready to deploy containers"
fi

echo ""
echo "📋 Next Steps:"
echo "-------------"
echo "1. Enable WSL integration in Docker Desktop settings"
echo "2. Restart Docker Desktop if needed"
echo "3. Run this script again to verify"
echo ""
echo "============================================"