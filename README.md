

# Multi-Agent Coder

A multi-agent system for coding tasks with five agents: Analyst, Developer, Tester, Optimizer, and Researcher.

## Features

- **Analyst**: Breaks down tasks into subtasks
- **Developer**: Writes code for each subtask in multiple languages
- **Tester**: Tests the code and provides feedback in the appropriate language
- **Feedback Loop**: Automatically fixes failed tests (up to 2 retries)
- **Multi-language Support**: Python, JavaScript, Java, C#
- **Version Control Integration**: Automatically commits generated code to Git
- Uses asyncio for parallel execution
- **Optimizer**: Analyzes all agents' work and suggests improvements
- **Researcher**: Fetches documentation, examples, and best practices from the web
- **Self-Improvement**: Optimizer logs improvements and learns over time
- Simple CLI interface

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/MaksimVF/multi-agent_coder.git
   cd multi-agent_coder
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the system with a task description and optional language:

```bash
# Default (Python)
python main.py --task "Write a function to add two numbers"

# JavaScript
python main.py --task "Write a function to add two numbers" --language javascript

# Java
python main.py --task "Write a function to add two numbers" --language java

# C#
python main.py --task "Write a function to add two numbers" --language csharp
```

### Version Control Features

Create a new Git branch and push changes:

```bash
python main.py --task "Write a function to add two numbers" --branch feature/add-function --push
```

This will:
1. Initialize Git repo if not already initialized
2. Set up Git config
3. Commit the generated code
4. Create and checkout a new branch
5. Push changes to the remote repository




### Advanced Testing Features

The system supports comprehensive testing capabilities with multiple test types:

- **Basic testing** (default): Simple execution test
- **Unit testing**: Creates and runs comprehensive unit tests with mocking (Python only)
- **Integration testing**: Tests component interactions and data flow
- **Performance testing**: Measures execution time and memory usage
- **Coverage testing**: Measures code coverage percentage
- **Security testing**: Detects common security vulnerabilities

Use the `--test-type` parameter:

```bash
# Unit testing
python main.py --task "Write a function to add two numbers" --test-type unit

# Performance testing
python main.py --task "Write a function to add two numbers" --test-type performance

# Integration testing
python main.py --task "Write a function to add two numbers" --test-type integration

# Coverage testing
python main.py --task "Write a function to add two numbers" --test-type coverage

# Security testing
python main.py --task "Write a function to add two numbers" --test-type security
```

Example output with enhanced metrics:

```
📋 Final Results:
1. ✅ Passed: Define function signature and parameters (basic)
2. ✅ Passed: Implement core function logic (unit)
3. ✅ Passed: Handle file operations safely (integration)
4. ✅ Passed: Add input validation and error handling (performance)
   📊 Performance: 12.45 ms
   📊 Memory Usage: 1024.00 KB
5. ✅ Passed: Write comprehensive docstring with examples (coverage)
   📊 Coverage: 95.2% (40/42 lines)
6. ✅ Passed: Add type hints and annotations (security)
   🔒 Security Issues: 0 found
```

### Testing Features Details

1. **Unit Testing**: Automatically generates comprehensive unit tests with:
   - Basic functionality tests
   - Edge case testing
   - Error handling verification
   - Mocking capabilities for dependencies

2. **Performance Testing**: Measures key performance metrics:
   - Execution time in milliseconds
   - Memory usage in kilobytes
   - Timeout detection

3. **Integration Testing**: Verifies component interactions:
   - Tests how functions work together
   - Validates data flow through the system
   - Verifies module integration

4. **Coverage Testing**: Provides code coverage analysis:
   - Measures percentage of code covered
   - Reports covered vs total lines
   - Identifies untested code paths

5. **Security Testing**: Detects common vulnerabilities:
   - eval() usage detection
   - Hardcoded credential detection
   - SQL injection patterns
   - Other security anti-patterns

6. **Error Handling**: Enhanced error reporting:
   - Detailed error messages
   - Full traceback information
   - Standard output/error separation

All test results are saved to `results.json` with comprehensive metrics for each test case.

```
🔍 Analyst is analyzing the task...
Analyzing task: Write a function to add two numbers
Identified 4 subtasks:
  - Define function signature
  - Implement function logic
  - Add input validation
  - Write docstring

💻 Developer is working on the code (python)...

🧪 Tester is testing the code...
✅ Test passed for code: Define function signature
✅ Test passed for code: Implement function logic
✅ Test passed for code: Add input validation
✅ Test passed for code: Write docstring

📋 Final Results:
1. ✅ Passed: Define function signature
2. ✅ Passed: Implement function logic
3. ✅ Passed: Add input validation
4. ✅ Passed: Write docstring

💾 Results saved to results.json
```

## Architecture

- `main.py`: Entry point with CLI interface and language support
- `analyst.py`: Analyst agent implementation
- `developer.py`: Developer agent with multi-language code generation
- `optimizer.py`: Optimizer agent for code analysis and improvement
- `researcher.py`: Researcher agent for web research and documentation
- `tester.py`: Tester agent with multi-language testing capabilities

## Supported Languages

- **Python**: Tested with python command
- **JavaScript**: Tested with node command
- **Java**: Requires javac and java commands (compilation + execution)
- **C#**: Requires dotnet command (basic support)

## Future Improvements

- Add more sophisticated task analysis with AI/ML
- Enhance feedback loop for non-Python languages
- Improve Java and C# testing support with native test frameworks
- Add support for additional languages (Go, Rust, etc.)
- Integrate with CI/CD pipelines for automated testing
- Add test result visualization and reporting
- Implement property-based testing
- Add support for test-driven development (TDD) workflows

## License

MIT
