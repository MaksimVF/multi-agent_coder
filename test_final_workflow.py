




import asyncio
from role_coordinator_final import RoleCoordinator

async def test_final_workflow():
    """Test the final workflow with CriticalEvaluator"""
    print("Testing final workflow with CriticalEvaluator...")

    # Create coordinator with standard workflow (separate roles)
    coordinator = RoleCoordinator(use_unified_roles=False)

    # Initial context
    initial_context = {
        "project_name": "E-commerce Platform",
        "requirements": "Create a scalable e-commerce platform with user authentication, product catalog, and order processing"
    }

    # Run workflow
    result = await coordinator.run_workflow(initial_context)

    print("\nWorkflow completed!")
    print(f"Final context keys: {list(result.keys())}")

    # Check if critical evaluations are present
    if "critical_evaluation" in result:
        print("\n🔍  Critical Evaluation Results:")
        evaluation = result["critical_evaluation"]

        if "architecture_evaluation" in evaluation:
            print(f"\nArchitecture Risk Level: {evaluation['architecture_evaluation']['risk_level']}")
            print(f"Architecture Issues: {evaluation['architecture_evaluation']['evaluation'][:100]}...")

        if "tech_stack_evaluation" in evaluation:
            print(f"\nTech Stack Risk Level: {evaluation['tech_stack_evaluation']['risk_level']}")
            print(f"Tech Stack Issues: {evaluation['tech_stack_evaluation']['evaluation'][:100]}...")

        if "code_evaluation" in evaluation:
            print(f"\nCode Risk Level: {evaluation['code_evaluation']['risk_level']}")
            print(f"Code Issues: {evaluation['code_evaluation']['evaluation'][:100]}...")

        if "alternative_scenarios" in evaluation:
            print(f"\nAlternative Scenarios: {len(evaluation['alternative_scenarios']['scenarios'])} generated")

        if "recommendations" in evaluation:
            print(f"\nRecommendations: {len(evaluation['recommendations']['recommendations'])} provided")

    # Check if QA results are present
    if "test_report" in result:
        print(f"\n✅  Test Results: {result['test_report']['summary']}")

    if "vulnerability_report" in result:
        print(f"\n🛡️  Vulnerabilities: {result['vulnerability_report']}")

    return result

if __name__ == "__main__":
    asyncio.run(test_final_workflow())



