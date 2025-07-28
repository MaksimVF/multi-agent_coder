
# Multi-Agent Coder

A multi-agent system for coding tasks with three agents: Analyst, Developer, and Tester.

## Features

- **Analyst**: Breaks down tasks into subtasks
- **Developer**: Writes code for each subtask
- **Tester**: Tests the code and provides feedback
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

Run the system with a task description:

```bash
python main.py --task "Write a function to add two numbers"
```

Example output:

```
🔍 Analyst is analyzing the task...
Analyzing task: Write a function to add two numbers
Identified 4 subtasks:
  - Define function signature
  - Implement function logic
  - Add input validation
  - Write docstring

💻 Developer is working on the code...

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

- `main.py`: Entry point with CLI interface
- `analyst.py`: Analyst agent implementation
- `developer.py`: Developer agent implementation
- `tester.py`: Tester agent implementation

## Future Improvements

- Add more sophisticated task analysis
- Implement feedback loop for failed tests
- Add support for different programming languages
- Integrate with version control systems
- Add more comprehensive testing capabilities

## License

MIT
