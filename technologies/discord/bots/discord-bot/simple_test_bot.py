#!/usr/bin/env python3
"""
Simple Discord bot to test message capture and Google Sheets
"""

import discord
import os
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

# Bot token
TOKEN = os.environ.get('DISCORD_BOT_TOKEN')
if not TOKEN:
    print("❌ DISCORD_BOT_TOKEN environment variable not set")
    exit(1)

# Google Sheets config
SPREADSHEET_ID = '1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do'
CREDENTIALS_PATH = '/Users/joshpayneair/Desktop/industrial-iot-stack/credentials/iot-stack-credentials.json'

class SimpleBot(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(intents=intents)
        
        # Setup Google Sheets
        try:
            scope = ['https://spreadsheets.google.com/feeds',
                    'https://www.googleapis.com/auth/drive']
            creds = Credentials.from_service_account_file(CREDENTIALS_PATH, scopes=scope)
            self.gc = gspread.authorize(creds)
            print("✅ Google Sheets connected")
        except Exception as e:
            print(f"❌ Google Sheets error: {e}")
            self.gc = None
    
    async def on_ready(self):
        print(f'🤖 Bot logged in as {self.user}')
        print(f'📋 Bot ID: {self.user.id}')
        print('💬 Listening for messages...')
        print('Try: @Mac Claude Bot add task Test message')
    
    async def on_message(self, message):
        # Log every message
        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Message from {message.author}: {message.content}")
        
        # Don't respond to self
        if message.author == self.user:
            return
        
        # Check if bot is mentioned
        if self.user.mentioned_in(message):
            print("✅ Bot was mentioned!")
            
            # Simple task creation
            if 'add task' in message.content.lower() or 'create task' in message.content.lower():
                print("📝 Task creation detected")
                
                # Extract task description
                content = message.content.lower()
                if 'add task' in content:
                    task_desc = message.content.split('add task', 1)[1].strip()
                elif 'create task' in content:
                    task_desc = message.content.split('create task', 1)[1].strip()
                else:
                    task_desc = "Unknown task"
                
                if self.gc:
                    try:
                        # Open sheet
                        sheet = self.gc.open_by_key(SPREADSHEET_ID)
                        ws = sheet.worksheet('Claude Tasks')
                        
                        # Get last task ID
                        all_values = ws.get_all_values()
                        last_num = 0
                        for row in all_values:
                            if row and row[0].startswith('CT-'):
                                try:
                                    num = int(row[0].split('-')[1])
                                    if num > last_num:
                                        last_num = num
                                except:
                                    pass
                        
                        # Create new task
                        new_id = f"CT-{last_num + 1:03d}"
                        new_row = [
                            new_id,
                            "Discord Bot",
                            task_desc,
                            "Medium",
                            "Pending",
                            f"Created via Discord by {message.author.name}",
                            "",
                            ""
                        ]
                        
                        ws.append_row(new_row)
                        
                        await message.channel.send(f"✅ Created task **{new_id}**: {task_desc}")
                        print(f"✅ Created {new_id} in Google Sheets")
                        
                    except Exception as e:
                        await message.channel.send(f"❌ Error creating task: {str(e)}")
                        print(f"❌ Error: {e}")
                else:
                    await message.channel.send("❌ Google Sheets not connected")
            
            # Simple status command
            elif 'status' in message.content.lower():
                await message.channel.send("🤖 Bot is online and working!")
                print("✅ Sent status response")

# Run bot
bot = SimpleBot()
bot.run(TOKEN)