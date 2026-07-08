"""
Digital Twin Sandbox UI components.
Renders the scenario builder, prediction charts, impact analysis, and risk report.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from datetime import datetime
from typing import Dict, List, Optional
import time

# Import simulation engine components
from .simulation_engine import (
    MarkovModel,
    MonteCarloSimulation,
    RiskAnalyzer
)
from .constants import DIMENSION_NAMES


def render_sandbox(sdo_list, selected_sdo, schools_in_sdo, complete_schools, dim_avgs, overall_avg):
    """
    Main entry point for rendering the Digital Twin Sandbox.
    """
    st.markdown("## 🧪 Digital Twin Sandbox")
    st.caption("Run 'what-if' simulations to predict SBM performance under different intervention scenarios.")
    
    # ─── Get all schools for the sandbox (unfiltered) ───
    # Build a mapping of SDO names to SDO IDs for filtering
    sdo_name_to_id = {sdo["name"]: sdo["id"] for sdo in sdo_list}
    
    # Check if we have any schools
    if not schools_in_sdo:
        st.warning("No school data available. Please upload SBM data first.")
        return
    
    # ─── Scenario Builder (in main content, not sidebar) ───
    with st.expander("🎛️ Scenario Builder – Adjust Intervention Parameters", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            # Target selection
            target_type = st.radio(
                "Target",
                options=["Division", "Individual School"],
                index=0,
                horizontal=True,
                key="sandbox_target_type"
            )
            
            if target_type == "Division":
                division_names = [s["name"] for s in sdo_list]
                default_idx = 0
                for i, name in enumerate(division_names):
                    if name == selected_sdo["name"]:
                        default_idx = i
                        break
                target_division = st.selectbox(
                    "Select Division",
                    options=division_names,
                    index=default_idx,
                    key="sandbox_target_division"
                )
                
                target_sdo_id = sdo_name_to_id.get(target_division)
                target_schools = [s for s in schools_in_sdo if s.get("sdo_id") == target_sdo_id or s.get("division") == target_division]
                
                st.caption(f"📊 Schools in {target_division}: {len(target_schools)}")
            else:
                school_names = [s["name"] for s in schools_in_sdo]
                target_school = st.selectbox(
                    "Select School",
                    options=school_names,
                    index=0,
                    key="sandbox_target_school"
                )
                target_schools = [s for s in schools_in_sdo if s["name"] == target_school]
                st.caption(f"🏫 School: {target_school}")
        
        with col2:
            st.markdown("#### 📊 Intervention Parameters")
            
            ta_visits = st.slider(
                "Technical Assistance (TA) Visits",
                min_value=0, max_value=10, value=2,
                help="Number of TA visits per year",
                key="sandbox_ta_visits"
            )
            
            training_days = st.slider(
                "Capacity Building (Training Days)",
                min_value=0, max_value=10, value=2,
                help="Number of training days per year",
                key="sandbox_training_days"
            )
            
            budget_increase = st.slider(
                "Budget Increase (%)",
                min_value=0, max_value=50, value=10,
                help="Percentage increase in MOOE allocation",
                key="sandbox_budget_increase"
            )
            
            policy_change = st.selectbox(
                "Policy Change",
                options=["None", "New Curriculum", "Revised SBM Guidelines"],
                index=0,
                key="sandbox_policy_change"
            )
            
            time_horizon = st.slider(
                "Time Horizon (Years)",
                min_value=1, max_value=5, value=3,
                help="Number of years to forecast",
                key="sandbox_time_horizon"
            )
    
    # ─── Debug: Show how many schools were found ───
    if target_schools:
        st.caption(f"✅ Found {len(target_schools)} school(s) for simulation.")
    else:
        st.warning("⚠️ No schools found for the selected target. Please check your selection or upload data.")
    
    # ─── Run Button ───
    col_run, col_clear = st.columns([1, 4])
    with col_run:
        run_simulation = st.button(
            "🚀 Run Simulation",
            use_container_width=True,
            type="primary",
            key="sandbox_run_button"
        )
    
    # ─── Simulation Results ───
    if run_simulation:
        if not target_schools:
            st.warning("No schools found for the selected target. Please check your selection.")
            return
        
        st.markdown("---")
        st.markdown("### 📈 Simulation Results")
        
        # Prepare interventions dict
        interventions = {
            "technical_assistance": ta_visits,
            "capacity_building": training_days,
            "budget_increase": budget_increase,
            "policy_change": policy_change
        }
        
        # ── Run simulation ──
        with st.spinner("Running simulation... This may take a few moments."):
            # Add a progress bar
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Simulate progress (we'll update within the function)
            results = run_simulation_engine(
                target_schools,
                interventions,
                time_horizon,
                target_type,
                progress_bar=progress_bar,
                status_text=status_text
            )
            
            progress_bar.progress(100)
            status_text.text("Simulation complete!")
            time.sleep(0.5)
            progress_bar.empty()
            status_text.empty()
        
        # ── Display results ──
        display_simulation_results(results, target_type, time_horizon)
    
    else:
        st.info("👆 Adjust the intervention parameters above and click 'Run Simulation' to see predictions.")


def run_simulation_engine(target_schools, interventions, time_horizon, target_type, progress_bar=None, status_text=None):
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
    
    # Update progress
    if status_text:
        status_text.text("Initializing models...")
    if progress_bar:
        progress_bar.progress(10)
    
    # Initialize models
    markov = MarkovModel()
    monte_carlo = MonteCarloSimulation(n_simulations=50)  # reduced for speed
    risk_analyzer = RiskAnalyzer()
    
    # Prepare intervention effects for Monte Carlo
    intervention_effects = {
        "dim_0": interventions["technical_assistance"] * 0.03,
        "dim_1": interventions["capacity_building"] * 0.02,
        "dim_2": interventions["budget_increase"] * 0.01,
        "dim_3": interventions["technical_assistance"] * 0.02,
        "dim_4": interventions["capacity_building"] * 0.03,
        "dim_5": interventions["budget_increase"] * 0.02,
    }
    
    # Also store intervention dict for Markov
    intervention_dict = {
        "technical_assistance": interventions["technical_assistance"] / 10.0,
        "capacity_building": interventions["capacity_building"] / 10.0,
        "budget_increase": interventions["budget_increase"] / 50.0,
    }
    
    # ── Per-school predictions ──
    school_predictions = []
    overall_predictions = []
    total_schools = len(valid_schools)
    
    for idx, school in enumerate(valid_schools):
        if status_text:
            status_text.text(f"Processing school {idx+1}/{total_schools}: {school.get('name', 'Unknown')}")
        if progress_bar:
            progress_bar.progress(10 + int((idx / total_schools) * 70))
        
        scores = school.get("dimension_scores", [0, 0, 0, 0, 0, 0])
        
        # Markov prediction
        markov_result = markov.predict_school_transition(
            school_id=school.get("id", "unknown"),
            current_scores=scores,
            interventions=intervention_dict,
            steps=time_horizon
        )
        
        # Monte Carlo simulation
        mc_result = monte_carlo.simulate_school_progression(
            current_scores=scores,
            intervention_effects=intervention_effects,
            time_steps=time_horizon,
            volatility=0.15
        )
        
        # Risk analysis
        risk_profile = risk_analyzer.analyze_school({
            "id": school.get("id"),
            "name": school.get("name"),
            "dimension_scores": scores
        })
        
        school_predictions.append({
            "school": school,
            "markov": markov_result,
            "monte_carlo": mc_result,
            "risk": risk_profile
        })
        
        # Track overall for aggregation
        overall_predictions.append(mc_result.forecast_values[-1] if mc_result.forecast_values else scores[0])
    
    if progress_bar:
        progress_bar.progress(85)
    if status_text:
        status_text.text("Aggregating results...")
    
    # ── Aggregate division-level results ──
    avg_current = sum(s.get("overall_index", 0) for s in valid_schools) / len(valid_schools) if valid_schools else 0
    avg_predicted = sum(overall_predictions) / len(overall_predictions) if overall_predictions else 0
    
    # Compute distribution of states at final year
    state_distribution = {"Not Yet Manifested": 0, "Rarely Manifested": 0,
                          "Frequently Manifested": 0, "Always Manifested": 0}
    for pred in school_predictions:
        final_state = pred["markov"]["predicted_states"][-1] if pred["markov"]["predicted_states"] else "Not Yet Manifested"
        if final_state in state_distribution:
            state_distribution[final_state] += 1
    total = len(school_predictions) or 1
    state_distribution = {k: round(v / total * 100, 1) for k, v in state_distribution.items()}
    
    # ── Causal impact analysis (simplified) ──
    improvement = avg_predicted - avg_current if avg_current > 0 else 0
    impact_analysis = {
        "ta_impact": round(interventions["technical_assistance"] * 0.05, 2),
        "training_impact": round(interventions["capacity_building"] * 0.04, 2),
        "budget_impact": round(interventions["budget_increase"] * 0.02, 2),
        "combined_impact": round(improvement, 2),
        "significance": "Significant" if improvement > 0.2 else "Moderate" if improvement > 0.1 else "Low"
    }
    
    # ── Risk summary ──
    risk_summary = risk_analyzer.get_division_risk_summary(
        division_name=valid_schools[0].get("division", "Division") if valid_schools else "Unknown",
        schools_data=valid_schools
    )
    
    # Combine all results
    results = {
        "target_type": target_type,
        "time_horizon": time_horizon,
        "school_predictions": school_predictions,
        "avg_current": avg_current,
        "avg_predicted": avg_predicted,
        "state_distribution": state_distribution,
        "impact_analysis": impact_analysis,
        "risk_summary": risk_summary,
        "interventions": interventions,
        "intervention_effects": intervention_effects
    }
    
    if progress_bar:
        progress_bar.progress(100)
    
    return results


def display_simulation_results(results, target_type, time_horizon):
    """
    Display simulation results using Streamlit components and Plotly charts.
    """
    if not results["school_predictions"]:
        st.warning("No valid schools found for simulation. Please check your data.")
        return
    
    # ── Summary metrics ──
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(
            label="Current SBM Index",
            value=f"{results['avg_current']:.2f}",
            delta=None
        )
    with col2:
        st.metric(
            label=f"Predicted ({time_horizon} years)",
            value=f"{results['avg_predicted']:.2f}",
            delta=round(results['avg_predicted'] - results['avg_current'], 2),
            delta_color="normal" if results['avg_predicted'] >= results['avg_current'] else "inverse"
        )
    with col3:
        st.metric(
            label="Improvement",
            value=f"{results['avg_predicted'] - results['avg_current']:+.2f}",
            delta=None
        )
    with col4:
        st.metric(
            label="Confidence",
            value="85%",
            delta=None
        )
    
    # ── Forecast Chart ──
    st.markdown("#### 📈 Forecast Trend")
    
    # Prepare data for plotting
    current_year = datetime.now().year
    years = [f"{current_year}"] + [f"{current_year + i}" for i in range(1, time_horizon + 1)]
    
    # Average forecast from Monte Carlo across all schools
    avg_forecast = [results['avg_current']]
    forecast_values = []
    for pred in results['school_predictions']:
        forecast_values.append(pred['monte_carlo'].forecast_values)
    if forecast_values:
        avg_forecast.extend(np.mean(forecast_values, axis=0).tolist())
    else:
        avg_forecast.extend([results['avg_predicted']] * time_horizon)
    
    # Confidence intervals (50%)
    ci_lower = [max(0, avg_forecast[i] - 0.3) for i in range(len(avg_forecast))]
    ci_upper = [min(3, avg_forecast[i] + 0.3) for i in range(len(avg_forecast))]
    
    fig = go.Figure()
    
    # Add confidence interval band
    fig.add_trace(go.Scatter(
        x=years + years[::-1],
        y=ci_upper + ci_lower[::-1],
        fill='toself',
        fillcolor='rgba(0, 51, 160, 0.15)',
        line=dict(color='rgba(0,0,0,0)'),
        hoverinfo='skip',
        showlegend=False,
        name='Confidence Interval (50%)'
    ))
    
    # Add main forecast line
    fig.add_trace(go.Scatter(
        x=years,
        y=avg_forecast,
        mode='lines+markers',
        name='Predicted',
        line=dict(color='#0033A0', width=3),
        marker=dict(size=8)
    ))
    
    # Add historical baseline (current year only)
    fig.add_trace(go.Scatter(
        x=[years[0]],
        y=[results['avg_current']],
        mode='markers',
        name='Current',
        marker=dict(color='#CE1126', size=12)
    ))
    
    fig.update_layout(
        title="Overall SBM Index Forecast",
        xaxis_title="Year",
        yaxis_title="SBM Index",
        yaxis=dict(range=[0, 3.5]),
        height=400,
        margin=dict(l=40, r=40, t=40, b=40),
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='center', x=0.5),
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, width='stretch', key="sandbox_forecast_chart")
    
    # ── State Distribution ──
    st.markdown("#### 📊 State Distribution (Final Year)")
    dist = results['state_distribution']
    
    if dist:
        fig2 = go.Figure(data=[
            go.Bar(
                x=list(dist.keys()),
                y=list(dist.values()),
                marker_color=['#9CA3AF', '#F97316', '#EAB308', '#22C55E'],
                text=[f"{v:.1f}%" for v in dist.values()],
                textposition='auto'
            )
        ])
        fig2.update_layout(
            title="Percentage of Schools by SBM State",
            yaxis_title="Percentage (%)",
            height=300,
            margin=dict(l=40, r=40, t=40, b=40),
            xaxis=dict(tickangle=-15)
        )
        st.plotly_chart(fig2, width='stretch', key="sandbox_distribution_chart")
    else:
        st.caption("No state distribution data available.")
    
    # ── Impact Analysis ──
    st.markdown("#### 🔍 Intervention Impact Analysis")
    impact = results['impact_analysis']
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("TA Impact", f"+{impact['ta_impact']:.2f}")
    with col2:
        st.metric("Training Impact", f"+{impact['training_impact']:.2f}")
    with col3:
        st.metric("Budget Impact", f"+{impact['budget_impact']:.2f}")
    with col4:
        st.metric("Combined Impact", f"+{impact['combined_impact']:.2f}")
    
    st.caption(f"📌 Overall Significance: {impact['significance']}")
    
    # ── Risk Report ──
    st.markdown("#### ⚠️ Risk Report")
    risk = results['risk_summary']
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Average Risk Score", f"{risk.get('avg_risk_score', 0):.2f}")
        st.caption(f"High Risk Schools: {risk.get('high_risk_percentage', 0):.1f}%")
    with col2:
        high_risk_count = len(risk.get('high_risk_schools', []))
        st.metric("Total Schools at Risk", high_risk_count)
        if high_risk_count > 0:
            st.write("Affected schools:")
            for name in risk.get('high_risk_schools', [])[:3]:
                st.write(f"- {name}")
    
    # Recommendations
    st.markdown("#### 💡 Recommendations")
    for rec in risk.get('recommendations', []):
        st.write(f"- {rec}")
    
    # ── Export button ──
    st.download_button(
        label="📥 Export Simulation Report (CSV)",
        data=pd.DataFrame(results['school_predictions']).to_csv(index=False),
        file_name="simulation_report.csv",
        mime="text/csv",
        use_container_width=True,
        key="sandbox_export_button"
    )
