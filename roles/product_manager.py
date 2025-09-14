



from typing import Dict, Any
from .base_role import BaseRole

class ProductManager(BaseRole):
    """Product Manager role - responsible for requirement analysis and documentation"""

    def __init__(self):
        super().__init__(
            name="ProductManager",
            description="Analyzes requirements and creates project documentation",
            tools=["requirement_analysis", "document_generation"]
        )

    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze requirements and generate project documentation"""
        # Extract requirements from context
        requirements = context.get("requirements", "")

        # Analyze requirements
        analysis = await self._analyze_requirements(requirements)

        # Generate PRD (Product Requirements Document)
        prd = await self._generate_prd(analysis)

        # Update context with results
        result = {
            "requirement_analysis": analysis,
            "prd": prd,
            "next_role": "Architect"
        }

        return result

    async def _analyze_requirements(self, requirements: str) -> Dict[str, Any]:
        """Analyze project requirements"""
        # This would use LLM to analyze requirements
        # For now, return a simple structure
        return {
            "functional_requirements": ["Main features", "User interface"],
            "non_functional_requirements": ["Performance", "Security"],
            "constraints": ["Technology stack", "Deadlines"]
        }

    async def _generate_prd(self, analysis: Dict[str, Any]) -> str:
        """Generate Product Requirements Document"""
        # This would use LLM to generate a proper PRD
        # For now, return a simple template
        return f"""
# Product Requirements Document

## Functional Requirements
{''.join(f"- {req}\n" for req in analysis['functional_requirements'])}

## Non-Functional Requirements
{''.join(f"- {req}\n" for req in analysis['non_functional_requirements'])}

## Constraints
{''.join(f"- {constraint}\n" for constraint in analysis['constraints'])}
"""


