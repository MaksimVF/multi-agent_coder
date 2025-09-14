





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
    from agent_registry import AgentRegistry
    from event_system import EventBus, EventType
    from advanced_code_generator import AdvancedCodeGenerator
    from problem_solver import ProblemSolver, ProblemContext
    from role_coordinator import RoleCoordinator
except ImportError as e:
    print(f"Error importing agent modules: {e}")
    raise

async def main():
    """Main function to run the enhanced multi-agent coder system."""
    print("🚀 Starting Enhanced Multi-Agent Coder System...")

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

    # Register agents with the registry
    AgentRegistry.register("analyst", Analyst, version="2.0", description="Task analysis agent")
    AgentRegistry.register("developer", Developer, version="2.0", description="Code development agent")
    AgentRegistry.register("tester", Tester, version="2.0", description="Code testing agent")
    AgentRegistry.register("optimizer", Optimizer, version="2.0", description="Code optimization agent")
    AgentRegistry.register("researcher", Researcher, version="2.0", description="Research agent")

    print("📋 Registered Agents:")
    for name, info in AgentRegistry.list_agents().items():
        print(f"  - {name}: {info.get('description', 'No description')} v{info.get('version', '1.0')}")

    # Initialize workflow with memory manager
    workflow = AgentWorkflow(memory_manager=memory_manager)

    # Add agents to workflow
    workflow.add_agent("analyst", analyst)
    workflow.add_agent("developer", developer)
    workflow.add_agent("tester", tester)
    workflow.add_agent("optimizer", optimizer)
    workflow.add_agent("researcher", researcher)

    # Demonstrate enhanced event system capabilities
    print("\n📡 Enhanced Event System Features:")
    print("  - Event prioritization and validation")
    print("  - Middleware processing pipeline")
    print("  - Advanced filtering and querying")
    print("  - Improved error handling and recovery")

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

    # Demonstrate enhanced event system features
    print("\n📊 Event System Statistics:")
    event_history = workflow.event_bus.get_event_history(limit=20)
    print(f"  Total events processed: {len(event_history)}")

    # Show event types
    event_types = set(event.event_type for event in event_history)
    print(f"  Event types: {', '.join(str(et.name) for et in event_types)}")

    # Show priority distribution
    from collections import Counter
    priorities = Counter(event.priority for event in event_history)
    print(f"  Priority distribution: {dict(priorities)}")

    # Demonstrate Problem Solver functionality
    print("\n🔧 Demonstrating Problem Solver Capabilities:")

    # Create a problem solver
    problem_solver = ProblemSolver({
        'max_iterations': 10,
        'output_dir': 'problem_solver_demo'
    })

    # Define a sample problem
    sample_problem = ProblemContext(
        problem_id="demo_problem_1",
        problem_type="bug",
        title="Fix Fibonacci function bug",
        description="The Fibonacci function fails with large inputs due to recursion depth issues",
        repository_path=os.getcwd()
    )

    # Solve the problem
    print("  - Solving sample problem...")
    solver_result = await problem_solver.solve_problem(sample_problem)

    # Show results
    print(f"  - Problem solved: {solver_result.get('success', False)}")
    print(f"  - Iterations: {solver_result.get('iterations', 0)}")
    print(f"  - Agents used: {', '.join(solver_result.get('agents_used', []))}")

    # Demonstrate new Role Coordinator with enhanced roles
    print("\n🎯 Demonstrating New Role Coordinator with Enhanced Roles:")
    print("  - Using Product Manager, Architect, Engineer, and QA Engineer roles")
    print("  - Creating project skeleton and implementing core components")

    # Create and run role coordinator with original roles
    role_coordinator = RoleCoordinator(use_unified_roles=False)

    # Example project requirements
    project_requirements = {
        "requirements": "Create a web application with frontend, backend, and database. "
                       "Include user authentication and REST API endpoints."
    }

    # Run the enhanced workflow with original roles
    print("  - Running enhanced development workflow with original roles...")
    coordinator_result = await role_coordinator.run_workflow(project_requirements)

    # Show results
    print("  - Workflow completed successfully!")
    print(f"  - Generated architecture: {coordinator_result.get('system_architecture', {}).get('components', [])}")
    print(f"  - Created files: {len(coordinator_result.get('project_structure', {}))} directories")
    print(f"  - Implemented components: {len(coordinator_result.get('code_implementation', {}))}")
    print(f"  - Test status: {coordinator_result.get('qa_status', 'unknown')}")

    # Demonstrate unified roles
    print("\n🎯 Demonstrating Unified Roles (Reduced Redundancy):")
    print("  - Using AnalystArchitect, DeveloperEngineer, and TesterQa roles")

    # Create and run role coordinator with unified roles
    unified_coordinator = RoleCoordinator(use_unified_roles=True)

    # Run the workflow with unified roles
    print("  - Running workflow with unified roles...")
    unified_result = await unified_coordinator.run_workflow(project_requirements)

    # Show results
    print("  - Unified workflow completed successfully!")
    print(f"  - Generated architecture: {unified_result.get('system_architecture', {}).get('components', [])}")
    print(f"  - Created files: {len(unified_result.get('project_structure', {}))} directories")
    print(f"  - Implemented components: {len(unified_result.get('code_implementation', {}))}")
    print(f"  - Test status: {unified_result.get('qa_status', 'unknown')}")

    # Demonstrate task decomposition
    print("\n🎯 Demonstrating Task Decomposition (MetaGPT-inspired):")
    print("  - Using TaskDecomposer to break down goals into specific tasks")

    # Create and run role coordinator with task decomposer
    decomposer_coordinator = RoleCoordinator(use_unified_roles=True, use_task_decomposer=True)

    # Run the workflow with task decomposition
    print("  - Running workflow with task decomposition...")
    decomposer_result = await decomposer_coordinator.run_workflow(project_requirements)

    # Show results
    print("  - Task decomposition workflow completed successfully!")
    print(f"  - Generated architecture: {decomposer_result.get('system_architecture', {}).get('components', [])}")
    print(f"  - Task list: {len(decomposer_result.get('task_list', []))} tasks")
    print(f"  - Task documentation:\n{decomposer_result.get('task_documentation', 'No documentation')}")
    print(f"  - Implemented components: {len(decomposer_result.get('code_implementation', {}))}")
    print(f"  - Test status: {decomposer_result.get('qa_status', 'unknown')}")

    # Demonstrate code review
    print("\n🔍 Demonstrating Code Review (MetaGPT-inspired):")
    print("  - Using Reviewer agent to perform systematic code review")

    # Create and run role coordinator with reviewer
    reviewer_coordinator = RoleCoordinator(
        use_unified_roles=True,
        use_task_decomposer=True,
        use_reviewer=True
    )

    # Run the workflow with code review
    print("  - Running workflow with code review...")
    reviewer_result = await reviewer_coordinator.run_workflow(project_requirements)

    # Show results
    print("  - Code review workflow completed successfully!")
    print(f"  - Generated architecture: {reviewer_result.get('system_architecture', {}).get('components', [])}")
    print(f"  - Task list: {len(reviewer_result.get('task_list', []))} tasks")
    print(f"  - Code review score: {reviewer_result.get('code_review', {}).get('quality_score', 0):.1f}/10")
    print(f"  - Issues found: {reviewer_result.get('code_review', {}).get('issues_found', 0)}")
    print(f"  - Review documentation:\n{reviewer_result.get('review_documentation', 'No documentation')}")
    print(f"  - Test status: {reviewer_result.get('qa_status', 'unknown')}")

if __name__ == "__main__":
    asyncio.run(main())



