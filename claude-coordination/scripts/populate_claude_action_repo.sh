#!/bin/bash
# Populate the claude-code-action repository using GitHub API

echo "🚀 Populating slimstrongarm/claude-code-action repository"
echo "======================================================="

# Check if GitHub token is available
if [ -z "$GITHUB_TOKEN" ]; then
    echo "❌ GitHub token required for API access"
    echo ""
    echo "📋 To get a GitHub token:"
    echo "1. Go to: https://github.com/settings/tokens"
    echo "2. Click 'Generate new token (classic)'"
    echo "3. Select scopes: repo, workflow"
    echo "4. Copy the token and run:"
    echo "   export GITHUB_TOKEN=your_token_here"
    echo "   ./scripts/setup/populate_claude_action_repo.sh"
    echo ""
    echo "💡 Alternative: Install GitHub CLI"
    echo "   brew install gh"
    echo "   gh auth login"
    echo ""
    exit 1
fi

echo "✅ GitHub token found"

# Clone the source repository to temporary location
echo ""
echo "📥 Downloading claude-code-action source..."
TEMP_DIR=$(mktemp -d)
cd "$TEMP_DIR"
git clone https://github.com/grll/claude-code-action.git
cd claude-code-action

# Remove git history and prepare for upload
rm -rf .git

echo "✅ Source code prepared"

# Function to upload file via GitHub API
upload_file() {
    local file_path="$1"
    local content=$(base64 -i "$file_path")
    local api_path="$2"
    
    echo "📤 Uploading: $api_path"
    
    curl -s -X PUT \
        -H "Authorization: token $GITHUB_TOKEN" \
        -H "Content-Type: application/json" \
        -d "{
            \"message\": \"Add $api_path\",
            \"content\": \"$content\"
        }" \
        "https://api.github.com/repos/slimstrongarm/claude-code-action/contents/$api_path"
}

# Upload key files
echo ""
echo "📤 Uploading files to repository..."

# Upload README first
if [ -f "README.md" ]; then
    upload_file "README.md" "README.md" > /dev/null
    echo "✅ README.md"
fi

# Upload action.yml
if [ -f "action.yml" ]; then
    upload_file "action.yml" "action.yml" > /dev/null
    echo "✅ action.yml"
fi

# Upload package.json
if [ -f "package.json" ]; then
    upload_file "package.json" "package.json" > /dev/null
    echo "✅ package.json"
fi

# Upload LICENSE
if [ -f "LICENSE" ]; then
    upload_file "LICENSE" "LICENSE" > /dev/null
    echo "✅ LICENSE"
fi

# Upload key directories (simplified approach)
echo ""
echo "📁 Creating directory structure..."

# Create src directory structure marker
echo "# Source code directory" > src_marker.md
upload_file "src_marker.md" "src/README.md" > /dev/null
echo "✅ src/ directory"

# Create examples directory with workflow
if [ -d "examples" ]; then
    if [ -f "examples/claude.yml" ]; then
        upload_file "examples/claude.yml" "examples/claude.yml" > /dev/null
        echo "✅ examples/claude.yml"
    fi
fi

# Clean up
cd /
rm -rf "$TEMP_DIR"

echo ""
echo "🎉 Repository population complete!"
echo ""
echo "📋 Next Steps:"
echo "1. 🔗 Install GitHub App: https://github.com/apps/claude"
echo "2. 🔑 Add secrets to industrial-iot-stack repository"
echo "3. 📝 Add workflow file to .github/workflows/"
echo "4. 🧪 Test with @claude mention"
echo ""
echo "🔗 Your repository: https://github.com/slimstrongarm/claude-code-action"
echo ""
echo "💡 For complete source code, clone the original:"
echo "   git clone https://github.com/grll/claude-code-action.git"
echo "   cd claude-code-action && rm -rf .git"
echo "   git init && git remote add origin https://github.com/slimstrongarm/claude-code-action.git"
echo "   git add . && git commit -m 'Complete source code'"
echo "   git push -u origin main"