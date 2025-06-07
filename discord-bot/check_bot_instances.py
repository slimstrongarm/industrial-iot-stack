#!/usr/bin/env python3
"""
Check Discord Bot Instances
Helps identify why there are duplicate Mac Claude Bot instances
"""

import discord
import asyncio
import os

TOKEN = os.environ.get('DISCORD_BOT_TOKEN')
if not TOKEN:
    print("❌ DISCORD_BOT_TOKEN environment variable not set")
    exit(1)

async def check_bot_instances():
    """Check bot instances in Discord"""
    intents = discord.Intents.default()
    intents.message_content = True
    intents.guilds = True
    intents.members = True
    
    client = discord.Client(intents=intents)
    
    @client.event
    async def on_ready():
        print("🤖 Bot Instance Checker")
        print("=" * 50)
        print(f"✅ Connected as: {client.user.name}#{client.user.discriminator}")
        print(f"📋 Bot ID: {client.user.id}")
        
        for guild in client.guilds:
            print(f"\n📍 Server: {guild.name}")
            
            # Count bot instances
            bot_members = []
            for member in guild.members:
                if member.bot and 'claude' in member.name.lower():
                    bot_members.append(member)
            
            print(f"🤖 Found {len(bot_members)} Claude bot(s):")
            for bot in bot_members:
                status = "🟢 Online" if str(bot.status) == "online" else f"⚫ {bot.status}"
                print(f"   • {bot.name}#{bot.discriminator} (ID: {bot.id}) - {status}")
                
                # Check if it's our bot
                if bot.id == client.user.id:
                    print(f"     ↳ This is the current bot instance")
        
        print("\n💡 Solution:")
        print("If you see multiple bots:")
        print("1. The offline one is likely a ghost instance")
        print("2. It should disappear after a few minutes")
        print("3. Or kick the offline bot from server settings")
        
        await client.close()
    
    try:
        await client.start(TOKEN)
    except Exception as e:
        print(f"❌ Error: {e}")

# Run check
asyncio.run(check_bot_instances())