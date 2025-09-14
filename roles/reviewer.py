







import json
from typing import Dict, Any, List, Tuple
from .base_role import BaseRole

class Reviewer(BaseRole):
    """Reviewer role - performs code review and generates feedback"""

    def __init__(self):
        super().__init__(
            name="Reviewer",
            description="Performs code review and generates feedback",
            tools=["static_analysis", "style_checker", "code_quality_analyzer"]
        )

    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Perform code review"""
        # Get code implementation from context
        implementation = context.get("code_implementation", {})

        # Perform code review
        review_results = await self._review_code(implementation)

        # Generate review documentation
        review_doc = await self._generate_review_documentation(review_results)

        return {
            "code_review": review_results,
            "review_documentation": review_doc,
            "next_role": "QaEngineer" if "QaEngineer" in context.get("workflow", []) else None
        }

    async def _review_code(self, implementation: Dict[str, str]) -> Dict[str, Any]:
        """Review implemented code"""
        review_results = {
            "files_reviewed": [],
            "issues_found": 0,
            "suggestions": [],
            "quality_score": 0.0,
            "file_reviews": {}
        }

        # Review each file
        for filename, code in implementation.items():
            file_review = await self._review_file(filename, code)
            review_results["files_reviewed"].append(filename)
            review_results["issues_found"] += len(file_review["issues"])
            review_results["suggestions"].extend(file_review["suggestions"])
            review_results["file_reviews"][filename] = file_review

        # Calculate quality score (simple metric)
        total_files = len(implementation)
        if total_files > 0:
            review_results["quality_score"] = max(0, 10 - review_results["issues_found"] / total_files)

        return review_results

    async def _review_file(self, filename: str, code: str) -> Dict[str, Any]:
        """Review a single file"""
        # This would use LLM for actual code analysis
        # For now, return a simple review structure
        issues = []
        suggestions = []

        # Basic checks
        if filename.endswith(".py"):
            # Check for missing docstrings
            if '"""' not in code and "'''" not in code:
                issues.append("Missing docstring")

            # Check for long lines
            lines = code.split('\n')
            for i, line in enumerate(lines, 1):
                if len(line) > 100:
                    issues.append(f"Line {i} exceeds 100 characters")

            # Suggestions
            if "def " in code and "->" not in code:
                suggestions.append("Add type hints to function definitions")

            if "import " in code and "from " not in code:
                suggestions.append("Consider using 'from module import function' for better readability")

        return {
            "issues": issues,
            "suggestions": suggestions,
            "score": max(0, 10 - len(issues))
        }

    async def _generate_review_documentation(self, review_results: Dict[str, Any]) -> str:
        """Generate code review documentation"""
        doc = "# Code Review Report\n\n"

        # Summary
        doc += f"## Summary\n"
        doc += f"- Files reviewed: {len(review_results['files_reviewed'])}\n"
        doc += f"- Issues found: {review_results['issues_found']}\n"
        doc += f"- Quality score: {review_results['quality_score']:.1f}/10\n\n"

        # Detailed review
        for filename, file_review in review_results['file_reviews'].items():
            doc += f"## {filename}\n"
            doc += f"- Score: {file_review['score']}/10\n"

            if file_review['issues']:
                doc += "### Issues\n"
                for issue in file_review['issues']:
                    doc += f"- {issue}\n"

            if file_review['suggestions']:
                doc += "### Suggestions\n"
                for suggestion in file_review['suggestions']:
                    doc += f"- {suggestion}\n"

            doc += "\n"

        return doc

    async def generate_review_comments(self, code: str) -> List[str]:
        """Generate review comments for code"""
        # This would use LLM to generate meaningful comments
        # For now, return some basic comments
        comments = []

        if '"""' not in code and "'''" not in code:
            comments.append("Please add docstring to explain the purpose of this code.")

        if "def " in code and "->" not in code:
            comments.append("Consider adding type hints to function definitions for better maintainability.")

        if "import " in code and "from " not in code:
            comments.append("Consider using 'from module import function' syntax for better readability.")

        return comments




