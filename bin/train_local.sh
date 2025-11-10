#!/bin/bash
# Train model locally

set -e

echo "Training baseline model..."

# Activate virtual environment
source venv/bin/activate

# Train model
python src/models/train_baseline.py

echo "Model training complete!"
