"""Pricing engine for premium adjustments."""

from src.models.explain import get_top_features_shap
import joblib
import pandas as pd

def map_score_to_premium(base_premium: float, risk_score: float, alpha: float = 0.02) -> float:
    """Map a risk score (0-100) to a new premium.

    Args:
        base_premium: The current premium in USD.
        risk_score: Risk score where 50 is neutral (0-100 scale).
        alpha: Scaling factor that controls sensitivity.

    Returns:
        new_premium: Adjusted premium in USD.
    """
    # Normalize the score around 50 (neutral)
    delta = (risk_score - 50) / 50.0
    return base_premium * (1 + alpha * delta)

def get_pricing_explanation(model_path: str, features_df: pd.DataFrame, risk_score: float, top_n: int = 3) -> dict:
    """Get pricing explanation with top contributing features.

    Args:
        model_path: Path to trained model
        features_df: DataFrame with features for this prediction
        risk_score: The predicted risk score
        top_n: Number of top features to include

    Returns:
        Dict with explanation data
    """
    model = joblib.load(model_path)
    top_features = get_top_features_shap(model, features_df, top_n=top_n)

    return {
        'risk_score': risk_score,
        'top_features': top_features,
        'model_version': 'v20251109_1'
    }

# Example usage
if __name__ == "__main__":
    base = 1000.0
    score = 60.0  # Higher risk
    new_premium = map_score_to_premium(base, score)
    print(f"New Premium: ${new_premium:.2f}")
