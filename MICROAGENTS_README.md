


# Microagent System for Multi-Agent Coder

## Overview

The microagent system provides domain-specific knowledge and repository instructions to enhance the capabilities of LLM-powered agents. This system is inspired by OpenHands' microagent architecture and provides contextual knowledge that can be triggered based on keywords in user requests or agent messages.

## Features

- **Domain-specific knowledge**: Microagents provide specialized knowledge for different domains (GitHub, security, Python, etc.)
- **Repository instructions**: Microagents can provide repository-specific guidelines and configurations
- **Trigger-based activation**: Microagents activate when their trigger keywords are detected in queries
- **Contextual enhancement**: Agents can use microagent knowledge to enhance their responses
- **Extensible architecture**: Easy to add new microagents for additional domains

## Microagent Types

### 1. Knowledge Microagents

Knowledge microagents provide domain-specific information and best practices. Examples:

- **GitHub**: GitHub API usage, pull request guidelines, repository management
- **Security**: Secure coding practices, authentication methods, vulnerability prevention
- **Python**: Python development best practices, framework recommendations, coding patterns

### 2. Repo Microagents

Repo microagents provide repository-specific instructions and configurations. Examples:

- **Project-specific guidelines**: Coding standards, testing requirements, deployment procedures
- **Tool configurations**: Linter settings, CI/CD pipeline configurations, environment setup

## Microagent Format

Microagents are defined in Markdown files with YAML metadata. Example structure:

```markdown
---
name: github
type: knowledge
version: 1.0.0
agent: DeveloperAgent
triggers:
- github
- git
- pull request
- pr
- repository
- repo
---
# GitHub Microagent Content

You have access to an environment variable, `GITHUB_TOKEN`, which allows you to interact with
the GitHub API.

<IMPORTANT>
You can use `curl` with the `GITHUB_TOKEN` to interact with GitHub's API.
ALWAYS use the GitHub API for operations instead of a web browser.
</IMPORTANT>
```

## Implementation

### Microagent Loading

Microagents are loaded from two locations:

1. **Global microagents**: `/workspace/multi-agent_coder/microagents/`
2. **User microagents**: `~/.multi_agent_coder/microagents/`

### Integration with Agents

Agents can access microagent knowledge through the `MemoryManager`:

```python
# Get microagent knowledge for a specific query
knowledge = memory_manager.find_microagent_knowledge("Create a GitHub pull request")

# Get repository instructions
repo_instructions = memory_manager.get_repo_instructions()

# Get contextual knowledge (both microagent knowledge and repo instructions)
contextual_knowledge = memory_manager.recall_contextual_knowledge("Secure Python web application")
```

### Enhanced LLM Responses

The `BaseLLMAgent` class has been enhanced to use microagent knowledge:

```python
# Generate response with contextual knowledge
response = await agent.generate_response_with_knowledge(
    "How do I implement secure authentication in Python?",
    system_message="You are a security expert."
)
```

## Creating Custom Microagents

To create a custom microagent:

1. Create a Markdown file in the `microagents/` directory
2. Add YAML metadata with name, type, version, agent, and triggers
3. Add the microagent content in Markdown format
4. The microagent will be automatically loaded and available to agents

## Benefits

1. **Improved Context**: Agents have access to relevant domain knowledge
2. **Consistency**: Standardized guidelines and best practices
3. **Extensibility**: Easy to add new knowledge domains
4. **Efficiency**: Agents can leverage pre-defined knowledge instead of generating it
5. **Security**: Built-in security guidelines and best practices

## Future Enhancements

- **Dynamic microagent loading**: Load microagents from remote repositories
- **Microagent versioning**: Support for versioned microagents
- **Collaborative microagents**: Microagents that can perform actions, not just provide knowledge
- **AI-generated microagents**: Automatically generate microagents from documentation

## Testing

Run the demo script to test the microagent system:

```bash
python demo_microagents.py
```

This will demonstrate microagent knowledge retrieval and usage in LLM responses.

