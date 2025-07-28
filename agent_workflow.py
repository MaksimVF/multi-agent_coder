




import asyncio
from typing import Dict, Any, List, Optional
import json

# Import LangGraph for agent coordination
try:
    from langgraph.graph import Graph
    from langgraph.graph import Node, Edge
except ImportError:
    print("Warning: langgraph not installed. Please install with 'pip install langgraph'")
    # Fallback to simple graph implementation
    class Node:
        def __init__(self, name, processor):
            self.name = name
            self.processor = processor

    class Edge:
        def __init__(self, source, target, condition=None):
            self.source = source
            self.target = target
            self.condition = condition

    class Graph:
        def __init__(self):
            self.nodes = {}
            self.edges = []

        def add_node(self, node):
            self.nodes[node.name] = node

        def add_edge(self, edge):
            self.edges.append((edge.source, edge.target))

        async def execute(self, start_node, data):
            # Simple sequential execution
            current = start_node
            result = data

            while current:
                # Find the next node
                next_node = None
                for source, target in self.edges:
                    if source == current:
                        next_node = target
                        break

                # Process current node
                if current in self.nodes:
                    node = self.nodes[current]
                    if hasattr(node.processor, 'process'):
                        result = await node.processor.process(result)
                    elif hasattr(node.processor, '__call__'):
                        result = await node.processor(result)

                # Move to next node
                if next_node:
                    current = next_node
                else:
                    break

            return result

class AgentWorkflow:
    """Agent workflow manager using LangGraph."""

    def __init__(self):
        """Initialize the agent workflow."""
        self.graph = Graph()
        self.agents = {}
        self.workflow_state = {}

    def register_agent(self, name: str, agent):
        """Register an agent with the workflow."""
        self.agents[name] = agent
        # Create a node for the agent
        node = Node(name=name, processor=agent)
        self.graph.add_node(node)

    def add_edge(self, source: str, target: str, condition: Optional[str] = None):
        """Add a directed edge between agents."""
        self.graph.add_edge(Edge(source=source, target=target, condition=condition))

    async def execute_workflow(self, start_agent: str, initial_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the agent workflow."""
        try:
            # Initialize workflow state
            self.workflow_state = {
                "current_agent": start_agent,
                "data": initial_data,
                "history": [],
                "status": "running"
            }

            # Execute the workflow
            result = await self.graph.execute(start_agent, initial_data)

            # Update workflow state
            self.workflow_state["status"] = "completed"
            self.workflow_state["result"] = result

            return {
                "status": "completed",
                "data": result,
                "workflow_state": self.workflow_state
            }

        except Exception as e:
            self.workflow_state["status"] = "failed"
            self.workflow_state["error"] = str(e)

            return {
                "status": "failed",
                "error": str(e),
                "workflow_state": self.workflow_state
            }

    def get_workflow_state(self) -> Dict[str, Any]:
        """Get the current workflow state."""
        return self.workflow_state

    def get_available_agents(self) -> List[str]:
        """Get a list of registered agents."""
        return list(self.agents.keys())

    def get_agent(self, name: str) -> Optional[Any]:
        """Get an agent by name."""
        return self.agents.get(name)

    async def run_agent(self, agent_name: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Run a single agent with the given data."""
        if agent_name not in self.agents:
            return {
                "status": "error",
                "error": f"Agent '{agent_name}' not found"
            }

        agent = self.agents[agent_name]

        try:
            # Check if the agent has a process method
            if hasattr(agent, 'process'):
                result = await agent.process(data)
            else:
                # Try to call the agent with the data
                result = await agent(data)

            return {
                "status": "completed",
                "result": result
            }

        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }

    def visualize_workflow(self) -> str:
        """Generate a simple visualization of the workflow."""
        visualization = "Workflow Visualization:\n"

        # Show nodes
        visualization += "Agents:\n"
        for agent_name in self.agents:
            visualization += f"  - {agent_name}\n"

        # Show edges
        visualization += "\nConnections:\n"
        for source, target in self.graph.edges:
            visualization += f"  {source} -> {target}\n"

        return visualization




