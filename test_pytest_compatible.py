
#!/usr/bin/env python3
"""
Test script that is compatible with pytest.
"""

import pytest
import asyncio
import sys
import os

# Add the current directory to Python path to import the modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tester import Tester

class TestPytestCompatible:
    """Test class that is compatible with pytest."""

    @pytest.mark.asyncio
    async def test_tester_basic_functionality(self):
        """Test basic functionality of the Tester class."""
        tester = Tester(temperature=0.3)

        # Test code sample
        test_code = {
            "code": """
def add(a, b):
    \"\"\"Add two numbers.\"\"\"
    return a + b

def subtract(a, b):
    \"\"\"Subtract two numbers.\"\"\"
    return a - b
""",
            "description": "Simple calculator with basic operations"
        }

        # Test basic testing
        result = await tester.test_code(test_code, "Calculator operations", "python", "basic")
        assert result["passed"] is True, f"Basic test failed: {result.get('error', 'Unknown error')}"

        # Test unit testing
        result = await tester.test_code(test_code, "Calculator operations", "python", "unit")
        assert result["passed"] is True, f"Unit test failed: {result.get('error', 'Unknown error')}"

        # Test security testing
        result = await tester.test_code(test_code, "Calculator operations", "python", "security")
        assert result["passed"] is True, f"Security test failed: {result.get('error', 'Unknown error')}"

    @pytest.mark.asyncio
    async def test_tester_security_issues(self):
        """Test that security issues are detected."""
        tester = Tester(temperature=0.3)

        # Test code with security issues
        insecure_code = {
            "code": """
import os
import pickle

def insecure_function():
    # Insecure code with eval and pickle
    user_input = "malicious_code"
    eval(user_input)

    # Hardcoded credentials
    password = "secret123"

    # Insecure pickle usage
    data = pickle.loads(b"insecure_data")
    return data
""",
            "description": "Insecure code with multiple vulnerabilities"
        }

        # Test security testing
        result = await tester.test_code(insecure_code, "Insecure code", "python", "security")
        assert result["passed"] is False, "Security test should fail for insecure code"
        assert "security_issues" in result, "Security issues should be reported"
        assert len(result["security_issues"]) > 0, "Should detect security issues"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
