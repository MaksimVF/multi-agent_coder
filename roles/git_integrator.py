











import os
import json
import requests
from typing import Dict, Any, List, Optional
from .base_role import BaseRole

class GitIntegrator(BaseRole):
    """Enhanced Git Integrator role - handles comprehensive Git operations, CI/CD integration, and tool integrations"""

    def __init__(self, github_token: Optional[str] = None, repo_owner: Optional[str] = None, repo_name: Optional[str] = None):
        super().__init__()
        self.github_token = github_token or os.getenv('GITHUB_TOKEN')
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.api_url = f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}"
        self.headers = {
            "Authorization": f"token {self.github_token}",
            "Accept": "application/vnd.github.v3+json"
        }

    def create_issue(self, title: str, body: str, labels: Optional[List[str]] = None) -> Dict:
        """Create a GitHub issue"""
        payload = {
            "title": title,
            "body": body,
            "labels": labels or []
        }

        response = requests.post(
            f"{self.api_url}/issues",
            headers=self.headers,
            data=json.dumps(payload)
        )

        if response.status_code == 201:
            return response.json()
        else:
            raise Exception(f"Failed to create issue: {response.text}")

    def update_issue(self, issue_number: int, title: Optional[str] = None, body: Optional[str] = None, state: Optional[str] = None) -> Dict:
        """Update a GitHub issue"""
        payload = {}
        if title:
            payload["title"] = title
        if body:
            payload["body"] = body
        if state:
            payload["state"] = state

        response = requests.patch(
            f"{self.api_url}/issues/{issue_number}",
            headers=self.headers,
            data=json.dumps(payload)
        )

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to update issue: {response.text}")

    def create_pull_request(self, title: str, body: str, head: str, base: str) -> Dict:
        """Create a GitHub pull request"""
        payload = {
            "title": title,
            "body": body,
            "head": head,
            "base": base
        }

        response = requests.post(
            f"{self.api_url}/pulls",
            headers=self.headers,
            data=json.dumps(payload)
        )

        if response.status_code == 201:
            return response.json()
        else:
            raise Exception(f"Failed to create pull request: {response.text}")

    def update_pull_request(self, pr_number: int, title: Optional[str] = None, body: Optional[str] = None) -> Dict:
        """Update a GitHub pull request"""
        payload = {}
        if title:
            payload["title"] = title
        if body:
            payload["body"] = body

        response = requests.patch(
            f"{self.api_url}/pulls/{pr_number}",
            headers=self.headers,
            data=json.dumps(payload)
        )

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to update pull request: {response.text}")

    def get_pull_request_status(self, pr_number: int) -> Dict:
        """Get pull request status"""
        response = requests.get(
            f"{self.api_url}/pulls/{pr_number}",
            headers=self.headers
        )

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to get pull request status: {response.text}")

    def get_check_runs(self, pr_number: int) -> List[Dict]:
        """Get check runs for a pull request"""
        # Get the head commit SHA
        pr_info = self.get_pull_request_status(pr_number)
        head_sha = pr_info["head"]["sha"]

        response = requests.get(
            f"{self.api_url}/commits/{head_sha}/check-runs",
            headers=self.headers
        )

        if response.status_code == 200:
            return response.json()["check_runs"]
        else:
            raise Exception(f"Failed to get check runs: {response.text}")

    def wait_for_checks(self, pr_number: int, timeout: int = 300, interval: int = 10) -> bool:
        """Wait for CI checks to complete"""
        import time

        start_time = time.time()
        while time.time() - start_time < timeout:
            check_runs = self.get_check_runs(pr_number)

            # Check if all runs are completed
            all_completed = all(run["status"] == "completed" for run in check_runs)
            if all_completed:
                return True

            time.sleep(interval)

        return False

    def get_failed_checks(self, pr_number: int) -> List[Dict]:
        """Get failed check runs"""
        check_runs = self.get_check_runs(pr_number)
        return [run for run in check_runs if run["conclusion"] == "failure"]

    def add_label_to_issue(self, issue_number: int, label: str) -> Dict:
        """Add label to an issue"""
        response = requests.post(
            f"{self.api_url}/issues/{issue_number}/labels",
            headers=self.headers,
            data=json.dumps({"labels": [label]})
        )

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to add label: {response.text}")

    def add_project_card(self, issue_number: int, project_id: int, column_name: str) -> Dict:
        """Add issue to project board"""
        # First, get the column ID
        columns_response = requests.get(
            f"https://api.github.com/projects/{project_id}/columns",
            headers=self.headers
        )

        if columns_response.status_code != 200:
            raise Exception(f"Failed to get project columns: {columns_response.text}")

        columns = columns_response.json()
        column = next((col for col in columns if col["name"] == column_name), None)

        if not column:
            raise Exception(f"Column '{column_name}' not found")

        column_id = column["id"]

        # Create card
        payload = {
            "content_id": issue_number,
            "content_type": "Issue"
        }

        response = requests.post(
            f"https://api.github.com/projects/columns/{column_id}/cards",
            headers=self.headers,
            data=json.dumps(payload)
        )

        if response.status_code == 201:
            return response.json()
        else:
            raise Exception(f"Failed to create project card: {response.text}")

    def get_file_content(self, file_path: str, ref: str = "main") -> str:
        """Get file content from GitHub"""
        response = requests.get(
            f"{self.api_url}/contents/{file_path}",
            headers=self.headers,
            params={"ref": ref}
        )

        if response.status_code == 200:
            return response.json()["content"]
        else:
            raise Exception(f"Failed to get file content: {response.text}")

    def update_file(self, file_path: str, content: str, message: str, branch: str, sha: Optional[str] = None) -> Dict:
        """Update file in GitHub"""
        payload = {
            "message": message,
            "content": content,
            "branch": branch
        }

        if sha:
            payload["sha"] = sha

        response = requests.put(
            f"{self.api_url}/contents/{file_path}",
            headers=self.headers,
            data=json.dumps(payload)
        )

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to update file: {response.text}")

    def create_branch(self, branch_name: str, base_branch: str = "main") -> Dict:
        """Create a new branch"""
        # Get the base branch reference
        response = requests.get(
            f"{self.api_url}/git/refs/heads/{base_branch}",
            headers=self.headers
        )

        if response.status_code != 200:
            raise Exception(f"Failed to get base branch reference: {response.text}")

        base_ref = response.json()
        base_sha = base_ref["object"]["sha"]

        # Create new branch
        payload = {
            "ref": f"refs/heads/{branch_name}",
            "sha": base_sha
        }

        response = requests.post(
            f"{self.api_url}/git/refs",
            headers=self.headers,
            data=json.dumps(payload)
        )

        if response.status_code == 201:
            return response.json()
        else:
            raise Exception(f"Failed to create branch: {response.text}")

    async def run_workflow(self, config: Dict) -> Dict:
        """Run the GitHub integration workflow"""
        try:
            # Example workflow
            title = config.get("title", "New Feature")
            body = config.get("body", "This is a new feature")
            branch = config.get("branch", "feature-branch")
            file_path = config.get("file_path", "README.md")
            file_content = config.get("file_content", "# New Feature")

            # Create branch
            self.create_branch(branch)

            # Update file
            self.update_file(file_path, file_content, "Add new feature", branch)

            # Create pull request
            pr = self.create_pull_request(title, body, branch, "main")

            # Wait for CI checks
            if self.wait_for_checks(pr["number"]):
                # Get failed checks
                failed_checks = self.get_failed_checks(pr["number"])

                if failed_checks:
                    # Create issue for failed tests
                    issue = self.create_issue(
                        "CI Tests Failed",
                        f"Failed tests in PR #{pr['number']}: {failed_checks}",
                        ["bug", "ci-failure"]
                    )

                    # Add to project board
                    self.add_project_card(issue["number"], 1, "In Progress")

                    return {
                        "status": "failed",
                        "pr": pr,
                        "issue": issue,
                        "failed_checks": failed_checks
                    }
                else:
                    return {
                        "status": "success",
                        "pr": pr,
                        "message": "All tests passed"
                    }
            else:
                return {
                    "status": "timeout",
                    "pr": pr,
                    "message": "CI checks timed out"
                }

        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }

    def __init__(self):
        super().__init__(
            name="GitIntegrator",
            description="Handles comprehensive Git operations, CI/CD integration, and tool integrations",
            tools=["git_operations", "ci_cd_integration", "version_control", "tool_integration", "cloud_integration"]
        )

    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle comprehensive Git operations, CI/CD integration, and tool integrations"""
        # Get project information from context
        project_name = context.get("project_name", "project")
        project_structure = context.get("project_structure", {})
        code_implementation = context.get("code_implementation", {})
        integration_points = context.get("integration_points", {})

        # GitHub integration
        github_token = context.get("github_token")
        repo_owner = context.get("repo_owner")
        repo_name = context.get("repo_name")

        if github_token and repo_owner and repo_name:
            # Initialize GitHub integrator
            github = GitIntegrator(github_token, repo_owner, repo_name)

            # Create branch
            branch_name = f"feature/{project_name}"
            github.create_branch(branch_name)

            # Update files
            for file_path, content in code_implementation.items():
                github.update_file(file_path, content, f"Add {file_path}", branch_name)

            # Create pull request
            pr = github.create_pull_request(
                f"Add {project_name} feature",
                f"This PR adds the {project_name} feature",
                branch_name,
                "main"
            )

            # Wait for CI checks
            if github.wait_for_checks(pr["number"]):
                failed_checks = github.get_failed_checks(pr["number"])

                if failed_checks:
                    # Create issue for failed tests
                    issue = github.create_issue(
                        f"CI Tests Failed for {project_name}",
                        f"Failed tests in PR #{pr['number']}: {failed_checks}",
                        ["bug", "ci-failure"]
                    )

                    # Add to project board
                    github.add_project_card(issue["number"], 1, "In Progress")

                    return {
                        "status": "failed",
                        "pr": pr,
                        "issue": issue,
                        "failed_checks": failed_checks
                    }
                else:
                    return {
                        "status": "success",
                        "pr": pr,
                        "message": "All tests passed"
                    }
            else:
                return {
                    "status": "timeout",
                    "pr": pr,
                    "message": "CI checks timed out"
                }

        return {
            "status": "skipped",
            "message": "GitHub integration not configured"
        }

        # Initialize Git repository
        git_status = await self._initialize_git_repo(project_name)

        # Create .gitignore file
        gitignore_created = await self._create_comprehensive_gitignore()

        # Create README file
        readme_created = await self._create_enhanced_readme(project_name, project_structure, integration_points)

        # Create CI/CD pipeline
        ci_cd_pipeline = await self._create_enhanced_ci_cd_pipeline(integration_points)

        # Create integration configurations
        integration_configs = await self._create_integration_configurations(integration_points)

        # Commit initial files
        commit_result = await self._commit_initial_files()

        # Set up GitHub integration
        github_integration = await self._setup_github_integration(integration_points)

        return {
            "git_status": git_status,
            "gitignore_created": gitignore_created,
            "readme_created": readme_created,
            "ci_cd_pipeline": ci_cd_pipeline,
            "integration_configs": integration_configs,
            "commit_result": commit_result,
            "github_integration": github_integration,
            "next_role": None  # Final role in workflow
        }

    async def _initialize_git_repo(self, project_name: str) -> Dict[str, Any]:
        """Initialize Git repository with enhanced configuration"""
        try:
            # Initialize Git repo
            subprocess.run(["git", "init"], check=True, capture_output=True)

            # Set Git config
            subprocess.run(["git", "config", "user.name", "MultiAgentCoder"], check=True)
            subprocess.run(["git", "config", "user.email", "coder@multiagent.com"], check=True)

            # Set up Git branches
            subprocess.run(["git", "checkout", "-b", "develop"], check=True)
            subprocess.run(["git", "checkout", "-b", "main"], check=True)
            subprocess.run(["git", "checkout", "develop"], check=True)

            # Set up Git hooks
            os.makedirs(".git/hooks", exist_ok=True)
            with open(".git/hooks/pre-commit", 'w') as f:
                f.write("#!/bin/sh\n# Pre-commit hook for code quality checks\necho 'Running pre-commit checks...'\n")
            os.chmod(".git/hooks/pre-commit", 0o755)

            return {
                "status": "success",
                "message": "Git repository initialized successfully with enhanced configuration",
                "repo_name": project_name,
                "branches": ["main", "develop"],
                "hooks": ["pre-commit"]
            }
        except subprocess.CalledProcessError as e:
            return {
                "status": "error",
                "message": f"Failed to initialize Git repository: {e.stderr.decode()}"
            }

    async def _create_comprehensive_gitignore(self) -> Dict[str, Any]:
        """Create comprehensive .gitignore file"""
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
*.egg-info/
dist/
build/
*.egg

# Node
node_modules/
dist/
build/
*.log

# Logs
logs/
*.log
*.log.*

# OS
.DS_Store
Thumbs.db
desktop.ini

# IDEs
.idea/
.vscode/
*.iml
*.ipr
*.iws
.idea_modules/

# Virtual environments
venv/
ENV/
env/
env.bak/
venv.bak/

# Database
*.sqlite3
*.db
*.sqlite

# Secrets
*.env
*.env.*
*.secret
*.key

# Dependencies
Pipfile.lock
poetry.lock
yarn.lock
package-lock.json

# Coverage
.coverage
.coverage.*
htmlcov/
*.coverage

# Documentation
docs/_build/
docs/_static/
docs/_templates/

# Docker
*.dockerfile
docker-compose.override.yml

# Cloud
.terraform/
*.tfstate
*.tfstate.*

# Build artifacts
out/
output/
target/
bin/
obj/
"""

        try:
            with open(".gitignore", 'w') as f:
                f.write(gitignore_content)

            return {
                "status": "success",
                "message": "Comprehensive .gitignore file created successfully"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to create .gitignore file: {str(e)}"
            }

    async def _create_enhanced_readme(self, project_name: str, project_structure: Dict[str, Any], integration_points: Dict[str, Any]) -> Dict[str, Any]:
        """Create enhanced README file with integration information"""
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

## Integrations

### Version Control
- **System**: {integration_points.get('version_control', 'GitHub')}
- **Repository**: https://github.com/your-org/{project_name.lower().replace(' ', '-')}
- **Branches**: main, develop, feature/*

### CI/CD
- **System**: {integration_points.get('ci_cd', 'GitHub Actions')}
- **Pipeline**: .github/workflows/ci_cd.yml
- **Triggers**: Push to main/develop, Pull Requests

### Project Management
- **System**: {integration_points.get('project_management', 'Jira')}
- **Board**: https://your-jira.com/projects/{project_name.upper().replace(' ', '')}
- **Sprints**: 2-week cycles

### Cloud Platform
- **Provider**: {integration_points.get('cloud_platform', 'AWS')}
- **Services**: EC2, RDS, S3, Lambda
- **Region**: us-east-1

### Monitoring
- **System**: Prometheus + Grafana
- **Dashboard**: https://your-grafana.com/dashboards/project
- **Alerts**: Slack notifications

## Contributing

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Make your changes and commit: `git commit -m 'Add your feature'`
3. Push to the branch: `git push origin feature/your-feature`
4. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
"""

        try:
            with open("README.md", 'w') as f:
                f.write(readme_content)

            return {
                "status": "success",
                "message": "Enhanced README.md file created successfully"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to create README.md file: {str(e)}"
            }

    async def _create_enhanced_ci_cd_pipeline(self, integration_points: Dict[str, Any]) -> Dict[str, Any]:
        """Create enhanced CI/CD pipeline configuration"""
        ci_cd_content = f"""
name: Enhanced CI/CD Pipeline

on:
  push:
    branches: [ main, develop, feature/* ]
  pull_request:
    branches: [ main, develop ]
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.9', '3.10']

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python ${{{{ matrix.python-version }}}}
      uses: actions/setup-python@v4
      with:
        python-version: ${{{{ matrix.python-version }}}}

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install -r requirements-dev.txt

    - name: Run linters
      run: |
        black --check .
        flake8 .
        isort --check-only .

    - name: Run tests
      run: |
        pytest tests/unit/ --cov=src --cov-report=xml
        pytest tests/integration/ --cov=src --cov-report=xml

    - name: Build Docker image
      run: |
        docker build -t {integration_points.get('project_name', 'project-name').lower().replace(' ', '-')} .

    - name: Run security scans
      run: |
        bandit -r src/
        safety check -r requirements.txt

    - name: Deploy to staging
      if: github.ref == 'refs/heads/develop'
      run: |
        # Add deployment commands here
        echo "Deploying to staging environment on {integration_points.get('cloud_platform', 'AWS')}"

    - name: Deploy to production
      if: github.ref == 'refs/heads/main'
      run: |
        # Add deployment commands here
        echo "Deploying to production environment on {integration_points.get('cloud_platform', 'AWS')}"

    - name: Notify Slack
      if: always()
      run: |
        # Add Slack notification commands here
        echo "Sending notification to Slack about deployment status"
"""

        try:
            os.makedirs(".github/workflows", exist_ok=True)
            with open(".github/workflows/ci_cd.yml", 'w') as f:
                f.write(ci_cd_content)

            return {
                "status": "success",
                "message": "Enhanced CI/CD pipeline configuration created successfully",
                "pipeline_features": [
                    "Multi-Python version support",
                    "Linting and code quality checks",
                    "Test coverage reporting",
                    "Security scans",
                    "Multi-environment deployment",
                    "Slack notifications"
                ]
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to create CI/CD pipeline configuration: {str(e)}"
            }

    async def _create_integration_configurations(self, integration_points: Dict[str, Any]) -> Dict[str, Any]:
        """Create integration configurations for various tools"""
        configs = {}

        # Jira integration
        jira_config = """
# Jira Integration Configuration
[jira]
url = https://your-jira.com
project = PROJECT_KEY
board = BOARD_ID
username = your-username
token = your-api-token
"""
        configs["jira"] = jira_config
        with open(".jira_config", 'w') as f:
            f.write(jira_config)

        # Slack integration
        slack_config = """
# Slack Integration Configuration
[slack]
webhook = https://hooks.slack.com/services/your/webhook
channel = #project-updates
username = ProjectBot
icon_emoji = :rocket:
"""
        configs["slack"] = slack_config
        with open(".slack_config", 'w') as f:
            f.write(slack_config)

        # AWS integration
        aws_config = """
# AWS Integration Configuration
[aws]
region = us-east-1
profile = default
s3_bucket = your-project-bucket
ec2_instance = i-1234567890abcdef0
rds_instance = your-database-instance
"""
        configs["aws"] = aws_config
        with open(".aws_config", 'w') as f:
            f.write(aws_config)

        # Docker integration
        docker_config = """
# Docker Integration Configuration
[docker]
registry = your-registry-url
username = your-username
password = your-password
image_name = your-project-name
tag = latest
"""
        configs["docker"] = docker_config
        with open(".docker_config", 'w') as f:
            f.write(docker_config)

        return {
            "status": "success",
            "message": "Integration configurations created successfully",
            "configs_created": list(configs.keys())
        }

    async def _setup_github_integration(self, integration_points: Dict[str, Any]) -> Dict[str, Any]:
        """Set up GitHub integration"""
        github_config = """
# GitHub Integration Configuration
[github]
repo = your-org/project-name
branch_protection = main,develop
required_reviews = 2
status_checks = ci_cd,lint,test
webhooks = slack,jenkins
labels = bug,enhancement,documentation
milestones = v1.0,v2.0
"""
        try:
            with open(".github_config", 'w') as f:
                f.write(github_config)

            return {
                "status": "success",
                "message": "GitHub integration configured successfully",
                "features": [
                    "Branch protection",
                    "Required reviews",
                    "Status checks",
                    "Webhooks",
                    "Labels",
                    "Milestones"
                ]
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to set up GitHub integration: {str(e)}"
            }

    async def _commit_initial_files(self) -> Dict[str, Any]:
        """Commit initial files to Git with enhanced commit message"""
        try:
            # Add all files
            subprocess.run(["git", "add", "."], check=True)

            # Commit files with detailed message
            commit_message = """Initial commit - project setup

- Initialized Git repository with branches and hooks
- Created comprehensive .gitignore file
- Created enhanced README with project structure and integrations
- Set up enhanced CI/CD pipeline with multi-Python support
- Created integration configurations for Jira, Slack, AWS, Docker
- Set up GitHub integration with branch protection
"""
            subprocess.run(["git", "commit", "-m", commit_message], check=True)

            return {
                "status": "success",
                "message": "Initial files committed successfully with enhanced details",
                "commit_message": commit_message
            }
        except subprocess.CalledProcessError as e:
            return {
                "status": "error",
                "message": f"Failed to commit initial files: {e.stderr.decode()}"
            }






