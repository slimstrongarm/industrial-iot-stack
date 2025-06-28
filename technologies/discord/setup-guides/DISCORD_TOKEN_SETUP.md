# 🔑 Discord Bot Token Setup

## Quick Start

You need to set your Discord bot token in the terminal before running the bot.

### Option 1: Set Token Temporarily (This Session Only)
```bash
# Set your Mac Claude bot token
export DISCORD_BOT_TOKEN='your_actual_token_here'

# Run the bot
./start_mac_claude_bot.sh
```

### Option 2: Set Token Permanently
Add to your `~/.zshrc` file:
```bash
echo 'export DISCORD_BOT_TOKEN="your_actual_token_here"' >> ~/.zshrc
source ~/.zshrc
```

### Option 3: Use a Token File (Most Secure)
```bash
# Create a token file
echo 'your_actual_token_here' > ~/.discord_mac_token

# Use it when running
export DISCORD_BOT_TOKEN=$(cat ~/.discord_mac_token)
./start_mac_claude_bot.sh
```

## Where to Find Your Token

1. Go to https://discord.com/developers/applications
2. Click on "Mac Claude Bot" application
3. Go to "Bot" section
4. Click "Reset Token" if needed
5. Copy the token

## Test the Bot

After setting the token and running the bot:

1. Go to Discord #mac-claude channel
2. Type: `@Mac Claude Bot status`
3. Go to #general channel  
4. Type: `@Mac Claude Bot help`

Both should work!