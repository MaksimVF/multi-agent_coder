
#!/usr/bin/env python3
"""
Basic test to check if the system can run.
"""

import asyncio
from analyst import Analyst

async def test_basic():
    """Test basic functionality."""
    print("Testing basic functionality...")

    # Create an analyst
    analyst = Analyst(temperature=0.3)

    # Test task analysis
    task = "Create a Python function to calculate Fibonacci numbers"
    result = await analyst.analyze_task(task)

    print(f"Analysis result: {result}")

    return True

if __name__ == "__main__":
    asyncio.run(test_basic())
