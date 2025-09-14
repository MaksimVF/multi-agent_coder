


#!/usr/bin/env python3
"""
Test import.
"""

import sys
sys.path.insert(0, '.')

try:
    from roles.git_integrator import GitIntegrator
    print('Import successful')
except Exception as e:
    print(f'Import failed: {e}')


