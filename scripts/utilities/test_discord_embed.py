#!/usr/bin/env python3
"""Test Discord webhook with embed (same as inter_claude_communication.py)"""

import requests
import json
from datetime import datetime

webhook_url = "https://discordapp.com/api/webhooks/1380061953883373660/lFn5d2hcBxAhaMJSpBNwjQNInczAGYQ-HYky70iSiNymhFXw7egnjUapMdAHZXrRWJhG"

# Test the exact same embed format as inter_claude_communication.py
embed = {
    "title": "🎉 Celebrations & Completions: 🚀 CT-084 TEST",
    "description": "🧪 **EMBED TEST** - Testing Mac Claude Discord embed functionality!",
    "color": 0x0099ff,
    "timestamp": datetime.now().isoformat(),
    "footer": {
        "text": "From: Mac Claude | ADK Enhanced"
    },
    "fields": []
}

payload = {"embeds": [embed]}

try:
    response = requests.post(webhook_url, json=payload, timeout=10)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 204:
        print("✅ SUCCESS! Embed sent to Discord!")
    else:
        print("❌ FAILED! Error sending embed")
        print(f"Payload: {json.dumps(payload, indent=2)}")
        
except Exception as e:
    print(f"❌ ERROR: {e}")