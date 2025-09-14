


from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseRole(ABC):
    """Base class for all agent roles"""

    def __init__(self, name: str, description: str, tools: List[str] = None):
        self.name = name
        self.description = description
        self.tools = tools or []
        self.state = {}

    @abstractmethod
    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the role's main functionality"""
        pass

    def add_tool(self, tool_name: str):
        """Add a tool to the role"""
        if tool_name not in self.tools:
            self.tools.append(tool_name)

    def update_state(self, key: str, value: Any):
        """Update the role's internal state"""
        self.state[key] = value

    def get_state(self, key: str) -> Any:
        """Get a value from the role's state"""
        return self.state.get(key)

