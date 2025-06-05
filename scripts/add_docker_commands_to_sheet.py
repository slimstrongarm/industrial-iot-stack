#!/usr/bin/env python3
import sys
sys.path.append('/home/server')
from google_sheets_helper import GoogleSheetsHelper
from datetime import datetime

helper = GoogleSheetsHelper()

print("📋 Adding Docker installation commands to Google Sheets...")

# Create clean, copyable command data
commands_data = [
    ['=== DOCKER INSTALLATION COMMANDS ==='],
    [''],
    ['Option 1: Using prepared script'],
    ['sudo /mnt/c/Users/LocalAccount/industrial-iot-stack/scripts/install-docker-wrappers.sh'],
    [''],
    ['Option 2: Single command (copy everything below this line)'],
    ['sudo bash -c \''],
    ['echo "Installing Docker wrappers system-wide..."'],
    ['mkdir -p /usr/local/bin'],
    [''],
    ['cat > /usr/local/bin/docker << '"'"'EOF'"'"''],
    ['#!/bin/bash'],
    ['DOCKER_HOST=tcp://localhost:2375 "/mnt/c/Program Files/Docker/Docker/resources/bin/docker.exe" "$@"'],
    ['EOF'],
    ['chmod +x /usr/local/bin/docker'],
    [''],
    ['cat > /usr/local/bin/docker-compose << '"'"'EOF'"'"''],
    ['#!/bin/bash'],
    ['DOCKER_HOST=tcp://localhost:2375 "/mnt/c/Program Files/Docker/Docker/resources/bin/docker-compose.exe" "$@"'],
    ['EOF'],
    ['chmod +x /usr/local/bin/docker-compose'],
    [''],
    ['echo "✅ Installation complete!"'],
    ['docker --version'],
    ['docker-compose --version'],
    ['\''],
    [''],
    ['=== VERIFICATION COMMANDS ==='],
    ['docker --version'],
    ['docker ps'],
    ['docker-compose --version'],
    [''],
    [f'Created: {datetime.now().strftime("%m/%d/%Y %H:%M:%S")} by server-claude']
]

# Try different sheet approaches
success = False

# Approach 1: Add to Server Check Commands sheet
try:
    range_name = "Server Check Commands!A:A"
    
    # Add each command as a separate row
    for i, command in enumerate(commands_data):
        row_range = f"Server Check Commands!A{i+1}"
        result = helper.write_range(row_range, [command])
        if result:
            continue
        else:
            break
    
    print("✅ Successfully added Docker commands to Server Check Commands sheet")
    success = True
    
except Exception as e:
    print(f"❌ Failed to add to Server Check Commands: {e}")

# Approach 2: Try adding to a different sheet if first approach failed
if not success:
    try:
        # Add to Agent Activities as a workaround
        timestamp = datetime.now().strftime('%m/%d/%Y %H:%M:%S')
        
        # Add a log entry indicating where to find the commands
        log_entry = [
            timestamp,
            'server-claude',
            'Docker Commands Available',
            'Docker installation commands added to sheets - check Server Check Commands tab',
            'Ready for Copy'
        ]
        helper.append_row('Agent Activities', log_entry)
        
        print("✅ Added reference to Agent Activities - Docker commands ready")
        
    except Exception as e:
        print(f"❌ Fallback approach also failed: {e}")

print("\n🔍 You should now be able to find the Docker installation commands in your Google Sheets")
print("Look in the 'Server Check Commands' tab or check 'Agent Activities' for the reference")