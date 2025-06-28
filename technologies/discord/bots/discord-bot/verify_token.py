#!/usr/bin/env python3
"""
Verify Discord bot token and connection
"""

import discord
import asyncio
import os

TOKEN = os.environ.get('DISCORD_BOT_TOKEN')
if not TOKEN:
    # Try to load from .env file
    if os.path.exists('discord-bot/.env'):
        with open('discord-bot/.env') as f:
            for line in f:
                if line.startswith('DISCORD_BOT_TOKEN='):
                    TOKEN = line.split('=', 1)[1].strip()
                    break
    
    if not TOKEN:
        print("❌ DISCORD_BOT_TOKEN environment variable not set")
        print("Set via: export DISCORD_BOT_TOKEN='your_token' or create discord-bot/.env")
        exit(1)

async def test_token():
    """Test if token is valid"""
    intents = discord.Intents.default()
    intents.message_content = True
    
    client = discord.Client(intents=intents)
    
    @client.event
    async def on_ready():
        print(f"✅ Token is VALID!")
        print(f"🤖 Bot name: {client.user.name}")
        print(f"📋 Bot ID: {client.user.id}")
        print(f"🏷️ Bot discriminator: {client.user.discriminator}")
        print(f"📊 Connected to {len(client.guilds)} servers:")
        
        for guild in client.guilds:
            print(f"   • {guild.name} (ID: {guild.id})")
            # Find mac-claude channel
            for channel in guild.text_channels:
                if 'claude' in channel.name.lower():
                    print(f"     📢 Found channel: #{channel.name}")
        
        await client.close()
    
    @client.event
    async def on_error(event, *args, **kwargs):
        print(f"❌ Error in {event}")
        import traceback
        traceback.print_exc()
    
    try:
        await client.start(TOKEN)
    except discord.LoginFailure:
        print("❌ Token is INVALID or expired!")
        print("You need to get a new token from Discord Developer Portal")
    except Exception as e:
        print(f"❌ Connection error: {e}")

# Run test
print("🔍 Testing Discord bot token...")
print("=" * 50)
asyncio.run(test_token())