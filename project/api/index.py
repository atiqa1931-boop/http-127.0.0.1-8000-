import sys
import os

# Add root directory to sys.path to allow backend imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.main import app

# Vercel needs the FastAPI instance to be exported as 'app'
# This is usually done automatically by the vercel-python runtime
# when it points to this file.
