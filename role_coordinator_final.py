


import asyncio
from typing import Dict, Any, List, Type
from roles import ProductManager, Architect, Engineer, QaEngineer
from roles.critical_evaluator import CriticalEvaluator
from roles.qa_tester import QaTester
from roles.unified_roles import AnalystArchitect, DeveloperEngineer
from roles.task_decomposer import TaskDecomposer
from roles.reviewer import Reviewer
from roles.documentation_specialist import DocumentationSpecialist
from roles.project_manager import ProjectManager
from roles.git_integrator import GitIntegrator
from roles.test_runner import TestRunner
from roles.agent_monitor import AgentMonitor
from roles.base_role import BaseRole

class RoleCoordinator:
    """Coordinates the execution of different roles in the development process"""

    def __init__(self, use_unified_roles: bool = False, use_task_decomposer: bool = False,
                 use_reviewer: bool = False, use_full_workflow: bool = False,
                 use_test_runner: bool = False, use_agent_monitor: bool = False,
                 use_standard_workflow: bool = True):
        if use_full_workflow:
            # Full workflow with all roles
            if use_unified_roles:
                self.roles = {
                    "ProjectManager": ProjectManager(),
                    "AnalystArchitect": AnalystArchitect(),
                    "TaskDecomposer": TaskDecomposer(),
                    "DeveloperEngineer": DeveloperEngineer(),
                    "Reviewer": Reviewer(),
                    "TestRunner": TestRunner(),
                    "DocumentationSpecialist": DocumentationSpecialist(),
                    "GitIntegrator": GitIntegrator(),
                    "AgentMonitor": AgentMonitor()
                }
                if use_test_runner:
                    if use_agent_monitor:
                        self.workflow = [
                            "AgentMonitor",
                            "ProjectManager",
                            "AnalystArchitect",
                            "TaskDecomposer",
                            "DeveloperEngineer",
                            "Reviewer",
                            "TestRunner",
                            "DocumentationSpecialist",
                            "GitIntegrator"
                        ]
                    else:
                        self.workflow = [
                            "ProjectManager",
                            "AnalystArchitect",
                            "TaskDecomposer",
                            "DeveloperEngineer",
                            "Reviewer",
                            "TestRunner",
                            "DocumentationSpecialist",
                            "GitIntegrator"
                        ]
                else:
                    if use_agent_monitor:
                        self.workflow = [
                            "AgentMonitor",
                            "ProjectManager",
                            "AnalystArchitect",
                            "TaskDecomposer",
                            "DeveloperEngineer",
                            "Reviewer",
                            "DocumentationSpecialist",
                            "GitIntegrator"
                        ]
                    else:
                        self.workflow = [
                            "ProjectManager",
                            "AnalystArchitect",
                            "TaskDecomposer",
                            "DeveloperEngineer",
                            "Reviewer",
                            "DocumentationSpecialist",
                            "GitIntegrator"
                        ]
            else:
                # Standard workflow with separate roles
                self.roles = {
                    "ProductManager": ProductManager(),
                    "Architect": Architect(),
                    "Engineer": Engineer(),
                    "CriticalEvaluator": CriticalEvaluator(),
                    "QaEngineer": QaEngineer(),
                    "QaTester": QaTester()
                }
                self.workflow = [
                    "ProductManager",
                    "Architect",
                    "CriticalEvaluator",  # Evaluate architecture decisions
                    "Engineer",
                    "CriticalEvaluator",  # Evaluate implementation decisions
                    "QaEngineer",
                    "QaTester"
                ]
        elif use_standard_workflow:
            # Standard workflow with separate roles
            self.roles = {
                "ProductManager": ProductManager(),
                "Architect": Architect(),
                "Engineer": Engineer(),
                "CriticalEvaluator": CriticalEvaluator(),
                "QaEngineer": QaEngineer(),
                "QaTester": QaTester()
            }
            self.workflow = [
                "ProductManager",
                "Architect",
                "CriticalEvaluator",  # Evaluate architecture decisions
                "Engineer",
                "CriticalEvaluator",  # Evaluate implementation decisions
                "QaEngineer",
                "QaTester"
            ]
        else:
            # Minimal workflow
            if use_unified_roles:
                if use_reviewer:
                    self.roles = {
                        "AnalystArchitect": AnalystArchitect(),
                        "TaskDecomposer": TaskDecomposer(),
                        "DeveloperEngineer": DeveloperEngineer(),
                        "Reviewer": Reviewer()
                    }
                    self.workflow = [
                        "AnalystArchitect",
                        "TaskDecomposer",
                        "DeveloperEngineer",
                        "Reviewer"
                    ]
                else:
                    self.roles = {
                        "AnalystArchitect": AnalystArchitect(),
                        "TaskDecomposer": TaskDecomposer(),
                        "DeveloperEngineer": DeveloperEngineer()
                    }
                    self.workflow = [
                        "AnalystArchitect",
                        "TaskDecomposer",
                        "DeveloperEngineer"
                    ]
            else:
                # Minimal workflow with separate roles
                self.roles = {
                    "ProductManager": ProductManager(),
                    "Architect": Architect(),
                    "Engineer": Engineer(),
                    "QaEngineer": QaEngineer(),
                    "QaTester": QaTester()
                }
                self.workflow = [
                    "ProductManager",
                    "Architect",
                    "Engineer",
                    "QaEngineer",
                    "QaTester"
                ]

        self.context = {}
        print(f"DEBUG: Initialized with {len(self.roles)} roles")
        print(f"DEBUG: Workflow: {self.workflow}")

    async def run_workflow(self, initial_context: Dict[str, Any]) -> Dict[str, Any]:
        """Run the complete development workflow"""
        self.context.update(initial_context)

        for role_name in self.workflow:
            role = self.roles[role_name]
            print(f"Executing {role_name}...")
            result = await role.execute(self.context)
            self.context.update(result)

            # Check if workflow should continue
            next_role = result.get("next_role")
            if next_role and next_role in self.roles:
                # Dynamic workflow adjustment
                current_index = self.workflow.index(role_name)
                if current_index + 1 < len(self.workflow):
                    # Insert next role after current one
                    next_role_index = self.workflow.index(next_role)
                    if next_role_index > current_index:
                        # Only adjust if the next role is not already next in sequence
                        remaining_roles = self.workflow[current_index+1:]
                        if next_role in remaining_roles:
                            remaining_roles.remove(next_role)
                            new_workflow = self.workflow[:current_index+1] + [next_role] + remaining_roles
                            self.workflow = new_workflow

        return self.context


