


# Multi-Agent Coder

**Advanced AI-Powered Code Generation System**

## Overview

Multi-Agent Coder is a sophisticated AI-driven system that leverages multiple intelligent agents to analyze, develop, test, and optimize code. The system uses LLM (Large Language Model) integration through LiteLLM and coordinates agents using LangGraph for efficient workflow management.

## Features

### Core Agents

1. **Analyst Agent**: Advanced task analysis with AI/ML capabilities
   - Detailed subtask breakdown with metadata
   - Machine learning analysis for task assessment
   - Embedding generation and similarity search
   - Risk assessment and skill requirements identification

2. **Developer Agent**: Intelligent code generation
   - Context-aware code generation
   - Multiple implementation approaches
   - Error handling and edge case management

3. **Tester Agent**: Comprehensive testing capabilities
   - Unit test generation
   - Test execution and validation
   - Test coverage analysis

4. **Optimizer Agent**: Code optimization and enhancement
   - Performance optimization
   - Code quality improvement
   - Best practice implementation

5. **Researcher Agent**: Web research and documentation
   - Online information retrieval
   - Documentation generation
   - Best practice research

### Advanced Capabilities

- **LLM Integration**: All agents leverage language models for intelligent decision making
- **LangGraph Workflow**: Coordinated agent collaboration using graph-based workflows
- **Mock Mode**: Graceful fallback when no API key is available
- **CI/CD Integration**: Automated testing and deployment pipeline

## Architecture

```
[User Task] → [Analyst] → [Developer] → [Tester] → [Optimizer] → [Final Code]
               ↑            ↑            ↑            ↑
              ML           LLM          LLM          LLM
            Analysis      Code Gen     Testing      Optimization
```

## Installation

```bash
# Clone the repository
git clone https://github.com/MaksimVF/multi-agent_coder.git
cd multi-agent_coder

# Install dependencies
pip install -r requirements.txt

# Set up environment variables (optional for LLM access)
export OPENAI_API_KEY='your-api-key'
export LITELLM_API_KEY='your-api-key'
```

## Usage

### Basic Usage

```bash
python main.py "Create a Python function to calculate factorial"
```

### Advanced Usage

```python
from analyst import Analyst
from developer import Developer
from tester import Tester
from optimizer import Optimizer
import asyncio

async def main():
    # Initialize agents
    analyst = Analyst(temperature=0.5)
    developer = Developer(temperature=0.7)
    tester = Tester(temperature=0.3)
    optimizer = Optimizer(temperature=0.5)

    # Analyze task
    task = "Create a Python function to calculate factorial"
    subtasks = await analyst.analyze_task(task)

    # Develop code
    code_artifacts = []
    for subtask in subtasks:
        code = await developer.develop_code(subtask, "python")
        code_artifacts.append(code)

    # Test code
    test_results = []
    for code in code_artifacts:
        tests = await tester.generate_tests(code)
        test_results.append(tests)

    # Optimize code
    optimized_code = []
    for code in code_artifacts:
        optimized = await optimizer.optimize_code(code)
        optimized_code.append(optimized)

    return optimized_code

# Run the workflow
result = asyncio.run(main())
```

## Testing

Run the comprehensive test suite:

```bash
python test_llm_agents.py
```

## CI/CD

The project includes a GitHub Actions workflow for automated testing:

- Python version matrix testing (3.9, 3.10, 3.11)
- Linting with flake8
- Code formatting with black
- Security scanning with bandit

## Configuration

Create a `.env` file for LLM configuration:

```
OPENAI_API_KEY=your_openai_key
LITELLM_API_KEY=your_litellm_key
MODEL=gpt-4o
TEMPERATURE=0.7
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a new Pull Request

## License

This project is licensed under the MIT License.

## Roadmap

- [x] LLM integration for all agents
- [x] LangGraph workflow coordination
- [x] Advanced task analysis with ML
- [x] CI/CD pipeline integration
- [ ] Enhanced error handling and recovery
- [ ] Multi-language support
- [ ] Performance benchmarking
- [ ] Cloud deployment templates

## Contact

For questions or support, please open an issue on GitHub.


