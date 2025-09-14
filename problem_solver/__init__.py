
"""
Problem Solver Module for Multi-Agent Coder

This module provides automated problem solving capabilities for handling
issues, bugs, and tasks in software development projects.
"""

from .problem_solver import ProblemSolver, ProblemContext
from .issue_handler import IssueHandlerFactory, Issue
from .task_processor import TaskProcessor, Task

__all__ = ["ProblemSolver", "ProblemContext", "IssueHandlerFactory", "Issue", "TaskProcessor", "Task"]
