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
        # First, get all sheet tabs to find the Mac Claude Session Summary tab
        spreadsheet = sheet.get(spreadsheetId=SPREADSHEET_ID).execute()
        sheets_list = spreadsheet.get('sheets', [])
        
        print("Available sheets/tabs:")
        mac_claude_tab = None
        for sheet_info in sheets_list:
            title = sheet_info['properties']['title']
            print(f"  - {title}")
            if 'mac claude' in title.lower() and 'session' in title.lower() and 'summary' in title.lower():
                mac_claude_tab = title
        
        if not mac_claude_tab:
            print("\nLooking for variations...")
            for sheet_info in sheets_list:
                title = sheet_info['properties']['title']
                if 'mac' in title.lower() and ('session' in title.lower() or 'summary' in title.lower()):
                    mac_claude_tab = title
                    print(f"Found potential match: {title}")
                    break
        
        if not mac_claude_tab:
            print("\nNo Mac Claude Session Summary tab found. Available tabs:")
            for sheet_info in sheets_list:
                print(f"  - {sheet_info['properties']['title']}")
            return
        
        print(f"\nReading from tab: '{mac_claude_tab}'")
        
        # Read the entire sheet content
        result = sheet.values().get(
            spreadsheetId=SPREADSHEET_ID,
            range=f"'{mac_claude_tab}'!A:Z"  # Read columns A through Z
        ).execute()
        
        values = result.get('values', [])
        
        if not values:
            print("No data found in the Mac Claude Session Summary tab.")
            return
        
        print(f"\n=== MAC CLAUDE SESSION SUMMARY TAB STRUCTURE ===")
        print(f"Total rows: {len(values)}")
        
        # Show the structure and content
        for i, row in enumerate(values[:50], 1):  # Show first 50 rows
            if row:  # Only show non-empty rows
                # Pad row to show empty cells
                padded_row = row + [''] * (10 - len(row)) if len(row) < 10 else row[:10]
                row_display = " | ".join(f"{cell:<20}" for cell in padded_row)
                print(f"Row {i:2d}: {row_display}")
        
        if len(values) > 50:
            print(f"... and {len(values) - 50} more rows")
        
        # Analyze the structure
        print(f"\n=== STRUCTURE ANALYSIS ===")
        
        # Find headers (likely in first few rows)
        headers_found = []
        for i, row in enumerate(values[:10]):
            if row and any(cell.strip() for cell in row):
                print(f"Row {i+1} content: {row}")
                if any(keyword in str(cell).lower() for cell in row 
                       for keyword in ['session', 'summary', 'date', 'task', 'status', 'notes']):
                    headers_found.append((i+1, row))
        
        if headers_found:
            print(f"\nPotential header rows:")
            for row_num, header_row in headers_found:
                print(f"  Row {row_num}: {header_row}")
        
        # Look for patterns
        print(f"\n=== FORMATTING PATTERNS ===")
        
        # Check for common patterns
        non_empty_rows = [i+1 for i, row in enumerate(values) if row and any(cell.strip() for cell in row)]
        print(f"Non-empty rows: {len(non_empty_rows)} out of {len(values)}")
        
        # Look for sections or categories
        section_markers = []
        for i, row in enumerate(values):
            if row and len(row) >= 1 and row[0].strip():
                cell = row[0].strip()
                if (cell.isupper() or 
                    cell.startswith('=') or 
                    '---' in cell or 
                    cell.endswith(':') or
                    len(cell.split()) <= 3):
                    section_markers.append((i+1, cell))
        
        if section_markers:
            print(f"\nPotential section markers:")
            for row_num, marker in section_markers[:20]:  # Show first 20
                print(f"  Row {row_num}: '{marker}'")
        
        # Also try to get any formatting information
        print(f"\n=== CHECKING FOR FORMATTING INFO ===")
        try:
            # Get formatting information
            spreadsheet_full = sheet.get(
                spreadsheetId=SPREADSHEET_ID,
                ranges=[f"'{mac_claude_tab}'!A1:Z100"],
                includeGridData=True
            ).execute()
            
            if 'sheets' in spreadsheet_full:
                sheet_data = spreadsheet_full['sheets'][0]
                if 'data' in sheet_data and sheet_data['data']:
                    grid_data = sheet_data['data'][0]
                    if 'rowData' in grid_data:
                        print("Found formatting data - analyzing colors and styles...")
                        
                        formatted_cells = []
                        for row_idx, row_data in enumerate(grid_data['rowData'][:20]):
                            if 'values' in row_data:
                                for col_idx, cell_data in enumerate(row_data['values']):
                                    if 'effectiveFormat' in cell_data:
                                        fmt = cell_data['effectiveFormat']
                                        cell_value = cell_data.get('formattedValue', '')
                                        
                                        # Check for background color
                                        bg_color = None
                                        if 'backgroundColor' in fmt:
                                            bg = fmt['backgroundColor']
                                            if any(bg.get(c, 0) != 1 for c in ['red', 'green', 'blue']):
                                                bg_color = f"RGB({bg.get('red', 0):.2f}, {bg.get('green', 0):.2f}, {bg.get('blue', 0):.2f})"
                                        
                                        # Check for text formatting
                                        text_fmt = []
                                        if 'textFormat' in fmt:
                                            tf = fmt['textFormat']
                                            if tf.get('bold'): text_fmt.append('BOLD')
                                            if tf.get('italic'): text_fmt.append('ITALIC')
                                            if tf.get('underline'): text_fmt.append('UNDERLINE')
                                        
                                        if bg_color or text_fmt:
                                            formatted_cells.append({
                                                'row': row_idx + 1,
                                                'col': col_idx + 1,
                                                'value': cell_value,
                                                'bg_color': bg_color,
                                                'text_format': text_fmt
                                            })
                        
                        if formatted_cells:
                            print("Formatted cells found:")
                            for cell in formatted_cells[:10]:  # Show first 10
                                print(f"  Row {cell['row']}, Col {cell['col']}: '{cell['value']}' - "
                                      f"Background: {cell['bg_color']}, Format: {cell['text_format']}")
                        else:
                            print("No special formatting detected in first 20 rows")
        
        except Exception as e:
            print(f"Could not retrieve formatting info: {e}")
    
    except Exception as e:
        print(f"Error reading spreadsheet: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()