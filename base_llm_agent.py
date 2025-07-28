
import os
from typing import Dict, Any, Optional
import json
import asyncio

# Import LiteLLM for LLM integration
try:
    import litellm
    from litellm import completion
except ImportError:
    print("Warning: litellm not installed. Please install with 'pip install litellm'")

class BaseLLMAgent:
    """Base class for LLM-powered agents."""

    def __init__(self, model: str = "gpt-4o", temperature: float = 0.7, max_tokens: int = 1000):
        """
        Initialize the LLM-powered agent.

        Args:
            model: The LLM model to use (default: gpt-4o)
            temperature: Creativity level (0.0-1.0)
            max_tokens: Maximum tokens for LLM responses
        """
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens

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
                    temperature=self.temperature,
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
