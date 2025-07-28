



import os
from typing import Dict, Any, Optional, List
import json
import asyncio

# Import LiteLLM for LLM integration
try:
    import litellm
    from litellm import completion
except ImportError:
    print("Warning: litellm not installed. Please install with 'pip install litellm'")

# Import memory manager
try:
    from memory_manager import MemoryManager
except ImportError:
    print("Warning: memory_manager not found. Memory features will be disabled.")
    MemoryManager = None

class BaseLLMAgent:
    """Base class for LLM-powered agents."""

    def __init__(
        self,
        model: str = "gpt-4o",
        temperature: float = 0.7,
        max_tokens: int = 1000,
        memory_manager: Optional["MemoryManager"] = None,
    ):
        """
        Initialize the LLM-powered agent.

        Args:
            model: The LLM model to use (default: gpt-4o)
            temperature: Creativity level (0.0-1.0)
            max_tokens: Maximum tokens for LLM responses
            memory_manager: Memory manager for agent memory
        """
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.memory_manager = memory_manager

        # Set up LiteLLM configuration
        self.litellm_config = {
            "model": self.model,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "api_key": self._get_api_key()
        }

        # Agent memory and state
        self.memory = {}
        self.conversation_history = []

    def _get_api_key(self) -> Optional[str]:
        """Get API key from environment variables."""
        # Try to get from environment variables
        api_key = os.environ.get("OPENAI_API_KEY") or os.environ.get("LITELLM_API_KEY")

        # If no API key found, warn the user
        if not api_key or api_key == "mock_key":
            print("Warning: No API key found. Set OPENAI_API_KEY or LITELLM_API_KEY environment variable.")
            print("Falling back to mock mode...")
            return "mock_key"

        return api_key

    async def _call_llm(self, prompt: str, system_message: Optional[str] = None) -> Dict[str, Any]:
        """
        Call the LLM with a prompt.

        Args:
            prompt: The input prompt
            system_message: Optional system message for context

        Returns:
            Dictionary with LLM response
        """
        try:
            # Prepare messages
            messages = []

            if system_message:
                messages.append({"role": "system", "content": system_message})

            # Add conversation history (last few exchanges)
            if self.conversation_history:
                # Add up to 5 recent exchanges to maintain context
                recent_history = self.conversation_history[-5:]
                messages.extend(recent_history)

            messages.append({"role": "user", "content": prompt})

            # Call LiteLLM
            response = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: completion(
                    model=self.model,
                    messages=messages,
                    temperature=float(self.temperature),
                    max_tokens=self.max_tokens,
                    api_key=self.litellm_config["api_key"]
                )
            )

            # Update conversation history
            self.conversation_history.append({"role": "user", "content": prompt})
            self.conversation_history.append({"role": "assistant", "content": response["choices"][0]["message"]["content"]})

            return {
                "success": True,
                "response": response["choices"][0]["message"]["content"],
                "usage": response.get("usage", {})
            }

        except Exception as e:
            print(f"Error calling LLM: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "response": f"Error: {str(e)}"
            }

    def update_memory(self, key: str, value: Any):
        """Update agent memory."""
        self.memory[key] = value

    def get_memory(self, key: str) -> Any:
        """Get value from agent memory."""
        return self.memory.get(key, None)

    def clear_memory(self):
        """Clear agent memory."""
        self.memory = {}

    def clear_conversation_history(self):
        """Clear conversation history."""
        self.conversation_history = []

    async def generate_response(self, prompt: str, system_message: Optional[str] = None) -> str:
        """
        Generate a response from the LLM.

        Args:
            prompt: Input prompt
            system_message: Optional system message

        Returns:
            LLM response text
        """
        result = await self._call_llm(prompt, system_message)
        return result["response"] if result["success"] else f"Error: {result['error']}"

    def store_memory(
        self,
        key: str,
        value: Any,
        memory_type: str = "short",
        expiration: int = 3600,
        metadata: Optional[Dict] = None,
    ) -> bool:
        """
        Store data in memory.

        Args:
            key: Memory key
            value: Data to store
            memory_type: "short" for Redis, "long" for Weaviate
            expiration: Expiration time in seconds (for short-term)
            metadata: Additional metadata

        Returns:
            True if successful, False otherwise
        """
        if not self.memory_manager:
            print("Warning: Memory manager not available")
            return False

        if memory_type == "short":
            return self.memory_manager.store_short_term(key, value, expiration, metadata)
        elif memory_type == "long":
            return self.memory_manager.store_long_term(
                str(value),
                metadata=metadata,
                agent=self.__class__.__name__,
                task_id=metadata.get("task_id", "unknown") if metadata else "unknown",
            ) is not None
        else:
            print(f"Error: Unknown memory type: {memory_type}")
            return False

    def retrieve_memory(
        self,
        key: str,
        memory_type: str = "short",
        query: Optional[str] = None,
        limit: int = 5,
    ) -> Any:
        """
        Retrieve data from memory.

        Args:
            key: Memory key (for short-term)
            memory_type: "short" for Redis, "long" for Weaviate
            query: Search query (for long-term)
            limit: Maximum results (for long-term)

        Returns:
            Retrieved data
        """
        if not self.memory_manager:
            print("Warning: Memory manager not available")
            return None

        if memory_type == "short":
            return self.memory_manager.retrieve_short_term(key)
        elif memory_type == "long":
            if not query:
                print("Error: Query required for long-term memory retrieval")
                return None
            return self.memory_manager.retrieve_long_term(query, limit=limit)
        else:
            print(f"Error: Unknown memory type: {memory_type}")
            return None

    def consolidate_memory(self, task_id: str) -> None:
        """
        Consolidate short-term memory to long-term memory.

        Args:
            task_id: Task ID to consolidate
        """
        if self.memory_manager:
            self.memory_manager.consolidate_memory(task_id, self.__class__.__name__)

    def get_recent_memory(self, hours: int = 24, limit: int = 10) -> List[Dict]:
        """
        Get recent memory entries.

        Args:
            hours: Time window in hours
            limit: Maximum results

        Returns:
            List of recent memory entries
        """
        if not self.memory_manager:
            return []
        return self.memory_manager.get_recent_memory(self.__class__.__name__, limit, hours)

