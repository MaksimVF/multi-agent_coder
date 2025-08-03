
#!/usr/bin/env python3
"""
Test script to verify the enhanced testing capabilities.
"""

import asyncio
import sys
import os
import pytest

# Add the current directory to Python path to import the tester
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tester import Tester

@pytest.mark.asyncio
async def test_enhanced_testing():
    """Test the enhanced testing capabilities."""

    tester = Tester()

    # Test code sample
    test_code = {
        "code": """
def add(a, b):
    \"\"\"Add two numbers.\"\"\"
    return a + b

def subtract(a, b):
    \"\"\"Subtract two numbers.\"\"\"
    return a - b

def multiply(a, b):
    \"\"\"Multiply two numbers.\"\"\"
    return a * b

def divide(a, b):
    \"\"\"Divide two numbers.\"\"\"
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return a / b

def main():
    \"\"\"Main function to demonstrate the operations.\"\"\"
    print("Calculator Operations:")
    print(f"2 + 3 = {add(2, 3)}")
    print(f"5 - 3 = {subtract(5, 3)}")
    print(f"2 * 3 = {multiply(2, 3)}")
    print(f"6 / 3 = {divide(6, 3)}")

if __name__ == "__main__":
    main()
""",
        "description": "Simple calculator with basic operations"
    }

    # Test different test types
    test_types = ["basic", "unit", "integration", "performance", "coverage", "security"]

    print("Testing enhanced testing capabilities...")
    print("=" * 50)

    for test_type in test_types:
        print(f"\n🧪 Running {test_type} test...")
        result = await tester.test_code(test_code, "Calculator operations", "python", test_type)

        status = "✅ PASSED" if result["passed"] else "❌ FAILED"
        print(f"   Result: {status}")

        # Print additional information based on test type
        if test_type == "performance" and "performance" in result:
            print(f"   📊 Execution Time: {result['performance']['execution_time_ms']:.2f} ms")
            if "memory_usage_kb" in result['performance']:
                print(f"   📊 Memory Usage: {result['performance']['memory_usage_kb']:.2f} KB")

        if test_type == "coverage" and "coverage" in result:
            print(f"   📊 Code Coverage: {result['coverage']['percentage']:.1f}%")

        if test_type == "security" and "security_issues" in result:
            print(f"   🔒 Security Issues: {len(result['security_issues'])}")

        if not result["passed"]:
            print(f"   🔍 Error: {result['error']}")

    print("\n" + "=" * 50)
    print("Enhanced testing verification completed!")

if __name__ == "__main__":
    asyncio.run(test_enhanced_testing())
