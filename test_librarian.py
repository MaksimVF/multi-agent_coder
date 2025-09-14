

import asyncio
from roles.librarian import LibrarianAgent
from memory_manager import MemoryManager

async def test_librarian():
    """Test Librarian Agent functionality"""
    print("📚 Testing Librarian Agent...")

    # Create a mock memory manager
    class MockMemoryManager:
        def __init__(self):
            self.redis_client = MockRedis()
            self.weaviate_client = MockWeaviate()

        def retrieve_long_term(self, query, limit=5, agent=None, task_id=None):
            # Mock response
            return [
                {
                    "content": "Fibonacci sequence is a series where each number is the sum of the two preceding ones.",
                    "metadata": {"type": "algorithm", "source": "wikipedia"},
                    "timestamp": "2025-09-14T12:00:00",
                    "agent": "researcher",
                    "task_id": "task_001",
                    "importance": 0.8
                },
                {
                    "content": "Memoization is an optimization technique used to speed up function calls by storing results of expensive function calls.",
                    "metadata": {"type": "optimization", "source": "geeksforgeeks"},
                    "timestamp": "2025-09-13T15:30:00",
                    "agent": "researcher",
                    "task_id": "task_002",
                    "importance": 0.7
                }
            ]

        def store_long_term(self, content, metadata=None, agent="unknown", task_id="unknown", importance=0.5):
            # Mock storage - just return a fake ID
            return "mock_id_123"

        def retrieve_short_term(self, key):
            # Mock response
            if key == "task_001:researcher:knowledge":
                return {
                    "value": "Python best practices for Fibonacci implementation",
                    "timestamp": "2025-09-14T14:00:00",
                    "metadata": {"type": "best_practice"}
                }
            return None

    class MockRedis:
        def keys(self, pattern):
            return ["task_001:researcher:knowledge"]

    class MockWeaviate:
        pass

    # Create librarian with mock memory manager
    librarian = LibrarianAgent(memory_manager=MockMemoryManager())

    # Test search functionality
    print("\n🔍 Testing search functionality...")
    search_results = await librarian.search_knowledge(
        query="Fibonacci sequence algorithms with memoization",
        task_id="task_001",
        agent="researcher"
    )

    print(f"Found {len(search_results)} results:")
    for i, result in enumerate(search_results):
        print(f"{i+1}. Relevance: {result['relevance']:.2f}")
        print(f"   Content: {result['content'][:50]}...")

    # Test context analysis
    print("\n🧠 Testing context analysis...")
    context_analysis = await librarian.analyze_context({
        "microagent_knowledge": [
            {
                "name": "python_microagent",
                "trigger": "Fibonacci",
                "content": "Fibonacci sequence is a series where each number is the sum of the two preceding ones."
            }
        ],
        "repo_instructions": [
            {
                "name": "coding_standards",
                "content": "All code must follow PEP 8 standards and include type hints."
            }
        ]
    })

    print(f"Generated {len(context_analysis['insights'])} insights:")
    for insight in context_analysis['insights']:
        print(f"- {insight['type']}: {insight['analysis'][:50]}...")

    # Test knowledge storage
    print("\n💾 Testing knowledge storage...")
    storage_result = await librarian.store_knowledge(
        content="New knowledge about Fibonacci optimization",
        metadata={"type": "optimization", "source": "research"},
        task_id="task_003",
        agent="librarian",
        importance=0.9
    )
    print(f"Knowledge stored successfully: {storage_result}")

    print("\n✅ All tests completed successfully!")

if __name__ == "__main__":
    asyncio.run(test_librarian())

