#!/bin/bash
# Connect to Industrial IoT Server

TAILSCALE_IP="100.94.84.126"
USERNAME="localaccount"

echo "🔗 Connecting to Industrial IoT Server via Tailscale..."
echo "📍 Server IP: $TAILSCALE_IP"
echo "👤 Username: $USERNAME"
echo ""
echo "You'll be prompted for the password for 'localaccount'"
echo ""

# Connect with interactive password prompt
ssh $USERNAME@$TAILSCALE_IP