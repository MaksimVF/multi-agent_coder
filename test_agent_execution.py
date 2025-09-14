



"""
Test script to check if agents are working properly
"""

import asyncio
from agent_registry import AgentRegistry
from analyst import Analyst
from developer import Developer

async def test_agent_execution():
    """Test if agents can execute tasks"""

    print("🧪 Testing Agent Execution...")

    # Create agents
    analyst = Analyst()
    developer = Developer()

    # Register agents
    AgentRegistry.register("analyst", Analyst)
    AgentRegistry.register("developer", Developer)

    # Test analyst
    print("\n  - Testing Analyst...")
    analyst_result = await analyst.analyze_task('Create a Python function named add that takes two numbers and returns their sum')

    print(f"  - Analyst result: {analyst_result}")

    # Test developer
    print("\n  - Testing Developer...")
    developer_result = await developer.develop_code({
        'description': 'Create a Python function named add that takes two numbers and returns their sum',
        'analysis': analyst_result
    }, 'python')

    print(f"  - Developer result: {developer_result}")

if __name__ == "__main__":
    asyncio.run(test_agent_execution())



