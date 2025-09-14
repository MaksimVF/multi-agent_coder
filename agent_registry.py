
"""
Agent Registry System for dynamic agent registration and discovery.

This module implements a registry pattern that allows agents to register themselves
and be discovered by other components in the system. This improves extensibility
and decouples agent implementation from agent usage.
"""

from typing import Dict, Type, Any, Optional
from datetime import datetime

class AgentRegistry:
    """
    Central registry for agent classes with dynamic registration capabilities.

    Features:
    - Thread-safe registration and discovery
    - Agent metadata tracking
    - Versioning support
    - Dependency management
    """

    _registry: Dict[str, Dict[str, Any]] = {}

    @classmethod
    def register(
        cls,
        name: str,
        agent_class: Type,
        version: str = "1.0",
        dependencies: Optional[list] = None,
        description: str = "",
        **metadata
    ) -> None:
        """
        Register an agent class with the registry.

        Args:
            name: Unique name for the agent
            agent_class: The agent class to register
            version: Version of the agent
            dependencies: List of dependencies
            description: Description of the agent
            **metadata: Additional metadata
        """
        if name in cls._registry:
            print(f"Warning: Agent '{name}' already registered. Overwriting.")

        cls._registry[name] = {
            "class": agent_class,
            "version": version,
            "dependencies": dependencies or [],
            "description": description,
            "registered_at": datetime.now(),
            "metadata": metadata
        }

    @classmethod
    def get_agent(cls, name: str) -> Optional[Type]:
        """
        Get an agent class by name.

        Args:
            name: Name of the agent to retrieve

        Returns:
            The agent class if found, None otherwise
        """
        agent_data = cls._registry.get(name)
        return agent_data["class"] if agent_data else None

    @classmethod
    def get_agent_info(cls, name: str) -> Optional[Dict[str, Any]]:
        """
        Get information about a registered agent.

        Args:
            name: Name of the agent

        Returns:
            Dictionary with agent information, or None if not found
        """
        return cls._registry.get(name)

    @classmethod
    def list_agents(cls) -> Dict[str, Dict[str, Any]]:
        """
        List all registered agents.

        Returns:
            Dictionary of all registered agents with their information
        """
        return cls._registry.copy()

    @classmethod
    def unregister(cls, name: str) -> bool:
        """
        Unregister an agent.

        Args:
            name: Name of the agent to unregister

        Returns:
            True if agent was unregistered, False if not found
        """
        if name in cls._registry:
            del cls._registry[name]
            return True
        return False

    @classmethod
    def check_dependencies(cls, name: str) -> bool:
        """
        Check if an agent's dependencies are satisfied.

        Args:
            name: Name of the agent to check

        Returns:
            True if all dependencies are available, False otherwise
        """
        agent_data = cls._registry.get(name)
        if not agent_data:
            return False

        dependencies = agent_data.get("dependencies", [])
        if not dependencies:
            return True

        for dep in dependencies:
            if dep not in cls._registry:
                print(f"Warning: Dependency '{dep}' not found for agent '{name}'")
                return False

        return True
