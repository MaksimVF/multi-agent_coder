

# Multi-Agent Problem Solver

The Multi-Agent Problem Solver is a module for automatically handling issues, bugs, and tasks in software development projects using a collaborative multi-agent approach.

## Features

- **Automated Issue Resolution**: Connects to GitHub, GitLab, and other platforms to automatically resolve issues
- **Multi-Agent Collaboration**: Uses different specialized agents (analyst, developer, tester, etc.) to solve problems
- **Iterative Problem Solving**: Employs an iterative approach to refine solutions until problems are solved
- **Workspace Management**: Creates isolated workspaces for problem solving to avoid conflicts
- **Extensible Architecture**: Easy to add new agent types and problem-solving strategies

## Components

1. **ProblemSolver**: Main orchestrator that coordinates the problem-solving process
2. **IssueHandler**: Handles integration with issue tracking systems
3. **TaskProcessor**: Processes individual tasks within the problem-solving workflow
4. **AgentRegistry**: Manages different types of agents for various tasks

## Installation

The problem solver is part of the multi-agent_coder package. Install the package to use this module.

## Usage

### Command Line Interface

```bash
python -m problem_solver.main --platform github --owner myorg --repo myrepo \
    --token mytoken --issue-number 123 --problem-type bug
```

### Programmatic Usage

```python
from problem_solver import ProblemSolver, ProblemContext

# Create problem solver
problem_solver = ProblemSolver()

# Define problem context
problem_context = ProblemContext(
    problem_id="issue_123",
    problem_type="bug",
    title="Fix null pointer exception",
    description="The application crashes with a null pointer exception when...",
    repository_path="/path/to/repo"
)

# Solve the problem
result = await problem_solver.solve_problem(problem_context)

print(f"Problem solved: {result['success']}")
```

## Configuration

The problem solver can be configured with various options:

- `max_iterations`: Maximum number of iterations for solving a problem (default: 20)
- `output_dir`: Directory to store problem-solving results (default: 'problem_solver_output')
- `workspace_base`: Base directory for creating isolated workspaces (default: '/tmp/multi_agent_workspace')

## Extending the Problem Solver

You can extend the problem solver by:

1. **Adding New Agents**: Implement new agent types and register them in the AgentRegistry
2. **Customizing Problem-Solving Plans**: Modify the `_create_solving_plan` method to create custom workflows
3. **Enhancing Issue Handlers**: Add support for more issue tracking platforms by implementing new IssueHandlerInterface classes

## Example Workflow

1. **Issue Detection**: The system detects an issue from GitHub/GitLab or receives a local problem
2. **Workspace Setup**: Creates an isolated workspace for solving the problem
3. **Agent Initialization**: Initializes appropriate agents based on the problem type
4. **Problem Analysis**: Analyzes the problem and creates a solving plan
5. **Iterative Solving**: Executes the plan iteratively, refining the solution until the problem is solved
6. **Result Reporting**: Reports the results and creates a summary of the problem-solving process

## Contributing

Contributions to the problem solver are welcome! Please follow the project's contribution guidelines.

## License

This module is licensed under the same license as the multi-agent_coder project.

