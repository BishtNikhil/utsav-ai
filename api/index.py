"""
Vercel Serverless Function entry point for UtsavAI.

Exposes the FastAPI ASGI app instance for Vercel's Python runtime.
Ensures root repository path is included in sys.path.
"""

import sys
import os

# Resolve the project root directory
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from app.main import app

# Vercel ASGI expects an 'app' callable
__all__ = ["app"]
