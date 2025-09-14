










import os
from typing import Dict, Any, List
from .base_role import BaseRole

class ProjectManager(BaseRole):
    """Project Manager role - handles project planning, task tracking, and sprint management"""

    def __init__(self):
        super().__init__(
            name="ProjectManager",
            description="Handles project planning, task tracking, and sprint management",
            tools=["project_planning", "task_tracking", "sprint_management", "report_generation"]
        )

    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Manage project planning and task tracking"""
        # Get project information from context
        requirements = context.get("requirements", "")
        task_list = context.get("task_list", [])
        project_status = context.get("project_status", {})

        # Create project plan
        project_plan = await self._create_project_plan(requirements, task_list)

        # Plan sprints
        sprint_plan = await self._plan_sprints(task_list)

        # Track progress
        progress_report = await self._track_progress(project_status, task_list)

        # Generate project timeline
        timeline = await self._generate_timeline(project_plan)

        return {
            "project_plan": project_plan,
            "sprint_plan": sprint_plan,
            "progress_report": progress_report,
            "project_timeline": timeline,
            "next_role": "AnalystArchitect"  # Next role in workflow
        }

    async def _create_project_plan(self, requirements: str, task_list: List[str]) -> Dict[str, Any]:
        """Create comprehensive project plan"""
        return {
            "project_name": "Comprehensive Web Application",
            "description": "A web application with frontend, backend, and database",
            "requirements": requirements,
            "tasks": task_list,
            "milestones": [
                {"name": "Architecture Design", "date": "2025-10-01"},
                {"name": "Backend Development", "date": "2025-10-15"},
                {"name": "Frontend Development", "date": "2025-10-30"},
                {"name": "Testing", "date": "2025-11-15"},
                {"name": "Deployment", "date": "2025-11-30"}
            ],
            "budget": {
                "total": 50000,
                "development": 30000,
                "testing": 10000,
                "deployment": 5000,
                "contingency": 5000
            },
            "resources": {
                "developers": 5,
                "testers": 2,
                "devops": 1,
                "project_manager": 1
            }
        }

    async def _plan_sprints(self, task_list: List[str]) -> Dict[str, Any]:
        """Plan sprints based on task list"""
        sprints = []
        tasks_per_sprint = 5
        sprint_number = 1

        for i in range(0, len(task_list), tasks_per_sprint):
            sprint_tasks = task_list[i:i + tasks_per_sprint]
            sprints.append({
                "sprint_number": sprint_number,
                "tasks": sprint_tasks,
                "start_date": f"2025-10-{sprint_number*15}",
                "end_date": f"2025-10-{sprint_number*15 + 14}",
                "goal": f"Complete sprint {sprint_number} tasks"
            })
            sprint_number += 1

        return {
            "total_sprints": len(sprints),
            "sprints": sprints,
            "current_sprint": 1
        }

    async def _track_progress(self, project_status: Dict[str, Any], task_list: List[str]) -> Dict[str, Any]:
        """Track project progress"""
        completed_tasks = project_status.get("completed_tasks", 0)
        total_tasks = len(task_list)

        return {
            "completed_tasks": completed_tasks,
            "total_tasks": total_tasks,
            "progress_percentage": (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0,
            "status": "On track" if completed_tasks >= total_tasks * 0.8 else "At risk",
            "next_milestone": project_status.get("next_milestone", "Architecture Design")
        }

    async def _generate_timeline(self, project_plan: Dict[str, Any]) -> str:
        """Generate project timeline (text representation)"""
        timeline = """
# Project Timeline

```mermaid
gantt
    title Project Timeline
    dateFormat  YYYY-MM-DD
    section Project Phases
    Architecture Design   :2025-10-01, 2025-10-15
    Backend Development   :2025-10-15, 2025-10-30
    Frontend Development  :2025-10-30, 2025-11-15
    Testing              :2025-11-15, 2025-11-30
    Deployment           :2025-11-30, 2025-12-15
```

## Timeline Description

1. **Architecture Design (2025-10-01 to 2025-10-15)**: Design system architecture and create project skeleton
2. **Backend Development (2025-10-15 to 2025-10-30)**: Implement backend services and API
3. **Frontend Development (2025-10-30 to 2025-11-15)**: Implement frontend components and UI
4. **Testing (2025-11-15 to 2025-11-30)**: Perform comprehensive testing
5. **Deployment (2025-11-30 to 2025-12-15)**: Deploy to production environment
"""

        return timeline







