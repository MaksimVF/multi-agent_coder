


#!/usr/bin/env python3
import asyncio
import sys
import os
import pytest

# Set a mock API key for testing
os.environ["OPENAI_API_KEY"] = "mock_key"

from analyst import Analyst
from developer import Developer
from tester import Tester
from optimizer import Optimizer
from researcher import Researcher
from agent_workflow import AgentWorkflow

@pytest.mark.asyncio
async def test_llm_agents():
    """Test the LLM-powered agents."""
    print("🧪 Testing LLM-powered agents...")

    # Create agents
    analyst = Analyst(temperature=0.5)
    developer = Developer(temperature=0.7)
    tester = Tester(temperature=0.3)
    researcher = Researcher(temperature=0.7)
    optimizer = Optimizer(temperature=0.5)
    optimizer.researcher = researcher

    # Test Analyst
    print("\n1. Testing Analyst...")
    task_description = "Create a Python function to calculate the factorial of a number"
    subtasks = await analyst.analyze_task(task_description)
    print(f"   Generated {len(subtasks)} subtasks:")
    for i, subtask in enumerate(subtasks[:3], 1):
        print(f"   {i}. {subtask.get('description', 'Unknown')}")

    # Test Developer
    print("\n2. Testing Developer...")
    if subtasks:
        code = await developer.develop_code(subtasks[0], "python")
        print(f"   Generated code for: {code.get('description', 'Unknown')}")
        print(f"   Code snippet: {code.get('code', 'No code')[:100]}...")

    # Test Tester
    print("\n3. Testing Tester...")
    if 'code' in locals():
        test_result = await tester.test_code(code, subtasks[0], "python", "basic")
        print(f"   Test result: {'✅ Passed' if test_result.get('passed', False) else '❌ Failed'}")

    # Test Researcher
    print("\n4. Testing Researcher...")
    research_results = await researcher.research_topic("Python factorial function")
    print(f"   Research completed: {research_results.get('status', 'Unknown')}")

    # Test Optimizer
    print("\n5. Testing Optimizer...")
    if 'code' in locals() and 'test_result' in locals():
        optimization_result = await optimizer.analyze_and_optimize(
            task_description,
            code,
            [test_result],
            "python"
        )
        print(f"   Generated {len(optimization_result.get('suggestions', []))} suggestions:")
        for i, suggestion in enumerate(optimization_result.get('suggestions', [])[:2], 1):
            print(f"   {i}. {suggestion.get('type', 'Unknown')}: {suggestion.get('details', 'No details')}")

    # Test Workflow
    print("\n6. Testing Agent Workflow...")
    workflow = AgentWorkflow()
    workflow.register_agent("analyst", analyst)
    workflow.register_agent("developer", developer)
    workflow.register_agent("tester", tester)
    workflow.register_agent("optimizer", optimizer)

    workflow.add_edge("analyst", "developer")
    workflow.add_edge("developer", "tester")
    workflow.add_edge("tester", "optimizer")

    initial_data = {
        "task_description": "Create a Python function to add two numbers",
        "language": "python",
        "test_type": "basic"
    }

    workflow_result = await workflow.execute_workflow("analyst", initial_data)

    if workflow_result["status"] == "completed":
        print("   ✅ Workflow completed successfully!")
        print(f"   Generated {len(workflow_result['data'].get('test_results', []))} test results")
    else:
        print(f"   ❌ Workflow failed: {workflow_result.get('error', 'Unknown error')}")

    print("\n🎉 LLM-powered agent testing completed!")

if __name__ == "__main__":
    asyncio.run(test_llm_agents())


