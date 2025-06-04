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
            result = subprocess.run(['docker', 'ps', '--format', 'table {{.Names}}	{{.Status}}'], 
                                  capture_output=True, text=True)
            await message.channel.send(f"```
{result.stdout}
```")
        
        elif 'mqtt' in message.content.lower():
            # Check MQTT broker
            result = subprocess.run(['docker', 'logs', '--tail', '10', 'emqx'], 
                                  capture_output=True, text=True)
            await message.channel.send(f"MQTT Broker logs:
```
{result.stdout[-1000:]}
```")
        
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