#!/usr/bin/env python3
"""Verify Discord Bot Tokens"""

import base64
import re

# The tokens from the scripts
MAC_TOKEN = 'MTM4MTMxQxOTk0NTk3NTc3Mzc3OA.G9KB9Q.jODzGUt8TnHyaqAAy0KbB4tdalezysXG-_6xJ4'
SERVER_TOKEN = 'MTM4MTMzNjM1OTE5Njk1MDU5OA.GNW9ge.4BHWL_xhn8AdNqoMT_cQY2gse0neDPb-TxHLG4'

def verify_token_format(token, name):
    """Verify Discord token format"""
    print(f"\n🔍 Verifying {name}:")
    print(f"Token: {token}")
    
    # Discord token format: USER_ID.TIMESTAMP.HMAC
    parts = token.split('.')
    
    if len(parts) != 3:
        print(f"❌ Invalid format - should have 3 parts separated by dots, has {len(parts)}")
        return False
    
    # Check first part (should be base64 encoded user ID)
    try:
        user_id_part = parts[0]
        # Try to decode base64
        decoded = base64.b64decode(user_id_part + '==')  # Add padding
        print(f"✅ User ID part looks valid: {user_id_part}")
    except Exception as e:
        print(f"❌ User ID part invalid - not proper base64: {e}")
        print(f"   Problem character might be: {user_id_part}")
        return False
    
    # Check timestamp part
    if not parts[1].startswith('G'):
        print(f"⚠️  Timestamp part unusual - typically starts with G: {parts[1]}")
    else:
        print(f"✅ Timestamp part looks valid: {parts[1]}")
    
    # Check HMAC part
    if len(parts[2]) < 20:
        print(f"❌ HMAC part too short: {parts[2]}")
        return False
    else:
        print(f"✅ HMAC part looks valid: {parts[2][:20]}...")
    
    return True

# Verify both tokens
print("🤖 Discord Token Verification")
print("=" * 60)

mac_valid = verify_token_format(MAC_TOKEN, "Mac Claude Token")
server_valid = verify_token_format(SERVER_TOKEN, "Server Claude Token")

print("\n📊 Summary:")
print(f"Mac Claude Token: {'✅ Valid Format' if mac_valid else '❌ Invalid Format'}")
print(f"Server Claude Token: {'✅ Valid Format' if server_valid else '❌ Invalid Format'}")

print("\n💡 Notes:")
print("1. The token format looks unusual - there might be a typo")
print("2. The 'Qx' in the Mac token (MTM4MTMxQxOT...) looks suspicious")
print("3. Discord tokens are case-sensitive")
print("4. Make sure no extra spaces or characters when copying")

print("\n🔧 To get the correct token:")
print("1. Go to https://discord.com/developers/applications")
print("2. Click on 'Mac Claude Bot' (MCB)")
print("3. Go to 'Bot' section")
print("4. Click 'Reset Token' to generate a new one")
print("5. Copy the ENTIRE token carefully")