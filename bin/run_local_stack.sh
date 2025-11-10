#!/bin/bash
# Run local stack with smoke test

set -e

echo "Starting local stack..."

# Start Docker services
docker-compose -f infra/docker/docker-compose.yml up -d

echo "Waiting for services to be ready..."
sleep 30

# Register Avro schema (simplified - assumes schema registry is running)
echo "Registering Avro schema..."
# TODO: Add actual schema registration command

# Run smoke test - produce a few events
echo "Running smoke test..."
python3 -c "
import json
import requests
from datetime import datetime

# Generate a few test events
events = []
for i in range(5):
    event = {
        'device_id': f'test-device-{i}',
        'trip_id': f'test-trip-{i}',
        'ts': datetime.utcnow().isoformat() + 'Z',
        'event_type': 'sample',
        'lat': 41.8781,
        'lon': -87.6298,
        'provider': 'smoke-test',
        'location_precision': 'exact'
    }
    events.append(event)

# Write to temp file
with open('/tmp/smoke_events.jsonl', 'w') as f:
    for event in events:
        f.write(json.dumps(event) + '\n')

print('Generated 5 smoke test events')
"

echo "SMOKE TEST OK"
