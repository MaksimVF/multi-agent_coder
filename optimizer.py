





import os
from typing import Dict, Any, List, Optional
import json
import asyncio

# Import LiteLLM for LLM integration
try:
    import litellm
    from litellm import completion
except ImportError:
    print("Warning: litellm not installed. Please install with 'pip install litellm'")

# Import base agent class
try:
    from base_llm_agent import BaseLLMAgent
except ImportError:
    print("Warning: base_llm_agent not found. Please check the file exists.")
    class BaseLLMAgent:
        pass

class Optimizer(BaseLLMAgent):
    """
    Optimizer Agent for code optimization and enhancement with Weaviate integration.

    Features:
    - Code optimization using LLM
    - Performance improvement
    - Code quality enhancement
    - Best practice implementation
    - Weaviate knowledge base integration
    - Historical optimization patterns
    """

    def __init__(
        self,
        model: str = "gpt-4o",
        temperature: float = 0.5,
        memory_manager: Optional["MemoryManager"] = None,
    ):
        """
        Initialize the LLM-powered Optimizer.

        Args:
            model: LLM model to use
            temperature: Creativity level for LLM
            memory_manager: Memory manager for Weaviate integration
        """
        super().__init__(model=model, temperature=temperature, memory_manager=memory_manager)

    async def optimize_code(self, code_data: Dict) -> Dict:
        """
        Optimize code using LLM and Weaviate knowledge base.

        Args:
            code_data: Code data to optimize

        Returns:
            Optimized code data
        """
        # Check Weaviate for similar code patterns
        similar_patterns = []
        if self.memory_manager:
            similar_patterns = self._find_similar_patterns(code_data.get("code", ""))

        # Build prompt with similar patterns
        prompt = f"""Optimize the following code for better performance, readability, and maintainability:

Original Code:
{code_data.get('code', '')}

{'Similar patterns found in knowledge base:' if similar_patterns else ''}
{''.join(f'Pattern {i+1}:\n{p["content"]}\n\n' for i, p in enumerate(similar_patterns))}

Provide the optimized version with explanations of the improvements made."""

        result = await self._call_llm(prompt)

        if result.get("success", False):
            optimized_code = {
                "original_code": code_data.get("code", ""),
                "optimized_code": result["response"],
                "improvements": self._extract_improvements(result["response"]),
                "description": code_data.get("description", ""),
                "similar_patterns_used": [p["content"] for p in similar_patterns],
            }

            # Store optimization result in Weaviate
            if self.memory_manager:
                self.memory_manager.store_long_term(
                    code_data.get("code", ""),
                    metadata={
                        "optimized_version": result["response"],
                        "improvements": optimized_code["improvements"],
                        "description": code_data.get("description", ""),
                        "type": "code_optimization",
                    },
                    agent="optimizer",
                    task_id=code_data.get("task_id", "unknown"),
                    importance=0.8,
                )

            return optimized_code
        else:
            return {
                "original_code": code_data.get("code", ""),
                "optimized_code": code_data.get("code", ""),
                "improvements": ["No improvements could be made"],
                "description": code_data.get("description", ""),
                "error": result.get("error", "Unknown error"),
            }

    def _find_similar_patterns(self, code: str, limit: int = 3) -> List[Dict]:
        """Find similar code patterns in Weaviate."""
        if not self.memory_manager:
            return []

        # Use semantic search to find similar patterns
        return self.memory_manager.retrieve_long_term(
            code,
            limit=limit,
            agent="optimizer",
        )

    def _extract_improvements(self, response: str) -> List[str]:
        """Extract improvement explanations from LLM response."""
        lines = response.split('\n')
        improvements = []

        # Look for lines that start with improvement indicators
        for line in lines:
            if any(
                line.lower().startswith(prefix)
                for prefix in [
                    "- ", "* ", "• ", "improvement:", "optimization:", "change:", "enhancement:"
                ]
            ):
                improvements.append(line.strip())

        return improvements if improvements else ["General code quality improvements"]

    async def review_code_quality(self, code_data: Dict) -> Dict:
        """
        Review code quality and provide suggestions using Weaviate knowledge.

        Args:
            code_data: Code data to review

        Returns:
            Code quality review
        """
        # Get historical reviews for similar code
        historical_reviews = []
        if self.memory_manager:
            historical_reviews = self.memory_manager.retrieve_long_term(
                code_data.get("code", ""),
                limit=2,
                agent="optimizer",
            )

        prompt = f"""Review the following code for quality, performance, and best practices:

Code to Review:
{code_data.get('code', '')}

{'Historical reviews for similar code:' if historical_reviews else ''}
{''.join(f'Review {i+1}:\n{r["content"]}\n\n' for i, r in enumerate(historical_reviews))}

Provide a detailed analysis including:
1. Code quality score (1-10)
2. Performance analysis
3. Best practice compliance
4. Specific improvement suggestions"""

        result = await self._call_llm(prompt)

        if result.get("success", False):
            review_data = {
                "code": code_data.get("code", ""),
                "review": result["response"],
                "score": self._extract_score(result["response"]),
                "description": code_data.get("description", ""),
                "historical_references": [r["content"] for r in historical_reviews],
            }

            # Store review in Weaviate
            if self.memory_manager:
                self.memory_manager.store_long_term(
                    result["response"],
                    metadata={
                        "code": code_data.get("code", ""),
                        "score": review_data["score"],
                        "description": code_data.get("description", ""),
                        "type": "code_review",
                    },
                    agent="optimizer",
                    task_id=code_data.get("task_id", "unknown"),
                    importance=0.7,
                )

            return review_data
        else:
            return {
                "code": code_data.get("code", ""),
                "review": "Could not complete review",
                "score": 5,
                "description": code_data.get("description", ""),
                "error": result.get("error", "Unknown error"),
            }

    def _extract_score(self, response: str) -> int:
        """Extract quality score from review response."""
        import re
        match = re.search(r'quality score[:\s]*(\d+)', response.lower())
        if match:
            try:
                return int(match.group(1))
            except ValueError:
                pass
        return 5  # Default score

    async def generate_best_practices(self, language: str = "python") -> List[str]:
        """
        Generate best practices for a programming language using Weaviate knowledge.

        Args:
            language: Programming language

        Returns:
            List of best practices
        """
        # Check Weaviate for existing best practices
        existing_practices = []
        if self.memory_manager:
            existing_practices = self.memory_manager.retrieve_long_term(
                f"{language} best practices",
                limit=5,
                agent="optimizer",
            )

        if existing_practices:
            return [p["content"] for p in existing_practices]

        # Generate new best practices if not found in Weaviate
        prompt = f"""Provide the top 10 best practices for {language} programming:

1. [Best practice 1]
2. [Best practice 2]
...
10. [Best practice 10]"""

        result = await self._call_llm(prompt)

        if result.get("success", False):
            lines = result["response"].split('\n')
            practices = []
            for line in lines:
                if line.strip() and not line.lower().startswith(('provide', 'best practices', 'top 10')):
                    practices.append(line.strip())

            # Store new practices in Weaviate
            if self.memory_manager and practices:
                for i, practice in enumerate(practices[:10], 1):
                    self.memory_manager.store_long_term(
                        practice,
                        metadata={
                            "language": language,
                            "rank": i,
                            "type": "best_practice",
                        },
                        agent="optimizer",
                        task_id="best_practices",
                        importance=0.6,
                    )

            return practices[:10]
        else:
            return ["Write clean, readable code",
                   "Use meaningful variable names",
                   "Follow PEP 8 guidelines for Python",
                   "Write unit tests",
                   "Handle exceptions properly"]

    async def optimize_with_knowledge_base(self, code_data: Dict) -> Dict:
        """
        Optimize code using patterns from the Weaviate knowledge base.

        Args:
            code_data: Code data to optimize

        Returns:
            Optimized code with knowledge base references
        """
        if not self.memory_manager:
            return await self.optimize_code(code_data)

        # Find optimization patterns in Weaviate
        patterns = self.memory_manager.retrieve_long_term(
            f"optimization patterns for {code_data.get('description', 'code')}",
            limit=5,
            agent="optimizer",
        )

        if not patterns:
            return await self.optimize_code(code_data)

        prompt = f"""Optimize the following code using these proven optimization patterns:

Original Code:
{code_data.get('code', '')}

Optimization Patterns:
{''.join(f'Pattern {i+1}:\n{p["content"]}\n\n' for i, p in enumerate(patterns))}

Apply the most relevant patterns and provide the optimized code."""

        result = await self._call_llm(prompt)

        if result.get("success", False):
            return {
                "original_code": code_data.get("code", ""),
                "optimized_code": result["response"],
                "patterns_used": [p["content"] for p in patterns],
                "description": code_data.get("description", ""),
            }
        else:
            return {
                "original_code": code_data.get("code", ""),
                "optimized_code": code_data.get("code", ""),
                "patterns_used": [],
                "description": code_data.get("description", ""),
                "error": result.get("error", "Unknown error"),
            }




