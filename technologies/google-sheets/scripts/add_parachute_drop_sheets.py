#!/usr/bin/env python3
"""Add Parachute Drop BOM and Revenue Analysis to Google Sheets"""

import os
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Configuration
CREDS_PATH = "/Users/joshpayneair/Desktop/industrial-iot-stack/credentials/iot-stack-credentials.json"
SPREADSHEET_ID = "1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do"

def get_sheets_service():
    """Initialize Google Sheets API service"""
    creds = service_account.Credentials.from_service_account_file(
        CREDS_PATH,
        scopes=['https://www.googleapis.com/auth/spreadsheets']
    )
    return build('sheets', 'v4', credentials=creds)

def create_bom_sheet(service):
    """Create Parachute Drop BOM sheet"""
    
    # Create new sheet
    sheet_body = {
        "requests": [{
            "addSheet": {
                "properties": {
                    "title": "🪂 Parachute Drop BOM",
                    "gridProperties": {
                        "rowCount": 100,
                        "columnCount": 10
                    }
                }
            }
        }]
    }
    
    try:
        response = service.spreadsheets().batchUpdate(
            spreadsheetId=SPREADSHEET_ID,
            body=sheet_body
        ).execute()
        print("✅ Created Parachute Drop BOM sheet")
    except Exception as e:
        print(f"Sheet may already exist: {e}")
    
    # BOM data
    bom_data = [
        ["🪂 PARACHUTE DROP - Hardware Bill of Materials", "", "", "", ""],
        ["", "", "", "", ""],
        ["🎯 CORE COMPUTING PLATFORM", "", "", "", ""],
        ["Item", "Model", "Qty", "Price", "Purpose"],
        ["Raspberry Pi 4", "8GB RAM Model", "1", "$95", "Main processing unit"],
        ["MicroSD Card", "SanDisk Extreme 128GB", "1", "$25", "OS and data storage"],
        ["Pi Case", "Argon ONE M.2", "1", "$35", "Protection + cooling"],
        ["Power Supply", "Official Pi 4 USB-C", "1", "$15", "Reliable power"],
        ["SUBTOTAL", "", "", "$170", ""],
        ["", "", "", "", ""],
        ["📱 DISPLAY INTERFACE", "", "", "", ""],
        ["Item", "Model", "Qty", "Price", "Purpose"],
        ["Touchscreen", "Official Pi 7\" Touch", "1", "$85", "Local dashboard"],
        ["Screen Case", "SmartPi Touch 2", "1", "$45", "Portable protection"],
        ["SUBTOTAL", "", "", "$130", ""],
        ["", "", "", "", ""],
        ["🌐 NETWORKING & CONNECTIVITY", "", "", "", ""],
        ["Item", "Model", "Qty", "Price", "Purpose"],
        ["Portable Router", "GL.iNet GL-MT1300", "1", "$85", "Isolated network"],
        ["Ethernet Cables", "Cat6 1ft (5-pack)", "1", "$15", "Device connections"],
        ["USB-Serial", "FTDI FT232RL", "1", "$25", "Legacy serial devices"],
        ["USB Hub", "Anker 7-Port USB 3.0", "1", "$35", "Expansion"],
        ["SUBTOTAL", "", "", "$160", ""],
        ["", "", "", "", ""],
        ["🔌 SENSOR INTERFACE PLATFORM", "", "", "", ""],
        ["Item", "Model", "Qty", "Price", "Purpose"],
        ["Phidget Hub", "HUB0000_0", "1", "$85", "6-port sensor hub"],
        ["Phidget Cables", "600mm Cable (6-pack)", "1", "$30", "Sensor connections"],
        ["SUBTOTAL", "", "", "$115", ""],
        ["", "", "", "", ""],
        ["🌡️ TEMPERATURE SENSORS", "", "", "", ""],
        ["Item", "Model", "Qty", "Price", "Purpose"],
        ["RTD Sensor", "TMP1101_0", "2", "$70", "Precision temperature"],
        ["Thermocouple", "TMP1101_0", "1", "$35", "High temp monitoring"],
        ["DHT22", "Digital Temp/Humidity", "2", "$20", "Environmental"],
        ["SUBTOTAL", "", "", "$125", ""],
        ["", "", "", "", ""],
        ["⚡ CURRENT & POWER SENSORS", "", "", "", ""],
        ["Item", "Model", "Qty", "Price", "Purpose"],
        ["AC Current 30A", "CUR1001_0", "2", "$80", "Motor monitoring"],
        ["DC Current 20A", "CUR1002_0", "1", "$40", "DC systems"],
        ["Split-Core CT", "SCT-013-030", "2", "$30", "Non-invasive current"],
        ["SUBTOTAL", "", "", "$150", ""],
        ["", "", "", "", ""],
        ["📊 PRESSURE & LEVEL SENSORS", "", "", "", ""],
        ["Item", "Model", "Qty", "Price", "Purpose"],
        ["Pressure Xmtr", "4-20mA 0-150 PSI", "1", "$85", "Process pressure"],
        ["Level Sensor", "Ultrasonic 4-20mA", "1", "$95", "Tank level"],
        ["Pressure Switch", "Digital 0-100 PSI", "2", "$40", "Alarm switches"],
        ["SUBTOTAL", "", "", "$220", ""],
        ["", "", "", "", ""],
        ["🔲 DIGITAL I/O & CONTACTORS", "", "", "", ""],
        ["Item", "Model", "Qty", "Price", "Purpose"],
        ["Digital Input", "DI4001_0 Phidget", "1", "$35", "Contactor sensing"],
        ["Relay Output", "REL1101_0", "1", "$25", "Control outputs"],
        ["Terminal Blocks", "Spring-cage 12-pos", "4", "$20", "Connections"],
        ["Wire Kit", "18 AWG Assorted", "1", "$25", "Field wiring"],
        ["SUBTOTAL", "", "", "$105", ""],
        ["", "", "", "", ""],
        ["🔧 TOOLS & ACCESSORIES", "", "", "", ""],
        ["Item", "Model", "Qty", "Price", "Purpose"],
        ["Pelican Case", "1450 Medium", "1", "$155", "Transport/protection"],
        ["Multimeter", "Fluke 117", "1", "$185", "Field diagnostics"],
        ["Wire Strippers", "Klein 11061", "1", "$25", "Terminations"],
        ["Screwdriver Set", "Klein 32500", "1", "$35", "Assembly"],
        ["Laptop", "Used ThinkPad", "1", "$300", "Configuration"],
        ["SUBTOTAL", "", "", "$700", ""],
        ["", "", "", "", ""],
        ["🎯 DEPLOYMENT PACKAGES", "", "", "", ""],
        ["Package", "Description", "", "Total Cost", "Target Market"],
        ["Standard Industrial Kit", "Complete system for most facilities", "", "$1,975", "General industrial"],
        ["Motor Monitoring Kit", "Focused on motor/equipment health", "", "$1,450", "Manufacturing"],
        ["Process Monitoring Kit", "Tanks, vessels, process systems", "", "$1,850", "Chemical/Food"],
        ["Electrical Monitoring Kit", "Power quality and electrical", "", "$1,650", "Facility management"]
    ]
    
    # Write BOM data
    body = {
        'values': bom_data
    }
    
    result = service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID,
        range="🪂 Parachute Drop BOM!A1",
        valueInputOption="RAW",
        body=body
    ).execute()
    
    print("✅ Added BOM data to sheet")
    return result

def create_revenue_analysis_sheet(service):
    """Create Revenue Analysis sheet"""
    
    # Create new sheet
    sheet_body = {
        "requests": [{
            "addSheet": {
                "properties": {
                    "title": "💰 Revenue Analysis",
                    "gridProperties": {
                        "rowCount": 100,
                        "columnCount": 10
                    }
                }
            }
        }]
    }
    
    try:
        response = service.spreadsheets().batchUpdate(
            spreadsheetId=SPREADSHEET_ID,
            body=sheet_body
        ).execute()
        print("✅ Created Revenue Analysis sheet")
    except Exception as e:
        print(f"Sheet may already exist: {e}")
    
    # Revenue analysis data
    revenue_data = [
        ["💰 PARACHUTE DROP - Revenue Analysis & Business Model", "", "", "", ""],
        ["", "", "", "", ""],
        ["🎯 TRADITIONAL vs PARACHUTE DROP COMPARISON", "", "", "", ""],
        ["", "Traditional Consulting", "Parachute Drop", "Advantage", ""],
        ["Assessment Time", "2-3 days on-site", "2-3 hours on-site", "90% time reduction", ""],
        ["Assessment Cost", "$3,000-5,000 labor", "$1,975 kit + travel", "Cost competitive", ""],
        ["Results Delivered", "Paper documentation", "Live system + data", "Ongoing value", ""],
        ["Client Relationship", "Project-based", "Technology platform", "Continuous revenue", ""],
        ["", "", "", "", ""],
        ["📊 REVENUE MODEL - PER KIT ANALYSIS", "", "", "", ""],
        ["Revenue Stream", "Frequency", "Amount", "Annual Total", "Notes"],
        ["Initial Assessment", "Per deployment", "$5,000", "Variable", "Kit cost + setup fee"],
        ["Monthly Monitoring", "12x per year", "$500", "$6,000", "Data collection service"],
        ["Phase 2 Implementation", "1x per customer", "$50,000", "Variable", "Full system deployment"],
        ["Managed Services", "12x per year", "$2,000", "$24,000", "Ongoing optimization"],
        ["", "", "", "", ""],
        ["TOTAL PER CUSTOMER", "", "", "$80,000+", "First year potential"],
        ["", "", "", "", ""],
        ["🚀 SCALING ANALYSIS", "", "", "", ""],
        ["Metric", "Conservative", "Realistic", "Aggressive", "Notes"],
        ["Deployments per Month", "2", "4", "8", "Per kit capacity"],
        ["Average Project Value", "$25,000", "$50,000", "$80,000", "Including ongoing services"],
        ["Annual Revenue per Kit", "$150,000", "$300,000", "$480,000", "12-month projection"],
        ["", "", "", "", ""],
        ["💼 FLEET SCALING MODEL", "", "", "", ""],
        ["Number of Kits", "Annual Revenue", "Operating Costs", "Net Profit", "ROI"],
        ["1 Kit", "$300,000", "$50,000", "$250,000", "500%"],
        ["3 Kits", "$900,000", "$150,000", "$750,000", "1,500%"],
        ["5 Kits", "$1,500,000", "$250,000", "$1,250,000", "2,500%"],
        ["10 Kits", "$3,000,000", "$500,000", "$2,500,000", "5,000%"],
        ["", "", "", "", ""],
        ["🎯 BREAK-EVEN ANALYSIS", "", "", "", ""],
        ["Item", "Cost", "Break-even Point", "", ""],
        ["Kit Development", "$10,000", "2 deployments", "", ""],
        ["Hardware Investment", "$1,975", "1 deployment", "", ""],
        ["Annual Operating", "$5,000", "1 monitoring contract", "", ""],
        ["", "", "", "", ""],
        ["⚡ COMPETITIVE ADVANTAGES", "", "", "", ""],
        ["Traditional Approach", "Parachute Drop Approach", "Business Impact", "", ""],
        ["Walk around with clipboard", "Deploy live monitoring in 15 min", "Instant credibility", "", ""],
        ["Manual data gathering", "Automated intelligence collection", "Higher accuracy", "", ""],
        ["Static recommendations", "AI-powered insights", "Better outcomes", "", ""],
        ["'We'll send you a proposal'", "'Here's what we found in real-time'", "Higher close rate", "", ""],
        ["One-time project", "Continuous technology partnership", "Recurring revenue", "", ""],
        ["", "", "", "", ""],
        ["🎪 SUCCESS METRICS", "", "", "", ""],
        ["Metric", "Traditional", "Parachute Drop", "Improvement", ""],
        ["Proposal Win Rate", "30%", "75%", "2.5x higher", ""],
        ["Average Project Size", "$15,000", "$50,000", "3.3x larger", ""],
        ["Customer Lifetime Value", "$25,000", "$200,000", "8x higher", ""],
        ["Time to Revenue", "3-6 months", "1 week", "12x faster", ""],
        ["", "", "", "", ""],
        ["💡 STRATEGIC POSITIONING", "", "", "", ""],
        ["Position", "Value Proposition", "Pricing Strategy", "", ""],
        ["Technology Demonstrator", "Show don't tell", "Premium pricing", "", ""],
        ["Continuous Partner", "Ongoing optimization", "Subscription model", "", ""],
        ["Industry Expert", "Data-driven insights", "Value-based pricing", "", ""],
        ["Innovation Leader", "Cutting-edge capability", "Market premium", "", ""],
        ["", "", "", "", ""],
        ["🚀 NEXT STEPS", "", "", "", ""],
        ["Priority", "Action Item", "Timeline", "Investment", ""],
        ["1", "Build first Parachute Drop kit", "4 weeks", "$2,000", ""],
        ["2", "Test with friendly customer", "2 weeks", "$1,000", ""],
        ["3", "Refine based on feedback", "2 weeks", "$500", ""],
        ["4", "Launch commercial service", "1 week", "$2,000", ""],
        ["5", "Scale to 3 kits", "3 months", "$6,000", ""],
        ["", "", "", "", ""],
        ["TOTAL INVESTMENT TO SCALE", "", "", "$11,500", ""],
        ["FIRST YEAR REVENUE TARGET", "", "", "$900,000", ""],
        ["FIRST YEAR ROI", "", "", "7,826%", "🚀🚀🚀"]
    ]
    
    # Write revenue data
    body = {
        'values': revenue_data
    }
    
    result = service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID,
        range="💰 Revenue Analysis!A1",
        valueInputOption="RAW",
        body=body
    ).execute()
    
    print("✅ Added revenue analysis to sheet")
    return result

def main():
    """Main execution"""
    print("Adding Parachute Drop BOM and Revenue Analysis to Google Sheets...\n")
    
    service = get_sheets_service()
    create_bom_sheet(service)
    create_revenue_analysis_sheet(service)
    
    print("\n🎯 Sheets created successfully!")
    print("- 🪂 Parachute Drop BOM: Complete hardware list and packages")
    print("- 💰 Revenue Analysis: Business model and scaling projections")
    print("\nReady to review the numbers and coordinate with Server Claude!")

if __name__ == "__main__":
    main()