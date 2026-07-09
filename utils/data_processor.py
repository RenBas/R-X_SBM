# data_processor.py
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple

# ----------------------------------------------------------------------
# Constants – these should match your existing definitions
# If you have a constants.py file, you can import from there.
# Otherwise, define them here.
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
    for i in range(1, 9):  # Each dimension has 8 indicators
        INDICATOR_IDS.append(f"{dim_prefix}_{i}")

# Map indicator to dimension (for quick lookup)
INDICATOR_TO_DIM = {}
for dim_name, prefix in zip(DIMENSION_NAMES, ["CT", "LE", "LG", "AC", "HR", "FR"]):
    for i in range(1, 9):
        INDICATOR_TO_DIM[f"{prefix}_{i}"] = dim_name

# ----------------------------------------------------------------------
# Main processing function – now accepts a single wide‑format DataFrame
# ----------------------------------------------------------------------

def process_uploaded_data(df: pd.DataFrame) -> Dict:
    """
    Process the uploaded SBM Excel file (wide format) and return
    structured data for the dashboard.

    Parameters
    ----------
    df : pd.DataFrame
        The raw data from the uploaded file, with columns:
        School ID, School Name, Division, Latitude, Longitude, Offering,
        and the 42 indicator columns (CT_1 ... FR_42).

    Returns
    -------
    dict
        Contains 'sdo_list' and 'schools' as described in the original code,
        plus an additional 'monte_carlo' key with simulation results.
    """
    # 1. Make a clean copy
    data = df.copy()

    # 2. Sanitise column names (strip spaces)
    data.columns = data.columns.str.strip()

    # 3. Identify which of the 42 indicator columns actually exist in the file
    existing_indicators = [col for col in INDICATOR_IDS if col in data.columns]
    if not existing_indicators:
        raise ValueError("No indicator columns (CT_1 ... FR_42) found in the uploaded file.")

    # 4. Prepare school information
    school_info = data[["School ID", "School Name", "Division", "Latitude", "Longitude", "Offering"]].copy()
    # If Enrollment column exists, use it; otherwise set to 0
    if "Enrollment" in data.columns:
        school_info["Enrollment"] = pd.to_numeric(data["Enrollment"], errors='coerce').fillna(0).astype(int)
    else:
        school_info["Enrollment"] = 0

    # Convert IDs to string
    school_info["School ID"] = school_info["School ID"].astype(str)

    # Clean coordinates
    school_info["Latitude"] = pd.to_numeric(school_info["Latitude"], errors='coerce').fillna(0.0)
    school_info["Longitude"] = pd.to_numeric(school_info["Longitude"], errors='coerce').fillna(0.0)

    # 5. Melt the indicator columns into a long‑form assessment table
    assessment_df = data.melt(
        id_vars=["School ID"],
        value_vars=existing_indicators,
        var_name="Indicator ID",
        value_name="Score"
    )

    # Clean scores: numeric, clip to 0‑3, drop NaNs
    assessment_df["Score"] = pd.to_numeric(assessment_df["Score"], errors='coerce')
    assessment_df = assessment_df.dropna(subset=["Score"])
    assessment_df["Score"] = assessment_df["Score"].clip(0, 3)

    # 6. Build the list of SDOs (Divisions)
    divisions = school_info["Division"].unique()
    sdo_list = []
    for idx, div_name in enumerate(divisions, start=1):
        # Get average lat/lng for this division (or fallback to 0)
        div_schools = school_info[school_info["Division"] == div_name]
        lat_mean = div_schools["Latitude"].mean() or 0.0
        lng_mean = div_schools["Longitude"].mean() or 0.0
        sdo_list.append({
            "id": idx,
            "name": div_name,
            "capital": div_name,
            "lat": lat_mean,
            "lng": lng_mean,
            # These will be filled later
            "dimension_scores": [0.0] * 6,
            "overall_index": 0.0,
            "lowest_dim_index": 0,
            "lowest_dim_score": 0.0,
            "lowest_dim_name": DIMENSION_NAMES[0],
            "urgency_factor": 0.0
        })

    # Create a quick lookup from division name to sdo_id
    div_to_id = {sdo["name"]: sdo["id"] for sdo in sdo_list}

    # 7. Process each school
    schools_list = []
    for _, school_row in school_info.iterrows():
        school_id = school_row["School ID"]
        school_name = school_row["School Name"]
        division = school_row["Division"]
        sdo_id = div_to_id.get(division, None)
        lat = school_row["Latitude"]
        lng = school_row["Longitude"]
        enrollment = school_row["Enrollment"]
        school_type = school_row.get("Offering", "Elementary")  # or "School Type" if available

        # Get scores for this school
        school_scores = assessment_df[assessment_df["School ID"] == school_id]

        if school_scores.empty:
            # No scores → treat as Pending
            dim_scores = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
            overall_index = 0.0
            degree = "Pending"
            data_status = "Pending"
        else:
            # Compute dimension averages
            dim_scores = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
            dim_counts = [0, 0, 0, 0, 0, 0]

            for _, row in school_scores.iterrows():
                indicator = row["Indicator ID"]
                score = row["Score"]
                dim_name = INDICATOR_TO_DIM.get(indicator)
                if dim_name and dim_name in DIMENSION_NAMES:
                    idx_dim = DIMENSION_NAMES.index(dim_name)
                    if score > 0:   # only count non‑zero scores
                        dim_scores[idx_dim] += score
                        dim_counts[idx_dim] += 1

            for i in range(6):
                if dim_counts[i] > 0:
                    dim_scores[i] = round(dim_scores[i] / dim_counts[i], 1)
                else:
                    dim_scores[i] = 0.0

            overall_index = round(sum(dim_scores) / 6, 1) if any(dim_scores) else 0.0

            # Degree based on overall index
            if overall_index >= 2.5:
                degree = "Always Manifested"
            elif overall_index >= 2.0:
                degree = "Frequently Manifested"
            elif overall_index >= 1.0:
                degree = "Rarely Manifested"
            else:
                degree = "Not Yet Manifested"

            data_status = "Completed"

        # Lowest dimension
        if any(dim_scores):
            lowest_idx = dim_scores.index(min(dim_scores))
            lowest_score = min(dim_scores)
        else:
            lowest_idx = 0
            lowest_score = 0.0

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

    # 8. Compute SDO‑level averages
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
        else:
            # No schools with data for this division
            sdo["dimension_scores"] = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
            sdo["overall_index"] = 0.0
            sdo["lowest_dim_index"] = 0
            sdo["lowest_dim_score"] = 0.0
            sdo["lowest_dim_name"] = DIMENSION_NAMES[0]

    # 9. Compute urgency factors (normalised lowest dimension scores)
    all_lowest = [sdo["lowest_dim_score"] for sdo in sdo_list]
    min_score = min(all_lowest) if all_lowest else 0
    max_score = max(all_lowest) if all_lowest else 1
    range_val = max_score - min_score or 0.001

    for sdo in sdo_list:
        raw = (sdo["lowest_dim_score"] - min_score) / range_val
        sdo["urgency_factor"] = round(1 - raw, 3)

    # ------------------------------------------------------------------
    # 10. Monte Carlo Simulation (500 iterations)
    #     Simulates the overall index for each school by adding small
    #     random noise, then computes the distribution of the national
    #     average overall index.
    # ------------------------------------------------------------------
    monte_carlo_results = run_monte_carlo(schools_list, n_iter=500)

    # Return the final structure (add monte_carlo to the output)
    return {
        "sdo_list": sdo_list,
        "schools": schools_list,
        "monte_carlo": monte_carlo_results   # new key
    }


# ----------------------------------------------------------------------
# Monte Carlo simulation function (can be used separately)
# ----------------------------------------------------------------------

def run_monte_carlo(schools: List[Dict], n_iter: int = 500, noise_std: float = 0.1) -> Dict:
    """
    Run Monte Carlo simulation on school overall indices.

    Parameters
    ----------
    schools : list of school dicts (with 'dimension_scores' and 'data_status')
    n_iter : int, number of iterations (default 500)
    noise_std : float, standard deviation of the normal noise added to each dimension score

    Returns
    -------
    dict with keys:
        'mean' : average simulated overall index
        'lower' : 2.5th percentile
        'upper' : 97.5th percentile
        'all_results' : list of all simulated averages
    """
    # Filter only schools with actual data (not Pending)
    valid_schools = [s for s in schools if s["data_status"] != "Pending"]
    if not valid_schools:
        return {"mean": 0.0, "lower": 0.0, "upper": 0.0, "all_results": []}

    np.random.seed(42)   # for reproducibility
    results = []

    for _ in range(n_iter):
        simulated_overalls = []
        for s in valid_schools:
            dims = np.array(s["dimension_scores"])
            # Add Gaussian noise, clip to [0, 3]
            noisy = np.clip(dims + np.random.normal(0, noise_std, size=6), 0, 3)
            # Overall index for this school
            overall = np.mean(noisy)
            simulated_overalls.append(overall)

        # Average across all schools (could be weighted by enrollment if desired)
        avg_overall = np.mean(simulated_overalls)
        results.append(avg_overall)

    # Compute statistics
    mean = np.mean(results)
    lower = np.percentile(results, 2.5)
    upper = np.percentile(results, 97.5)

    return {
        "mean": round(mean, 3),
        "lower": round(lower, 3),
        "upper": round(upper, 3),
        "all_results": [round(x, 3) for x in results]  # keep for plotting
    }
