


class Developer:
    def develop_code(self, subtask):
        """Develop code for a given subtask."""
        code = {
            "description": subtask["description"],
            "code": self._generate_code(subtask)
        }
        return code

    def fix_code(self, code, error):
        """Fix code based on test error."""
        description = code["description"]
        original_code = code["code"]

        print(f"Attempting to fix error: {error}")

        # Enhanced fix logic
        if "SyntaxError" in error:
            if "return a +" in error:
                # Fix the syntax error we intentionally introduced
                if "Syntax error for testing" in original_code:
                    fixed_code = original_code.replace("return a +  # Syntax error for testing", "return a + b")
                    return {
                        "description": description,
                        "code": fixed_code
                    }
                elif "Another syntax error for testing" in original_code:
                    fixed_code = original_code.replace("return a +  # Another syntax error for testing", "return a + b")
                    return {
                        "description": description,
                        "code": fixed_code
                    }
            elif "invalid syntax" in error:
                # Try to fix common syntax errors by adding missing parts
                if original_code.count("return") > original_code.count("b"):
                    fixed_code = original_code.replace("return a +", "return a + b")
                    return {
                        "description": description,
                        "code": fixed_code
                    }
            # Fallback - add a comment to make it syntactically valid
            fixed_code = original_code + "\n# Fixed syntax error"
            return {
                "description": description,
                "code": fixed_code
            }
        elif "NameError" in error:
            # Fix missing variable definitions
            if "not defined" in error:
                fixed_code = "b = 0\n" + original_code
                return {
                    "description": description,
                    "code": fixed_code
                }
        elif "TypeError" in error:
            # Fix type-related errors
            if "missing" in error and "positional argument" in error:
                # Add missing arguments
                fixed_code = original_code.replace("def add_numbers(a: int, b: int)", "def add_numbers(a: int = 0, b: int = 0)")
                return {
                    "description": description,
                    "code": fixed_code
                }

        # For other errors, just return the original code
        return code

    def _generate_code(self, subtask):
        """Generate code based on subtask description."""
        description = subtask["description"].lower()

        if "function signature" in description:
            return """def add_numbers(a: int, b: int) -> int:
    \"\"\"
    Add two numbers together.

    Args:
        a: First number
        b: Second number

    Returns:
        Sum of a and b
    \"\"\"
    return a + b
"""
        elif "function logic" in description:
            return """def add_numbers(a: int, b: int) -> int:
    \"\"\"
    Add two numbers together.

    Args:
        a: First number
        b: Second number

    Returns:
        Sum of a and b
    \"\"\"
    return a +  # Syntax error for testing
"""
        elif "input validation" in description:
            return """def add_numbers(a: int, b: int) -> int:
    \"\"\"
    Add two numbers together.

    Args:
        a: First number
        b: Second number

    Returns:
        Sum of a and b

    Raises:
        TypeError: If inputs are not integers
    \"\"\"
    if not isinstance(a, int) or not isinstance(b, int):
        raise TypeError("Both inputs must be integers")
    return a +  # Another syntax error for testing
"""
        elif "docstring" in description:
            return """def add_numbers(a: int, b: int) -> int:
    \"\"\"
    Add two numbers together.

    This function takes two integer inputs and returns their sum.
    It performs basic input validation to ensure both inputs are integers.

    Args:
        a: First number to add
        b: Second number to add

    Returns:
        Sum of a and b

    Raises:
        TypeError: If inputs are not integers

    Examples:
        >>> add_numbers(2, 3)
        5
        >>> add_numbers(-1, 1)
        0
    \"\"\"
    if not isinstance(a, int) or not isinstance(b, int):
        raise TypeError("Both inputs must be integers")
    return a + b
"""
        elif "class structure" in description:
            return """class Calculator:
    \"\"\"
    A simple calculator class that can perform basic arithmetic operations.
    \"\"\"

    def __init__(self):
        \"\"\"Initialize the calculator.\"\"\"
        pass
"""
        elif "implement methods" in description:
            return """class Calculator:
    \"\"\"
    A simple calculator class that can perform basic arithmetic operations.
    \"\"\"

    def __init__(self):
        \"\"\"Initialize the calculator.\"\"\"
        pass

    def add(self, a: int, b: int) -> int:
        \"\"\"
        Add two numbers.

        Args:
            a: First number
            b: Second number

        Returns:
            Sum of a and b
        \"\"\"
        return a + b

    def subtract(self, a: int, b: int) -> int:
        \"\"\"
        Subtract second number from first.

        Args:
            a: First number
            b: Second number

        Returns:
            Difference between a and b
        \"\"\"
        return a - b
"""
        else:
            return """# Basic implementation
def example_function():
    \"\"\"
    Example function that demonstrates basic functionality.
    \"\"\"
    return "Hello, World!"
"""

