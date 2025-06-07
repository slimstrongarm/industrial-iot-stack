#!/bin/bash
# Setup Claude Code Action Repository for Industrial IoT Stack

echo "🚀 Setting up Claude Code Action for Industrial IoT Stack"
echo "========================================================="

# Check if GitHub CLI is available
if ! command -v gh &> /dev/null; then
    echo "❌ GitHub CLI (gh) is not installed"
    echo "   Install it from: https://cli.github.com/"
    exit 1
fi

# Check if logged into GitHub CLI
if ! gh auth status &> /dev/null; then
    echo "❌ Not logged into GitHub CLI"
    echo "   Run: gh auth login"
    exit 1
fi

echo "✅ GitHub CLI is ready"

# Create repository from the source
echo ""
echo "📦 Creating claude-code-action repository in your organization..."

# Fork/create the repository
gh repo create slimstrongarm/claude-code-action \
    --public \
    --description "Claude Code Action with OAuth support for Claude Max - Industrial IoT Stack integration" \
    --homepage "https://grll.bearblog.dev/use-claude-github-actions-with-claude-max/"

if [ $? -eq 0 ]; then
    echo "✅ Repository created successfully!"
else
    echo "⚠️  Repository might already exist, continuing..."
fi

# Clone the source repository to a temporary location
echo ""
echo "📥 Downloading source code..."
TEMP_DIR=$(mktemp -d)
git clone https://github.com/grll/claude-code-action.git "$TEMP_DIR/claude-code-action"

# Navigate to the temporary directory
cd "$TEMP_DIR/claude-code-action"

# Remove original git history and set up new remote
rm -rf .git
git init
git remote add origin https://github.com/slimstrongarm/claude-code-action.git

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

# Push to the new repository
echo ""
echo "📤 Pushing to your repository..."
git branch -M main
git push -u origin main

if [ $? -eq 0 ]; then
    echo "✅ Code pushed successfully!"
else
    echo "❌ Failed to push code"
    exit 1
fi

# Clean up temporary directory
cd /
rm -rf "$TEMP_DIR"

echo ""
echo "🎉 Claude Code Action repository setup complete!"
echo ""
echo "📋 Next Steps:"
echo "1. 🔗 Install GitHub App: https://github.com/apps/claude"
echo "2. 🔑 Configure secrets in your repository settings"
echo "3. 📝 Add workflow to industrial-iot-stack/.github/workflows/"
echo "4. 🧪 Test with @claude mention in an issue"
echo ""
echo "📖 Full documentation: CLAUDE_CODE_ACTION_SETUP.md"
echo "🔗 Your new repository: https://github.com/slimstrongarm/claude-code-action"
echo ""
echo "🏭 Ready to enhance Industrial IoT Stack development with AI assistance!"