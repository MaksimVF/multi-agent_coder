


import json
import re
from typing import List, Dict, Any
from base_llm_agent import BaseLLMAgent

class Analyst(BaseLLMAgent):
    """LLM-powered Analyst agent for task analysis."""

    def __init__(self, model: str = "gpt-4o", temperature: float = 0.5):
        """
        Initialize the LLM-powered Analyst.

        Args:
            model: LLM model to use
            temperature: Creativity level for LLM
        """
        super().__init__(model=model, temperature=temperature)

        # Analyst-specific configuration
        self.system_message = (
            "You are an expert software analyst. Your job is to analyze coding tasks, "
            "break them down into subtasks, and provide insights about requirements and code quality."
        )

    async def analyze_task(self, task_description: str) -> List[Dict[str, str]]:
        """Analyze a task and break it down into subtasks using LLM."""
        print(f"🔍 Analyzing task with LLM: {task_description}")

        prompt = f"""
        Analyze the following coding task and break it down into logical subtasks:

        Task: {task_description}

        Provide the subtasks as a JSON list with each subtask having a 'description' field.
        Consider the programming language, main functionality, and any specific requirements.
        """

        # Call LLM to analyze the task
        response = await self.generate_response(prompt, self.system_message)

        try:
            # Try to parse the response as JSON
            subtasks = json.loads(response)
            print(f"📋 Identified {len(subtasks)} subtasks from LLM:")
            for subtask in subtasks:
                print(f"  - {subtask.get('description', 'Unknown')}")
            return subtasks
        except json.JSONDecodeError:
            print("⚠️  LLM response not valid JSON, falling back to manual parsing")
            # Fallback: parse the response manually
            return self._parse_subtasks_response(response)

    def _parse_subtasks_response(self, response: str) -> List[Dict[str, str]]:
        """Parse subtasks from LLM response when it's not valid JSON."""
        subtasks = []
        lines = response.split('\n')

        for line in lines:
            line = line.strip()
            if line and ('-' in line or '•' in line or '*' in line or line.strip().isdigit()):
                # Extract subtask description
                description = line.split('-', 1)[-1].split('•', 1)[-1].split('*', 1)[-1].strip()
                description = re.sub(r'^\d+\.\s*', '', description)  # Remove numbering
                if description:
                    subtasks.append({"description": description})

        # Add default subtasks if none were found
        if not subtasks:
            print("⚠️  No subtasks found in LLM response, using fallback")
            subtasks = [
                {"description": "function signature"},
                {"description": "function logic"},
                {"description": "input validation"},
                {"description": "unit tests"}
            ]

        return subtasks

    async def analyze_requirements(self, requirements: str) -> Dict[str, Any]:
        """Analyze requirements using LLM."""
        prompt = f"""
        Analyze the following software requirements and extract key information:

        Requirements: {requirements}

        Provide the analysis as a JSON object with these fields:
        - language: The programming language
        - main_functionality: The main feature or function to implement
        - constraints: List of any constraints or requirements
        - dependencies: List of any dependencies or libraries needed
        """

        response = await self.generate_response(prompt, self.system_message)

        try:
            analysis = json.loads(response)
            return analysis
        except json.JSONDecodeError:
            # Fallback to simple analysis
            return self._simple_requirements_analysis(requirements)

    def _simple_requirements_analysis(self, requirements: str) -> Dict[str, Any]:
        """Fallback requirements analysis when LLM response is invalid."""
        analysis = {
            "language": "unknown",
            "main_functionality": "unknown",
            "constraints": [],
            "dependencies": []
        }

        # Try to identify language
        requirements_lower = requirements.lower()
        if "python" in requirements_lower:
            analysis["language"] = "python"
        elif "javascript" in requirements_lower or "js" in requirements_lower:
            analysis["language"] = "javascript"
        elif "java" in requirements_lower:
            analysis["language"] = "java"
        elif "c#" in requirements_lower or "csharp" in requirements_lower:
            analysis["language"] = "csharp"

        return analysis

    async def analyze_code_quality(self, code: str) -> Dict[str, Any]:
        """Analyze code quality using LLM."""
        prompt = f"""
        Analyze the following code for quality, readability, maintainability, and performance.
        Provide suggestions for improvement.

        Code:
        {code}

        Provide the analysis as a JSON object with these fields:
        - readability: 'good', 'average', or 'needs improvement'
        - maintainability: 'good', 'average', or 'needs improvement'
        - performance: 'good', 'average', or 'needs improvement'
        - suggestions: List of improvement suggestions
        """

        response = await self.generate_response(prompt, self.system_message)

        try:
            analysis = json.loads(response)
            return analysis
        except json.JSONDecodeError:
            # Fallback to simple analysis
            return self._simple_code_quality_analysis(code)

    def _simple_code_quality_analysis(self, code: str) -> Dict[str, Any]:
        """Fallback code quality analysis."""
        analysis = {
            "readability": "average",
            "maintainability": "average",
            "performance": "average",
            "suggestions": ["Consider adding more comments", "Review variable naming"]
        }
        return analysis

    async def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process incoming data for the workflow."""
        task_description = data.get("task_description", "")

        if task_description:
            subtasks = await self.analyze_task(task_description)
            return {"subtasks": subtasks}
        else:
            return {"error": "No task description provided"}


    def _analyze_function_task(self, task_description):
        """Analyze a function-related task."""
        subtasks = [
            {"id": 1, "description": "Define function signature and parameters"},
            {"id": 2, "description": "Implement core function logic"},
            {"id": 3, "description": "Add input validation and error handling"},
            {"id": 4, "description": "Write comprehensive docstring with examples"},
            {"id": 5, "description": "Add type hints and annotations"}
        ]

        # Add specific subtasks based on function type
        if "math" in task_description or "calculate" in task_description:
            subtasks.insert(2, {"id": 2.5, "description": "Implement mathematical formula"})
        elif "file" in task_description or "io" in task_description:
            subtasks.insert(2, {"id": 2.5, "description": "Handle file operations safely"})
        elif "network" in task_description or "api" in task_description:
            subtasks.insert(2, {"id": 2.5, "description": "Implement network communication"})

        return subtasks

    def _analyze_class_task(self, task_description):
        """Analyze a class-related task."""
        subtasks = [
            {"id": 1, "description": "Define class structure and inheritance"},
            {"id": 2, "description": "Implement core methods"},
            {"id": 3, "description": "Add properties with getters/setters"},
            {"id": 4, "description": "Implement __init__ and __str__ methods"},
            {"id": 5, "description": "Write class-level docstring"},
            {"id": 6, "description": "Add type hints and annotations"}
        ]

        # Add specific subtasks based on class type
        if "database" in task_description or "model" in task_description:
            subtasks.insert(2, {"id": 2.5, "description": "Implement database integration"})
        elif "ui" in task_description or "interface" in task_description:
            subtasks.insert(2, {"id": 2.5, "description": "Design user interface elements"})
        elif "manager" in task_description or "controller" in task_description:
            subtasks.insert(2, {"id": 2.5, "description": "Implement control logic"})

        return subtasks

    def _analyze_algorithm_task(self, task_description):
        """Analyze an algorithm-related task."""
        return [
            {"id": 1, "description": "Define algorithm requirements"},
            {"id": 2, "description": "Design algorithm structure"},
            {"id": 3, "description": "Implement core algorithm logic"},
            {"id": 4, "description": "Add edge case handling"},
            {"id": 5, "description": "Optimize algorithm performance"},
            {"id": 6, "description": "Write algorithm documentation"}
        ]

    def _analyze_api_task(self, task_description):
        """Analyze an API-related task."""
        return [
            {"id": 1, "description": "Define API endpoints"},
            {"id": 2, "description": "Design request/response format"},
            {"id": 3, "description": "Implement API handlers"},
            {"id": 4, "description": "Add authentication/authorization"},
            {"id": 5, "description": "Implement error handling"},
            {"id": 6, "description": "Write API documentation"}
        ]

    def _analyze_generic_task(self, task_description):
        """Analyze a generic task."""
        return [
            {"id": 1, "description": "Understand requirements"},
            {"id": 2, "description": "Design solution architecture"},
            {"id": 3, "description": "Implement core functionality"},
            {"id": 4, "description": "Add error handling and validation"},
            {"id": 5, "description": "Write documentation and comments"},
            {"id": 6, "description": "Test and debug solution"}
        ]



