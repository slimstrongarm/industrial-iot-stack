#!/bin/bash
# Installation script for Docker WSL wrappers
# This script needs to be run with sudo

echo "🐳 Docker WSL Wrapper Installation Script"
echo "========================================"
echo ""
echo "This script will install Docker wrapper commands in /usr/local/bin"
echo "to allow Docker Desktop to work with Claude Code in WSL."
echo ""

# Check if running with sudo
if [ "$EUID" -ne 0 ]; then 
    echo "❌ Please run this script with sudo:"
    echo "   sudo ./install-docker-wrappers.sh"
    exit 1
fi

# Create /usr/local/bin if it doesn't exist
mkdir -p /usr/local/bin

# Install docker wrapper
echo "📦 Installing docker wrapper..."
cat > /usr/local/bin/docker << 'EOF'
#!/bin/bash
DOCKER_HOST=tcp://localhost:2375 "/mnt/c/Program Files/Docker/Docker/resources/bin/docker.exe" "$@"
EOF
chmod +x /usr/local/bin/docker

# Install docker-compose wrapper
echo "📦 Installing docker-compose wrapper..."
cat > /usr/local/bin/docker-compose << 'EOF'
#!/bin/bash
DOCKER_HOST=tcp://localhost:2375 "/mnt/c/Program Files/Docker/Docker/resources/bin/docker-compose.exe" "$@"
EOF
chmod +x /usr/local/bin/docker-compose

# Test the installation
echo ""
echo "🧪 Testing installation..."
echo -n "Docker version: "
/usr/local/bin/docker --version

echo ""
echo "✅ Installation complete!"
echo ""
echo "You can now use 'docker' and 'docker-compose' commands normally."
echo "To verify the setup, run: docker ps"