#!/bin/bash
# Run all tests

set -e

echo "Running unit tests..."
python -m pytest tests/unit/ -v

echo "Running integration tests..."
python -m pytest tests/integration/ -v

echo "Running schema validation tests..."
python scripts/check_schema.py

echo "All tests completed successfully!"
