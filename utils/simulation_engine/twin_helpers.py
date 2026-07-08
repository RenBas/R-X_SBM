"""
Shared helper functions for the Digital Twin Simulation Engine.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
from ..constants import DIMENSION_NAMES, INDICATORS


def calculate_degree_of_manifestation(score: float) -> str:
    """
    Calculate the degree of manifestation based on score.
    
    Args:
        score: Float between 0.0 and 3.0
        
    Returns:
        String: "Always Manifested", "Frequently Manifested", 
                "Rarely Manifested", or "Not Yet Manifested"
    """
    if score >= 2.5:
        return "Always Manifested"
    elif score >= 2.0:
        return "Frequently Manifested"
    elif score >= 1.0:
        return "Rarely Manifested"
    else:
        return "Not Yet Manifested"


def get_degree_value(degree: str) -> float:
    """
    Convert degree of manifestation to numeric value.
    
    Args:
        degree: Degree string
        
    Returns:
        Float: 3.0, 2.0, 1.0, or 0.0
    """
    mapping = {
        "Always Manifested": 3.0,
        "Frequently Manifested": 2.0,
        "Rarely Manifested": 1.0,
        "Not Yet Manifested": 0.0
    }
    return mapping.get(degree, 0.0)


def get_dimension_index(dimension_name: str) -> int:
    """Get the index of a dimension by name."""
    try:
        return DIMENSION_NAMES.index(dimension_name)
    except ValueError:
        return -1


def normalize_scores(scores: List[float]) -> List[float]:
    """Normalize scores to ensure they are within 0.0–3.0."""
    return [max(0.0, min(3.0, round(float(s), 1))) for s in scores]


def validate_sbm_data(school_df: pd.DataFrame, assessment_df: pd.DataFrame) -> Tuple[bool, str]:
    """
    Validate uploaded SBM data before processing.
    
    Args:
        school_df: School Information DataFrame
        assessment_df: SBM Assessment DataFrame
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    # Check required columns in school_df
    required_school_cols = ["School ID", "School Name", "Division", "Latitude", "Longitude", "Enrollment", "Data Status"]
    missing_school_cols = [col for col in required_school_cols if col not in school_df.columns]
    if missing_school_cols:
        return False, f"Missing columns in School Information: {missing_school_cols}"
    
    # Check required columns in assessment_df
    required_assessment_cols = ["School ID", "Indicator ID", "Dimension", "Score"]
    missing_assessment_cols = [col for col in required_assessment_cols if col not in assessment_df.columns]
    if missing_assessment_cols:
        return False, f"Missing columns in SBM Assessment: {missing_assessment_cols}"
    
    # Check that all School IDs in assessment exist in school_df
    school_ids = set(school_df["School ID"].astype(str))
    assessment_ids = set(assessment_df["School ID"].astype(str))
    missing_ids = assessment_ids - school_ids
    if missing_ids:
        return False, f"School IDs in assessment not found in School Information: {missing_ids}"
    
    # Check score range (0.0–3.0)
    score_col = assessment_df[assessment_df["Score"] != ""]["Score"]
    if not score_col.empty:
        scores = pd.to_numeric(score_col, errors='coerce')
        if (scores < 0).any() or (scores > 3).any():
            return False, "Scores must be between 0.0 and 3.0"
    
    return True, ""


def compute_dimension_averages_from_scores(scores_df: pd.DataFrame, school_id: str) -> List[float]:
    """
    Compute dimension averages for a specific school from raw indicator scores.
    
    Args:
        scores_df: DataFrame with columns: School ID, Indicator ID, Score
        school_id: School ID to compute averages for
        
    Returns:
        List of 6 dimension averages (0.0–3.0)
    """
    school_scores = scores_df[scores_df["School ID"].astype(str) == str(school_id)]
    if school_scores.empty:
        return [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    
    # Map indicator IDs to dimensions
    indicator_to_dimension = {}
    for indicator in INDICATORS:
        indicator_to_dimension[indicator["id"]] = indicator["dimension"]
    
    # Group scores by dimension
    dim_scores = {dim: [] for dim in DIMENSION_NAMES}
    for _, row in school_scores.iterrows():
        if pd.isna(row["Score"]) or row["Score"] == "":
            continue
        dim = indicator_to_dimension.get(row["Indicator ID"])
        if dim:
            dim_scores[dim].append(float(row["Score"]))
    
    # Compute averages
    averages = []
    for dim in DIMENSION_NAMES:
        if dim_scores[dim]:
            averages.append(round(sum(dim_scores[dim]) / len(dim_scores[dim]), 1))
        else:
            averages.append(0.0)
    
    return averages


def compute_overall_index(dimension_averages: List[float]) -> float:
    """Compute overall SBM index from dimension averages."""
    if not dimension_averages or all(d == 0 for d in dimension_averages):
        return 0.0
    return round(sum(dimension_averages) / len(dimension_averages), 1)


def calculate_urgency_factor(score: float) -> float:
    """
    Calculate urgency factor based on score.
    Lower scores = higher urgency.
    """
    if score >= 2.5:
        return 0.0  # Stable
    elif score >= 2.0:
        return (2.5 - score) / 0.5 * 0.5  # 0.0 to 0.5
    elif score >= 1.0:
        return 0.5 + (2.0 - score) / 1.0 * 0.3  # 0.5 to 0.8
    else:
        return 0.8 + (1.0 - score) / 1.0 * 0.2  # 0.8 to 1.0
