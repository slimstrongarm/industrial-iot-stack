#!/usr/bin/env python3
"""Test inter_claude_communication with debug output"""

import sys
sys.path.append('/Users/joshpayneair/Desktop/industrial-iot-stack/.claude/adk_enhanced')

from inter_claude_communication import InterClaudeCommunication

# Initialize with debug
comm = InterClaudeCommunication("mac_claude")

print(f"Discord webhook URL loaded: {comm.discord_webhook_url is not None}")
if comm.discord_webhook_url:
    print(f"Webhook URL: {comm.discord_webhook_url[:50]}...")
else:
    print("❌ No webhook URL loaded!")

# Test a simple message
print("\n🧪 Testing simple celebration message...")
result = comm.send_completion_celebration(
    "TEST-001",
    ["Discord messaging test"],
    {"Test": "Success"}
)

print(f"Message send result: {result}")