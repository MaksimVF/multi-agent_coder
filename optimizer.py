



import json
import os
import datetime
from pathlib import Path
import re
import ast
import traceback
from typing import Dict, Any
from base_llm_agent import BaseLLMAgent

class Optimizer(BaseLLMAgent):


    """LLM-powered Optimizer agent for code analysis and improvement."""

    def __init__(self, model: str = "gpt-4o", temperature: float = 0.5):
        """
        Initialize the LLM-powered Optimizer.

        Args:
            model: LLM model to use
            temperature: Creativity level for LLM
        """
        super().__init__(model=model, temperature=temperature)

        # Optimizer-specific configuration
        self.system_message = (
            "You are an expert code optimizer. Your job is to analyze code, "
            "identify performance bottlenecks, and suggest improvements for "
            "readability, maintainability, and performance."
        )

        self.improvements_log = Path("improvements.log")
        self.history_log = Path("optimizer_history.json")
        self.researcher = None  # Will be set by main

        # Load history
        self.history = self._load_history()

    def _load_history(self):
        """Load optimization history."""
        if self.history_log.exists():
            try:
                with open(self.history_log, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}

    def _save_history(self):
        """Save optimization history."""
        try:
            with open(self.history_log, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save optimization history: {e}")

    def _log_improvement(self, improvement_type, details, code_sample=None):
        """Log an improvement suggestion."""
        try:
            timestamp = datetime.datetime.now().isoformat()
            entry = {
                "timestamp": timestamp,
                "type": improvement_type,
                "details": details,
                "code_sample": code_sample
            }

            with open(self.improvements_log, 'a', encoding='utf-8') as f:
                f.write(json.dumps(entry, indent=2) + "\n\n")

            # Also add to history
            if "history" not in self.history:
                self.history["history"] = []
            self.history["history"].append(entry)
            self._save_history()

        except Exception as e:
            print(f"Warning: Could not log improvement: {e}")

    async def analyze_and_optimize(self, task_description, code_data, test_results, language="python"):
        """Analyze the work of all agents and suggest optimizations."""
        try:
            print("🔍 Optimizer is analyzing the results...")

            # Analyze the task and results
            analysis = {
                "task": task_description,
                "language": language,
                "code_quality": self._analyze_code_quality(code_data),
                "test_results": self._analyze_test_results(test_results),
                "performance": self._analyze_performance(test_results),
                "security": self._analyze_security(test_results),
                "suggestions": []
            }

            # Generate suggestions
            suggestions = self._generate_suggestions(analysis)

            # Research additional improvements
            research_suggestions = await self._research_improvements(language, task_description)

            # Combine all suggestions
            all_suggestions = suggestions + research_suggestions

            # Log improvements
            for suggestion in all_suggestions:
                self._log_improvement(
                    suggestion["type"],
                    suggestion["details"],
                    suggestion.get("code", None)
                )

            # Return final analysis and suggestions
            analysis["suggestions"] = all_suggestions

            return {
                "success": True,
                "analysis": analysis,
                "suggestions": all_suggestions,
                "final_code": code_data["code"]
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "traceback": traceback.format_exc()
            }

    def _analyze_code_quality(self, code_data):
        """Analyze code quality."""
        try:
            code = code_data["code"]
            analysis = {
                "length": len(code),
                "lines": len(code.split('\n')),
                "functions": 0,
                "classes": 0,
                "comments": 0,
                "issues": []
            }

            # Count comments
            lines = code.split('\n')
            for line in lines:
                stripped = line.strip()
                if stripped.startswith('#'):
                    analysis["comments"] += 1
                elif stripped.startswith('//') and code_data.get("language", "python") in ["javascript", "java", "csharp"]:
                    analysis["comments"] += 1
                elif stripped.startswith('/*') and '*/' in stripped:
                    analysis["comments"] += 1

            # Parse Python code for functions and classes
            if code_data.get("language", "python") == "python":
                try:
                    tree = ast.parse(code)
                    for node in ast.walk(tree):
                        if isinstance(node, ast.FunctionDef):
                            analysis["functions"] += 1
                        elif isinstance(node, ast.ClassDef):
                            analysis["classes"] += 1
                except:
                    pass

            # Check for common code quality issues
            if "eval(" in code:
                analysis["issues"].append("Potential security issue: eval() usage detected")

            if "password" in code.lower() and ("=" in code or ":" in code):
                analysis["issues"].append("Potential security issue: hardcoded password detected")

            # Check for long functions (more than 50 lines)
            if analysis["functions"] > 0 and analysis["lines"] / analysis["functions"] > 50:
                analysis["issues"].append("Functions may be too long - consider refactoring")

            return analysis

        except Exception as e:
            return {
                "error": str(e),
                "issues": ["Could not analyze code quality"]
            }

    def _analyze_test_results(self, test_results):
        """Analyze test results."""
        try:
            analysis = {
                "total_tests": len(test_results),
                "passed": 0,
                "failed": 0,
                "test_types": {},
                "issues": []
            }

            for result in test_results:
                if result["passed"]:
                    analysis["passed"] += 1
                else:
                    analysis["failed"] += 1

                test_type = result.get("test_type", "basic")
                if test_type not in analysis["test_types"]:
                    analysis["test_types"][test_type] = {"passed": 0, "failed": 0}

                if result["passed"]:
                    analysis["test_types"][test_type]["passed"] += 1
                else:
                    analysis["test_types"][test_type]["failed"] += 1

            # Check for test result issues
            if analysis["failed"] > 0:
                analysis["issues"].append(f"{analysis['failed']} tests failed")

            # Check if all test types were used
            expected_types = ["basic", "unit", "integration", "performance", "coverage", "security"]
            missing_types = [t for t in expected_types if t not in analysis["test_types"]]
            if missing_types:
                analysis["issues"].append(f"Missing test types: {', '.join(missing_types)}")

            return analysis

        except Exception as e:
            return {
                "error": str(e),
                "issues": ["Could not analyze test results"]
            }

    def _analyze_performance(self, test_results):
        """Analyze performance metrics."""
        try:
            analysis = {
                "execution_time_ms": 0,
                "memory_usage_kb": 0,
                "issues": []
            }

            for result in test_results:
                if "performance" in result:
                    perf = result["performance"]
                    if "execution_time_ms" in perf:
                        analysis["execution_time_ms"] = max(analysis["execution_time_ms"], perf["execution_time_ms"])
                    if "memory_usage_kb" in perf:
                        analysis["memory_usage_kb"] = max(analysis["memory_usage_kb"], perf["memory_usage_kb"])

            # Check for performance issues
            if analysis["execution_time_ms"] > 1000:  # More than 1 second
                analysis["issues"].append("Slow execution - consider performance optimization")

            if analysis["memory_usage_kb"] > 10000:  # More than 10MB
                analysis["issues"].append("High memory usage - consider memory optimization")

            return analysis

        except Exception as e:
            return {
                "error": str(e),
                "issues": ["Could not analyze performance"]
            }

    def _analyze_security(self, test_results):
        """Analyze security findings."""
        try:
            analysis = {
                "security_issues": 0,
                "issues": []
            }

            for result in test_results:
                if "security_issues" in result:
                    analysis["security_issues"] += len(result["security_issues"])

            if analysis["security_issues"] > 0:
                analysis["issues"].append(f"Found {analysis['security_issues']} security issues")

            return analysis

        except Exception as e:
            return {
                "error": str(e),
                "issues": ["Could not analyze security"]
            }

    def _generate_suggestions(self, analysis):
        """Generate optimization suggestions based on analysis."""
        suggestions = []

        # Code quality suggestions
        if "issues" in analysis["code_quality"] and analysis["code_quality"]["issues"]:
            for issue in analysis["code_quality"]["issues"]:
                suggestions.append({
                    "type": "code_quality",
                    "details": f"Code quality issue: {issue}",
                    "priority": "medium"
                })

        # Test result suggestions
        if "issues" in analysis["test_results"] and analysis["test_results"]["issues"]:
            for issue in analysis["test_results"]["issues"]:
                suggestions.append({
                    "type": "testing",
                    "details": f"Testing issue: {issue}",
                    "priority": "high" if "failed" in issue else "medium"
                })

        # Performance suggestions
        if "issues" in analysis["performance"] and analysis["performance"]["issues"]:
            for issue in analysis["performance"]["issues"]:
                suggestions.append({
                    "type": "performance",
                    "details": f"Performance issue: {issue}",
                    "priority": "high"
                })

        # Security suggestions
        if "issues" in analysis["security"] and analysis["security"]["issues"]:
            for issue in analysis["security"]["issues"]:
                suggestions.append({
                    "type": "security",
                    "details": f"Security issue: {issue}",
                    "priority": "critical"
                })

        # General suggestions
        if analysis["test_results"]["passed"] == analysis["test_results"]["total_tests"]:
            suggestions.append({
                "type": "general",
                "details": "All tests passed - good job!",
                "priority": "low"
            })

        if analysis["code_quality"]["comments"] < analysis["code_quality"]["lines"] * 0.1:
            suggestions.append({
                "type": "documentation",
                "details": "Consider adding more comments to the code",
                "priority": "low"
            })

        return suggestions

    async def _research_improvements(self, language, task_description):
        """Research additional improvements using the Researcher agent."""
        try:
            if not self.researcher:
                return []

            suggestions = []

            # Research optimizations
            opt_results = await self.researcher.research_optimizations(language, task_description)
            for result in opt_results:
                suggestions.append({
                    "type": "optimization",
                    "details": result["content"],
                    "source": "researcher",
                    "priority": "medium"
                })

            # Research best practices
            bp_results = await self.researcher.search_web(f"{language} best practices {task_description}")
            for result in bp_results:
                suggestions.append({
                    "type": "best_practice",
                    "details": f"Found best practice: {result['snippet']} - {result['url']}",
                    "source": "researcher",
                    "priority": "medium"
                })

            # Research code examples
            example_results = await self.researcher.get_code_examples(language, task_description)
            for result in example_results:
                suggestions.append({
                    "type": "example",
                    "details": f"Code example: {result['title']}",
                    "code": result["code"],
                    "source": "researcher",
                    "priority": "low"
                })

            return suggestions

        except Exception as e:
            return [{
                "type": "error",
                "details": f"Research failed: {str(e)}",
                "priority": "low"
            }]

    def get_improvement_history(self):
        """Get the history of improvements."""
        return self.history.get("history", [])

    def get_statistics(self):
        """Get optimization statistics."""
        history = self.history.get("history", [])
        stats = {
            "total_suggestions": len(history),
            "by_type": {},
            "by_priority": {}
        }

        for entry in history:
            suggestion_type = entry.get("type", "unknown")
            priority = entry.get("priority", "medium")

            if suggestion_type not in stats["by_type"]:
                stats["by_type"][suggestion_type] = 0
            stats["by_type"][suggestion_type] += 1

            if priority not in stats["by_priority"]:
                stats["by_priority"][priority] = 0
            stats["by_priority"][priority] += 1

        return stats


