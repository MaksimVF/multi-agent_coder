

"""LLM-based security analyzer."""

import asyncio
from typing import Optional

from base_llm_agent import BaseLLMAgent
from . import SecurityRisk, SecurityAnalyzer, BasicSecurityAnalyzer

class LLMSecurityAnalyzer(SecurityAnalyzer):
    """Security analyzer that uses LLM to assess security risks."""

    def __init__(self, model: str = "gpt-4o", temperature: float = 0.3):
        """Initialize the LLM security analyzer."""
        self.model = model
        self.temperature = temperature
        self.llm_agent = BaseLLMAgent(model=model, temperature=temperature)

    async def analyze_action(self, action):
        """Analyze an action using LLM for security risks."""
        try:
            # Prepare a description of the action
            action_description = self._get_action_description(action)

            # Create a prompt for security analysis
            prompt = f"""
            Analyze the following action for security risks:

            Action: {action_description}

            Evaluate the security risk level (LOW, MEDIUM, HIGH) based on:
            1. Potential for data loss or corruption
            2. Potential for privilege escalation
            3. Potential for information disclosure
            4. Potential for system compromise
            5. Potential for denial of service

            Respond with a single word: LOW, MEDIUM, or HIGH.
            """

            # Get LLM response
            response = await self.llm_agent.generate_response(prompt)
            risk_level = response.strip().upper()

            # Map response to SecurityRisk enum
            if risk_level == "HIGH":
                return SecurityRisk.HIGH
            elif risk_level == "MEDIUM":
                return SecurityRisk.MEDIUM
            else:
                return SecurityRisk.LOW

        except Exception as e:
            print(f"Error in LLM security analysis: {e}")
            return SecurityRisk.UNKNOWN

    def _get_action_description(self, action):
        """Get a textual description of an action."""
        description = f"Action type: {action.__class__.__name__}\n"

        # Add action-specific details
        if hasattr(action, 'command'):
            description += f"Command: {getattr(action, 'command', '')}\n"
        if hasattr(action, 'code'):
            description += f"Code: {getattr(action, 'code', '')}\n"
        if hasattr(action, 'path'):
            description += f"Path: {getattr(action, 'path', '')}\n"
        if hasattr(action, 'content'):
            description += f"Content: {getattr(action, 'content', '')}\n"
        if hasattr(action, 'thought'):
            description += f"Thought: {getattr(action, 'thought', '')}\n"

        return description

class HybridSecurityAnalyzer(SecurityAnalyzer):
    """Hybrid security analyzer that combines basic and LLM analysis."""

    def __init__(self, model: str = "gpt-4o", temperature: float = 0.3):
        """Initialize the hybrid security analyzer."""
        self.basic_analyzer = BasicSecurityAnalyzer()
        self.llm_analyzer = LLMSecurityAnalyzer(model=model, temperature=temperature)

    async def analyze_action(self, action):
        """Analyze an action using both basic and LLM analysis."""
        # First, get basic analysis
        basic_risk = await self.basic_analyzer.analyze_action(action)

        # If basic analysis shows HIGH risk, return immediately
        if basic_risk == SecurityRisk.HIGH:
            return basic_risk

        # If basic analysis shows MEDIUM risk, use LLM for confirmation
        if basic_risk == SecurityRisk.MEDIUM:
            llm_risk = await self.llm_analyzer.analyze_action(action)
            # Return the higher of the two risks
            return max(basic_risk, llm_risk)

        # For LOW or UNKNOWN, use LLM analysis
        llm_risk = await self.llm_analyzer.analyze_action(action)
        return llm_risk

