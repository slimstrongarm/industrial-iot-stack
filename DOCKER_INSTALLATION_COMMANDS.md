# Docker System-Wide Installation Commands

## Ready-to-Run Commands

The Docker wrapper scripts are tested and ready. Run these commands to install system-wide:

### Option 1: Single Command Installation
```bash
sudo bash -c '
echo "Installing Docker wrappers system-wide..."
mkdir -p /usr/local/bin

# Install docker wrapper
cat > /usr/local/bin/docker << '"'"'EOF'"'"'
#!/bin/bash
DOCKER_HOST=tcp://localhost:2375 "/mnt/c/Program Files/Docker/Docker/resources/bin/docker.exe" "$@"
EOF
chmod +x /usr/local/bin/docker

# Install docker-compose wrapper
cat > /usr/local/bin/docker-compose << '"'"'EOF'"'"'
#!/bin/bash
DOCKER_HOST=tcp://localhost:2375 "/mnt/c/Program Files/Docker/Docker/resources/bin/docker-compose.exe" "$@"
EOF
chmod +x /usr/local/bin/docker-compose

echo "✅ Docker wrappers installed successfully!"
echo "Testing installation..."
/usr/local/bin/docker --version
/usr/local/bin/docker-compose --version
'
```

### Option 2: Use Our Installation Script
```bash
sudo /mnt/c/Users/LocalAccount/industrial-iot-stack/scripts/install-docker-wrappers.sh
```

## Verification Commands
After installation, test with:
```bash
# Test Docker
docker --version
docker ps

# Test Docker Compose  
docker-compose --version

# Verify system PATH includes /usr/local/bin
echo $PATH | grep -o "/usr/local/bin"
```

## Current Status
- ✅ Wrapper scripts created and tested
- ✅ Docker Desktop accessible via TCP socket (localhost:2375)
- ✅ Both docker and docker-compose commands work
- ⏳ **Pending**: System-wide installation (requires sudo)

## Benefits After Installation
- All scripts and services can use `docker` commands
- No need to specify full paths or set environment variables
- Docker Compose will work automatically
- Monitoring tools and CI/CD pipelines will function normally

## Installation Date
- **Prepared**: June 3, 2025
- **Status**: Ready for installation
- **Tested**: ✅ Wrappers verified working