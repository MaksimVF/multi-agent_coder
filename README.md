

# Multi-Agent Coder

A multi-agent system for coding tasks with three agents: Analyst, Developer, and Tester.

## Features

- **Analyst**: Breaks down tasks into subtasks
- **Developer**: Writes code for each subtask in multiple languages
- **Tester**: Tests the code and provides feedback in the appropriate language
- **Feedback Loop**: Automatically fixes failed tests (up to 2 retries)
- **Multi-language Support**: Python, JavaScript, Java, C#
- **Version Control Integration**: Automatically commits generated code to Git
- Uses asyncio for parallel execution
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

The system supports different types of testing:

- **Basic testing** (default): Simple execution test
- **Unit testing**: Creates and runs unit tests (Python only for now)
- **Integration testing**: Tests component interactions
- **Performance testing**: Measures execution time

Use the `--test-type` parameter:

```bash
# Unit testing
python main.py --task "Write a function to add two numbers" --test-type unit

# Performance testing
python main.py --task "Write a function to add two numbers" --test-type performance

# Integration testing
python main.py --task "Write a function to add two numbers" --test-type integration
```

Example output:

```
📋 Final Results:
1. ✅ Passed: Define function signature and parameters
2. ✅ Passed: Implement core function logic
3. ✅ Passed: Handle file operations safely
4. ✅ Passed: Add input validation and error handling
5. ✅ Passed: Write comprehensive docstring with examples
6. ✅ Passed: Add type hints and annotations
   Performance: 25.37 ms
```

### Testing Features Details

1. **Unit Testing**: Automatically generates and runs unit tests for Python code
2. **Performance Testing**: Measures execution time in milliseconds
3. **Integration Testing**: Tests interactions between components
4. **Error Handling**: Provides detailed error messages for failed tests

All test results are saved to `results.json` with detailed information about each test case.

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
- `tester.py`: Tester agent with multi-language testing capabilities

## Supported Languages

- **Python**: Tested with python command
- **JavaScript**: Tested with node command
- **Java**: Requires javac and java commands (compilation + execution)
- **C#**: Requires dotnet command (basic support)

## Future Improvements

- Add more sophisticated task analysis
- Enhance feedback loop for non-Python languages
- Improve Java and C# testing support
- Integrate with version control systems
- Add more comprehensive testing capabilities

## License

MIT
