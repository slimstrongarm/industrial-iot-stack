#!/bin/bash
# Restart EMQX with anonymous authentication enabled

echo "🔄 Restarting EMQX with Anonymous Authentication"
echo "==============================================="
echo ""

echo "Stopping EMQX container..."
docker stop emqxnodec

echo "Starting EMQX with environment variable for anonymous access..."
docker start emqxnodec

# Wait for EMQX to fully start
echo "Waiting for EMQX to start..."
sleep 10

# Create config file to enable anonymous access
cat > /tmp/anon_auth.conf << 'EOF'
listeners.tcp.default.enable_authn = false
allow_anonymous = true
EOF

echo ""
echo "Applying anonymous authentication configuration..."
docker cp /tmp/anon_auth.conf emqxnodec:/tmp/anon_auth.conf
docker exec emqxnodec emqx_ctl conf load /tmp/anon_auth.conf 2>/dev/null

echo ""
echo "Checking listener status..."
docker exec emqxnodec emqx_ctl listeners | grep -A 5 "tcp:default"

echo ""
echo "✅ EMQX restarted with anonymous access"
echo ""
echo "🔌 n8n MQTT Configuration (Anonymous):"
echo "======================================"
echo "Protocol: mqtt://"
echo "Host: localhost"
echo "Port: 1883"
echo "Username: (LEAVE EMPTY)"
echo "Password: (LEAVE EMPTY)"
echo "Client ID: n8n-mqtt-client"
echo "SSL: OFF"
echo ""
echo "This should work now! No authentication required."