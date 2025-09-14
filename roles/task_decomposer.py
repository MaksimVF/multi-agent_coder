






import json
from typing import Dict, Any, List
from .base_role import BaseRole

class TaskDecomposer(BaseRole):
    """Task Decomposer role - breaks down high-level goals into specific tasks"""

    def __init__(self):
        super().__init__(
            name="TaskDecomposer",
            description="Breaks down project goals into specific development tasks",
            tools=["task_analysis", "dependency_analysis"]
        )

    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Decompose project goals into specific tasks"""
        # Get system architecture and requirements from context
        requirements = context.get("requirements", "")
        architecture = context.get("system_architecture", {})

        # Analyze requirements and architecture
        task_list = await self._decompose_tasks(requirements, architecture)

        # Generate task documentation
        task_doc = await self._generate_task_documentation(task_list)

        return {
            "task_list": task_list,
            "task_documentation": task_doc,
            "next_role": "DeveloperEngineer"
        }

    async def _decompose_tasks(self, requirements: str, architecture: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Decompose project into specific tasks"""
        # This would use LLM to analyze requirements and architecture
        # For now, return a simple task structure
        components = architecture.get("components", ["frontend", "backend", "database"])

        task_list = []
        for component in components:
            if component == "frontend":
                task_list.append({
                    "file": "app.js",
                    "description": "Create frontend application",
                    "methods": ["initApp", "renderUI"],
                    "dependencies": []
                })
            elif component == "backend":
                task_list.append({
                    "file": "api.py",
                    "description": "Create backend API",
                    "methods": ["create_app", "setup_routes"],
                    "dependencies": ["app.js"]
                })
            elif component == "database":
                task_list.append({
                    "file": "models.py",
                    "description": "Create database models",
                    "methods": ["init_db", "create_tables"],
                    "dependencies": ["api.py"]
                })

        return task_list

    async def _generate_task_documentation(self, task_list: List[Dict[str, Any]]) -> str:
        """Generate task documentation"""
        doc = "# Task List\n\n"

        for i, task in enumerate(task_list, 1):
            doc += f"## Task {i}: {task['description']}\n"
            doc += f"- File: {task['file']}\n"
            doc += f"- Methods: {', '.join(task['methods'])}\n"
            if task['dependencies']:
                doc += f"- Dependencies: {', '.join(task['dependencies'])}\n"
            doc += "\n"

        return doc

    async def analyze_dependencies(self, task_list: List[Dict[str, Any]]) -> List[str]:
        """Analyze task dependencies"""
        # Simple dependency analysis
        all_files = [task['file'] for task in task_list]
        return all_files



