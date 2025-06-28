# Server Connection Information

## Tailscale Details
- **IP Address**: 100.94.84.126
- **Status**: Ready for connection
- **Date Provided**: June 1, 2025

## Next Steps for Server Claude

### 1. SSH Connection Test
```bash
# From Mac terminal (this instance)
ssh localaccount@100.94.84.126
```

### 2. Required Information Still Needed:
- [x] SSH Username: `localaccount`
- [ ] SSH Authentication method (key or password)
- [ ] WSL or native Windows SSH?

### 3. Once Connected, Server Claude Will:
1. Run Docker audit script
2. Set up TMUX session (Blue theme)
3. Deploy Docker containers
4. Update Google Sheets progress
5. Establish Git sync for communication

## Connection Script
Save this as `connect_to_server.sh`:
```bash
#!/bin/bash
# Industrial IoT Server Connection

TAILSCALE_IP="100.94.84.126"
USERNAME="your_username_here"

echo "🔗 Connecting to Industrial IoT Server..."
echo "📍 Tailscale IP: $TAILSCALE_IP"

# SSH with tmux session creation
ssh -t $USERNAME@$TAILSCALE_IP "tmux new-session -s claude-server || tmux attach-session -t claude-server"
```

## Docker & WSL Investigation Commands

When SSH'd into the Windows server, run these commands to check Docker/WSL state:

### Quick Check (Windows CMD via SSH):
```cmd
# Check Docker Desktop
docker --version

# Check WSL distributions
wsl -l -v

# Enter default WSL
wsl

# Once in WSL, check Docker
docker --version
docker ps
```

### If Docker not working in WSL:
1. Exit WSL (type `exit`)
2. On Windows host, open Docker Desktop
3. Settings → Resources → WSL Integration
4. Enable integration with your WSL distro
5. Apply & Restart

### Alternative: Use Docker from Windows directly:
```cmd
# From Windows SSH session
"C:\Program Files\Docker\Docker\resources\bin\docker.exe" --version
```