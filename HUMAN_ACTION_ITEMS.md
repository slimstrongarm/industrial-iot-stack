# Human Architect Action Items - Docker Migration & Tailscale Setup

## 🚨 IMMEDIATE ACTION REQUIRED

### 1. Server Access Information Needed
**Claude is waiting for:**
- [ ] **Tailscale IP address** of your POC server (format: 100.x.x.x)
- [ ] **SSH username** for server access
- [ ] **Confirmation** that Tailscale is installed and connected on server

**Provide by running:**
```bash
# On your server
tailscale status
# Look for the server's IP (100.x.x.x)
```

### 2. Initial Server Setup Tasks
**Before Claude can deploy Docker:**
- [ ] Install Docker and Docker Compose on server (if not done)
- [ ] Create base directory: `mkdir -p /opt/industrial-iot-stack`
- [ ] Set permissions: `sudo chown -R $USER:$USER /opt/industrial-iot-stack`

### 3. Critical Files to Transfer
**From your MacBook to server:**
- [ ] **Flint module file**: `ignition-project-scan-endpoint.modl`
- [ ] **Ignition Gateway backup** (if you want to preserve settings)
- [ ] **Export all 8-9 Ignition projects** as .zip files

## 📋 DECISION POINTS REQUIRING APPROVAL

### Architecture Decisions
1. **Docker Network Subnet**
   - Proposed: `172.20.0.0/16`
   - [ ] Approve or provide alternative

2. **Service Ports**
   - Ignition: 8088 (web), 62541 (OPC-UA)
   - Node-RED: 1880
   - MQTT: 1883
   - [ ] Confirm no conflicts with existing services

3. **Data Persistence Strategy**
   - Volumes mounted to `/opt/industrial-iot-stack/volumes/`
   - [ ] Approve location or specify alternative

### Security Decisions
4. **Gateway Credentials**
   - Current: slimstrongarm/0804
   - [ ] Keep same or provide new secure credentials

5. **Tailscale Access**
   - All services behind Tailscale VPN only
   - [ ] Confirm no public internet exposure needed

## 🤖 AUTOMATED TASKS (Claude will handle)

### Phase 1: Docker Setup
- Create Docker Compose configurations
- Set up persistent volumes
- Configure inter-service networking
- Deploy monitoring stack (Portainer, Grafana)

### Phase 2: Service Migration
- Deploy Ignition container
- Install Flint module via volume mount
- Import exported projects
- Configure MQTT Engine module
- Test VS Code Flint connection

### Phase 3: Integration Testing
- Verify all services healthy
- Test MQTT data flow
- Validate Node-RED → Ignition connection
- Set up automated backups

## 🔄 HANDOFF SEQUENCE

### Step 1: You provide (TODAY)
```bash
# Run this and share output:
echo "Server IP: $(tailscale ip -4)"
echo "Username: $USER"
echo "Docker: $(docker --version 2>/dev/null || echo 'Not installed')"
```

### Step 2: Claude prepares
- Docker Compose files ready to deploy
- Migration scripts prepared
- TMUX session layout configured

### Step 3: You execute
- SSH into server
- Clone deployment files
- Run initial setup script

### Step 4: Claude validates
- Connect via your SSH session
- Run deployment commands
- Monitor service health
- Troubleshoot any issues

## ⏰ TIMELINE EXPECTATIONS

### Today (Human Tasks - 30 min)
- [ ] Provide server access details
- [ ] Export Ignition projects
- [ ] Locate Flint module file

### Tomorrow (Deployment - 2-3 hours)
- [ ] Morning: Initial Docker deployment
- [ ] Afternoon: Service migration
- [ ] Evening: Testing and validation

### This Week
- [ ] Production readiness testing
- [ ] Documentation updates
- [ ] Team training on new setup

## 🚦 CURRENT BLOCKERS

1. **Waiting for server details** - Cannot proceed without Tailscale IP
2. **Ignition exports needed** - Projects must be exported before migration
3. **Flint module location** - Need exact path to .modl file

## 📞 COMMUNICATION PROTOCOL

### When to interrupt current Claude session:
- Server access details ready
- Critical decisions needed
- Blocking issues encountered

### What to include in update:
```
SERVER_READY:
- Tailscale IP: 100.x.x.x
- Username: yourusername
- Docker installed: yes
- Projects exported: yes
- Flint module at: /path/to/module.modl
```

## 🎯 SUCCESS CRITERIA

**Human tasks complete when:**
- [ ] Claude can SSH to server
- [ ] All files ready for transfer
- [ ] Architecture decisions approved
- [ ] 30-minute availability for deployment support

**Ready to proceed indicator:**
"Claude, server is ready at 100.x.x.x with username 'myuser'. Docker is installed. Projects are exported to ~/ignition-exports/. Flint module is at ~/Downloads/ignition-project-scan-endpoint.modl. Proceed with deployment."

---

**Note**: This migration is critical for scalability. Once on Docker, we can replicate the entire stack for other clients. Your 30 minutes today enables weeks of future automation.