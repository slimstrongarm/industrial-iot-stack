#!/usr/bin/env python3
"""
Create a live file tree visualization in Google Sheets for easy project navigation
"""

import os
import json
import sys
from pathlib import Path
from datetime import datetime

# Add the scripts directory to Python path for imports
script_dir = Path(__file__).parent
sys.path.append(str(script_dir))

try:
    from google.oauth2.service_account import Credentials
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
except ImportError:
    print("❌ Google API libraries not installed")
    sys.exit(1)

def scan_directory_tree(root_path, max_depth=4, ignore_patterns=None):
    """Scan directory and create tree structure"""
    
    if ignore_patterns is None:
        ignore_patterns = [
            '.git', '__pycache__', 'node_modules', '.pytest_cache',
            '.vscode', '.idea', '*.pyc', '*.log', '.env',
            'Temp', 'temp', 'tmp', '.tmp', 'AppData'
        ]
    
    tree_data = []
    
    def should_ignore(path_name):
        """Check if path should be ignored"""
        for pattern in ignore_patterns:
            if pattern.startswith('*'):
                if path_name.endswith(pattern[1:]):
                    return True
            elif pattern in path_name or path_name == pattern:
                return True
        return False
    
    def scan_recursive(current_path, depth=0, parent_path=""):
        """Recursively scan directory"""
        if depth > max_depth:
            return
        
        try:
            items = sorted(os.listdir(current_path))
        except (PermissionError, FileNotFoundError):
            return
        
        for item in items:
            if should_ignore(item):
                continue
                
            item_path = os.path.join(current_path, item)
            relative_path = os.path.relpath(item_path, root_path)
            
            # Create indentation for tree structure
            indent = "  " * depth
            
            if os.path.isdir(item_path):
                # Directory
                tree_data.append({
                    'level': depth,
                    'type': 'directory',
                    'name': f"{indent}📁 {item}/",
                    'path': relative_path,
                    'size': '',
                    'modified': '',
                    'parent': parent_path
                })
                
                # Recurse into subdirectory
                scan_recursive(item_path, depth + 1, relative_path)
            else:
                # File
                try:
                    stat_info = os.stat(item_path)
                    size = stat_info.st_size
                    modified = datetime.fromtimestamp(stat_info.st_mtime).strftime('%Y-%m-%d %H:%M')
                    
                    # File type icon
                    file_icon = get_file_icon(item)
                    
                    tree_data.append({
                        'level': depth,
                        'type': 'file',
                        'name': f"{indent}{file_icon} {item}",
                        'path': relative_path,
                        'size': format_file_size(size),
                        'modified': modified,
                        'parent': parent_path
                    })
                except (PermissionError, FileNotFoundError):
                    continue
    
    scan_recursive(root_path)
    return tree_data

def get_file_icon(filename):
    """Get appropriate icon for file type"""
    ext = Path(filename).suffix.lower()
    
    icons = {
        '.py': '🐍',
        '.js': '📜',
        '.json': '📋',
        '.md': '📝',
        '.txt': '📄',
        '.yml': '⚙️',
        '.yaml': '⚙️',
        '.docker': '🐳',
        '.sh': '⚡',
        '.bat': '⚡',
        '.sql': '🗃️',
        '.csv': '📊',
        '.xml': '📰',
        '.html': '🌐',
        '.css': '🎨',
        '.png': '🖼️',
        '.jpg': '🖼️',
        '.jpeg': '🖼️',
        '.gif': '🖼️',
        '.pdf': '📕',
        '.zip': '📦',
        '.tar': '📦',
        '.gz': '📦'
    }
    
    return icons.get(ext, '📄')

def format_file_size(size_bytes):
    """Format file size in human readable format"""
    if size_bytes == 0:
        return "0 B"
    
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"

def create_file_tree_sheet():
    """Create file tree visualization in Google Sheets"""
    
    # Configuration
    SPREADSHEET_ID = "1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do"
    CREDENTIALS_FILE = "/home/server/google-sheets-credentials.json"
    ROOT_PATH = "/mnt/c/Users/LocalAccount/industrial-iot-stack"
    
    print("🌳 Creating File Tree Visualization")
    print("=" * 40)
    
    try:
        # Load credentials
        creds = Credentials.from_service_account_file(
            CREDENTIALS_FILE,
            scopes=['https://www.googleapis.com/auth/spreadsheets']
        )
        
        # Build service
        service = build('sheets', 'v4', credentials=creds)
        
        print("✅ Connected to Google Sheets API")
        
        # Scan directory tree
        print(f"📂 Scanning directory tree: {ROOT_PATH}")
        tree_data = scan_directory_tree(ROOT_PATH, max_depth=5)
        
        print(f"📊 Found {len(tree_data)} items")
        
        # Create new sheet
        new_sheet_title = "File Tree Visualization"
        
        # Check if sheet already exists
        spreadsheet = service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID).execute()
        existing_sheets = [sheet['properties']['title'] for sheet in spreadsheet['sheets']]
        
        if new_sheet_title in existing_sheets:
            print(f"⚠️  Sheet '{new_sheet_title}' already exists, will overwrite")
        else:
            # Create new sheet
            request_body = {
                'requests': [{
                    'addSheet': {
                        'properties': {
                            'title': new_sheet_title,
                            'gridProperties': {
                                'rowCount': max(len(tree_data) + 10, 100),
                                'columnCount': 8
                            }
                        }
                    }
                }]
            }
            
            service.spreadsheets().batchUpdate(
                spreadsheetId=SPREADSHEET_ID,
                body=request_body
            ).execute()
            
            print(f"✅ Created new sheet: {new_sheet_title}")
        
        # Prepare sheet data
        sheet_data = [
            # Header row
            ["File/Directory", "Type", "Path", "Size", "Modified", "Level", "Parent", "Actions"],
            
            # Summary row
            [f"📊 Project Tree ({len(tree_data)} items)", "", ROOT_PATH, "", datetime.now().strftime('%Y-%m-%d %H:%M'), "", "", "Last Updated"],
            ["", "", "", "", "", "", "", ""],
        ]
        
        # Add tree data
        for item in tree_data:
            sheet_data.append([
                item['name'],
                item['type'].title(),
                item['path'],
                item['size'],
                item['modified'],
                item['level'],
                item['parent'],
                '🔗 Open' if item['type'] == 'file' else '📂 Browse'
            ])
        
        # Add quick navigation section
        sheet_data.extend([
            ["", "", "", "", "", "", "", ""],
            ["🚀 QUICK NAVIGATION", "", "", "", "", "", "", ""],
            ["📁 Key Directories", "", "", "", "", "", "", ""],
            ["📂 scripts/", "directory", "scripts", "", "", "", "", "Python automation scripts"],
            ["📂 docs/", "directory", "docs", "", "", "", "", "Documentation files"],
            ["📂 configs/", "directory", "configs", "", "", "", "", "Configuration files"],
            ["", "", "", "", "", "", "", ""],
            ["📄 Key Files", "", "", "", "", "", "", ""],
            ["📝 README.md", "file", "README.md", "", "", "", "", "Project overview"],
            ["⚙️ docker-compose.yml", "file", "docker-compose.yml", "", "", "", "", "Docker stack config"],
            ["📋 STACK_CONFIG.md", "file", "STACK_CONFIG.md", "", "", "", "", "System configuration"],
            ["📊 N8N_INTEGRATION_COMPLETE.md", "file", "N8N_INTEGRATION_COMPLETE.md", "", "", "", "", "n8n setup guide"],
            ["", "", "", "", "", "", "", ""],
            ["📊 STATISTICS", "", "", "", "", "", "", ""],
            [f"Total Files: {len([x for x in tree_data if x['type'] == 'file'])}", "", "", "", "", "", "", ""],
            [f"Total Directories: {len([x for x in tree_data if x['type'] == 'directory'])}", "", "", "", "", "", "", ""],
            [f"Max Depth: {max([x['level'] for x in tree_data]) if tree_data else 0}", "", "", "", "", "", "", ""],
            [f"Last Scan: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", "", "", "", "", "", "", ""]
        ])
        
        # Write data to sheet
        range_name = f"'{new_sheet_title}'!A1"
        body = {
            'values': sheet_data
        }
        
        result = service.spreadsheets().values().update(
            spreadsheetId=SPREADSHEET_ID,
            range=range_name,
            valueInputOption='RAW',
            body=body
        ).execute()
        
        print(f"✅ File tree visualization created")
        print(f"📊 {result.get('updatedCells')} cells updated")
        
        # Apply formatting
        sheet_id = None
        spreadsheet = service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID).execute()
        for sheet in spreadsheet['sheets']:
            if sheet['properties']['title'] == new_sheet_title:
                sheet_id = sheet['properties']['sheetId']
                break
        
        if sheet_id:
            # Format header and sections
            format_requests = [
                # Header row
                {
                    'repeatCell': {
                        'range': {
                            'sheetId': sheet_id,
                            'startRowIndex': 0,
                            'endRowIndex': 1,
                            'startColumnIndex': 0,
                            'endColumnIndex': 8
                        },
                        'cell': {
                            'userEnteredFormat': {
                                'backgroundColor': {'red': 0.2, 'green': 0.7, 'blue': 0.2},
                                'textFormat': {'bold': True, 'foregroundColor': {'red': 1, 'green': 1, 'blue': 1}}
                            }
                        },
                        'fields': 'userEnteredFormat(backgroundColor,textFormat)'
                    }
                },
                # Directory rows (light blue background)
                {
                    'addConditionalFormatRule': {
                        'rule': {
                            'ranges': [{
                                'sheetId': sheet_id,
                                'startRowIndex': 3,
                                'endRowIndex': len(sheet_data),
                                'startColumnIndex': 0,
                                'endColumnIndex': 8
                            }],
                            'booleanRule': {
                                'condition': {
                                    'type': 'TEXT_CONTAINS',
                                    'values': [{'userEnteredValue': '📁'}]
                                },
                                'format': {
                                    'backgroundColor': {'red': 0.9, 'green': 0.95, 'blue': 1.0}
                                }
                            }
                        },
                        'index': 0
                    }
                }
            ]
            
            service.spreadsheets().batchUpdate(
                spreadsheetId=SPREADSHEET_ID,
                body={'requests': format_requests}
            ).execute()
            
            print("✅ Applied formatting to file tree")
        
        # Create summary
        files_count = len([x for x in tree_data if x['type'] == 'file'])
        dirs_count = len([x for x in tree_data if x['type'] == 'directory'])
        
        print(f"\n📊 File Tree Summary:")
        print(f"📄 Files: {files_count}")
        print(f"📁 Directories: {dirs_count}")
        print(f"🎯 Total Items: {len(tree_data)}")
        print(f"📏 Max Depth: {max([x['level'] for x in tree_data]) if tree_data else 0} levels")
        
        print(f"\n🌳 Key Features:")
        print("• Visual tree structure with indentation")
        print("• File type icons for easy identification")
        print("• File sizes and modification dates")
        print("• Quick navigation section")
        print("• Live statistics")
        print("• Filterable by file type or directory")
        
        return True
        
    except HttpError as error:
        print(f"❌ Google Sheets API error: {error}")
        return False
    except Exception as error:
        print(f"❌ Unexpected error: {error}")
        return False

def create_github_tree_alternative():
    """Create GitHub-style tree using tree command if available"""
    
    print("\n🐙 GitHub Alternative: Generate tree command output")
    print("=" * 50)
    
    try:
        import subprocess
        
        # Try to use tree command
        result = subprocess.run(['tree', '-a', '-I', '.git|__pycache__|node_modules|.pytest_cache|Temp'], 
                              capture_output=True, text=True, cwd='/mnt/c/Users/LocalAccount/industrial-iot-stack')
        
        if result.returncode == 0:
            # Save tree output to file
            tree_output = result.stdout
            with open('/mnt/c/Users/LocalAccount/industrial-iot-stack/PROJECT_TREE.txt', 'w') as f:
                f.write(f"# Project File Tree\n")
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                f.write("```\n")
                f.write(tree_output)
                f.write("\n```\n")
            
            print("✅ Created PROJECT_TREE.txt with tree command output")
            print("📁 File saved: PROJECT_TREE.txt")
            return True
        else:
            print("⚠️  tree command not available")
            return False
            
    except Exception as e:
        print(f"❌ Error generating tree: {e}")
        return False

if __name__ == "__main__":
    print("🌳 File Tree Visualization Creator")
    print("=" * 40)
    
    # Create Google Sheets visualization
    sheets_success = create_file_tree_sheet()
    
    # Try GitHub alternative
    github_success = create_github_tree_alternative()
    
    if sheets_success:
        print("\n🎉 Google Sheets file tree created successfully!")
        print("📊 Open 'File Tree Visualization' tab to browse project structure")
        
        print("\n💡 Features Available:")
        print("• Interactive file browser in Google Sheets")
        print("• Visual tree structure with icons")
        print("• File sizes and modification dates")
        print("• Quick navigation shortcuts")
        print("• Live project statistics")
        
    if github_success:
        print("📄 Text-based tree also saved to PROJECT_TREE.txt")
        
    if not sheets_success and not github_success:
        print("\n📝 Manual alternative: Use 'ls -la' or file explorer")
        sys.exit(1)