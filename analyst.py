

class Analyst:
    def analyze_task(self, task_description):
        """Analyze a task and break it into subtasks."""
        print(f"Analyzing task: {task_description}")

        # Simple analysis - in a real system this would be more sophisticated
        if "function" in task_description.lower():
            subtasks = [
                {"id": 1, "description": "Define function signature"},
                {"id": 2, "description": "Implement function logic"},
                {"id": 3, "description": "Add input validation"},
                {"id": 4, "description": "Write docstring"}
            ]
        elif "class" in task_description.lower():
            subtasks = [
                {"id": 1, "description": "Define class structure"},
                {"id": 2, "description": "Implement methods"},
                {"id": 3, "description": "Add properties"},
                {"id": 4, "description": "Write class docstring"}
            ]
        else:
            subtasks = [
                {"id": 1, "description": "Understand requirements"},
                {"id": 2, "description": "Design solution"},
                {"id": 3, "description": "Implement solution"},
                {"id": 4, "description": "Test solution"}
            ]

        print(f"Identified {len(subtasks)} subtasks:")
        for subtask in subtasks:
            print(f"  - {subtask['description']}")

        return subtasks

