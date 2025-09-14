
"""
Test the problem solver with a full workflow.
"""

import asyncio
import os
import sys
from problem_solver.problem_solver import ProblemSolver, ProblemContext
from analyst import Analyst
from developer import Developer
from tester import Tester
from agent_registry import AgentRegistry

async def test_problem_solver():
    """Test the problem solver with a simple task."""
    print("🧪 Testing Problem Solver with full workflow...")

    # Register agents
    AgentRegistry.register("analyst", Analyst, version="2.0", description="Task analysis agent")
    AgentRegistry.register("developer", Developer, version="2.0", description="Code development agent")
    AgentRegistry.register("tester", Tester, version="2.0", description="Code testing agent")

    # Create a temporary directory for the test
    test_dir = "/tmp/test_problem_solver"
    os.makedirs(test_dir, exist_ok=True)

    # Create a simple test file
    test_file = os.path.join(test_dir, "test.py")
    with open(test_file, "w") as f:
        f.write("# Test file\nprint('Hello, world!')\n")

    # Create problem context
    problem_context = ProblemContext(
        problem_id="test_001",
        problem_type="task",
        title="Create a Python function named add",
        description="Create a Python function named add that takes two numbers and returns their sum",
        repository_path=test_dir
    )

    # Create problem solver
    solver = ProblemSolver()

    # Run the problem solver
    result = await solver.solve_problem(problem_context)

    # Print results
    print(f"Problem solving result: {result['success']}")
    print(f"Message: {result['message']}")
    print(f"Iterations: {result['iterations']}")
    print(f"Agents used: {result['agents_used']}")

    # Check if the function was created in the workspace
    workspace_path = "/tmp/multi_agent_workspace"
    if os.path.exists(workspace_path):
        # Find the most recent problem directory
        problem_dirs = []
        for item in os.listdir(workspace_path):
            if item.startswith("problem_"):
                problem_dirs.append(item)

        if problem_dirs:
            # Sort by problem number
            problem_dirs.sort()
            most_recent = problem_dirs[-1]
            solution_file = os.path.join(workspace_path, most_recent, "solution.py")

            if os.path.exists(solution_file):
                print("✅ Function file created successfully!")
                with open(solution_file, "r") as f:
                    print("File content:")
                    print(f.read())
            else:
                print("❌ Function file not created in workspace")
        else:
            print("❌ No problem directories found in workspace")
    else:
        print("❌ Workspace directory not found")

    # Clean up
    import shutil
    shutil.rmtree(test_dir)

    return result

if __name__ == "__main__":
    asyncio.run(test_problem_solver())
