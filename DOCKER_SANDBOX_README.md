

# Docker Sandbox for Secure Code Execution

## Overview

This Docker sandbox provides isolated execution environments for running untrusted code with strict resource limits and security restrictions.

## Features

- **Process isolation**: Each code execution runs in its own container
- **Resource limits**: CPU, memory, and execution time limits
- **Network restrictions**: Network access disabled by default
- **Multi-language support**: Python, JavaScript, Java, and more
- **Automatic cleanup**: Containers are removed after execution

## Setup Instructions

### 1. Install Docker

Follow the official Docker installation guide for your platform:
https://docs.docker.com/get-docker/

### 2. Build the Sandbox Image

```bash
cd /path/to/multi-agent_coder
docker build -t sandbox-python -f Dockerfile.sandbox .
```

### 3. Configure the Tester

The Tester class will automatically use Docker when available. If Docker is not running, it will fallback to subprocess execution.

### 4. Security Configuration

The sandbox includes:

- **Memory limits**: 512MB by default
- **CPU limits**: 1 CPU core by default
- **Timeout**: 30 seconds execution limit
- **Network disabled**: No internet access
- **Non-root user**: Code runs as non-privileged user

## Usage

The Docker sandbox is automatically used by the Tester class when executing code. No additional configuration is needed.

## Customization

To customize the sandbox behavior, modify the Dockerfile.sandbox or entrypoint.sh files:

- **Dockerfile.sandbox**: Define the base environment and dependencies
- **entrypoint.sh**: Set resource limits and security restrictions
- **requirements.txt**: Add Python dependencies for the sandbox

## Security Best Practices

1. **Never run untrusted code without isolation**
2. **Regularly update the base Docker image**
3. **Monitor resource usage and container behavior**
4. **Use additional security tools like AppArmor or SELinux**
5. **Consider using gVisor or Kata Containers for stronger isolation**

## Troubleshooting

- **Docker not available**: The system will fallback to subprocess execution
- **Permission errors**: Ensure your user has access to Docker
- **Resource limits**: Adjust limits in the Tester class configuration

