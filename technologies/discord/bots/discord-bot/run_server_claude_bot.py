#!/usr/bin/env python3
"""
Server Claude Discord Bot Launcher - 24/7 Operation
Designed to run on the server for always-on mobile coordination
"""

import os
import sys

# Set Discord bot tokens from environment
os.environ['MAC_DISCORD_BOT_TOKEN'] = os.environ.get('MAC_DISCORD_BOT_TOKEN', '')
os.environ['SERVER_DISCORD_BOT_TOKEN'] = os.environ.get('SERVER_DISCORD_BOT_TOKEN', '')

print("🏭 Server Claude Discord Bot Launcher")
print("=" * 60)
print("🎯 24/7 Mobile Coordination Bot")
print("📱 Designed for: Phone → Discord → Server Claude → Google Sheets")
print("✅ Environment variables set")
print("🚀 Starting Server Claude Bot...")
print()

# Import and run the bot
try:
    from industrial_iot_claude_bot import IndustrialIoTBot
    
    # Create bot instance
    bot = IndustrialIoTBot()
    
    # Get token
    token = bot.get_bot_token()
    
    if not token:
        print(f"❌ No token found for {bot.instance_type}")
        sys.exit(1)
    
    print(f"🎯 Instance: {bot.instance_type}")
    print(f"🔑 Token: {token[:20]}...")
    print("⚡ Starting Discord connection...")
    print("📱 Ready for mobile commands!")
    print()
    
    # Run the bot
    bot.run(token)
    
except KeyboardInterrupt:
    print("\n🛑 Server Claude Bot stopped")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()