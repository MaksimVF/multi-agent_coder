

"""
Demo script to test the microagent system integration.
"""

import asyncio
from memory_manager import MemoryManager
from base_llm_agent import BaseLLMAgent

async def test_microagent_knowledge():
    """Test microagent knowledge retrieval and usage."""
    print("=== Testing Microagent System ===")

    # Create memory manager (this will load microagents)
    memory_manager = MemoryManager()

    # Debug: Check if microagents are loaded
    print(f"Loaded {len(memory_manager.knowledge_microagents)} knowledge microagents")
    print(f"Loaded {len(memory_manager.repo_microagents)} repo microagents")
    print(f"Knowledge microagents: {list(memory_manager.knowledge_microagents.keys())}")
    print(f"Repo microagents: {list(memory_manager.repo_microagents.keys())}")

    # Create LLM agent with memory manager
    agent = BaseLLMAgent(memory_manager=memory_manager)

    # Test 1: Get microagent knowledge for GitHub-related task
    print("\n1. Testing GitHub microagent knowledge:")
    github_knowledge = agent.get_microagent_knowledge("Create a pull request on GitHub")
    print(f"Found {len(github_knowledge)} knowledge entries:")
    for k in github_knowledge:
        print(f"  - {k['name']} (triggered by '{k['trigger']}'): {len(k['content'].split())} words")

    # Test 2: Get microagent knowledge for security-related task
    print("\n2. Testing security microagent knowledge:")
    security_knowledge = agent.get_microagent_knowledge("Implement secure authentication")
    print(f"Found {len(security_knowledge)} knowledge entries:")
    for k in security_knowledge:
        print(f"  - {k['name']} (triggered by '{k['trigger']}'): {len(k['content'].split())} words")

    # Test 3: Get microagent knowledge for Python-related task
    print("\n3. Testing Python microagent knowledge:")
    python_knowledge = agent.get_microagent_knowledge("Write a Python Flask application")
    print(f"Found {len(python_knowledge)} knowledge entries:")
    for k in python_knowledge:
        print(f"  - {k['name']} (triggered by '{k['trigger']}'): {len(k['content'].split())} words")

    # Test 4: Get repo instructions
    print("\n4. Testing repository instructions:")
    repo_instructions = agent.get_repo_instructions()
    print(f"Found {len(repo_instructions)} repo instruction entries:")
    for r in repo_instructions:
        print(f"  - {r['name']}: {len(r['content'].split())} words")

    # Test 5: Generate response with knowledge
    print("\n5. Testing LLM response with contextual knowledge:")
    test_prompt = "How do I create a secure GitHub pull request in Python?"
    response = await agent.generate_response_with_knowledge(test_prompt)
    print(f"Response (first 100 chars): {response[:100]}...")

    print("\n=== Microagent System Test Completed ===")

async def test_contextual_knowledge():
    """Test contextual knowledge gathering."""
    print("\n=== Testing Contextual Knowledge ===")

    memory_manager = MemoryManager()
    agent = BaseLLMAgent(memory_manager=memory_manager)

    # Test with a complex task description
    task_description = """
    Create a secure Python web application that:
    1. Uses Flask for the web framework
    2. Implements JWT authentication
    3. Stores user data securely
    4. Integrates with GitHub for version control
    5. Includes comprehensive unit tests
    """

    # Get contextual knowledge
    contextual_knowledge = agent.get_contextual_knowledge(task_description)

    print(f"Found {len(contextual_knowledge['microagent_knowledge'])} knowledge entries")
    print(f"Found {len(contextual_knowledge['repo_instructions'])} repo instruction entries")

    # Show which microagents were triggered
    triggered_agents = [k['name'] for k in contextual_knowledge['microagent_knowledge']]
    print(f"Triggered microagents: {triggered_agents}")

    print("=== Contextual Knowledge Test Completed ===")

if __name__ == "__main__":
    asyncio.run(test_microagent_knowledge())
    asyncio.run(test_contextual_knowledge())

