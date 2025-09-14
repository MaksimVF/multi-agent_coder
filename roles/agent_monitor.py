











import os
import time
import asyncio
import traceback
from typing import Dict, Any, List, Optional
from .base_role import BaseRole

class AgentMonitor(BaseRole):
    """Agent Monitor role - monitors agent execution, handles errors, and manages restarts"""

    def __init__(self):
        super().__init__(
            name="AgentMonitor",
            description="Monitors agent execution, handles errors, and manages restarts",
            tools=["agent_monitoring", "error_handling", "restart_management", "logging"]
        )
        self.agent_status = {}
        self.error_log = []
        self.max_retries = 3
        self.timeout = 30  # seconds

    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Monitor agent execution and handle errors"""
        # Get agent information from context
        agents = context.get("agents", [])
        workflow = context.get("workflow", [])

        # Initialize monitoring
        await self._initialize_monitoring(agents)

        # Monitor each agent in the workflow
        for agent_name in workflow:
            try:
                # Execute agent with monitoring
                result = await self._execute_with_monitoring(agent_name, context)

                # Update context with agent results
                context.update(result)

                # Update agent status
                self.agent_status[agent_name]["status"] = "completed"
                self.agent_status[agent_name]["retries"] = 0

            except Exception as e:
                # Handle agent failure
                await self._handle_agent_failure(agent_name, str(e), context)

        return {
            "agent_status": self.agent_status,
            "error_log": self.error_log,
            "monitoring_status": "completed",
            "next_role": None  # Final role in workflow
        }

    async def _initialize_monitoring(self, agents: List[str]) -> None:
        """Initialize monitoring for all agents"""
        for agent_name in agents:
            self.agent_status[agent_name] = {
                "status": "pending",
                "start_time": None,
                "end_time": None,
                "retries": 0,
                "errors": []
            }

    async def _execute_with_monitoring(self, agent_name: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute agent with timeout and error handling"""
        # Update agent status
        self.agent_status[agent_name]["status"] = "running"
        self.agent_status[agent_name]["start_time"] = time.time()

        try:
            # Get agent instance
            agent = self._get_agent_instance(agent_name)

            # Execute agent with timeout
            result = await asyncio.wait_for(agent.execute(context), timeout=self.timeout)

            # Update agent status
            self.agent_status[agent_name]["status"] = "completed"
            self.agent_status[agent_name]["end_time"] = time.time()

            return result

        except asyncio.TimeoutError:
            # Handle timeout
            error_msg = f"Agent {agent_name} exceeded timeout of {self.timeout} seconds"
            self._log_error(agent_name, error_msg)
            raise Exception(error_msg)

        except Exception as e:
            # Handle other errors
            error_msg = f"Agent {agent_name} failed with error: {str(e)}"
            self._log_error(agent_name, error_msg)
            raise Exception(error_msg)

    async def _handle_agent_failure(self, agent_name: str, error: str, context: Dict[str, Any]) -> None:
        """Handle agent failure with retries"""
        # Update agent status
        self.agent_status[agent_name]["status"] = "failed"
        self.agent_status[agent_name]["retries"] += 1

        # Log error
        self._log_error(agent_name, error)

        # Check if retries exceeded
        if self.agent_status[agent_name]["retries"] > self.max_retries:
            # Give up after max retries
            final_error = f"Agent {agent_name} failed after {self.max_retries} retries"
            self._log_error(agent_name, final_error)
            raise Exception(final_error)

        # Wait before retry
        await asyncio.sleep(2 ** self.agent_status[agent_name]["retries"])  # Exponential backoff

        # Retry agent execution
        result = await self._execute_with_monitoring(agent_name, context)

        # Update context with retry results
        context.update(result)

    def _get_agent_instance(self, agent_name: str) -> BaseRole:
        """Get agent instance by name"""
        # This would be implemented to get the actual agent instance
        # For now, return a mock agent
        return MockAgent(agent_name)

    def _log_error(self, agent_name: str, error: str) -> None:
        """Log error for an agent"""
        error_entry = {
            "agent": agent_name,
            "error": error,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "retries": self.agent_status[agent_name]["retries"]
        }
        self.error_log.append(error_entry)

        # Write to error log file
        with open("agent_errors.log", "a") as f:
            f.write(f"Agent: {agent_name}\n")
            f.write(f"Error: {error}\n")
            f.write(f"Timestamp: {error_entry['timestamp']}\n")
            f.write(f"Retries: {error_entry['retries']}\n")
            f.write("="*50 + "\n")

    async def _detect_infinite_loops(self, agent_name: str, context: Dict[str, Any]) -> bool:
        """Detect infinite loops in agent execution"""
        # Check if agent is taking too long
        if self.agent_status[agent_name]["status"] == "running":
            elapsed = time.time() - self.agent_status[agent_name]["start_time"]
            if elapsed > self.timeout * 2:  # Double timeout for loop detection
                error_msg = f"Agent {agent_name} may be in an infinite loop (elapsed: {elapsed}s)"
                self._log_error(agent_name, error_msg)
                return True
        return False

    async def _graceful_shutdown(self, agent_name: str) -> None:
        """Gracefully shutdown an agent"""
        # Update agent status
        self.agent_status[agent_name]["status"] = "stopped"
        self.agent_status[agent_name]["end_time"] = time.time()

        # Log shutdown
        self._log_error(agent_name, "Agent gracefully stopped")

class MockAgent(BaseRole):
    """Mock agent for testing AgentMonitor"""

    def __init__(self, name: str):
        super().__init__(
            name=name,
            description=f"Mock agent for {name}",
            tools=["mock_execution"]
        )

    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Mock agent execution"""
        # Simulate some work
        await asyncio.sleep(1)

        # Return mock results
        return {
            f"{self.name}_result": "success",
            "next_role": None
        }











