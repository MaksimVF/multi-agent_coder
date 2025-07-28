


class Analyst:
    def analyze_task(self, task_description):
        """Analyze a task and break it into subtasks."""
        print(f"Analyzing task: {task_description}")

        # Enhanced analysis with more sophisticated task breakdown
        task_lower = task_description.lower()

        # Check for specific task types
        if any(keyword in task_lower for keyword in ["function", "method", "procedure", "routine"]):
            subtasks = self._analyze_function_task(task_lower)
        elif any(keyword in task_lower for keyword in ["class", "object", "structure", "component"]):
            subtasks = self._analyze_class_task(task_lower)
        elif any(keyword in task_lower for keyword in ["algorithm", "logic", "process", "workflow"]):
            subtasks = self._analyze_algorithm_task(task_lower)
        elif any(keyword in task_lower for keyword in ["api", "interface", "service", "endpoint"]):
            subtasks = self._analyze_api_task(task_lower)
        else:
            subtasks = self._analyze_generic_task(task_lower)

        print(f"Identified {len(subtasks)} subtasks:")
        for subtask in subtasks:
            print(f"  - {subtask['description']}")

        return subtasks

    def _analyze_function_task(self, task_description):
        """Analyze a function-related task."""
        subtasks = [
            {"id": 1, "description": "Define function signature and parameters"},
            {"id": 2, "description": "Implement core function logic"},
            {"id": 3, "description": "Add input validation and error handling"},
            {"id": 4, "description": "Write comprehensive docstring with examples"},
            {"id": 5, "description": "Add type hints and annotations"}
        ]

        # Add specific subtasks based on function type
        if "math" in task_description or "calculate" in task_description:
            subtasks.insert(2, {"id": 2.5, "description": "Implement mathematical formula"})
        elif "file" in task_description or "io" in task_description:
            subtasks.insert(2, {"id": 2.5, "description": "Handle file operations safely"})
        elif "network" in task_description or "api" in task_description:
            subtasks.insert(2, {"id": 2.5, "description": "Implement network communication"})

        return subtasks

    def _analyze_class_task(self, task_description):
        """Analyze a class-related task."""
        subtasks = [
            {"id": 1, "description": "Define class structure and inheritance"},
            {"id": 2, "description": "Implement core methods"},
            {"id": 3, "description": "Add properties with getters/setters"},
            {"id": 4, "description": "Implement __init__ and __str__ methods"},
            {"id": 5, "description": "Write class-level docstring"},
            {"id": 6, "description": "Add type hints and annotations"}
        ]

        # Add specific subtasks based on class type
        if "database" in task_description or "model" in task_description:
            subtasks.insert(2, {"id": 2.5, "description": "Implement database integration"})
        elif "ui" in task_description or "interface" in task_description:
            subtasks.insert(2, {"id": 2.5, "description": "Design user interface elements"})
        elif "manager" in task_description or "controller" in task_description:
            subtasks.insert(2, {"id": 2.5, "description": "Implement control logic"})

        return subtasks

    def _analyze_algorithm_task(self, task_description):
        """Analyze an algorithm-related task."""
        return [
            {"id": 1, "description": "Define algorithm requirements"},
            {"id": 2, "description": "Design algorithm structure"},
            {"id": 3, "description": "Implement core algorithm logic"},
            {"id": 4, "description": "Add edge case handling"},
            {"id": 5, "description": "Optimize algorithm performance"},
            {"id": 6, "description": "Write algorithm documentation"}
        ]

    def _analyze_api_task(self, task_description):
        """Analyze an API-related task."""
        return [
            {"id": 1, "description": "Define API endpoints"},
            {"id": 2, "description": "Design request/response format"},
            {"id": 3, "description": "Implement API handlers"},
            {"id": 4, "description": "Add authentication/authorization"},
            {"id": 5, "description": "Implement error handling"},
            {"id": 6, "description": "Write API documentation"}
        ]

    def _analyze_generic_task(self, task_description):
        """Analyze a generic task."""
        return [
            {"id": 1, "description": "Understand requirements"},
            {"id": 2, "description": "Design solution architecture"},
            {"id": 3, "description": "Implement core functionality"},
            {"id": 4, "description": "Add error handling and validation"},
            {"id": 5, "description": "Write documentation and comments"},
            {"id": 6, "description": "Test and debug solution"}
        ]



