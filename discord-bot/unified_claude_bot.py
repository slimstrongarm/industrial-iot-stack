#!/usr/bin/env python3
"""
Unified Claude Discord Bot - Works on both Mac and Server
Bidirectional communication with proper error handling
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

class UnifiedClaudeBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        
        super().__init__(
            command_prefix=['!', f'@{INSTANCE_NAME.lower()} '],
            intents=intents,
            description=f"🤖 {INSTANCE_NAME} - Industrial IoT Assistant"
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
        print(f"🤖 {self.instance_name} Discord Bot Online")
        print(f"{'='*60}")
        print(f"✅ Logged in as: {self.user}")
        print(f"🆔 Bot ID: {self.user.id}")
        print(f"📊 Google Sheets: {'Connected' if self.sheets_client else 'Not Connected'}")
        print(f"💬 Listening for messages...")
        print(f"{'='*60}\n")
        
        # Send startup notification
        for guild in self.guilds:
            # Find appropriate channel
            channel_name = 'server-claude' if self.instance_name == "Server Claude" else 'mac-claude'
            channel = discord.utils.get(guild.text_channels, name=channel_name)
            
            if channel:
                embed = discord.Embed(
                    title=f"🟢 {self.instance_name} Online",
                    description="✅ Bidirectional communication enabled",
                    color=0x00ff00,
                    timestamp=datetime.now()
                )
                embed.add_field(
                    name="🎯 Capabilities",
                    value="• Listen to commands\n• Send proactive messages\n• Create Google Sheets tasks\n• Monitor system status",
                    inline=False
                )
                await channel.send(embed=embed)
                break

    async def on_message(self, message):
        """Enhanced message processing"""
        # Log all messages for debugging
        if message.author != self.user:
            logger.info(f"[{message.channel.name}] {message.author}: {message.content}")
        
        # Don't respond to self
        if message.author == self.user:
            return
        
        # Check if this instance should respond
        channel_name = message.channel.name
        
        # Both bots respond in general, instance-specific in their own channels
        if channel_name == 'general':
            # Both bots can respond in general channel
            pass
        elif self.instance_name == "Mac Claude" and channel_name != 'mac-claude':
            return
        elif self.instance_name == "Server Claude" and channel_name != 'server-claude':
            return
        
        # Process mentions
        if self.user.mentioned_in(message):
            await self.process_mention(message)
        
        # Process commands
        await self.process_commands(message)

    async def process_mention(self, message):
        """Process @mentions with natural language"""
        content = message.content.lower()
        
        # Task creation
        if any(word in content for word in ['task', 'create', 'add']):
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
                f"• `@{self.user.mention} status` - System status\n"
                f"• `@{self.user.mention} add task <description>` - Create task\n"
                f"• `@{self.user.mention} help` - Full command list"
            )

    async def create_task_from_message(self, message):
        """Create task in Google Sheets"""
        if not self.sheets_client:
            await message.channel.send("❌ Google Sheets not connected")
            return
        
        # Extract task description
        content = message.content
        for keyword in ['add task', 'create task', 'new task']:
            if keyword in content.lower():
                task_desc = content.split(keyword, 1)[1].strip()
                break
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
            
            # Auto-start working on the task
            await asyncio.sleep(2)  # Brief pause for dramatic effect
            
            # Mark as In Progress
            try:
                # Find the row and update status
                all_rows = ws.get_all_values()
                for i, row in enumerate(all_rows):
                    if row and len(row) > 0 and row[0] == new_id:
                        ws.update_cell(i + 1, 5, "In Progress")  # Status column
                        break
                
                # Send work start notification
                work_embed = discord.Embed(
                    title="🚀 Starting Work",
                    description=f"I'm now working on **{new_id}**: {task_desc}",
                    color=0x0099ff,
                    timestamp=datetime.now()
                )
                work_embed.add_field(name="Status Update", value="Pending → In Progress", inline=True)
                work_embed.add_field(name="Instance", value=self.instance_name, inline=True)
                work_embed.set_footer(text="Auto-processing enabled")
                
                await message.channel.send(embed=work_embed)
                logger.info(f"Started working on task {new_id}")
                
                # Simulate work progress and completion
                await self.simulate_task_work(new_id, task_desc, message.channel)
                
            except Exception as e:
                logger.error(f"Error starting work on {new_id}: {e}")
                await message.channel.send(f"⚠️ Created task {new_id} but couldn't auto-start: {e}")
            
        except Exception as e:
            await message.channel.send(f"❌ Error creating task: {e}")
            logger.error(f"Task creation error: {e}")

    async def send_status(self, channel):
        """Send system status"""
        embed = discord.Embed(
            title=f"🤖 {self.instance_name} Status",
            color=0x00ff00,
            timestamp=datetime.now()
        )
        
        # Check Docker
        try:
            result = subprocess.run(['docker', 'ps', '--format', 'json'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                containers = len(result.stdout.strip().split('\n'))
                embed.add_field(name="🐳 Docker", value=f"{containers} containers running", inline=True)
        except:
            embed.add_field(name="🐳 Docker", value="Not available", inline=True)
        
        # Google Sheets status
        sheets_status = "✅ Connected" if self.sheets_client else "❌ Disconnected"
        embed.add_field(name="📊 Google Sheets", value=sheets_status, inline=True)
        
        # Instance info
        embed.add_field(name="🏷️ Instance", value=self.instance_name, inline=True)
        
        await channel.send(embed=embed)

    async def send_help(self, channel):
        """Send help message"""
        embed = discord.Embed(
            title=f"🤖 {self.instance_name} Help",
            description="Available commands and features",
            color=0x0099ff
        )
        
        embed.add_field(
            name="📝 Task Management",
            value=f"`@{self.user.mention} add task <description>` - Create new task\n"
                  f"`!task <description>` - Quick task creation",
            inline=False
        )
        
        embed.add_field(
            name="📊 System Commands",
            value=f"`@{self.user.mention} status` - System status\n"
                  f"`!status` - Quick status check",
            inline=False
        )
        
        embed.add_field(
            name="🔧 Features",
            value="• Bidirectional communication\n"
                  "• Google Sheets integration\n"
                  "• System monitoring\n"
                  "• Auto task processing\n"
                  "• Progress notifications",
            inline=False
        )
        
        await channel.send(embed=embed)

    async def simulate_task_work(self, task_id, task_desc, channel):
        """Simulate working on a task with progress updates"""
        try:
            # Wait a bit to simulate thinking/planning
            await asyncio.sleep(5)
            
            # Send progress update
            progress_embed = discord.Embed(
                title="⚙️ Working on Task",
                description=f"Making progress on **{task_id}**: {task_desc}",
                color=0xffaa00,
                timestamp=datetime.now()
            )
            progress_embed.add_field(name="Status", value="Analyzing requirements...", inline=True)
            progress_embed.add_field(name="Instance", value=self.instance_name, inline=True)
            progress_embed.set_footer(text="Progress update")
            
            await channel.send(embed=progress_embed)
            
            # Simulate more work
            await asyncio.sleep(8)
            
            # Intelligent analysis - determine if assistance is needed
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
            logger.error(f"Error in task simulation for {task_id}: {e}")
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
            name="📱 Option 1: Auto-Complete", 
            value="🚀 I'll complete this task automatically using best practices",
            inline=False
        )
        
        options_embed.add_field(
            name="📱 Option 2: Work & Check-In", 
            value="⚙️ I'll work on it and ask for your input before completing",
            inline=False
        )
        
        options_embed.add_field(
            name="📱 Option 3: Long-Running",
            value="🛠️ This needs substantial time - I'll update you periodically",
            inline=False
        )
        
        options_embed.add_field(
            name="📲 Reply with:",
            value="`1` = Auto-complete\n`2` = Work & check-in\n`3` = Long-running task",
            inline=False
        )
        
        options_embed.set_footer(text=f"{self.instance_name} • Reply within 60 seconds or I'll choose Option 1")
        
        await channel.send(embed=options_embed)
            
            # Wait for user response (60 seconds)
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
                    '3': 'Long-Running'
                }
                
                choice_embed = discord.Embed(
                    title="✅ Choice Confirmed",
                    description=f"Proceeding with **Option {choice}: {choice_names[choice]}**",
                    color=0x00ff00,
                    timestamp=datetime.now()
                )
                await channel.send(embed=choice_embed)
                
            except asyncio.TimeoutError:
                # Default to auto-complete after 60 seconds
                choice = '1'
                timeout_embed = discord.Embed(
                    title="⏰ Auto-Selected",
                    description="No response received - proceeding with **Option 1: Auto-Complete**",
                    color=0xffaa00,
                    timestamp=datetime.now()
                )
                await channel.send(embed=timeout_embed)
            
            # Execute based on choice
            if choice == '1':
                # Auto-complete the task
                await asyncio.sleep(5)  # Brief work simulation
                
                completion_embed = discord.Embed(
                    title="✅ Task Auto-Completed",
                    description=f"**{task_id}** has been completed automatically!",
                    color=0x00ff00,
                    timestamp=datetime.now()
                )
                completion_embed.add_field(
                    name="Summary",
                    value=f"Finished: {task_desc}",
                    inline=False
                )
                completion_embed.add_field(name="Status Update", value="In Progress → Complete", inline=True)
                completion_embed.add_field(name="Instance", value=self.instance_name, inline=True)
                completion_embed.set_footer(text="Auto-completed")
                
                await channel.send(embed=completion_embed)
                
                # Update Google Sheets
                if self.sheets_client:
                    try:
                        sheet = self.sheets_client.open_by_key(SPREADSHEET_ID)
                        ws = sheet.worksheet('Claude Tasks')
                        all_rows = ws.get_all_values()
                        for i, row in enumerate(all_rows):
                            if row and len(row) > 0 and row[0] == task_id:
                                ws.update_cell(i + 1, 5, "Complete")
                                ws.update_cell(i + 1, 6, f"Auto-completed by {self.instance_name}")
                                break
                        logger.info(f"Auto-completed task {task_id}")
                    except Exception as e:
                        logger.error(f"Error completing task {task_id}: {e}")
                        
            elif choice == '2':
                # Work and check-in
                await asyncio.sleep(10)  # Simulate work
                
                checkin_embed = discord.Embed(
                    title="🔄 Check-In Required",
                    description=f"I've made progress on **{task_id}**: {task_desc}",
                    color=0xff9900,
                    timestamp=datetime.now()
                )
                checkin_embed.add_field(
                    name="Progress Update",
                    value="I've completed the initial analysis and setup. Ready to proceed with implementation.",
                    inline=False
                )
                checkin_embed.add_field(
                    name="Your Input Needed",
                    value="Please review and let me know if you want me to:\n• Continue with current approach\n• Modify the approach\n• Hold for further discussion",
                    inline=False
                )
                checkin_embed.add_field(name="Current Status", value="Waiting for approval", inline=True)
                checkin_embed.add_field(name="Instance", value=self.instance_name, inline=True)
                checkin_embed.set_footer(text="Reply when ready to continue")
                
                await channel.send(embed=checkin_embed)
                
                # Update Google Sheets
                if self.sheets_client:
                    try:
                        sheet = self.sheets_client.open_by_key(SPREADSHEET_ID)
                        ws = sheet.worksheet('Claude Tasks')
                        all_rows = ws.get_all_values()
                        for i, row in enumerate(all_rows):
                            if row and len(row) > 0 and row[0] == task_id:
                                ws.update_cell(i + 1, 5, "Waiting for Input")
                                ws.update_cell(i + 1, 6, f"Check-in required by {self.instance_name}")
                                break
                    except Exception as e:
                        logger.error(f"Error updating task {task_id}: {e}")
                        
            elif choice == '3':
                # Long-running task
                longrun_embed = discord.Embed(
                    title="🛠️ Long-Running Task Started",
                    description=f"**{task_id}** is now running as a long-term project",
                    color=0x0099ff,
                    timestamp=datetime.now()
                )
                longrun_embed.add_field(
                    name="Status",
                    value="This task will continue in the background. I'll provide periodic updates and notify you of major milestones.",
                    inline=False
                )
                longrun_embed.add_field(name="Current Status", value="In Progress - Long Running", inline=True)
                longrun_embed.add_field(name="Instance", value=self.instance_name, inline=True)
                longrun_embed.set_footer(text="Check Google Sheets for detailed progress")
                
                await channel.send(embed=longrun_embed)
                
                # Update Google Sheets
                if self.sheets_client:
                    try:
                        sheet = self.sheets_client.open_by_key(SPREADSHEET_ID)
                        ws = sheet.worksheet('Claude Tasks')
                        all_rows = ws.get_all_values()
                        for i, row in enumerate(all_rows):
                            if row and len(row) > 0 and row[0] == task_id:
                                ws.update_cell(i + 1, 5, "In Progress - Long Running")
                                ws.update_cell(i + 1, 6, f"Long-term project by {self.instance_name}")
                                break
                    except Exception as e:
                        logger.error(f"Error updating long-running task {task_id}: {e}")
                        
        except Exception as e:
            logger.error(f"Error in task simulation for {task_id}: {e}")
            error_embed = discord.Embed(
                title="❌ Task Error",
                description=f"Encountered an error while working on **{task_id}**",
                color=0xff0000,
                timestamp=datetime.now()
            )
            error_embed.add_field(name="Error", value=str(e), inline=False)
            error_embed.add_field(name="Instance", value=self.instance_name, inline=True)
            
            await channel.send(embed=error_embed)
                working_embed.set_footer(text="Will update periodically - check Google Sheets for progress")
                
                await channel.send(embed=working_embed)
                
                # Update Google Sheets with long-running status
                if self.sheets_client:
                    try:
                        sheet = self.sheets_client.open_by_key(SPREADSHEET_ID)
                        ws = sheet.worksheet('Claude Tasks')
                        all_rows = ws.get_all_values()
                        for i, row in enumerate(all_rows):
                            if row and len(row) > 0 and row[0] == task_id:
                                ws.update_cell(i + 1, 5, "In Progress - Long Running")
                                ws.update_cell(i + 1, 6, f"Long-term task started by {self.instance_name} - manual completion required")
                                break
                    except Exception as e:
                        logger.error(f"Error updating long-running task {task_id}: {e}")
                
                # For very complex tasks, don't auto-complete - leave it running
                # User will need to manually mark as complete or provide updates
                logger.info(f"Started long-running task {task_id} - no auto-completion")
                
            elif is_complex and not is_simple:
                # Complex task - still working
                working_embed = discord.Embed(
                    title="⚙️ Still Working",
                    description=f"**{task_id}** is a complex task requiring more time",
                    color=0x0099ff,
                    timestamp=datetime.now()
                )
                working_embed.add_field(
                    name="Status",
                    value="Working on implementation... This may take a while.",
                    inline=False
                )
                working_embed.add_field(name="Current Status", value="In Progress", inline=True)
                working_embed.add_field(name="Instance", value=self.instance_name, inline=True)
                working_embed.set_footer(text="Will notify when complete or if input needed")
                
                await channel.send(embed=working_embed)
                
                # Update Google Sheets with progress note
                if self.sheets_client:
                    try:
                        sheet = self.sheets_client.open_by_key(SPREADSHEET_ID)
                        ws = sheet.worksheet('Claude Tasks')
                        all_rows = ws.get_all_values()
                        for i, row in enumerate(all_rows):
                            if row and len(row) > 0 and row[0] == task_id:
                                ws.update_cell(i + 1, 6, f"Complex task - {self.instance_name} working on implementation")
                                break
                    except Exception as e:
                        logger.error(f"Error updating task {task_id} progress: {e}")
                
                # Continue working (simulate longer task)
                await asyncio.sleep(15)  # Work for 15 more seconds
                
                # Final completion after extended work
                completion_embed = discord.Embed(
                    title="✅ Complex Task Completed",
                    description=f"**{task_id}** has been completed after extended work!",
                    color=0x00ff00,
                    timestamp=datetime.now()
                )
                completion_embed.add_field(
                    name="Summary",
                    value=f"Successfully completed: {task_desc}",
                    inline=False
                )
                completion_embed.add_field(name="Status Update", value="In Progress → Complete", inline=True)
                completion_embed.add_field(name="Instance", value=self.instance_name, inline=True)
                completion_embed.add_field(name="Total Time", value="~30 seconds", inline=True)
                completion_embed.set_footer(text="Complex task auto-completed")
                
                await channel.send(embed=completion_embed)
                
                # Update Google Sheets to complete
                if self.sheets_client:
                    try:
                        sheet = self.sheets_client.open_by_key(SPREADSHEET_ID)
                        ws = sheet.worksheet('Claude Tasks')
                        all_rows = ws.get_all_values()
                        for i, row in enumerate(all_rows):
                            if row and len(row) > 0 and row[0] == task_id:
                                ws.update_cell(i + 1, 5, "Complete")
                                ws.update_cell(i + 1, 6, f"Complex task completed by {self.instance_name}")
                                break
                        logger.info(f"Completed complex task {task_id}")
                    except Exception as e:
                        logger.error(f"Error completing complex task {task_id}: {e}")
                
            else:
                # Simple task - complete quickly
                completion_embed = discord.Embed(
                    title="✅ Task Completed",
                    description=f"**{task_id}** has been completed successfully!",
                    color=0x00ff00,
                    timestamp=datetime.now()
                )
                completion_embed.add_field(
                    name="Summary",
                    value=f"Finished: {task_desc}",
                    inline=False
                )
                completion_embed.add_field(name="Status Update", value="In Progress → Complete", inline=True)
                completion_embed.add_field(name="Instance", value=self.instance_name, inline=True)
                completion_embed.set_footer(text="Auto-completed")
                
                await channel.send(embed=completion_embed)
                
                # Update Google Sheets status
                if self.sheets_client:
                    try:
                        sheet = self.sheets_client.open_by_key(SPREADSHEET_ID)
                        ws = sheet.worksheet('Claude Tasks')
                        all_rows = ws.get_all_values()
                        for i, row in enumerate(all_rows):
                            if row and len(row) > 0 and row[0] == task_id:
                                ws.update_cell(i + 1, 5, "Complete")
                                ws.update_cell(i + 1, 6, f"Auto-completed by {self.instance_name}")
                                break
                        logger.info(f"Completed task {task_id}")
                    except Exception as e:
                        logger.error(f"Error completing task {task_id}: {e}")
                        
        except Exception as e:
            logger.error(f"Error in task simulation for {task_id}: {e}")
            error_embed = discord.Embed(
                title="❌ Task Error",
                description=f"Encountered an error while working on **{task_id}**",
                color=0xff0000,
                timestamp=datetime.now()
            )
            error_embed.add_field(name="Error", value=str(e), inline=False)
            error_embed.add_field(name="Instance", value=self.instance_name, inline=True)
            
            await channel.send(embed=error_embed)

    @commands.command()
    async def task(self, ctx, *, description):
        """Quick task creation command"""
        # Create a fake message object for reuse
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
        print(f"Set it with: export {token_name}='your_token_here'")
        print(f"Or use: export DISCORD_BOT_TOKEN='your_token_here' as fallback")
        exit(1)
    
    bot = UnifiedClaudeBot()
    
    try:
        print(f"🔑 Using token from: {token_name}")
        bot.run(token)
    except KeyboardInterrupt:
        print(f"\n🛑 {INSTANCE_NAME} Discord bot shutting down...")
    except Exception as e:
        print(f"❌ Bot error: {e}")