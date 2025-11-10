"""Schema validation utilities for telemetry events."""

import json
import jsonschema
from typing import Dict, Any

# JSON Schema for telemetry_event
TELEMETRY_SCHEMA = {
    "type": "object",
    "properties": {
        "device_id": {"type": "string"},
        "policy_id": {"type": ["string", "null"]},
        "trip_id": {"type": "string"},
        "ts": {"type": "string", "format": "date-time"},
        "event_type": {"type": "string", "enum": ["heartbeat", "sample", "start_trip", "end_trip", "alert"]},
        "lat": {"type": ["number", "null"]},
        "lon": {"type": ["number", "null"]},
        "gps_accuracy_m": {"type": ["number", "null"]},
        "speed_kmh": {"type": ["number", "null"]},
        "accel_x_m_s2": {"type": ["number", "null"]},
        "accel_y_m_s2": {"type": ["number", "null"]},
        "accel_z_m_s2": {"type": ["number", "null"]},
        "brake_strength": {"type": ["number", "null"]},
        "steering_angle_deg": {"type": ["number", "null"]},
        "heading_deg": {"type": ["number", "null"]},
        "odometer_km": {"type": ["number", "null"]},
        "engine_rpm": {"type": ["integer", "null"]},
        "battery_level_pct": {"type": ["number", "null"]},
        "sample_rate_hz": {"type": ["number", "null"]},
        "provider": {"type": "string"},
        "hashed_driver_id": {"type": ["string", "null"]},
        "location_precision": {"type": "string", "enum": ["exact", "coarse", "aggregated"]}
    },
    "required": ["device_id", "trip_id", "ts", "event_type", "provider", "location_precision"]
}

def validate_telemetry_event(event: Dict[str, Any]) -> bool:
    """Validate a telemetry event against the schema.

    Args:
        event: Dictionary representing the telemetry event.

    Returns:
        bool: True if valid, raises ValidationError if invalid.
    """
    try:
        jsonschema.validate(instance=event, schema=TELEMETRY_SCHEMA)
        return True
    except jsonschema.ValidationError as e:
        raise ValueError(f"Invalid telemetry event: {e.message}") from e
