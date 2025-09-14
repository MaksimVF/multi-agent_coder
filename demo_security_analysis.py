


#!/usr/bin/env python3
"""
Demo script showing security analysis capabilities in multi-agent coder.
"""

import asyncio
from tester import Tester

from security import SecurityRisk, BasicSecurityAnalyzer
from security.llm_analyzer import LLMSecurityAnalyzer, HybridSecurityAnalyzer


async def demo_security_analysis():
    """Demonstrate security analysis capabilities."""
    print("=== Multi-Agent Coder: Security Analysis Demo ===\n")

    # Create a tester with security capabilities
    tester = Tester()

    # Sample code with security issues
    python_code_with_issues = '''
import os
import pickle

def dangerous_function():
    # Dangerous eval usage
    user_input = "print('Hello')"
    eval(user_input)

    # Hardcoded credentials
    password = "secret123"

    # Pickle usage
    data = pickle.loads(b"some_data")

    return "This code has security issues"
'''

    python_code_safe = '''
def safe_function():
    # Safe code
    result = "Hello, world!"
    return result
'''

    # Test security analysis
    print("1. Testing Python code with security issues...")
    result_issues = await tester.test_code(
        {"code": python_code_with_issues, "description": "Test dangerous code"},
        {"task": "security_test"},
        language="python",
        test_type="security"
    )
    print(f"Security test result: {'PASS' if result_issues['passed'] else 'FAIL'}")
    if 'security_issues' in result_issues:
        print("Security issues found:")
        for issue in result_issues['security_issues']:
            print(f"  - {issue}")
    if 'security_risk' in result_issues:
        risk_level = result_issues['security_risk']
        if risk_level == SecurityRisk.HIGH.value:
            print(f"Security risk: HIGH (value: {risk_level})")
        elif risk_level == SecurityRisk.MEDIUM.value:
            print(f"Security risk: MEDIUM (value: {risk_level})")
        elif risk_level == SecurityRisk.LOW.value:
            print(f"Security risk: LOW (value: {risk_level})")
        else:
            print(f"Security risk: UNKNOWN (value: {risk_level})")
    print()

    print("2. Testing safe Python code...")
    result_safe = await tester.test_code(
        {"code": python_code_safe, "description": "Test safe code"},
        {"task": "security_test"},
        language="python",
        test_type="security"
    )
    print(f"Security test result: {'PASS' if result_safe['passed'] else 'FAIL'}")
    if 'security_issues' in result_safe:
        print("Security issues found:")
        for issue in result_safe['security_issues']:
            print(f"  - {issue}")
    if 'security_risk' in result_safe:
        risk_level = result_safe['security_risk']
        if risk_level == SecurityRisk.HIGH.value:
            print(f"Security risk: HIGH (value: {risk_level})")
        elif risk_level == SecurityRisk.MEDIUM.value:
            print(f"Security risk: MEDIUM (value: {risk_level})")
        elif risk_level == SecurityRisk.LOW.value:
            print(f"Security risk: LOW (value: {risk_level})")
        else:
            print(f"Security risk: UNKNOWN (value: {risk_level})")
    print()

    # Test JavaScript code
    js_code_with_issues = '''
function dangerousFunction() {
    // Dangerous eval usage
    let userInput = "console.log('Hello')";
    eval(userInput);

    // Hardcoded credentials
    let apiKey = "secret123";

    // XSS risk
    document.getElementById("content").innerHTML = "<script>alert('XSS')</script>";

    return "This code has security issues";
}
'''

    print("3. Testing JavaScript code with security issues...")
    result_js = await tester.test_code(
        {"code": js_code_with_issues, "description": "Test dangerous JS code"},
        {"task": "security_test"},
        language="javascript",
        test_type="security"
    )
    print(f"Security test result: {'PASS' if result_js['passed'] else 'FAIL'}")
    if 'security_issues' in result_js:
        print("Security issues found:")
        for issue in result_js['security_issues']:
            print(f"  - {issue}")
    if 'security_risk' in result_js:
        risk_level = result_js['security_risk']
        if risk_level == SecurityRisk.HIGH.value:
            print(f"Security risk: HIGH (value: {risk_level})")
        elif risk_level == SecurityRisk.MEDIUM.value:
            print(f"Security risk: MEDIUM (value: {risk_level})")
        elif risk_level == SecurityRisk.LOW.value:
            print(f"Security risk: LOW (value: {risk_level})")
        else:
            print(f"Security risk: UNKNOWN (value: {risk_level})")
    print()

    # Test different security analyzers
    print("4. Testing different security analyzers...")

    # Create a mock action
    class MockAction:
        def __init__(self, code, language):
            self.code = code
            self.language = language

    action = MockAction(python_code_with_issues, "python")

    # Basic analyzer
    basic_analyzer = BasicSecurityAnalyzer()
    basic_risk = await basic_analyzer.analyze_action(action)
    print(f"Basic analyzer risk: {basic_risk.name}")

    # LLM analyzer (if available)
    try:
        llm_analyzer = LLMSecurityAnalyzer(model="gpt-4o", temperature=0.3)
        llm_risk = await llm_analyzer.analyze_action(action)
        print(f"LLM analyzer risk: {llm_risk.name}")
    except Exception as e:
        print(f"LLM analyzer not available: {e}")

    # Hybrid analyzer
    hybrid_analyzer = HybridSecurityAnalyzer(model="gpt-4o", temperature=0.3)
    hybrid_risk = await hybrid_analyzer.analyze_action(action)
    print(f"Hybrid analyzer risk: {hybrid_risk.name}")
    print()

    print("=== Demo Complete ===")

if __name__ == "__main__":
    asyncio.run(demo_security_analysis())

