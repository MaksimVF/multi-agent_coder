


"""
Test script for the Problem Solver
"""

import asyncio
import os
import json
from problem_solver import ProblemSolver, ProblemContext

async def test_problem_solver():
    """Test the problem solver with a simple problem"""

    print("🧪 Testing Problem Solver...")

    # Create a problem solver
    problem_solver = ProblemSolver({
        'max_iterations': 5,
        'output_dir': 'test_problem_solver_output'
    })

    # Define a simple problem
    problem_context = ProblemContext(
        problem_id="test_problem_1",
        problem_type="task",
        title="Create Math Function",
        description="Create a Python function named 'add' in a file called 'solution.py' that takes two numbers and returns their sum. The function should handle edge cases and include type hints.",
        repository_path=os.getcwd()
    )

    # Solve the problem
    print("  - Solving test problem...")
    result = await problem_solver.solve_problem(problem_context)

    # Print results
    print("\n📊 Problem Solver Test Results:")
    print(f"  - Success: {result.get('success', False)}")
    print(f"  - Iterations: {result.get('iterations', 0)}")
    print(f"  - Agents Used: {', '.join(result.get('agents_used', []))}")
    print(f"  - Changes Made: {len(result.get('changes', []))}")

    # Save results
    output_file = os.path.join('test_problem_solver_output', 'test_result.json')
    with open(output_file, 'w') as f:
        json.dump(result, f, indent=2)

    print(f"  - Results saved to: {output_file}")

    return result

if __name__ == "__main__":
    asyncio.run(test_problem_solver())


