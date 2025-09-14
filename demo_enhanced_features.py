


"""
Demo script showing the enhanced features of the multi-agent system.

This script demonstrates:
1. Agent Registry functionality
2. Event-driven communication
3. Advanced code generation
4. Dynamic agent discovery
"""

import os
import json
import asyncio
from typing import Dict, Any, List

# Import new components
from agent_registry import AgentRegistry
from event_system import EventBus, EventType, AgentEvent
from advanced_code_generator import AdvancedCodeGenerator
from memory_manager import MemoryManager

# Import agent classes
from analyst import Analyst
from developer import Developer
from tester import Tester
from optimizer import Optimizer

async def demo_agent_registry():
    """Demonstrate agent registry functionality."""
    print("\n📋 Demo: Agent Registry")

    # Clear existing registry
    AgentRegistry._registry = {}

    # Register some agents
    AgentRegistry.register("analyst", Analyst, version="2.0", description="Task analysis agent")
    AgentRegistry.register("developer", Developer, version="2.0", description="Code development agent")
    AgentRegistry.register("tester", Tester, version="2.0", description="Code testing agent")
    AgentRegistry.register("optimizer", Optimizer, version="2.0", description="Code optimization agent")

    # List all registered agents
    print("Registered Agents:")
    for name, info in AgentRegistry.list_agents().items():
        print(f"  - {name}: {info.get('description')} v{info.get('version')}")

    # Get specific agent info
    analyst_info = AgentRegistry.get_agent_info("analyst")
    print(f"\nAnalyst Agent Info: {analyst_info}")

    # Check dependencies
    print(f"Analyst dependencies satisfied: {AgentRegistry.check_dependencies('analyst')}")

async def demo_event_system():
    """Demonstrate event-driven communication."""
    print("\n📡 Demo: Event System")

    # Create event bus
    event_bus = EventBus()

    # Define event handlers
    async def handle_task_event(event: AgentEvent):
        print(f"📋 Task Event: {event.event_type.name} - {event.data}")

    async def handle_error_event(event: AgentEvent):
        print(f"⚠️ Error Event: {event.data.get('error')}")

    # Subscribe to events
    sub1 = event_bus.subscribe(EventType.TASK_CREATED, handle_task_event)
    sub2 = event_bus.subscribe(EventType.TASK_UPDATED, handle_task_event)
    sub3 = event_bus.subscribe(EventType.ERROR_OCCURRED, handle_error_event)

    # Publish some events
    await event_bus.publish(
        AgentEvent(
            event_type=EventType.TASK_CREATED,
            source="demo",
            data={"task_id": "demo_001", "description": "Demo task"}
        )
    )

    await event_bus.publish(
        AgentEvent(
            event_type=EventType.TASK_UPDATED,
            source="demo",
            data={"task_id": "demo_001", "status": "running"}
        )
    )

    # Publish an error event
    await event_bus.publish(
        AgentEvent(
            event_type=EventType.ERROR_OCCURRED,
            source="demo",
            data={"error": "Demo error occurred", "task_id": "demo_001"}
        )
    )

    # Get event history
    print("\nEvent History:")
    for event in event_bus.get_event_history(limit=5):
        print(f"  - {event.event_type.name}: {event.data}")

async def demo_advanced_code_generation():
    """Demonstrate advanced code generation."""
    print("\n💻 Demo: Advanced Code Generation")

    # Initialize memory manager
    memory_manager = MemoryManager(
        redis_host=os.getenv("REDIS_HOST", "localhost"),
        redis_port=int(os.getenv("REDIS_PORT", 6379)),
        weaviate_url=os.getenv("WEAVIATE_URL", "http://localhost:8080"),
    )

    # Create advanced code generator
    code_generator = AdvancedCodeGenerator(memory_manager=memory_manager)

    # Define requirements
    requirements = {
        "description": "Create a Python function to calculate Fibonacci numbers with memoization",
        "requirements": [
            "Use recursive approach",
            "Implement memoization",
            "Add type hints",
            "Include docstring",
        ]
    }

    # Generate code
    print("Generating code...")
    code_result = await code_generator.generate_code(
        requirements=requirements,
        language="python",
        context={"task_id": "demo_001"}
    )

    print("\nGenerated Code:")
    print(code_result.get("code", "No code generated"))

    # Generate unit tests
    print("\nGenerating unit tests...")
    test_result = await code_generator.generate_unit_tests(
        code=code_result.get("code", ""),
        requirements=requirements,
        language="python"
    )

    print("\nGenerated Tests:")
    print(test_result.get("tests", "No tests generated"))

    # Optimize code
    print("\nOptimizing code...")
    optimize_result = await code_generator.optimize_code(
        code=code_result.get("code", ""),
        requirements=requirements,
        language="python"
    )

    print("\nOptimized Code:")
    print(optimize_result.get("optimized", "No optimized code"))

    # Close memory manager
    memory_manager.close()

async def demo_dynamic_agent_discovery():
    """Demonstrate dynamic agent discovery."""
    print("\n🔍 Demo: Dynamic Agent Discovery")

    # Initialize memory manager
    memory_manager = MemoryManager(
        redis_host=os.getenv("REDIS_HOST", "localhost"),
        redis_port=int(os.getenv("REDIS_PORT", 6379)),
        weaviate_url=os.getenv("WEAVIATE_URL", "http://localhost:8080"),
    )

    # Register agents
    AgentRegistry.register("analyst", Analyst, version="2.0", description="Task analysis agent")
    AgentRegistry.register("developer", Developer, version="2.0", description="Code development agent")

    # Function to get agent instance (similar to workflow._get_agent_instance)
    def get_agent_instance(agent_name: str):
        agent_class = AgentRegistry.get_agent(agent_name)
        if agent_class:
            try:
                return agent_class(memory_manager=memory_manager)
            except Exception:
                try:
                    return agent_class()
                except Exception:
                    return None
        return None

    # Discover and use agents
    analyst = get_agent_instance("analyst")
    developer = get_agent_instance("developer")
    unknown = get_agent_instance("unknown_agent")

    print(f"Discovered analyst: {analyst is not None}")
    print(f"Discovered developer: {developer is not None}")
    print(f"Discovered unknown agent: {unknown is not None}")

    if analyst:
        # Use the discovered analyst
        requirements = {
            "description": "Create a Python function to calculate Fibonacci numbers",
            "requirements": ["Use recursive approach", "Add type hints"]
        }
        subtasks = await analyst.analyze_task(requirements["description"])
        print(f"\nAnalyst generated {len(subtasks)} subtasks")

    # Close memory manager
    memory_manager.close()

async def main():
    """Run all demos."""
    print("🚀 Running Enhanced Features Demo...")

    # Run demos
    await demo_agent_registry()
    await demo_event_system()
    await demo_advanced_code_generation()
    await demo_dynamic_agent_discovery()

    print("\n✅ All demos completed successfully!")

if __name__ == "__main__":
    asyncio.run(main())


