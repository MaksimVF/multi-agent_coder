


import asyncio
from role_coordinator_optimized import RoleCoordinator

async def test_new_roles():
    """Test the new QA roles structure"""
    print("Testing new QA roles structure...")

    # Create coordinator with standard workflow
    coordinator = RoleCoordinator(use_unified_roles=False)

    # Initial context
    initial_context = {
        "project_name": "Test Project",
        "requirements": "Create a simple web API with FastAPI"
    }

    # Run workflow
    result = await coordinator.run_workflow(initial_context)

    print("\nWorkflow completed!")
    print(f"Final context keys: {list(result.keys())}")

    # Check if QA results are present
    if "test_report" in result:
        print("\nTest Report:")
        print(result["test_report"]["summary"])
    if "vulnerability_report" in result:
        print("\nVulnerability Report:")
        print(result["vulnerability_report"])

    return result

if __name__ == "__main__":
    asyncio.run(test_new_roles())

