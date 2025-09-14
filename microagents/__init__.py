


"""
Microagents module for Multi-Agent Coder.

This module provides microagent functionality inspired by OpenHands,
including knowledge microagents and repo microagents.
"""

import os
from typing import Dict, List, Optional, Tuple, Union
from pathlib import Path
import yaml
import markdown

class Microagent:
    """Base class for microagents."""

    def __init__(self, name: str, type: str, version: str, agent: str, triggers: List[str], content: str):
        self.name = name
        self.type = type
        self.version = version
        self.agent = agent
        self.triggers = triggers
        self.content = content

    def match_trigger(self, query: str) -> Optional[str]:
        """Check if any trigger matches the query."""
        query_lower = query.lower()
        for trigger in self.triggers:
            if trigger.lower() in query_lower:
                return trigger
        return None

    @classmethod
    def from_file(cls, file_path: str) -> Optional['Microagent']:
        """Load a microagent from a markdown file."""
        try:
            with open(file_path, 'r') as f:
                content = f.read()

            # Extract metadata and content
            metadata, markdown_content = content.split('---', 2)[1:3]
            metadata = yaml.safe_load(metadata)

            # Create the appropriate microagent type
            if metadata['type'] == 'repo':
                return RepoMicroagent(
                    name=metadata['name'],
                    type=metadata['type'],
                    version=metadata['version'],
                    agent=metadata['agent'],
                    triggers=metadata['triggers'],
                    content=markdown_content
                )
            else:
                return KnowledgeMicroagent(
                    name=metadata['name'],
                    type=metadata['type'],
                    version=metadata['version'],
                    agent=metadata['agent'],
                    triggers=metadata['triggers'],
                    content=markdown_content
                )
        except Exception as e:
            print(f"Error loading microagent from {file_path}: {e}")
            return None

class RepoMicroagent(Microagent):
    """Microagent that provides repository-specific instructions."""

    def __init__(self, name: str, type: str, version: str, agent: str, triggers: List[str], content: str):
        super().__init__(name, type, version, agent, triggers, content)

class KnowledgeMicroagent(Microagent):
    """Microagent that provides domain-specific knowledge."""

    def __init__(self, name: str, type: str, version: str, agent: str, triggers: List[str], content: str):
        super().__init__(name, type, version, agent, triggers, content)

def load_microagent_from_file(file_path: str) -> Optional[Union[RepoMicroagent, KnowledgeMicroagent]]:
    """Load a microagent from a markdown file."""
    try:
        with open(file_path, 'r') as f:
            content = f.read()

        # Extract metadata and content
        metadata, markdown_content = content.split('---', 2)[1:3]
        metadata = yaml.safe_load(metadata)

        # Create the appropriate microagent type
        if metadata['type'] == 'repo':
            return RepoMicroagent(
                name=metadata['name'],
                type=metadata['type'],
                version=metadata['version'],
                agent=metadata['agent'],
                triggers=metadata['triggers'],
                content=markdown_content
            )
        else:
            return KnowledgeMicroagent(
                name=metadata['name'],
                type=metadata['type'],
                version=metadata['version'],
                agent=metadata['agent'],
                triggers=metadata['triggers'],
                content=markdown_content
            )
    except Exception as e:
        print(f"Error loading microagent from {file_path}: {e}")
        return None

def load_microagents_from_dir(directory: str) -> Tuple[Dict[str, RepoMicroagent], Dict[str, KnowledgeMicroagent]]:
    """Load all microagents from a directory."""
    repo_agents = {}
    knowledge_agents = {}

    if not os.path.exists(directory):
        return repo_agents, knowledge_agents

    for filename in os.listdir(directory):
        if filename.endswith('.md'):
            file_path = os.path.join(directory, filename)
            microagent = load_microagent_from_file(file_path)

            if microagent:
                if isinstance(microagent, RepoMicroagent):
                    repo_agents[microagent.name] = microagent
                elif isinstance(microagent, KnowledgeMicroagent):
                    knowledge_agents[microagent.name] = microagent

    return repo_agents, knowledge_agents

# Global microagents directory
GLOBAL_MICROAGENTS_DIR = os.path.dirname(__file__)
USER_MICROAGENTS_DIR = os.path.expanduser('~/.multi_agent_coder/microagents')

# Load global microagents
repo_microagents = {}
knowledge_microagents = {}

if os.path.exists(GLOBAL_MICROAGENTS_DIR):
    repo_microagents, knowledge_microagents = load_microagents_from_dir(GLOBAL_MICROAGENTS_DIR)

# Export loaded microagents
__all__ = [
    'Microagent',
    'RepoMicroagent',
    'KnowledgeMicroagent',
    'load_microagent_from_file',
    'load_microagents_from_dir',
    'GLOBAL_MICROAGENTS_DIR',
    'USER_MICROAGENTS_DIR',
    'repo_microagents',
    'knowledge_microagents',
]


