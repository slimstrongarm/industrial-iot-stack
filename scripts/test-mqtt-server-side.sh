#!/bin/bash
# Server-side MQTT integration test script
# Tests EMQX functionality and prepares for Mac-Server integration

echo "🔍 CT-004: MQTT Integration Test - Server Side"
echo "=============================================="
echo ""

# Check if EMQX container is running
if ! docker ps | grep -q emqxnodec; then
    echo "❌ EMQX container (emqxnodec) is not running"
    echo "   Start it with: docker start emqxnodec"
    exit 1
fi

echo "✅ EMQX container is running"
echo ""

# Get server IP information
echo "🌐 Server Network Information:"
echo "  • Container IP: $(docker inspect emqxnodec --format '{{.NetworkSettings.IPAddress}}')"
echo "  • Host IP (Docker): $(hostname -I | awk '{print $1}')"
echo "  • EMQX Status: $(docker exec emqxnodec emqx_ctl status)"
echo ""

# Check EMQX listeners
echo "📡 EMQX Listeners Status:"
docker exec emqxnodec emqx_ctl listeners | grep -E "(tcp|running|current_conn)"
echo ""

# Test local MQTT publishing capability
echo "🧪 Testing Server-Side MQTT Publishing..."
echo "Publishing test message to topic 'server/status'..."

# Publish a test message from server
docker exec emqxnodec emqx_ctl publish topic='server/status' payload='{"status":"online","timestamp":"'$(date -Iseconds)'","source":"server-test"}' qos=1

if [ $? -eq 0 ]; then
    echo "✅ Server can publish MQTT messages successfully"
else
    echo "❌ Server MQTT publishing failed"
    exit 1
fi

echo ""

# Check current connections
echo "👥 Current MQTT Clients:"
CLIENTS=$(docker exec emqxnodec emqx_ctl clients list)
if [ -z "$CLIENTS" ]; then
    echo "  • No clients currently connected (ready for Mac connection)"
else
    echo "$CLIENTS"
fi

echo ""

# Monitor topics
echo "📋 Available Topics for Testing:"
echo "  • server/status - Server status updates"
echo "  • server/data - Server data broadcasts"
echo "  • mac/status - Mac client status (for Mac to publish)"
echo "  • mac/data - Mac sensor data (for Mac to publish)"
echo "  • test/bidirectional - Bidirectional test topic"
echo ""

# Dashboard access info
echo "🖥️  EMQX Dashboard Access:"
echo "  • URL: http://localhost:18083"
echo "  • Default Login: admin / public"
echo "  • Monitor connections and topics in real-time"
echo ""

# Test server-side subscription simulation
echo "🔄 Testing Server-Side MQTT Subscription..."
echo "Starting background subscriber for Mac messages..."

# Start background process to listen for Mac messages
(
    docker exec emqxnodec emqx_ctl subscribe topic='mac/+' qos=1 &
    SUBSCRIBER_PID=$!
    
    # Wait a bit for subscription to initialize
    sleep 2
    
    echo "✅ Server is now listening for Mac messages on 'mac/*' topics"
    echo "   Background subscriber PID: $SUBSCRIBER_PID"
    
    # Keep subscriber running for 30 seconds
    sleep 30
    
    # Clean up
    kill $SUBSCRIBER_PID 2>/dev/null
) &

# Connection instructions for Mac
echo "📱 Instructions for Mac Client:"
echo "===============================
To test from Mac, use these commands:

1. Install Mosquitto (if not already installed):
   brew install mosquitto

2. Get server IP address (replace <SERVER_IP>):
   # Use Tailscale IP or local network IP
   
3. Test connection:
   mosquitto_pub -h <SERVER_IP> -p 1883 -t mac/test -m 'Hello from Mac'

4. Subscribe to server messages:
   mosquitto_sub -h <SERVER_IP> -p 1883 -t server/+ -v

5. Publish sensor data:
   mosquitto_pub -h <SERVER_IP> -p 1883 -t mac/sensor/temp -m '{\"value\":23.5,\"unit\":\"C\"}'

Expected Results:
✅ Mac messages appear in EMQX dashboard
✅ Server can see Mac client in connections list
✅ Bidirectional communication works reliably
"

echo ""
echo "🎯 Server is ready for Mac integration testing!"
echo "📊 Monitor progress at: http://localhost:18083"
echo ""
echo "📋 Next Steps:"
echo "  1. Run Mac-side MQTT client tests"
echo "  2. Verify bidirectional communication"
echo "  3. Document test results"
echo "  4. Mark CT-004 as Complete"