#!/usr/bin/env python3
"""
Formbricks API Testing Script
Run this after obtaining API key from Formbricks dashboard
"""

import requests
import json
from datetime import datetime

# Configuration - UPDATE WITH YOUR API KEY
FORMBRICKS_API_KEY = "fbk_your_api_key_here"
BASE_URL = "https://app.formbricks.com"

headers = {
    "Authorization": f"Bearer {FORMBRICKS_API_KEY}",
    "Content-Type": "application/json"
}

def test_formbricks_api():
    """Test Formbricks API connectivity and endpoints"""
    
    print("🧪 Testing Formbricks API")
    print("=" * 30)
    
    if FORMBRICKS_API_KEY == "fbk_your_api_key_here":
        print("❌ Please update FORMBRICKS_API_KEY with your actual API key")
        return False
    
    # Test endpoints
    endpoints = [
        ("GET", "/api/v1/surveys", "List surveys"),
        ("GET", "/api/v1/responses", "Get responses"),  
        ("GET", "/api/v1/me", "Get user info"),
    ]
    
    for method, endpoint, description in endpoints:
        url = f"{BASE_URL}{endpoint}"
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ {description}: {len(data) if isinstance(data, list) else 'Success'}")
            elif response.status_code == 401:
                print(f"❌ {description}: Authentication failed - check API key")
            elif response.status_code == 403:
                print(f"⚠️  {description}: Forbidden - check API permissions")
            else:
                print(f"⚠️  {description}: Status {response.status_code}")
                
        except Exception as e:
            print(f"❌ {description}: Error - {str(e)[:50]}")
    
    print("\n🎯 Next Steps:")
    print("1. Configure n8n HTTP Request node with API key")
    print("2. Set up webhook or polling workflow")
    print("3. Test form submission → Google Sheets flow")
    
    return True

if __name__ == "__main__":
    test_formbricks_api()
