"""Baseline model training for risk scoring."""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error
import joblib
import os
import argparse
import numpy as np

def train_risk_model(features: pd.DataFrame, labels: pd.Series, seed: int = 42) -> GradientBoostingRegressor:
    """Train a baseline GBM model for risk scoring.

    Args:
        features: Feature DataFrame.
        labels: Target labels (e.g., claim probability).
        seed: Random seed for reproducibility.

    Returns:
        Trained model.
    """
    # Set seeds for reproducibility
    np.random.seed(seed)

    X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=seed)

    model = GradientBoostingRegressor(n_estimators=100, random_state=seed)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    print(f"Test MSE: {mse}")

    return model

# Example usage
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--seed', type=int, default=2025, help='Random seed')
    args = parser.parse_args()

    # Dummy data
    features = pd.DataFrame({
        'f_trip_max_speed': [60, 80, 50, 70],
        'f_trip_avg_accel': [0.5, 1.2, 0.3, 0.8],
        'f_trip_harsh_brake_count': [0, 2, 1, 0]
    })
    labels = pd.Series([0.1, 0.8, 0.2, 0.3])  # claim probabilities

    model = train_risk_model(features, labels, seed=args.seed)

    # Save model
    os.makedirs('models/riskscore/gbm/v20251109_1', exist_ok=True)
    joblib.dump(model, 'models/riskscore/gbm/v20251109_1/model.pkl')
