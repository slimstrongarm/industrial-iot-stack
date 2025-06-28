#!/usr/bin/env python3
"""Enhance Server Claude agent task descriptions with detailed context and specifications"""

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

def enhance_agent_descriptions(service):
    """Update Server Claude agent tasks with detailed descriptions"""
    
    # Enhanced task definitions with full context
    enhanced_tasks = [
        [
            "CT-076",
            "Server Claude", 
            "ADK Agent - Docker Orchestrator",
            "High",
            "Not Started",
            "Create Docker Management Agent: Specialized ADK-powered agent for container lifecycle management. Must integrate with existing ADK framework, use state persistence for container states, and coordinate with other agents via Discord. Handle docker-compose operations, health monitoring, auto-restart policies, and resource allocation. Reference .claude/adk_enhanced/ patterns.",
            "Fully functional DockerOrchestrator agent in .claude/adk_enhanced/docker_orchestrator.py that: 1) Monitors all containers in real-time, 2) Auto-recovers failed services, 3) Sends Discord alerts for critical events, 4) Maintains persistent state of container health history, 5) Integrates with TaskCoordinationEngine for workload distribution"
        ],
        [
            "CT-077",
            "Server Claude",
            "ADK Agent - SystemD Guardian", 
            "High",
            "Not Started",
            "Create SystemD Service Agent: Build ADK-compliant agent for Linux service management. Must handle systemctl operations, journal log analysis, service dependency mapping, and failure recovery. Integrate with ConflictPreventionEngine to avoid service restart conflicts. Support both user and system services, timer units, and socket activation.",
            "Complete SystemDGuardian agent with: 1) Service state monitoring and control, 2) Automatic failure recovery with exponential backoff, 3) Journal log integration for error detection, 4) Service dependency visualization, 5) Discord notifications for service failures, 6) Integration with backup agent for state snapshots before major operations"
        ],
        [
            "CT-078",
            "Server Claude",
            "ADK Agent - Log Intelligence",
            "Medium", 
            "Not Started",
            "Create Log Analysis Agent: Implement intelligent log monitoring using ADK patterns. Parse multiple log formats (syslog, JSON, custom), detect anomalies using pattern matching, correlate events across services, and generate actionable insights. Must handle log rotation, compression, and archival. Integrate with Discord for critical alerts.",
            "LogIntelligence agent featuring: 1) Real-time log streaming from multiple sources, 2) Pattern-based anomaly detection with ML-ready hooks, 3) Event correlation engine for root cause analysis, 4) Automated log archival and rotation management, 5) Performance metrics extraction from logs, 6) Integration with other agents for contextual analysis"
        ],
        [
            "CT-079",
            "Server Claude",
            "ADK Agent - Resilience Manager",
            "Medium",
            "Not Started", 
            "Create Backup & Recovery Agent: Design comprehensive disaster recovery system using ADK architecture. Handle automated backups of configs, databases, and state files. Implement 3-2-1 backup strategy, test restore procedures, maintain backup catalog, and coordinate with other agents for pre-backup service preparation. Support incremental and full backups.",
            "ResilienceManager agent providing: 1) Automated daily backups with versioning, 2) Pre-backup coordination with Docker and SystemD agents, 3) Backup integrity verification and test restores, 4) Disaster recovery runbooks with one-click restore, 5) Backup metrics and storage optimization, 6) Discord alerts for backup failures or storage issues"
        ],
        [
            "CT-080",
            "Server Claude",
            "ADK Agent - Performance Oracle",
            "Medium",
            "Not Started",
            "Create Performance Monitoring Agent: Build comprehensive resource monitoring using ADK framework. Track CPU, memory, disk, network metrics. Identify bottlenecks, predict resource exhaustion, suggest optimizations. Must integrate with Docker agent for container metrics, SystemD agent for service performance, and maintain historical baselines for anomaly detection.", 
            "PerformanceOracle agent delivering: 1) Real-time system metrics with 1-minute granularity, 2) Container-specific resource tracking via Docker integration, 3) Predictive alerts for resource exhaustion (disk, memory), 4) Performance optimization recommendations based on usage patterns, 5) Historical trend analysis with 30-day retention, 6) Automated report generation for capacity planning"
        ]
    ]
    
    # Update the rows
    body = {
        'values': enhanced_tasks
    }
    
    result = service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID,
        range="Claude Tasks!A76:G80",
        valueInputOption="RAW",
        body=body
    ).execute()
    
    print("Enhanced Server Claude agent task descriptions!")
    print("\nKey improvements:")
    print("- Task Type: Now specifies ADK Agent type with descriptive names")
    print("- Description: Includes implementation requirements, ADK integration needs, and technical specifications")
    print("- Expected Output: Detailed deliverables with numbered feature requirements")
    print("\nServer Claude now has comprehensive implementation guides for each specialized agent!")
    
    return result

def main():
    """Main execution"""
    print("Enhancing Server Claude agent task descriptions...\n")
    
    service = get_sheets_service()
    enhance_agent_descriptions(service)
    
    print("\n✅ Completed! Server Claude's agent tasks now have detailed implementation context.")

if __name__ == "__main__":
    main()