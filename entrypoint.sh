

#!/bin/bash
# Secure entrypoint for code execution sandbox

# Set resource limits
ulimit -t 30        # CPU time limit: 30 seconds
ulimit -f 10240     # File size limit: 10MB
ulimit -v 1048576   # Virtual memory limit: 1GB
ulimit -m 524288    # Memory limit: 512MB
ulimit -n 1024      # File descriptors limit: 1024

# Set secure environment
export PATH=/home/sandboxuser/.local/bin:$PATH
export TMPDIR=/tmp/sandbox
mkdir -p "$TMPDIR"
chmod 700 "$TMPDIR"

# Disable network access by default
# (This would be handled by Docker network settings in production)
# iptables -P OUTPUT DROP

# Run the provided command
if [ "$#" -eq 0 ]; then
    echo "No command provided. Usage: docker run <image> <command>"
    exit 1
fi

# Execute the command with timeout
timeout 30s "$@"
exit_code=$?

if [ $exit_code -eq 124 ]; then
    echo "ERROR: Command timed out after 30 seconds"
    exit 124
else
    exit $exit_code
fi

