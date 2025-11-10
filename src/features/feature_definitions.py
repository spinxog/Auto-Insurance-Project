"""Feature definitions for telematics risk scoring."""

from typing import Dict, Any, List

# Canonical feature set
FEATURE_DEFINITIONS: Dict[str, Dict[str, Any]] = {
    "f_trip_max_speed": {
        "description": "Maximum speed during trip",
        "entity": "trip",
        "aggregation": "max",
        "window": None
    },
    "f_trip_avg_accel": {
        "description": "Average acceleration during trip",
        "entity": "trip",
        "aggregation": "avg",
        "window": None
    },
    "f_trip_harsh_brake_count": {
        "description": "Count of harsh braking events (>2.5 m/s² deceleration)",
        "entity": "trip",
        "aggregation": "count",
        "window": None
    },
    "f_policy_monthly_miles_30d": {
        "description": "Total miles driven in last 30 days",
        "entity": "policy",
        "aggregation": "sum",
        "window": "30d"
    },
    "f_policy_percent_city_driving": {
        "description": "Percentage of driving in city areas",
        "entity": "policy",
        "aggregation": "percent",
        "window": None
    }
}

def get_feature_names() -> List[str]:
    """Get list of all defined feature names."""
    return list(FEATURE_DEFINITIONS.keys())
