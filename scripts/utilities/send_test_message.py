#!/usr/bin/env python3
"""Send test message to verify Discord is working"""

import sys
sys.path.append('/Users/joshpayneair/Desktop/industrial-iot-stack/.claude/adk_enhanced')

from inter_claude_communication import InterClaudeCommunication

# Send a clear test message about CT-084
comm = InterClaudeCommunication("mac_claude")

message = """🪂 **CT-084 PARACHUTE DROP PROGRESS**

Hey Server Claude! Mac Claude here with an update:

✅ **COMPLETED CT-084 FOUNDATIONS:**
• Complete Pi image builder script  
• Enhanced discovery agent with AI-powered tag intelligence
• Auto sensor configurator for Phidget hub
• Node-RED dashboard generator

🎯 **NEXT**: Waiting for your Docker Agent (CT-076) completion so we can integrate everything!

Can you see this message? Testing Discord coordination! 🤖💬"""

result = comm._send_message(
    channel="coordination",
    title="🪂 CT-084 Progress Update",
    message=message,
    target="server_claude", 
    color=0x00ff00
)

print(f"Message sent: {result}")

# Also send a simple content message
import requests
webhook_url = "https://discordapp.com/api/webhooks/1380061953883373660/lFn5d2hcBxAhaMJSpBNwjQNInczAGYQ-HYky70iSiNymhFXw7egnjUapMdAHZXrRWJhG"

simple_payload = {
    "content": "🧪 **SIMPLE TEST** - Can you see this direct message? Mac Claude testing Discord!",
    "username": "Mac Claude"
}

response = requests.post(webhook_url, json=simple_payload)
print(f"Simple message status: {response.status_code}")