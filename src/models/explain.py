"""Model explanation utilities using SHAP."""

import shap
import pandas as pd
import numpy as np
from typing import List, Dict, Any

def get_top_features_shap(model, features: pd.DataFrame, top_n: int = 3) -> List[Dict[str, Any]]:
    """Get top N features contributing to prediction using SHAP.

    Args:
        model: Trained model with predict method
        features: Feature DataFrame for a single prediction
        top_n: Number of top features to return

    Returns:
        List of dicts with feature name and contribution
    """
    # Create SHAP explainer
    explainer = shap.TreeExplainer(model)

    # Get SHAP values for the instance
    shap_values = explainer.shap_values(features)

    # For single prediction, shap_values might be 1D
    if len(features) == 1:
        shap_values = shap_values.reshape(1, -1)

    # Get feature importances for this prediction
    instance_shap = shap_values[0]  # First (only) instance
    feature_names = features.columns

    # Sort by absolute contribution
    contributions = list(zip(feature_names, instance_shap))
    contributions.sort(key=lambda x: abs(x[1]), reverse=True)

    # Return top N
    top_features = []
    for name, contrib in contributions[:top_n]:
        top_features.append({
            'feature': name,
            'contribution': float(contrib)
        })

    return top_features
