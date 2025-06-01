#!/bin/bash
# Monitor Node-RED logs in real-time

echo "🔍 Monitoring Node-RED logs..."
echo "Press Ctrl+C to stop monitoring"
echo "================================"

# Follow the log file
tail -f /Users/joshpayneair/Desktop/industrial-iot-stack/Steel_Bonnet/node-red-flows/node-red.log | grep -E "(Test|tag|creation|Equipment|TEST_FERMENTER|error|warn)" --color=always