



"""
Main entry point for the Problem Solver
"""

import asyncio
import argparse
import json
import os
from typing import Dict, Any

from .problem_solver import ProblemSolver, ProblemContext
from .issue_handler import IssueHandlerFactory

def main():
    """Main function to run the problem solver"""
    parser = argparse.ArgumentParser(description='Multi-Agent Problem Solver')
    parser.add_argument('--platform', type=str, choices=['github', 'gitlab'], help='Issue platform')
    parser.add_argument('--owner', type=str, help='Repository owner')
    parser.add_argument('--repo', type=str, help='Repository name')
    parser.add_argument('--token', type=str, help='Access token')
    parser.add_argument('--issue-number', type=int, help='Issue number to solve')
    parser.add_argument('--problem-type', type=str, choices=['issue', 'bug', 'task', 'performance', 'security'],
                       default='issue', help='Type of problem to solve')
    parser.add_argument('--repository-path', type=str, default='.', help='Path to local repository')
    parser.add_argument('--output-dir', type=str, default='problem_solver_output', help='Output directory')
    parser.add_argument('--max-iterations', type=int, default=20, help='Maximum iterations for solving')

    args = parser.parse_args()

    # Create problem solver
    config = {
        'output_dir': args.output_dir,
        'max_iterations': args.max_iterations,
        'workspace_base': os.path.join(args.output_dir, 'workspaces')
    }

    problem_solver = ProblemSolver(config)

    if args.platform and args.owner and args.repo and args.issue_number:
        # Handle issue from GitHub/GitLab
        issue_handler = IssueHandlerFactory.create_handler(
            args.platform,
            args.owner,
            args.repo,
            args.token
        )

        # Get issue details
        issue = issue_handler.get_issue(args.issue_number)

        # Create problem context
        problem_context = ProblemContext(
            problem_id=f"{args.platform}_issue_{args.issue_number}",
            problem_type=args.problem_type,
            title=issue.title,
            description=issue.body,
            repository_path=args.repository_path,
            additional_context={
                'platform': args.platform,
                'owner': args.owner,
                'repo': args.repo,
                'issue_number': args.issue_number,
                'comments': issue.comments
            }
        )

        # Solve the problem
        result = asyncio.run(problem_solver.solve_problem(problem_context))

        # Output results
        output_file = os.path.join(args.output_dir, f"problem_{args.issue_number}_result.json")
        with open(output_file, 'w') as f:
            json.dump(result, f, indent=2)

        print(f"Problem solving completed. Results saved to {output_file}")

        # Post results as comment
        summary = result.get('summary', {})
        comment = (
            f"## Problem Solving Results\n\n"
            f"**Problem**: {summary.get('title', 'Unknown')}\n"
            f"**Status**: {'✅ Solved' if summary.get('success') else '❌ Not solved'}\n"
            f"**Iterations**: {summary.get('iterations', 0)}\n"
            f"**Agents Used**: {', '.join(summary.get('agents_used', []))}\n"
        )

        issue_handler.create_comment(args.issue_number, comment)
        print(f"Comment posted to issue #{args.issue_number}")

    else:
        # Handle local problem
        problem_context = ProblemContext(
            problem_id="local_problem_1",
            problem_type=args.problem_type,
            title="Local Problem",
            description="Solve a local coding problem",
            repository_path=args.repository_path
        )

        # Solve the problem
        result = asyncio.run(problem_solver.solve_problem(problem_context))

        # Output results
        output_file = os.path.join(args.output_dir, "local_problem_result.json")
        with open(output_file, 'w') as f:
            json.dump(result, f, indent=2)

        print(f"Local problem solving completed. Results saved to {output_file}")

if __name__ == '__main__':
    main()


