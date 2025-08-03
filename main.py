





import os
import json
import asyncio
from typing import Dict, Any, List

# Import agent classes
try:
    from analyst import Analyst
    from developer import Developer
    from tester import Tester
    from optimizer import Optimizer
    from researcher import Researcher
    from agent_workflow import AgentWorkflow
    from memory_manager import MemoryManager
except ImportError as e:
    print(f"Error importing agent modules: {e}")
    raise

async def main():
    """Main function to run the multi-agent coder system with memory integration."""
    print("🚀 Starting Multi-Agent Coder System with Memory Integration...")

    # Initialize memory manager
    memory_manager = MemoryManager(
        redis_host=os.getenv("REDIS_HOST", "localhost"),
        redis_port=int(os.getenv("REDIS_PORT", 6379)),
        weaviate_url=os.getenv("WEAVIATE_URL", "http://localhost:8080"),
    )

    # Initialize agents with memory manager
    analyst = Analyst(memory_manager=memory_manager)
    developer = Developer(memory_manager=memory_manager)
    tester = Tester(memory_manager=memory_manager)
    optimizer = Optimizer(memory_manager=memory_manager)
    researcher = Researcher(memory_manager=memory_manager)

    # Initialize workflow with memory manager
    workflow = AgentWorkflow(memory_manager=memory_manager)

    # Add agents to workflow
    workflow.add_agent("analyst", analyst)
    workflow.add_agent("developer", developer)
    workflow.add_agent("tester", tester)
    workflow.add_agent("optimizer", optimizer)
    workflow.add_agent("researcher", researcher)

    # Define a sample task
    sample_task = {
        "id": "task_001",
        "description": "Create a Python function to calculate Fibonacci numbers with memoization",
        "requirements": [
            "Use recursive approach",
            "Implement memoization",
            "Add type hints",
            "Include docstring",
        ],
    }

    # Set initial state
    workflow.set_initial_state(sample_task, task_id=sample_task["id"])

    # Execute workflow
    print("📋 Executing workflow with memory integration...")
    result = await workflow.execute_workflow()

    # Print results
    print("\n📊 Workflow Results:")
    print(json.dumps(result, indent=2))

    # Get status
    status = workflow.get_status()
    print("\n📋 Final Status:")
    print(json.dumps(status, indent=2))

    # Get task history from memory
    print("\n💾 Task History from Memory:")
    task_history = workflow.get_task_history(sample_task["id"])
    print(json.dumps(task_history, indent=2))

    # Test memory recovery
    print("\n🔄 Testing Task Recovery from Memory:")
    recovery_result = workflow.recover_task(sample_task["id"])
    print(f"Recovery successful: {recovery_result}")

    # Test knowledge base population
    print("\n📚 Populating Knowledge Base with Research:")
    research_topics = [
        "Python best practices",
        "Fibonacci sequence algorithms",
        "Memoization techniques",
        "Code optimization patterns",
    ]
    kb_result = await researcher.populate_knowledge_base(research_topics)
    print(f"Knowledge base populated with {len(research_topics)} topics")

    # Close memory manager
    memory_manager.close()

if __name__ == "__main__":
    asyncio.run(main())



