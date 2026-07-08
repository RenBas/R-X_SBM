def run_simulation_engine(target_schools, interventions, time_horizon, target_type):
    """
    Execute the simulation engine and return results.
    """
    # Filter out schools with no data (all scores zero or pending)
    valid_schools = []
    for school in target_schools:
        scores = school.get("dimension_scores", [0, 0, 0, 0, 0, 0])
        if school.get("data_status") == "Pending" or all(s == 0 for s in scores):
            continue
        valid_schools.append(school)
    
    if not valid_schools:
        # Return empty results
        return {
            "target_type": target_type,
            "time_horizon": time_horizon,
            "school_predictions": [],
            "avg_current": 0,
            "avg_predicted": 0,
            "state_distribution": {},
            "impact_analysis": {"ta_impact": 0, "training_impact": 0, "budget_impact": 0, "combined_impact": 0, "significance": "No Data"},
            "risk_summary": {"avg_risk_score": 0, "high_risk_percentage": 0, "high_risk_schools": [], "recommendations": ["No valid schools with data."]},
            "interventions": interventions,
            "intervention_effects": {}
        }
    
    # Initialize models
    markov = MarkovModel()
    monte_carlo = MonteCarloSimulation(n_simulations=200)  # reduce simulations for speed
    risk_analyzer = RiskAnalyzer()
    
    # ... rest of the function with try/except around risky parts
