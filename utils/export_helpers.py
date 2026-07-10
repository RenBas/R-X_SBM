"""Export utilities for SBM Dashboard."""

import io
import pandas as pd
from fpdf import FPDF
import plotly.graph_objects as go
from .constants import DIMENSION_NAMES
from .chart_helpers import create_radar_chart, create_indicators_table


def generate_excel_report(division_name, schools_in_sdo, complete_schools, dim_avgs, regional_dim_avgs):
    """Create an Excel file with multiple sheets."""
    output = io.BytesIO()

    # Sheet 1: Division Summary
    overall_avg = round(sum(s.get("overall_index", 0) for s in complete_schools) / len(complete_schools), 1) if complete_schools else 0.0
    summary_data = {
        "Metric": ["Division", "Total Schools", "Complete Schools", "Overall SBM Index"],
        "Value": [division_name, len(schools_in_sdo), len(complete_schools), f"{overall_avg:.1f}"]
    }
    df_summary = pd.DataFrame(summary_data)

    # Dimension averages
    dim_data = {"Dimension": DIMENSION_NAMES, "Division Average": dim_avgs, "Regional Average": regional_dim_avgs}
    df_dims = pd.DataFrame(dim_data)

    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df_summary.to_excel(writer, sheet_name="Division Summary", index=False)
        df_dims.to_excel(writer, sheet_name="Dimension Averages", index=False)

        # Sheet 2: School List
        rows = []
        for school in schools_in_sdo:
            dim_scores = school.get("dimension_scores", [0]*6)
            overall = school.get("overall_index", 0)
            lowest_idx = school.get("lowest_dim_index", 0)
            lowest_dim = DIMENSION_NAMES[lowest_idx] if 0 <= lowest_idx < 6 else "?"
            rows.append({
                "School": school.get("name", ""),
                "Type": school.get("type", ""),
                "Enrollment": school.get("enrollment", 0),
                "Overall": overall,
                "Curriculum & Teaching": dim_scores[0],
                "Learning Environment": dim_scores[1],
                "Leadership": dim_scores[2],
                "Governance & Accountability": dim_scores[3],
                "HR & Team Dev.": dim_scores[4],
                "Finance & Resource": dim_scores[5],
                "Lowest Dim.": f"{lowest_dim} ({school.get('lowest_dim_score', 0):.1f})"
            })
        df_schools = pd.DataFrame(rows)
        df_schools.to_excel(writer, sheet_name="School List", index=False)

        # Sheet 3: Indicators
        df_indicators = create_indicators_table(schools_in_sdo)
        if not df_indicators.empty:
            df_indicators.to_excel(writer, sheet_name="Indicators", index=False)

    output.seek(0)
    return output


def generate_pdf_report(division_name, schools_in_sdo, complete_schools, dim_avgs, regional_dim_avgs, overall_avg):
    """Create a PDF report with key metrics and a radar chart (uses built-in Helvetica, ASCII only)."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)

    # Title (use plain hyphen to avoid Unicode)
    title = f"SBM Dashboard Report - {division_name}"
    pdf.cell(0, 10, title, ln=True, align="C")
    pdf.ln(8)

    # Metrics
    pdf.set_font("Helvetica", size=11)
    pdf.cell(0, 7, f"Total Schools: {len(schools_in_sdo)}", ln=True)
    pdf.cell(0, 7, f"Complete Data: {len(complete_schools)}", ln=True)
    pdf.cell(0, 7, f"Overall SBM Index: {overall_avg:.1f} / 3.0", ln=True)
    pdf.ln(5)

    # Dimension averages table
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 7, "Dimension Averages", ln=True)
    pdf.set_font("Helvetica", size=9)

    col_widths = [65, 35, 35]
    # Header
    pdf.cell(col_widths[0], 6, "Dimension", border=1)
    pdf.cell(col_widths[1], 6, "Division", border=1)
    pdf.cell(col_widths[2], 6, "Regional", border=1)
    pdf.ln()
    for i, dim in enumerate(DIMENSION_NAMES):
        pdf.cell(col_widths[0], 6, dim, border=1)
        pdf.cell(col_widths[1], 6, f"{dim_avgs[i]:.1f}", border=1)
        pdf.cell(col_widths[2], 6, f"{regional_dim_avgs[i]:.1f}", border=1)
        pdf.ln()

    pdf.ln(8)

    # Radar chart image (skip if kaleido is missing)
    try:
        fig = create_radar_chart(dim_avgs, regional_dim_avgs)
        img_bytes = fig.to_image(format="png", width=500, height=500)
        img_io = io.BytesIO(img_bytes)
        pdf.image(img_io, x=10, w=180)
    except Exception:
        pdf.set_font("Helvetica", "I", 10)
        pdf.cell(0, 7, "(Radar chart not available - requires additional system dependency)", ln=True)

    # Output to BytesIO
    pdf_output = io.BytesIO()
    pdf.output(pdf_output)
    pdf_output.seek(0)
    return pdf_output
