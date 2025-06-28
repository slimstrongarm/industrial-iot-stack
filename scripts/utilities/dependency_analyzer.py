#!/usr/bin/env python3
"""
Smart Dependency Analyzer for Industrial IoT Tasks
Automatically suggests and sets dependencies based on task content and logical flow
"""

import re
from typing import List, Dict, Set

class DependencyAnalyzer:
    def __init__(self):
        # Define dependency patterns and rules
        self.dependency_rules = {
            # Infrastructure must come first
            'infrastructure': {
                'keywords': ['docker network', 'create network', 'setup infrastructure', 'install docker'],
                'priority': 1,
                'dependencies': []
            },
            
            # Base Docker setup
            'docker_compose': {
                'keywords': ['docker compose', 'docker-compose', 'compose file'],
                'priority': 2,
                'dependencies': ['infrastructure']
            },
            
            # Service-specific compose files
            'service_compose': {
                'keywords': ['compose for', 'docker compose for node-red', 'docker compose for ignition', 'docker compose for mqtt'],
                'priority': 3,
                'dependencies': ['docker_compose']
            },
            
            # Container deployment
            'deployment': {
                'keywords': ['deploy', 'start container', 'run container'],
                'priority': 4,
                'dependencies': ['service_compose']
            },
            
            # Configuration and setup
            'configuration': {
                'keywords': ['configure', 'setup', 'install module'],
                'priority': 5,
                'dependencies': ['deployment']
            },
            
            # Research tasks (can run early/parallel)
            'research': {
                'keywords': ['research', 'investigate', 'analyze'],
                'priority': 1,
                'dependencies': []
            },
            
            # Documentation (can run parallel)
            'documentation': {
                'keywords': ['document', 'create guide', 'write docs'],
                'priority': 1,
                'dependencies': []
            },
            
            # Testing (needs things to be built first)
            'testing': {
                'keywords': ['test', 'verify', 'validate'],
                'priority': 6,
                'dependencies': ['configuration']
            },
            
            # Export/migration tasks
            'export': {
                'keywords': ['export', 'migrate', 'transfer'],
                'priority': 2,
                'dependencies': []
            },
            
            # Import tasks (need exports first)
            'import': {
                'keywords': ['import', 'restore', 'load'],
                'priority': 7,
                'dependencies': ['export', 'deployment']
            }
        }
        
        # Service-specific dependencies
        self.service_dependencies = {
            'ignition': {
                'requires': ['docker_network'],
                'enables': ['flint_integration', 'project_import']
            },
            'node-red': {
                'requires': ['mqtt_broker'],
                'enables': ['flow_deployment']
            },
            'mqtt': {
                'requires': ['docker_network'],
                'enables': ['node-red', 'ignition_mqtt']
            },
            'flint': {
                'requires': ['ignition'],
                'enables': ['vscode_integration']
            }
        }
    
    def analyze_task(self, task_description: str, existing_tasks: List[Dict]) -> Dict:
        """Analyze a task and suggest dependencies"""
        description_lower = task_description.lower()
        
        # Categorize the task
        task_category = self.categorize_task(description_lower)
        
        # Find service being worked on
        service = self.identify_service(description_lower)
        
        # Get suggested dependencies
        suggested_deps = self.suggest_dependencies(
            task_category, service, description_lower, existing_tasks
        )
        
        return {
            'category': task_category,
            'service': service,
            'suggested_dependencies': suggested_deps,
            'reasoning': self.explain_dependencies(task_category, service, suggested_deps)
        }
    
    def categorize_task(self, description: str) -> str:
        """Categorize task based on keywords"""
        for category, rules in self.dependency_rules.items():
            for keyword in rules['keywords']:
                if keyword in description:
                    return category
        return 'general'
    
    def identify_service(self, description: str) -> str:
        """Identify which service the task is about"""
        services = ['ignition', 'node-red', 'mqtt', 'flint', 'docker', 'grafana', 'portainer']
        for service in services:
            if service in description or service.replace('-', '') in description:
                return service
        return 'general'
    
    def suggest_dependencies(self, category: str, service: str, description: str, existing_tasks: List[Dict]) -> List[str]:
        """Suggest specific task dependencies based on analysis"""
        suggested = []
        
        # Build map of existing tasks
        task_map = {}
        for task in existing_tasks:
            task_id = task.get('Task ID', '')
            task_desc = task.get('Task Description', '').lower()
            task_map[task_id] = {
                'description': task_desc,
                'status': task.get('Status', ''),
                'category': self.categorize_task(task_desc),
                'service': self.identify_service(task_desc)
            }
        
        # Apply category-based rules
        if category in self.dependency_rules:
            rule_deps = self.dependency_rules[category]['dependencies']
            for dep_category in rule_deps:
                # Find tasks in that category
                for task_id, task_info in task_map.items():
                    if task_info['category'] == dep_category:
                        suggested.append(task_id)
        
        # Apply service-specific rules
        if service in self.service_dependencies:
            service_reqs = self.service_dependencies[service]['requires']
            for req_service in service_reqs:
                # Find tasks that set up required services
                for task_id, task_info in task_map.items():
                    if req_service.replace('_', '-') in task_info['description']:
                        suggested.append(task_id)
        
        # Special case logic
        if 'compose for' in description:
            # Docker Compose for specific service needs base compose
            for task_id, task_info in task_map.items():
                if ('docker compose' in task_info['description'] and 
                    'for' not in task_info['description']):  # Base compose file
                    suggested.append(task_id)
        
        if 'deploy' in description and service != 'general':
            # Deployment needs compose file for that service
            for task_id, task_info in task_map.items():
                if (f'compose for {service}' in task_info['description'] or
                    f'docker compose for {service}' in task_info['description']):
                    suggested.append(task_id)
        
        # Remove duplicates and self-references
        suggested = list(set(suggested))
        
        return suggested
    
    def explain_dependencies(self, category: str, service: str, dependencies: List[str]) -> str:
        """Explain why these dependencies were suggested"""
        if not dependencies:
            return "No dependencies needed - this task can run independently"
        
        explanations = []
        
        if category == 'service_compose':
            explanations.append("Service-specific Docker Compose files need base Docker setup")
        elif category == 'deployment':
            explanations.append("Container deployment requires compose files to be ready")
        elif category == 'configuration':
            explanations.append("Configuration tasks need services to be deployed first")
        elif category == 'testing':
            explanations.append("Testing requires system components to be configured")
        elif category == 'import':
            explanations.append("Import tasks need export tasks and deployment infrastructure")
        
        if service != 'general':
            explanations.append(f"Tasks for {service} may depend on infrastructure setup")
        
        return "; ".join(explanations) if explanations else "Based on task analysis and logical ordering"

def analyze_new_task(task_description: str, existing_tasks: List[Dict]) -> Dict:
    """Convenience function to analyze a new task"""
    analyzer = DependencyAnalyzer()
    return analyzer.analyze_task(task_description, existing_tasks)

# Test function
if __name__ == "__main__":
    # Example existing tasks
    existing_tasks = [
        {"Task ID": "DM-001", "Task Description": "Create Docker Compose for Ignition", "Status": "In Progress"},
        {"Task ID": "DM-002", "Task Description": "Research Flint Docker integration", "Status": "Complete"},
        {"Task ID": "DM-003", "Task Description": "Design modular stack architecture", "Status": "In Progress"},
        {"Task ID": "DM-004", "Task Description": "Setup Tailscale SSH connection to server", "Status": "Pending"},
        {"Task ID": "DM-005", "Task Description": "Create Ignition project export script", "Status": "Complete"}
    ]
    
    # Test new task
    new_task = "Create Docker Compose for Node-RED"
    analysis = analyze_new_task(new_task, existing_tasks)
    
    print(f"Task: {new_task}")
    print(f"Category: {analysis['category']}")
    print(f"Service: {analysis['service']}")
    print(f"Suggested Dependencies: {analysis['suggested_dependencies']}")
    print(f"Reasoning: {analysis['reasoning']}")