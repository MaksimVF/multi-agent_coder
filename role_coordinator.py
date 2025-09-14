



import asyncio
from typing import Dict, Any, List
from roles import ProductManager, Architect, Engineer, QaEngineer
from roles.unified_roles import AnalystArchitect, DeveloperEngineer, TesterQa
from roles.task_decomposer import TaskDecomposer
from roles.reviewer import Reviewer
from roles.documentation_specialist import DocumentationSpecialist
from roles.project_manager import ProjectManager
from roles.git_integrator import GitIntegrator

class RoleCoordinator:
    """Coordinates the execution of different roles in the development process"""

    def __init__(self, use_unified_roles: bool = False, use_task_decomposer: bool = False, use_reviewer: bool = False, use_full_workflow: bool = False):
        if use_full_workflow:
            # Full workflow with all roles
            if use_unified_roles:
                self.roles = {
                    "ProjectManager": ProjectManager(),
                    "AnalystArchitect": AnalystArchitect(),
                    "TaskDecomposer": TaskDecomposer(),
                    "DeveloperEngineer": DeveloperEngineer(),
                    "Reviewer": Reviewer(),
                    "TesterQa": TesterQa(),
                    "DocumentationSpecialist": DocumentationSpecialist(),
                    "GitIntegrator": GitIntegrator()
                }
                self.workflow = [
                    "ProjectManager",
                    "AnalystArchitect",
                    "TaskDecomposer",
                    "DeveloperEngineer",
                    "Reviewer",
                    "TesterQa",
                    "DocumentationSpecialist",
                    "GitIntegrator"
                ]
            else:
                self.roles = {
                    "ProjectManager": ProjectManager(),
                    "ProductManager": ProductManager(),
                    "Architect": Architect(),
                    "TaskDecomposer": TaskDecomposer(),
                    "Engineer": Engineer(),
                    "Reviewer": Reviewer(),
                    "QaEngineer": QaEngineer(),
                    "DocumentationSpecialist": DocumentationSpecialist(),
                    "GitIntegrator": GitIntegrator()
                }
                self.workflow = [
                    "ProjectManager",
                    "ProductManager",
                    "Architect",
                    "TaskDecomposer",
                    "Engineer",
                    "Reviewer",
                    "QaEngineer",
                    "DocumentationSpecialist",
                    "GitIntegrator"
                ]
        else:
            # Standard workflow
            if use_unified_roles:
                if use_task_decomposer:
                    if use_reviewer:
                        self.roles = {
                            "AnalystArchitect": AnalystArchitect(),
                            "TaskDecomposer": TaskDecomposer(),
                            "DeveloperEngineer": DeveloperEngineer(),
                            "Reviewer": Reviewer(),
                            "TesterQa": TesterQa()
                        }
                        self.workflow = [
                            "AnalystArchitect",
                            "TaskDecomposer",
                            "DeveloperEngineer",
                            "Reviewer",
                            "TesterQa"
                        ]
                    else:
                        self.roles = {
                            "AnalystArchitect": AnalystArchitect(),
                            "TaskDecomposer": TaskDecomposer(),
                            "DeveloperEngineer": DeveloperEngineer(),
                            "TesterQa": TesterQa()
                        }
                        self.workflow = [
                            "AnalystArchitect",
                            "TaskDecomposer",
                            "DeveloperEngineer",
                            "TesterQa"
                        ]
                else:
                    if use_reviewer:
                        self.roles = {
                            "AnalystArchitect": AnalystArchitect(),
                            "DeveloperEngineer": DeveloperEngineer(),
                            "Reviewer": Reviewer(),
                            "TesterQa": TesterQa()
                        }
                        self.workflow = [
                            "AnalystArchitect",
                            "DeveloperEngineer",
                            "Reviewer",
                            "TesterQa"
                        ]
                    else:
                        self.roles = {
                            "AnalystArchitect": AnalystArchitect(),
                            "DeveloperEngineer": DeveloperEngineer(),
                            "TesterQa": TesterQa()
                        }
                        self.workflow = [
                            "AnalystArchitect",
                            "DeveloperEngineer",
                            "TesterQa"
                        ]
            else:
                if use_task_decomposer:
                    if use_reviewer:
                        self.roles = {
                            "ProductManager": ProductManager(),
                            "Architect": Architect(),
                            "TaskDecomposer": TaskDecomposer(),
                            "Engineer": Engineer(),
                            "Reviewer": Reviewer(),
                            "QaEngineer": QaEngineer()
                        }
                        self.workflow = [
                            "ProductManager",
                            "Architect",
                            "TaskDecomposer",
                            "Engineer",
                            "Reviewer",
                            "QaEngineer"
                        ]
                    else:
                        self.roles = {
                            "ProductManager": ProductManager(),
                            "Architect": Architect(),
                            "TaskDecomposer": TaskDecomposer(),
                            "Engineer": Engineer(),
                            "QaEngineer": QaEngineer()
                        }
                        self.workflow = [
                            "ProductManager",
                            "Architect",
                            "TaskDecomposer",
                            "Engineer",
                            "QaEngineer"
                        ]
                else:
                    if use_reviewer:
                        self.roles = {
                            "ProductManager": ProductManager(),
                            "Architect": Architect(),
                            "Engineer": Engineer(),
                            "Reviewer": Reviewer(),
                            "QaEngineer": QaEngineer()
                        }
                        self.workflow = [
                            "ProductManager",
                            "Architect",
                            "Engineer",
                            "Reviewer",
                            "QaEngineer"
                        ]
                    else:
                        self.roles = {
                            "ProductManager": ProductManager(),
                            "Architect": Architect(),
                            "Engineer": Engineer(),
                            "QaEngineer": QaEngineer()
                        }
                        self.workflow = [
                            "ProductManager",
                            "Architect",
                            "Engineer",
                            "QaEngineer"
                        ]

        self.context = {}

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
            if next_role and next_role != role_name:
                # Find the next role in workflow
                try:
                    current_index = self.workflow.index(role_name)
                    next_index = self.workflow.index(next_role)
                    if next_index < current_index:
                        # If next role is before current, we're looping back
                        break
                except ValueError:
                    # Next role not found, continue to next in sequence
                    pass

        return self.context

    def get_role(self, role_name: str) -> BaseRole:
        """Get a specific role by name"""
        return self.roles.get(role_name)

    def add_role(self, role: BaseRole):
        """Add a custom role to the coordinator"""
        self.roles[role.name] = role
        if role.name not in self.workflow:
            self.workflow.append(role.name)

    def set_workflow(self, workflow: List[str]):
        """Set a custom workflow order"""
        self.workflow = workflow

async def main():
    # Example usage
    coordinator = RoleCoordinator()

    # Initial context with project requirements
    initial_context = {
        "requirements": "Create a web application with frontend, backend, and database"
    }

    # Run the complete workflow
    result = await coordinator.run_workflow(initial_context)

    print("Final result:")
    print(f"Requirement Analysis: {result.get('requirement_analysis')}")
    print(f"System Architecture: {result.get('system_architecture')}")
    print(f"Project Structure: {result.get('project_structure')}")
    print(f"Code Implementation: {list(result.get('code_implementation', {}).keys())}")
    print(f"Test Results: {result.get('test_results')}")
    print(f"QA Status: {result.get('qa_status')}")

if __name__ == "__main__":
    asyncio.run(main())


