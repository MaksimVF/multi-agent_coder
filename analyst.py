





import json
import re
from typing import List, Dict, Any, Optional
from base_llm_agent import BaseLLMAgent

class Analyst(BaseLLMAgent):
    """LLM-powered Analyst agent for task analysis and breakdown."""

    def __init__(self, temperature: float = 0.5):
        """Initialize the Analyst agent."""
        super().__init__(temperature=temperature)
        self.system_message = """You are an expert task analyst. Your job is to break down complex tasks into manageable subtasks with detailed analysis."""

    async def analyze_task(self, task_description: str) -> List[Dict[str, Any]]:
        """Analyze a task and break it down into subtasks using advanced AI/ML techniques."""
        print(f"🔍 Analyzing task with LLM: {task_description}")

        # Prepare enhanced prompt for LLM with AI/ML task analysis
        prompt = f"""Perform an advanced analysis of the following task using AI/ML techniques. Break it down into smaller, manageable subtasks with the following details:

1. Clear description of the subtask
2. Expected output or result
3. Dependencies on other subtasks
4. Estimated difficulty (easy, medium, hard)
5. Required technical skills or domains
6. Potential challenges or edge cases
7. Suggested approach or algorithm
8. Time estimate (low, medium, high)

Task: {task_description}

Return the analysis as valid JSON in the following format:
{{
    "analysis_summary": {{
        "task_complexity": "string",
        "main_domains": ["string"],
        "key_challenges": ["string"],
        "suggested_approach": "string"
    }},
    "subtasks": [
        {{
            "description": "string",
            "expected_output": "string",
            "dependencies": ["string"],
            "difficulty": "string",
            "required_skills": ["string"],
            "potential_challenges": ["string"],
            "suggested_approach": "string",
            "time_estimate": "string"
        }}
    ],
    "risk_assessment": {{
        "high_risk_areas": ["string"],
        "mitigation_strategies": ["string"]
    }}
}}"""

        # Call LLM to analyze the task
        try:
            llm_response = await self._call_llm(prompt)
            response_text = llm_response.get("content", "{}")

            # Try to parse the JSON response
            try:
                analysis = json.loads(response_text)
                subtasks = analysis.get("subtasks", [])

                # Store the full analysis for reference
                self.memory["last_analysis"] = analysis

                print(f"📋 Identified {len(subtasks)} subtasks from LLM:")
                for subtask in subtasks:
                    print(f"  - {subtask.get('description', 'Unknown')}")

                return subtasks
            except json.JSONDecodeError:
                print("⚠️  LLM response not valid JSON, falling back to manual parsing")
                # Fallback: Extract subtasks from text response with AI-enhanced parsing
                return await self._parse_subtasks_response(response_text, task_description)

        except Exception as e:
            print(f"Error calling LLM: {e}")
            # Fallback to AI-enhanced simple analysis
            return await self._create_fallback_subtasks(task_description)

    async def _parse_subtasks_response(self, response: str, task_description: str) -> List[Dict[str, Any]]:
        """Parse subtasks from LLM response when it's not valid JSON."""
        subtasks = []
        lines = response.split('\n')
        current_subtask = None
        current_section = None

        for line in lines:
            line = line.strip()

            # Detect new subtask
            if line.startswith("- ") or line.strip().isdigit() or "subtask" in line.lower():
                if current_subtask:
                    subtasks.append(current_subtask)
                current_subtask = {
                    "description": line.replace("- ", "").replace("subtask", "").strip(),
                    "expected_output": "",
                    "dependencies": [],
                    "difficulty": "medium",
                    "required_skills": [],
                    "potential_challenges": [],
                    "suggested_approach": "",
                    "time_estimate": "medium"
                }
                current_section = "description"

            # Parse different sections
            elif current_subtask:
                if line.lower().startswith(("output:", "result:")):
                    current_subtask["expected_output"] = line.replace("output:", "").replace("result:", "").strip()
                    current_section = "output"
                elif line.lower().startswith(("dep:", "depends:", "dependencies:")):
                    deps = line.replace("dep:", "").replace("depends:", "").replace("dependencies:", "").strip()
                    current_subtask["dependencies"] = [d.strip() for d in deps.split(",") if d.strip()]
                    current_section = "dependencies"
                elif line.lower().startswith(("diff:", "difficulty:")):
                    current_subtask["difficulty"] = line.replace("diff:", "").replace("difficulty:", "").strip().lower()
                    current_section = "difficulty"
                elif line.lower().startswith(("skills:", "required:", "expertise:")):
                    skills = line.replace("skills:", "").replace("required:", "").replace("expertise:", "").strip()
                    current_subtask["required_skills"] = [s.strip() for s in skills.split(",") if s.strip()]
                    current_section = "skills"
                elif line.lower().startswith(("challenges:", "risks:", "issues:")):
                    challenges = line.replace("challenges:", "").replace("risks:", "").replace("issues:", "").strip()
                    current_subtask["potential_challenges"] = [c.strip() for c in challenges.split(",") if c.strip()]
                    current_section = "challenges"
                elif line.lower().startswith(("approach:", "method:", "algorithm:")):
                    current_subtask["suggested_approach"] = line.replace("approach:", "").replace("method:", "").replace("algorithm:", "").strip()
                    current_section = "approach"
                elif line.lower().startswith(("time:", "estimate:", "effort:")):
                    current_subtask["time_estimate"] = line.replace("time:", "").replace("estimate:", "").replace("effort:", "").strip().lower()
                    current_section = "time"
                elif current_section and line:
                    # Continue the current section
                    if current_section == "description":
                        current_subtask["description"] += " " + line
                    elif current_section == "output":
                        current_subtask["expected_output"] += " " + line
                    elif current_section == "approach":
                        current_subtask["suggested_approach"] += " " + line

        if current_subtask:
            subtasks.append(current_subtask)

        # Add default subtasks if none were found
        if not subtasks:
            print("⚠️  No subtasks found in LLM response, using fallback")
            return await self._create_fallback_subtasks(task_description)

        return subtasks

    async def _create_fallback_subtasks(self, task_description: str) -> List[Dict[str, Any]]:
        """Create fallback subtasks using basic AI analysis."""
        # Use a simpler prompt for fallback
        prompt = f"""Break down this task into basic subtasks: {task_description}

        Provide a simple list of subtasks."""

        try:
            response = await self.generate_response(prompt, self.system_message)
            lines = response.split('\n')

            subtasks = []
            for line in lines:
                line = line.strip()
                if line and ('-' in line or '•' in line or '*' in line or line.strip().isdigit()):
                    # Extract subtask description
                    description = line.split('-', 1)[-1].split('•', 1)[-1].split('*', 1)[-1].strip()
                    description = re.sub(r'^\d+\.\s*', '', description)  # Remove numbering
                    if description:
                        subtasks.append({
                            "description": description,
                            "expected_output": "Completed subtask",
                            "dependencies": [],
                            "difficulty": "medium",
                            "required_skills": ["programming"],
                            "potential_challenges": ["implementation"],
                            "suggested_approach": "standard",
                            "time_estimate": "medium"
                        })

            # Add default subtasks if none were found
            if not subtasks:
                subtasks = [
                    {
                        "description": "function signature",
                        "expected_output": "Function definition",
                        "dependencies": [],
                        "difficulty": "easy",
                        "required_skills": ["programming"],
                        "potential_challenges": ["naming"],
                        "suggested_approach": "standard",
                        "time_estimate": "low"
                    },
                    {
                        "description": "function logic",
                        "expected_output": "Working implementation",
                        "dependencies": ["function signature"],
                        "difficulty": "medium",
                        "required_skills": ["programming", "algorithms"],
                        "potential_challenges": ["edge cases"],
                        "suggested_approach": "iterative",
                        "time_estimate": "medium"
                    },
                    {
                        "description": "input validation",
                        "expected_output": "Validated inputs",
                        "dependencies": ["function signature"],
                        "difficulty": "medium",
                        "required_skills": ["programming", "security"],
                        "potential_challenges": ["invalid inputs"],
                        "suggested_approach": "defensive",
                        "time_estimate": "medium"
                    },
                    {
                        "description": "unit tests",
                        "expected_output": "Test coverage",
                        "dependencies": ["function logic", "input validation"],
                        "difficulty": "medium",
                        "required_skills": ["testing"],
                        "potential_challenges": ["coverage"],
                        "suggested_approach": "tdd",
                        "time_estimate": "medium"
                    }
                ]

            return subtasks

        except Exception as e:
            print(f"Error in fallback analysis: {e}")
            # Ultimate fallback
            return [{
                "description": task_description,
                "expected_output": "Completed task",
                "dependencies": [],
                "difficulty": "medium",
                "required_skills": ["problem_solving", "programming"],
                "potential_challenges": ["task_ambiguity", "resource_limitation"],
                "suggested_approach": "iterative_development",
                "time_estimate": "medium"
            }]

    async def perform_ml_analysis(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform machine learning analysis on task data."""
        # This would be a placeholder for actual ML analysis
        # In a real implementation, this could use:
        # - Natural Language Processing (NLP) for task understanding
        # - Clustering algorithms for subtask identification
        # - Predictive models for difficulty estimation
        # - Graph analysis for dependency mapping

        print("🧠 Performing ML analysis on task data...")

        # For now, we'll simulate ML analysis using LLM
        prompt = f"""Perform machine learning analysis on the following task data:

{json.dumps(task_data, indent=2)}

Analyze:
1. Task sentiment and complexity
2. Key technical domains involved
3. Potential risk factors
4. Optimal development approach
5. Resource allocation recommendations

Return as valid JSON."""

        try:
            llm_response = await self._call_llm(prompt)
            response_text = llm_response.get("content", "{}")

            try:
                ml_analysis = json.loads(response_text)
                self.memory["ml_analysis"] = ml_analysis
                return ml_analysis
            except json.JSONDecodeError:
                print("⚠️  ML analysis response not valid JSON")
                return {
                    "sentiment": "neutral",
                    "complexity": "medium",
                    "domains": ["software_development", "ai_ml"],
                    "risk_factors": ["ambiguous_requirements"],
                    "recommended_approach": "agile_development",
                    "resource_allocation": "balanced"
                }

        except Exception as e:
            print(f"Error in ML analysis: {e}")
            return {
                "sentiment": "neutral",
                "complexity": "medium",
                "domains": ["software_development"],
                "risk_factors": ["unknown"],
                "recommended_approach": "standard",
                "resource_allocation": "normal"
            }

    async def generate_task_embedding(self, task_description: str) -> List[float]:
        """Generate an embedding vector for the task description."""
        # This would be a placeholder for actual embedding generation
        # In a real implementation, this could use:
        # - Transformer models for text embedding
        # - Domain-specific embedding techniques
        # - Dimensionality reduction for visualization

        print("🎯 Generating task embedding...")

        # For now, we'll simulate embedding generation
        # In a real implementation, we'd call an embedding API or local model
        return [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

    async def identify_similar_tasks(self, task_embedding: List[float], threshold: float = 0.8) -> List[Dict[str, Any]]:
        """Identify similar tasks based on embedding similarity."""
        # This would be a placeholder for actual similarity search
        # In a real implementation, this could use:
        # - Vector databases for efficient similarity search
        # - Cosine similarity or other distance metrics
        # - Historical task data for comparison

        print("🔍 Identifying similar tasks...")

        # For now, we'll simulate similarity search
        return [
            {
                "task_id": "task_001",
                "description": "Create a Python function to calculate factorial",
                "similarity": 0.85,
                "outcome": "successful",
                "lessons_learned": ["use recursion carefully", "handle large numbers"]
            },
            {
                "task_id": "task_002",
                "description": "Implement a sorting algorithm in Python",
                "similarity": 0.78,
                "outcome": "successful",
                "lessons_learned": ["choose right algorithm", "optimize for edge cases"]
            }
        ]





