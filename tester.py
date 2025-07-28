




import subprocess
import tempfile
import os

class Tester:
    def test_code(self, code_data, language="python"):
        """Test the given code."""
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


