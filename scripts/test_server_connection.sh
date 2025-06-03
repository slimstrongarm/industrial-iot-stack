#!/bin/bash
# Test connection to Industrial IoT Server

TAILSCALE_IP="100.94.84.126"
USERNAME="localaccount"

echo "🔗 Testing connection to Industrial IoT Server..."
echo "📍 Tailscale IP: $TAILSCALE_IP"
echo "👤 Username: $USERNAME"
echo ""
echo "Attempting SSH connection..."
echo "You may be prompted for a password."
echo ""

# Test SSH connection
ssh -o ConnectTimeout=10 -o StrictHostKeyChecking=no $USERNAME@$TAILSCALE_IP "echo '✅ SSH Connection Successful!'; uname -a; echo ''; echo 'Checking for WSL:'; wsl -l -v 2>/dev/null || echo 'WSL not accessible from this SSH session'"