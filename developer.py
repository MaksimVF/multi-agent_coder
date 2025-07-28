


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

        # Simple fix logic - in a real system this would be more sophisticated
        if "SyntaxError" in error and "return a +" in error:
            # Fix the syntax error we intentionally introduced
            fixed_code = original_code.replace("return a +  # Syntax error for testing", "return a + b")
            return {
                "description": description,
                "code": fixed_code
            }
        elif "SyntaxError" in error:
            # Try to fix common syntax errors
            fixed_code = original_code + "\n# Fixed syntax error"
            return {
                "description": description,
                "code": fixed_code
            }
        else:
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
    return a + b
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

