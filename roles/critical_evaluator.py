

import os
from typing import Dict, Any
from .base_role import BaseRole

class CriticalEvaluator(BaseRole):
    """Critical Evaluator role - provides critical assessment of decisions made by other agents"""

    def __init__(self, model: str = "gpt-4o", alternative_model: str = "claude-3-opus"):
        super().__init__(
            name="CriticalEvaluator",
            description="Critically evaluates architecture, technology, and code decisions",
            tools=["risk_analysis", "scenario_modeling", "alternative_generation"]
        )
        self.model = model
        self.alternative_model = alternative_model

    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute critical evaluation of current decisions"""
        evaluation_results = {}

        # Evaluate architecture if available
        if "system_architecture" in context:
            architecture = context["system_architecture"]
            evaluation_results["architecture_evaluation"] = await self._evaluate_architecture(architecture)

        # Evaluate technology stack if available
        if "tech_stack" in context:
            tech_stack = context["tech_stack"]
            evaluation_results["tech_stack_evaluation"] = await self._evaluate_tech_stack(tech_stack)

        # Evaluate code if available
        if "code_implementation" in context:
            implementation = context["code_implementation"]
            evaluation_results["code_evaluation"] = await self._evaluate_code(implementation)

        # Generate alternative scenarios
        evaluation_results["alternative_scenarios"] = await self._generate_alternative_scenarios(context)

        return {
            "critical_evaluation": evaluation_results,
            "recommendations": await self._generate_recommendations(evaluation_results)
        }

    async def _evaluate_architecture(self, architecture: Dict[str, Any]) -> Dict[str, Any]:
        """Critically evaluate system architecture"""
        # Use alternative LLM for different perspective
        evaluation = await self._analyze_with_alternative_model(
            f"Critically evaluate this architecture: {architecture}. "
            "Identify potential issues, scalability concerns, and maintenance challenges."
        )

        return {
            "evaluation": evaluation,
            "risk_level": self._assess_risk_level(evaluation)
        }

    async def _evaluate_tech_stack(self, tech_stack: Dict[str, Any]) -> Dict[str, Any]:
        """Critically evaluate technology stack"""
        evaluation = await self._analyze_with_alternative_model(
            f"Critically evaluate this technology stack: {tech_stack}. "
            "Identify potential compatibility issues, long-term support concerns, "
            "and community adoption challenges."
        )

        return {
            "evaluation": evaluation,
            "risk_level": self._assess_risk_level(evaluation)
        }

    async def _evaluate_code(self, implementation: Dict[str, str]) -> Dict[str, Any]:
        """Critically evaluate code implementation"""
        # Sample code for evaluation
        code_sample = "\n".join(list(implementation.values())[:3])  # First 3 files

        evaluation = await self._analyze_with_alternative_model(
            f"Critically evaluate this code implementation: {code_sample}. "
            "Identify potential maintainability issues, performance bottlenecks, "
            "and security vulnerabilities."
        )

        return {
            "evaluation": evaluation,
            "risk_level": self._assess_risk_level(evaluation)
        }

    async def _generate_alternative_scenarios(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate alternative scenarios and their potential outcomes"""
        scenarios = []

        # Scenario 1: High load
        if "system_architecture" in context:
            scenarios.append({
                "name": "high_load_scenario",
                "description": "What happens if the system experiences 10x the expected load?",
                "analysis": await self._analyze_with_alternative_model(
                    "Analyze what would happen if the system experiences 10x the expected load. "
                    "Identify potential bottlenecks and failure points."
                )
            })

        # Scenario 2: Technology obsolescence
        if "tech_stack" in context:
            scenarios.append({
                "name": "obsolescence_scenario",
                "description": "What if a key technology becomes obsolete in 2 years?",
                "analysis": await self._analyze_with_alternative_model(
                    "Analyze the impact if a key technology in the stack becomes obsolete in 2 years. "
                    "What would be the migration challenges?"
                )
            })

        return {"scenarios": scenarios}

    async def _generate_recommendations(self, evaluations: Dict[str, Any]) -> Dict[str, Any]:
        """Generate recommendations based on evaluations"""
        recommendations = []

        # Analyze all evaluations
        for evaluation_type, evaluation in evaluations.items():
            if "risk_level" in evaluation and evaluation["risk_level"] > 2:  # Medium or higher risk
                recommendations.append({
                    "area": evaluation_type.replace("_evaluation", ""),
                    "issue": evaluation["evaluation"],
                    "recommendation": await self._analyze_with_alternative_model(
                        f"Based on this issue: {evaluation['evaluation']}, "
                        "provide specific recommendations for improvement."
                    )
                })

        return {"recommendations": recommendations}

    def _assess_risk_level(self, evaluation: str) -> int:
        """Assess risk level based on evaluation text"""
        # Simple heuristic for risk assessment
        risk_keywords = ["critical", "major", "severe", "high risk", "significant"]
        medium_keywords = ["moderate", "concern", "potential", "medium risk"]

        evaluation_lower = evaluation.lower()
        if any(keyword in evaluation_lower for keyword in risk_keywords):
            return 3  # High risk
        elif any(keyword in evaluation_lower for keyword in medium_keywords):
            return 2  # Medium risk
        else:
            return 1  # Low risk

    async def _analyze_with_alternative_model(self, prompt: str) -> str:
        """Analyze using alternative LLM model"""
        # In a real implementation, this would use a different LLM API
        # For now, we'll simulate with a simple response
        return f"[Alternative Model Analysis]: {prompt}\n\n" \
               "This is a simulated critical evaluation. In a real implementation, " \
               "this would use {self.alternative_model} to provide an alternative perspective."

