


#!/usr/bin/env python3
import asyncio
import json
from pathlib import Path

from optimizer import Optimizer
from researcher import Researcher

async def demo_optimizer():
    print("🎯 Multi-Agent Coder - Optimizer Demo")
    print("============================================================")

    # Create agents
    researcher = Researcher()
    optimizer = Optimizer()
    optimizer.researcher = researcher

    # Sample task and code
    task_description = "Write a calculator with add, subtract, multiply, and divide functions"
    language = "python"

    # Sample code
    code = """
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
"""

    # Sample test results
    test_results = [
        {
            "description": "Basic functionality test",
            "passed": True,
            "test_type": "basic",
            "performance": {
                "execution_time_ms": 25.45,
                "memory_usage_kb": 1024.0
            }
        },
        {
            "description": "Edge case testing",
            "passed": True,
            "test_type": "unit",
            "performance": {
                "execution_time_ms": 30.12,
                "memory_usage_kb": 1536.0
            }
        },
        {
            "description": "Security check",
            "passed": True,
            "test_type": "security",
            "security_issues": []
        }
    ]

    # Run optimization
    print("\n🔧 Running Optimizer...")
    optimization_result = await optimizer.analyze_and_optimize(
        task_description,
        {"code": code, "description": task_description, "language": language},
        test_results,
        language
    )

    if optimization_result["success"]:
        print("\n💡 Optimization Results:")
        print(f"   📊 Analysis: {len(optimization_result['suggestions'])} suggestions generated")

        # Print all suggestions
        for i, suggestion in enumerate(optimization_result['suggestions'], 1):
            print(f"\n   {i}. {suggestion['type']}: {suggestion['details']}")
            if "code" in suggestion:
                print(f"      Code example:\n      {suggestion['code']}")

        # Show statistics
        print("\n📊 Optimization Statistics:")
        stats = optimizer.get_statistics()
        print(f"   Total suggestions: {stats['total_suggestions']}")
        print(f"   By type: {stats['by_type']}")
        print(f"   By priority: {stats['by_priority']}")

        # Show history
        print("\n📚 Improvement History:")
        history = optimizer.get_improvement_history()
        print(f"   Total entries: {len(history)}")
        if history:
            print(f"   Last entry: {history[-1]['type']} - {history[-1]['details']}")

    else:
        print(f"   ⚠️  Optimization failed: {optimization_result['error']}")

    # Test researcher
    print("\n🔍 Testing Researcher...")
    print("\n   1. Searching for documentation...")
    docs = await researcher.fetch_documentation("python argparse")
    print(f"      Found: {docs['title']}")

    print("\n   2. Researching optimizations...")
    opts = await researcher.research_optimizations("python", "performance")
    print(f"      Found {len(opts)} optimization tips")

    print("\n   3. Getting code examples...")
    examples = await researcher.get_code_examples("python", "argparse")
    if examples:
        print(f"      Example: {examples[0]['title']}")
        print(f"      Code:\n      {examples[0]['code']}")

    print("\n============================================================")
    print("🎉 Optimizer Demo Completed!")

if __name__ == "__main__":
    asyncio.run(demo_optimizer())


