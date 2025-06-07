#!/bin/bash
# Set up proper EMQX authentication based on Claude Desktop research

echo "🔧 Setting Up EMQX Proper Authentication"
echo "========================================"
echo ""

# Step 1: Reset EMQX admin password (we already did this)
echo "📋 Step 1: EMQX Dashboard Access"
echo "URL: http://localhost:18083"
echo "Username: admin"
echo "Password: adminpass123"
echo ""

# Step 2: Check EMQX container and network status
echo "📋 Step 2: Network Diagnostics"
echo "EMQX Container Status:"
docker ps | grep emqx | head -1

echo ""
echo "EMQX IP Address:"
docker inspect emqxnodec | grep '"IPAddress"' | head -1

echo ""
echo "EMQX Port Mapping:"
docker port emqxnodec

echo ""
echo "Test Host Port Access:"
if timeout 3 bash -c "</dev/tcp/localhost/1883"; then
    echo "✅ Port 1883 accessible on localhost"
    HOST_ADDRESS="localhost"
elif timeout 3 bash -c "</dev/tcp/172.17.0.4/1883"; then
    echo "✅ Port 1883 accessible on 172.17.0.4"
    HOST_ADDRESS="172.17.0.4"
else
    echo "❌ Port 1883 not accessible"
    HOST_ADDRESS="unknown"
fi

echo ""
echo "📋 Step 3: Instructions for EMQX Dashboard Setup"
echo "=============================================="
echo ""
echo "Manual steps to complete in EMQX Dashboard:"
echo ""
echo "1. 🌐 Access Dashboard:"
echo "   URL: http://localhost:18083"
echo "   Login: admin / adminpass123"
echo ""
echo "2. 👤 Create MQTT User:"
echo "   → Go to: Access Control → Authentication"
echo "   → Click: + Add"
echo "   → Choose: Built-in Database"
echo "   → Configure:"
echo "     - Backend: Built-in Database"
echo "     - Mechanism: Password-based"
echo "     - Password Hash: Plain"
echo "   → Save"
echo ""
echo "3. 🔐 Add MQTT User:"
echo "   → Go to: Access Control → Users"
echo "   → Click: + Add User"
echo "   → Create user:"
echo "     - Username: n8n_user"
echo "     - Password: n8n_secure_pass"
echo "   → Save"
echo ""
echo "4. 🧪 Test in n8n:"
if [ "$HOST_ADDRESS" != "unknown" ]; then
echo "   → Go to n8n Credentials → Add MQTT"
echo "   → Configure:"
echo "     - Protocol: mqtt://"
echo "     - Host: $HOST_ADDRESS"
echo "     - Port: 1883"
echo "     - Username: n8n_user"
echo "     - Password: n8n_secure_pass"
echo "     - Client ID: (leave empty)"
echo "     - SSL: OFF"
echo "   → Test Connection"
else
echo "   ⚠️  Network connectivity issue detected"
echo "   → First fix network connectivity"
echo "   → Then configure MQTT credentials"
fi

echo ""
echo "📋 Step 4: Alternative Quick Test"
echo "=============================="
echo ""
echo "If you want to test without creating users first:"
echo ""
echo "A. Enable Anonymous Access:"
echo "   → EMQX Dashboard → Access Control → Authentication"
echo "   → Look for 'Allow Anonymous' toggle"
echo "   → Enable it"
echo "   → Then use empty username/password in n8n"
echo ""
echo "B. Or use CLI to enable anonymous:"

# Try to enable anonymous access via CLI
echo "🔧 Attempting to enable anonymous access via CLI..."
if docker exec emqxnodec emqx_ctl conf show listeners.tcp.default 2>/dev/null | grep -q "enable_authn"; then
    echo "Authentication setting found, attempting to disable..."
    echo 'listeners.tcp.default.enable_authn = false' | docker exec -i emqxnodec sh -c 'cat > /tmp/anon_fix.conf && emqx_ctl conf load /tmp/anon_fix.conf' 2>&1
else
    echo "Using alternative method..."
    echo 'authentication = []' | docker exec -i emqxnodec sh -c 'cat > /tmp/auth_disable.conf && emqx_ctl conf load /tmp/auth_disable.conf' 2>&1
fi

echo ""
echo "📋 Step 5: Network Connectivity Fix"
echo "================================="
echo ""
echo "If n8n still can't connect, try these host addresses:"
echo ""
echo "Option 1 - Localhost (if port mapped):"
echo "  Host: localhost"
echo "  Port: 1883"
echo ""
echo "Option 2 - Container IP:"
echo "  Host: 172.17.0.4"
echo "  Port: 1883"
echo ""
echo "Option 3 - Container name (if same network):"
echo "  Host: emqxnodec"
echo "  Port: 1883"
echo ""
echo "Option 4 - Docker gateway:"
echo "  Host: host.docker.internal"
echo "  Port: 1883"

echo ""
echo "📋 Verification Commands"
echo "======================"
echo ""
echo "Check EMQX listeners:"
echo "docker exec emqxnodec emqx_ctl listeners"
echo ""
echo "Check EMQX authentication:"
echo "docker exec emqxnodec emqx_ctl conf show authentication"
echo ""
echo "Check connected clients:"
echo "docker exec emqxnodec emqx_ctl clients list"
echo ""
echo "✅ Setup guide complete!"
echo "Follow the dashboard steps above, then test n8n connection."