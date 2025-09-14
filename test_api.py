

#!/usr/bin/env python3
"""
Test the API server.
"""

import uvicorn
from api_server import app

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")

