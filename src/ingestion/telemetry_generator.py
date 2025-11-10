"""Telemetry generator for POC simulation."""

import json
import random
import uuid
from datetime import datetime, timedelta, UTC
from typing import List, Dict, Any

def generate_telemetry_events(num_events: int = 100) -> List[Dict[str, Any]]:
    """Generate a list of sample telemetry events.

    Args:
        num_events: Number of events to generate.

    Returns:
        List of telemetry event dictionaries.
    """
    events = []
    device_id = str(uuid.uuid4())
    policy_id = str(uuid.uuid4())
    base_ts = datetime.now(UTC)

    # Generate multiple trips
    num_trips = max(1, num_events // 50)  # At least 1 trip, roughly 50 events per trip
    trip_ids = [str(uuid.uuid4()) for _ in range(num_trips)]

    for i in range(num_events):
        trip_id = trip_ids[i % num_trips]  # Cycle through trip_ids
        ts = base_ts + timedelta(seconds=i)
        event = {
            "device_id": device_id,
            "policy_id": policy_id,
            "trip_id": trip_id,
            "ts": ts.isoformat() + "Z",
            "event_type": random.choice(["heartbeat", "sample", "start_trip", "end_trip", "alert"]),
            "lat": 41.8781 + random.uniform(-0.01, 0.01),
            "lon": -87.6298 + random.uniform(-0.01, 0.01),
            "gps_accuracy_m": random.uniform(1, 10),
            "speed_kmh": random.uniform(0, 120),
            "accel_x_m_s2": random.uniform(-2, 2),
            "accel_y_m_s2": random.uniform(-5, 5),
            "accel_z_m_s2": random.uniform(-1, 1),
            "brake_strength": random.uniform(0, 1) if random.random() > 0.5 else None,
            "steering_angle_deg": random.uniform(-180, 180),
            "heading_deg": random.uniform(0, 360),
            "odometer_km": 12345.6 + i * 0.1,
            "engine_rpm": random.randint(800, 6000) if random.random() > 0.3 else None,
            "battery_level_pct": random.uniform(10, 100),
            "sample_rate_hz": 1.0,
            "provider": "simulator-v1.0",
            "hashed_driver_id": str(uuid.uuid4()) if random.random() > 0.5 else None,
            "location_precision": random.choice(["exact", "coarse", "aggregated"])
        }
        events.append(event)

    return events

if __name__ == "__main__":
    events = generate_telemetry_events(10)
    for event in events:
        print(json.dumps(event))
