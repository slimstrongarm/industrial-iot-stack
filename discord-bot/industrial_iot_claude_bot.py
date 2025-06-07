#!/usr/bin/env python3
"""
🤖 Industrial IoT Claude Discord Bot
Enhanced Discord bot following .claude standards with Google Sheets integration

Features:
- Real-time Claude interaction via Discord
- Industrial IoT system monitoring (MQTT, Docker, Node-RED)
- Google Sheets Claude Tasks integration
- Natural language command processing
- Proactive system alerts

Usage:
    export DISCORD_BOT_TOKEN='your_token_here'
    python3 industrial_iot_claude_bot.py
"""

import discord
from discord.ext import commands, tasks
import os
import subprocess
import asyncio
import json
import aiohttp
from datetime import datetime
import logging
from pathlib import Path

# Google Sheets integration
import gspread
from google.oauth2.service_account import Credentials

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot configuration following .claude standards
SPREADSHEET_ID = '1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do'
CREDENTIALS_PATH = '/Users/joshpayneair/Desktop/industrial-iot-stack/credentials/iot-stack-credentials.json'

class IndustrialIoTBot(commands.Bot):
    """Enhanced Discord bot for Industrial IoT stack management"""
    
    def __init__(self):
        # Discord intents for message content
        intents = discord.Intents.default()
        intents.message_content = True
        
        super().__init__(
            command_prefix=['!', '@claude '],
            intents=intents,
            description="🏭 Industrial IoT Claude Bot - Real-time system interaction"
        )
        
        # Industrial IoT system state
        self.system_status = {
            'mqtt_broker': 'unknown',
            'node_red': 'unknown', 
            'ignition': 'unknown',
            'docker_containers': [],
            'last_update': None
        }
        
        # Google Sheets client
        self.sheets_client = None
        self.setup_google_sheets()
        
    def setup_google_sheets(self):
        """Initialize Google Sheets API client"""
        try:
            if os.path.exists(CREDENTIALS_PATH):
                scope = ['https://spreadsheets.google.com/feeds',
                        'https://www.googleapis.com/auth/drive']
                creds = Credentials.from_service_account_file(CREDENTIALS_PATH, scopes=scope)
                self.sheets_client = gspread.authorize(creds)
                logger.info("✅ Google Sheets client initialized")
            else:
                logger.warning("⚠️ Google Sheets credentials not found")
        except Exception as e:
            logger.error(f"❌ Google Sheets setup failed: {e}")

    async def on_ready(self):
        """Bot startup - following .claude standards"""
        print("🤖 Industrial IoT Claude Discord Bot")
        print("=" * 60)
        print(f"✅ Connected as: {self.user}")
        print(f"📊 Connected to {len(self.guilds)} servers")
        print(f"🔧 System endpoints available:")
        print(f"   • Node-RED: http://localhost:1880")
        print(f"   • n8n: http://localhost:5678")
        print(f"   • Ignition: http://localhost:8088")
        print(f"📝 Google Sheets ID: {SPREADSHEET_ID}")
        print("⚡ Real-time Discord ↔ Claude integration active!")
        print("Press Ctrl+C to stop")
        print()
        
        # Start background monitoring
        self.system_monitor.start()
        
        # Send startup notification to mac-claude channel
        for guild in self.guilds:
            mac_claude_channel = discord.utils.get(guild.text_channels, name='mac-claude')
            if mac_claude_channel:
                embed = discord.Embed(
                    title="🤖 Enhanced Industrial IoT Claude Bot Online",
                    description="Advanced system monitoring and Claude interaction enabled",
                    color=0x00ff00,
                    timestamp=datetime.now()
                )
                embed.add_field(
                    name="🆕 New Features", 
                    value="• Google Sheets Claude Tasks integration\n• Enhanced system monitoring\n• Natural language command processing\n• Real-time Industrial IoT awareness", 
                    inline=False
                )
                embed.add_field(name="🔧 Try Commands", value="@claude status, @claude help, @claude mqtt", inline=False)
                await mac_claude_channel.send(embed=embed)
                break

    @tasks.loop(minutes=5)
    async def system_monitor(self):
        """Background system monitoring with proactive alerts"""
        try:
            # Update system status
            await self.update_system_status()
            
            # Check for issues and send alerts
            await self.check_system_health()
            
        except Exception as e:
            logger.error(f"System monitor error: {e}")

    async def update_system_status(self):
        """Update Industrial IoT system status"""
        # Check Docker containers
        try:
            result = subprocess.run(['docker', 'ps', '--format', 'json'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                containers = []
                for line in result.stdout.strip().split('\n'):
                    if line:
                        container = json.loads(line)
                        containers.append({
                            'name': container.get('Names', ''),
                            'status': container.get('Status', ''),
                            'image': container.get('Image', '')
                        })
                self.system_status['docker_containers'] = containers
        except Exception as e:
            logger.error(f"Docker status check failed: {e}")

        # Check Node-RED
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get('http://localhost:1880/flows', timeout=5) as resp:
                    if resp.status == 200:
                        self.system_status['node_red'] = 'online'
                    else:
                        self.system_status['node_red'] = 'offline'
        except:
            self.system_status['node_red'] = 'offline'

        # Check MQTT broker
        mqtt_status = 'offline'
        for container in self.system_status['docker_containers']:
            if 'mosquitto' in container['name'].lower() or 'emqx' in container['name'].lower():
                if 'Up' in container['status']:
                    mqtt_status = 'online'
                break
        self.system_status['mqtt_broker'] = mqtt_status
        
        self.system_status['last_update'] = datetime.now()

    async def check_system_health(self):
        """Check for system issues and send proactive alerts"""
        alerts = []
        
        # Check for offline services
        if self.system_status['node_red'] == 'offline':
            alerts.append("🚨 Node-RED appears to be offline")
            
        if self.system_status['mqtt_broker'] == 'offline':
            alerts.append("🚨 MQTT broker appears to be offline")
            
        # Check for stopped containers
        critical_containers = ['mosquitto', 'emqx', 'nodered']
        running_containers = [c['name'] for c in self.system_status['docker_containers']]
        
        for critical in critical_containers:
            if not any(critical in name.lower() for name in running_containers):
                alerts.append(f"⚠️ Critical container '{critical}' not running")
        
        # Send alerts to appropriate channels
        if alerts:
            for guild in self.guilds:
                alerts_channel = discord.utils.get(guild.text_channels, name='alerts')
                if alerts_channel:
                    embed = discord.Embed(
                        title="🚨 System Health Alert",
                        description="\n".join(alerts),
                        color=0xff0000,
                        timestamp=datetime.now()
                    )
                    await alerts_channel.send(embed=embed)

    async def on_message(self, message):
        """Enhanced message processing with Industrial IoT context"""
        # Don't respond to self
        if message.author == self.user:
            return

        # Natural language processing for Industrial IoT commands
        if self.user.mentioned_in(message):
            await self.process_natural_language(message)
        else:
            # Only process as commands if not mentioned
            await self.process_commands(message)

    async def process_natural_language(self, message):
        """Enhanced NLP for Industrial IoT commands following .claude standards"""
        content = message.content.lower()
        logger.info(f"Processing message from {message.author}: {message.content}")
        
        # Remove bot mention and command prefix
        content = content.replace(f'<@{self.user.id}>', '').replace('!', '').strip()
        logger.info(f"Cleaned content: {content}")
        
        # Status and health checks
        if any(word in content for word in ['status', 'health', 'check']):
            await self.send_system_status(message.channel)
            
        # Task management integration with Google Sheets
        elif 'task' in content and any(word in content for word in ['add', 'create', 'new']):
            logger.info("Detected task creation request")
            await self.handle_task_creation(message, content)
            
        # MQTT broker commands
        elif any(word in content for word in ['mqtt', 'broker']):
            await self.send_mqtt_status(message.channel)
            
        # Docker container commands
        elif any(word in content for word in ['docker', 'container']):
            await self.send_docker_status(message.channel)
            
        # Node-RED commands  
        elif any(word in content for word in ['node-red', 'nodered', 'flows']):
            await self.send_nodered_status(message.channel)
            
        # Help command
        elif 'help' in content:
            await self.send_help(message.channel)
            
        else:
            # Generic Claude response
            embed = discord.Embed(
                title="🤖 Claude Industrial IoT Assistant",
                description="I can help with Industrial IoT system management. Try:\n"
                          "• `@claude status` - System overview\n"
                          "• `@claude help` - Full command list\n"
                          "• `@claude mqtt` - MQTT broker status\n"
                          "• `@claude docker` - Container status",
                color=0x0099ff
            )
            await message.channel.send(embed=embed)

    async def send_system_status(self, channel):
        """Send comprehensive system status following .claude standards"""
        embed = discord.Embed(
            title="🏭 Industrial IoT Stack Status",
            description="Real-time system overview",
            color=0x00ff00 if all(status != 'offline' for status in [
                self.system_status['node_red'], 
                self.system_status['mqtt_broker']
            ]) else 0xff9900,
            timestamp=self.system_status['last_update'] or datetime.now()
        )
        
        # Core services status
        embed.add_field(
            name="🔧 Core Services",
            value=f"**Node-RED**: {self.get_status_emoji(self.system_status['node_red'])} {self.system_status['node_red']}\n"
                  f"**MQTT Broker**: {self.get_status_emoji(self.system_status['mqtt_broker'])} {self.system_status['mqtt_broker']}\n"
                  f"**Ignition**: {self.get_status_emoji(self.system_status['ignition'])} {self.system_status['ignition']}",
            inline=False
        )
        
        # Docker containers
        if self.system_status['docker_containers']:
            container_list = []
            for container in self.system_status['docker_containers'][:5]:  # Limit to 5 for Discord
                status_emoji = "🟢" if "Up" in container['status'] else "🔴"
                container_list.append(f"{status_emoji} {container['name']}")
            
            embed.add_field(
                name="🐳 Docker Containers",
                value="\n".join(container_list) if container_list else "No containers found",
                inline=False
            )
        
        # System endpoints (following .claude standards)
        embed.add_field(
            name="🌐 System Endpoints",
            value="**Node-RED**: http://localhost:1880\n"
                  "**n8n**: http://localhost:5678\n"  
                  "**Ignition**: http://localhost:8088\n"
                  "**MQTT**: localhost:1883",
            inline=False
        )
        
        await channel.send(embed=embed)

    async def send_mqtt_status(self, channel):
        """Send MQTT broker detailed status"""
        embed = discord.Embed(
            title="📡 MQTT Broker Status",
            color=0x00ff00 if self.system_status['mqtt_broker'] == 'online' else 0xff0000
        )
        
        # Find MQTT containers
        mqtt_containers = [c for c in self.system_status['docker_containers'] 
                          if any(broker in c['name'].lower() for broker in ['mosquitto', 'emqx'])]
        
        if mqtt_containers:
            for container in mqtt_containers:
                embed.add_field(
                    name=f"🐳 {container['name']}",
                    value=f"**Status**: {container['status']}\n**Image**: {container['image']}",
                    inline=False
                )
        else:
            embed.description = "No MQTT broker containers found"
            
        # Add connection endpoints
        embed.add_field(
            name="📍 Connection Endpoints",
            value="**Local**: localhost:1883\n**WebSocket**: localhost:9001",
            inline=False
        )
        
        await channel.send(embed=embed)

    async def send_docker_status(self, channel):
        """Send Docker containers status"""
        embed = discord.Embed(
            title="🐳 Docker Container Status",
            color=0x0099ff
        )
        
        if self.system_status['docker_containers']:
            for container in self.system_status['docker_containers']:
                status_emoji = "🟢" if "Up" in container['status'] else "🔴"
                embed.add_field(
                    name=f"{status_emoji} {container['name']}",
                    value=f"**Status**: {container['status']}\n**Image**: {container['image'][:30]}...",
                    inline=True
                )
        else:
            embed.description = "No Docker containers found"
            
        await channel.send(embed=embed)

    async def send_nodered_status(self, channel):
        """Send Node-RED specific status"""
        embed = discord.Embed(
            title="🔗 Node-RED Status",
            color=0x00ff00 if self.system_status['node_red'] == 'online' else 0xff0000
        )
        
        embed.add_field(
            name="🌐 Access Points",
            value="**UI**: http://localhost:1880\n"
                  "**Dashboard**: http://localhost:1880/ui\n"
                  "**API**: http://localhost:1880/flows",
            inline=False
        )
        
        if self.system_status['node_red'] == 'online':
            embed.add_field(
                name="✅ Status",
                value="Node-RED is online and accessible",
                inline=False
            )
        else:
            embed.add_field(
                name="❌ Status", 
                value="Node-RED appears to be offline",
                inline=False
            )
            
        await channel.send(embed=embed)

    async def handle_task_creation(self, message, content):
        """Handle task creation with Google Sheets integration"""
        if not self.sheets_client:
            await message.channel.send("❌ Google Sheets integration not available")
            return
            
        # Extract task description (simple implementation)
        task_desc = content.replace('task', '').replace('add', '').replace('create', '').replace('new', '').strip()
        
        if not task_desc:
            await message.channel.send("Please provide a task description. Example: `@claude add task Fix MQTT connection issue`")
            return
            
        try:
            # Open the spreadsheet and get Claude Tasks sheet
            sheet = self.sheets_client.open_by_key(SPREADSHEET_ID)
            claude_tasks = sheet.worksheet('Claude Tasks')
            
            # Get all values to find the next task ID
            all_values = claude_tasks.get_all_values()
            
            # Find the last CT number
            last_ct_num = 0
            for row in all_values:
                if row and row[0].startswith('CT-'):
                    try:
                        ct_num = int(row[0].split('-')[1])
                        if ct_num > last_ct_num:
                            last_ct_num = ct_num
                    except:
                        continue
            
            # Create new task ID
            new_task_id = f"CT-{last_ct_num + 1:03d}"
            
            # Prepare new row data
            new_row = [
                new_task_id,                    # Task ID
                "Mac Claude",                   # Assigned To (Mac Claude will work on it!)
                task_desc,                      # Task Title
                "Medium",                       # Priority
                "Pending",                      # Status
                f"Created via Discord by {message.author.name}: {task_desc}",  # Description
                "",                             # Expected Output
                ""                              # Dependencies
            ]
            
            # Append to sheet
            claude_tasks.append_row(new_row)
            
            # Send success message
            embed = discord.Embed(
                title="✅ Task Created Successfully",
                description=f"**{new_task_id}**: {task_desc}",
                color=0x00ff00,
                timestamp=datetime.now()
            )
            embed.add_field(
                name="📊 Details",
                value=f"**Assigned To**: Mac Claude\n**Priority**: Medium\n**Status**: Pending",
                inline=False
            )
            embed.add_field(
                name="🔗 View in Google Sheets",
                value=f"[Claude Tasks](https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID})",
                inline=False
            )
            embed.set_footer(text=f"Created by {message.author.name}")
            
            await message.channel.send(embed=embed)
            logger.info(f"Created task {new_task_id}: {task_desc}")
            
        except Exception as e:
            logger.error(f"Failed to create task: {e}")
            await message.channel.send(f"❌ Failed to create task: {str(e)}")

    async def send_help(self, channel):
        """Send comprehensive help following .claude standards"""
        embed = discord.Embed(
            title="🤖 Industrial IoT Claude Bot - Command Reference",
            description="Real-time Industrial IoT system interaction",
            color=0x0099ff
        )
        
        embed.add_field(
            name="📊 System Commands",
            value="`@claude status` - Complete system overview\n"
                  "`@claude health` - System health check\n"
                  "`@claude mqtt` - MQTT broker status\n"
                  "`@claude docker` - Container status\n"
                  "`@claude node-red` - Node-RED status",
            inline=False
        )
        
        embed.add_field(
            name="📝 Task Management",
            value="`@claude add task <description>` - Create new task\n"
                  "`@claude tasks` - View current tasks",
            inline=False
        )
        
        embed.add_field(
            name="🔧 Quick Access",
            value="**Node-RED**: http://localhost:1880\n"
                  "**n8n**: http://localhost:5678\n"
                  "**Ignition**: http://localhost:8088\n"
                  "**Google Sheets**: [Claude Tasks](https://docs.google.com/spreadsheets/d/1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do)",
            inline=False
        )
        
        embed.add_field(
            name="🏭 Industrial IoT Features",
            value="• Real-time system monitoring\n"
                  "• Proactive alerts and notifications\n"
                  "• Google Sheets task integration\n"
                  "• Equipment status tracking",
            inline=False
        )
        
        await channel.send(embed=embed)

    def get_status_emoji(self, status):
        """Get appropriate emoji for status"""
        if status == 'online':
            return "🟢"
        elif status == 'offline':
            return "🔴"
        else:
            return "🟡"

# Initialize and run bot
if __name__ == "__main__":
    # Check for Discord token
    token = os.environ.get('DISCORD_BOT_TOKEN')
    if not token:
        print("❌ DISCORD_BOT_TOKEN environment variable not set")
        print("Export your Discord bot token:")
        print("export DISCORD_BOT_TOKEN='your_token_here'")
        exit(1)
    
    # Create and run bot
    bot = IndustrialIoTBot()
    
    try:
        bot.run(token)
    except KeyboardInterrupt:
        print("\n🤖 Discord Claude Bot shutting down...")
    except Exception as e:
        print(f"❌ Bot error: {e}")