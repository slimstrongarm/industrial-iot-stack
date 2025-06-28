#!/usr/bin/env python3
"""Test Discord webhook directly"""

import requests
import json

webhook_url = "https://discordapp.com/api/webhooks/1380061953883373660/lFn5d2hcBxAhaMJSpBNwjQNInczAGYQ-HYky70iSiNymhFXw7egnjUapMdAHZXrRWJhG"

payload = {
    "content": "🧪 **DISCORD TEST** - Mac Claude Python webhook test!",
    "username": "Mac Claude Bot"
}

try:
    response = requests.post(webhook_url, json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 204:
        print("✅ SUCCESS! Message sent to Discord!")
    else:
        print("❌ FAILED! Error sending message")
        
except Exception as e:
    print(f"❌ ERROR: {e}")