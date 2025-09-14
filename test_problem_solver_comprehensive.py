

"""
Comprehensive test for the problem solver with different types of problems.
"""

import asyncio
import os
import sys
import shutil
from problem_solver.problem_solver import ProblemSolver, ProblemContext
from analyst import Analyst
from developer import Developer
from tester import Tester
from agent_registry import AgentRegistry

async def test_add_function():
    """Test creating an add function."""
    print("🧪 Testing Problem Solver with add function...")

    # Register agents
    AgentRegistry.register("analyst", Analyst, version="2.0", description="Task analysis agent")
    AgentRegistry.register("developer", Developer, version="2.0", description="Code development agent")
    AgentRegistry.register("tester", Tester, version="2.0", description="Code testing agent")

    # Create a temporary repository
    repo_path = "/tmp/test_repo"
    os.makedirs(repo_path, exist_ok=True)

    # Create a simple README file
    with open(os.path.join(repo_path, "README.md"), "w") as f:
        f.write("# Test Repository\n\nThis is a test repository for problem solving.")

    # Create problem context
    problem_context = ProblemContext(
        problem_id="test_add_001",
        problem_type="task",
        title="Create a Python function named add",
        description="Create a Python function named add that takes two numbers and returns their sum",
        repository_path=repo_path
    )

    # Create problem solver
    solver = ProblemSolver()

    # Run the problem solver
    result = await solver.solve_problem(problem_context)

    # Check if the function was created
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
                print("✅ Add function created successfully!")
                with open(solution_file, "r") as f:
                    content = f.read()
                    print("File content:")
                    print(content)

                    # Verify the function contains 'add'
                    if "def add" in content and "return a + b" in content:
                        print("✅ Function implementation is correct!")
                        return True
                    else:
                        print("❌ Function implementation is incorrect")
                        return False
            else:
                print("❌ Function file not created")
                return False
        else:
            print("❌ No problem directories found in workspace")
            return False
    else:
        print("❌ Workspace directory not found")
        return False

async def test_subtract_function():
    """Test creating a subtract function."""
    print("\n🧪 Testing Problem Solver with subtract function...")

    # Register agents
    AgentRegistry.register("analyst", Analyst, version="2.0", description="Task analysis agent")
    AgentRegistry.register("developer", Developer, version="2.0", description="Code development agent")
    AgentRegistry.register("tester", Tester, version="2.0", description="Code testing agent")

    # Create a temporary repository
    repo_path = "/tmp/test_repo2"
    os.makedirs(repo_path, exist_ok=True)

    # Create a simple README file
    with open(os.path.join(repo_path, "README.md"), "w") as f:
        f.write("# Test Repository 2\n\nThis is a test repository for problem solving.")

    # Create problem context
    problem_context = ProblemContext(
        problem_id="test_subtract_001",
        problem_type="task",
        title="Create a Python function named subtract",
        description="Create a Python function named subtract that takes two numbers and returns their difference",
        repository_path=repo_path
    )

    # Create problem solver
    solver = ProblemSolver()

    # Run the problem solver
    result = await solver.solve_problem(problem_context)

    # Check if the function was created
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
                print("✅ Subtract function created successfully!")
                with open(solution_file, "r") as f:
                    content = f.read()
                    print("File content:")
                    print(content)

                    # Verify the function contains 'subtract'
                    if "def subtract" in content and "return a - b" in content:
                        print("✅ Function implementation is correct!")
                        return True
                    else:
                        print("❌ Function implementation is incorrect")
                        return False
            else:
                print("❌ Function file not created")
                return False
        else:
            print("❌ No problem directories found in workspace")
            return False
    else:
        print("❌ Workspace directory not found")
        return False

async def run_tests():
    """Run all tests."""
    print("Running comprehensive problem solver tests...")

    # Clean up workspace first
    workspace_path = "/tmp/multi_agent_workspace"
    if os.path.exists(workspace_path):
        shutil.rmtree(workspace_path)

    # Run tests
    test1_result = await test_add_function()
    test2_result = await test_subtract_function()

    # Summary
    print("\n📊 Test Results:")
    print(f"Add function test: {'✅ PASSED' if test1_result else '❌ FAILED'}")
    print(f"Subtract function test: {'✅ PASSED' if test2_result else '❌ FAILED'}")

    if test1_result and test2_result:
        print("\n🎉 All tests passed!")
    else:
        print("\n❌ Some tests failed")

    return test1_result and test2_result

if __name__ == "__main__":
    asyncio.run(run_tests())

