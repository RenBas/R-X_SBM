"""
Simulation Engine for SBM Digital Twin – Phase 2.
"""

from .markov_model import MarkovModel, StateTransition
from .monte_carlo import MonteCarloSimulation
from .risk_analyzer import RiskAnalyzer
# from .forecaster import Forecaster  # Disabled to avoid sklearn dependency
from .twin_helpers import (
    calculate_degree_of_manifestation,
    get_dimension_index,
    normalize_scores,
    validate_sbm_data,
    compute_dimension_averages_from_scores,
    compute_overall_index,
    calculate_urgency_factor
)

__all__ = [
    "MarkovModel",
    "StateTransition",
    "MonteCarloSimulation",
    "RiskAnalyzer",
    # "Forecaster",
    "calculate_degree_of_manifestation",
    "get_dimension_index",
    "normalize_scores",
    "validate_sbm_data",
    "compute_dimension_averages_from_scores",
    "compute_overall_index",
    "calculate_urgency_factor",
]
