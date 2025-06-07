#!/usr/bin/env python3
"""
Discord Bot Setup Instructions for Server Claude
Quick deployment guide for development coordination bot
"""

import json
from datetime import datetime
from pathlib import Path

def create_bot_setup():
    """Create Discord bot setup instructions for Server Claude"""
    
    # Bot setup instructions
    setup_guide = {
        "task": "CT-022",
        "purpose": "Development coordination bot for Josh",
        "quick_steps": [
            {
                "step": 1,
                "action": "Create Discord Application",
                "url": "https://discord.com/developers/applications",
                "details": [
                    "Click 'New Application'",
                    "Name: 'IoT Stack Claude Bot'",
                    "Create application"
                ]
            },
            {
                "step": 2,
                "action": "Create Bot User",
                "details": [
                    "Go to 'Bot' section",
                    "Click 'Add Bot'",
                    "Copy bot token (save securely)",
                    "Enable 'Message Content Intent'"
                ]
            },
            {
                "step": 3,
                "action": "Generate Invite Link",
                "details": [
                    "Go to 'OAuth2' → 'URL Generator'",
                    "Select 'bot' scope",
                    "Select permissions: Send Messages, Read Message History, Use Slash Commands",
                    "Copy generated URL"
                ]
            }
        ],
        "bot_code_template": """
import discord
from discord.ext import commands
import os
import subprocess
import asyncio

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    # Find the correct channels
    for guild in bot.guilds:
        for channel in guild.channels:
            if channel.name == 'server-claude':
                await channel.send("🟢 Server Claude bot online and monitoring!")

@bot.event
async def on_message(message):
    # Don't respond to self
    if message.author == bot.user:
        return
    
    # Monitor server-claude channel
    if message.channel.name == 'server-claude':
        # Natural language processing
        if 'status' in message.content.lower():
            # Check Docker status
            result = subprocess.run(['docker', 'ps', '--format', 'table {{.Names}}\t{{.Status}}'], 
                                  capture_output=True, text=True)
            await message.channel.send(f"```\n{result.stdout}\n```")
        
        elif 'mqtt' in message.content.lower():
            # Check MQTT broker
            result = subprocess.run(['docker', 'logs', '--tail', '10', 'emqx'], 
                                  capture_output=True, text=True)
            await message.channel.send(f"MQTT Broker logs:\n```\n{result.stdout[-1000:]}\n```")
        
        elif 'help' in message.content.lower():
            help_text = '''
**Server Claude Commands:**
• Ask about **status** - Show Docker containers
• Mention **mqtt** - Check MQTT broker
• Say **restart [container]** - Restart a container
• Ask about **logs** - Show recent logs
• Mention **deploy** - Deploy latest changes
            '''
            await message.channel.send(help_text)

# Run bot
bot.run(os.environ['DISCORD_BOT_TOKEN'])
""",
        "deployment": {
            "dockerfile": """
FROM python:3.9-slim
WORKDIR /app
RUN pip install discord.py python-dotenv
COPY bot.py .
CMD ["python", "bot.py"]
""",
            "docker_compose": """
services:
  discord-bot:
    build: .
    container_name: discord-claude-bot
    environment:
      - DISCORD_BOT_TOKEN=${DISCORD_BOT_TOKEN}
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    restart: unless-stopped
"""
        }
    }
    
    # Save setup guide
    setup_dir = Path.home() / 'Desktop/industrial-iot-stack/discord-bot'
    setup_dir.mkdir(exist_ok=True)
    
    # Write files
    with open(setup_dir / 'setup_instructions.json', 'w') as f:
        json.dump(setup_guide, f, indent=2)
    
    with open(setup_dir / 'bot.py', 'w') as f:
        f.write(setup_guide['bot_code_template'].strip())
    
    with open(setup_dir / 'Dockerfile', 'w') as f:
        f.write(setup_guide['deployment']['dockerfile'].strip())
    
    with open(setup_dir / 'docker-compose.yml', 'w') as f:
        f.write(setup_guide['deployment']['docker_compose'].strip())
    
    print(f"✅ Discord bot setup files created in: {setup_dir}")
    print("\n📋 Quick Start for Server Claude:")
    print("1. Create Discord app at https://discord.com/developers")
    print("2. Copy bot token")
    print("3. Deploy with: docker-compose up -d")
    print("\n⏱️ Estimated time: 10-15 minutes")

if __name__ == "__main__":
    create_bot_setup()