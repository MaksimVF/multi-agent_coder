




import os
from typing import Dict, Any, List
from .base_role import BaseRole

class Architect(BaseRole):
    """Architect role - responsible for comprehensive system design and project architecture"""

    def __init__(self):
        super().__init__(
            name="Architect",
            description="Designs comprehensive system architecture and creates project skeleton",
            tools=["system_design", "tech_stack_selection", "architecture_diagrams", "document_generation", "file_management"]
        )

    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Design comprehensive system architecture and create project skeleton"""
        # Get PRD and requirements from context
        prd = context.get("prd", "")
        requirements = context.get("requirements", "")

        # Select technology stack
        tech_stack = await self._select_tech_stack(requirements)

        # Design comprehensive architecture
        architecture = await self._design_architecture(prd, tech_stack)

        # Create project skeleton
        project_structure = await self._create_project_skeleton(architecture)

        # Generate architecture documentation
        arch_doc = await self._generate_architecture_doc(architecture)

        # Generate component interaction diagram
        interaction_diagram = await self._generate_interaction_diagram(architecture)

        # Update context with results
        result = {
            "system_architecture": architecture,
            "project_structure": project_structure,
            "architecture_documentation": arch_doc,
            "interaction_diagram": interaction_diagram,
            "tech_stack": tech_stack,
            "next_role": "Engineer"
        }

        return result

    async def _select_tech_stack(self, requirements: str) -> Dict[str, Any]:
        """Select appropriate technology stack based on requirements"""
        # This would use LLM to analyze requirements and select tech stack
        # For now, return a comprehensive tech stack
        return {
            "backend": {
                "language": "Python",
                "framework": "FastAPI",
                "database": "PostgreSQL",
                "orm": "SQLAlchemy",
                "auth": "JWT",
                "async": "asyncio"
            },
            "frontend": {
                "language": "JavaScript",
                "framework": "React",
                "state_management": "Redux",
                "styling": "Tailwind CSS",
                "build": "Vite"
            },
            "devops": {
                "containerization": "Docker",
                "orchestration": "Kubernetes",
                "ci_cd": "GitHub Actions",
                "monitoring": "Prometheus + Grafana",
                "logging": "ELK Stack"
            },
            "testing": {
                "unit": "pytest",
                "integration": "pytest + FastAPI test client",
                "e2e": "Cypress",
                "coverage": "coverage.py",
                "mocking": "unittest.mock"
            },
            "security": {
                "auth": "OAuth2 + JWT",
                "encryption": "AES-256",
                "vulnerability_scanning": "Bandit + Snyk",
                "secrets": "HashiCorp Vault"
            }
        }

    async def _design_architecture(self, prd: str, tech_stack: Dict[str, Any]) -> Dict[str, Any]:
        """Design comprehensive system architecture based on PRD and tech stack"""
        # This would use LLM to design comprehensive architecture
        # For now, return a detailed architecture
        return {
            "components": {
                "frontend": {
                    "files": ["App.jsx", "index.jsx", "components/", "pages/", "store/"],
                    "responsibilities": ["User interface", "State management", "API calls", "Routing"],
                    "technologies": tech_stack["frontend"],
                    "patterns": ["Component-based", "State management", "Hooks"]
                },
                "backend": {
                    "files": ["main.py", "api.py", "models.py", "services/", "repositories/"],
                    "responsibilities": ["Business logic", "API endpoints", "Database access", "Authentication"],
                    "technologies": tech_stack["backend"],
                    "patterns": ["MVC", "Service layer", "Repository", "Dependency injection"]
                },
                "database": {
                    "files": ["migrations/", "models.py", "seeds/"],
                    "responsibilities": ["Data storage", "Schema management", "Data seeding"],
                    "technologies": {"database": tech_stack["backend"]["database"], "orm": tech_stack["backend"]["orm"]},
                    "patterns": ["Active Record", "Data mapper"]
                },
                "auth": {
                    "files": ["auth.py", "middlewares.py"],
                    "responsibilities": ["User authentication", "Authorization", "Token management"],
                    "technologies": tech_stack["security"],
                    "patterns": ["JWT", "OAuth2"]
                }
            },
            "data_flow": {
                "frontend_to_backend": "REST API calls with JWT authentication",
                "backend_to_database": "ORM queries with connection pooling",
                "authentication": "OAuth2 + JWT tokens with refresh tokens",
                "real_time": "WebSocket for notifications",
                "caching": "Redis for frequently accessed data"
            },
            "patterns": {
                "architecture": ["Microservices", "Event-driven", "CQRS"],
                "frontend": ["Atomic design", "Feature-based structure"],
                "backend": ["Domain-driven design", "Hexagonal architecture"],
                "database": ["Database per service", "Event sourcing"]
            },
            "scalability": {
                "horizontal": ["Load balancers", "Auto-scaling", "Service discovery"],
                "vertical": ["Database optimization", "Query optimization", "Caching"],
                "data": ["Sharding", "Partitioning", "Read replicas"]
            },
            "resilience": {
                "fault_tolerance": ["Circuit breakers", "Retries", "Bulkheads"],
                "monitoring": ["Health checks", "Logging", "Tracing"],
                "recovery": ["Automatic failover", "Data backup", "Disaster recovery"]
            }
        }

    async def _create_project_skeleton(self, architecture: Dict[str, Any]) -> Dict[str, List[str]]:
        """Create comprehensive project skeleton based on architecture"""
        # Create enhanced file structure
        structure = {
            "root": ["README.md", "requirements.txt", "setup.py", "Dockerfile", "docker-compose.yml", ".github/workflows/"],
            "src": ["main.py", "config.py", "settings.py"],
            "frontend": ["index.jsx", "App.jsx", "components/", "pages/", "store/", "assets/"],
            "backend": ["api.py", "models.py", "services/", "repositories/", "auth/", "middlewares/"],
            "database": ["migrations/", "models.py", "seeds/"],
            "tests": ["unit/", "integration/", "e2e/", "conftest.py"],
            "docs": ["architecture.md", "api.md", "development.md"]
        }

        # Create directories and files
        for directory, files in structure.items():
            if directory != "root":
                os.makedirs(directory, exist_ok=True)
            for file in files:
                path = os.path.join(directory, file) if directory != "root" else file
                if not os.path.exists(path):
                    if file.endswith('/'):  # It's a directory
                        os.makedirs(path, exist_ok=True)
                    else:
                        with open(path, 'w') as f:
                            f.write(f"# {file}\n# Part of {directory}\n")

        return structure

    async def _generate_architecture_doc(self, architecture: Dict[str, Any]) -> str:
        """Generate comprehensive architecture documentation"""
        doc = """
# Comprehensive System Architecture Documentation

## Table of Contents
1. [Overview](#overview)
2. [Components](#components)
3. [Data Flow](#data-flow)
4. [Patterns](#patterns)
5. [Scalability](#scalability)
6. [Resilience](#resilience)
7. [Technology Stack](#technology-stack)

## Overview

This document provides a comprehensive overview of the system architecture, including all components, their interactions, technology choices, and design patterns.

## Components

"""

        # Components section
        for component_name, component in architecture["components"].items():
            doc += f"### {component_name.capitalize()}\n"
            doc += f"- **Files**: {', '.join(component['files'])}\n"
            doc += f"- **Responsibilities**: {', '.join(component['responsibilities'])}\n"
            doc += f"- **Technologies**: {', '.join([f'{k}: {v}' for k, v in component['technologies'].items()])}\n"
            doc += f"- **Patterns**: {', '.join(component['patterns'])}\n"
            doc += "\n"

        # Data flow section
        doc += "## Data Flow\n"
        for flow_name, flow_desc in architecture["data_flow"].items():
            doc += f"- **{flow_name.replace('_', ' ').title()}**: {flow_desc}\n"

        # Patterns section
        doc += "\n## Patterns\n"
        for pattern_type, patterns in architecture["patterns"].items():
            doc += f"### {pattern_type.capitalize()} Patterns\n"
            for pattern in patterns:
                doc += f"- {pattern}\n"

        # Scalability section
        doc += "\n## Scalability\n"
        for scale_type, strategies in architecture["scalability"].items():
            doc += f"### {scale_type.capitalize()} Scaling\n"
            for strategy in strategies:
                doc += f"- {strategy}\n"

        # Resilience section
        doc += "\n## Resilience\n"
        for resilience_type, strategies in architecture["resilience"].items():
            doc += f"### {resilience_type.replace('_', ' ').title()}\n"
            for strategy in strategies:
                doc += f"- {strategy}\n"

        # Technology stack section
        doc += "\n## Technology Stack\n"
        tech_stack = await self._select_tech_stack("")
        for category, items in tech_stack.items():
            doc += f"### {category.capitalize()}\n"
            for item, value in items.items():
                doc += f"- **{item.capitalize()}**: {value}\n"

        return doc

    async def _generate_interaction_diagram(self, architecture: Dict[str, Any]) -> str:
        """Generate component interaction diagram (text representation)"""
        diagram = """
# Component Interaction Diagram

```mermaid
graph TD
    A[Frontend] -->|REST API with JWT| B[Backend]
    B -->|ORM Queries| C[Database]
    A -->|WebSocket| B
    B -->|JWT Auth| A
    C -->|Data| B
    D[Auth Service] -->|OAuth2| B
    E[Cache] -->|Redis| B
    F[Message Queue] -->|Events| B
```

## Interaction Description

1. **Frontend to Backend**: User interactions trigger REST API calls with JWT authentication
2. **Backend to Database**: Business logic processes data and queries database via ORM
3. **Authentication**: OAuth2 + JWT tokens with refresh tokens for secure access
4. **Real-time**: WebSocket connection for real-time notifications
5. **Caching**: Redis caching for frequently accessed data
6. **Event-driven**: Message queue for asynchronous event processing
"""

        return diagram





