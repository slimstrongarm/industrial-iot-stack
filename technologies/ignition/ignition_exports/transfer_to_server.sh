#!/bin/bash
# Transfer exports to server via Tailscale

TAILSCALE_IP="100.x.x.x"  # Update with your server's Tailscale IP
USERNAME="your-username"   # Update with your username
REMOTE_DIR="/tmp/ignition_imports"

echo "📤 Transferring Ignition exports to server..."
echo "Note: Update TAILSCALE_IP and USERNAME in this script first!"

# Create remote directory
ssh $USERNAME@$TAILSCALE_IP "mkdir -p $REMOTE_DIR"

# Transfer all export files
scp *.zip $USERNAME@$TAILSCALE_IP:$REMOTE_DIR/

# Transfer import script
scp import_to_docker.sh $USERNAME@$TAILSCALE_IP:$REMOTE_DIR/

echo "✅ Transfer complete!"
echo "Next steps on server:"
echo "1. cd $REMOTE_DIR"
echo "2. ./import_to_docker.sh"
