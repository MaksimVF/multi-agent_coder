


"""
Demo of the problem solver capabilities.
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

async def demo_problem_solver():
    """Demo the problem solver with various tasks."""
    print("🎯 Demo: Multi-Agent Problem Solver")
    print("=" * 50)

    # Register agents
    AgentRegistry.register("analyst", Analyst, version="2.0", description="Task analysis agent")
    AgentRegistry.register("developer", Developer, version="2.0", description="Code development agent")
    AgentRegistry.register("tester", Tester, version="2.0", description="Code testing agent")

    # Clean up workspace first
    workspace_path = "/tmp/multi_agent_workspace"
    if os.path.exists(workspace_path):
        shutil.rmtree(workspace_path)

    # Create problem solver
    solver = ProblemSolver()

    # Demo 1: Create an add function
    print("\n🧩 Task 1: Create an add function")
    print("-" * 30)

    repo_path = "/tmp/demo_repo"
    os.makedirs(repo_path, exist_ok=True)
    with open(os.path.join(repo_path, "README.md"), "w") as f:
        f.write("# Demo Repository\n\nDemo for problem solver.")

    problem_context = ProblemContext(
        problem_id="demo_add",
        problem_type="task",
        title="Create a Python function named add",
        description="Create a Python function named add that takes two numbers and returns their sum",
        repository_path=repo_path
    )

    result = await solver.solve_problem(problem_context)

    # Show results
    if result['success']:
        # Find the solution file
        problem_dirs = []
        for item in os.listdir(workspace_path):
            if item.startswith("problem_"):
                problem_dirs.append(item)

        if problem_dirs:
            problem_dirs.sort()
            most_recent = problem_dirs[-1]
            solution_file = os.path.join(workspace_path, most_recent, "solution.py")

            if os.path.exists(solution_file):
                with open(solution_file, "r") as f:
                    content = f.read()
                    print("✅ Solution created:")
                    print(content)
    else:
        print(f"❌ Failed: {result['message']}")

    # Demo 2: Create a subtract function
    print("\n🧩 Task 2: Create a subtract function")
    print("-" * 30)

    repo_path2 = "/tmp/demo_repo2"
    os.makedirs(repo_path2, exist_ok=True)
    with open(os.path.join(repo_path2, "README.md"), "w") as f:
        f.write("# Demo Repository 2\n\nDemo for problem solver.")

    problem_context2 = ProblemContext(
        problem_id="demo_subtract",
        problem_type="task",
        title="Create a Python function named subtract",
        description="Create a Python function named subtract that takes two numbers and returns their difference",
        repository_path=repo_path2
    )

    result2 = await solver.solve_problem(problem_context2)

    # Show results
    if result2['success']:
        # Find the solution file
        problem_dirs = []
        for item in os.listdir(workspace_path):
            if item.startswith("problem_"):
                problem_dirs.append(item)

        if problem_dirs:
            problem_dirs.sort()
            most_recent = problem_dirs[-1]
            solution_file = os.path.join(workspace_path, most_recent, "solution.py")

            if os.path.exists(solution_file):
                with open(solution_file, "r") as f:
                    content = f.read()
                    print("✅ Solution created:")
                    print(content)
    else:
        print(f"❌ Failed: {result2['message']}")

    # Demo 3: Create a multiply function
    print("\n🧩 Task 3: Create a multiply function")
    print("-" * 30)

    repo_path3 = "/tmp/demo_repo3"
    os.makedirs(repo_path3, exist_ok=True)
    with open(os.path.join(repo_path3, "README.md"), "w") as f:
        f.write("# Demo Repository 3\n\nDemo for problem solver.")

    problem_context3 = ProblemContext(
        problem_id="demo_multiply",
        problem_type="task",
        title="Create a Python function named multiply",
        description="Create a Python function named multiply that takes two numbers and returns their product",
        repository_path=repo_path3
    )

    result3 = await solver.solve_problem(problem_context3)

    # Show results
    if result3['success']:
        # Find the solution file
        problem_dirs = []
        for item in os.listdir(workspace_path):
            if item.startswith("problem_"):
                problem_dirs.append(item)

        if problem_dirs:
            problem_dirs.sort()
            most_recent = problem_dirs[-1]
            solution_file = os.path.join(workspace_path, most_recent, "solution.py")

            if os.path.exists(solution_file):
                with open(solution_file, "r") as f:
                    content = f.read()
                    print("✅ Solution created:")
                    print(content)
    else:
        print(f"❌ Failed: {result3['message']}")

    # Summary
    print("\n📊 Demo Summary")
    print("=" * 50)
    print(f"Task 1 (Add): {'✅ SUCCESS' if result['success'] else '❌ FAILED'}")
    print(f"Task 2 (Subtract): {'✅ SUCCESS' if result2['success'] else '❌ FAILED'}")
    print(f"Task 3 (Multiply): {'✅ SUCCESS' if result3['success'] else '❌ FAILED'}")

    total_success = sum([result['success'], result2['success'], result3['success']])
    print(f"\n🎯 Overall: {total_success}/3 tasks completed successfully")

    if total_success == 3:
        print("\n🎉 All tasks completed successfully!")
        print("The problem solver is working correctly and can handle multiple types of tasks.")
    else:
        print(f"\n⚠️  {3 - total_success} tasks failed. Please check the implementation.")

if __name__ == "__main__":
    asyncio.run(demo_problem_solver())

