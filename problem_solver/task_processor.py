


"""
Task Processor for Problem Solver

This module handles the processing of individual tasks within a problem-solving workflow.
"""

import os
import asyncio
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

from agent_registry import AgentRegistry
from memory_manager import MemoryManager

@dataclass
class Task:
    """Represents a task to be processed"""
    task_id: str
    task_type: str
    description: str
    input_data: Optional[Dict[str, Any]] = None
    dependencies: Optional[List[str]] = None

class TaskProcessor:
    """Processes individual tasks using agents"""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.agent_registry = AgentRegistry()
        self.memory_manager = MemoryManager()
        self.task_queue = asyncio.Queue()

    async def process_task(self, task: Task) -> Dict[str, Any]:
        """Process a single task"""
        result = {
            'task_id': task.task_id,
            'success': False,
            'output': None,
            'error': None,
            'agent_used': None
        }

        try:
            # Select appropriate agent
            agent_name = self._select_agent_for_task(task)
            agent = self.agent_registry.get_agent(agent_name)

            # Prepare input for agent
            agent_input = {
                'task': task.description,
                'input_data': task.input_data or {},
                'task_type': task.task_type
            }

            # Execute agent
            agent_result = await agent.execute(agent_input)

            # Process agent output
            result.update({
                'success': True,
                'output': agent_result,
                'agent_used': agent_name
            })

        except Exception as e:
            result.update({
                'success': False,
                'error': str(e)
            })

        return result

    async def process_task_queue(self) -> List[Dict[str, Any]]:
        """Process a queue of tasks"""
        results = []

        while not self.task_queue.empty():
            task = await self.task_queue.get()
            result = await self.process_task(task)
            results.append(result)
            self.task_queue.task_done()

        return results

    def add_task_to_queue(self, task: Task) -> None:
        """Add a task to the processing queue"""
        self.task_queue.put_nowait(task)

    def _select_agent_for_task(self, task: Task) -> str:
        """Select the appropriate agent for a task"""
        # Map task types to agents
        task_to_agent = {
            'analyze': 'analyst',
            'design': 'analyst',
            'implement': 'developer',
            'test': 'tester',
            'debug': 'debugger',
            'optimize': 'optimizer',
            'review': 'analyst',
            'document': 'developer'
        }

        # Get agent based on task type or default to analyst
        return task_to_agent.get(task.task_type.lower(), 'analyst')

    def create_subtasks(self, task_description: str) -> List[Task]:
        """Create subtasks from a task description"""
        # Simple implementation - should be enhanced with AI-based task decomposition
        subtasks = []

        # Example: For a coding task, create analyze, implement, test subtasks
        if 'code' in task_description.lower() or 'implement' in task_description.lower():
            base_task_id = f"task_{len(subtasks)}"

            subtasks.append(Task(
                task_id=f"{base_task_id}_analyze",
                task_type="analyze",
                description=f"Analyze requirements for: {task_description}"
            ))

            subtasks.append(Task(
                task_id=f"{base_task_id}_implement",
                task_type="implement",
                description=f"Implement solution for: {task_description}",
                dependencies=[f"{base_task_id}_analyze"]
            ))

            subtasks.append(Task(
                task_id=f"{base_task_id}_test",
                task_type="test",
                description=f"Test implementation for: {task_description}",
                dependencies=[f"{base_task_id}_implement"]
            ))

        else:
            # Default single task
            subtasks.append(Task(
                task_id=f"task_{len(subtasks)}",
                task_type=task.task_type,
                description=task_description
            ))

        return subtasks


