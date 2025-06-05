#!/usr/bin/env python3
"""
Formbricks API Integration Client - Mac Claude CT-018
Hybrid approach supporting both API and webhook methods
"""

import requests
import json
from datetime import datetime
from pathlib import Path
import gspread
from oauth2client.service_account import ServiceAccountCredentials

class FormbricksAPIClient:
    """
    Formbricks API client for brewery equipment monitoring
    Supports both direct API calls and webhook processing
    """
    
    def __init__(self, api_key=None, base_url="https://app.formbricks.com"):
        """Initialize Formbricks API client"""
        self.api_key = api_key or "YOUR_FORMBRICKS_API_KEY"
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # Google Sheets integration
        self.sheet_client = self._init_sheets()
    
    def _init_sheets(self):
        """Initialize Google Sheets connection for logging"""
        try:
            creds_file = str(Path.home() / 'Desktop/industrial-iot-stack/credentials/iot-stack-credentials.json')
            scope = ['https://spreadsheets.google.com/feeds',
                     'https://www.googleapis.com/auth/drive']
            creds = ServiceAccountCredentials.from_json_keyfile_name(creds_file, scope)
            client = gspread.authorize(creds)
            sheet_id = '1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do'
            return client.open_by_key(sheet_id)
        except Exception as e:
            print(f"⚠️  Sheets connection warning: {e}")
            return None
    
    # === SURVEY MANAGEMENT ===
    
    def get_surveys(self):
        """Get all surveys from Formbricks"""
        try:
            response = requests.get(
                f"{self.base_url}/api/v1/surveys",
                headers=self.headers,
                timeout=10
            )
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"API Error: {response.status_code}"}
        except Exception as e:
            return {"error": str(e)}
    
    def create_equipment_survey(self, equipment_type, location):
        """Create equipment-specific survey"""
        survey_data = {
            "name": f"{equipment_type} Inspection - {location}",
            "type": "link",
            "questions": [
                {
                    "type": "openText",
                    "headline": f"Equipment ID for {equipment_type}",
                    "required": True,
                    "placeholder": "Enter equipment serial number"
                },
                {
                    "type": "rating",
                    "headline": "Overall Equipment Condition",
                    "required": True,
                    "scale": "star",
                    "range": 5
                },
                {
                    "type": "multipleChoiceSingle",
                    "headline": "Issues Observed",
                    "choices": [
                        {"label": "No issues"},
                        {"label": "Minor wear"},
                        {"label": "Needs maintenance"},
                        {"label": "Critical issue"},
                        {"label": "Safety concern"}
                    ]
                },
                {
                    "type": "openText",
                    "headline": "Additional Notes",
                    "required": False,
                    "placeholder": "Describe any observations or recommendations"
                }
            ]
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/api/v1/surveys",
                headers=self.headers,
                json=survey_data,
                timeout=10
            )
            return response.json() if response.status_code == 201 else {"error": response.text}
        except Exception as e:
            return {"error": str(e)}
    
    # === RESPONSE MANAGEMENT ===
    
    def get_survey_responses(self, survey_id, limit=50):
        """Get responses for a specific survey"""
        try:
            response = requests.get(
                f"{self.base_url}/api/v1/surveys/{survey_id}/responses",
                headers=self.headers,
                params={"limit": limit},
                timeout=10
            )
            return response.json() if response.status_code == 200 else {"error": response.text}
        except Exception as e:
            return {"error": str(e)}
    
    def get_all_responses(self, limit=100):
        """Get all responses across surveys"""
        try:
            response = requests.get(
                f"{self.base_url}/api/v1/responses",
                headers=self.headers,
                params={"limit": limit},
                timeout=10
            )
            return response.json() if response.status_code == 200 else {"error": response.text}
        except Exception as e:
            return {"error": str(e)}
    
    # === ANALYTICS & REPORTING ===
    
    def analyze_equipment_health(self, equipment_type=None):
        """Analyze equipment health trends from form responses"""
        all_responses = self.get_all_responses()
        
        if "error" in all_responses:
            return all_responses
        
        analysis = {
            "total_inspections": 0,
            "equipment_health": {},
            "critical_issues": [],
            "maintenance_needed": [],
            "last_inspection": None
        }
        
        for response in all_responses.get("data", []):
            analysis["total_inspections"] += 1
            
            # Parse response data for health metrics
            data = response.get("data", {})
            for question, answer in data.items():
                if "condition" in question.lower():
                    # Health rating analysis
                    rating = answer.get("value", 0)
                    equipment = data.get("equipment_id", "unknown")
                    
                    if equipment not in analysis["equipment_health"]:
                        analysis["equipment_health"][equipment] = []
                    analysis["equipment_health"][equipment].append(rating)
                
                if "issues" in question.lower():
                    issue_type = answer.get("value", "")
                    if "critical" in issue_type.lower():
                        analysis["critical_issues"].append({
                            "equipment": data.get("equipment_id", "unknown"),
                            "issue": issue_type,
                            "timestamp": response.get("createdAt")
                        })
                    elif "maintenance" in issue_type.lower():
                        analysis["maintenance_needed"].append({
                            "equipment": data.get("equipment_id", "unknown"),
                            "timestamp": response.get("createdAt")
                        })
        
        return analysis
    
    # === WEBHOOK PROCESSING ===
    
    def process_webhook_data(self, webhook_payload):
        """Process incoming webhook data from n8n"""
        try:
            # Extract form response data
            response_data = webhook_payload.get("data", {})
            equipment_id = response_data.get("equipment_id", "unknown")
            health_rating = response_data.get("condition_rating", 0)
            issues = response_data.get("issues", "none")
            
            # Real-time alert logic
            alerts = []
            if health_rating <= 2:
                alerts.append({
                    "type": "critical",
                    "equipment": equipment_id,
                    "message": f"Low health rating: {health_rating}/5"
                })
            
            if "critical" in issues.lower() or "safety" in issues.lower():
                alerts.append({
                    "type": "urgent",
                    "equipment": equipment_id,
                    "message": f"Critical issue reported: {issues}"
                })
            
            # Log to Google Sheets
            if self.sheet_client:
                self._log_to_sheets(response_data, alerts)
            
            return {
                "processed": True,
                "alerts": alerts,
                "equipment": equipment_id
            }
            
        except Exception as e:
            return {"error": str(e)}
    
    def _log_to_sheets(self, response_data, alerts):
        """Log form response and alerts to Google Sheets"""
        try:
            # Log to Form Submissions sheet
            form_sheet = self.sheet_client.worksheet('Form Submissions')
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            form_sheet.append_row([
                timestamp,
                response_data.get("equipment_id", ""),
                response_data.get("condition_rating", ""),
                response_data.get("issues", ""),
                response_data.get("notes", ""),
                "Formbricks API"
            ])
            
            # Log critical alerts to Equipment Alerts sheet
            if alerts:
                alert_sheet = self.sheet_client.worksheet('Equipment Alerts')
                for alert in alerts:
                    alert_sheet.append_row([
                        timestamp,
                        alert["equipment"],
                        alert["type"],
                        alert["message"],
                        "Formbricks API",
                        "PENDING"
                    ])
                    
        except Exception as e:
            print(f"❌ Sheets logging error: {e}")
    
    # === INTEGRATION TESTING ===
    
    def test_integration(self):
        """Test Formbricks API integration"""
        print("🧪 Testing Formbricks API Integration - CT-018")
        print("=" * 50)
        
        # Test API connection
        print("\n1️⃣  Testing API Connection...")
        surveys = self.get_surveys()
        if "error" not in surveys:
            survey_count = len(surveys.get("data", []))
            print(f"   ✅ Connected! Found {survey_count} surveys")
        else:
            print(f"   ❌ API Error: {surveys['error']}")
        
        # Test webhook processing
        print("\n2️⃣  Testing Webhook Processing...")
        sample_webhook = {
            "data": {
                "equipment_id": "AC-001",
                "condition_rating": 2,
                "issues": "Critical pressure issue",
                "notes": "Immediate attention required"
            }
        }
        
        result = self.process_webhook_data(sample_webhook)
        if "error" not in result:
            alert_count = len(result["alerts"])
            print(f"   ✅ Webhook processed! Generated {alert_count} alerts")
        else:
            print(f"   ❌ Webhook Error: {result['error']}")
        
        # Test analytics
        print("\n3️⃣  Testing Analytics...")
        analysis = self.analyze_equipment_health()
        if "error" not in analysis:
            inspection_count = analysis["total_inspections"]
            print(f"   ✅ Analytics working! {inspection_count} inspections analyzed")
        else:
            print(f"   ❌ Analytics Error: {analysis['error']}")
        
        print("\n" + "=" * 50)
        print("🎯 Formbricks API integration test complete!")

# === BREWERY DEMO FUNCTIONS ===

def create_steel_bonnet_surveys():
    """Create brewery-specific surveys for Steel Bonnet demo"""
    client = FormbricksAPIClient()
    
    equipment_types = [
        ("Air Compressor", "Utilities"),
        ("Glycol Chiller", "Cellar"),
        ("Walk-in Chiller", "Storage"),
        ("Boiler", "Utilities")
    ]
    
    created_surveys = []
    for equipment, location in equipment_types:
        result = client.create_equipment_survey(equipment, location)
        if "error" not in result:
            created_surveys.append(result)
            print(f"✅ Created survey: {equipment} - {location}")
        else:
            print(f"❌ Failed to create {equipment} survey: {result['error']}")
    
    return created_surveys

def main():
    """Demo the Formbricks API integration"""
    client = FormbricksAPIClient()
    client.test_integration()
    
    print("\n🏭 Creating Steel Bonnet brewery surveys...")
    create_steel_bonnet_surveys()

if __name__ == "__main__":
    main()