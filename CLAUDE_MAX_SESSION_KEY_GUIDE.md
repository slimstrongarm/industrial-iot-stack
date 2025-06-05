# Claude Max Session Key Extraction Guide

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
curl -H "Cookie: sessionKey=YOUR_SESSION_KEY" \
     https://claude.ai/api/organizations
```

## 💡 Alternative: API Credit Approach
If session key management becomes cumbersome:
1. Get small API credit allocation ($5-10)
2. Use standard ANTHROPIC_API_KEY approach
3. Monitor usage at console.anthropic.com
4. Supplement with manual Max usage for development

Created: Session key extraction guide for Claude Max subscription
