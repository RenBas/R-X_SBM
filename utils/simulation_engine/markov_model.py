"""
Markov Chain Model for SBM State Transitions.

Predicts the probability of a school transitioning between SBM states
based on current state and intervention intensity.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
from .twin_helpers import get_degree_value, calculate_degree_of_manifestation


class StateTransition:
    """Represents a state transition in the Markov Chain."""
    
    STATES = ["Not Yet Manifested", "Rarely Manifested", "Frequently Manifested", "Always Manifested"]
    STATE_VALUES = {"Not Yet Manifested": 0, "Rarely Manifested": 1, "Frequently Manifested": 2, "Always Manifested": 3}
    
    def __init__(self):
        # Base transition probability matrix
        # Rows: current state, Columns: next state
        # Default: small positive probability of improvement, larger probability of staying
        self.base_matrix = np.array([
            [0.60, 0.30, 0.08, 0.02],  # Not Yet Manifested
            [0.10, 0.55, 0.30, 0.05],  # Rarely Manifested
            [0.02, 0.15, 0.55, 0.28],  # Frequently Manifested
            [0.01, 0.04, 0.20, 0.75],  # Always Manifested
        ])
        
        # Intervention impact multipliers
        # How much each intervention type shifts transition probabilities
        self.intervention_multipliers = {
            "technical_assistance": 1.15,
            "capacity_building": 1.10,
            "budget_increase": 1.05,
            "policy_change": 1.12,
        }
    
    def get_state_index(self, state: str) -> int:
        """Convert state string to index."""
        return self.STATE_VALUES.get(state, 0)
    
    def get_state_from_score(self, score: float) -> str:
        """Convert score to state."""
        return calculate_degree_of_manifestation(score)
    
    def get_transition_probabilities(self, current_state: str, interventions: Dict[str, float] = None) -> np.ndarray:
        """
        Get transition probabilities for a given state with intervention effects.
        
        Args:
            current_state: Current degree of manifestation
            interventions: Dictionary of intervention intensities (0.0–1.0)
            
        Returns:
            Array of probabilities for moving to each state
        """
        state_idx = self.get_state_index(current_state)
        base_probs = self.base_matrix[state_idx].copy()
        
        if interventions:
            # Apply intervention multipliers
            effect = 0.0
            for intervention, intensity in interventions.items():
                multiplier = self.intervention_multipliers.get(intervention, 1.0)
                effect += (multiplier - 1.0) * intensity
            
            # Shift probabilities toward higher states
            if effect > 0:
                # Shift mass upward
                shift = min(effect * 0.3, 0.5)  # Max 50% shift
                for i in range(len(base_probs) - 1, 0, -1):
                    # Move probability from lower to higher states
                    base_probs[i] += base_probs[i-1] * shift
                    base_probs[i-1] -= base_probs[i-1] * shift
                
                # Ensure all probabilities are positive
                base_probs = np.maximum(base_probs, 0.001)
                # Normalize
                base_probs = base_probs / base_probs.sum()
        
        return base_probs
    
    def predict_next_state(self, current_state: str, interventions: Dict[str, float] = None) -> Tuple[str, np.ndarray]:
        """
        Predict the next state based on current state and interventions.
        
        Args:
            current_state: Current degree of manifestation
            interventions: Intervention intensities
            
        Returns:
            Tuple of (predicted_state, probability_distribution)
        """
        probs = self.get_transition_probabilities(current_state, interventions)
        next_state_idx = np.random.choice(len(self.STATES), p=probs)
        return self.STATES[next_state_idx], probs
    
    def predict_multiple_steps(self, current_state: str, steps: int, 
                               interventions: Dict[str, float] = None) -> List[Tuple[str, float]]:
        """
        Predict state progression over multiple time steps.
        
        Args:
            current_state: Starting state
            steps: Number of steps to simulate
            interventions: Intervention intensities (applied at each step)
            
        Returns:
            List of (state, confidence_score) for each step
        """
        results = []
        state = current_state
        
        for _ in range(steps):
            probs = self.get_transition_probabilities(state, interventions)
            state_idx = np.argmax(probs)  # Most likely next state
            next_state = self.STATES[state_idx]
            confidence = probs[state_idx]
            
            results.append((next_state, confidence))
            state = next_state
        
        return results


class MarkovModel:
    """Main Markov Chain model for SBM predictions."""
    
    def __init__(self):
        self.transition = StateTransition()
        self.historical_data = None
    
    def load_historical_data(self, data: pd.DataFrame):
        """Load historical SBM assessment data for training."""
        self.historical_data = data
    
    def fit_transition_matrix(self):
        """Fit transition matrix from historical data (if available)."""
        # TODO: Implement data-driven transition matrix fitting
        # For now, use the default base_matrix
        pass
    
    def predict_school_transition(self, school_id: str, current_scores: List[float],
                                   interventions: Dict[str, float] = None,
                                   steps: int = 3) -> Dict:
        """
        Predict a school's state transitions over multiple time periods.
        
        Args:
            school_id: School identifier
            current_scores: List of 6 dimension scores
            interventions: Intervention intensities
            steps: Number of steps to predict
            
        Returns:
            Dict with prediction results
        """
        # Compute current overall index
        overall = round(sum(current_scores) / len(current_scores), 1)
        current_state = self.transition.get_state_from_score(overall)
        
        # Predict transitions
        transitions = self.transition.predict_multiple_steps(current_state, steps, interventions)
        
        # Build results
        results = {
            "school_id": school_id,
            "current_state": current_state,
            "current_index": overall,
            "steps": [],
            "predicted_states": [],
            "confidence_scores": []
        }
        
        for i, (state, confidence) in enumerate(transitions):
            # Convert state back to a rough score for visualization
            score_map = {"Not Yet Manifested": 0.5, "Rarely Manifested": 1.5, 
                         "Frequently Manifested": 2.5, "Always Manifested": 3.0}
            predicted_score = score_map.get(state, 1.0)
            
            step_data = {
                "step": i + 1,
                "state": state,
                "score": predicted_score,
                "confidence": confidence,
                "time_period": f"Year {i + 1}"
            }
            results["steps"].append(step_data)
            results["predicted_states"].append(state)
            results["confidence_scores"].append(confidence)
        
        return results
    
    def predict_division_summary(self, division_name: str, schools_data: List[Dict],
                                 interventions: Dict[str, float] = None,
                                 steps: int = 3) -> Dict:
        """
        Predict state transitions for all schools in a division.
        
        Args:
            division_name: Division name
            schools_data: List of school data dictionaries
            interventions: Intervention intensities
            steps: Number of steps to predict
            
        Returns:
            Dict with division-level summary predictions
        """
        results = []
        for school in schools_data:
            school_id = school.get("id")
            scores = school.get("dimension_scores", [0, 0, 0, 0, 0, 0])
            pred = self.predict_school_transition(school_id, scores, interventions, steps)
            results.append(pred)
        
        # Aggregate results
        summary = {
            "division": division_name,
            "total_schools": len(results),
            "current_distribution": self._get_state_distribution([r["current_state"] for r in results]),
            "predicted_distribution": {},
            "average_confidence": {},
            "school_predictions": results
        }
        
        # Distribution for each step
        for step in range(1, steps + 1):
            states = []
            for r in results:
                if step <= len(r["predicted_states"]):
                    states.append(r["predicted_states"][step - 1])
            summary["predicted_distribution"][f"Year {step}"] = self._get_state_distribution(states)
            summary["average_confidence"][f"Year {step}"] = round(
                sum(r["confidence_scores"][step - 1] for r in results if step <= len(r["confidence_scores"])) / len(results), 2
            )
        
        return summary
    
    def _get_state_distribution(self, states: List[str]) -> Dict:
        """Get distribution of states."""
        distribution = {"Not Yet Manifested": 0, "Rarely Manifested": 0, 
                        "Frequently Manifested": 0, "Always Manifested": 0}
        for state in states:
            if state in distribution:
                distribution[state] += 1
        total = len(states) or 1
        return {k: round(v / total * 100, 1) for k, v in distribution.items()}
