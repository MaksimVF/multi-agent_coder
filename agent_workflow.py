




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

class AgentWorkflow:
    """
    Agent Workflow Coordinator using LangGraph with memory integration.

    Features:
    - Graph-based agent coordination
    - State management with memory
    - Error handling and recovery
    - Dynamic workflow adaptation
    - Short-term and long-term memory integration
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
        self.state = {
            "task": None,
            "subtasks": [],
            "current_subtask": None,
            "results": {},
            "status": "initialized",
            "errors": [],
            "task_id": None,
        }

    def add_agent(self, agent_name: str, agent_instance: Any) -> None:
        """
        Add an agent to the workflow.

        Args:
            agent_name: Name of the agent
            agent_instance: Agent instance
        """
        node = AgentNode(agent_name, agent_instance)
        self.nodes[agent_name] = node
        self.graph.add_node(node)

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
        Execute the workflow with memory integration.

        Returns:
            Workflow results
        """
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
            # Analyze task
            if "analyst" in self.nodes:
                analyst = self.nodes["analyst"].agent
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

                # Update status in memory
                if self.memory_manager:
                    self.memory_manager.store_short_term(
                        f"{self.state['task_id']}:status",
                        {"status": "task_analyzed"},
                        expiration=86400,
                        metadata={"type": "status"},
                    )

            # Process subtasks
            for i, subtask in enumerate(self.state["subtasks"]):
                self.state["current_subtask"] = subtask

                # Store subtask in memory
                if self.memory_manager:
                    self.memory_manager.store_short_term(
                        f"{self.state['task_id']}:subtask_{i}",
                        subtask,
                        expiration=86400,
                        metadata={"type": "subtask", "index": i},
                    )

                # Develop code
                if "developer" in self.nodes:
                    developer = self.nodes["developer"].agent
                    code_result = await developer.develop_code(subtask, "python")

                    # Store development result in memory
                    if self.memory_manager:
                        self.memory_manager.store_short_term(
                            f"{self.state['task_id']}:subtask_{i}_code",
                            code_result,
                            expiration=86400,
                            metadata={"type": "code", "agent": "developer"},
                        )

                    self.state["results"][f"subtask_{i}_code"] = code_result

                # Test code
                if "tester" in self.nodes:
                    tester = self.nodes["tester"].agent
                    test_result = await tester.generate_tests(code_result)

                    # Store test result in memory
                    if self.memory_manager:
                        self.memory_manager.store_short_term(
                            f"{self.state['task_id']}:subtask_{i}_tests",
                            test_result,
                            expiration=86400,
                            metadata={"type": "tests", "agent": "tester"},
                        )

                    self.state["results"][f"subtask_{i}_tests"] = test_result

                # Optimize code
                if "optimizer" in self.nodes:
                    optimizer = self.nodes["optimizer"].agent
                    optimized_code = await optimizer.optimize_code(code_result)

                    # Store optimization result in memory
                    if self.memory_manager:
                        self.memory_manager.store_short_term(
                            f"{self.state['task_id']}:subtask_{i}_optimized",
                            optimized_code,
                            expiration=86400,
                            metadata={"type": "optimized_code", "agent": "optimizer"},
                        )

                    self.state["results"][f"subtask_{i}_optimized"] = optimized_code

            # Consolidate memory to long-term storage
            if self.memory_manager:
                self.memory_manager.consolidate_memory(self.state["task_id"])

            self.state["status"] = "completed"

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


