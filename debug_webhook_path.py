#!/usr/bin/env python3
"""Debug webhook path resolution"""

from pathlib import Path

# Test the exact path logic from inter_claude_communication.py
script_path = Path("/Users/joshpayneair/Desktop/industrial-iot-stack/.claude/adk_enhanced/inter_claude_communication.py")
webhook_file = script_path.parent.parent.parent / "credentials" / "discord_webhook.txt"

print(f"Script path: {script_path}")
print(f"Parent: {script_path.parent}")
print(f"Parent.parent: {script_path.parent.parent}")
print(f"Parent.parent.parent: {script_path.parent.parent.parent}")
print(f"Webhook file path: {webhook_file}")
print(f"Webhook file exists: {webhook_file.exists()}")

if webhook_file.exists():
    with open(webhook_file, 'r') as f:
        content = f.read()
        print(f"File content preview: {content[:200]}...")
        for line in content.split('\n'):
            if line.startswith('Webhook URL:'):
                webhook_url = line.replace('Webhook URL:', '').strip()
                print(f"Found webhook URL: {webhook_url}")
                break
else:
    print("❌ Webhook file not found!")
    
# Test relative to current directory
current_webhook = Path("credentials/discord_webhook.txt")
print(f"\nCurrent directory webhook: {current_webhook}")
print(f"Current directory webhook exists: {current_webhook.exists()}")