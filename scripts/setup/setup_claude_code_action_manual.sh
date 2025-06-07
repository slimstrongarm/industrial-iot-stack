#!/bin/bash
# Manual setup for Claude Code Action Repository

echo "🚀 Manual Setup for Claude Code Action Repository"
echo "================================================"
echo ""
echo "Since GitHub CLI is not available, here's the manual process:"
echo ""
echo "📋 Step 1: Create Repository on GitHub"
echo "----------------------------------------"
echo "1. Go to: https://github.com/new"
echo "2. Repository name: claude-code-action"
echo "3. Description: 'Claude Code Action with OAuth support for Claude Max - Industrial IoT Stack integration'"
echo "4. Make it Public"
echo "5. Do NOT initialize with README"
echo "6. Click 'Create repository'"
echo ""
echo "✅ Press Enter when you've created the repository..."
read

echo ""
echo "📥 Step 2: Clone and Prepare the Code"
echo "-------------------------------------"

# Create a temporary directory
TEMP_DIR="/tmp/claude-code-action-setup"
rm -rf "$TEMP_DIR"
mkdir -p "$TEMP_DIR"
cd "$TEMP_DIR"

echo "Cloning source repository..."
git clone https://github.com/grll/claude-code-action.git
cd claude-code-action

# Remove original git history
rm -rf .git
git init

# Configure git (using your email)
git config user.email "noreply@anthropic.com"
git config user.name "Claude Code"

# Add your repository as remote
echo ""
echo "📝 Step 3: Set up your remote"
echo "-----------------------------"
echo "Enter your GitHub username (e.g., slimstrongarm):"
read GITHUB_USERNAME

git remote add origin https://github.com/$GITHUB_USERNAME/claude-code-action.git

# Add all files and make initial commit
git add .
git commit -m "🎉 Initial commit: Claude Code Action with OAuth support

Forked from: https://github.com/grll/claude-code-action
Article: https://grll.bearblog.dev/use-claude-github-actions-with-claude-max/

Features:
- OAuth authentication for Claude Max subscribers
- Interactive code assistant for GitHub PRs and issues
- Automated code review and implementation
- Progress tracking with dynamic updates
- Flexible tool access and GitHub API integration

Perfect for Industrial IoT Stack development workflow automation.

🤖 Generated with Claude Code

Co-Authored-By: Claude <noreply@anthropic.com>"

echo ""
echo "📤 Step 4: Push to Your Repository"
echo "----------------------------------"
echo "Ready to push to: https://github.com/$GITHUB_USERNAME/claude-code-action"
echo ""
echo "Run these commands:"
echo "  git branch -M main"
echo "  git push -u origin main"
echo ""
echo "Would you like me to push now? (y/n)"
read PUSH_CONFIRM

if [ "$PUSH_CONFIRM" = "y" ] || [ "$PUSH_CONFIRM" = "Y" ]; then
    git branch -M main
    git push -u origin main
    
    if [ $? -eq 0 ]; then
        echo "✅ Successfully pushed to GitHub!"
    else
        echo "❌ Push failed. You may need to:"
        echo "   1. Check your GitHub credentials"
        echo "   2. Make sure the repository was created"
        echo "   3. Try pushing manually with: git push -u origin main"
    fi
fi

echo ""
echo "🎉 Setup Complete!"
echo ""
echo "📋 Next Steps:"
echo "1. 🔗 Install GitHub App: https://github.com/apps/claude"
echo "2. 🔑 Add these secrets to your repository:"
echo "   - ANTHROPIC_API_KEY or"
echo "   - CLAUDE_MAX_SESSION_KEY (for OAuth)"
echo "3. 📝 Copy workflow from examples/claude.yml to .github/workflows/"
echo "4. 🧪 Test with @claude mention in an issue"
echo ""
echo "📖 Full documentation: $TEMP_DIR/claude-code-action/README.md"
echo "🔗 Your repository: https://github.com/$GITHUB_USERNAME/claude-code-action"
echo ""
echo "🏭 Ready to enhance Industrial IoT Stack with AI assistance!"