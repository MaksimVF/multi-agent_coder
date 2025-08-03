




import subprocess
import tempfile
import os
import time
import sys
import traceback
import importlib.util
import docker
from pathlib import Path
import coverage
import unittest

from unittest.mock import Mock, patch
import json
from typing import Dict, Any, Optional

from base_llm_agent import BaseLLMAgent

class Tester(BaseLLMAgent):
    """LLM-powered Tester agent for code testing and validation."""

    def __init__(self, model: str = "gpt-4o", temperature: float = 0.3, memory_manager: Optional["MemoryManager"] = None):
        """
        Initialize the LLM-powered Tester.

        Args:
            model: LLM model to use
            temperature: Creativity level for LLM
            memory_manager: Memory manager for agent memory
        """
        super().__init__(model=model, temperature=temperature, memory_manager=memory_manager)

        # Tester-specific configuration
        self.system_message = (
            "You are an expert software tester. Your job is to analyze code, "
            "generate test cases, and validate code quality and correctness."
        )

        # Docker sandbox configuration
        self.use_docker_sandbox = False
        self.docker_image = "sandbox-python"
        self.docker_timeout = 30  # seconds
        self.docker_memory_limit = "512m"
        self.docker_cpu_limit = 1.0

        try:
            import docker
            self.docker_client = docker.from_env()
            # Try to ping Docker to verify it's available
            self.docker_client.ping()
            self.use_docker_sandbox = True
            print("Docker available - using sandbox for code execution")
        except (ImportError, AttributeError, docker.errors.DockerException) as e:
            print(f"Docker not available, using subprocess: {e}")
            self.use_docker_sandbox = False
        except Exception as e:
            print(f"Error initializing Docker: {e}")
            self.use_docker_sandbox = False

    async def test_code(self, code_data: Dict[str, Any], subtask: Dict[str, Any], language: str = "python", test_type: str = "basic") -> Dict[str, Any]:
        """Test the given code with enhanced testing capabilities."""
        code = code_data["code"]
        description = code_data["description"]

        try:
            # Call the appropriate test method based on test_type
            if test_type == "basic":
                return await self._basic_test(code_data, subtask, language)
            elif test_type == "unit":
                return await self._unit_test(code, language, description)
            elif test_type == "integration":
                return await self._integration_test(code, language, description)
            elif test_type == "performance":
                return await self._performance_test(code, language)
            elif test_type == "coverage":
                return await self._coverage_test(code, language, description)
            elif test_type == "security":
                return await self._security_test(code, language, description)
            else:
                return {
                    "description": description,
                    "passed": False,
                    "error": f"Unknown test type: {test_type}"
                }

        except Exception as e:
            return {
                "description": description,
                "passed": False,
                "error": str(e),
                "traceback": traceback.format_exc()
            }


    async def generate_test_cases(self, code: str, language: str = "python") -> Dict[str, Any]:
        """Generate test cases using LLM."""
        prompt = f"""
        Generate comprehensive test cases for the following {language} code:

        Code:
        {code}

        Provide the test cases as a JSON object with these fields:
        - test_cases: List of test case objects, each with:
            - description: What the test verifies
            - input: Input data for the test
            - expected_output: Expected result
            - type: 'unit', 'integration', or 'edge case'
        - test_strategy: Brief explanation of the testing approach
        """

        try:
            response = await self.generate_response(prompt, self.system_message)
            try:
                test_cases = json.loads(response)
                return test_cases
            except json.JSONDecodeError:
                # Fallback: extract test cases from response
                return {
                    "test_cases": [
                        {
                            "description": "Basic functionality test",
                            "input": "standard input",
                            "expected_output": "expected result",
                            "type": "unit"
                        }
                    ],
                    "test_strategy": "Basic testing approach"
                }
        except Exception as e:
            return {
                "test_cases": [],
                "error": str(e),
                "traceback": traceback.format_exc()
            }



    # Alias for generate_test_cases
    async def generate_tests(self, code_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate test cases for the given code."""
        return await self.generate_test_cases(code_data["code"], code_data.get("language", "python"))

    async def process(self, data: Dict[str, Any]) -> Dict[str, Any]:

        """Process incoming data for the workflow."""
        if "code" in data and "subtask" in data and "language" in data and "test_type" in data:
            test_result = await self.test_code(
                data["code"],
                data["subtask"],
                data["language"],
                data["test_type"]
            )
            return {"test_result": test_result}
        else:
            return {"error": "Insufficient data for testing"}

    async def _basic_test(self, code_data, subtask, language):
        """Run basic execution test."""
        code = code_data["code"]
        description = code_data["description"]

        try:
            # Determine file extension and execution command based on language
            if language == "python":
                file_suffix = '.py'
                command = ['python', '{filename}']
            elif language == "javascript":
                file_suffix = '.js'
                command = ['node', '{filename}']
            elif language == "java":
                return await self._java_test(code, description)
            elif language == "csharp":
                file_suffix = '.cs'
                command = ['dotnet', 'run', '--project', '{filename}']
            else:
                # Default to Python
                file_suffix = '.py'
                command = ['python', '{filename}']

            # Write code to a temporary file and execute
            with tempfile.NamedTemporaryFile(mode='w', suffix=file_suffix, delete=False) as f:
                f.write(code)
                temp_file = f.name

            result = self._execute_command(command, description, temp_file)

            # Clean up
            os.unlink(temp_file)
            return result

        except Exception as e:
            return {
                "description": description,
                "passed": False,
                "error": str(e),
                "traceback": traceback.format_exc()
            }

    async def _java_test(self, code, description):
        """Test Java code with compilation and execution."""
        file_suffix = '.java'

        # Write code to a temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix=file_suffix, delete=False) as f:
            f.write(code)
            temp_file = f.name

        # Compile the Java code
        compile_result = subprocess.run(
            ['javac', temp_file],
            capture_output=True,
            text=True,
            timeout=10
        )

        if compile_result.returncode != 0:
            os.unlink(temp_file)
            return {
                "description": description,
                "passed": False,
                "error": compile_result.stderr or "Java compilation failed"
            }

        # Run the compiled Java code
        class_name = os.path.splitext(os.path.basename(temp_file))[0]
        command = ['java', class_name]

        # Clean up the source file but keep the class file for execution
        os.unlink(temp_file)

        # Execute the compiled code
        result = self._execute_command(command, description, cleanup_pattern=f"{class_name}.class")

        # Clean up class file
        try:
            os.unlink(f"{class_name}.class")
        except:
            pass

        return result

    def _execute_command(self, command, description, filename=None, cleanup_pattern=None):
        """Execute a command with the given filename using enhanced security measures."""
        try:
            # Replace placeholder with actual filename if provided
            if filename:
                actual_command = [arg.replace('{filename}', filename) for arg in command]
            else:
                actual_command = command

            # Set resource limits for security
            import resource
            # Limit CPU time (10 seconds)
            resource.setrlimit(resource.RLIMIT_CPU, (10, 10))
            # Limit memory (500MB)
            resource.setrlimit(resource.RLIMIT_AS, (500 * 1024 * 1024, 500 * 1024 * 1024))

            # Execute in a restricted environment
            env = os.environ.copy()
            # Remove sensitive environment variables
            for var in ['OPENAI_API_KEY', 'LITELLM_API_KEY', 'GITHUB_TOKEN', 'GITLAB_TOKEN']:
                if var in env:
                    del env[var]

            # Try to execute the code with strict security
            result = subprocess.run(
                actual_command,
                capture_output=True,
                text=True,
                timeout=10,
                env=env,
                # Restrict capabilities - note: this requires proper system configuration
                # For now, we rely on the restricted environment
            )

            # Check if execution was successful
            if result.returncode == 0:
                return {
                    "description": description,
                    "passed": True,
                    "output": result.stdout,
                    "stderr": result.stderr
                }
            else:
                return {
                    "description": description,
                    "passed": False,
                    "error": result.stderr or "Unknown error",
                    "stdout": result.stdout
                }

        except subprocess.TimeoutExpired:
            return {
                "description": description,
                "passed": False,
                "error": "Execution timed out (10 seconds)",
                "timeout": True
            }
        except Exception as e:
            return {
                "description": description,
                "passed": False,
                "error": str(e),
                "traceback": traceback.format_exc()
            }
        finally:
            # Ensure resource limits are reset
            try:
                resource.setrlimit(resource.RLIMIT_CPU, (resource.RLIM_INFINITY, resource.RLIM_INFINITY))
                resource.setrlimit(resource.RLIMIT_AS, (resource.RLIM_INFINITY, resource.RLIM_INFINITY))
            except:
                pass

    async def _unit_test(self, code, language, description):
        """Create and run comprehensive unit tests."""
        if language == "python":
            try:
                # Generate test code
                test_code = self._generate_python_unit_test(code, description)

                # Write test to a temporary file
                with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as temp_file:
                    temp_file.write(test_code.encode('utf-8'))
                    test_path = temp_file.name

                # Try Docker sandbox first, fallback to subprocess
                docker_result = self._execute_in_docker_sandbox(test_code, "python")

                if docker_result:
                    result = docker_result
                    # Clean up
                    os.unlink(test_path)
                else:
                    # Fallback to subprocess
                    result = subprocess.run(
                        ['python', test_path],
                        capture_output=True,
                        text=True,
                        timeout=10
                    )

                    # Clean up
                    os.unlink(test_path)

                if result.returncode == 0:
                    return {
                        "description": description,
                        "passed": True,
                        "output": "Unit tests passed",
                        "test_type": "unit"
                    }
                else:
                    return {
                        "description": description,
                        "passed": False,
                        "error": result.stderr or "Unit tests failed",
                        "test_type": "unit",
                        "stdout": result.stdout
                    }
            except Exception as e:
                return {
                    "description": description,
                    "passed": False,
                    "error": str(e),
                    "traceback": traceback.format_exc(),
                    "test_type": "unit"
                }
        else:
            return {
                "description": description,
                "passed": False,
                "error": f"Unit testing not yet supported for {language}",
                "test_type": "unit"
            }

    async def _integration_test(self, code, language, description):
        """Run integration tests that verify how components work together."""
        if language == "python":
            try:
                # For integration testing, we need to analyze the code structure
                # and create tests that verify how different components interact

                # First, let's try to import the code to analyze its structure
                with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as temp_file:
                    temp_file.write(code.encode('utf-8'))
                    temp_path = temp_file.name

                # Generate integration test
                integration_test = self._generate_integration_test(code, description)

                # Write integration test to a file
                with tempfile.NamedTemporaryFile(suffix="_integration.py", delete=False) as test_file:
                    test_file.write(integration_test.encode('utf-8'))
                    test_path = test_file.name

                # Run the integration test
                result = subprocess.run(
                    ['python', test_path],
                    capture_output=True,
                    text=True,
                    timeout=10
                )

                # Clean up
                os.unlink(temp_path)
                os.unlink(test_path)

                if result.returncode == 0:
                    return {
                        "description": description,
                        "passed": True,
                        "output": "Integration tests passed",
                        "test_type": "integration"
                    }
                else:
                    return {
                        "description": description,
                        "passed": False,
                        "error": result.stderr or "Integration tests failed",
                        "test_type": "integration",
                        "stdout": result.stdout
                    }
            except Exception as e:
                return {
                    "description": description,
                    "passed": False,
                    "error": str(e),
                    "traceback": traceback.format_exc(),
                    "test_type": "integration"
                }
        else:
            return {
                "description": description,
                "passed": False,
                "error": f"Integration testing not yet supported for {language}",
                "test_type": "integration"
            }

    async def _performance_test(self, code, language):
        """Measure execution time and other performance metrics."""
        import time
        import resource

        if language == "python":
            try:
                # Create a temporary file with the code
                with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as temp_file:
                    temp_file.write(code.encode('utf-8'))
                    temp_path = temp_file.name

                # Measure performance metrics
                start_time = time.time()
                start_memory = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

                result = subprocess.run(
                    ['python', temp_path],
                    capture_output=True,
                    text=True,
                    timeout=10
                )

                end_time = time.time()
                end_memory = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

                # Clean up
                os.unlink(temp_path)

                execution_time = end_time - start_time
                memory_usage = end_memory - start_memory  # in KB

                if result.returncode == 0:
                    return {
                        "description": "Performance test",
                        "passed": True,
                        "output": result.stdout,
                        "performance": {
                            "execution_time_ms": execution_time * 1000,
                            "memory_usage_kb": memory_usage
                        },
                        "test_type": "performance"
                    }
                else:
                    return {
                        "description": "Performance test",
                        "passed": False,
                        "error": result.stderr or "Performance test failed",
                        "performance": {
                            "execution_time_ms": execution_time * 1000,
                            "memory_usage_kb": memory_usage
                        },
                        "test_type": "performance"
                    }
            except subprocess.TimeoutExpired:
                return {
                    "description": "Performance test",
                    "passed": False,
                    "error": "Execution timed out (10 seconds)",
                    "timeout": True,
                    "test_type": "performance"
                }
            except Exception as e:
                return {
                    "description": "Performance test",
                    "passed": False,
                    "error": str(e),
                    "traceback": traceback.format_exc(),
                    "test_type": "performance"
                }
        else:
            return {
                "description": "Performance test",
                "passed": False,
                "error": f"Performance testing not yet supported for {language}",
                "test_type": "performance"
            }

    async def _coverage_test(self, code, language, description):
        """Measure code coverage."""
        if language == "python":
            try:
                # Create a temporary file with the code
                with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as temp_file:
                    temp_file.write(code.encode('utf-8'))
                    temp_path = temp_file.name

                # Generate a simple test to run the code
                test_code = f"""
import {os.path.splitext(os.path.basename(temp_path))[0]}
# Run the main functionality
if __name__ == "__main__":
    # Try to execute the main functionality
    try:
        # Look for common entry points
        if hasattr({os.path.splitext(os.path.basename(temp_path))[0]}, 'main'):
            {os.path.splitext(os.path.basename(temp_path))[0]}.main()
        elif hasattr({os.path.splitext(os.path.basename(temp_path))[0]}, 'run'):
            {os.path.splitext(os.path.basename(temp_path))[0]}.run()
        # Add more entry points as needed
    except:
        pass
"""

                with tempfile.NamedTemporaryFile(suffix="_test.py", delete=False) as test_file:
                    test_file.write(test_code.encode('utf-8'))
                    test_path = test_file.name

                # Run coverage measurement
                cov = coverage.Coverage()
                cov.start()

                result = subprocess.run(
                    ['python', test_path],
                    capture_output=True,
                    text=True,
                    timeout=10
                )

                cov.stop()
                cov.save()

                # Get coverage percentage using the correct API
                try:
                    # Get the analysis data
                    data = cov.get_data()

                    # Calculate coverage
                    covered_lines = data.measured_lines()
                    total_lines = len(data.lines())

                    coverage_percent = 0
                    if total_lines > 0:
                        coverage_percent = (len(covered_lines) / total_lines * 100)

                    covered = len(covered_lines)

                except Exception as e:
                    coverage_percent = 0
                    covered = 0
                    total_lines = 0

                # Clean up
                os.unlink(temp_path)
                os.unlink(test_path)

                if result.returncode == 0:
                    return {
                        "description": description,
                        "passed": True,
                        "output": result.stdout,
                        "coverage": {
                            "percentage": coverage_percent,
                            "covered_lines": covered,
                            "total_lines": total_lines
                        },
                        "test_type": "coverage"
                    }
                else:
                    return {
                        "description": description,
                        "passed": False,
                        "error": result.stderr or "Coverage test failed",
                        "coverage": {
                            "percentage": coverage_percent,
                            "covered_lines": covered,
                            "total_lines": total_lines
                        },
                        "test_type": "coverage"
                    }
            except Exception as e:
                return {
                    "description": description,
                    "passed": False,
                    "error": str(e),
                    "traceback": traceback.format_exc(),
                    "test_type": "coverage"
                }
        else:
            return {
                "description": description,
                "passed": False,
                "error": f"Coverage testing not yet supported for {language}",
                "test_type": "coverage"
            }

    async def _security_test(self, code, language, description):
        """Run basic security checks.

        TODO: Enhance security by implementing:
        1. Docker-based sandboxing for code execution
        2. Integration with static analysis tools (Bandit, ESLint, etc.)
        3. Network isolation for executed code
        4. Filesystem restrictions
        5. Comprehensive security testing for all supported languages
        """
        if language == "python":
            try:
                # Check for common security issues
                security_issues = []

                # Check for eval() usage
                if "eval(" in code:
                    security_issues.append("Potential security issue: eval() usage detected")

                # Check for pickle usage
                if "pickle" in code:
                    security_issues.append("Potential security issue: pickle usage detected")

                # Check for hardcoded credentials
                import re
                credential_patterns = [
                    r"password\s*=\s*['\"][^'\"]*['\"]",
                    r"secret\s*=\s*['\"][^'\"]*['\"]",
                    r"api_key\s*=\s*['\"][^'\"]*['\"]",
                    r"token\s*=\s*['\"][^'\"]*['\"]"
                ]

                for pattern in credential_patterns:
                    if re.search(pattern, code, re.IGNORECASE):
                        security_issues.append(f"Potential security issue: hardcoded credentials detected")

                # Check for SQL injection vulnerabilities
                if re.search(r"\.execute\s*\(.*?\s*\+\s.*?\)", code):
                    security_issues.append("Potential security issue: SQL injection risk detected")

                if security_issues:
                    return {
                        "description": description,
                        "passed": False,
                        "error": "Security issues found",
                        "security_issues": security_issues,
                        "test_type": "security"
                    }
                else:
                    return {
                        "description": description,
                        "passed": True,
                        "output": "No security issues found",
                        "test_type": "security"
                    }
            except Exception as e:
                return {
                    "description": description,
                    "passed": False,
                    "error": str(e),
                    "traceback": traceback.format_exc(),
                    "test_type": "security"
                }
        elif language == "javascript":
            try:
                # Check for common JavaScript security issues
                security_issues = []

                # Check for eval() usage
                if "eval(" in code:
                    security_issues.append("Potential security issue: eval() usage detected")

                # Check for innerHTML usage (XSS risk)
                if ".innerHTML" in code:
                    security_issues.append("Potential security issue: innerHTML usage detected (XSS risk)")

                # Check for hardcoded credentials
                import re
                credential_patterns = [
                    r"password\s*=\s*['\"][^'\"]*['\"]",
                    r"secret\s*=\s*['\"][^'\"]*['\"]",
                    r"api_key\s*=\s*['\"][^'\"]*['\"]",
                    r"token\s*=\s*['\"][^'\"]*['\"]"
                ]

                for pattern in credential_patterns:
                    if re.search(pattern, code, re.IGNORECASE):
                        security_issues.append(f"Potential security issue: hardcoded credentials detected")

                # Check for SQL injection vulnerabilities
                if re.search(r"\.query\s*\(.*?\s*\+\s.*?\)", code):
                    security_issues.append("Potential security issue: SQL injection risk detected")

                if security_issues:
                    return {
                        "description": description,
                        "passed": False,
                        "error": "Security issues found",
                        "security_issues": security_issues,
                        "test_type": "security"
                    }
                else:
                    return {
                        "description": description,
                        "passed": True,
                        "output": "No security issues found",
                        "test_type": "security"
                    }
            except Exception as e:
                return {
                    "description": description,
                    "passed": False,
                    "error": str(e),
                    "traceback": traceback.format_exc(),
                    "test_type": "security"
                }
        elif language == "java":
            try:
                # Check for common Java security issues
                security_issues = []

                # Check for Runtime.exec usage
                if "Runtime.getRuntime().exec" in code:
                    security_issues.append("Potential security issue: Runtime.exec usage detected")

                # Check for hardcoded credentials
                import re
                credential_patterns = [
                    r"password\s*=\s*['\"][^'\"]*['\"]",
                    r"secret\s*=\s*['\"][^'\"]*['\"]",
                    r"api_key\s*=\s*['\"][^'\"]*['\"]",
                    r"token\s*=\s*['\"][^'\"]*['\"]"
                ]

                for pattern in credential_patterns:
                    if re.search(pattern, code, re.IGNORECASE):
                        security_issues.append(f"Potential security issue: hardcoded credentials detected")

                # Check for SQL injection vulnerabilities
                if re.search(r"Statement\.executeQuery\s*\(.*?\s*\+\s.*?\)", code):
                    security_issues.append("Potential security issue: SQL injection risk detected")

                if security_issues:
                    return {
                        "description": description,
                        "passed": False,
                        "error": "Security issues found",
                        "security_issues": security_issues,
                        "test_type": "security"
                    }
                else:
                    return {
                        "description": description,
                        "passed": True,
                        "output": "No security issues found",
                        "test_type": "security"
                    }
            except Exception as e:
                return {
                    "description": description,
                    "passed": False,
                    "error": str(e),
                    "traceback": traceback.format_exc(),
                    "test_type": "security"
                }
        else:
            return {
                "description": description,
                "passed": False,
                "error": f"Security testing not yet supported for {language}",
                "test_type": "security"
            }

    def _execute_in_docker_sandbox(self, code: str, language: str = "python") -> Dict[str, Any]:
        """Execute code in an isolated Docker container for enhanced security."""
        if not self.use_docker_sandbox:
            return None

        try:
            # Create a temporary file with the code
            with tempfile.NamedTemporaryFile(mode='w', suffix=f'.{language}', delete=False) as f:
                f.write(code)
                temp_file = f.name

            # Determine the Docker command based on language
            if language == "python":
                cmd = ["python", os.path.basename(temp_file)]
                workdir = "/home/sandboxuser/code"
                file_path = f"/home/sandboxuser/code/{os.path.basename(temp_file)}"
            elif language == "javascript":
                cmd = ["node", os.path.basename(temp_file)]
                workdir = "/home/sandboxuser/code"
                file_path = f"/home/sandboxuser/code/{os.path.basename(temp_file)}"
            elif language == "java":
                # For Java, we need to compile first
                base_name = os.path.splitext(os.path.basename(temp_file))[0]
                cmd = ["sh", "-c", f"javac {os.path.basename(temp_file)} && java {base_name}"]
                workdir = "/home/sandboxuser/code"
                file_path = f"/home/sandboxuser/code/{os.path.basename(temp_file)}"
            else:
                return None  # Fallback to subprocess for unsupported languages

            # Run the container with strict resource limits
            container = self.docker_client.containers.run(
                image=self.docker_image,
                command=cmd,
                volumes={os.path.dirname(temp_file): {'bind': workdir, 'mode': 'ro'}},
                working_dir=workdir,
                mem_limit=self.docker_memory_limit,
                cpu_period=100000,  # 100ms period
                cpu_quota=int(self.docker_cpu_limit * 100000),  # CPU limit
                network_disabled=True,  # Disable network for security
                auto_remove=True,  # Clean up container after execution
                detach=False,
                stdout=True,
                stderr=True
            )

            # Process the result
            result = {
                "stdout": container.decode('utf-8') if hasattr(container, 'decode') else str(container),
                "stderr": "",
                "returncode": 0
            }

            # Clean up
            os.unlink(temp_file)

            return result

        except docker.errors.ContainerError as e:
            return {
                "stdout": "",
                "stderr": str(e.stderr.decode('utf-8') if hasattr(e, 'stderr') else str(e)),
                "returncode": e.exit_status if hasattr(e, 'exit_status') else 1
            }
        except docker.errors.DockerException as e:
            print(f"Docker error: {e}")
            return None
        except Exception as e:
            print(f"Error in Docker execution: {e}")
            return None

    def _generate_python_unit_test(self, code, description):
        """Generate comprehensive Python unit test code."""
        # Parse the code to understand its structure
        test_code = f"""
import unittest
import sys
import io
from unittest.mock import Mock, patch

# Code to test
{code}

class TestGeneratedCode(unittest.TestCase):
    def setUp(self):
        # Set up any necessary mocks or test data
        pass

    def tearDown(self):
        # Clean up after tests
        pass

    def test_basic_functionality(self):
        # Basic test - try to execute the main functionality
        try:
            # Test common function names
            module_name = '{os.path.splitext(description)[0]}'

            # Try to import the module
            try:
                module = sys.modules[module_name]
            except KeyError:
                # Module not found, try to import it
                try:
                    spec = importlib.util.spec_from_file_location(module_name, __file__)
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                except:
                    module = None

            if module:
                # Test common functions
                if hasattr(module, 'main'):
                    with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
                        module.main()
                        output = mock_stdout.getvalue()
                        self.assertTrue(len(output) > 0, "No output from main function")

                if hasattr(module, 'add'):
                    result = module.add(1, 2)
                    self.assertEqual(result, 3, "add(1, 2) should return 3")

                if hasattr(module, 'subtract'):
                    result = module.subtract(5, 3)
                    self.assertEqual(result, 2, "subtract(5, 3) should return 2")

                if hasattr(module, 'multiply'):
                    result = module.multiply(2, 3)
                    self.assertEqual(result, 6, "multiply(2, 3) should return 6")

                if hasattr(module, 'divide'):
                    result = module.divide(6, 3)
                    self.assertEqual(result, 2, "divide(6, 3) should return 2")

                    # Test division by zero
                    with self.assertRaises(ZeroDivisionError):
                        module.divide(1, 0)

            # Add more test cases as needed
        except Exception as e:
            self.fail(f"Test failed with exception: {{e}}")

    def test_edge_cases(self):
        # Test edge cases and error conditions
        try:
            module_name = '{os.path.splitext(description)[0]}'
            module = sys.modules.get(module_name)

            if module:
                if hasattr(module, 'add'):
                    # Test with negative numbers
                    self.assertEqual(module.add(-1, -2), -3)
                    # Test with zero
                    self.assertEqual(module.add(0, 0), 0)
                    # Test with large numbers
                    self.assertEqual(module.add(1000000, 2000000), 3000000)

                if hasattr(module, 'divide'):
                    # Test with negative numbers
                    self.assertEqual(module.divide(-6, -3), 2)
                    # Test with decimal results
                    result = module.divide(5, 2)
                    self.assertTrue(abs(result - 2.5) < 0.0001)

        except Exception as e:
            self.fail(f"Edge case test failed with exception: {{e}}")

    def test_error_handling(self):
        # Test error handling
        try:
            module_name = '{os.path.splitext(description)[0]}'
            module = sys.modules.get(module_name)

            if module:
                if hasattr(module, 'divide'):
                    # Test division by zero
                    with self.assertRaises(ZeroDivisionError):
                        module.divide(1, 0)

                if hasattr(module, 'sqrt'):
                    # Test square root of negative number
                    with self.assertRaises(ValueError):
                        module.sqrt(-1)

        except Exception as e:
            self.fail(f"Error handling test failed with exception: {{e}}")

if __name__ == '__main__':
    unittest.main()
"""
        return test_code

    def _generate_integration_test(self, code, description):
        """Generate integration test code."""
        test_code = f"""
import unittest
import sys
import io
from unittest.mock import Mock, patch

# Code to test
{code}

class TestIntegration(unittest.TestCase):
    def setUp(self):
        # Set up any necessary mocks or test data
        pass

    def tearDown(self):
        # Clean up after tests
        pass

    def test_module_integration(self):
        # Test how different components work together
        try:
            # Test functions directly from the code
            from __main__ import add, subtract, multiply, divide

            # Test integration between functions
            # Test that add and multiply work together
            result1 = add(2, 3)
            result2 = multiply(result1, 2)
            self.assertEqual(result2, 10, "add(2,3) * 2 should be 10")

            # Test that subtract and divide work together
            result1 = subtract(10, 4)
            result2 = divide(result1, 3)
            self.assertEqual(result2, 2, "(10-4)/3 should be 2")

        except Exception as e:
            self.fail(f"Integration test failed with exception: {{e}}")

    def test_data_flow(self):
        # Test data flow through the system
        try:
            # Test functions directly
            from __main__ import add, subtract, multiply, divide

            # Test a simple data processing flow
            # Process: (2 + 3) * 2 - 4 / 2
            result1 = add(2, 3)
            result2 = multiply(result1, 2)
            result3 = subtract(result2, 4)
            result4 = divide(result3, 2)

            self.assertEqual(result4, 3, "Complex operation should yield 3")

        except Exception as e:
            self.fail(f"Data flow test failed with exception: {{e}}")

if __name__ == '__main__':
    unittest.main()
"""
        return test_code


