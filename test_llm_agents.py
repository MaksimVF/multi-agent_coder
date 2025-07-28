





import os
import json
import asyncio
import unittest
from unittest.mock import patch, MagicMock

# Import agent classes
try:
    from analyst import Analyst
    from developer import Developer
    from tester import Tester
    from optimizer import Optimizer
    from researcher import Researcher
    from agent_workflow import AgentWorkflow
    from memory_manager import MemoryManager
except ImportError as e:
    print(f"Error importing agent modules: {e}")
    raise

class TestLLMAgents(unittest.IsolatedAsyncioTestCase):
    """Test LLM-powered agents with memory integration."""

    async def asyncSetUp(self):
        """Set up test environment."""
        # Initialize memory manager
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
    async def test_analyst_task_analysis(self, mock_completion):
        """Test Analyst task analysis with memory."""
        # Mock LLM response
        mock_completion.return_value = {
            "choices": [{"message": {"content": '["subtask1", "subtask2"]'}}],
            "usage": {"total_tokens": 100},
        }

        # Test task analysis
        task_description = "Create a Python function to calculate Fibonacci numbers"
        result = await self.analyst.analyze_task(task_description)

        # Verify result
        self.assertIn("subtasks", result)
        self.assertEqual(len(result["subtasks"]), 2)

        # Verify memory storage
        memory_result = self.analyst.retrieve_memory("test_analysis", memory_type="short")
        self.assertIsNotNone(memory_result)

    @patch("litellm.completion")
    async def test_developer_code_generation(self, mock_completion):
        """Test Developer code generation with memory."""
        # Mock LLM response
        mock_completion.return_value = {
            "choices": [{"message": {"content": "def fibonacci(n):\n    return n"}}],
            "usage": {"total_tokens": 150},
        }

        # Test code generation
        subtask = {"description": "Implement Fibonacci function"}
        result = await self.developer.develop_code(subtask, "python")

        # Verify result
        self.assertIn("code", result)
        self.assertIn("def fibonacci", result["code"])

        # Verify memory storage
        memory_result = self.developer.retrieve_memory("test_code", memory_type="short")
        self.assertIsNotNone(memory_result)

    @patch("litellm.completion")
    async def test_tester_test_generation(self, mock_completion):
        """Test Tester test generation with memory."""
        # Mock LLM response
        mock_completion.return_value = {
            "choices": [{"message": {"content": "def test_fibonacci():\n    assert fibonacci(5) == 5"}}],
            "usage": {"total_tokens": 120},
        }

        # Test test generation
        code_data = {"code": "def fibonacci(n):\n    return n"}
        result = await self.tester.generate_tests(code_data)

        # Verify result
        self.assertIn("tests", result)
        self.assertIn("test_fibonacci", result["tests"])

        # Verify memory storage
        memory_result = self.tester.retrieve_memory("test_tests", memory_type="short")
        self.assertIsNotNone(memory_result)

    @patch("litellm.completion")
    async def test_optimizer_code_optimization(self, mock_completion):
        """Test Optimizer code optimization with memory."""
        # Mock LLM response
        mock_completion.return_value = {
            "choices": [{"message": {"content": "def optimized_fibonacci(n, memo={}):\n    return n"}}],
            "usage": {"total_tokens": 130},
        }

        # Test code optimization
        code_data = {"code": "def fibonacci(n):\n    return n"}
        result = await self.optimizer.optimize_code(code_data)

        # Verify result
        self.assertIn("optimized_code", result)
        self.assertIn("optimized_fibonacci", result["optimized_code"])

        # Verify memory storage
        memory_result = self.optimizer.retrieve_memory("test_optimized", memory_type="short")
        self.assertIsNotNone(memory_result)

    @patch("litellm.completion")
    async def test_researcher_topic_research(self, mock_completion):
        """Test Researcher topic research with memory."""
        # Mock LLM response
        mock_completion.return_value = {
            "choices": [{"message": {"content": '{"summary": "Fibonacci is a sequence..."}'}}],
            "usage": {"total_tokens": 200},
        }

        # Test topic research
        topic = "Fibonacci sequence"
        result = await self.researcher.research_topic(topic)

        # Verify result
        self.assertIn("summary", result)
        self.assertIn("Fibonacci", result["summary"])

        # Verify memory storage
        memory_result = self.researcher.retrieve_memory("test_research", memory_type="short")
        self.assertIsNotNone(memory_result)

    @patch("litellm.completion")
    async def test_workflow_execution(self, mock_completion):
        """Test complete workflow execution with memory."""
        # Mock LLM responses
        mock_completion.return_value = {
            "choices": [{"message": {"content": "Mock response"}}],
            "usage": {"total_tokens": 100},
        }

        # Define a sample task
        sample_task = {
            "id": "test_task_001",
            "description": "Test workflow execution",
            "requirements": ["Test requirement 1", "Test requirement 2"],
        }

        # Set initial state
        self.workflow.set_initial_state(sample_task, task_id=sample_task["id"])

        # Execute workflow
        result = await self.workflow.execute_workflow()

        # Verify result
        self.assertIn("status", result)
        self.assertEqual(result["status"], "completed")
        self.assertIn("results", result)

        # Verify memory storage
        task_history = self.workflow.get_task_history(sample_task["id"])
        self.assertGreater(len(task_history), 0, "Task history should not be empty")

        # Verify memory recovery
        recovery_result = self.workflow.recover_task(sample_task["id"])
        self.assertTrue(recovery_result, "Task recovery should be successful")

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
        agent_no_memory = Analyst()

        # Test memory operations without memory manager
        store_result = agent_no_memory.store_memory("test_key", "test_value")
        self.assertFalse(store_result, "Memory operations should fail without memory manager")

        retrieve_result = agent_no_memory.retrieve_memory("test_key")
        self.assertIsNone(retrieve_result, "Memory retrieval should return None without memory manager")

    async def test_error_handling(self):
        """Test error handling in agents."""
        # Test with invalid input
        with self.assertRaises(Exception):
            await self.analyst.analyze_task(None)

        with self.assertRaises(Exception):
            await self.developer.develop_code(None, "python")

if __name__ == "__main__":
    unittest.main()





