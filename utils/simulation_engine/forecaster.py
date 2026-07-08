"""
Forecaster – Time-series forecasting for SBM indices.
Dummy implementation without sklearn dependency.
"""

import numpy as np
from typing import Dict, List, Optional

class Forecaster:
    """
    Dummy forecaster that does not use sklearn.
    """
    def __init__(self, degree: int = 2):
        self.degree = degree
        self.history = {}
    
    def fit_historical_data(self, school_id: str, historical_scores: List[float]) -> None:
        self.history[school_id] = historical_scores
    
    def predict_future(self, school_id: str, steps: int = 3) -> Dict:
        history = self.history.get(school_id, [])
        if not history:
            return self._default_prediction(steps)
        # Simple linear extrapolation as fallback
        if len(history) >= 2:
            # Linear trend based on first and last point
            first = history[0]
            last = history[-1]
            slope = (last - first) / (len(history) - 1)
            last_point = last
            predictions = []
            for i in range(1, steps + 1):
                pred = last_point + slope * i
                predictions.append(max(0, min(3, round(pred, 2))))
            return {
                "school_id": school_id,
                "predictions": predictions,
                "confidence_intervals": {"50%": (p-0.2, p+0.2) for p in predictions},
                "trend_direction": "Upward" if slope > 0 else "Downward" if slope < 0 else "Stable",
                "predicted_change": round(predictions[-1] - history[-1], 2)
            }
        else:
            return self._default_prediction(steps)
    
    def _default_prediction(self, steps: int) -> Dict:
        return {
            "school_id": "unknown",
            "predictions": [1.5] * steps,
            "confidence_intervals": {"50%": (1.0, 2.0)},
            "trend_direction": "Unknown",
            "predicted_change": 0.0
        }
    
    def batch_predict(self, schools_data: List[Dict], steps: int = 3) -> List[Dict]:
        results = []
        for school in schools_data:
            school_id = school.get("id")
            hist = school.get("historical_scores", [])
            if not hist:
                # Use current score as history
                scores = school.get("dimension_scores", [0, 0, 0, 0, 0, 0])
                if any(scores):
                    hist = [sum(scores)/len(scores)]
                else:
                    hist = []
            self.fit_historical_data(school_id, hist)
            pred = self.predict_future(school_id, steps)
            pred["school_name"] = school.get("name", "Unknown")
            results.append(pred)
        return results
