"""Streaming transformations for telemetry."""

import pandas as pd
from typing import List, Dict, Any
from datetime import datetime

def compute_trip_features(events: pd.DataFrame) -> pd.DataFrame:
    """Compute trip-level features from a DataFrame of telemetry events.

    Args:
        events: DataFrame with columns ['device_id','trip_id','ts','speed_kmh',
                'accel_x_m_s2','accel_y_m_s2','lat','lon'].

    Returns:
        DataFrame containing one row per trip with features:
            - trip_max_speed: float
            - trip_avg_speed: float
            - harsh_brake_count: int
            - night_driving_minutes: int
    """
    # Ensure ts is datetime
    if 'ts' in events.columns:
        if events['ts'].dtype == 'object':
            events['ts'] = pd.to_datetime(events['ts'].str.rstrip('Z'), utc=True)
        else:
            events['ts'] = pd.to_datetime(events['ts'], utc=True)

    # Group by trip_id
    trip_features = events.groupby('trip_id').agg(
        trip_max_speed=('speed_kmh', 'max'),
        trip_avg_speed=('speed_kmh', 'mean'),
        harsh_brake_count=('accel_y_m_s2', lambda x: (x <= -2.5).sum())  # deceleration >= 2.5 m/s²
    ).reset_index()

    # Calculate night driving minutes (22:00-05:00)
    def calculate_night_minutes(group):
        night_start = 22
        night_end = 5
        night_minutes = 0
        for ts in group['ts']:
            hour = ts.hour
            if hour >= night_start or hour < night_end:
                night_minutes += 1  # Assuming 1 minute per event for simplicity
        return night_minutes

    night_driving = events.groupby('trip_id').apply(calculate_night_minutes, include_groups=False).reset_index(name='night_driving_minutes')
    trip_features = trip_features.merge(night_driving, on='trip_id', how='left')

    return trip_features

# Example usage
if __name__ == "__main__":
    # Sample data
    sample_events = pd.DataFrame({
        'trip_id': ['trip1', 'trip1', 'trip1', 'trip2'],
        'speed_kmh': [50, 60, 55, 45],
        'accel_y_m_s2': [0, -3, 1, -1]
    })
    features = compute_trip_features(sample_events)
    print(features)
