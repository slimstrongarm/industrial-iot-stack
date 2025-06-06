#!/bin/bash
# Mac Claude Max TMUX Session Startup
# One-command setup for Industrial IoT Stack development

set -e

echo "🚀 Starting Mac Claude Max Session..."
echo "======================================="

# Kill existing session if it exists
tmux kill-session -t mac-claude-max 2>/dev/null || true

# Create new session with multiple windows
tmux new-session -d -s mac-claude-max -n main

# Window 0: Main workspace with context
tmux send-keys -t mac-claude-max:main "clear" Enter
tmux send-keys -t mac-claude-max:main "cd ~/Desktop/industrial-iot-stack" Enter
tmux send-keys -t mac-claude-max:main "echo '🎯 Mac Claude Max Session Ready'" Enter
tmux send-keys -t mac-claude-max:main "echo '================================'" Enter
tmux send-keys -t mac-claude-max:main "echo ''" Enter
tmux send-keys -t mac-claude-max:main "echo '📋 Project Context:'" Enter
tmux send-keys -t mac-claude-max:main "cat .claude/context/current_session.md" Enter
tmux send-keys -t mac-claude-max:main "echo ''" Enter
tmux send-keys -t mac-claude-max:main "echo '🎯 Current Status:'" Enter
tmux send-keys -t mac-claude-max:main "head -20 STATUS.md" Enter
tmux send-keys -t mac-claude-max:main "echo ''" Enter
tmux send-keys -t mac-claude-max:main "echo '⚡ Quick Commands:'" Enter
tmux send-keys -t mac-claude-max:main "echo '  • Check tasks: python3 scripts/quick_status.py'" Enter
tmux send-keys -t mac-claude-max:main "echo '  • Update sheets: python3 scripts/comprehensive_sheets_update.py'" Enter
tmux send-keys -t mac-claude-max:main "echo '  • Test connections: python3 scripts/test_github_actions_access.py'" Enter
tmux send-keys -t mac-claude-max:main "echo '  • Switch window: Ctrl+B then 1,2,3,4'" Enter
tmux send-keys -t mac-claude-max:main "echo ''" Enter

# Window 1: Google Sheets monitor
tmux new-window -t mac-claude-max -n sheets
tmux send-keys -t mac-claude-max:sheets "cd ~/Desktop/industrial-iot-stack" Enter
tmux send-keys -t mac-claude-max:sheets "echo '📊 Google Sheets Monitor'" Enter
tmux send-keys -t mac-claude-max:sheets "echo '====================='" Enter
tmux send-keys -t mac-claude-max:sheets "echo 'Monitoring Claude Tasks and Agent Activities...'" Enter
tmux send-keys -t mac-claude-max:sheets "echo ''" Enter
tmux send-keys -t mac-claude-max:sheets "echo 'To check latest tasks:'" Enter
tmux send-keys -t mac-claude-max:sheets "echo 'python3 scripts/check_current_format.py'" Enter

# Window 2: Git operations
tmux new-window -t mac-claude-max -n git
tmux send-keys -t mac-claude-max:git "cd ~/Desktop/industrial-iot-stack" Enter
tmux send-keys -t mac-claude-max:git "echo '🌿 Git Operations'" Enter
tmux send-keys -t mac-claude-max:git "echo '==============='" Enter
tmux send-keys -t mac-claude-max:git "git status" Enter
tmux send-keys -t mac-claude-max:git "echo ''" Enter
tmux send-keys -t mac-claude-max:git "echo 'Recent commits:'" Enter
tmux send-keys -t mac-claude-max:git "git log --oneline -5" Enter

# Window 3: Testing and validation
tmux new-window -t mac-claude-max -n test
tmux send-keys -t mac-claude-max:test "cd ~/Desktop/industrial-iot-stack" Enter
tmux send-keys -t mac-claude-max:test "echo '🧪 Testing & Validation'" Enter
tmux send-keys -t mac-claude-max:test "echo '==================='" Enter
tmux send-keys -t mac-claude-max:test "echo 'Available tests:'" Enter
tmux send-keys -t mac-claude-max:test "echo '• Google Sheets: python3 scripts/test_github_actions_access.py'" Enter
tmux send-keys -t mac-claude-max:test "echo '• WhatsApp flow: node whatsapp-integration/test-alert.js'" Enter
tmux send-keys -t mac-claude-max:test "echo '• Quick status: python3 scripts/quick_status.py'" Enter

# Window 4: Claude context and handoff
tmux new-window -t mac-claude-max -n claude
tmux send-keys -t mac-claude-max:claude "cd ~/Desktop/industrial-iot-stack" Enter
tmux send-keys -t mac-claude-max:claude "echo '🤖 Claude Context & Handoff'" Enter
tmux send-keys -t mac-claude-max:claude "echo '=========================='" Enter
tmux send-keys -t mac-claude-max:claude "echo 'Context files:'" Enter
tmux send-keys -t mac-claude-max:claude "ls -la .claude/" Enter
tmux send-keys -t mac-claude-max:claude "echo ''" Enter
tmux send-keys -t mac-claude-max:claude "echo 'To prepare handoff:'" Enter
tmux send-keys -t mac-claude-max:claude "echo 'cp .claude/handoff_template.md current_handoff.md'" Enter

# Set status bar to green (Mac identifier)
tmux set-option -t mac-claude-max status-bg green
tmux set-option -t mac-claude-max status-fg black
tmux set-option -t mac-claude-max status-left "#[bg=green,fg=black,bold] 🍎 MAC CLAUDE MAX #[default]"

# Go back to main window
tmux select-window -t mac-claude-max:main

echo ""
echo "✅ Mac Claude Max session created!"
echo ""
echo "🎯 To attach: tmux attach -t mac-claude-max"
echo "💡 To detach: Ctrl+B then D"
echo "⚡ Switch windows: Ctrl+B then 0,1,2,3,4"
echo ""
echo "🚀 Session includes:"
echo "   Window 0: Main workspace with project context"
echo "   Window 1: Google Sheets monitoring"
echo "   Window 2: Git operations"
echo "   Window 3: Testing and validation"
echo "   Window 4: Claude context and handoff"
echo ""

# Auto-attach if not already in tmux
if [ -z "$TMUX" ]; then
    echo "🔌 Auto-attaching to session..."
    tmux attach -t mac-claude-max
else
    echo "📋 Already in TMUX - run: tmux attach -t mac-claude-max"
fi