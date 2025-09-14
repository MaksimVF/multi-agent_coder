




import os
from typing import Dict, Any, List, Optional
import json
import asyncio
from datetime import datetime

# Import LiteLLM for LLM integration
try:
    import litellm
    from litellm import completion
except ImportError:
    print("Warning: litellm not installed. Please install with 'pip install litellm'")

# Import LangGraph for agent coordination
try:
    from langgraph import AgentGraph, AgentNode
except ImportError:
    print("Warning: langgraph not installed. Please install with 'pip install langgraph'")
    # Fallback to simple graph implementation
    class AgentGraph:
        def __init__(self):
            self.nodes = {}
            self.edges = []

        def add_node(self, node):
            self.nodes[node.name] = node

        def add_edge(self, source, target):
            self.edges.append((source, target))

        async def execute(self, start_node, data):
            # Simple execution - just return the data
            return {"status": "completed", "results": data}

    class AgentNode:
        def __init__(self, agent_name, agent_instance):
            self.name = agent_name
            self.agent = agent_instance

# Import memory manager
try:
    from memory_manager import MemoryManager
except ImportError:
    print("Warning: memory_manager not found. Memory features will be disabled.")
    MemoryManager = None

# Import new components
try:
    from agent_registry import AgentRegistry
except ImportError:
    print("Warning: agent_registry not found. Agent registry features will be disabled.")
    class AgentRegistry:
        _registry = {}
        @classmethod
        def register(cls, name, agent_class, **kwargs): pass
        @classmethod
        def get_agent(cls, name): return None

try:
    from event_system import EventBus, EventType, AgentEvent
except ImportError:
    print("Warning: event_system not found. Event system features will be disabled.")
    class EventBus:
        def __init__(self): pass
        async def publish(self, event): pass
        def subscribe(self, event_type, callback): return "dummy_id"
        def unsubscribe(self, subscription_id): return False

try:
    from advanced_code_generator import AdvancedCodeGenerator
except ImportError:
    print("Warning: advanced_code_generator not found. Using basic code generation.")
    AdvancedCodeGenerator = None

class AgentWorkflow:
    """
    Enhanced Agent Workflow Coordinator with dynamic agent registration and event-driven architecture.

    Features:
    - Graph-based agent coordination
    - State management with memory
    - Error handling and recovery
    - Dynamic workflow adaptation
    - Short-term and long-term memory integration
    - Agent registry integration
    - Event-driven communication
    - Advanced code generation
    """

    def __init__(self, memory_manager: Optional["MemoryManager"] = None):
        """
        Initialize the Agent Workflow.

        Args:
            memory_manager: Memory manager for workflow memory
        """
        self.graph = AgentGraph()
        self.nodes = {}
        self.memory_manager = memory_manager
        self.event_bus = EventBus()
        self.state = {
            "task": None,
            "subtasks": [],
            "current_subtask": None,
            "results": {},
            "status": "initialized",
            "errors": [],
            "task_id": None,
        }

        # Set up event subscriptions
        self._setup_event_subscriptions()

    def _setup_event_subscriptions(self):
        """Set up event subscriptions for workflow management."""
        # Subscribe to task events
        self.event_bus.subscribe(EventType.TASK_CREATED, self._handle_task_created)
        self.event_bus.subscribe(EventType.TASK_UPDATED, self._handle_task_updated)
        self.event_bus.subscribe(EventType.SUBTASK_COMPLETED, self._handle_subtask_completed)
        self.event_bus.subscribe(EventType.ERROR_OCCURRED, self._handle_error)

    async def _handle_task_created(self, event: AgentEvent):
        """Handle task created events."""
        print(f"Task created: {event.data.get('task_id')}")
        self.state["task_id"] = event.data.get("task_id")

    async def _handle_task_updated(self, event: AgentEvent):
        """Handle task updated events."""
        print(f"Task updated: {event.data.get('task_id')}")
        if "status" in event.data:
            self.state["status"] = event.data["status"]

    async def _handle_subtask_completed(self, event: AgentEvent):
        """Handle subtask completed events."""
        print(f"Subtask completed: {event.data.get('subtask_id')}")
        # Update workflow state

    async def _handle_error(self, event: AgentEvent):
        """Handle error events."""
        print(f"Error occurred: {event.data.get('error')}")
        self.state["errors"].append(event.data.get("error", "Unknown error"))

    def add_agent(self, agent_name: str, agent_instance: Any) -> None:
        """
        Add an agent to the workflow and register it with the agent registry.

        Args:
            agent_name: Name of the agent
            agent_instance: Agent instance
        """
        # Register agent with the registry
        AgentRegistry.register(agent_name, agent_instance.__class__)

        # Create node and add to graph
        node = AgentNode(agent_name, agent_instance)
        self.nodes[agent_name] = node
        self.graph.add_node(node)

        # Publish agent registration event
        asyncio.create_task(self.event_bus.publish(
            AgentEvent(
                event_type=EventType.AGENT_REGISTERED,
                source="workflow",
                data={"agent_name": agent_name}
            )
        ))

    def add_edge(self, source: str, target: str) -> None:
        """
        Add a directed edge between two agents in the workflow.

        Args:
            source: Source agent name
            target: Target agent name
        """
        self.graph.add_edge(source, target)

    def set_initial_state(self, task: Dict, task_id: str = None) -> None:
        """
        Set the initial state of the workflow.

        Args:
            task: Task data
            task_id: Unique task identifier
        """
        self.state = {
            "task": task,
            "task_id": task_id or f"task_{int(datetime.now().timestamp())}",
            "subtasks": [],
            "current_subtask": None,
            "results": {},
            "status": "initialized",
            "errors": [],
        }

        # Store initial task in memory
        if self.memory_manager:
            self.memory_manager.store_short_term(
                f"{self.state['task_id']}:initial_task",
                task,
                expiration=86400,  # Keep for 24 hours
                metadata={"type": "task", "status": "initialized"},
            )

    async def execute_workflow(self) -> Dict:
        """
        Execute the workflow with enhanced features including:
        - Event-driven communication
        - Advanced code generation
        - Improved error handling
        - Dynamic agent discovery

        Returns:
            Workflow results
        """
        # Publish task started event
        await self.event_bus.publish(
            AgentEvent(
                event_type=EventType.TASK_UPDATED,
                source="workflow",
                data={"status": "running", "task_id": self.state["task_id"]}
            )
        )

        self.state["status"] = "running"

        # Update task status in memory
        if self.memory_manager:
            self.memory_manager.store_short_term(
                f"{self.state['task_id']}:status",
                {"status": "running"},
                expiration=86400,
                metadata={"type": "status"},
            )

        try:
            # Analyze task using dynamic agent discovery
            analyst = self._get_agent_instance("analyst")
            if analyst:
                subtasks = await analyst.analyze_task(self.state["task"]["description"])

                # Store analysis results in memory
                if self.memory_manager:
                    self.memory_manager.store_short_term(
                        f"{self.state['task_id']}:analysis",
                        subtasks,
                        expiration=86400,
                        metadata={"type": "analysis", "agent": "analyst"},
                    )

                self.state["subtasks"] = subtasks
                self.state["status"] = "task_analyzed"

                # Publish task analyzed event
                await self.event_bus.publish(
                    AgentEvent(
                        event_type=EventType.TASK_UPDATED,
                        source="workflow",
                        data={"status": "task_analyzed", "task_id": self.state["task_id"]}
                    )
                )

            # Process subtasks
            for i, subtask in enumerate(self.state["subtasks"]):
                self.state["current_subtask"] = subtask

                # Publish subtask started event
                await self.event_bus.publish(
                    AgentEvent(
                        event_type=EventType.SUBTASK_CREATED,
                        source="workflow",
                        data={
                            "subtask_id": f"subtask_{i}",
                            "task_id": self.state["task_id"],
                            "description": subtask.get("description", "")
                        }
                    )
                )

                # Store subtask in memory
                if self.memory_manager:
                    self.memory_manager.store_short_term(
                        f"{self.state['task_id']}:subtask_{i}",
                        subtask,
                        expiration=86400,
                        metadata={"type": "subtask", "index": i},
                    )

                # Use advanced code generator if available
                if AdvancedCodeGenerator:
                    code_generator = AdvancedCodeGenerator(memory_manager=self.memory_manager)
                    code_result = await code_generator.generate_code(
                        requirements=subtask,
                        language="python",
                        context={"task_id": self.state["task_id"], "subtask_index": i}
                    )
                else:
                    # Fallback to developer agent
                    developer = self._get_agent_instance("developer")
                    if developer:
                        code_result = await developer.develop_code(subtask, "python")
                    else:
                        code_result = {"code": "# No developer agent available", "status": "error"}

                # Store development result in memory
                if self.memory_manager:
                    self.memory_manager.store_short_term(
                        f"{self.state['task_id']}:subtask_{i}_code",
                        code_result,
                        expiration=86400,
                        metadata={"type": "code", "agent": "developer"},
                    )

                self.state["results"][f"subtask_{i}_code"] = code_result

                # Generate tests using advanced code generator
                if AdvancedCodeGenerator:
                    test_generator = AdvancedCodeGenerator(memory_manager=self.memory_manager)
                    test_result = await test_generator.generate_unit_tests(
                        code=code_result.get("code", ""),
                        requirements=subtask,
                        language="python"
                    )
                else:
                    # Fallback to tester agent
                    tester = self._get_agent_instance("tester")
                    if tester:
                        test_result = await tester.generate_tests(code_result)
                    else:
                        test_result = {"tests": "# No tester agent available", "status": "error"}

                # Store test result in memory
                if self.memory_manager:
                    self.memory_manager.store_short_term(
                        f"{self.state['task_id']}:subtask_{i}_tests",
                        test_result,
                        expiration=86400,
                        metadata={"type": "tests", "agent": "tester"},
                    )

                self.state["results"][f"subtask_{i}_tests"] = test_result

                # Optimize code using advanced code generator
                if AdvancedCodeGenerator:
                    optimizer = AdvancedCodeGenerator(memory_manager=self.memory_manager)
                    optimized_code = await optimizer.optimize_code(
                        code=code_result.get("code", ""),
                        requirements=subtask,
                        language="python"
                    )
                else:
                    # Fallback to optimizer agent
                    optimizer_agent = self._get_agent_instance("optimizer")
                    if optimizer_agent:
                        optimized_code = await optimizer_agent.optimize_code(code_result)
                    else:
                        optimized_code = {"optimized": code_result.get("code", ""), "status": "skipped"}

                # Store optimization result in memory
                if self.memory_manager:
                    self.memory_manager.store_short_term(
                        f"{self.state['task_id']}:subtask_{i}_optimized",
                        optimized_code,
                        expiration=86400,
                        metadata={"type": "optimized_code", "agent": "optimizer"},
                    )

                self.state["results"][f"subtask_{i}_optimized"] = optimized_code

                # Publish subtask completed event
                await self.event_bus.publish(
                    AgentEvent(
                        event_type=EventType.SUBTASK_COMPLETED,
                        source="workflow",
                        data={
                            "subtask_id": f"subtask_{i}",
                            "task_id": self.state["task_id"],
                            "status": "completed"
                        }
                    )
                )

            # Consolidate memory to long-term storage
            if self.memory_manager:
                self.memory_manager.consolidate_memory(self.state["task_id"])

            self.state["status"] = "completed"

            # Publish task completed event
            await self.event_bus.publish(
                AgentEvent(
                    event_type=EventType.TASK_COMPLETED,
                    source="workflow",
                    data={"task_id": self.state["task_id"], "status": "completed"}
                )
            )

            # Update final status in memory
            if self.memory_manager:
                self.memory_manager.store_short_term(
                    f"{self.state['task_id']}:status",
                    {"status": "completed"},
                    expiration=86400,
                    metadata={"type": "status"},
                )
                self.memory_manager.store_long_term(
                    json.dumps(self.state),
                    metadata={"type": "final_result", "task_id": self.state["task_id"]},
                    agent="workflow",
                    task_id=self.state["task_id"],
                    importance=1.0,
                )

            return self.state

        except Exception as e:
            self.state["status"] = "error"
            self.state["errors"].append(str(e))

            # Publish error event
            await self.event_bus.publish(
                AgentEvent(
                    event_type=EventType.ERROR_OCCURRED,
                    source="workflow",
                    data={"error": str(e), "task_id": self.state["task_id"]}
                )
            )

            # Store error in memory
            if self.memory_manager:
                self.memory_manager.store_short_term(
                    f"{self.state['task_id']}:error",
                    str(e),
                    expiration=86400,
                    metadata={"type": "error"},
                )
                self.memory_manager.store_short_term(
                    f"{self.state['task_id']}:status",
                    {"status": "error"},
                    expiration=86400,
                    metadata={"type": "status"},
                )

            return self.state

    def _get_agent_instance(self, agent_name: str) -> Optional[Any]:
        """Get agent instance by name with dynamic discovery."""
        # First check if agent is already in nodes
        if agent_name in self.nodes:
            return self.nodes[agent_name].agent

        # Try to discover agent from registry
        agent_class = AgentRegistry.get_agent(agent_name)
        if agent_class and hasattr(agent_class, "memory_manager"):
            # Create instance with memory manager if needed
            try:
                return agent_class(memory_manager=self.memory_manager)
            except Exception:
                try:
                    return agent_class()
                except Exception:
                    return None

        return None

    def get_status(self) -> Dict:
        """
        Get the current workflow status.

        Returns:
            Workflow status
        """
        # Get status from memory if available
        if self.memory_manager and self.state.get("task_id"):
            status_data = self.memory_manager.retrieve_short_term(
                f"{self.state['task_id']}:status"
            )
            if status_data:
                current_status = status_data.get("value", {}).get("status", self.state["status"])
            else:
                current_status = self.state["status"]
        else:
            current_status = self.state["status"]

        return {
            "status": current_status,
            "task": self.state["task"],
            "progress": f"{len(self.state['results'])}/{len(self.state['subtasks'])}",
            "errors": self.state["errors"],
            "task_id": self.state.get("task_id"),
        }

    def get_task_history(self, task_id: str) -> Dict:
        """
        Get the complete history for a task from memory.

        Args:
            task_id: Task identifier

        Returns:
            Task history data
        """
        if not self.memory_manager:
            return {}

        history = {}
        pattern = f"{task_id}:*"
        keys = self.memory_manager.redis_client.keys(pattern)

        for key in keys:
            data = self.memory_manager.retrieve_short_term(key)
            if data:
                history[key] = data

        return history

    def recover_task(self, task_id: str) -> bool:
        """
        Recover a task from memory.

        Args:
            task_id: Task identifier

        Returns:
            True if recovery successful, False otherwise
        """
        if not self.memory_manager:
            return False

        try:
            # Get initial task
            task_data = self.memory_manager.retrieve_short_term(
                f"{task_id}:initial_task"
            )
            if not task_data:
                return False

            # Get status
            status_data = self.memory_manager.retrieve_short_term(
                f"{task_id}:status"
            )
            status = status_data.get("value", {}).get("status", "unknown") if status_data else "unknown"

            # Get analysis
            analysis_data = self.memory_manager.retrieve_short_term(
                f"{task_id}:analysis"
            )
            analysis = analysis_data.get("value", []) if analysis_data else []

            # Get results
            results = {}
            pattern = f"{task_id}:subtask_*"
            keys = self.memory_manager.redis_client.keys(pattern)

            for key in keys:
                if "code" in key:
                    results.setdefault(key, self.memory_manager.retrieve_short_term(key))
                elif "tests" in key:
                    results.setdefault(key, self.memory_manager.retrieve_short_term(key))
                elif "optimized" in key:
                    results.setdefault(key, self.memory_manager.retrieve_short_term(key))

            # Restore state
            self.state = {
                "task": task_data.get("value", {}),
                "task_id": task_id,
                "subtasks": analysis,
                "current_subtask": None,
                "results": results,
                "status": status,
                "errors": [],
            }

            return True

        except Exception as e:
            print(f"Error recovering task: {e}")
            return False


