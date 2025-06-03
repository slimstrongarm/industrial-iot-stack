# WSL Permission Issues - Quick Fixes

## Common Permission Problems & Solutions

### 1. 🔑 SSH Server Won't Start
```bash
# Fix SSH permissions
sudo chown root:root /etc/ssh/*
sudo chmod 600 /etc/ssh/ssh_host_*_key
sudo chmod 644 /etc/ssh/ssh_host_*_key.pub

# Start SSH service
sudo service ssh start
# OR
sudo systemctl enable ssh
sudo systemctl start ssh
```

### 2. 📁 File Permission Issues
```bash
# Fix WSL file permissions
# Add to ~/.bashrc or /etc/wsl.conf
[automount]
enabled = true
options = "metadata,umask=22,fmask=11"

# Then restart WSL
wsl --shutdown
# Reopen WSL
```

### 3. 🐳 Docker Permission Denied
```bash
# Add user to docker group
sudo usermod -aG docker $USER

# Apply changes without logging out
newgrp docker

# Verify
docker run hello-world
```

### 4. 🚫 Cannot Write to Windows Drives
```bash
# If /mnt/c is read-only
# Create /etc/wsl.conf if not exists
sudo nano /etc/wsl.conf

# Add:
[automount]
enabled = true
options = "metadata"
mountFsTab = true

# Restart WSL
```

### 5. 🔧 Systemd Issues (WSL2)
```bash
# Enable systemd in WSL2
# Edit /etc/wsl.conf
[boot]
systemd=true

# Restart WSL completely
wsl --shutdown
```

### 6. 🌐 Network Permission Issues
```bash
# If you can't bind to ports
# Check Windows Firewall
# Or use higher ports (>1024)

# Allow port binding
sudo setcap 'cap_net_bind_service=+ep' /usr/bin/node
```

## Quick Permission Reset Script
```bash
#!/bin/bash
# Save as fix-permissions.sh

echo "Fixing common WSL permissions..."

# Fix SSH
echo "Fixing SSH permissions..."
sudo chown root:root /etc/ssh/* 2>/dev/null
sudo chmod 600 /etc/ssh/ssh_host_*_key 2>/dev/null
sudo chmod 644 /etc/ssh/ssh_host_*_key.pub 2>/dev/null

# Fix Docker
echo "Adding user to docker group..."
sudo usermod -aG docker $USER 2>/dev/null

# Fix common directories
echo "Fixing home directory permissions..."
sudo chown -R $USER:$USER $HOME
chmod 755 $HOME

echo "Done! You may need to:"
echo "1. Run 'newgrp docker' for Docker access"
echo "2. Run 'wsl --shutdown' and restart for full effect"
```

## Docker Desktop Settings (if using)
1. Open Docker Desktop
2. Settings → Resources → WSL Integration
3. Enable integration with your WSL distro
4. Apply & Restart

## Still Having Issues?

### Nuclear Option - Fresh WSL
```bash
# From PowerShell (admin)
wsl --unregister Ubuntu
wsl --install -d Ubuntu

# This gives you a clean slate
```

### Alternative - Use WSL1 Instead
```bash
# From PowerShell
wsl --set-version Ubuntu 1
# WSL1 has fewer permission issues but less features
```

## For Your IIoT Stack

### Create a setup script:
```bash
#!/bin/bash
# iiot-wsl-setup.sh

# Update system
sudo apt update && sudo apt upgrade -y

# Install essentials
sudo apt install -y \
    docker.io \
    docker-compose \
    openssh-server \
    git \
    curl \
    wget

# Fix Docker permissions
sudo usermod -aG docker $USER

# Start services
sudo service docker start
sudo service ssh start

# Create project directory
mkdir -p ~/industrial-iot-stack
cd ~/industrial-iot-stack

echo "WSL environment ready!"
echo "Run 'newgrp docker' to activate docker group"
```

Need me to help with your specific error message?