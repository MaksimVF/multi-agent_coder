
"""Security module for multi-agent coder."""

from enum import Enum

class SecurityRisk(int, Enum):
    """Security risk levels for actions."""
    UNKNOWN = -1
    LOW = 0
    MEDIUM = 1
    HIGH = 2

class SecurityAnalyzer:
    """Base class for security analyzers."""

    async def analyze_action(self, action):
        """Analyze an action for security risks.

        Args:
            action: The action to analyze

        Returns:
            SecurityRisk: The security risk level
        """
        raise NotImplementedError("Subclasses must implement this method")

class BasicSecurityAnalyzer(SecurityAnalyzer):
    """Basic security analyzer that checks for common security issues."""

    async def analyze_action(self, action):
        """Analyze an action for basic security risks."""
        # Default to UNKNOWN risk
        risk = SecurityRisk.UNKNOWN

        # Check if the action has specific security attributes
        if hasattr(action, 'command'):
            # For command actions, check for dangerous commands
            command = getattr(action, 'command', '')
            if self._is_dangerous_command(command):
                risk = SecurityRisk.HIGH
            elif self._is_potentially_unsafe_command(command):
                risk = SecurityRisk.MEDIUM
            else:
                risk = SecurityRisk.LOW

        elif hasattr(action, 'code'):
            # For code execution actions, check for dangerous patterns
            code = getattr(action, 'code', '')
            if self._is_dangerous_code(code):
                risk = SecurityRisk.HIGH
            elif self._is_potentially_unsafe_code(code):
                risk = SecurityRisk.MEDIUM
            else:
                risk = SecurityRisk.LOW

        elif hasattr(action, 'path'):
            # For file actions, check for sensitive paths
            path = getattr(action, 'path', '')
            if self._is_sensitive_path(path):
                risk = SecurityRisk.MEDIUM
            else:
                risk = SecurityRisk.LOW

        return risk

    def _is_dangerous_command(self, command):
        """Check if a command is dangerous."""
        dangerous_patterns = [
            'rm -rf',
            'dd if=',
            'mkfs',
            'fdisk',
            'format',
            'chown',
            'chmod 777',
            'wget | sh',
            'curl | sh',
            'sudo '
        ]

        for pattern in dangerous_patterns:
            if pattern in command.lower():
                return True
        return False

    def _is_potentially_unsafe_command(self, command):
        """Check if a command is potentially unsafe."""
        unsafe_patterns = [
            'rm ',
            'mv ',
            'cp ',
            'chmod ',
            'kill',
            'pkill',
            'apt-get',
            'yum',
            'pip install',
            'npm install'
        ]

        for pattern in unsafe_patterns:
            if pattern in command.lower():
                return True
        return False

    def _is_dangerous_code(self, code):
        """Check if code contains dangerous patterns."""
        dangerous_patterns = [
            'os.system(',
            'os.popen(',
            'subprocess.run(',
            'subprocess.Popen(',
            'eval(',
            'exec(',
            '__import__(',
            'pickle.loads(',
            'yaml.load('
        ]

        for pattern in dangerous_patterns:
            if pattern in code:
                return True
        return False

    def _is_potentially_unsafe_code(self, code):
        """Check if code contains potentially unsafe patterns."""
        unsafe_patterns = [
            'open(',
            'file.write(',
            'requests.get(',
            'requests.post(',
            'socket.',
            'http.',
            'ftp.',
            'telnet.'
        ]

        for pattern in unsafe_patterns:
            if pattern in code:
                return True
        return False

    def _is_sensitive_path(self, path):
        """Check if a path is sensitive."""
        sensitive_paths = [
            '/etc',
            '/root',
            '/home',
            '/var',
            '/usr',
            '/bin',
            '/sbin',
            '/lib',
            '/proc',
            '/sys',
            '/dev',
            '/tmp'
        ]

        for sensitive in sensitive_paths:
            if path.startswith(sensitive):
                return True
        return False
