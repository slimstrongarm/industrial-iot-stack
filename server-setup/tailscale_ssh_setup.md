# Tailscale SSH Setup Guide
Generated: 2025-06-01 11:50
Task: Setup Tailscale SSH connection to server

## 🎯 Objective
Set up secure SSH access to your POC server via Tailscale for Docker deployment.

## 📋 Prerequisites
- [ ] Tailscale account created
- [ ] Server with Tailscale installed
- [ ] MacBook with Tailscale installed

## 🔧 Setup Steps

### 1. Install Tailscale (if not already done)
```bash
# On macOS (MacBook)
brew install tailscale

# On server (Ubuntu/Debian)
curl -fsSL https://tailscale.com/install.sh | sh
```

### 2. Connect Both Devices
```bash
# On both MacBook and server
sudo tailscale up
```

### 3. Get Tailscale IPs
```bash
# Check your Tailscale network
tailscale status

# Find server IP (format: 100.x.x.x)
```

### 4. Test SSH Connection
```bash
# Replace with your server's Tailscale IP
ssh username@100.x.x.x

# If prompted, accept the host key
```

### 5. Set up Key-based Authentication (Recommended)
```bash
# Generate SSH key if you don't have one
ssh-keygen -t ed25519 -C "iot-stack-deployment"

# Copy public key to server
ssh-copy-id username@100.x.x.x
```

### 6. Create Connection Script
```bash
# File: connect_to_server.sh
#!/bin/bash
SERVER_IP="100.x.x.x"  # Update with actual IP
USERNAME="your-username"  # Update with actual username

echo "🔗 Connecting to IoT Server via Tailscale..."
ssh $USERNAME@$SERVER_IP
```

## 🧪 Test Commands
```bash
# Basic connectivity test
ping 100.x.x.x

# SSH with verbose output
ssh -v username@100.x.x.x

# Test Docker access
ssh username@100.x.x.x "docker --version"
```

## 🐛 Troubleshooting

### Connection Refused
- Check if SSH service is running: `systemctl status ssh`
- Check firewall: `ufw status`

### Permission Denied
- Verify username is correct
- Check SSH key permissions: `chmod 600 ~/.ssh/id_ed25519`

### Tailscale Not Connected
- Restart Tailscale: `sudo tailscale down && sudo tailscale up`
- Check status: `tailscale status`

## 🎯 Next Steps After Connection Works
1. Transfer Docker configs to server
2. Set up TMUX sessions for persistent deployment
3. Deploy containers via SSH

## 📝 Connection Details to Save
- Server Tailscale IP: 100.x.x.x
- Username: your-username
- SSH Key: ~/.ssh/id_ed25519
- Connection script: connect_to_server.sh

---
Generated by: MacBook Claude
Task ID: DM-004
