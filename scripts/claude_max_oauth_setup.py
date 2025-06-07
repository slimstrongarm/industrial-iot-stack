#!/usr/bin/env python3
"""
Help setup Claude Max subscription OAuth instead of API key for GitHub Actions
"""

import json
import requests
from datetime import datetime
from pathlib import Path

def analyze_oauth_options():
    """Analyze different approaches for using Claude Max subscription"""
    
    print("🔐 CLAUDE MAX SUBSCRIPTION OAUTH ANALYSIS")
    print("=" * 50)
    
    options = {
        "option_1_session_key": {
            "name": "Claude Max Session Key",
            "description": "Extract session key from your logged-in Claude Max browser session",
            "difficulty": "Medium",
            "reliability": "Good (but expires periodically)",
            "steps": [
                "1. Log into Claude.ai with your Max subscription",
                "2. Open browser dev tools (F12)",
                "3. Go to Application/Storage → Cookies → claude.ai",
                "4. Find 'sessionKey' cookie value",
                "5. Add as CLAUDE_MAX_SESSION_KEY secret"
            ],
            "pros": [
                "Uses your existing Max subscription",
                "No additional API costs",
                "Full Claude Max capabilities"
            ],
            "cons": [
                "Session expires periodically (need to refresh)",
                "Browser-dependent extraction",
                "Security considerations"
            ]
        },
        "option_2_reverse_proxy": {
            "name": "Local Reverse Proxy",
            "description": "Run local proxy that authenticates with your Max account",
            "difficulty": "Hard",
            "reliability": "Excellent (but complex)",
            "steps": [
                "1. Create local Claude Max proxy server",
                "2. Authenticate proxy with your Max account",
                "3. Expose proxy via ngrok or similar",
                "4. Point GitHub Action to proxy URL",
                "5. Manage proxy authentication refreshing"
            ],
            "pros": [
                "Most reliable long-term solution",
                "Handles authentication automatically",
                "Full control over requests"
            ],
            "cons": [
                "Complex setup and maintenance",
                "Requires always-on server",
                "Advanced technical knowledge needed"
            ]
        },
        "option_3_anthropic_workbench": {
            "name": "Anthropic Workbench API",
            "description": "Use Anthropic's official Workbench API with credits",
            "difficulty": "Easy",
            "reliability": "Excellent",
            "steps": [
                "1. Go to console.anthropic.com",
                "2. Create API key in Workbench",
                "3. Add credits to account ($5-20)",
                "4. Use standard API key approach",
                "5. Monitor usage in console"
            ],
            "pros": [
                "Official Anthropic solution",
                "Very reliable and stable",
                "Easy to implement",
                "Usage monitoring built-in"
            ],
            "cons": [
                "Separate from Max subscription",
                "Additional cost for API usage",
                "Need to manage credits"
            ]
        },
        "option_4_hybrid_approach": {
            "name": "Hybrid: Manual + Automation",
            "description": "Use Max for development, API for automation",
            "difficulty": "Easy",
            "reliability": "Good",
            "steps": [
                "1. Use Claude Max for manual GitHub interactions",
                "2. Set up small API credit pool for automation",
                "3. Configure GitHub Action to use API key",
                "4. Monitor and top up credits as needed",
                "5. Best of both worlds"
            ],
            "pros": [
                "Leverages your Max subscription for main use",
                "Reliable automation with API",
                "Low additional cost",
                "Simple implementation"
            ],
            "cons": [
                "Dual approach complexity",
                "Some additional API costs",
                "Need to manage both accounts"
            ]
        }
    }
    
    return options

def create_session_key_extractor():
    """Create guide for extracting Claude Max session key"""
    
    print("\n🔑 Creating session key extraction guide...")
    
    extractor_guide = '''# Claude Max Session Key Extraction Guide

## 🎯 Goal
Extract your Claude Max session key to use your subscription in GitHub Actions.

## ⚠️ Important Security Notes
- Session keys are sensitive - treat like passwords
- Keys expire periodically (usually 30-90 days)
- Only use in secure environments (GitHub Secrets)
- Never commit session keys to code

## 📱 Step-by-Step Extraction

### Method 1: Browser Dev Tools (Recommended)
1. **Open Claude.ai** in your browser
2. **Log in** with your Max subscription account
3. **Open Developer Tools** (F12 or right-click → Inspect)
4. **Go to Application tab** (Chrome) or Storage tab (Firefox)
5. **Click on Cookies** → claude.ai
6. **Find 'sessionKey'** in the cookie list
7. **Copy the Value** (long string starting with 'sk-ant-')

### Method 2: Network Tab
1. **Open Developer Tools** → Network tab
2. **Refresh** the Claude.ai page
3. **Look for API requests** to api.claude.ai
4. **Check request headers** for 'Cookie' or 'Authorization'
5. **Extract sessionKey** from the cookie string

### Method 3: Browser Console (Advanced)
```javascript
// Run in browser console on claude.ai
document.cookie.split(';').find(c => c.includes('sessionKey'))
```

## 🔧 Using the Session Key

### In GitHub Secrets:
1. Go to repository Settings → Secrets and Variables → Actions
2. Click "New repository secret"
3. Name: `CLAUDE_MAX_SESSION_KEY`
4. Value: Your extracted session key (starts with 'sk-ant-')

### In GitHub Workflow:
```yaml
- uses: slimstrongarm/claude-code-action@main
  with:
    github-token: ${{ secrets.GITHUB_TOKEN }}
    session-key: ${{ secrets.CLAUDE_MAX_SESSION_KEY }}
    # Don't use anthropic-api-key when using session-key
```

## 🔄 Session Key Refresh Process

### When Keys Expire:
- GitHub Action will start failing with auth errors
- Extract new session key using same process
- Update GitHub secret with new key
- Test with simple @claude comment

### Automation Ideas:
- Set calendar reminder to refresh monthly
- Monitor GitHub Action failures for auth errors
- Create simple test issue for monthly verification

## 🛡️ Security Best Practices
- Use organization secrets for shared repositories
- Limit secret access to necessary workflows only
- Regularly rotate session keys
- Monitor for unusual API usage
- Never log or expose session keys in outputs

## 🔍 Troubleshooting

### Common Issues:
1. **"Unauthorized" errors**: Session key expired, extract new one
2. **"Rate limited" errors**: Too many requests, Claude Max has limits
3. **"Invalid session" errors**: Key format wrong, re-extract carefully

### Verification:
```bash
# Test session key manually
curl -H "Cookie: sessionKey=YOUR_SESSION_KEY" \\
     https://claude.ai/api/organizations
```

## 💡 Alternative: API Credit Approach
If session key management becomes cumbersome:
1. Get small API credit allocation ($5-10)
2. Use standard ANTHROPIC_API_KEY approach
3. Monitor usage at console.anthropic.com
4. Supplement with manual Max usage for development

Created: Session key extraction guide for Claude Max subscription
'''
    
    guide_file = Path("/mnt/c/Users/LocalAccount/industrial-iot-stack/CLAUDE_MAX_SESSION_KEY_GUIDE.md")
    with open(guide_file, 'w') as f:
        f.write(extractor_guide)
    
    print(f"✅ Session key guide created: {guide_file}")
    return True

def update_github_workflow_for_oauth():
    """Update the GitHub workflow to support both API key and session key"""
    
    print("\n📝 Updating GitHub workflow for OAuth support...")
    
    enhanced_workflow = '''name: Claude Code Action
on:
  issue_comment:
    types: [created, edited]
  pull_request_review:
    types: [submitted]
  issues:
    types: [opened]

permissions:
  contents: write
  issues: write
  pull-requests: write

jobs:
  claude:
    if: contains(github.event.comment.body, '@claude')
    runs-on: ubuntu-latest
    steps:
      - uses: slimstrongarm/claude-code-action@main
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          # Option 1: Use Claude Max session key (preferred)
          session-key: ${{ secrets.CLAUDE_MAX_SESSION_KEY }}
          # Option 2: Use Anthropic API key (fallback)
          # anthropic-api-key: ${{ secrets.ANTHROPIC_API_KEY }}
          
          # Additional configuration
          max-tokens: 4000
          temperature: 0.3
          
          # Industrial IoT Stack specific context
          system-prompt: |
            You are Claude assisting with an Industrial IoT Stack project.
            Key components: EMQX MQTT, n8n workflows, Discord integration, 
            Google Sheets API, Node-RED, Ignition Edge.
            Provide specific, actionable advice for industrial automation.
'''
    
    workflow_file = Path("/mnt/c/Users/LocalAccount/industrial-iot-stack/.github/workflows/claude.yml")
    with open(workflow_file, 'w') as f:
        f.write(enhanced_workflow)
    
    print(f"✅ Enhanced workflow created: {workflow_file}")
    return True

def send_oauth_analysis_notification():
    """Send Discord notification with OAuth analysis"""
    
    webhook_url = "https://discordapp.com/api/webhooks/1380061953883373660/lFn5d2hcBxAhaMJSpBNwjQNInczAGYQ-HYky70iSiNymhFXw7egnjUapMdAHZXrRWJhG"
    
    oauth_msg = {
        "embeds": [{
            "title": "🔐 CLAUDE MAX OAUTH ANALYSIS",
            "description": "Solutions for using Claude Max subscription instead of API key",
            "color": 0x7c3aed,  # Purple for authentication
            "fields": [
                {
                    "name": "🎯 The Challenge",
                    "value": "Use existing Claude Max subscription in GitHub Actions instead of separate API key",
                    "inline": False
                },
                {
                    "name": "🔑 Option 1: Session Key (Recommended)",
                    "value": "• Extract session key from browser\n• Use CLAUDE_MAX_SESSION_KEY secret\n• Leverages your Max subscription\n• ⚠️ Expires periodically",
                    "inline": True
                },
                {
                    "name": "💳 Option 2: Small API Credits",
                    "value": "• Add $5-10 API credits\n• Use ANTHROPIC_API_KEY\n• Most reliable for automation\n• 💰 Small additional cost",
                    "inline": True
                },
                {
                    "name": "📋 Created Resources",
                    "value": "• Session key extraction guide\n• Enhanced GitHub workflow\n• OAuth troubleshooting docs\n• Multiple implementation options",
                    "inline": False
                },
                {
                    "name": "🚀 Recommended Approach",
                    "value": "Try session key first, fallback to API credits if needed. Session key lets you use Max subscription!",
                    "inline": False
                }
            ],
            "footer": {
                "text": "Claude Max OAuth - Industrial IoT Stack GitHub Integration"
            },
            "timestamp": datetime.now().isoformat()
        }]
    }
    
    try:
        response = requests.post(webhook_url, json=oauth_msg, timeout=10)
        if response.status_code == 204:
            print("📢 OAuth analysis notification sent to Discord!")
    except Exception as e:
        print(f"⚠️  Discord notification failed: {e}")

def main():
    """Main OAuth analysis and setup"""
    
    print("🔐 CLAUDE MAX OAUTH SETUP ASSISTANCE")
    print("=" * 45)
    
    # Analyze OAuth options
    options = analyze_oauth_options()
    
    print("\n📊 OAUTH OPTIONS ANALYSIS:")
    for key, option in options.items():
        print(f"\n🔹 {option['name']}")
        print(f"   Difficulty: {option['difficulty']}")
        print(f"   Reliability: {option['reliability']}")
        print(f"   Description: {option['description']}")
    
    # Create session key extraction guide
    create_session_key_extractor()
    
    # Update GitHub workflow
    update_github_workflow_for_oauth()
    
    # Send Discord notification
    send_oauth_analysis_notification()
    
    print(f"\n✅ OAUTH SETUP ANALYSIS COMPLETE!")
    print("=" * 40)
    
    print("📋 Created Resources:")
    print("  • CLAUDE_MAX_SESSION_KEY_GUIDE.md")
    print("  • Enhanced GitHub workflow with OAuth support")
    print("  • Multiple implementation options analyzed")
    
    print(f"\n🎯 RECOMMENDED APPROACH:")
    print("1️⃣ Try Session Key Method:")
    print("   • Extract session key from claude.ai browser")
    print("   • Add as CLAUDE_MAX_SESSION_KEY secret")
    print("   • Uses your existing Max subscription")
    
    print(f"\n2️⃣ Fallback to API Credits:")
    print("   • Add $5-10 credits at console.anthropic.com")
    print("   • Use ANTHROPIC_API_KEY approach")
    print("   • Most reliable for automation")
    
    print(f"\n🔧 Next Steps:")
    print("   • Follow CLAUDE_MAX_SESSION_KEY_GUIDE.md")
    print("   • Extract session key from browser")
    print("   • Test with @claude hello in GitHub issue")
    
    return True

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎉 Claude Max OAuth guidance ready!")
        print("Check the guide to use your Max subscription!")
    else:
        print("\n❌ OAuth analysis failed")
        sys.exit(1)