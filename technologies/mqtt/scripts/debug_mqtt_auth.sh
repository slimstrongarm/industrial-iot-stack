#!/bin/bash
# Debug MQTT authentication by monitoring EMQX logs during connection attempts

echo "🔍 MQTT Authentication Debug"
echo "============================"
echo ""

echo "📋 Step 1: Current EMQX Configuration"
echo "Authentication status:"
docker exec emqxnodec emqx_ctl conf show authentication | head -10

echo ""
echo "Active listeners:"
docker exec emqxnodec emqx_ctl listeners | grep -A 5 tcp:default

echo ""
echo "📋 Step 2: Monitor EMQX logs for connection attempts"
echo "Instructions:"
echo "1. This script will start monitoring EMQX logs"
echo "2. In another window/tab, test n8n MQTT connection"
echo "3. Watch for authentication errors in the logs"
echo "4. Press Ctrl+C to stop monitoring"
echo ""
echo "Starting log monitor in 5 seconds..."
sleep 5

echo "🔍 Monitoring EMQX logs (try n8n connection now):"
echo "================================================="
docker logs -f emqxnodec --tail 0