#!/bin/bash
# Master script to run local development environment

set -e

echo "Starting local telematics pipeline..."

# Ensure we're in the project root
cd "$(dirname "$0")/.."

# Activate virtual environment
source venv/bin/activate

# Start Docker services
echo "Starting Docker services..."
cd infra/docker
docker-compose up -d

# Wait for services to be ready
echo "Waiting for services to start..."
sleep 30

# Seed data
echo "Seeding data..."
cd ../..
./bin/seed_data

# Train model
echo "Training model..."
./bin/train_local.sh

# Serve model
echo "Starting model server..."
./bin/serve_model_local.sh &

echo "Local environment ready!"
echo "Access points:"
echo "- Control Plane: http://localhost:8080"
echo "- Model Server: http://localhost:8000"
echo "- Kafka: localhost:9094"
echo "- Schema Registry: http://localhost:8081"
echo "- MinIO: http://localhost:9001"
