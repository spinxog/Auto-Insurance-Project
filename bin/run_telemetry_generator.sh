#!/bin/bash
# Run telemetry generator for POC

cd "$(dirname "$0")/.."
python src/ingestion/telemetry_generator.py
