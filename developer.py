



import json
from typing import Dict, Any, Optional
from base_llm_agent import BaseLLMAgent

class Developer(BaseLLMAgent):
    """LLM-powered Developer agent for code generation and fixing."""

    def __init__(self, model: str = "gpt-4o", temperature: float = 0.7, memory_manager: Optional["MemoryManager"] = None):
        """
        Initialize the LLM-powered Developer.

        Args:
            model: LLM model to use
            temperature: Creativity level for LLM
            memory_manager: Memory manager for agent memory
        """
        super().__init__(model=model, temperature=temperature, memory_manager=memory_manager)

        # Developer-specific configuration
        self.system_message = (
            "You are an expert software developer. Your job is to generate high-quality code "
            "based on task descriptions, fix coding errors, and implement best practices."
        )

    async def develop_code(self, subtask: Dict[str, Any], language: str = "python") -> Dict[str, Any]:
        """Develop code for a given subtask using LLM."""
        description = subtask.get("description", "")

        prompt = f"""
        Generate {language} code for the following task:

        Task: {description}

        Provide the code as a JSON object with these fields:
        - description: Brief description of what the code does
        - code: The actual code implementation
        - language: The programming language used
        """

        print(f"💻 Generating {language} code for: {description}")

        response = await self.generate_response(prompt, self.system_message)

        try:
            code_data = json.loads(response)
            return code_data
        except json.JSONDecodeError:
            # Fallback: extract code from response
            return {
                "description": description,
                "code": response,
                "language": language
            }

    async def fix_code(self, code: Dict[str, Any], error: str, language: str = "python") -> Dict[str, Any]:
        """Fix code based on test error using LLM."""
        description = code.get("description", "")
        original_code = code.get("code", "")

        print(f"🛠️  Fixing code error with LLM: {error}")

        prompt = f"""
        Fix the following {language} code that has an error. Provide the corrected code.

        Original code:
        {original_code}

        Error:
        {error}

        Provide the fixed code as a JSON object with these fields:
        - description: Brief description of what the code does
        - code: The fixed code implementation
        - language: The programming language used
        - explanation: Brief explanation of what was fixed
        """

        response = await self.generate_response(prompt, self.system_message)

        try:
            fixed_code_data = json.loads(response)
            return fixed_code_data
        except json.JSONDecodeError:
            # Fallback: try to extract fixed code
            if "```" in response:
                # Extract code from code blocks
                code_blocks = response.split("```")
                if len(code_blocks) > 1:
                    fixed_code = code_blocks[1].strip()
                    return {
                        "description": description,
                        "code": fixed_code,
                        "language": language,
                        "explanation": "Attempted to fix the error"
                    }

            # If no code block found, return original with comment
            return {
                "description": description,
                "code": original_code + f"\n# Attempted fix for error: {error}",
                "language": language,
                "explanation": "Could not automatically fix the error"
            }

    async def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process incoming data for the workflow."""
        if "subtask" in data and "language" in data:
            code = await self.develop_code(data["subtask"], data["language"])
            return {"code": code}
        elif "code" in data and "error" in data and "language" in data:
            fixed_code = await self.fix_code(data["code"], data["error"], data["language"])
            return {"fixed_code": fixed_code}
        else:
            return {"error": "Insufficient data for code generation or fixing"}

    def _generate_code(self, subtask, language="python"):
        """Generate code based on subtask description."""
        description = subtask["description"].lower()

        if language == "python":
            return self._generate_python_code(description)
        elif language == "javascript":
            return self._generate_javascript_code(description)
        elif language == "java":
            return self._generate_java_code(description)
        elif language == "csharp":
            return self._generate_csharp_code(description)
        else:
            return self._generate_python_code(description)

    def _generate_python_code(self, description):
        """Generate Python code."""
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

    def _generate_javascript_code(self, description):
        """Generate JavaScript code."""
        if "function signature" in description:
            return """/**
 * Add two numbers together.
 *
 * @param {number} a - First number
 * @param {number} b - Second number
 * @returns {number} Sum of a and b
 */
function addNumbers(a, b) {
    return a + b;
}
"""
        elif "function logic" in description:
            return """/**
 * Add two numbers together.
 *
 * @param {number} a - First number
 * @param {number} b - Second number
 * @returns {number} Sum of a and b
 */
function addNumbers(a, b) {
    return a + b;
}
"""
        elif "input validation" in description:
            return """/**
 * Add two numbers together.
 *
 * @param {number} a - First number
 * @param {number} b - Second number
 * @returns {number} Sum of a and b
 * @throws {TypeError} If inputs are not numbers
 */
function addNumbers(a, b) {
    if (typeof a !== 'number' || typeof b !== 'number') {
        throw new TypeError('Both inputs must be numbers');
    }
    return a + b;
}
"""
        elif "class structure" in description:
            return """/**
 * A simple calculator class that can perform basic arithmetic operations.
 */
class Calculator {
    constructor() {
        // Initialize the calculator
    }
}
"""
        elif "implement methods" in description:
            return """/**
 * A simple calculator class that can perform basic arithmetic operations.
 */
class Calculator {
    constructor() {
        // Initialize the calculator
    }

    /**
     * Add two numbers.
     *
     * @param {number} a - First number
     * @param {number} b - Second number
     * @returns {number} Sum of a and b
     */
    add(a, b) {
        return a + b;
    }

    /**
     * Subtract second number from first.
     *
     * @param {number} a - First number
     * @param {number} b - Second number
     * @returns {number} Difference between a and b
     */
    subtract(a, b) {
        return a - b;
    }
}
"""
        else:
            return """// Basic implementation
function exampleFunction() {
    /**
     * Example function that demonstrates basic functionality.
     */
    return "Hello, World!";
}
"""

    def _generate_java_code(self, description):
        """Generate Java code."""
        if "function signature" in description or "function logic" in description:
            return """/**
 * Adds two numbers together.
 *
 * @param a First number
 * @param b Second number
 * @return Sum of a and b
 */
public int addNumbers(int a, int b) {
    return a + b;
}
"""
        elif "input validation" in description:
            return """/**
 * Adds two numbers together with validation.
 *
 * @param a First number
 * @param b Second number
 * @return Sum of a and b
 * @throws IllegalArgumentException If inputs are invalid
 */
public int addNumbers(int a, int b) {
    // Basic validation
    return a + b;
}
"""
        elif "class structure" in description:
            return """/**
 * A simple calculator class that can perform basic arithmetic operations.
 */
public class Calculator {
    public Calculator() {
        // Initialize the calculator
    }
}
"""
        elif "implement methods" in description:
            return """/**
 * A simple calculator class that can perform basic arithmetic operations.
 */
public class Calculator {
    public Calculator() {
        // Initialize the calculator
    }

    /**
     * Adds two numbers.
     *
     * @param a First number
     * @param b Second number
     * @return Sum of a and b
     */
    public int add(int a, int b) {
        return a + b;
    }

    /**
     * Subtracts second number from first.
     *
     * @param a First number
     * @param b Second number
     * @return Difference between a and b
     */
    public int subtract(int a, int b) {
        return a - b;
    }
}
"""
        else:
            return """// Basic implementation
public class Example {
    /**
     * Example method that demonstrates basic functionality.
     */
    public String exampleMethod() {
        return "Hello, World!";
    }
}
"""

    def _generate_csharp_code(self, description):
        """Generate C# code."""
        if "function signature" in description or "function logic" in description:
            return """/// <summary>
/// Adds two numbers together.
/// </summary>
/// <param name="a">First number</param>
/// <param name="b">Second number</param>
/// <returns>Sum of a and b</returns>
public int AddNumbers(int a, int b)
{
    return a + b;
}
"""
        elif "input validation" in description:
            return """/// <summary>
/// Adds two numbers together with validation.
/// </summary>
/// <param name="a">First number</param>
/// <param name="b">Second number</param>
/// <returns>Sum of a and b</returns>
/// <exception cref="ArgumentException">Thrown when inputs are invalid</exception>
public int AddNumbers(int a, int b)
{
    // Basic validation
    return a + b;
}
"""
        elif "class structure" in description:
            return """/// <summary>
/// A simple calculator class that can perform basic arithmetic operations.
/// </summary>
public class Calculator
{
    public Calculator()
    {
        // Initialize the calculator
    }
}
"""
        elif "implement methods" in description:
            return """/// <summary>
/// A simple calculator class that can perform basic arithmetic operations.
/// </summary>
public class Calculator
{
    public Calculator()
    {
        // Initialize the calculator
    }

    /// <summary>
    /// Adds two numbers.
    /// </summary>
    /// <param name="a">First number</param>
    /// <param name="b">Second number</param>
    /// <returns>Sum of a and b</returns>
    public int Add(int a, int b)
    {
        return a + b;
    }

    /// <summary>
    /// Subtracts second number from first.
    /// </summary>
    /// <param name="a">First number</param>
    /// <param name="b">Second number</param>
    /// <returns>Difference between a and b</returns>
    public int Subtract(int a, int b)
    {
        return a - b;
    }
}
"""
        else:
            return """// Basic implementation
public class Example
{
    /// <summary>
    /// Example method that demonstrates basic functionality.
    /// </summary>
    /// <returns>Greeting message</returns>
    public string ExampleMethod()
    {
        return "Hello, World!";
    }
}
"""

