#!/usr/bin/env python3
import os
import subprocess
import signal
import time

# Kill existing bot processes
try:
    subprocess.run(['pkill', '-f', 'industrial_iot_claude_bot.py'], check=False)
    print("🛑 Stopped existing bot processes")
    time.sleep(2)
except:
    print("No existing processes found")

# Set environment
os.environ['DISCORD_BOT_TOKEN'] = 'MTM4MDQxOTk0NTk3NTc3OTM3OA.G9KB9Q.jODzGUt8TnHyaqAAy0KbB4tdalezysXG-_6xJ4'

# Change to project directory
os.chdir('/Users/joshpayneair/Desktop/industrial-iot-stack')

# Start the bot
print("🚀 Starting Discord bot with start task feature...")
subprocess.Popen([
    'python3', 
    'discord-bot/industrial_iot_claude_bot.py'
], stdout=open('discord_bot.log', 'w'), stderr=subprocess.STDOUT)

print("✅ Bot started!")
print("📝 New feature: @Mac Claude Bot start task CT-XXX")
print("📄 Logs: discord_bot.log")