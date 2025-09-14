











import os
import subprocess
from typing import Dict, Any, List
from .base_role import BaseRole

class GitIntegrator(BaseRole):
    """Git Integrator role - handles Git operations and CI/CD integration"""

    def __init__(self):
        super().__init__(
            name="GitIntegrator",
            description="Handles Git operations and CI/CD integration",
            tools=["git_operations", "ci_cd_integration", "version_control"]
        )

    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle Git operations and CI/CD integration"""
        # Get project information from context
        project_name = context.get("project_name", "project")
        project_structure = context.get("project_structure", {})
        code_implementation = context.get("code_implementation", {})

        # Initialize Git repository
        git_status = await self._initialize_git_repo(project_name)

        # Create .gitignore file
        gitignore_created = await self._create_gitignore()

        # Create README file
        readme_created = await self._create_readme(project_name, project_structure)

        # Create CI/CD pipeline
        ci_cd_pipeline = await self._create_ci_cd_pipeline()

        # Commit initial files
        commit_result = await self._commit_initial_files()

        return {
            "git_status": git_status,
            "gitignore_created": gitignore_created,
            "readme_created": readme_created,
            "ci_cd_pipeline": ci_cd_pipeline,
            "commit_result": commit_result,
            "next_role": None  # Final role in workflow
        }

    async def _initialize_git_repo(self, project_name: str) -> Dict[str, Any]:
        """Initialize Git repository"""
        try:
            # Initialize Git repo
            subprocess.run(["git", "init"], check=True, capture_output=True)

            # Set Git config
            subprocess.run(["git", "config", "user.name", "MultiAgentCoder"], check=True)
            subprocess.run(["git", "config", "user.email", "coder@multiagent.com"], check=True)

            return {
                "status": "success",
                "message": "Git repository initialized successfully",
                "repo_name": project_name
            }
        except subprocess.CalledProcessError as e:
            return {
                "status": "error",
                "message": f"Failed to initialize Git repository: {e.stderr.decode()}"
            }

    async def _create_gitignore(self) -> Dict[str, Any]:
        """Create .gitignore file"""
        gitignore_content = """
# Python
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
ENV/
env.bak/
venv.bak/
*.swp
*.swo

# Node
node_modules/
dist/
build/

# Logs
logs/
*.log

# OS
.DS_Store
Thumbs.db

# IDEs
.idea/
.vscode/
*.iml
"""

        try:
            with open(".gitignore", 'w') as f:
                f.write(gitignore_content)

            return {
                "status": "success",
                "message": ".gitignore file created successfully"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to create .gitignore file: {str(e)}"
            }

    async def _create_readme(self, project_name: str, project_structure: Dict[str, Any]) -> Dict[str, Any]:
        """Create README file"""
        readme_content = f"""
# {project_name}

## Project Description

This project is a comprehensive web application with frontend, backend, and database components.

## Project Structure

```

        # Add project structure
        for directory, files in project_structure.items():
            readme_content += f"{directory}/\n"
            for file in files:
                readme_content += f"  - {file}\n"

        readme_content += """
```

## Getting Started

1. Install dependencies: `pip install -r requirements.txt`
2. Set up database: `alembic upgrade head`
3. Run development server: `uvicorn main:app --reload`

## Development

- Follow PEP 8 for Python code
- Write comprehensive docstrings
- Use meaningful variable names

## Testing

- Run unit tests: `pytest tests/unit/`
- Run integration tests: `pytest tests/integration/`
- Run E2E tests: `cypress run`

## Deployment

- Build Docker image: `docker build -t {project_name.lower().replace(' ', '-')} .`
- Deploy to Kubernetes: `kubectl apply -f k8s/`
"""

        try:
            with open("README.md", 'w') as f:
                f.write(readme_content)

            return {
                "status": "success",
                "message": "README.md file created successfully"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to create README.md file: {str(e)}"
            }

    async def _create_ci_cd_pipeline(self) -> Dict[str, Any]:
        """Create CI/CD pipeline configuration"""
        ci_cd_content = """
name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v2

    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt

    - name: Run tests
      run: |
        pytest tests/unit/
        pytest tests/integration/

    - name: Build Docker image
      run: |
        docker build -t project-name .

    - name: Deploy to staging
      if: github.ref == 'refs/heads/develop'
      run: |
        # Add deployment commands here
        echo "Deploying to staging environment"

    - name: Deploy to production
      if: github.ref == 'refs/heads/main'
      run: |
        # Add deployment commands here
        echo "Deploying to production environment"
"""

        try:
            os.makedirs(".github/workflows", exist_ok=True)
            with open(".github/workflows/ci_cd.yml", 'w') as f:
                f.write(ci_cd_content)

            return {
                "status": "success",
                "message": "CI/CD pipeline configuration created successfully"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to create CI/CD pipeline configuration: {str(e)}"
            }

    async def _commit_initial_files(self) -> Dict[str, Any]:
        """Commit initial files to Git"""
        try:
            # Add all files
            subprocess.run(["git", "add", "."], check=True)

            # Commit files
            subprocess.run(["git", "commit", "-m", "Initial commit - project setup"], check=True)

            return {
                "status": "success",
                "message": "Initial files committed successfully"
            }
        except subprocess.CalledProcessError as e:
            return {
                "status": "error",
                "message": f"Failed to commit initial files: {e.stderr.decode()}"
            }






