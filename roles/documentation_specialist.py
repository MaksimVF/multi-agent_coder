








import os
from typing import Dict, Any, List
from .base_role import BaseRole

class DocumentationSpecialist(BaseRole):
    """Documentation Specialist role - generates comprehensive project documentation"""

    def __init__(self):
        super().__init__(
            name="DocumentationSpecialist",
            description="Generates comprehensive project documentation and reports",
            tools=["document_generation", "markdown_formatting", "diagram_generation"]
        )

    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive project documentation"""
        # Get project information from context
        requirements = context.get("requirements", "")
        architecture = context.get("system_architecture", {})
        tech_stack = context.get("tech_stack", {})
        project_structure = context.get("project_structure", {})
        code_review = context.get("code_review", {})
        test_results = context.get("test_results", {})

        # Generate technical specification
        tech_spec = await self._generate_technical_specification(requirements, architecture, tech_stack)

        # Generate development guide
        dev_guide = await self._generate_development_guide(architecture, project_structure, tech_stack)

        # Generate API documentation
        api_docs = await self._generate_api_documentation(architecture)

        # Generate project report
        project_report = await self._generate_project_report(architecture, code_review, test_results)

        # Create documentation files
        doc_files = await self._create_documentation_files(tech_spec, dev_guide, api_docs, project_report)

        return {
            "technical_specification": tech_spec,
            "development_guide": dev_guide,
            "api_documentation": api_docs,
            "project_report": project_report,
            "documentation_files": doc_files,
            "next_role": None  # Final role in workflow
        }

    async def _generate_technical_specification(self, requirements: str, architecture: Dict[str, Any], tech_stack: Dict[str, Any]) -> str:
        """Generate technical specification document"""
        doc = """
# Technical Specification

## Table of Contents
1. [Introduction](#introduction)
2. [System Overview](#system-overview)
3. [Architecture](#architecture)
4. [Technology Stack](#technology-stack)
5. [Components](#components)
6. [Data Flow](#data-flow)
7. [Security](#security)
8. [Scalability](#scalability)

## Introduction

This document provides a comprehensive technical specification for the project.

## System Overview

The system is designed to meet the following requirements:
"""

        # Add requirements
        doc += f"{requirements}\n\n"

        # Add architecture overview
        doc += "## Architecture\n"
        doc += f"The system follows a {architecture.get('patterns', {}).get('architecture', ['modular'])[0]} architecture.\n\n"

        # Add technology stack
        doc += "## Technology Stack\n"
        for category, items in tech_stack.items():
            doc += f"### {category.capitalize()}\n"
            for item, value in items.items():
                doc += f"- **{item.capitalize()}**: {value}\n"

        # Add components
        doc += "\n## Components\n"
        for component_name, component in architecture.get("components", {}).items():
            doc += f"### {component_name.capitalize()}\n"
            doc += f"- **Responsibilities**: {', '.join(component['responsibilities'])}\n"
            doc += f"- **Technologies**: {', '.join([f'{k}: {v}' for k, v in component['technologies'].items()])}\n"

        # Add data flow
        doc += "\n## Data Flow\n"
        for flow_name, flow_desc in architecture.get("data_flow", {}).items():
            doc += f"- **{flow_name.replace('_', ' ').title()}**: {flow_desc}\n"

        # Add security
        doc += "\n## Security\n"
        security = tech_stack.get("security", {})
        for measure, value in security.items():
            doc += f"- **{measure.capitalize()}**: {value}\n"

        # Add scalability
        doc += "\n## Scalability\n"
        for scale_type, strategies in architecture.get("scalability", {}).items():
            doc += f"### {scale_type.capitalize()} Scaling\n"
            for strategy in strategies:
                doc += f"- {strategy}\n"

        return doc

    async def _generate_development_guide(self, architecture: Dict[str, Any], project_structure: Dict[str, Any], tech_stack: Dict[str, Any]) -> str:
        """Generate development guide"""
        doc = """
# Development Guide

## Table of Contents
1. [Getting Started](#getting-started)
2. [Project Structure](#project-structure)
3. [Development Setup](#development-setup)
4. [Coding Standards](#coding-standards)
5. [Testing](#testing)
6. [Deployment](#deployment)

## Getting Started

Welcome to the development guide for this project.

## Project Structure

The project has the following structure:
"""

        # Add project structure
        for directory, files in project_structure.items():
            doc += f"\n### {directory.capitalize()}\n"
            doc += f"- Files: {', '.join(files)}\n"

        # Add development setup
        doc += "\n## Development Setup\n"
        doc += "1. Install dependencies: `pip install -r requirements.txt`\n"
        doc += "2. Set up database: `alembic upgrade head`\n"
        doc += "3. Run development server: `uvicorn main:app --reload`\n"

        # Add coding standards
        doc += "\n## Coding Standards\n"
        doc += "- Follow PEP 8 for Python code\n"
        doc += "- Use TypeScript for frontend code\n"
        doc += "- Write comprehensive docstrings\n"
        doc += "- Use meaningful variable names\n"

        # Add testing
        doc += "\n## Testing\n"
        doc += "- Run unit tests: `pytest tests/unit/`\n"
        doc += "- Run integration tests: `pytest tests/integration/`\n"
        doc += "- Run E2E tests: `cypress run`\n"

        # Add deployment
        doc += "\n## Deployment\n"
        doc += "- Build Docker image: `docker build -t project-name .`\n"
        doc += "- Deploy to Kubernetes: `kubectl apply -f k8s/`\n"

        return doc

    async def _generate_api_documentation(self, architecture: Dict[str, Any]) -> str:
        """Generate API documentation"""
        doc = """
# API Documentation

## Table of Contents
1. [Authentication](#authentication)
2. [Endpoints](#endpoints)
3. [Request/Response Format](#requestresponse-format)
4. [Error Handling](#error-handling)

## Authentication

The API uses JWT for authentication. Include the token in the Authorization header:
```
Authorization: Bearer <token>
```

## Endpoints

### Authentication
- **POST /api/auth/login** - User login
- **POST /api/auth/register** - User registration
- **POST /api/auth/refresh** - Refresh token

### Users
- **GET /api/users** - Get user list
- **GET /api/users/{id}** - Get user details
- **POST /api/users** - Create user
- **PUT /api/users/{id}** - Update user
- **DELETE /api/users/{id}** - Delete user

## Request/Response Format

All requests and responses use JSON format.

### Example Request
```json
{
    "username": "testuser",
    "password": "securepassword"
}
```

### Example Response
```json
{
    "id": 1,
    "username": "testuser",
    "token": "jwt.token.here"
}
```

## Error Handling

Errors are returned with appropriate HTTP status codes and JSON body:
```json
{
    "error": "error_code",
    "message": "Error description"
}
```
"""

        return doc

    async def _generate_project_report(self, architecture: Dict[str, Any], code_review: Dict[str, Any], test_results: Dict[str, Any]) -> str:
        """Generate project report"""
        doc = """
# Project Report

## Table of Contents
1. [Project Overview](#project-overview)
2. [Architecture Summary](#architecture-summary)
3. [Code Quality](#code-quality)
4. [Test Results](#test-results)
5. [Recommendations](#recommendations)

## Project Overview

This report provides an overview of the project status, code quality, and test results.

## Architecture Summary

The project follows a comprehensive architecture with the following components:
"""

        # Add architecture summary
        for component_name in architecture.get("components", {}).keys():
            doc += f"- {component_name.capitalize()}\n"

        # Add code quality
        doc += "\n## Code Quality\n"
        doc += f"- Quality score: {code_review.get('quality_score', 0):.1f}/10\n"
        doc += f"- Issues found: {code_review.get('issues_found', 0)}\n"
        doc += f"- Files reviewed: {len(code_review.get('files_reviewed', []))}\n"

        # Add test results
        doc += "\n## Test Results\n"
        doc += f"- Total tests: {test_results.get('total_tests', 0)}\n"
        doc += f"- Passed: {test_results.get('passed', 0)}\n"
        doc += f"- Failed: {test_results.get('failed', 0)}\n"
        doc += f"- Coverage: {test_results.get('coverage', 0)}%\n"

        # Add recommendations
        doc += "\n## Recommendations\n"
        doc += "- Address all code review issues\n"
        doc += "- Improve test coverage to > 90%\n"
        doc += "- Optimize performance bottlenecks\n"

        return doc

    async def _create_documentation_files(self, tech_spec: str, dev_guide: str, api_docs: str, project_report: str) -> Dict[str, str]:
        """Create documentation files"""
        docs_dir = "docs"
        os.makedirs(docs_dir, exist_ok=True)

        # Create technical specification
        with open(f"{docs_dir}/TECHNICAL_SPEC.md", 'w') as f:
            f.write(tech_spec)

        # Create development guide
        with open(f"{docs_dir}/DEVELOPMENT_GUIDE.md", 'w') as f:
            f.write(dev_guide)

        # Create API documentation
        with open(f"{docs_dir}/API_DOCS.md", 'w') as f:
            f.write(api_docs)

        # Create project report
        with open(f"{docs_dir}/PROJECT_REPORT.md", 'w') as f:
            f.write(project_report)

        return {
            "technical_specification": f"{docs_dir}/TECHNICAL_SPEC.md",
            "development_guide": f"{docs_dir}/DEVELOPMENT_GUIDE.md",
            "api_documentation": f"{docs_dir}/API_DOCS.md",
            "project_report": f"{docs_dir}/PROJECT_REPORT.md"
        }





