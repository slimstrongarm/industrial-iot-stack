#!/bin/bash
# Check GitHub bot status and configuration

echo "🤖 CHECKING GITHUB BOT STATUS"
echo "=============================="

# Check if ANTHROPIC_API_KEY is set in GitHub secrets
echo -e "\n📋 Checking GitHub workflow configuration:"
if [ -f .github/workflows/claude.yml ]; then
    echo "✅ claude.yml workflow exists"
    echo "   - Triggers on: @claude mentions in issues/PRs"
    echo "   - Requires: ANTHROPIC_API_KEY secret"
else
    echo "❌ claude.yml workflow not found"
fi

# Check recent GitHub activity
echo -e "\n📊 Recent repository activity:"
git log --oneline -5 --pretty=format:"%h %s (%cr)"

echo -e "\n\n⚠️  TO VERIFY BOT IS WORKING:"
echo "1. Go to: https://github.com/joshpayneair/industrial-iot-stack/settings/secrets/actions"
echo "2. Verify ANTHROPIC_API_KEY is set"
echo "3. Create a test issue and mention @claude"
echo "4. Check Actions tab for workflow runs"

echo -e "\n🔍 MANUAL CHECK REQUIRED:"
echo "The bot won't appear in git history - it comments on GitHub issues/PRs"
echo "Check: https://github.com/joshpayneair/industrial-iot-stack/issues"