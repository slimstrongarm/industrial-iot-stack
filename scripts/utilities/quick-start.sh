#!/bin/bash
# Industrial IoT Stack - One-Command Quick Start
# Usage: curl -s https://raw.githubusercontent.com/slimstrongarm/industrial-iot-stack/main/quick-start.sh | bash

echo "🚀 Industrial IoT Stack - Quick Start"
echo "====================================="
echo ""

# Check if we're in the right directory
if [ ! -f "STATUS.md" ]; then
    echo "📁 Navigating to project directory..."
    cd ~/Desktop/industrial-iot-stack 2>/dev/null || {
        echo "❌ Project directory not found!"
        echo "   Expected: ~/Desktop/industrial-iot-stack"
        echo "   Please navigate to the project directory first."
        exit 1
    }
fi

echo "📋 Loading project context..."
echo ""

# Show critical information
echo "🎯 CURRENT STATUS:"
echo "=================="
head -15 STATUS.md
echo ""

echo "🤖 CLAUDE CONTEXT:"
echo "=================="
if [ -f ".claude/context/current_session.md" ]; then
    head -10 .claude/context/current_session.md
else
    echo "⚠️ Claude context not found - run: python3 scripts/create_claude_context_structure.py"
fi
echo ""

echo "⚡ QUICK COMMANDS:"
echo "=================="
echo "• Full status: cat STATUS.md"
echo "• Quick status: python3 scripts/quick_status.py"
echo "• Start TMUX: ./scripts/start-mac-claude-max.sh"
echo "• Test Google Sheets: python3 scripts/test_github_actions_access.py"
echo "• Update sheets: python3 scripts/comprehensive_sheets_update.py"
echo ""

echo "🎪 FRIDAY DEMO READINESS: 95%"
echo "🚨 CRITICAL: Fix GitHub Actions YAML syntax error (line 269)"
echo ""

echo "🍎 To start Mac Claude Max TMUX session:"
echo "   ./scripts/start-mac-claude-max.sh"
echo ""

echo "✅ Quick start complete! Ready for development."