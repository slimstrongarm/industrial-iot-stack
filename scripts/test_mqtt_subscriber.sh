#!/bin/bash
# Test MQTT subscription

echo "🧪 MQTT Connection Test"
echo "======================="
echo ""
echo "Installing mosquitto client..."
sudo apt-get update -qq && sudo apt-get install -y mosquitto-clients -qq

echo ""
echo "Testing subscription to test/# topic..."
echo "Waiting for messages (press Ctrl+C to stop)..."
echo ""

# Subscribe to test topic
mosquitto_sub -h localhost -p 1883 -t "test/#" -v