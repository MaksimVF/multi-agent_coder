










import os
from typing import Dict, Any, List
from .base_role import BaseRole

class ProjectManager(BaseRole):
    """Enhanced Project Manager role - handles comprehensive project management including risk, resource, and quality management"""

    def __init__(self):
        super().__init__(
            name="ProjectManager",
            description="Handles comprehensive project management including planning, risk, resource, and quality management",
            tools=["project_planning", "task_tracking", "sprint_management", "risk_management", "resource_management", "quality_management", "report_generation", "integration_management"]
        )

    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Manage comprehensive project management"""
        # Get project information from context
        requirements = context.get("requirements", "")
        task_list = context.get("task_list", [])
        project_status = context.get("project_status", {})

        # Create comprehensive project plan
        project_plan = await self._create_comprehensive_project_plan(requirements, task_list)

        # Plan sprints with enhanced details
        sprint_plan = await self._plan_enhanced_sprints(task_list)

        # Manage risks
        risk_management = await self._manage_risks(project_plan)

        # Manage resources
        resource_management = await self._manage_resources(project_plan)

        # Manage quality
        quality_management = await self._manage_quality(project_plan)

        # Track progress with enhanced metrics
        progress_report = await self._track_enhanced_progress(project_status, task_list)

        # Generate comprehensive project timeline
        timeline = await self._generate_comprehensive_timeline(project_plan)

        # Generate project dashboard
        dashboard = await self._generate_project_dashboard(project_plan, progress_report, risk_management)

        return {
            "project_plan": project_plan,
            "sprint_plan": sprint_plan,
            "risk_management": risk_management,
            "resource_management": resource_management,
            "quality_management": quality_management,
            "progress_report": progress_report,
            "project_timeline": timeline,
            "project_dashboard": dashboard,
            "next_role": "AnalystArchitect"  # Next role in workflow
        }

    async def _create_comprehensive_project_plan(self, requirements: str, task_list: List[str]) -> Dict[str, Any]:
        """Create comprehensive project plan with risk, resource, and quality management"""
        return {
            "project_name": "Comprehensive Web Application",
            "description": "A web application with frontend, backend, and database",
            "requirements": requirements,
            "tasks": task_list,
            "milestones": [
                {"name": "Architecture Design", "date": "2025-10-01", "status": "planned"},
                {"name": "Backend Development", "date": "2025-10-15", "status": "planned"},
                {"name": "Frontend Development", "date": "2025-10-30", "status": "planned"},
                {"name": "Testing", "date": "2025-11-15", "status": "planned"},
                {"name": "Deployment", "date": "2025-11-30", "status": "planned"}
            ],
            "budget": {
                "total": 50000,
                "development": 30000,
                "testing": 10000,
                "deployment": 5000,
                "contingency": 5000,
                "used": 0,
                "remaining": 50000
            },
            "resources": {
                "developers": {"total": 5, "available": 5, "allocated": 0},
                "testers": {"total": 2, "available": 2, "allocated": 0},
                "devops": {"total": 1, "available": 1, "allocated": 0},
                "project_manager": {"total": 1, "available": 1, "allocated": 0},
                "servers": {"total": 3, "available": 3, "allocated": 0}
            },
            "risks": [
                {"id": 1, "description": "Technical debt accumulation", "impact": "high", "probability": "medium", "mitigation": "Regular code reviews and refactoring"},
                {"id": 2, "description": "Team member turnover", "impact": "medium", "probability": "low", "mitigation": "Knowledge sharing and documentation"},
                {"id": 3, "description": "Scope creep", "impact": "high", "probability": "medium", "mitigation": "Clear requirements and change management"}
            ],
            "quality_metrics": {
                "code_coverage": {"target": 90, "current": 0},
                "defect_density": {"target": 0.5, "current": 0},
                "performance": {"target": "200ms response time", "current": "N/A"},
                "user_satisfaction": {"target": 95, "current": 0}
            },
            "communication_plan": {
                "stakeholder_meetings": "Weekly",
                "team_meetings": "Daily standups",
                "progress_reports": "Bi-weekly",
                "tools": ["Slack", "Jira", "Confluence"]
            },
            "integration_points": {
                "version_control": "GitHub",
                "ci_cd": "GitHub Actions",
                "project_management": "Jira",
                "cloud_platform": "AWS"
            }
        }

    async def _plan_enhanced_sprints(self, task_list: List[str]) -> Dict[str, Any]:
        """Plan enhanced sprints with detailed information"""
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
                "goal": f"Complete sprint {sprint_number} tasks",
                "status": "planned",
                "velocity": 0,
                "completed_tasks": 0,
                "remaining_tasks": len(sprint_tasks),
                "risks": [],
                "dependencies": []
            })
            sprint_number += 1

        return {
            "total_sprints": len(sprints),
            "sprints": sprints,
            "current_sprint": 1,
            "average_velocity": 0,
            "burn_down_chart": "N/A"
        }

    async def _manage_risks(self, project_plan: Dict[str, Any]) -> Dict[str, Any]:
        """Manage project risks"""
        risks = project_plan.get("risks", [])

        return {
            "total_risks": len(risks),
            "high_impact_risks": [r for r in risks if r["impact"] == "high"],
            "medium_impact_risks": [r for r in risks if r["impact"] == "medium"],
            "low_impact_risks": [r for r in risks if r["impact"] == "low"],
            "mitigation_strategies": {r["id"]: r["mitigation"] for r in risks},
            "risk_status": "Managed" if len(risks) > 0 else "No risks identified"
        }

    async def _manage_resources(self, project_plan: Dict[str, Any]) -> Dict[str, Any]:
        """Manage project resources"""
        resources = project_plan.get("resources", {})

        return {
            "total_resources": sum(r["total"] for r in resources.values()),
            "available_resources": sum(r["available"] for r in resources.values()),
            "allocated_resources": sum(r["allocated"] for r in resources.values()),
            "resource_utilization": {
                resource: {
                    "total": info["total"],
                    "available": info["available"],
                    "allocated": info["allocated"],
                    "utilization_rate": info["allocated"] / info["total"] if info["total"] > 0 else 0
                }
                for resource, info in resources.items()
            },
            "resource_status": "Balanced" if all(r["available"] >= 0 for r in resources.values()) else "Overallocated"
        }

    async def _manage_quality(self, project_plan: Dict[str, Any]) -> Dict[str, Any]:
        """Manage project quality"""
        quality_metrics = project_plan.get("quality_metrics", {})

        return {
            "quality_metrics": quality_metrics,
            "quality_status": "On target" if all(
                metric["current"] >= metric["target"] for metric in quality_metrics.values()
            ) else "Needs improvement",
            "quality_actions": {
                "code_coverage": "Implement more unit tests",
                "defect_density": "Improve code reviews",
                "performance": "Optimize database queries",
                "user_satisfaction": "Gather user feedback"
            }
        }

    async def _track_enhanced_progress(self, project_status: Dict[str, Any], task_list: List[str]) -> Dict[str, Any]:
        """Track project progress with enhanced metrics"""
        completed_tasks = project_status.get("completed_tasks", 0)
        total_tasks = len(task_list)

        return {
            "completed_tasks": completed_tasks,
            "total_tasks": total_tasks,
            "progress_percentage": (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0,
            "status": "On track" if completed_tasks >= total_tasks * 0.8 else "At risk",
            "next_milestone": project_status.get("next_milestone", "Architecture Design"),
            "burn_down_chart": "N/A",
            "velocity": completed_tasks / (project_status.get("weeks_elapsed", 1)),
            "earned_value": {
                "planned_value": total_tasks * 0.8,
                "earned_value": completed_tasks,
                "cost_performance_index": completed_tasks / (total_tasks * 0.8) if total_tasks > 0 else 0
            },
            "critical_path": ["Architecture Design", "Backend Development", "Testing"]
        }

    async def _generate_comprehensive_timeline(self, project_plan: Dict[str, Any]) -> str:
        """Generate comprehensive project timeline (text representation)"""
        timeline = """
# Comprehensive Project Timeline

```mermaid
gantt
    title Comprehensive Project Timeline
    dateFormat  YYYY-MM-DD
    section Project Phases
    Architecture Design   :2025-10-01, 2025-10-15
    Backend Development   :2025-10-15, 2025-10-30
    Frontend Development  :2025-10-30, 2025-11-15
    Testing              :2025-11-15, 2025-11-30
    Deployment           :2025-11-30, 2025-12-15
    section Milestones
    MVP Release          :2025-11-30, 2025-11-30
    Beta Testing         :2025-12-01, 2025-12-15
    Final Release        :2025-12-30, 2025-12-30
```

## Timeline Description

1. **Architecture Design (2025-10-01 to 2025-10-15)**: Design system architecture and create project skeleton
2. **Backend Development (2025-10-15 to 2025-10-30)**: Implement backend services and API
3. **Frontend Development (2025-10-30 to 2025-11-15)**: Implement frontend components and UI
4. **Testing (2025-11-15 to 2025-11-30)**: Perform comprehensive testing
5. **Deployment (2025-11-30 to 2025-12-15)**: Deploy to production environment
6. **MVP Release (2025-11-30)**: Release minimum viable product
7. **Beta Testing (2025-12-01 to 2025-12-15)**: Conduct beta testing with users
8. **Final Release (2025-12-30)**: Final product release
"""

        return timeline

    async def _generate_project_dashboard(self, project_plan: Dict[str, Any], progress_report: Dict[str, Any], risk_management: Dict[str, Any]) -> str:
        """Generate project dashboard (text representation)"""
        dashboard = """
# Project Dashboard

## Project Overview
- **Project Name**: {project_name}
- **Status**: {status}
- **Progress**: {progress_percentage:.1f}%
- **Budget**: ${used}/${total} ({remaining} remaining)

## Key Metrics
- **Completed Tasks**: {completed_tasks}/{total_tasks}
- **Velocity**: {velocity} tasks/week
- **Earned Value**: {earned_value} (CPI: {cpi:.2f})
- **Quality**: {quality_status}
- **Risks**: {risk_count} (High: {high_risk_count}, Medium: {medium_risk_count})

## Timeline
```mermaid
gantt
    title Project Timeline
    dateFormat  YYYY-MM-DD
    section Phases
    Architecture Design   :2025-10-01, 2025-10-15
    Backend Development   :2025-10-15, 2025-10-30
    Frontend Development  :2025-10-30, 2025-11-15
    Testing              :2025-11-15, 2025-11-30
    Deployment           :2025-11-30, 2025-12-15
```

## Risk Management
- **Total Risks**: {risk_count}
- **High Impact**: {high_risk_count}
- **Medium Impact**: {medium_risk_count}
- **Low Impact**: {low_risk_count}

## Resource Utilization
- **Developers**: {dev_utilization:.1f}%
- **Testers**: {test_utilization:.1f}%
- **DevOps**: {devops_utilization:.1f}%
- **Servers**: {server_utilization:.1f}%
"""

        # Fill in dashboard data
        project_name = project_plan.get("project_name", "Project")
        status = progress_report.get("status", "Unknown")
        progress_percentage = progress_report.get("progress_percentage", 0)
        used = project_plan.get("budget", {}).get("used", 0)
        total = project_plan.get("budget", {}).get("total", 0)
        remaining = project_plan.get("budget", {}).get("remaining", 0)
        completed_tasks = progress_report.get("completed_tasks", 0)
        total_tasks = progress_report.get("total_tasks", 0)
        velocity = progress_report.get("velocity", 0)
        earned_value = progress_report.get("earned_value", {}).get("earned_value", 0)
        cpi = progress_report.get("earned_value", {}).get("cost_performance_index", 0)
        quality_status = "On target"  # Simplified for example
        risk_count = risk_management.get("total_risks", 0)
        high_risk_count = len(risk_management.get("high_impact_risks", []))
        medium_risk_count = len(risk_management.get("medium_impact_risks", []))
        low_risk_count = len(risk_management.get("low_impact_risks", []))
        dev_utilization = project_plan.get("resources", {}).get("developers", {}).get("utilization_rate", 0) * 100
        test_utilization = project_plan.get("resources", {}).get("testers", {}).get("utilization_rate", 0) * 100
        devops_utilization = project_plan.get("resources", {}).get("devops", {}).get("utilization_rate", 0) * 100
        server_utilization = project_plan.get("resources", {}).get("servers", {}).get("utilization_rate", 0) * 100

        # Format dashboard
        dashboard = dashboard.format(
            project_name=project_name,
            status=status,
            progress_percentage=progress_percentage,
            used=used,
            total=total,
            remaining=remaining,
            completed_tasks=completed_tasks,
            total_tasks=total_tasks,
            velocity=velocity,
            earned_value=earned_value,
            cpi=cpi,
            quality_status=quality_status,
            risk_count=risk_count,
            high_risk_count=high_risk_count,
            medium_risk_count=medium_risk_count,
            low_risk_count=low_risk_count,
            dev_utilization=dev_utilization,
            test_utilization=test_utilization,
            devops_utilization=devops_utilization,
            server_utilization=server_utilization
        )

        return dashboard







