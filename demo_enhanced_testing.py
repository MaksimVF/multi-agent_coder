

#!/usr/bin/env python3
"""
Demonstration of enhanced testing capabilities in the multi-agent coder.
"""

import asyncio
import sys
import os

# Add the current directory to Python path to import the tester
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tester import Tester

async def demo_enhanced_testing():
    """Demonstrate the enhanced testing capabilities."""

    tester = Tester()

    # Sample code to test - a simple calculator with some potential issues
    calculator_code = {
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

def power(a, b):
    \"\"\"Raise a to the power of b.\"\"\"
    return a ** b

def main():
    \"\"\"Main function to demonstrate the operations.\"\"\"
    print("Calculator Operations:")
    print(f"2 + 3 = {add(2, 3)}")
    print(f"5 - 3 = {subtract(5, 3)}")
    print(f"2 * 3 = {multiply(2, 3)}")
    print(f"6 / 3 = {divide(6, 3)}")
    print(f"2 ^ 3 = {power(2, 3)}")

if __name__ == "__main__":
    main()
""",
        "description": "Enhanced calculator with power operation"
    }

    # Code with potential security issue for testing
    insecure_code = {
        "code": """
def process_user_input(user_data):
    \"\"\"Process user input with potential security issues.\"\"\"
    # Potential security issue: eval usage
    result = eval(user_data)
    return result

def connect_to_database():
    \"\"\"Connect to database with hardcoded credentials.\"\"\"
    # Potential security issue: hardcoded credentials
    password = "secret123"
    connection_string = f"db+mysql://user:{password}@localhost/db"
    print(f"Connecting to database: {connection_string}")
    return connection_string

def main():
    \"\"\"Main function.\"\"\"
    print("Processing data...")
    result = process_user_input("2 + 3")
    print(f"Result: {result}")
    connect_to_database()

if __name__ == "__main__":
    main()
""",
        "description": "Code with potential security issues"
    }

    print("🎯 Multi-Agent Coder - Enhanced Testing Capabilities Demo")
    print("=" * 60)

    # Test the calculator code with different test types
    print("\n🧮 Testing Calculator Code:")
    print("-" * 40)

    test_types = ["basic", "unit", "integration", "performance", "coverage", "security"]

    for test_type in test_types:
        print(f"\n🧪 Running {test_type.upper()} test...")
        result = await tester.test_code(calculator_code, "Calculator operations", "python", test_type)

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
            print(f"   🔒 Security Issues: {len(result['security_issues'])} found")

        if not result["passed"]:
            print(f"   🔍 Error: {result['error']}")

    # Test the insecure code with security testing
    print("\n🔒 Testing Security Vulnerabilities:")
    print("-" * 40)

    security_result = await tester.test_code(insecure_code, "Security test", "python", "security")
    print(f"🧪 Running SECURITY test...")
    status = "✅ PASSED" if security_result["passed"] else "❌ FAILED"
    print(f"   Result: {status}")

    if "security_issues" in security_result:
        print(f"   🔒 Security Issues Found: {len(security_result['security_issues'])}")
        for issue in security_result['security_issues']:
            print(f"      - {issue}")

    print("\n" + "=" * 60)
    print("🎉 Enhanced Testing Demo Completed!")
    print("\nKey improvements in testing capabilities:")
    print("✅ Multiple test types: basic, unit, integration, performance, coverage, security")
    print("✅ Comprehensive unit testing with mocking and edge case testing")
    print("✅ Integration testing to verify component interactions")
    print("✅ Performance metrics including execution time and memory usage")
    print("✅ Code coverage measurement")
    print("✅ Security vulnerability detection")
    print("✅ Detailed error reporting with tracebacks")

if __name__ == "__main__":
    asyncio.run(demo_enhanced_testing())

