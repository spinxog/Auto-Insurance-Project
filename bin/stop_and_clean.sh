#!/bin/bash
# Stop Docker services and clean up volumes/data

set -e

echo "Stopping Docker services..."
docker-compose -f infra/docker/docker-compose.yml down

echo "Removing Docker volumes..."
docker volume prune -f

echo "Cleaning local data directories..."
rm -rf data/tmp/*
rm -rf data/logs/*

echo "Cleanup complete."
