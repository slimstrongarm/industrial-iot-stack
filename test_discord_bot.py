#!/usr/bin/env python3
"""Test Discord bot with tokens"""

import os
import socket

# Set the Discord bot tokens
os.environ['MAC_DISCORD_BOT_TOKEN'] = 'MTM4MTMxQxOTk0NTk3NTc3Mzc3OA.G9KB9Q.jODzGUt8TnHyaqAAy0KbB4tdalezysXG-_6xJ4'
os.environ['SERVER_DISCORD_BOT_TOKEN'] = 'MTM4MTMzNjM1OTE5Njk1MDU5OA.GNW9ge.4BHWL_xhn8AdNqoMT_cQY2gse0neDPb-TxHLG4'

print("🤖 Discord Bot Token Test")
print("=" * 40)

# Detect instance
hostname = socket.gethostname().lower()
if "server" in hostname or "flint" in hostname or "linux" in hostname:
    instance_type = "Server Claude"
    token = os.environ.get('SERVER_DISCORD_BOT_TOKEN')
else:
    instance_type = "Mac Claude" 
    token = os.environ.get('MAC_DISCORD_BOT_TOKEN')

print(f"🏷️  Detected Instance: {instance_type}")
print(f"🔑 Token Available: {'✅ Yes' if token else '❌ No'}")
if token:
    print(f"🔍 Token Preview: {token[:20]}...")

print("\n🚀 Environment Variables Set:")
print(f"   MAC_DISCORD_BOT_TOKEN: {'✅ Set' if os.environ.get('MAC_DISCORD_BOT_TOKEN') else '❌ Missing'}")
print(f"   SERVER_DISCORD_BOT_TOKEN: {'✅ Set' if os.environ.get('SERVER_DISCORD_BOT_TOKEN') else '❌ Missing'}")

print(f"\n✅ Ready to run Discord bot as {instance_type}!")
print("\nNow run:")
print("   cd discord-bot && python3 industrial_iot_claude_bot.py")

# Import and test the bot class
try:
    import sys
    sys.path.append('/Users/joshpayneair/Desktop/industrial-iot-stack/discord-bot')
    from industrial_iot_claude_bot import IndustrialIoTBot
    
    print(f"\n🔬 Testing Bot Class...")
    bot = IndustrialIoTBot()
    print(f"   Instance Type: {bot.instance_type}")
    print(f"   Token Method: {bot.get_bot_token()[:20] if bot.get_bot_token() else 'None'}...")
    print("✅ Bot class working correctly!")
    
except Exception as e:
    print(f"❌ Bot class error: {e}")