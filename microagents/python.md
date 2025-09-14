

---
name: python
type: knowledge
version: 1.0.0
agent: DeveloperAgent
triggers:
- python
- pip
- virtualenv
- requirements
- pytest
- unittest
- flask
- django
- fastapi
---

## Python Development Best Practices

### Virtual Environments
Always use virtual environments to isolate dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Dependency Management
- Use `requirements.txt` for simple projects
- Use `pipenv` or `poetry` for complex dependency management
- Pin exact versions in production

### Testing
- Use `pytest` for unit testing
- Use `unittest.mock` for mocking dependencies
- Aim for high test coverage (80%+)
- Write integration tests for critical paths

### Code Quality
- Follow PEP 8 style guide
- Use type hints for function signatures
- Use linters (flake8, pylint) and formatters (black)
- Write docstrings for modules, classes, and functions

### Web Frameworks
- **Flask**: Lightweight, good for small APIs
- **Django**: Full-featured, includes ORM and admin
- **FastAPI**: Modern, high-performance, async support

### Common Python Patterns
```python
# Context managers for resource management
with open('file.txt') as f:
    data = f.read()

# List comprehensions
squares = [x**2 for x in range(10)]

# Generators for memory efficiency
def read_large_file(file_path):
    with open(file_path) as f:
        for line in f:
            yield line.strip()
```

### Performance Tips
- Use built-in functions and libraries when possible
- Avoid global variables in performance-critical code
- Use `str.format()` or f-strings instead of concatenation
- Profile with `cProfile` or `line_profiler`


