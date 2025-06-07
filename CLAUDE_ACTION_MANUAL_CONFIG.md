# Manual Claude Action Configuration

## 🎯 Issue: Official GitHub App vs OAuth Fork

The official Claude GitHub app (https://github.com/apps/claude) is for the standard Anthropic API, but we're using the **OAuth fork** that supports Claude Max subscriptions.

## 🔧 **Solution: Manual Configuration**

### Step 1: Skip GitHub App Installation
We don't need the official GitHub app since we're using the OAuth fork.

### Step 2: Add Your API Secret
1. Go to: https://github.com/slimstrongarm/industrial-iot-stack/settings/secrets/actions
2. Click "New repository secret"
3. Choose **ONE** of these options:

**Option A: Anthropic API Key**
- Name: `ANTHROPIC_API_KEY`
- Value: Your Anthropic API key

**Option B: Claude Max OAuth (Recommended)**
- Name: `CLAUDE_MAX_SESSION_KEY` 
- Value: Your Claude Max session key

### Step 3: Get Your Claude Max Session Key
1. Open Claude Code in terminal
2. Run: `/login` (if not already logged in)
3. Check your session with: `/whoami`
4. The session key is in your Claude Max account settings

### Step 4: Update Workflow
Edit `.github/workflows/claude.yml` to use the right authentication:

```yaml
# For Claude Max OAuth (recommended):
- uses: slimstrongarm/claude-code-action@main
  with:
    github-token: ${{ secrets.GITHUB_TOKEN }}
    session-key: ${{ secrets.CLAUDE_MAX_SESSION_KEY }}

# OR for direct API:
- uses: slimstrongarm/claude-code-action@main
  with:
    github-token: ${{ secrets.GITHUB_TOKEN }}
    anthropic-api-key: ${{ secrets.ANTHROPIC_API_KEY }}
```

### Step 5: Test Without GitHub App
1. Create a test issue in your `industrial-iot-stack` repository
2. Comment: `@claude Hello! Can you help test this integration?`
3. The workflow should trigger and Claude should respond

## ⚠️ **Important Notes**

- The **OAuth fork** doesn't require the official GitHub app
- It works directly with your repository secrets
- Uses your **existing Claude Max subscription** (no extra costs)
- More reliable for our Industrial IoT Stack setup

## 🚀 **Benefits of This Approach**

- ✅ **Uses your Claude Max subscription**
- ✅ **No GitHub app complications**
- ✅ **Works with our existing setup**
- ✅ **Ready for brewery demo**

---

**Next**: Add your secret and test the integration!