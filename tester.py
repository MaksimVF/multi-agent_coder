




import subprocess
import tempfile
import os

class Tester:
    async def test_code(self, code_data, subtask, language="python", test_type="basic"):
        """Test the given code."""
        code = code_data["code"]
        description = code_data["description"]

        try:
            # Call the appropriate test method based on test_type
            if test_type == "basic":
                # Continue with existing logic
                pass  # The existing logic will be executed
            elif test_type == "unit":
                return await self._unit_test(code, language, description)
            elif test_type == "integration":
                # For now, integration test is the same as basic test
                return await self.test_code(code_data, description, language, "basic")
            elif test_type == "performance":
                return await self._performance_test(code, language)
            else:
                return {
                    "description": description,
                    "passed": False,
                    "error": f"Unknown test type: {test_type}"
                }

            # Determine file extension and execution command based on language
            if language == "python":
                file_suffix = '.py'
                command = ['python', '{filename}']
            elif language == "javascript":
                file_suffix = '.js'
                command = ['node', '{filename}']
            elif language == "java":
                # For Java, we need to compile first
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
                # We'll clean up the class file after execution
                return self._execute_command(command, description, cleanup_pattern=f"{class_name}.class")

            elif language == "csharp":
                file_suffix = '.cs'
                command = ['dotnet', 'run', '--project', '{filename}']
            else:
                # Default to Python
                file_suffix = '.py'
                command = ['python', '{filename}']

            # Write code to a temporary file and execute
            if language != "java":  # Java is handled separately above
                with tempfile.NamedTemporaryFile(mode='w', suffix=file_suffix, delete=False) as f:
                    f.write(code)
                    temp_file = f.name

                result = self._execute_command(command, description, temp_file)

                # Clean up
                os.unlink(temp_file)
                return result
            else:
                # Java was already handled
                return {
                    "description": description,
                    "passed": False,
                    "error": "Java execution not properly implemented"
                }

        except Exception as e:
            return {
                "description": description,
                "passed": False,
                "error": str(e)
            }

    def _execute_command(self, command, description, filename, cleanup_pattern=None):
        """Execute a command with the given filename."""
        try:
            # Replace placeholder with actual filename
            actual_command = [arg.replace('{filename}', filename) for arg in command]

            # Try to execute the code
            result = subprocess.run(
                actual_command,
                capture_output=True,
                text=True,
                timeout=10
            )

            # Check if execution was successful
            if result.returncode == 0:
                return {
                    "description": description,
                    "passed": True,
                    "output": result.stdout
                }
            else:
                return {
                    "description": description,
                    "passed": False,
                    "error": result.stderr or "Unknown error"
                }

        except Exception as e:
            return {
                "description": description,
                "passed": False,
                "error": str(e)
            }

    async def _unit_test(self, code, language, subtask):
        """Create and run unit tests."""
        if language == "python":
            # Create a test function
            test_code = self._generate_python_unit_test(code, subtask)

            # Write test to a temporary file
            with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as temp_file:
                temp_file.write(test_code.encode('utf-8'))
                test_path = temp_file.name

            # Run the test using a different approach
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
                    "description": subtask,
                    "passed": True,
                    "output": "Unit tests passed"
                }
            else:
                return {
                    "description": subtask,
                    "passed": False,
                    "error": result.stderr or "Unit tests failed"
                }
        else:
            return {
                "description": subtask,
                "passed": False,
                "error": f"Unit testing not yet supported for {language}"
            }

    async def _performance_test(self, code, language):
        """Measure execution time."""
        import time

        if language == "python":
            # Create a temporary file with the code
            with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as temp_file:
                temp_file.write(code.encode('utf-8'))
                temp_path = temp_file.name

            # Measure execution time
            start_time = time.time()
            result = subprocess.run(
                ['python', temp_path],
                capture_output=True,
                text=True,
                timeout=10
            )
            end_time = time.time()

            # Clean up
            os.unlink(temp_path)

            execution_time = end_time - start_time

            if result.returncode == 0:
                return {
                    "description": "Performance test",
                    "passed": True,
                    "output": result.stdout,
                    "performance": {
                        "execution_time_ms": execution_time * 1000
                    }
                }
            else:
                return {
                    "description": "Performance test",
                    "passed": False,
                    "error": result.stderr or "Performance test failed"
                }
        else:
            return {
                "description": "Performance test",
                "passed": False,
                "error": f"Performance testing not yet supported for {language}"
            }

    def _generate_python_unit_test(self, code, subtask):
        """Generate Python unit test code."""
        # Simple test generation - this can be enhanced
        test_code = f"""
import unittest

# Code to test
{code}

class TestGeneratedCode(unittest.TestCase):
    def test_basic_functionality(self):
        # Basic test - try to execute the main functionality
        try:
            # Check if there's an add function and test it
            if hasattr(__import__('__main__'), 'add'):
                from __main__ import add
                result = add(1, 2)
                self.assertEqual(result, 3)
            # Add more test cases as needed
        except Exception as e:
            self.fail(f"Test failed with exception: {{e}}")

if __name__ == '__main__':
    unittest.main()
"""
        return test_code


