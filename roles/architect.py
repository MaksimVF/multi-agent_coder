




import os
from typing import Dict, Any, List
from .base_role import BaseRole

class Architect(BaseRole):
    """Architect role - responsible for system design and project skeleton creation"""

    def __init__(self):
        super().__init__(
            name="Architect",
            description="Designs system architecture and creates project skeleton",
            tools=["system_design", "code_generation", "file_management"]
        )

    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Design system architecture and create project skeleton"""
        # Get PRD from context
        prd = context.get("prd", "")

        # Design system architecture
        architecture = await self._design_architecture(prd)

        # Create project skeleton
        project_structure = await self._create_project_skeleton(architecture)

        # Generate architecture documentation
        arch_doc = await self._generate_architecture_doc(architecture)

        # Update context with results
        result = {
            "system_architecture": architecture,
            "project_structure": project_structure,
            "architecture_documentation": arch_doc,
            "next_role": "Engineer"
        }

        return result

    async def _design_architecture(self, prd: str) -> Dict[str, Any]:
        """Design system architecture based on PRD"""
        # This would use LLM to design architecture
        # For now, return a simple structure
        return {
            "components": ["frontend", "backend", "database"],
            "technologies": ["Python", "FastAPI", "React"],
            "data_flow": "frontend -> backend -> database"
        }

    async def _create_project_skeleton(self, architecture: Dict[str, Any]) -> Dict[str, List[str]]:
        """Create project skeleton based on architecture"""
        # Create basic file structure
        structure = {
            "root": ["README.md", "requirements.txt", "setup.py"],
            "src": ["main.py", "config.py"],
            "frontend": ["index.html", "app.js"],
            "backend": ["api.py", "models.py"],
            "tests": ["test_main.py", "test_api.py"]
        }

        # Create directories and files
        for directory, files in structure.items():
            if directory != "root":
                os.makedirs(directory, exist_ok=True)
            for file in files:
                path = os.path.join(directory, file) if directory != "root" else file
                if not os.path.exists(path):
                    with open(path, 'w') as f:
                        f.write(f"# {file}\n# Part of {directory}\n")

        return structure

    async def _generate_architecture_doc(self, architecture: Dict[str, Any]) -> str:
        """Generate architecture documentation"""
        return f"""
# System Architecture

## Components
{''.join(f"- {component}\n" for component in architecture['components'])}

## Technologies
{''.join(f"- {tech}\n" for tech in architecture['technologies'])}

## Data Flow
{architecture['data_flow']}
"""



