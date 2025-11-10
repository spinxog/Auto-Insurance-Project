"""Model serving for risk scoring."""

import joblib
import pandas as pd
from typing import Dict, Any
from src.models.train_baseline import train_risk_model  # For fallback

class RiskScorer:
    """Risk scoring service."""

    def __init__(self, model_path: str = 'models/riskscore/gbm/v20251109_1/model.pkl'):
        try:
            self.model = joblib.load(model_path)
        except FileNotFoundError:
            # Fallback to training a dummy model
            features = pd.DataFrame({'f_trip_max_speed': [60], 'f_trip_avg_accel': [0.5], 'f_trip_harsh_brake_count': [0]})
            labels = pd.Series([0.5])
            self.model = train_risk_model(features, labels)

    def score(self, features: Dict[str, float]) -> float:
        """Compute risk score from features.

        Args:
            features: Dictionary of feature values.

        Returns:
            Risk score (0-100).
        """
        df = pd.DataFrame([features])
        prediction = self.model.predict(df)[0]
        # Scale to 0-100
        score = min(100, max(0, prediction * 100))
        return score

# Example usage
if __name__ == "__main__":
    scorer = RiskScorer()
    sample_features = {
        'f_trip_max_speed': 70.0,
        'f_trip_avg_accel': 0.8,
        'f_trip_harsh_brake_count': 1.0
    }
    score = scorer.score(sample_features)
    print(f"Risk Score: {score}")
