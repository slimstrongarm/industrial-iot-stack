#!/bin/bash
# Start Mac Claude task monitoring and worker

echo "🤖 Mac Claude Task Automation System"
echo "===================================="
echo

case "$1" in
    monitor)
        echo "👀 Starting Mac Claude Task Monitor..."
        echo "This will watch for new tasks assigned to Mac Claude"
        python3 /Users/joshpayneair/Desktop/industrial-iot-stack/scripts/mac_claude_task_monitor.py
        ;;
    
    worker)
        echo "💪 Starting Mac Claude Task Worker..."
        echo "This will automatically work on tasks assigned to Mac Claude"
        python3 /Users/joshpayneair/Desktop/industrial-iot-stack/scripts/mac_claude_task_worker.py
        ;;
    
    both)
        echo "🚀 Starting both Monitor and Worker..."
        # Start monitor in background
        python3 /Users/joshpayneair/Desktop/industrial-iot-stack/scripts/mac_claude_task_monitor.py &
        MONITOR_PID=$!
        echo "Monitor started (PID: $MONITOR_PID)"
        
        # Start worker in foreground
        python3 /Users/joshpayneair/Desktop/industrial-iot-stack/scripts/mac_claude_task_worker.py
        
        # Kill monitor when worker stops
        kill $MONITOR_PID 2>/dev/null
        ;;
    
    test)
        echo "🧪 Testing Mac Claude automation..."
        echo
        echo "1. Discord bot assigns tasks to 'Mac Claude' ✅"
        echo "2. Task monitor watches for new assignments ✅"
        echo "3. Task worker automatically processes them ✅"
        echo
        echo "Try creating a task in Discord:"
        echo "@Mac Claude Bot add task Test Mac Claude automation"
        ;;
    
    *)
        echo "Usage: $0 {monitor|worker|both|test}"
        echo
        echo "Options:"
        echo "  monitor - Watch for new tasks assigned to Mac Claude"
        echo "  worker  - Automatically work on Mac Claude tasks"
        echo "  both    - Run both monitor and worker"
        echo "  test    - Show test instructions"
        exit 1
        ;;
esac