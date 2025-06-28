#!/usr/bin/env python3
"""
Mac Claude Discord Bot Launcher
Sets environment variables and runs the bot
"""

import os
import sys

# Set Discord bot tokens from environment
os.environ['MAC_DISCORD_BOT_TOKEN'] = os.environ.get('MAC_DISCORD_BOT_TOKEN', '')
os.environ['SERVER_DISCORD_BOT_TOKEN'] = os.environ.get('SERVER_DISCORD_BOT_TOKEN', '')

print("🤖 Mac Claude Discord Bot Launcher")
print("=" * 50)
print("✅ Environment variables set")
print("🚀 Starting Mac Claude Bot...")
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
    print()
    
    # Run the bot
    bot.run(token)
    
except KeyboardInterrupt:
    print("\n🛑 Bot stopped by user")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()