


import subprocess
import tempfile
import os

class Tester:
    def test_code(self, code_data):
        """Test the given code."""
        code = code_data["code"]
        description = code_data["description"]

        try:
            # Write code to a temporary file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(code)
                temp_file = f.name

            # Try to execute the code
            result = subprocess.run(
                ['python', temp_file],
                capture_output=True,
                text=True,
                timeout=5
            )

            # Clean up
            os.unlink(temp_file)

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


