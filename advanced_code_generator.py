


"""
Advanced Code Generation Module.

This module provides enhanced code generation capabilities that leverage LLM
more effectively by using dynamic prompts, context-aware generation, and
iterative refinement.
"""

import asyncio
import json
from typing import Dict, Any, List, Optional
from base_llm_agent import BaseLLMAgent

class AdvancedCodeGenerator(BaseLLMAgent):
    """
    Advanced code generator that uses LLM more effectively.

    Features:
    - Context-aware code generation
    - Iterative refinement
    - Dynamic prompt construction
    - Error recovery
    - Multi-language support
    """

    def __init__(
        self,
        temperature: float = 0.3,
        memory_manager: Optional["MemoryManager"] = None
    ):
        """Initialize the advanced code generator."""
        super().__init__(temperature=temperature, memory_manager=memory_manager)
        self.system_message = """You are an expert code generator. Your job is to generate high-quality, efficient code based on requirements. Follow best practices and use appropriate design patterns."""

    async def generate_code(
        self,
        requirements: Dict[str, Any],
        language: str = "python",
        context: Optional[Dict[str, Any]] = None,
        max_attempts: int = 3
    ) -> Dict[str, Any]:
        """
        Generate code with iterative refinement.

        Args:
            requirements: Code requirements
            language: Programming language
            context: Additional context
            max_attempts: Maximum refinement attempts

        Returns:
            Dictionary with generated code and metadata
        """
        context = context or {}
        current_attempt = 0
        last_error = None
        last_result = None

        while current_attempt < max_attempts:
            try:
                # Generate code with current context
                last_result = await self._generate_code_attempt(
                    requirements,
                    language,
                    context,
                    current_attempt
                )

                # Validate the generated code
                validation = await self._validate_code(last_result["code"], language)

                if validation["valid"]:
                    return {
                        "code": last_result["code"],
                        "metadata": last_result["metadata"],
                        "validation": validation,
                        "attempts": current_attempt + 1
                    }
                else:
                    # Add validation errors to context for next attempt
                    context["validation_errors"] = validation["errors"]
                    last_error = validation["errors"]
                    current_attempt += 1

            except Exception as e:
                print(f"Code generation error (attempt {current_attempt + 1}): {e}")
                context["error"] = str(e)
                last_error = str(e)
                current_attempt += 1

        # Return best effort if max attempts reached
        return {
            "code": last_result.get("code", "") if last_result else "",
            "metadata": last_result.get("metadata", {}) if last_result else {},
            "validation": {"valid": False, "errors": [last_error]},
            "attempts": current_attempt,
            "status": "partial_success"
        }

    async def _generate_code_attempt(
        self,
        requirements: Dict[str, Any],
        language: str,
        context: Dict[str, Any],
        attempt: int
    ) -> Dict[str, Any]:
        """Generate code with a single attempt."""
        # Build dynamic prompt based on context
        prompt = self._build_dynamic_prompt(requirements, language, context, attempt)

        # Generate code using LLM
        response = await self.generate_response(prompt, self.system_message)

        # Parse the response
        try:
            # Try to extract code from response
            code_block = self._extract_code_block(response, language)
            if not code_block:
                raise ValueError("No code block found in response")

            return {
                "code": code_block,
                "metadata": {
                    "requirements": requirements,
                    "language": language,
                    "context": context,
                    "attempt": attempt,
                    "prompt": prompt
                }
            }
        except Exception as e:
            print(f"Error parsing code response: {e}")
            raise

    def _build_dynamic_prompt(
        self,
        requirements: Dict[str, Any],
        language: str,
        context: Dict[str, Any],
        attempt: int
    ) -> str:
        """Build a dynamic prompt based on current context."""
        prompt_parts = []

        # Add attempt information
        if attempt > 0:
            prompt_parts.append(f"--- Attempt {attempt + 1} ---")

        # Add main requirements
        prompt_parts.append(f"Generate {language} code for the following requirements:")
        prompt_parts.append(json.dumps(requirements, indent=2))

        # Add context information
        if context:
            prompt_parts.append("\nAdditional context:")
            for key, value in context.items():
                if key == "validation_errors":
                    prompt_parts.append(f"- Previous validation errors: {value}")
                elif key == "error":
                    prompt_parts.append(f"- Previous error: {value}")
                else:
                    prompt_parts.append(f"- {key}: {value}")

        # Add language-specific instructions
        prompt_parts.append(f"\nFollow {language} best practices:")
        if language == "python":
            prompt_parts.append("- Use type hints")
            prompt_parts.append("- Follow PEP 8 style guide")
            prompt_parts.append("- Include docstrings")
            prompt_parts.append("- Handle edge cases")
        elif language == "javascript":
            prompt_parts.append("- Use async/await for I/O operations")
            prompt_parts.append("- Follow ES6+ standards")
            prompt_parts.append("- Include JSDoc comments")
            prompt_parts.append("- Handle promise rejections")

        # Add output format instructions
        prompt_parts.append("\nOutput format:")
        prompt_parts.append("Return only the code block, starting with:")
        prompt_parts.append(f"```{language}")
        prompt_parts.append("...your code here...")
        prompt_parts.append("```")

        return "\n".join(prompt_parts)

    def _extract_code_block(self, response: str, language: str) -> Optional[str]:
        """Extract code block from LLM response."""
        # Look for code block markers
        start_marker = f"```{language}"
        end_marker = "```"

        start_idx = response.find(start_marker)
        if start_idx == -1:
            return None

        end_idx = response.find(end_marker, start_idx + len(start_marker))
        if end_idx == -1:
            return None

        # Extract and clean the code
        code = response[start_idx + len(start_marker):end_idx].strip()
        return code

    async def _validate_code(self, code: str, language: str) -> Dict[str, Any]:
        """Validate generated code."""
        # Basic validation - can be extended with actual code analysis
        if not code.strip():
            return {"valid": False, "errors": ["Empty code generated"]}

        # For Python, we can do some basic syntax checking
        if language == "python":
            try:
                compile(code, "<string>", "exec")
                return {"valid": True, "errors": []}
            except SyntaxError as e:
                return {"valid": False, "errors": [f"Syntax error: {str(e)}"]}

        # For other languages, we'll do basic checks
        return {"valid": True, "errors": []}

    async def refine_code(
        self,
        code: str,
        feedback: Dict[str, Any],
        language: str = "python"
    ) -> Dict[str, Any]:
        """
        Refine existing code based on feedback.

        Args:
            code: Original code
            feedback: Feedback for refinement
            language: Programming language

        Returns:
            Refined code and metadata
        """
        prompt = f"""Refine the following {language} code based on the feedback provided:

Original code:
```{language}
{code}
```

Feedback:
{json.dumps(feedback, indent=2)}

Provide the refined code:
```{language}
...refined code here...
```
"""

        response = await self.generate_response(prompt, self.system_message)

        # Extract refined code
        refined_code = self._extract_code_block(response, language)

        if refined_code:
            return {
                "original": code,
                "refined": refined_code,
                "feedback": feedback
            }
        else:
            return {
                "original": code,
                "refined": code,  # Return original if extraction fails
                "feedback": feedback,
                "error": "Failed to extract refined code"
            }

    async def generate_unit_tests(
        self,
        code: str,
        requirements: Dict[str, Any],
        language: str = "python"
    ) -> Dict[str, Any]:
        """
        Generate unit tests for the given code.

        Args:
            code: Code to test
            requirements: Original requirements
            language: Programming language

        Returns:
            Generated tests and metadata
        """
        prompt = f"""Generate comprehensive unit tests for the following {language} code:

Code:
```{language}
{code}
```

Original requirements:
{json.dumps(requirements, indent=2)}

Provide the test code:
```{language}
...test code here...
```
"""

        response = await self.generate_response(prompt, self.system_message)
        tests = self._extract_code_block(response, language)

        return {
            "code": code,
            "tests": tests or "",
            "requirements": requirements
        }

    async def optimize_code(
        self,
        code: str,
        requirements: Dict[str, Any],
        language: str = "python"
    ) -> Dict[str, Any]:
        """
        Optimize existing code.

        Args:
            code: Code to optimize
            requirements: Original requirements
            language: Programming language

        Returns:
            Optimized code and metadata
        """
        prompt = f"""Optimize the following {language} code for performance and readability:

Code:
```{language}
{code}
```

Original requirements:
{json.dumps(requirements, indent=2)}

Provide the optimized code:
```{language}
...optimized code here...
```
"""

        response = await self.generate_response(prompt, self.system_message)
        optimized_code = self._extract_code_block(response, language)

        return {
            "original": code,
            "optimized": optimized_code or code,
            "requirements": requirements
        }

