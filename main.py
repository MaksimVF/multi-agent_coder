
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
from vcs_manager import VCSManager

async def main(task_description, language="python"):
    # Create message queue
    message_queue = []

    # Create agents
    analyst = Analyst()
    developer = Developer()
    tester = Tester()

    # Analyst analyzes the task
    print("🔍 Analyst is analyzing the task...")
    subtasks = analyst.analyze_task(task_description)
    message_queue.append({
        "from": "analyst",
        "to": "developer",
        "content": subtasks
    })

    # Developer writes code for each subtask
    print(f"\n💻 Developer is working on the code ({language})...")
    all_code = []
    for subtask in subtasks:
        code = developer.develop_code(subtask, language)
        all_code.append(code)
        message_queue.append({
            "from": "developer",
            "to": "tester",
            "content": code
        })

    # Tester tests the code
    print("\n🧪 Tester is testing the code...")
    test_results = []
    failed_tests = []

    # First round of testing
    for code in all_code:
        result = tester.test_code(code, language)
        test_results.append(result)
        if not result["passed"]:
            print(f"❌ Test failed for code: {code['description']}")
            print(f"Error: {result['error']}")
            failed_tests.append((code, result["error"]))
            # Send back to developer for fixes
            message_queue.append({
                "from": "tester",
                "to": "developer",
                "content": {
                    "code": code,
                    "error": result["error"]
                }
            })
        else:
            print(f"✅ Test passed for code: {code['description']}")

    # Feedback loop for failed tests
    max_retries = 2
    retry_count = 0

    while failed_tests and retry_count < max_retries:
        print(f"\n🔄 Retry attempt {retry_count + 1}...")
        new_failed_tests = []

        for code, error in failed_tests:
            print(f"🛠️  Fixing: {code['description']}")
            # Developer fixes the code
            fixed_code = developer.fix_code(code, error, language)
            # Test the fixed code
            result = tester.test_code(fixed_code, language)
            if result["passed"]:
                print(f"✅ Fixed: {fixed_code['description']}")
                # Replace the old result with the new one
                for i, old_result in enumerate(test_results):
                    if old_result["description"] == code["description"]:
                        test_results[i] = result
                        break
            else:
                print(f"❌ Still failing: {fixed_code['description']}")
                print(f"Error: {result['error']}")
                new_failed_tests.append((fixed_code, result["error"]))

        failed_tests = new_failed_tests
        retry_count += 1

    # Final results
    print("\n📋 Final Results:")
    for i, result in enumerate(test_results, 1):
        status = "✅ Passed" if result["passed"] else "❌ Failed"
        print(f"{i}. {status}: {result['description']}")

    return test_results

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Multi-Agent Coder")
    parser.add_argument("--task", required=True, help="Description of the coding task")

    parser.add_argument("--language", choices=["python", "javascript", "java", "csharp"], default="python", help="Programming language to use")
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





