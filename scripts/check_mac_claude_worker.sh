#!/bin/bash
# Check Mac Claude Worker status

echo "🔍 Checking Mac Claude Worker Status"
echo "===================================="
echo

# Check if worker is running
if pgrep -f "mac_claude_task_worker.py" > /dev/null; then
    PID=$(pgrep -f "mac_claude_task_worker.py")
    echo "✅ Mac Claude Worker is running (PID: $PID)"
    echo
    
    # Check work log
    if [ -f "/Users/joshpayneair/Desktop/industrial-iot-stack/scripts/mac_claude_work.log" ]; then
        echo "📄 Recent worker activity:"
        echo "------------------------"
        tail -20 /Users/joshpayneair/Desktop/industrial-iot-stack/scripts/mac_claude_work.log
    else
        echo "⚠️  No work log found yet"
    fi
else
    echo "❌ Mac Claude Worker is NOT running!"
    echo
    echo "To start it:"
    echo "scripts/start_mac_claude_monitoring.sh worker"
fi

echo
echo "📊 Current Mac Claude tasks in Google Sheets:"
echo "• CT-049 is currently Pending"
echo "• Worker checks every 30 seconds"
echo "• Should change to 'In Progress' then 'Complete'"