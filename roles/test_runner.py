









import os
import subprocess
import time
from typing import Dict, Any, List, Tuple
from .base_role import BaseRole

class TestRunner(BaseRole):
    """Test Runner role - handles automated testing, error logging, and fix retries"""

    def __init__(self):
        super().__init__(
            name="TestRunner",
            description="Handles automated testing, error logging, and fix retries",
            tools=["test_execution", "error_logging", "code_fixing", "timeout_management"]
        )

    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Run automated testing with error handling and fix retries"""
        # Get code implementation from context
        code_implementation = context.get("code_implementation", {})
        test_config = context.get("test_config", {})

        # Run initial tests
        test_results = await self._run_tests(code_implementation, test_config)

        # Check if tests passed
        if test_results["status"] == "success":
            return {
                "test_results": test_results,
                "next_role": "GitIntegrator"
            }

        # If tests failed, try to fix and retry
        max_retries = test_config.get("max_retries", 3)
        retry_delay = test_config.get("retry_delay", 5)  # seconds
        timeout = test_config.get("timeout", 30)  # seconds per test

        for attempt in range(1, max_retries + 1):
            # Log test failure
            error_log = await self._log_test_errors(test_results)

            # Try to fix errors
            fix_attempt = await self._fix_errors(code_implementation, test_results)

            # Update code implementation with fixes
            code_implementation.update(fix_attempt["fixed_files"])

            # Run tests again
            test_results = await self._run_tests(code_implementation, test_config, timeout)

            # Check if tests passed
            if test_results["status"] == "success":
                return {
                    "test_results": test_results,
                    "error_logs": [error_log],
                    "fix_attempts": attempt,
                    "next_role": "GitIntegrator"
                }

            # Wait before next retry
            time.sleep(retry_delay)

        # If all retries failed
        return {
            "test_results": test_results,
            "error_logs": await self._log_test_errors(test_results),
            "fix_attempts": max_retries,
            "status": "failed",
            "message": "All test retries failed"
        }

    async def _run_tests(self, code_implementation: Dict[str, str], test_config: Dict[str, Any], timeout: int = 30) -> Dict[str, Any]:
        """Run tests with timeout"""
        test_commands = test_config.get("commands", ["pytest tests/"])

        results = {
            "status": "success",
            "tests_run": 0,
            "tests_passed": 0,
            "tests_failed": 0,
            "errors": [],
            "coverage": 0
        }

        for command in test_commands:
            try:
                # Run test command with timeout
                process = await asyncio.create_subprocess_shell(
                    command,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )

                # Wait for process to complete with timeout
                try:
                    stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=timeout)

                    # Parse test results
                    if process.returncode != 0:
                        results["status"] = "failed"
                        results["errors"].append({
                            "command": command,
                            "stdout": stdout.decode(),
                            "stderr": stderr.decode()
                        })
                    else:
                        # Parse test output (simplified)
                        output = stdout.decode()
                        if "passed" in output:
                            results["tests_passed"] += 1
                        if "failed" in output:
                            results["tests_failed"] += 1
                        results["tests_run"] += 1

                except asyncio.TimeoutError:
                    # Kill process if timeout exceeded
                    process.kill()
                    await process.wait()
                    results["status"] = "failed"
                    results["errors"].append({
                        "command": command,
                        "error": "Test timeout exceeded",
                        "timeout": timeout
                    })

            except Exception as e:
                results["status"] = "failed"
                results["errors"].append({
                    "command": command,
                    "error": str(e)
                })

        # Calculate coverage (simplified)
        if results["tests_run"] > 0:
            results["coverage"] = (results["tests_passed"] / results["tests_run"]) * 100

        return results

    async def _log_test_errors(self, test_results: Dict[str, Any]) -> Dict[str, Any]:
        """Log test errors with detailed information"""
        error_logs = []

        for error in test_results.get("errors", []):
            error_log = {
                "command": error.get("command", ""),
                "error": error.get("error", ""),
                "stdout": error.get("stdout", ""),
                "stderr": error.get("stderr", ""),
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "severity": "high" if "timeout" in error.get("error", "").lower() else "medium"
            }
            error_logs.append(error_log)

            # Write to error log file
            with open("test_errors.log", "a") as f:
                f.write(f"Error: {error_log['error']}\n")
                f.write(f"Command: {error_log['command']}\n")
                f.write(f"Timestamp: {error_log['timestamp']}\n")
                f.write(f"Severity: {error_log['severity']}\n")
                f.write("="*50 + "\n")

        return {
            "error_logs": error_logs,
            "log_file": "test_errors.log"
        }

    async def _fix_errors(self, code_implementation: Dict[str, str], test_results: Dict[str, Any]) -> Dict[str, Any]:
        """Attempt to fix test errors automatically"""
        fixed_files = {}

        for error in test_results.get("errors", []):
            # Simple error fixing logic (can be enhanced with LLM)
            if "import error" in error.get("stderr", "").lower():
                # Try to fix import errors
                for filename, code in code_implementation.items():
                    if "import" in code:
                        # Add missing import (simplified)
                        fixed_code = code + "\n# Auto-fixed import\n"
                        fixed_files[filename] = fixed_code

            elif "syntax error" in error.get("stderr", "").lower():
                # Try to fix syntax errors
                for filename, code in code_implementation.items():
                    # Simple syntax fix (simplified)
                    fixed_code = code.replace(";", "\n")
                    fixed_files[filename] = fixed_code

            elif "timeout" in error.get("error", "").lower():
                # Add timeout handling
                for filename, code in code_implementation.items():
                    if "def " in code:
                        # Add timeout decorator (simplified)
                        fixed_code = code.replace("def ", "@timeout(30)\ndef ")
                        fixed_files[filename] = fixed_code

        return {
            "fixed_files": fixed_files,
            "fixes_applied": len(fixed_files)
        }

    async def _validate_code_quality(self, code_implementation: Dict[str, str]) -> Dict[str, Any]:
        """Validate code quality before commit"""
        quality_checks = {
            "status": "success",
            "issues": [],
            "score": 10
        }

        # Run linters
        for filename, code in code_implementation.items():
            if filename.endswith(".py"):
                # Run flake8 (simplified)
                try:
                    process = await asyncio.create_subprocess_shell(
                        f"flake8 {filename}",
                        stdout=asyncio.subprocess.PIPE,
                        stderr=asyncio.subprocess.PIPE
                    )
                    stdout, stderr = await process.communicate()

                    if process.returncode != 0:
                        quality_checks["status"] = "failed"
                        quality_checks["issues"].append({
                            "file": filename,
                            "issue": "Linting error",
                            "details": stdout.decode()
                        })
                        quality_checks["score"] -= 2

                except Exception as e:
                    quality_checks["issues"].append({
                        "file": filename,
                        "issue": "Linting failed",
                        "details": str(e)
                    })

            # Check for docstrings
            if '"""' not in code and "'''" not in code:
                quality_checks["issues"].append({
                    "file": filename,
                    "issue": "Missing docstring",
                    "details": "Add docstring to explain the purpose"
                })
                quality_checks["score"] -= 1

        return quality_checks







