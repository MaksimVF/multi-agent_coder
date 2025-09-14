





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
    from roles.librarian import LibrarianAgent
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
    librarian = LibrarianAgent(memory_manager=memory_manager)

    # Register agents with the registry
    AgentRegistry.register("analyst", Analyst, version="2.0", description="Task analysis agent")
    AgentRegistry.register("developer", Developer, version="2.0", description="Code development agent")
    AgentRegistry.register("tester", Tester, version="2.0", description="Code testing agent")
    AgentRegistry.register("optimizer", Optimizer, version="2.0", description="Code optimization agent")
    AgentRegistry.register("researcher", Researcher, version="2.0", description="Research agent")
    AgentRegistry.register("librarian", LibrarianAgent, version="1.0", description="Knowledge management agent")

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
    workflow.add_agent("librarian", librarian)

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

    # Demonstrate Librarian Agent functionality
    print("\n📚 Demonstrating Librarian Agent Knowledge Search:")
    print("  - Searching for relevant knowledge about Fibonacci algorithms")

    # Use librarian to search for knowledge
    search_results = await librarian.search_knowledge(
        query="Fibonacci sequence algorithms with memoization",
        task_id=sample_task["id"],
        agent="researcher"
    )

    print(f"  - Found {len(search_results)} relevant knowledge items:")
    for i, result in enumerate(search_results[:3]):  # Show top 3 results
        print(f"    {i+1}. Relevance: {result['relevance']:.2f}")
        print(f"       Source: {result['source']}")
        print(f"       Content: {result['content'][:100]}...")
        print(f"       Metadata: {result['metadata']}")

    # Demonstrate context analysis
    print("\n🔍 Demonstrating Librarian Agent Context Analysis:")
    context_analysis = await librarian.analyze_context({
        "microagent_knowledge": [
            {
                "name": "python_microagent",
                "trigger": "Fibonacci",
                "content": "Fibonacci sequence is a series where each number is the sum of the two preceding ones."
            }
        ],
        "repo_instructions": [
            {
                "name": "coding_standards",
                "content": "All code must follow PEP 8 standards and include type hints."
            }
        ]
    })

    print(f"  - Generated {len(context_analysis['insights'])} insights:")
    for insight in context_analysis['insights']:
        print(f"    - {insight['type']}: {insight['analysis']}")

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

    # Demonstrate full workflow
    print("\n🚀 Demonstrating Full Workflow (MetaGPT-inspired):")
    print("  - Using all roles including Project Manager, Documentation Specialist, and Git Integrator")

    # Create and run role coordinator with full workflow
    full_coordinator = RoleCoordinator(
        use_unified_roles=True,
        use_task_decomposer=True,
        use_reviewer=True,
        use_full_workflow=True
    )

    # Run the full workflow
    print("  - Running full workflow...")
    full_result = await full_coordinator.run_workflow(project_requirements)

    # Show results
    print("  - Full workflow completed successfully!")
    print(f"  - Project plan: {full_result.get('project_plan', {}).get('project_name', 'No project name')}")
    print(f"  - Sprints planned: {full_result.get('sprint_plan', {}).get('total_sprints', 0)}")
    print(f"  - Progress: {full_result.get('progress_report', {}).get('progress_percentage', 0):.1f}%")
    print(f"  - Generated architecture: {len(full_result.get('system_architecture', {}).get('components', {}))} components")
    print(f"  - Task list: {len(full_result.get('task_list', []))} tasks")
    print(f"  - Code review score: {full_result.get('code_review', {}).get('quality_score', 0):.1f}/10")
    print(f"  - Documentation files: {len(full_result.get('documentation_files', {}))}")
    print(f"  - Git status: {full_result.get('git_status', {}).get('status', 'unknown')}")
    print(f"  - Test status: {full_result.get('qa_status', 'unknown')}")

    # Demonstrate workflow with TestRunner
    print("\n🧪 Demonstrating Workflow with TestRunner (Devika-inspired):")
    print("  - Using TestRunner for automated testing and error fixing")

    # Create and run role coordinator with TestRunner
    test_runner_coordinator = RoleCoordinator(
        use_unified_roles=True,
        use_task_decomposer=True,
        use_reviewer=True,
        use_full_workflow=True,
        use_test_runner=True
    )

    # Run the workflow with TestRunner
    print("  - Running workflow with TestRunner...")
    test_runner_result = await test_runner_coordinator.run_workflow(project_requirements)

    # Show results
    print("  - TestRunner workflow completed!")
    print(f"  - Test results: {test_runner_result.get('test_results', {}).get('status', 'unknown')}")
    print(f"  - Tests run: {test_runner_result.get('test_results', {}).get('tests_run', 0)}")
    print(f"  - Tests passed: {test_runner_result.get('test_results', {}).get('tests_passed', 0)}")
    print(f"  - Tests failed: {test_runner_result.get('test_results', {}).get('tests_failed', 0)}")
    print(f"  - Coverage: {test_runner_result.get('test_results', {}).get('coverage', 0):.1f}%")
    print(f"  - Fix attempts: {test_runner_result.get('fix_attempts', 0)}")
    print(f"  - Error logs: {len(test_runner_result.get('error_logs', {}).get('error_logs', []))}")
    print(f"  - Git status: {test_runner_result.get('git_status', {}).get('status', 'unknown')}")

    # Demonstrate workflow with AgentMonitor
    print("\n🔍 Demonstrating Workflow with AgentMonitor:")
    print("  - Using AgentMonitor for error handling and agent recovery")

    # Create and run role coordinator with AgentMonitor
    agent_monitor_coordinator = RoleCoordinator(
        use_unified_roles=True,
        use_task_decomposer=True,
        use_reviewer=True,
        use_full_workflow=True,
        use_test_runner=True,
        use_agent_monitor=True
    )

    # Run the workflow with AgentMonitor
    print("  - Running workflow with AgentMonitor...")
    agent_monitor_result = await agent_monitor_coordinator.run_workflow(project_requirements)

    # Show results
    print("  - AgentMonitor workflow completed!")
    print(f"  - Agent status: {len(agent_monitor_result.get('agent_status', {}))} agents monitored")
    print(f"  - Error log: {len(agent_monitor_result.get('error_log', []))} errors logged")
    print(f"  - Monitoring status: {agent_monitor_result.get('monitoring_status', 'unknown')}")
    print(f"  - Test results: {agent_monitor_result.get('test_results', {}).get('status', 'unknown')}")
    print(f"  - Git status: {agent_monitor_result.get('git_status', {}).get('status', 'unknown')}")

if __name__ == "__main__":
    asyncio.run(main())



