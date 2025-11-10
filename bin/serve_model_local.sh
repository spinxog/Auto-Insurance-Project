#!/bin/bash
# Serve model locally

set -e

echo "Starting model server..."

# Activate virtual environment
source venv/bin/activate

# Start model server
uvicorn src.serving.risk_scorer:app --host 0.0.0.0 --port 8000 --reload

echo "Model server started!"
