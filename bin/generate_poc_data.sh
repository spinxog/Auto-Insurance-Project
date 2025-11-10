#!/bin/bash
# Deterministic POC data generator

set -e

SEED=42
COUNT=500

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --seed)
            SEED="$2"
            shift 2
            ;;
        --count)
            COUNT="$2"
            shift 2
            ;;
        *)
            echo "Usage: $0 [--seed N] [--count N]"
            exit 1
            ;;
    esac
done

echo "Generating $COUNT POC telemetry events with seed $SEED"

# Use Python to generate deterministic data
python3 -c "
import json
import random
import uuid
from datetime import datetime, timedelta

random.seed($SEED)

events = []
base_ts = datetime.utcnow()

for i in range($COUNT):
    ts = base_ts + timedelta(seconds=i*10)  # 10 second intervals
    event = {
        'device_id': str(uuid.UUID(int=random.getrandbits(128))),
        'policy_id': str(uuid.UUID(int=random.getrandbits(128))) if random.random() > 0.1 else None,
        'trip_id': str(uuid.UUID(int=random.getrandbits(128))),
        'ts': ts.isoformat() + 'Z',
        'event_type': random.choice(['heartbeat', 'sample', 'start_trip', 'end_trip', 'alert']),
        'lat': 41.8781 + random.uniform(-0.1, 0.1),
        'lon': -87.6298 + random.uniform(-0.1, 0.1),
        'gps_accuracy_m': random.uniform(1, 20),
        'speed_kmh': random.uniform(0, 120),
        'accel_x_m_s2': random.uniform(-3, 3),
        'accel_y_m_s2': random.uniform(-5, 5),
        'accel_z_m_s2': random.uniform(-2, 2),
        'brake_strength': random.uniform(0, 1) if random.random() > 0.7 else None,
        'steering_angle_deg': random.uniform(-180, 180),
        'heading_deg': random.uniform(0, 360),
        'odometer_km': 10000 + i * 0.1,
        'engine_rpm': random.randint(800, 6000) if random.random() > 0.3 else None,
        'battery_level_pct': random.uniform(10, 100),
        'sample_rate_hz': 0.1,
        'provider': 'poc-generator-v1.0',
        'hashed_driver_id': str(uuid.UUID(int=random.getrandbits(128))) if random.random() > 0.2 else None,
        'location_precision': random.choice(['exact', 'coarse', 'aggregated'])
    }
    events.append(event)

with open('data/samples/poc_telemetry.jsonl', 'w') as f:
    for event in events:
        f.write(json.dumps(event) + '\n')

print(f'Generated {len(events)} events')
"

echo "POC data generated successfully"
