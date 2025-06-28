#!/usr/bin/env python3
"""
Update .claude/INDEX.md to include ADK Hybrid Architecture information
without changing the existing format
"""

import requests
from pathlib import Path

def update_index_md():
    """Update INDEX.md with ADK information"""
    
    try:
        # Fetch current INDEX.md from GitHub
        url = "https://raw.githubusercontent.com/slimstrongarm/industrial-iot-stack/main/.claude/INDEX.md"
        response = requests.get(url)
        
        if response.status_code != 200:
            print(f"❌ Failed to fetch INDEX.md: {response.status_code}")
            return False
        
        current_content = response.text
        print("✅ Fetched current INDEX.md from GitHub")
        
        # Find the Development Tools section and add ADK information
        lines = current_content.split('\n')
        updated_lines = []
        
        for i, line in enumerate(lines):
            updated_lines.append(line)
            
            # Add ADK section after "Development Tools" header
            if line.strip() == "## 🛠️ Development Tools":
                # Add ADK section right after the header
                updated_lines.extend([
                    "",
                    "### ADK Hybrid Architecture",
                    "- **[ADK Onboarding Guide](ADK_ONBOARDING_GUIDE.md)** - Quick start for Claude instances",
                    "- **[Hybrid ADK Architecture](HYBRID_ADK_ARCHITECTURE.md)** - Complete technical specification",
                    "- **[CT-066 Completion Summary](CT-066_COMPLETION_SUMMARY.md)** - Implementation details",
                    "- **[State Persistence Engine](.claude/adk_enhanced/state_persistence.py)** - Instant context recovery",
                    "- **[Coordination Engine](.claude/adk_enhanced/coordination_engine.py)** - Smart task assignment",
                    "- **[Conflict Prevention](.claude/adk_enhanced/conflict_prevention.py)** - Work coordination",
                    "- **[Enhanced Mac Worker](scripts/adk_integration/enhanced_mac_worker.py)** - ADK-powered automation",
                    ""
                ])
        
        # Join the lines back together
        updated_content = '\n'.join(updated_lines)
        
        # Update the "Last Updated" timestamp at the bottom
        import datetime
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
        updated_content = updated_content.replace(
            "**Last Updated**: 2025-06-04 23:30:00 UTC",
            f"**Last Updated**: {current_time}"
        )
        
        # Write to local .claude folder (which will be committed to external repo)
        claude_dir = Path(__file__).parent.parent / ".claude"
        if not claude_dir.exists():
            claude_dir.mkdir(exist_ok=True)
        
        index_file = claude_dir / "INDEX.md"
        with open(index_file, 'w') as f:
            f.write(updated_content)
        
        print(f"✅ Updated local {index_file}")
        print("📋 Added ADK Hybrid Architecture section to Development Tools")
        
        return True
        
    except Exception as e:
        print(f"❌ Error updating INDEX.md: {e}")
        return False

def main():
    """Main function"""
    print("📚 Updating .claude/INDEX.md with ADK information")
    print("=" * 50)
    
    success = update_index_md()
    
    if success:
        print("\n✅ INDEX.md update completed!")
        print("\n📋 What was added:")
        print("   • ADK Hybrid Architecture section in Development Tools")
        print("   • Links to all ADK components and documentation")
        print("   • Preserves existing format and structure")
        print("   • Updated timestamp")
        print("\n🔄 Ready to commit and push to external repo")
    else:
        print("\n❌ Update failed")

if __name__ == "__main__":
    main()