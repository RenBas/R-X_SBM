"""
Causal Model for Intervention Impact Analysis.

Identifies which interventions have the greatest causal impact on SBM performance.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler


class InterventionImpact:
    """Represents the impact of an intervention on SBM performance."""
    
    def __init__(self, intervention_name: str, coefficient: float, p_value: float, confidence_interval: Tuple[float, float]):
        self.name = intervention_name
        self.coefficient = coefficient
        self.p_value = p_value
        self.confidence_interval = confidence_interval
        self.significance = "Significant" if p_value < 0.05 else "Not Significant"
        self.effect_size = self._calculate_effect_size()
    
    def _calculate_effect_size(self) -> str:
        """Calculate effect size category."""
        if abs(self.coefficient) >= 0.5:
            return "Large"
        elif abs(self.coefficient) >= 0.2:
            return "Medium"
        else:
            return "Small"
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "intervention": self.name,
            "coefficient": round(self.coefficient, 3),
            "p_value": round(self.p_value, 4),
            "significant": self.significance == "Significant",
            "effect_size": self.effect_size,
            "ci_lower": round(self.confidence_interval[0], 3),
            "ci_upper": round(self.confidence_interval[1], 3)
        }


class CausalModel:
    """
    Causal inference model for identifying intervention impacts.
    
    Uses linear regression with control variables to estimate the causal
    effect of each intervention on SBM outcomes.
    """
    
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.intervention_impacts = []
        self.r_squared = 0.0
        self.is_fitted = False
    
    def fit(self, data: pd.DataFrame, outcome_col: str, treatment_cols: List[str], 
            control_cols: List[str] = None) -> Dict:
        """
        Fit the causal model.
        
        Args:
            data: DataFrame with SBM scores and intervention data
            outcome_col: Column name for the outcome variable (e.g., "Overall SBM Index")
            treatment_cols: List of intervention columns (e.g., "TA_visits", "Training_hours")
            control_cols: List of control variables (e.g., "Enrollment", "Urban_Rural")
            
        Returns:
            Dict with model results
        """
        if control_cols is None:
            control_cols = []
        
        # Prepare features
        feature_cols = treatment_cols + control_cols
        X = data[feature_cols].values
        y = data[outcome_col].values
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Fit model
        self.model = LinearRegression()
        self.model.fit(X_scaled, y)
        self.is_fitted = True
        
        # Compute R-squared
        y_pred = self.model.predict(X_scaled)
        ss_res = np.sum((y - y_pred) ** 2)
        ss_tot = np.sum((y - np.mean(y)) ** 2)
        self.r_squared = 1 - (ss_res / ss_tot)
        
        # Compute standard errors (approximate)
        n = len(y)
        k = len(feature_cols)
        mse = ss_res / (n - k - 1)
        var_beta = mse * np.linalg.pinv(X_scaled.T @ X_scaled).diagonal()
        se_beta = np.sqrt(var_beta)
        
        # Compute t-statistics and p-values
        t_stats = self.model.coef_ / se_beta
        from scipy import stats
        p_values = 2 * (1 - stats.t.cdf(np.abs(t_stats), n - k - 1))
        
        # Compute confidence intervals (95%)
        t_critical = stats.t.ppf(0.975, n - k - 1)
        ci_lower = self.model.coef_ - t_critical * se_beta
        ci_upper = self.model.coef_ + t_critical * se_beta
        
        # Store intervention impacts
        self.intervention_impacts = []
        for i, col in enumerate(feature_cols):
            if col in treatment_cols:
                impact = InterventionImpact(
                    intervention_name=col,
                    coefficient=self.model.coef_[i],
                    p_value=p_values[i],
                    confidence_interval=(ci_lower[i], ci_upper[i])
                )
                self.intervention_impacts.append(impact)
        
        return self.get_summary()
    
    def predict(self, data: pd.DataFrame, feature_cols: List[str]) -> np.ndarray:
        """Predict SBM outcomes for new data."""
        if not self.is_fitted:
            raise ValueError("Model must be fitted before predicting.")
        
        X = data[feature_cols].values
        X_scaled = self.scaler.transform(X)
        return self.model.predict(X_scaled)
    
    def get_summary(self) -> Dict:
        """Get a summary of the causal model results."""
        return {
            "r_squared": round(self.r_squared, 3),
            "is_fitted": self.is_fitted,
            "num_treatments": len(self.intervention_impacts),
            "impacts": [imp.to_dict() for imp in self.intervention_impacts],
            "top_impact": self._get_top_impact()
        }
    
    def _get_top_impact(self) -> Optional[Dict]:
        """Get the intervention with the largest coefficient."""
        if not self.intervention_impacts:
            return None
        top = max(self.intervention_impacts, key=lambda x: abs(x.coefficient))
        return top.to_dict()
    
    def generate_recommendations(self) -> List[str]:
        """
        Generate actionable recommendations based on causal analysis.
        
        Returns:
            List of recommendation strings
        """
        if not self.is_fitted or not self.intervention_impacts:
            return ["Run the causal model to generate recommendations."]
        
        recommendations = []
        
        # Find significant positive impacts
        positive_impacts = [imp for imp in self.intervention_impacts 
                           if imp.coefficient > 0 and imp.significance == "Significant"]
        negative_impacts = [imp for imp in self.intervention_impacts 
                           if imp.coefficient < 0 and imp.significance == "Significant"]
        
        if positive_impacts:
            top = max(positive_impacts, key=lambda x: x.coefficient)
            recommendations.append(
                f"✅ Prioritize {top.name}: This intervention has the highest positive "
                f"impact on SBM performance (β = {top.coefficient:.2f}, p < 0.05). "
                f"Increasing this by one unit is associated with a {top.coefficient:.2f} "
                f"point improvement in the SBM index."
            )
        
        if negative_impacts:
            top_neg = min(negative_impacts, key=lambda x: x.coefficient)
            recommendations.append(
                f"⚠️ Review {top_neg.name}: This intervention shows a negative association "
                f"with SBM performance (β = {top_neg.coefficient:.2f}, p < 0.05). "
                f"Consider whether the current implementation is effective or needs adjustment."
            )
        
        # Suggest combined interventions
        if len(positive_impacts) >= 2:
            combined_effect = sum(imp.coefficient for imp in positive_impacts[:2])
            recommendations.append(
                f"💡 Consider combined interventions: Focusing on both "
                f"{positive_impacts[0].name} and {positive_impacts[1].name} "
                f"could yield a combined effect of {combined_effect:.2f} points."
            )
        
        if not recommendations:
            recommendations.append(
                "📊 No significant causal impacts detected. Consider collecting more data "
                "or refining intervention measurements."
            )
        
        return recommendations
