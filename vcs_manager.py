

import subprocess
import os
from pathlib import Path

class VCSManager:
    def __init__(self, repo_path=None):
        """Initialize VCS manager."""
        self.repo_path = repo_path or os.getcwd()
        self.repo_path = Path(self.repo_path).absolute()

    def initialize_repo(self):
        """Initialize a new Git repository."""
        try:
            result = subprocess.run(
                ['git', 'init'],
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                return {"success": True, "message": "Git repository initialized"}
            else:
                return {"success": False, "error": result.stderr}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def commit_code(self, files, message="Auto-commit generated code"):
        """Commit code files to Git repository."""
        try:
            # Add files to Git
            for file_path in files:
                full_path = self.repo_path / file_path
                if full_path.exists():
                    subprocess.run(
                        ['git', 'add', '-f', str(full_path)],
                        cwd=self.repo_path,
                        check=True
                    )

            # Commit the files
            result = subprocess.run(
                ['git', 'commit', '-m', message],
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                return {"success": True, "message": "Code committed successfully"}
            else:
                return {"success": False, "error": result.stderr}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def setup_git_config(self, username="MultiAgentCoder", email="coder@multiagent.system"):
        """Set up Git configuration."""
        try:
            subprocess.run(
                ['git', 'config', 'user.name', username],
                cwd=self.repo_path,
                check=True
            )
            subprocess.run(
                ['git', 'config', 'user.email', email],
                cwd=self.repo_path,
                check=True
            )
            return {"success": True, "message": "Git config set up"}
        except Exception as e:
            return {"success": False, "error": str(e)}



    def create_branch(self, branch_name):
        """Create a new Git branch."""
        try:
            result = subprocess.run(
                ['git', 'checkout', '-b', branch_name],
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                return {"success": True, "message": f"Branch '{branch_name}' created and checked out"}
            else:
                return {"success": False, "error": result.stderr}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def push_changes(self, branch_name=None):
        """Push changes to remote repository."""
        try:
            if branch_name:
                # Push specific branch
                result = subprocess.run(
                    ['git', 'push', 'origin', branch_name],
                    cwd=self.repo_path,
                    capture_output=True,
                    text=True
                )
            else:
                # Push current branch
                result = subprocess.run(
                    ['git', 'push'],
                    cwd=self.repo_path,
                    capture_output=True,
                    text=True
                )

            if result.returncode == 0:
                return {"success": True, "message": "Changes pushed successfully"}
            else:
                return {"success": False, "error": result.stderr}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_status(self):


        """Get Git repository status."""
        try:
            result = subprocess.run(
                ['git', 'status', '--porcelain'],
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                return {"success": True, "status": result.stdout}
            else:
                return {"success": False, "error": result.stderr}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def create_branch(self, branch_name):
        """Create a new Git branch."""
        try:
            result = subprocess.run(
                ['git', 'checkout', '-b', branch_name],
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                return {"success": True, "message": f"Branch '{branch_name}' created"}
            else:
                return {"success": False, "error": result.stderr}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def push_changes(self, remote="origin", branch=None):
        """Push changes to remote repository."""
        try:
            branch = branch or self._get_current_branch()
            if not branch:
                return {"success": False, "error": "No branch specified and could not determine current branch"}

            result = subprocess.run(
                ['git', 'push', remote, branch],
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                return {"success": True, "message": f"Changes pushed to {remote}/{branch}"}
            else:
                return {"success": False, "error": result.stderr}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _get_current_branch(self):
        """Get the current Git branch."""
        try:
            result = subprocess.run(
                ['git', 'branch', '--show-current'],
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                return result.stdout.strip()
            return None
        except Exception:
            return None

