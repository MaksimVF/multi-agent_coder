



import os
import json
import asyncio
import unittest
from unittest.mock import patch, MagicMock

# Import agent classes
try:
    from memory_manager import MemoryManager
    from base_llm_agent import BaseLLMAgent
    from analyst import Analyst
    from developer import Developer
    from tester import Tester
    from optimizer import Optimizer
    from researcher import Researcher
    from agent_workflow import AgentWorkflow
except ImportError as e:
    print(f"Error importing agent modules: {e}")
    raise

class TestMemoryIntegration(unittest.IsolatedAsyncioTestCase):
    """Test memory integration in the multi-agent coder system."""

    async def asyncSetUp(self):
        """Set up test environment."""
        # Mock memory manager for testing
        self.memory_manager = MemoryManager(
            redis_host=os.getenv("REDIS_HOST", "localhost"),
            redis_port=int(os.getenv("REDIS_PORT", 6379)),
            weaviate_url=os.getenv("WEAVIATE_URL", "http://localhost:8080"),
        )

        # Initialize agents with memory manager
        self.analyst = Analyst(memory_manager=self.memory_manager)
        self.developer = Developer(memory_manager=self.memory_manager)
        self.tester = Tester(memory_manager=self.memory_manager)
        self.optimizer = Optimizer(memory_manager=self.memory_manager)
        self.researcher = Researcher(memory_manager=self.memory_manager)

        # Initialize workflow with memory manager
        self.workflow = AgentWorkflow(memory_manager=self.memory_manager)

        # Add agents to workflow
        self.workflow.add_agent("analyst", self.analyst)
        self.workflow.add_agent("developer", self.developer)
        self.workflow.add_agent("tester", self.tester)
        self.workflow.add_agent("optimizer", self.optimizer)
        self.workflow.add_agent("researcher", self.researcher)

    async def asyncTearDown(self):
        """Clean up test environment."""
        if self.memory_manager:
            self.memory_manager.close()

    @patch("litellm.completion")
    async def test_memory_integration(self, mock_completion):
        """Test memory integration in the workflow."""
        # Mock LLM responses
        mock_completion.return_value = {
            "choices": [{"message": {"content": "Mock response"}}],
            "usage": {"total_tokens": 100},
        }

        # Define a sample task
        sample_task = {
            "id": "test_task_001",
            "description": "Test memory integration",
            "requirements": ["Use memory", "Test integration"],
        }

        # Set initial state
        self.workflow.set_initial_state(sample_task, task_id=sample_task["id"])

        # Execute workflow
        result = await self.workflow.execute_workflow()

        # Verify memory storage
        task_history = self.workflow.get_task_history(sample_task["id"])
        self.assertGreater(len(task_history), 0, "Task history should not be empty")

        # Verify memory recovery
        recovery_result = self.workflow.recover_task(sample_task["id"])
        self.assertTrue(recovery_result, "Task recovery should be successful")

    @patch("litellm.completion")
    async def test_knowledge_base_population(self, mock_completion):
        """Test knowledge base population."""
        # Mock LLM responses
        mock_completion.return_value = {
            "choices": [{"message": {"content": "Mock research result"}}],
            "usage": {"total_tokens": 100},
        }

        # Test knowledge base population
        research_topics = ["Test topic 1", "Test topic 2"]
        kb_result = await self.researcher.populate_knowledge_base(research_topics)

        # Verify knowledge base population
        self.assertEqual(kb_result["topics_researched"], len(research_topics))
        self.assertEqual(kb_result["status"], "completed")

    @patch("litellm.completion")
    async def test_memory_consolidation(self, mock_completion):
        """Test memory consolidation."""
        # Mock LLM responses
        mock_completion.return_value = {
            "choices": [{"message": {"content": "Mock response"}}],
            "usage": {"total_tokens": 100},
        }

        # Define a sample task
        sample_task = {
            "id": "test_consolidation_001",
            "description": "Test memory consolidation",
            "requirements": ["Test consolidation"],
        }

        # Set initial state
        self.workflow.set_initial_state(sample_task, task_id=sample_task["id"])

        # Execute workflow
        result = await self.workflow.execute_workflow()

        # Consolidate memory
        self.memory_manager.consolidate_memory(sample_task["id"])

        # Verify long-term memory
        long_term_results = self.memory_manager.retrieve_long_term(
            sample_task["description"],
            limit=5
        )
        self.assertGreater(len(long_term_results), 0, "Long-term memory should contain results")

    async def test_memory_fallback(self):
        """Test memory fallback when memory manager is not available."""
        # Create agent without memory manager
        agent_no_memory = BaseLLMAgent()

        # Test memory operations without memory manager
        store_result = agent_no_memory.store_memory("test_key", "test_value")
        self.assertFalse(store_result, "Memory operations should fail without memory manager")

        retrieve_result = agent_no_memory.retrieve_memory("test_key")
        self.assertIsNone(retrieve_result, "Memory retrieval should return None without memory manager")

if __name__ == "__main__":
    unittest.main()



