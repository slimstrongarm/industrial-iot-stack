#!/usr/bin/env python3
"""
Start Discord bot with debug output
Shows exactly what messages are being processed
"""

import os
# Load token from environment or .env file
if not os.environ.get('DISCORD_BOT_TOKEN'):
    if os.path.exists('discord-bot/.env'):
        with open('discord-bot/.env') as f:
            for line in f:
                if line.startswith('DISCORD_BOT_TOKEN='):
                    os.environ['DISCORD_BOT_TOKEN'] = line.split('=', 1)[1].strip()
                    break

# Import after setting env var
from industrial_iot_claude_bot import IndustrialIoTBot
import discord
import logging

# Enhanced logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class DebugBot(IndustrialIoTBot):
    """Debug version with enhanced logging"""
    
    async def on_message(self, message):
        """Enhanced message processing with debug output"""
        # Log all messages
        print(f"\n📨 MESSAGE RECEIVED:")
        print(f"   Author: {message.author} (ID: {message.author.id})")
        print(f"   Content: '{message.content}'")
        print(f"   Channel: {message.channel.name}")
        print(f"   Bot mentioned: {self.user.mentioned_in(message)}")
        print(f"   Bot user: {self.user} (ID: {self.user.id})")
        
        # Don't respond to self
        if message.author == self.user:
            print("   ↳ Ignoring (self message)")
            return
        
        # Check for mentions more thoroughly
        bot_id_string = f"<@{self.user.id}>"
        bot_id_string_nick = f"<@!{self.user.id}>"
        
        is_mentioned = (
            self.user.mentioned_in(message) or 
            bot_id_string in message.content or
            bot_id_string_nick in message.content or
            message.content.lower().startswith('@claude')
        )
        
        print(f"   Bot ID strings: {bot_id_string}, {bot_id_string_nick}")
        print(f"   Is mentioned: {is_mentioned}")
        
        if is_mentioned:
            print("   ↳ Processing as natural language")
            await self.process_natural_language(message)
        else:
            print("   ↳ Not mentioned, skipping")

# Run debug bot
if __name__ == "__main__":
    print("🐛 Starting Discord Bot in DEBUG mode")
    print("=" * 60)
    print("This will show detailed message processing information")
    print()
    
    bot = DebugBot()
    bot.run(os.environ['DISCORD_BOT_TOKEN'])