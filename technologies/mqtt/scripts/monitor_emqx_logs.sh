#!/bin/bash
# Monitor EMQX logs to see exact authentication error

echo "📋 EMQX Log Monitor"
echo "==================="
echo ""
echo "Instructions:"
echo "1. This will monitor EMQX logs in real-time"
echo "2. Try connecting from n8n while this is running"
echo "3. Look for authentication error messages"
echo "4. Press Ctrl+C to stop"
echo ""
echo "Starting log monitor..."
echo ""

docker logs -f emqxnodec --tail 0 2>&1 | grep -E "(auth|client|connect|n8n|mqtt)" --line-buffered