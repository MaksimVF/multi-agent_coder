


# Multi-Agent Coder

**Advanced AI-Powered Code Generation System with Enhanced Architecture**

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

### Enhanced Architecture

- **Agent Registry**: Dynamic agent registration and discovery
- **Event System**: Decoupled event-driven communication
- **Advanced Code Generation**: Iterative refinement and validation
- **Memory Management**: Short-term and long-term memory integration

## New Architecture

```
[User Task] → [Agent Registry] → [Event Bus] → [Enhanced Workflow] → [Final Code]
               ↑                  ↑                  ↑                  ↑
            [Dynamic]         [Decoupled]        [Advanced]         [Memory]
           Discovery          Events            Code Gen          Integration
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

### Advanced Usage with New Features

```python
from agent_registry import AgentRegistry
from event_system import EventBus, EventType
from advanced_code_generator import AdvancedCodeGenerator
from analyst import Analyst
from developer import Developer
from tester import Tester
from optimizer import Optimizer
import asyncio

async def enhanced_workflow():
    # Initialize event bus
    event_bus = EventBus()

    # Register agents
    AgentRegistry.register("analyst", Analyst, version="2.0")
    AgentRegistry.register("developer", Developer, version="2.0")
    AgentRegistry.register("tester", Tester, version="2.0")
    AgentRegistry.register("optimizer", Optimizer, version="2.0")

    # Initialize agents
    analyst = Analyst(temperature=0.5)
    developer = Developer(temperature=0.7)
    tester = Tester(temperature=0.3)
    optimizer = Optimizer(temperature=0.5)

    # Use advanced code generator
    code_generator = AdvancedCodeGenerator()

    # Analyze task
    task = "Create a Python function to calculate factorial"
    subtasks = await analyst.analyze_task(task)

    # Generate code with advanced generator
    code_artifacts = []
    for subtask in subtasks:
        code = await code_generator.generate_code(
            requirements=subtask,
            language="python"
        )
        code_artifacts.append(code)

    # Generate tests
    test_results = []
    for code in code_artifacts:
        tests = await code_generator.generate_unit_tests(
            code=code["code"],
            requirements=code["metadata"]["requirements"]
        )
        test_results.append(tests)

    # Optimize code
    optimized_code = []
    for code in code_artifacts:
        optimized = await code_generator.optimize_code(
            code=code["code"],
            requirements=code["metadata"]["requirements"]
        )
        optimized_code.append(optimized)

    return optimized_code

# Run the enhanced workflow
result = asyncio.run(enhanced_workflow())
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
- [x] **Enhanced error handling and recovery**
- [x] **Dynamic agent registration**
- [x] **Event-driven architecture**
- [x] **Advanced code generation**
- [ ] Multi-language support
- [ ] Performance benchmarking
- [ ] Cloud deployment templates

## Contact

For questions or support, please open an issue on GitHub.


