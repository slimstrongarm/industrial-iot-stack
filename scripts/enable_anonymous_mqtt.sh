#!/bin/bash
# Quick fix: Enable anonymous MQTT access in EMQX

echo "🔧 Enabling Anonymous MQTT Access"
echo "================================="
echo ""

echo "📋 Current EMQX authentication status:"
docker exec emqxnodec emqx_ctl conf show authentication 2>/dev/null | head -5

echo ""
echo "🔧 Method 1: Disable authentication on TCP listener"
echo 'listeners.tcp.default.enable_authn = false' | docker exec -i emqxnodec sh -c 'cat > /tmp/disable_auth.conf && emqx_ctl conf load /tmp/disable_auth.conf'

echo ""
echo "🔧 Method 2: Clear all authentication providers"
echo 'authentication = []' | docker exec -i emqxnodec sh -c 'cat > /tmp/clear_auth.conf && emqx_ctl conf load /tmp/clear_auth.conf'

echo ""
echo "🔧 Method 3: Clear authorization sources"
echo 'authorization.sources = []' | docker exec -i emqxnodec sh -c 'cat > /tmp/clear_authz.conf && emqx_ctl conf load /tmp/clear_authz.conf'

echo ""
echo "🧪 Testing anonymous MQTT connection..."
sleep 2

# Test anonymous connection
if timeout 5 mosquitto_pub -h localhost -p 1883 -t "test/anonymous" -m "Test message - $(date)" 2>/dev/null; then
    echo "✅ Anonymous MQTT publish successful!"
    MQTT_STATUS="working"
else
    echo "❌ Anonymous MQTT publish still failing"
    MQTT_STATUS="failed"
fi

echo ""
echo "📊 Results:"
echo "==========="
if [ "$MQTT_STATUS" = "working" ]; then
    echo "✅ EMQX anonymous access is now working!"
    echo ""
    echo "🧪 Test n8n MQTT credentials with:"
    echo "   Protocol: mqtt://"
    echo "   Host: localhost"
    echo "   Port: 1883"
    echo "   Username: (leave empty)"
    echo "   Password: (leave empty)"
    echo "   Client ID: (leave empty or use: n8n-test-client)"
    echo "   SSL: OFF"
    echo ""
    echo "🎯 Next steps:"
    echo "1. Test n8n MQTT credential (should pass now)"
    echo "2. Test Mac ↔ Server MQTT if n8n works"
    echo "3. Configure proper authentication later"
    
else
    echo "❌ Still having issues. Let's check EMQX logs:"
    echo ""
    docker logs emqxnodec --tail 10
    echo ""
    echo "🔧 Alternative: Restart EMQX container"
    echo "docker restart emqxnodec"
fi

echo ""
echo "🔍 Current EMQX listener status:"
docker exec emqxnodec emqx_ctl listeners | grep -A 5 tcp:default