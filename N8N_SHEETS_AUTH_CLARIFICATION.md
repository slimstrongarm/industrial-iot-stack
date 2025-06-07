# n8n Google Sheets Authentication - Service Account vs OAuth2

## ⚠️ Important: Use Service Account, NOT OAuth2!

### You're Seeing OAuth2 (Wrong Option)
If you see fields for:
- Client ID
- Client Secret  
- OAuth Redirect URL

This is the **OAuth2** authentication method - we don't want this!

### Find the Service Account Option

1. **In the Credential Type Selection**:
   - Look for **"Google Sheets API"** (OAuth2) ❌
   - Look for **"Google Sheets Service Account"** ✅
   
2. **Search specifically for**:
   - Type: "Service Account" in the search
   - Or look for "Google Sheets (Service Account)"
   - Or "Google API - Service Account"

### What Service Account Fields Look Like
The correct credential type should show:
- **Service Account Email**: A field for email
- **Private Key**: A large text area for JSON content
- NO Client ID or OAuth redirect URL

### If You Can't Find Service Account Option

#### Option 1: Use Google API Credential
1. Search for **"Google API"**
2. Choose **"Service Account"** authentication
3. Add scope: `https://www.googleapis.com/auth/spreadsheets`

#### Option 2: Create Google Credential First
1. Add credential type: **"Google API - Service Account"**
2. Name: `Google-ServiceAccount`
3. Service Account Email: `server-claude@iiot-stack-automation.iam.gserviceaccount.com`
4. Private Key: (paste the entire JSON content)
5. Then in Google Sheets node, reference this credential

### Getting the JSON Content
```bash
# Display the JSON content (remove sensitive parts for sharing)
cat /home/server/google-sheets-credentials.json
```

Copy the ENTIRE content including the curly braces.

## 📸 Visual Guide

### Wrong (OAuth2):
```
Credential Type: Google Sheets API
- Client ID: [________]
- Client Secret: [________]
- OAuth Redirect URL: https://...
```

### Right (Service Account):
```
Credential Type: Google Sheets Service Account
- Service Account Email: [________]
- Private Key: [Large text area for JSON]
```

Let me know what credential types you see in the dropdown!