
#!/usr/bin/env python3
import argparse
import asyncio
import json
import sys
from pathlib import Path

from analyst import Analyst
from developer import Developer
from tester import Tester

async def main(task_description):
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
    print("\n💻 Developer is working on the code...")
    all_code = []
    for subtask in subtasks:
        code = developer.develop_code(subtask)
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
        result = tester.test_code(code)
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
            fixed_code = developer.fix_code(code, error)
            # Test the fixed code
            result = tester.test_code(fixed_code)
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
    args = parser.parse_args()

    # Run the main function
    results = asyncio.run(main(args.task))

    # Save results to a file
    output_file = Path("results.json")
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\n💾 Results saved to {output_file}")
