# data_processor.py
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple

# ----------------------------------------------------------------------
# Constants
# ----------------------------------------------------------------------
DIMENSION_NAMES = [
    "Core Teaching",
    "Learning Environment",
    "Leadership & Governance",
    "Accountability",
    "Human Resources",
    "Financial Resources"
]

# Generate all 42 indicator IDs from CT_1 to FR_42
INDICATOR_IDS = []
for dim_prefix in ["CT", "LE", "LG", "AC", "HR", "FR"]:
    for i in range(1, 9):
        INDICATOR_IDS.append(f"{dim_prefix}_{i}")

# Map indicator to dimension
INDICATOR_TO_DIM = {}
for dim_name, prefix in zip(DIMENSION_NAMES, ["CT", "LE", "LG", "AC", "HR", "FR"]):
    for i in range(1, 9):
        INDICATOR_TO_DIM[f"{prefix}_{i}"] = dim_name


# ----------------------------------------------------------------------
# Main processing function
# ----------------------------------------------------------------------
def process_uploaded_data(df: pd.DataFrame) -> Dict:
    """
    Process the uploaded SBM Excel file (wide format) and return
    structured data for the dashboard, including Monte Carlo results.
    """
    data = df.copy()
    data.columns = data.columns.str.strip()

    # Identify existing indicator columns
    existing_indicators = [col for col in INDICATOR_IDS if col in data.columns]
    if not existing_indicators:
        raise ValueError("No indicator columns (CT_1 ... FR_42) found.")

    # Prepare school info
    school_info = data[["School ID", "School Name", "Division", "Latitude", "Longitude", "Offering"]].copy()
    if "Enrollment" in data.columns:
        school_info["Enrollment"] = pd.to_numeric(data["Enrollment"], errors='coerce').fillna(0).astype(int)
    else:
        school_info["Enrollment"] = 0

    school_info["School ID"] = school_info["School ID"].astype(str)
    school_info["Latitude"] = pd.to_numeric(school_info["Latitude"], errors='coerce').fillna(0.0)
    school_info["Longitude"] = pd.to_numeric(school_info["Longitude"], errors='coerce').fillna(0.0)

    # Melt indicators → long format
    assessment_df = data.melt(
        id_vars=["School ID"],
        value_vars=existing_indicators,
        var_name="Indicator ID",
        value_name="Score"
    )
    assessment_df["Score"] = pd.to_numeric(assessment_df["Score"], errors='coerce')
    assessment_df = assessment_df.dropna(subset=["Score"])
    assessment_df["Score"] = assessment_df["Score"].clip(0, 3)

    # Build SDO list
    divisions = school_info["Division"].unique()
    sdo_list = []
    for idx, div_name in enumerate(divisions, start=1):
        div_schools = school_info[school_info["Division"] == div_name]
        lat_mean = div_schools["Latitude"].mean() or 0.0
        lng_mean = div_schools["Longitude"].mean() or 0.0
        sdo_list.append({
            "id": idx,
            "name": div_name,
            "capital": div_name,
            "lat": lat_mean,
            "lng": lng_mean,
            "dimension_scores": [0.0] * 6,
            "overall_index": 0.0,
            "lowest_dim_index": 0,
            "lowest_dim_score": 0.0,
            "lowest_dim_name": DIMENSION_NAMES[0],
            "urgency_factor": 0.0
        })
    div_to_id = {sdo["name"]: sdo["id"] for sdo in sdo_list}

    # Process each school
    schools_list = []
    for _, school_row in school_info.iterrows():
        school_id = school_row["School ID"]
        school_name = school_row["School Name"]
        division = school_row["Division"]
        sdo_id = div_to_id.get(division)
        lat = school_row["Latitude"]
        lng = school_row["Longitude"]
        enrollment = school_row["Enrollment"]
        school_type = school_row.get("Offering", "Elementary")

        school_scores = assessment_df[assessment_df["School ID"] == school_id]

        if school_scores.empty:
            dim_scores = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
            overall_index = 0.0
            degree = "Pending"
            data_status = "Pending"
        else:
            dim_scores = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
            dim_counts = [0, 0, 0, 0, 0, 0]
            for _, row in school_scores.iterrows():
                indicator = row["Indicator ID"]
                score = row["Score"]
                dim_name = INDICATOR_TO_DIM.get(indicator)
                if dim_name and dim_name in DIMENSION_NAMES:
                    idx_dim = DIMENSION_NAMES.index(dim_name)
                    if score > 0:
                        dim_scores[idx_dim] += score
                        dim_counts[idx_dim] += 1
            for i in range(6):
                dim_scores[i] = round(dim_scores[i] / dim_counts[i], 1) if dim_counts[i] > 0 else 0.0

            overall_index = round(sum(dim_scores) / 6, 1) if any(dim_scores) else 0.0
            degree = (
                "Always Manifested" if overall_index >= 2.5 else
                "Frequently Manifested" if overall_index >= 2.0 else
                "Rarely Manifested" if overall_index >= 1.0 else
                "Not Yet Manifested"
            )
            data_status = "Completed"

        lowest_idx = dim_scores.index(min(dim_scores)) if any(dim_scores) else 0
        lowest_score = min(dim_scores) if any(dim_scores) else 0.0

        schools_list.append({
            "id": school_id,
            "name": school_name,
            "type": school_type,
            "sdo_id": sdo_id,
            "lat": lat,
            "lng": lng,
            "enrollment": enrollment,
            "overall_index": overall_index,
            "degree": degree,
            "dimension_scores": dim_scores,
            "data_status": data_status,
            "lowest_dim_index": lowest_idx,
            "lowest_dim_score": lowest_score,
            "division": division
        })

    # Compute SDO-level averages
    for sdo in sdo_list:
        sdo_id = sdo["id"]
        sdo_schools = [s for s in schools_list if s["sdo_id"] == sdo_id and s["data_status"] != "Pending"]
        if sdo_schools:
            dim_avgs = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
            for s in sdo_schools:
                for i in range(6):
                    dim_avgs[i] += s["dimension_scores"][i]
            dim_avgs = [round(v / len(sdo_schools), 1) for v in dim_avgs]
            sdo["dimension_scores"] = dim_avgs
            sdo["overall_index"] = round(sum(dim_avgs) / 6, 1)
            sdo["lowest_dim_index"] = dim_avgs.index(min(dim_avgs))
            sdo["lowest_dim_score"] = min(dim_avgs)
            sdo["lowest_dim_name"] = DIMENSION_NAMES[sdo["lowest_dim_index"]]

    # Urgency factors
    all_lowest = [sdo["lowest_dim_score"] for sdo in sdo_list]
    min_score = min(all_lowest) if all_lowest else 0
    max_score = max(all_lowest) if all_lowest else 1
    range_val = max_score - min_score or 0.001
    for sdo in sdo_list:
        raw = (sdo["lowest_dim_score"] - min_score) / range_val
        sdo["urgency_factor"] = round(1 - raw, 3)

    # ------------------------------------------------------------------
    # Monte Carlo Simulation (500 iterations)
    # ------------------------------------------------------------------
    monte_carlo_results = run_monte_carlo(schools_list, n_iter=500)

    return {
        "sdo_list": sdo_list,
        "schools": schools_list,
        "monte_carlo": monte_carlo_results
    }


# ----------------------------------------------------------------------
# Monte Carlo simulation
# ----------------------------------------------------------------------
def run_monte_carlo(schools: List[Dict], n_iter: int = 500, noise_std: float = 0.1) -> Dict:
    """
    Run Monte Carlo simulation on school overall indices.
    Returns mean, 95% CI, and all results.
    """
    valid_schools = [s for s in schools if s["data_status"] != "Pending"]
    if not valid_schools:
        return {"mean": 0.0, "lower": 0.0, "upper": 0.0, "all_results": []}

    np.random.seed(42)
    results = []

    for _ in range(n_iter):
        simulated_overalls = []
        for s in valid_schools:
            dims = np.array(s["dimension_scores"])
            noisy = np.clip(dims + np.random.normal(0, noise_std, size=6), 0, 3)
            simulated_overalls.append(np.mean(noisy))
        results.append(np.mean(simulated_overalls))

    return {
        "mean": round(np.mean(results), 3),
        "lower": round(np.percentile(results, 2.5), 3),
        "upper": round(np.percentile(results, 97.5), 3),
        "all_results": [round(x, 3) for x in results]
    }
