
#!/usr/bin/env python3
import argparse
import asyncio
import json

import sys
import subprocess

from pathlib import Path

from analyst import Analyst
from developer import Developer
from tester import Tester
from optimizer import Optimizer
from researcher import Researcher
from vcs_manager import VCSManager
from agent_workflow import AgentWorkflow

async def main(task_description, language="python"):
    """Main function using LLM-powered agents and LangGraph workflow."""
    print("🚀 Starting Multi-Agent Coder with LLM Intelligence")

    # Create LLM-powered agents
    analyst = Analyst(temperature=0.5)
    developer = Developer(temperature=0.7)
    tester = Tester()
    researcher = Researcher()
    optimizer = Optimizer()
    optimizer.researcher = researcher  # Connect optimizer to researcher

    # Create agent workflow
    workflow = AgentWorkflow()
    workflow.register_agent("analyst", analyst)
    workflow.register_agent("developer", developer)
    workflow.register_agent("tester", tester)
    workflow.register_agent("optimizer", optimizer)

    # Define workflow edges
    workflow.add_edge("analyst", "developer")
    workflow.add_edge("developer", "tester")
    workflow.add_edge("tester", "optimizer")

    # Prepare initial data for workflow
    initial_data = {
        "task_description": task_description,
        "language": language,
        "test_type": args.test_type
    }

    # Execute the workflow
    print("\n🔄 Starting agent workflow...")
    workflow_result = await workflow.execute_workflow("analyst", initial_data)

    if workflow_result["status"] == "completed":
        print("\n✅ Workflow completed successfully!")

        # Extract final results
        final_results = workflow_result["data"]
        test_results = final_results.get("test_results", [])
        optimization_result = final_results.get("optimization_result", {})

        # Print final results
        print("\n📋 Final Results:")
        for i, result in enumerate(test_results, 1):
            status = "✅ Passed" if result["passed"] else "❌ Failed"
            print(f"{i}. {status}: {result['description']} ({result.get('test_type', 'basic')})")

            # Print additional metrics based on test type
            if "performance" in result:
                print(f"   📊 Performance: {result['performance']['execution_time_ms']:.2f} ms")
                if "memory_usage_kb" in result['performance']:
                    print(f"   📊 Memory Usage: {result['performance']['memory_usage_kb']:.2f} KB")

            if "coverage" in result:
                print(f"   📊 Coverage: {result['coverage']['percentage']:.1f}% "
                      f"({result['coverage']['covered_lines']}/{result['coverage']['total_lines']} lines)")

            if "security_issues" in result:
                print(f"   🔒 Security Issues: {len(result['security_issues'])} found")
                for issue in result['security_issues']:
                    print(f"      - {issue}")

            # Print error details if failed
            if not result["passed"]:
                print(f"   🔍 Error: {result['error']}")
                if "traceback" in result:
                    print(f"   🔍 Traceback: {result['traceback']}")

        # Print optimization results
        if optimization_result and optimization_result.get("success"):
            print("\n💡 Optimization Results:")
            print(f"   📊 Analysis: {len(optimization_result['suggestions'])} suggestions generated")

            # Print top suggestions
            for i, suggestion in enumerate(optimization_result['suggestions'][:3], 1):
                print(f"   {i}. {suggestion['type']}: {suggestion['details']}")

        return final_results
    else:
        print(f"❌ Workflow failed: {workflow_result.get('error', 'Unknown error')}")
        return {"error": workflow_result.get('error', 'Workflow failed')}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Multi-Agent Coder")
    parser.add_argument("--task", required=True, help="Description of the coding task")


    parser.add_argument("--language", choices=["python", "javascript", "java", "csharp"], default="python", help="Programming language to use")
    parser.add_argument("--test-type", choices=["basic", "unit", "integration", "performance", "coverage", "security"], default="basic", help="Type of testing to perform")

    parser.add_argument("--branch", help="Git branch to create and push to")
    parser.add_argument("--push", action="store_true", help="Push changes to remote repository")

    args = parser.parse_args()

    # Run the main function
    results = asyncio.run(main(args.task, args.language))

    # Save results to a file
    output_file = Path("results.json")
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)




    print(f"\n💾 Results saved to {output_file}")

    # Version Control Integration
    vcs = VCSManager()
    print("\n📁 Version Control Integration:")

    # Initialize Git repo if not already initialized
    if not (vcs.repo_path / ".git").exists():
        init_result = vcs.initialize_repo()
        print(f"  - Git init: {init_result['message'] if init_result['success'] else init_result['error']}")

        # Set up Git config
        config_result = vcs.setup_git_config()
        print(f"  - Git config: {config_result['message'] if config_result['success'] else config_result['error']}")

    # Commit the generated code
    files_to_commit = [str(output_file)]
    # Add any generated code files (look for files with language extensions)
    if args.language == "python":
        files_to_commit.extend(["*.py"])
    elif args.language == "javascript":
        files_to_commit.extend(["*.js"])
    elif args.language == "java":
        files_to_commit.extend(["*.java"])
    elif args.language == "csharp":
        files_to_commit.extend(["*.cs"])

    commit_result = vcs.commit_code(files_to_commit, message=f"Generated code for task: {args.task}")
    print(f"  - Git commit: {commit_result['message'] if commit_result['success'] else commit_result['error']}")

    # Get Git status
    status_result = vcs.get_status()
    if status_result['success']:
        if status_result['status']:
            print(f"  - Git status: {len(status_result['status'].splitlines())} changed files")
        else:
            print(f"  - Git status: Working directory clean")
    else:


        print(f"  - Git status: {status_result['error']}")

    # Create branch if specified
    if args.branch:
        branch_result = vcs.create_branch(args.branch)
        print(f"  - Git branch: {branch_result['message'] if branch_result['success'] else branch_result['error']}")

    # Push to remote if specified
    if args.push:
        # First check if remote exists
        try:
            remote_result = subprocess.run(
                ['git', 'remote', 'get-url', 'origin'],
                cwd=vcs.repo_path,
                capture_output=True,
                text=True
            )
            if remote_result.returncode == 0:
                push_result = vcs.push_changes(args.branch if args.branch else None)
                print(f"  - Git push: {push_result['message'] if push_result['success'] else push_result['error']}")
            else:
                print("  - Git push: Skipped - no remote repository configured")
        except Exception as e:
            print(f"  - Git push: {str(e)}")





