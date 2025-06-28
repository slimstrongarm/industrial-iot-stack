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
    print(f'Guilds: {[g.name for g in bot.guilds]}')
    # Find the correct channels
    for guild in bot.guilds:
        print(f'Checking guild: {guild.name}')
        for channel in guild.channels:
            print(f'  Channel: {channel.name}')
            if channel.name == 'mac-claude':
                print(f'  Found mac-claude channel!')
                await channel.send("🟢 Mac Claude bot online and monitoring!")

@bot.event
async def on_message(message):
    # Don't respond to self
    if message.author == bot.user:
        return
    
    # Monitor mac-claude channel  
    if message.channel.name == 'mac-claude':
        # Natural language processing
        if 'status' in message.content.lower():
            # Check Docker status
            result = subprocess.run(['docker', 'ps', '--format', 'table {{.Names}}	{{.Status}}'], 
                                  capture_output=True, text=True)
            await message.channel.send(f"```\n{result.stdout}\n```")
        
        elif 'mqtt' in message.content.lower():
            # Check MQTT broker
            result = subprocess.run(['docker', 'logs', '--tail', '10', 'emqx'], 
                                  capture_output=True, text=True)
            await message.channel.send(f"MQTT Broker logs:\n```\n{result.stdout[-1000:]}\n```")
        
        elif 'help' in message.content.lower():
            help_text = '''
**Mac Claude Commands:**
• Ask about **status** - Show local services
• Mention **mqtt** - Check MQTT broker (Mosquitto)
• Say **git** - Show repository status
• Ask about **logs** - Show recent logs
• Mention **deploy** - Deploy latest changes to server
            '''
            await message.channel.send(help_text)

# Run bot
bot.run(os.environ['DISCORD_BOT_TOKEN'])