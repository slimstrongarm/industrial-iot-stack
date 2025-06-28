#!/bin/bash
# Restore Claude Max Session with All Credentials and Access
echo "🔄 Restoring Claude Max Session with Full Access..."

# Kill any existing sessions
tmux kill-server 2>/dev/null || true

# Create new session
cd ~/Desktop/industrial-iot-stack
tmux new-session -d -s claude-max-restored

# Set green status bar
tmux set-option -t claude-max-restored status-bg green
tmux set-option -t claude-max-restored status-fg black
tmux set-option -t claude-max-restored status-left "#[bg=green,fg=black,bold] 🤖 CLAUDE MAX RESTORED #[default]"

# Window 0: Main workspace with context restoration
tmux send-keys -t claude-max-restored "clear" Enter
tmux send-keys -t claude-max-restored "cd ~/Desktop/industrial-iot-stack" Enter
tmux send-keys -t claude-max-restored "echo '🤖 CLAUDE MAX SESSION RESTORED'" Enter
tmux send-keys -t claude-max-restored "echo '================================'" Enter
tmux send-keys -t claude-max-restored "echo ''" Enter

# Verify all credentials are accessible
tmux send-keys -t claude-max-restored "echo '🔑 Checking credentials and access...'" Enter
tmux send-keys -t claude-max-restored "echo ''" Enter

# Google Sheets credentials
tmux send-keys -t claude-max-restored "echo '📊 Google Sheets:'" Enter
tmux send-keys -t claude-max-restored "if [ -f credentials/iot-stack-credentials.json ]; then echo '  ✅ Credentials found'; else echo '  ❌ Missing credentials'; fi" Enter

# GitHub access
tmux send-keys -t claude-max-restored "echo '🐙 GitHub:'" Enter
tmux send-keys -t claude-max-restored "git remote -v | head -1" Enter

# Check project status
tmux send-keys -t claude-max-restored "echo ''" Enter
tmux send-keys -t claude-max-restored "echo '📋 Current Priority: CT-030 - GitHub Actions YAML Syntax Error'" Enter
tmux send-keys -t claude-max-restored "echo '🎯 Friday Demo Status: 95% Ready'" Enter
tmux send-keys -t claude-max-restored "echo '🚀 Ready Components: Discord bot, WhatsApp alerts'" Enter
tmux send-keys -t claude-max-restored "echo ''" Enter

# Load current task state
tmux send-keys -t claude-max-restored "echo '🔄 Loading current task state...'" Enter
tmux send-keys -t claude-max-restored "python3 -c \"import json; data=json.load(open('scripts/.claude_tasks_state.json')); print(f'Last check: {data[\"last_check\"]}'); print(f'Active tasks: {len([t for t in data[\"tasks\"].values() if t[\"status\"] != \"Complete\"])}')\""" Enter

tmux send-keys -t claude-max-restored "echo ''" Enter
tmux send-keys -t claude-max-restored "echo '⚡ Ready for commands!'" Enter
tmux send-keys -t claude-max-restored "echo '  • Fix YAML: yamllint .github/workflows/claude-max-automation.yml'" Enter
tmux send-keys -t claude-max-restored "echo '  • Check status: python3 scripts/quick_status.py'" Enter
tmux send-keys -t claude-max-restored "echo '  • Test access: python3 scripts/test_github_actions_access.py'" Enter

# Window 1: GitHub Actions focus
tmux new-window -t claude-max-restored -n github
tmux send-keys -t claude-max-restored:github "cd ~/Desktop/industrial-iot-stack" Enter
tmux send-keys -t claude-max-restored:github "echo '🐙 GitHub Actions Debugging'" Enter
tmux send-keys -t claude-max-restored:github "echo '========================'" Enter
tmux send-keys -t claude-max-restored:github "echo '🎯 Current Issue: YAML syntax error line 269'" Enter
tmux send-keys -t claude-max-restored:github "echo '📁 File: .github/workflows/claude-max-automation.yml'" Enter
tmux send-keys -t claude-max-restored:github "echo ''" Enter
tmux send-keys -t claude-max-restored:github "echo 'Commands ready:'" Enter
tmux send-keys -t claude-max-restored:github "echo '  yamllint .github/workflows/claude-max-automation.yml'" Enter
tmux send-keys -t claude-max-restored:github "echo '  cat .github/workflows/claude-max-automation.yml | grep -n -A5 -B5 \"269\"'" Enter

# Window 2: Credentials & API Testing
tmux new-window -t claude-max-restored -n api-test
tmux send-keys -t claude-max-restored:api-test "cd ~/Desktop/industrial-iot-stack" Enter
tmux send-keys -t claude-max-restored:api-test "echo '🔑 API & Credentials Testing'" Enter
tmux send-keys -t claude-max-restored:api-test "echo '=========================='" Enter
tmux send-keys -t claude-max-restored:api-test "echo 'Test commands:'" Enter
tmux send-keys -t claude-max-restored:api-test "echo '  • Google Sheets: python3 scripts/test_sheets_access.py'" Enter
tmux send-keys -t claude-max-restored:api-test "echo '  • GitHub Actions: python3 scripts/test_github_actions_access.py'" Enter
tmux send-keys -t claude-max-restored:api-test "echo '  • Quick status: python3 scripts/quick_status.py'" Enter

# Back to main window
tmux select-window -t claude-max-restored:0

echo "✅ Claude Max session restored with full access!"
echo ""
echo "🎯 To attach: tmux attach -t claude-max-restored"
echo ""
echo "📋 Session includes:"
echo "  Window 0: Main workspace with credentials check"
echo "  Window 1: GitHub Actions debugging"
echo "  Window 2: API testing"
echo ""
echo "🚀 Priority: Fix GitHub Actions YAML syntax error (line 269)"