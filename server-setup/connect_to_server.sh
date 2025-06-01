#!/bin/bash
# SSH Connection Script for IoT Server
# Update these variables with your actual details

SERVER_IP="100.x.x.x"  # Your server's Tailscale IP
USERNAME="your-username"  # Your username on the server

echo "🔗 Connecting to IoT Server via Tailscale..."
echo "Server: $USERNAME@$SERVER_IP"
echo ""

# Check if Tailscale is running
if ! tailscale status >/dev/null 2>&1; then
    echo "❌ Tailscale not running. Start it with: sudo tailscale up"
    exit 1
fi

# Test ping first
echo "🏓 Testing connectivity..."
if ping -c 1 $SERVER_IP >/dev/null 2>&1; then
    echo "✅ Server is reachable"
else
    echo "❌ Cannot reach server. Check Tailscale connection."
    exit 1
fi

# Connect via SSH
echo "🚀 Connecting via SSH..."
ssh $USERNAME@$SERVER_IP
