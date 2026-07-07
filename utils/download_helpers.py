"""Download helpers for exporting reports and templates."""

import pandas as pd
import io
from .constants import INDICATORS, DIMENSION_NAMES

def generate_report_data(sdo_name, schools_in_sdo, complete_schools):
    """Generate a DataFrame for the current view (report)."""
    if not schools_in_sdo:
        return None
    
    # Build report rows
    rows = []
    for school in schools_in_sdo:
        school_name = school["name"]
        school_type = school["type"]
        enrollment = school["enrollment"]
        overall = school["overall_index"]
        degree = school["degree"]
        data_status = school["data_status"]
        # Dimension scores
        dim_scores = school["dimension_scores"]
        row = {
            "School": school_name,
            "Type": school_type,
            "Enrollment": enrollment,
            "SBM Level": degree,
            "Data Status": data_status,
            "Overall Index": overall,
            "Curriculum & Teaching": dim_scores[0],
            "Learning Environment": dim_scores[1],
            "Leadership": dim_scores[2],
            "Governance & Accountability": dim_scores[3],
            "Human Resource & Team Dev.": dim_scores[4],
            "Finance & Resource Mgmt.": dim_scores[5]
        }
        rows.append(row)
    
    df = pd.DataFrame(rows)
    return df

def generate_template_csv():
    """Generate a CSV template for SBM data collection."""
    rows = []
    for indicator in INDICATORS:
        rows.append({
            "Indicator_ID": indicator["id"],
            "Dimension": indicator["dimension"],
            "Indicator_Description": indicator["description"],
            "Score (0-3)": "",          # To be filled by school
            "Remarks": ""               # Optional remarks
        })
    df = pd.DataFrame(rows)
    return df

def generate_excel_template():
    """Generate an Excel template with multiple sheets (indicators + instructions)."""
    # We'll provide both CSV and Excel support; we'll keep CSV for simplicity,
    # but if needed we can implement Excel using pandas. For now, return CSV.
    return generate_template_csv()
