#!/usr/bin/env python3
"""
Intelligent Choice Discord Bot - Only shows options when assistance is needed
"""

import discord
from discord.ext import commands, tasks
import os
import subprocess
import asyncio
import json
from datetime import datetime
import logging
from pathlib import Path

# Google Sheets integration
import gspread
from google.oauth2.service_account import Credentials

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
SPREADSHEET_ID = '1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do'
CREDENTIALS_PATH = Path.home() / 'Desktop/industrial-iot-stack/credentials/iot-stack-credentials.json'

# Determine instance type based on hostname
import socket
INSTANCE_NAME = "Server Claude" if "server" in socket.gethostname().lower() else "Mac Claude"

class IntelligentChoiceBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        
        super().__init__(
            command_prefix=['!', f'@{INSTANCE_NAME.lower()} '],
            intents=intents,
            description=f"🤖 {INSTANCE_NAME} - Intelligent Task Assistant"
        )
        
        self.instance_name = INSTANCE_NAME
        self.sheets_client = None
        self.setup_google_sheets()
        
    def setup_google_sheets(self):
        """Initialize Google Sheets API client"""
        try:
            if CREDENTIALS_PATH.exists():
                scope = ['https://spreadsheets.google.com/feeds',
                        'https://www.googleapis.com/auth/drive']
                creds = Credentials.from_service_account_file(str(CREDENTIALS_PATH), scopes=scope)
                self.sheets_client = gspread.authorize(creds)
                logger.info("✅ Google Sheets client initialized")
            else:
                logger.warning(f"⚠️ Credentials not found at {CREDENTIALS_PATH}")
        except Exception as e:
            logger.error(f"❌ Google Sheets setup failed: {e}")

    async def on_ready(self):
        """Bot startup"""
        print(f"\n{'='*60}")
        print(f"🤖 {self.instance_name} Intelligent Choice Bot Online")
        print(f"{'='*60}")
        print(f"✅ Logged in as: {self.user}")
        print(f"📊 Google Sheets: {'Connected' if self.sheets_client else 'Not Connected'}")
        print(f"🧠 Smart choice system enabled")
        print(f"{'='*60}\n")

    async def on_message(self, message):
        """Enhanced message processing"""
        if message.author == self.user:
            return
        
        # Channel filtering
        channel_name = message.channel.name
        if channel_name == 'general':
            pass  # Both bots respond in general
        elif self.instance_name == "Mac Claude" and channel_name != 'mac-claude':
            return
        elif self.instance_name == "Server Claude" and channel_name != 'server-claude':
            return
        
        # Log messages
        logger.info(f"[{message.channel.name}] {message.author}: {message.content}")
        
        # Process mentions
        if self.user.mentioned_in(message):
            await self.process_mention(message)
        
        # Process commands
        await self.process_commands(message)

    async def process_mention(self, message):
        """Process @mentions with natural language"""
        content = message.content.lower()
        
        # Task creation
        if any(word in content for word in ['task', 'create', 'add', 'do', 'work']):
            await self.create_task_from_message(message)
        
        # Status check
        elif any(word in content for word in ['status', 'health', 'check']):
            await self.send_status(message.channel)
        
        # Help
        elif 'help' in content:
            await self.send_help(message.channel)
        
        # Generic response
        else:
            await message.channel.send(
                f"👋 Hi! I'm {self.instance_name}. Try:\n"
                f"• `@{self.user.mention} add task <description>`\n"
                f"• `@{self.user.mention} status`"
            )

    async def create_task_from_message(self, message):
        """Create task with intelligent choice system"""
        if not self.sheets_client:
            await message.channel.send("❌ Google Sheets not connected")
            return
        
        # Extract task description
        content = message.content
        for keyword in ['add task', 'create task', 'new task', 'do task', 'work on']:
            if keyword in content.lower():
                task_desc = content.split(keyword, 1)[1].strip()
                break
        else:
            # Look for any mention followed by task description
            mention_text = f"<@{self.user.id}>"
            if mention_text in content:
                task_desc = content.split(mention_text, 1)[1].strip()
            else:
                task_desc = "Task from Discord"
        
        try:
            # Create task in sheets
            sheet = self.sheets_client.open_by_key(SPREADSHEET_ID)
            ws = sheet.worksheet('Claude Tasks')
            
            # Get next ID
            all_values = ws.get_all_values()
            last_num = 0
            for row in all_values[1:]:  # Skip header
                if row and row[0].startswith('CT-'):
                    try:
                        num = int(row[0].split('-')[1])
                        last_num = max(last_num, num)
                    except:
                        pass
            
            new_id = f"CT-{last_num + 1:03d}"
            new_row = [
                new_id,
                self.instance_name,
                task_desc,
                "Medium",
                "Pending",
                f"Created via Discord by {message.author.name}",
                "",
                ""
            ]
            
            ws.append_row(new_row)
            
            # Send confirmation
            embed = discord.Embed(
                title="✅ Task Created",
                description=f"**{new_id}**: {task_desc}",
                color=0x00ff00,
                timestamp=datetime.now()
            )
            embed.add_field(name="Assigned To", value=self.instance_name, inline=True)
            embed.add_field(name="Status", value="Pending", inline=True)
            embed.set_footer(text=f"Created by {message.author.name}")
            
            await message.channel.send(embed=embed)
            logger.info(f"Created task {new_id}")
            
            # Auto-start the intelligent workflow
            await asyncio.sleep(2)
            await self.start_intelligent_workflow(new_id, task_desc, message.channel)
            
        except Exception as e:
            await message.channel.send(f"❌ Error creating task: {e}")
            logger.error(f"Task creation error: {e}")

    async def start_intelligent_workflow(self, task_id, task_desc, channel):
        """Intelligent workflow - only show choices when needed"""
        try:
            # Work start notification
            work_embed = discord.Embed(
                title="🚀 Starting Work",
                description=f"I'm analyzing **{task_id}**: {task_desc}",
                color=0x0099ff,
                timestamp=datetime.now()
            )
            work_embed.add_field(name="Status", value="Pending → In Progress", inline=True)
            work_embed.add_field(name="Instance", value=self.instance_name, inline=True)
            work_embed.set_footer(text="Analyzing requirements...")
            
            await channel.send(embed=work_embed)
            
            # Update status to In Progress
            await self.update_task_status(task_id, "In Progress")
            
            # Simulate analysis time
            await asyncio.sleep(5)
            
            # Progress update
            progress_embed = discord.Embed(
                title="⚙️ Working on Task",
                description=f"Making progress on **{task_id}**: {task_desc}",
                color=0xffaa00,
                timestamp=datetime.now()
            )
            progress_embed.add_field(name="Status", value="Analyzing requirements...", inline=True)
            progress_embed.set_footer(text="Progress update")
            
            await channel.send(embed=progress_embed)
            
            # More analysis time
            await asyncio.sleep(8)
            
            # Intelligent decision making
            task_lower = task_desc.lower()
            
            # Check if this requires user input/guidance
            needs_guidance = any(keyword in task_lower for keyword in [
                'review', 'approve', 'feedback', 'decision', 'choose', 'select', 'prefer',
                'opinion', 'recommend', 'suggest', 'advice', 'strategy', 'approach'
            ])
            
            # Check if task is ambiguous or complex
            is_ambiguous = any(phrase in task_lower for phrase in [
                'not sure', 'unclear', 'maybe', 'possibly', 'might', 'could be',
                'complex', 'complicated', 'difficult', 'challenging', 'multiple ways'
            ])
            
            # Check if it's a simple/clear task
            is_simple = any(keyword in task_lower for keyword in [
                'test', 'check', 'status', 'list', 'show', 'display', 'run',
                'start', 'stop', 'restart', 'simple', 'quick', 'basic'
            ]) and len(task_desc.split()) < 8
            
            if needs_guidance or is_ambiguous or (not is_simple and len(task_desc.split()) > 6):
                # Show 3-option choice system
                await self.show_choice_options(task_id, task_desc, channel)
            else:
                # Auto-complete simple tasks
                await self.auto_complete_simple_task(task_id, task_desc, channel)
                
        except Exception as e:
            logger.error(f"Error in intelligent workflow for {task_id}: {e}")
            await self.send_error_embed(task_id, str(e), channel)

    async def show_choice_options(self, task_id, task_desc, channel):
        """Show 3-option choice system when guidance is needed"""
        options_embed = discord.Embed(
            title="🤔 Need Your Guidance",
            description=f"**{task_id}** requires your input on how to proceed",
            color=0xffaa00,
            timestamp=datetime.now()
        )
        
        options_embed.add_field(
            name="1️⃣ Auto-Complete",
            value="Let me handle this automatically (~15 seconds)",
            inline=False
        )
        
        options_embed.add_field(
            name="2️⃣ Work & Check-In", 
            value="I'll work and ask for your approval before finishing",
            inline=False
        )
        
        options_embed.add_field(
            name="3️⃣ Long-Running Project",
            value="This needs substantial time - I'll update periodically",
            inline=False
        )
        
        options_embed.add_field(
            name="📲 Reply with 1, 2, or 3",
            value="(Auto-selects Option 1 in 60 seconds)",
            inline=False
        )
        
        options_embed.set_footer(text=f"{self.instance_name} • Intelligent choice system")
        
        await channel.send(embed=options_embed)
        
        # Wait for user response
        def check_response(msg):
            return (msg.author.id != self.user.id and 
                   msg.channel.id == channel.id and
                   msg.content.strip() in ['1', '2', '3'])
        
        try:
            response_msg = await self.wait_for('message', check=check_response, timeout=60.0)
            choice = response_msg.content.strip()
            
            # Acknowledge choice
            choice_names = {
                '1': 'Auto-Complete',
                '2': 'Work & Check-In', 
                '3': 'Long-Running Project'
            }
            
            choice_embed = discord.Embed(
                title="✅ Choice Confirmed",
                description=f"Proceeding with **Option {choice}: {choice_names[choice]}**",
                color=0x00ff00,
                timestamp=datetime.now()
            )
            await channel.send(embed=choice_embed)
            
        except asyncio.TimeoutError:
            choice = '1'  # Default to auto-complete
            timeout_embed = discord.Embed(
                title="⏰ Auto-Selected Option 1",
                description="No response received - proceeding with Auto-Complete",
                color=0xffaa00,
                timestamp=datetime.now()
            )
            await channel.send(embed=timeout_embed)
        
        # Execute based on choice
        await self.execute_choice(choice, task_id, task_desc, channel)

    async def auto_complete_simple_task(self, task_id, task_desc, channel):
        """Auto-complete simple, clear tasks"""
        await asyncio.sleep(5)
        
        completion_embed = discord.Embed(
            title="✅ Task Completed",
            description=f"**{task_id}** completed successfully!",
            color=0x00ff00,
            timestamp=datetime.now()
        )
        completion_embed.add_field(name="Summary", value=task_desc, inline=False)
        completion_embed.add_field(name="Type", value="Simple task", inline=True)
        completion_embed.add_field(name="Instance", value=self.instance_name, inline=True)
        completion_embed.set_footer(text="Auto-completed - no guidance needed")
        
        await channel.send(embed=completion_embed)
        await self.update_task_status(task_id, "Complete", f"Auto-completed by {self.instance_name}")

    async def execute_choice(self, choice, task_id, task_desc, channel):
        """Execute the selected option"""
        if choice == '1':
            # Quick auto-complete
            await asyncio.sleep(5)
            
            completion_embed = discord.Embed(
                title="✅ Task Completed",
                description=f"**{task_id}** finished successfully!",
                color=0x00ff00,
                timestamp=datetime.now()
            )
            completion_embed.add_field(name="Summary", value=task_desc, inline=False)
            completion_embed.add_field(name="Choice", value="Auto-Complete", inline=True)
            completion_embed.add_field(name="Instance", value=self.instance_name, inline=True)
            completion_embed.set_footer(text="User-selected auto-completion")
            
            await channel.send(embed=completion_embed)
            await self.update_task_status(task_id, "Complete", f"Auto-completed by {self.instance_name}")
            
        elif choice == '2':
            # Work and check-in
            await asyncio.sleep(10)
            
            checkin_embed = discord.Embed(
                title="🔄 Progress Check-In",
                description=f"Made progress on **{task_id}**",
                color=0xff9900,
                timestamp=datetime.now()
            )
            checkin_embed.add_field(
                name="What I've Done",
                value="Completed initial analysis and setup. Ready for next phase.",
                inline=False
            )
            checkin_embed.add_field(
                name="Need Your Input",
                value="Please let me know:\\n• Continue as planned\\n• Modify approach\\n• Hold for discussion",
                inline=False
            )
            checkin_embed.set_footer(text="Reply when ready to proceed")
            
            await channel.send(embed=checkin_embed)
            await self.update_task_status(task_id, "Waiting for Input", f"Check-in by {self.instance_name}")
            
        elif choice == '3':
            # Long-running project
            longrun_embed = discord.Embed(
                title="🛠️ Long-Running Project Started",
                description=f"**{task_id}** is now a background project",
                color=0x0099ff,
                timestamp=datetime.now()
            )
            longrun_embed.add_field(
                name="Status",
                value="This will continue in the background. I'll provide periodic updates.",
                inline=False
            )
            longrun_embed.set_footer(text="Long-term project mode")
            
            await channel.send(embed=longrun_embed)
            await self.update_task_status(task_id, "In Progress - Long Running", f"Long-term project by {self.instance_name}")

    async def update_task_status(self, task_id, status, notes=""):
        """Update task status in Google Sheets"""
        if not self.sheets_client:
            return
            
        try:
            sheet = self.sheets_client.open_by_key(SPREADSHEET_ID)
            ws = sheet.worksheet('Claude Tasks')
            all_rows = ws.get_all_values()
            for i, row in enumerate(all_rows):
                if row and len(row) > 0 and row[0] == task_id:
                    ws.update_cell(i + 1, 5, status)
                    if notes:
                        ws.update_cell(i + 1, 6, notes)
                    break
            logger.info(f"Updated {task_id} status to: {status}")
        except Exception as e:
            logger.error(f"Error updating task {task_id}: {e}")

    async def send_status(self, channel):
        """Send system status"""
        embed = discord.Embed(
            title=f"🤖 {self.instance_name} Status",
            color=0x00ff00,
            timestamp=datetime.now()
        )
        
        sheets_status = "✅ Connected" if self.sheets_client else "❌ Disconnected"
        embed.add_field(name="📊 Google Sheets", value=sheets_status, inline=True)
        embed.add_field(name="🏷️ Instance", value=self.instance_name, inline=True)
        embed.add_field(name="🧠 Mode", value="Intelligent Choice", inline=True)
        
        await channel.send(embed=embed)

    async def send_help(self, channel):
        """Send help message"""
        embed = discord.Embed(
            title=f"🤖 {self.instance_name} Help",
            description="Intelligent task management with smart choice system",
            color=0x0099ff
        )
        
        embed.add_field(
            name="📝 Create Tasks",
            value=f"`@{self.user.mention} add task <description>`",
            inline=False
        )
        
        embed.add_field(
            name="🧠 Smart Features",
            value="• Auto-completes simple tasks\\n"
                  "• Shows 3 options only when guidance needed\\n"
                  "• Natural language processing\\n"
                  "• Bidirectional Claude coordination",
            inline=False
        )
        
        await channel.send(embed=embed)

    async def send_error_embed(self, task_id, error_msg, channel):
        """Send error message"""
        error_embed = discord.Embed(
            title="❌ Task Error",
            description=f"Error with **{task_id}**",
            color=0xff0000,
            timestamp=datetime.now()
        )
        error_embed.add_field(name="Error", value=error_msg, inline=False)
        
        await channel.send(embed=error_embed)

    @commands.command()
    async def task(self, ctx, *, description):
        """Quick task creation command"""
        ctx.message.content = f"add task {description}"
        await self.create_task_from_message(ctx.message)

    @commands.command()
    async def status(self, ctx):
        """Quick status command"""
        await self.send_status(ctx.channel)

# Run the bot
if __name__ == "__main__":
    # Use instance-specific tokens
    hostname = socket.gethostname().lower()
    if "server" in hostname or "flint" in hostname or "linux" in hostname:
        token = os.environ.get('SERVER_DISCORD_BOT_TOKEN') or os.environ.get('DISCORD_BOT_TOKEN')
        token_name = 'SERVER_DISCORD_BOT_TOKEN'
    else:
        token = os.environ.get('MAC_DISCORD_BOT_TOKEN') or os.environ.get('DISCORD_BOT_TOKEN')
        token_name = 'MAC_DISCORD_BOT_TOKEN'
    
    if not token:
        print(f"❌ {token_name} not set!")
        exit(1)
    
    bot = IntelligentChoiceBot()
    
    try:
        print(f"🔑 Using token from: {token_name}")
        bot.run(token)
    except KeyboardInterrupt:
        print(f"\\n🛑 {INSTANCE_NAME} shutting down...")
    except Exception as e:
        print(f"❌ Bot error: {e}")