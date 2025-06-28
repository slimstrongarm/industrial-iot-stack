# Docker Desktop + WSL + Claude Code Integration Guide

## Overview
This document explains how to configure Docker Desktop to work with Claude Code on Windows WSL, addressing the conflict between Docker's WSL integration and Claude Code's requirements.

## Problem Statement
- **Issue**: Docker Desktop's "WSL Integration" feature conflicts with Claude Code
- **Symptom**: When WSL integration is enabled, Claude Code cannot connect to the WSL instance
- **Solution**: Disable WSL integration and use Docker Desktop via TCP socket

## Configuration Steps

### 1. Docker Desktop Settings
1. Open Docker Desktop
2. Go to Settings → Resources → WSL Integration
3. **Disable** "Enable integration with my default WSL distro"
4. Apply & Restart Docker Desktop

### 2. WSL Docker Access Setup

#### Option A: Wrapper Script (Recommended)
This creates a system-wide `docker` command that connects to Docker Desktop's TCP socket.

```bash
# Create docker wrapper script
sudo tee /usr/local/bin/docker > /dev/null << 'EOF'
#!/bin/bash
DOCKER_HOST=tcp://localhost:2375 "/mnt/c/Program Files/Docker/Docker/resources/bin/docker.exe" "$@"
EOF

# Make it executable
sudo chmod +x /usr/local/bin/docker

# Create docker-compose wrapper
sudo tee /usr/local/bin/docker-compose > /dev/null << 'EOF'
#!/bin/bash
DOCKER_HOST=tcp://localhost:2375 "/mnt/c/Program Files/Docker/Docker/resources/bin/docker-compose.exe" "$@"
EOF

# Make it executable
sudo chmod +x /usr/local/bin/docker-compose
```

#### Option B: Environment Variable (Session-based)
Add to your `~/.bashrc` or `~/.zshrc`:
```bash
export DOCKER_HOST=tcp://localhost:2375
alias docker='"/mnt/c/Program Files/Docker/Docker/resources/bin/docker.exe"'
alias docker-compose='"/mnt/c/Program Files/Docker/Docker/resources/bin/docker-compose.exe"'
```

## Verification

Test the setup:
```bash
# Check Docker version
docker --version

# Test Docker daemon connection
docker ps

# Run a test container
docker run hello-world
```

## Advantages of This Setup
- ✅ Claude Code can connect to WSL without conflicts
- ✅ Docker commands work normally in WSL
- ✅ No need for duplicate Docker installations
- ✅ Uses Docker Desktop's existing daemon and resources
- ✅ Compatible with docker-compose and other tools

## Troubleshooting

### Issue: "Cannot connect to Docker daemon"
- Ensure Docker Desktop is running
- Check if port 2375 is exposed in Docker Desktop settings
- Verify with: `curl http://localhost:2375/version`

### Issue: Permission denied on wrapper scripts
```bash
sudo chmod +x /usr/local/bin/docker
sudo chmod +x /usr/local/bin/docker-compose
```

### Issue: Docker commands not found
- Check PATH includes `/usr/local/bin`: `echo $PATH`
- Try absolute path: `/usr/local/bin/docker --version`

## Rollback Instructions
If you need to remove this setup:
```bash
# Remove wrapper scripts
sudo rm /usr/local/bin/docker
sudo rm /usr/local/bin/docker-compose

# Re-enable WSL integration in Docker Desktop if needed
```

## Implementation Date
- **Date**: June 3, 2025
- **Implemented by**: server-claude via Claude Code
- **Reason**: Enable Docker functionality while maintaining Claude Code access

## Related Documentation
- [Docker Desktop WSL Backend](https://docs.docker.com/desktop/windows/wsl/)
- [SERVER_SETUP_GUIDE.md](./SERVER_SETUP_GUIDE.md)
- [DOCKER_MIGRATION_STRATEGY.md](./DOCKER_MIGRATION_STRATEGY.md)