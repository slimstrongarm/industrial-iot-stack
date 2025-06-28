#!/usr/bin/env python3

import json
from googleapiclient.discovery import build
from google.oauth2 import service_account

def main():
    # Setup credentials
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
    SERVICE_ACCOUNT_FILE = '/home/server/google-sheets-credentials.json'
    SPREADSHEET_ID = '1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do'
    
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    
    service = build('sheets', 'v4', credentials=credentials)
    sheet = service.spreadsheets()
    
    try:
        # Read the entire Mac Claude Session Summary tab
        result = sheet.values().get(
            spreadsheetId=SPREADSHEET_ID,
            range="'Mac Claude Session Summary'!A:Z"
        ).execute()
        
        values = result.get('values', [])
        
        print("=== COMPLETE MAC CLAUDE SESSION SUMMARY STRUCTURE ===\n")
        
        # Print every row to see the complete structure
        for i, row in enumerate(values, 1):
            if row and any(cell.strip() for cell in row if cell):  # Only show rows with content
                # Show the first few columns that have content
                content_cells = [cell for cell in row if cell.strip()]
                if content_cells:
                    print(f"Row {i:2d}: {' | '.join(content_cells)}")
        
        print(f"\n=== VISUAL STRUCTURE ANALYSIS ===")
        
        # Identify sections based on emoji and formatting patterns
        sections = []
        current_section = None
        
        for i, row in enumerate(values, 1):
            if row and row[0].strip():
                cell = row[0].strip()
                
                # Check if this is a section header (contains emoji or is all caps with special chars)
                if ('📋' in cell or '🗂️' in cell or '🔧' in cell or '🏭' in cell or '🚀' in cell or '📁' in cell or
                    cell.isupper() or cell.startswith('=')):
                    if current_section:
                        sections.append(current_section)
                    current_section = {
                        'title': cell,
                        'start_row': i,
                        'content': []
                    }
                elif current_section:
                    current_section['content'].append((i, row))
        
        if current_section:
            sections.append(current_section)
        
        print("Identified sections:")
        for section in sections:
            print(f"\n📌 {section['title']} (starts at row {section['start_row']})")
            for row_num, row_content in section['content'][:5]:  # Show first 5 rows of each section
                if row_content and any(cell.strip() for cell in row_content if cell):
                    content = ' | '.join([cell for cell in row_content if cell.strip()])
                    print(f"    Row {row_num}: {content}")
            if len(section['content']) > 5:
                print(f"    ... and {len(section['content']) - 5} more rows")
        
        # Look for Discord information
        print(f"\n=== DISCORD INFORMATION SEARCH ===")
        discord_found = False
        for i, row in enumerate(values, 1):
            if row:
                for cell in row:
                    if cell and 'discord' in cell.lower():
                        print(f"Row {i}: {' | '.join([c for c in row if c.strip()])}")
                        discord_found = True
        
        if not discord_found:
            print("No Discord information found in Mac Claude Session Summary")
        
        # Check the separate Discord server link tab
        print(f"\n=== CHECKING DISCORD SERVER LINK TAB ===")
        try:
            discord_result = sheet.values().get(
                spreadsheetId=SPREADSHEET_ID,
                range="'Discord server link'!A:Z"
            ).execute()
            
            discord_values = discord_result.get('values', [])
            if discord_values:
                print("Discord server link tab content:")
                for i, row in enumerate(discord_values, 1):
                    if row and any(cell.strip() for cell in row if cell):
                        content = ' | '.join([cell for cell in row if cell.strip()])
                        print(f"  Row {i}: {content}")
            else:
                print("Discord server link tab is empty")
        except Exception as e:
            print(f"Could not read Discord server link tab: {e}")
        
        # Get formatting for the header
        print(f"\n=== HEADER FORMATTING DETAILS ===")
        try:
            spreadsheet_full = sheet.get(
                spreadsheetId=SPREADSHEET_ID,
                ranges=["'Mac Claude Session Summary'!A1:Z5"],
                includeGridData=True
            ).execute()
            
            if 'sheets' in spreadsheet_full:
                sheet_data = spreadsheet_full['sheets'][0]
                if 'data' in sheet_data and sheet_data['data']:
                    grid_data = sheet_data['data'][0]
                    if 'rowData' in grid_data:
                        for row_idx, row_data in enumerate(grid_data['rowData'][:5]):
                            if 'values' in row_data:
                                print(f"\nRow {row_idx + 1} formatting:")
                                for col_idx, cell_data in enumerate(row_data['values'][:10]):
                                    if 'effectiveFormat' in cell_data:
                                        fmt = cell_data['effectiveFormat']
                                        cell_value = cell_data.get('formattedValue', '')
                                        
                                        details = []
                                        
                                        # Background color
                                        if 'backgroundColor' in fmt:
                                            bg = fmt['backgroundColor']
                                            if any(bg.get(c, 0) != 1 for c in ['red', 'green', 'blue']):
                                                r, g, b = bg.get('red', 0), bg.get('green', 0), bg.get('blue', 0)
                                                details.append(f"BG: RGB({r:.2f}, {g:.2f}, {b:.2f})")
                                        
                                        # Text formatting
                                        if 'textFormat' in fmt:
                                            tf = fmt['textFormat']
                                            text_attrs = []
                                            if tf.get('bold'): text_attrs.append('BOLD')
                                            if tf.get('italic'): text_attrs.append('ITALIC')
                                            if tf.get('underline'): text_attrs.append('UNDERLINE')
                                            if text_attrs:
                                                details.append(f"Text: {', '.join(text_attrs)}")
                                            
                                            # Font size
                                            if 'fontSize' in tf:
                                                details.append(f"Size: {tf['fontSize']}")
                                        
                                        # Borders
                                        if 'borders' in fmt:
                                            borders = fmt['borders']
                                            border_sides = []
                                            for side in ['top', 'bottom', 'left', 'right']:
                                                if side in borders and borders[side].get('style') != 'NONE':
                                                    border_sides.append(side)
                                            if border_sides:
                                                details.append(f"Borders: {', '.join(border_sides)}")
                                        
                                        if details:
                                            print(f"  Col {col_idx + 1} ('{cell_value}'): {' | '.join(details)}")
        
        except Exception as e:
            print(f"Could not get detailed formatting: {e}")
    
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()