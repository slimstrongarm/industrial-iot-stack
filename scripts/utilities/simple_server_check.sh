#!/bin/bash
# Simple server check script

echo "Copy and paste these commands after SSH'ing to the server:"
echo ""
echo "# 1. Enter WSL:"
echo "wsl"
echo ""
echo "# 2. Quick service check:"
echo 'echo "=== SERVICE STATUS ===" && echo "" && echo "Node-RED:" && curl -s http://localhost:1880 >/dev/null 2>&1 && echo "✅ Running on :1880" || echo "❌ Not found" && echo "" && echo "MQTT:" && netstat -an | grep :1883 >/dev/null 2>&1 && echo "✅ Running on :1883" || echo "❌ Not found" && echo "" && echo "Ignition:" && curl -s http://localhost:8088/StatusPing >/dev/null 2>&1 && echo "✅ Running on :8088" || echo "❌ Not found" && echo "" && echo "Docker:" && docker ps >/dev/null 2>&1 && echo "✅ Docker is working" || echo "❌ Docker not accessible"'
echo ""
echo "# 3. Set up blue TMUX:"
echo 'tmux kill-session -t claude-server 2>/dev/null; echo "set -g status-style '\''bg=colour4 fg=colour15 bold'\''" > ~/.tmux.conf && echo "set -g status-left '\''#[bg=colour12,fg=colour0] SERVER '\''" >> ~/.tmux.conf && tmux new-session -s claude-server'