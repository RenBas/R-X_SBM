"""Download helpers for exporting reports and templates."""

import pandas as pd
import io
from datetime import datetime
from .constants import INDICATORS, DIMENSION_NAMES

def generate_report_data(sdo_name, schools_in_sdo, complete_schools):
    """Generate a DataFrame for the current view (report)."""
    if not schools_in_sdo:
        return None
    
    rows = []
    for school in schools_in_sdo:
        school_name = school["name"]
        school_type = school["type"]
        enrollment = school["enrollment"]
        overall = school["overall_index"]
        degree = school["degree"]
        data_status = school["data_status"]
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

def generate_excel_template():
    """
    Generate a comprehensive Excel template with 4 sheets:
    1. School Information
    2. SBM Assessment
    3. Dimension Scores Summary (auto-calculated)
    4. Technical Assistance History (optional)
    """
    # ─── Sheet 1: School Information ───
    school_info_data = [{
        "School ID": "",
        "School Name": "",
        "School Type": "Elementary",
        "Division": "",
        "Region": "Region X – Northern Mindanao",
        "Congressional District": "",
        "Latitude": "",
        "Longitude": "",
        "Enrollment": "",
        "Data Status": "Complete",
        "Assessment Date": datetime.now().strftime("%Y-%m-%d"),
        "School Head Name": "",
        "School Head Email": "",
        "Urban/Rural": "Urban",
        "Last SBM Assessment": ""
    }]
    school_df = pd.DataFrame(school_info_data)
    
    # ─── Sheet 2: SBM Assessment ───
    assessment_data = []
    for indicator in INDICATORS:
        assessment_data.append({
            "School ID": "",
            "Indicator ID": indicator["id"],
            "Dimension": indicator["dimension"],
            "Indicator Description": indicator["description"],
            "Score": "",
            "Degree of Manifestation": "",
            "Remarks": "",
            "Evidence/Supporting Docs": "",
            "Date Assessed": datetime.now().strftime("%Y-%m-%d")
        })
    assessment_df = pd.DataFrame(assessment_data)
    
    # ─── Sheet 3: Dimension Scores Summary ───
    summary_data = [{
        "School ID": "",
        "School Name": "",
        "Curriculum & Teaching": "",
        "Learning Environment": "",
        "Leadership": "",
        "Governance & Accountability": "",
        "HR & Team Development": "",
        "Finance & Resource Mgmt.": "",
        "Overall SBM Index": ""
    }]
    summary_df = pd.DataFrame(summary_data)
    
    # ─── Sheet 4: Technical Assistance History ───
    ta_data = [{
        "School ID": "",
        "TA Date": "",
        "TA Provider": "",
        "Focus Area": "",
        "Intervention Type": "",
        "Outcome": "",
        "Follow-up Needed": ""
    }]
    ta_df = pd.DataFrame(ta_data)
    
    # ─── Sheet 5: Instructions ───
    instructions_data = [
        {"Instructions": "📋 SBM Data Collection Template – DepEd Order No. 007, s. 2024"},
        {"Instructions": ""},
        {"Instructions": "=== SHEET 1: SCHOOL INFORMATION ==="},
        {"Instructions": "Fill in one row per school. This provides basic school data."},
        {"Instructions": ""},
        {"Instructions": "Column Guidelines:"},
        {"Instructions": "School ID: DepEd's unique school identifier (e.g., 12001)"},
        {"Instructions": "School Name: Full official school name"},
        {"Instructions": "School Type: Elementary / Secondary / Integrated / ALS"},
        {"Instructions": "Division: Schools Division Office name (e.g., SDO Cagayan de Oro City)"},
        {"Instructions": "Region: Region X – Northern Mindanao"},
        {"Instructions": "Congressional District: 1st, 2nd, 3rd, etc."},
        {"Instructions": "Latitude: GPS coordinate (e.g., 8.4780)"},
        {"Instructions": "Longitude: GPS coordinate (e.g., 124.6341)"},
        {"Instructions": "Enrollment: Total number of learners"},
        {"Instructions": "Data Status: Complete / Pending / Partial"},
        {"Instructions": "Assessment Date: When SBM assessment was conducted (YYYY-MM-DD)"},
        {"Instructions": "School Head Name: Name of School Head/Principal"},
        {"Instructions": "School Head Email: Email address for follow-up"},
        {"Instructions": "Urban/Rural: Urban / Rural"},
        {"Instructions": "Last SBM Assessment: Date of previous assessment (YYYY-MM-DD)"},
        {"Instructions": ""},
        {"Instructions": "=== SHEET 2: SBM ASSESSMENT ==="},
        {"Instructions": "Fill in one row per indicator for each school."},
        {"Instructions": ""},
        {"Instructions": "Column Guidelines:"},
        {"Instructions": "School ID: Must match the School ID in Sheet 1"},
        {"Instructions": "Indicator ID: 1 to 42 (refer to DepEd Order No. 007, s. 2024)"},
        {"Instructions": "Dimension: One of the six SBM dimensions"},
        {"Instructions": "Score: 0.0 – 3.0 (one decimal place)"},
        {"Instructions": "Degree of Manifestation: (auto-calculated based on Score)"},
        {"Instructions": "  • 2.5 – 3.0 = Always Manifested"},
        {"Instructions": "  • 2.0 – 2.4 = Frequently Manifested"},
        {"Instructions": "  • 1.0 – 1.9 = Rarely Manifested"},
        {"Instructions": "  • 0.0 – 0.9 = Not Yet Manifested"},
        {"Instructions": "Remarks: Optional notes (e.g., specific challenges observed)"},
        {"Instructions": "Evidence/Supporting Docs: URL or reference to supporting documents"},
        {"Instructions": "Date Assessed: Date this indicator was assessed"},
        {"Instructions": ""},
        {"Instructions": "=== SHEET 3: DIMENSION SCORES SUMMARY ==="},
        {"Instructions": "This sheet is auto-calculated by the system based on Sheet 2."},
        {"Instructions": "You do NOT need to fill this sheet manually."},
        {"Instructions": ""},
        {"Instructions": "=== SHEET 4: TECHNICAL ASSISTANCE HISTORY ==="},
        {"Instructions": "Optional – Track TA provided to each school."},
        {"Instructions": ""},
        {"Instructions": "=== DIMENSIONS (For Reference) ==="},
        {"Instructions": "1. Curriculum & Teaching"},
        {"Instructions": "2. Learning Environment"},
        {"Instructions": "3. Leadership"},
        {"Instructions": "4. Governance & Accountability"},
        {"Instructions": "5. Human Resource & Team Development"},
        {"Instructions": "6. Finance & Resource Management"},
        {"Instructions": ""},
        {"Instructions": "📞 For questions, contact: bhrod.sed@deped.gov.ph"},
    ]
    instructions_df = pd.DataFrame(instructions_data)
    
    # ─── Write to Excel ───
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        school_df.to_excel(writer, sheet_name="School Information", index=False)
        assessment_df.to_excel(writer, sheet_name="SBM Assessment", index=False)
        summary_df.to_excel(writer, sheet_name="Dimension Scores Summary", index=False)
        ta_df.to_excel(writer, sheet_name="TA History", index=False)
        instructions_df.to_excel(writer, sheet_name="Instructions", index=False, header=False)
        
        # Auto-adjust column widths
        for sheet_name in writer.sheets:
            worksheet = writer.sheets[sheet_name]
            for column in worksheet.columns:
                max_length = 0
                column_letter = column[0].column_letter
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = min(max_length + 2, 80)
                worksheet.column_dimensions[column_letter].width = adjusted_width
    
    output.seek(0)
    return output

def generate_template_csv():
    """Generate a CSV template for SBM data collection (legacy, single sheet)."""
    rows = []
    for indicator in INDICATORS:
        rows.append({
            "Indicator_ID": indicator["id"],
            "Dimension": indicator["dimension"],
            "Indicator_Description": indicator["description"],
            "Score (0-3)": "",
            "Remarks": ""
        })
    df = pd.DataFrame(rows)
    return df
