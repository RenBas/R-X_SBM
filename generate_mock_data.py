"""
Mock Data Generator for SBM Dashboard – Region X
Generates realistic sample data for testing the upload functionality.
"""

import pandas as pd
import random
import numpy as np
from datetime import datetime, timedelta
from utils.constants import INDICATORS, DIMENSION_NAMES

# ─── SEED FOR REPRODUCIBILITY ───
random.seed(42)
np.random.seed(42)

# ─── SDO DATA (14 Divisions) ───
SDO_DATA = [
    {"id": 1, "name": "SDO Bukidnon", "capital": "Malaybalay City", "lat": 8.1547, "lng": 125.0568},
    {"id": 2, "name": "SDO Malaybalay City", "capital": "Malaybalay City", "lat": 8.1547, "lng": 125.0568},
    {"id": 3, "name": "SDO Valencia City", "capital": "Valencia City", "lat": 7.9045, "lng": 125.0922},
    {"id": 4, "name": "SDO Camiguin", "capital": "Mambajao", "lat": 9.2514, "lng": 124.7048},
    {"id": 5, "name": "SDO Lanao del Norte", "capital": "Tubod", "lat": 8.0599, "lng": 123.7894},
    {"id": 6, "name": "SDO Iligan City", "capital": "Iligan City", "lat": 8.2300, "lng": 124.2435},
    {"id": 7, "name": "SDO Misamis Occidental", "capital": "Oroquieta City", "lat": 8.4862, "lng": 123.8050},
    {"id": 8, "name": "SDO Oroquieta City", "capital": "Oroquieta City", "lat": 8.4862, "lng": 123.8050},
    {"id": 9, "name": "SDO Ozamiz City", "capital": "Ozamiz City", "lat": 8.1451, "lng": 123.8447},
    {"id": 10, "name": "SDO Tangub City", "capital": "Tangub City", "lat": 8.0698, "lng": 123.7483},
    {"id": 11, "name": "SDO Misamis Oriental", "capital": "Cagayan de Oro City", "lat": 8.4780, "lng": 124.6341},
    {"id": 12, "name": "SDO Cagayan de Oro City", "capital": "Cagayan de Oro City", "lat": 8.4780, "lng": 124.6341},
    {"id": 13, "name": "SDO Gingoog City", "capital": "Gingoog City", "lat": 8.7933, "lng": 125.1240},
    {"id": 14, "name": "SDO El Salvador City", "capital": "El Salvador City", "lat": 8.5622, "lng": 124.5508},
]

# ─── SCHOOL NAME GENERATORS ───
SCHOOL_TYPES = ["Elementary", "Secondary", "Integrated"]
SCHOOL_PREFIXES = [
    "Central", "National", "Memorial", "Regional", "Provincial", "City",
    "North", "South", "East", "West", "Central", "San", "Santa", "Santo",
    "New", "Old", "Sto. Niño", "Immaculate Conception", "Sacred Heart",
    "Divine Mercy", "St. Joseph", "St. Michael", "Our Lady of Lourdes"
]
SCHOOL_SUFFIXES = [
    "Elementary School", "National High School", "Integrated School",
    "Central School", "Memorial School", "Academy", "Institute"
]
BARANGAYS = [
    "Poblacion", "San Jose", "San Roque", "San Antonio", "San Miguel",
    "Santo Niño", "San Isidro", "San Juan", "San Pedro", "San Vicente",
    "Bgy. 1", "Bgy. 2", "Bgy. 3", "Bgy. 4", "Bgy. 5", "Bgy. 6", "Bgy. 7",
    "Bgy. 8", "Bgy. 9", "Bgy. 10", "Bgy. 11", "Bgy. 12", "Bgy. 13", "Bgy. 14"
]

def generate_school_name(division_name, school_type):
    """Generate a realistic school name."""
    prefix = random.choice(SCHOOL_PREFIXES)
    suffix = random.choice(SCHOOL_SUFFIXES)
    # Some schools are named after the division/city
    if random.random() < 0.3:
        city = division_name.replace("SDO ", "").replace(" City", "")
        return f"{city} {suffix}"
    return f"{prefix} {suffix}"

def generate_coordinates(base_lat, base_lng, spread=0.15):
    """Generate random coordinates around a base location."""
    lat = base_lat + (random.random() - 0.5) * spread * 2
    lng = base_lng + (random.random() - 0.5) * spread * 2
    return round(lat, 6), round(lng, 6)

def generate_enrollment():
    """Generate realistic enrollment numbers."""
    # Elementary: 150–1200, Secondary: 200–2500, Integrated: 300–3000
    return random.randint(150, 2500)

def generate_assessment_date():
    """Generate a random date in the last 3 months."""
    days_ago = random.randint(1, 90)
    return (datetime.now() - timedelta(days=days_ago)).strftime("%Y-%m-%d")

def generate_sbm_scores(dimension_biases=None):
    """Generate scores for all 42 indicators with some patterns."""
    scores = []
    for indicator in INDICATORS:
        # Get the dimension index for this indicator
        dim_name = indicator["dimension"]
        dim_idx = DIMENSION_NAMES.index(dim_name)
        
        # Use dimension bias if provided
        if dimension_biases and dim_idx < len(dimension_biases):
            base = dimension_biases[dim_idx]
            # Add random variation
            score = base + (random.random() - 0.5) * 0.8
        else:
            # No bias: random score between 0.0 and 3.0
            score = random.uniform(0.3, 2.9)
        
        # Clamp to 0.0–3.0 and round to 1 decimal
        score = round(max(0.0, min(3.0, score)), 1)
        scores.append(score)
    return scores

def get_degree_of_manifestation(score):
    """Determine the degree of manifestation based on score."""
    if score >= 2.5:
        return "Always Manifested"
    elif score >= 2.0:
        return "Frequently Manifested"
    elif score >= 1.0:
        return "Rarely Manifested"
    else:
        return "Not Yet Manifested"

# ─── GENERATE SCHOOLS ───
def generate_mock_data(num_schools_per_division=None):
    """
    Generate mock data for all divisions.
    Returns two DataFrames: (school_info_df, assessment_df)
    """
    if num_schools_per_division is None:
        # Random number of schools per division (3–8)
        num_schools_per_division = [random.randint(3, 8) for _ in SDO_DATA]
    
    all_schools = []
    all_assessments = []
    school_id_counter = 10000
    
    for idx, sdo in enumerate(SDO_DATA):
        num_schools = num_schools_per_division[idx] if isinstance(num_schools_per_division, list) else num_schools_per_division
        division_name = sdo["name"]
        
        # Random biases for dimensions to create variety
        # Some divisions are strong in certain areas, weak in others
        dim_biases = []
        for d in range(6):
            # Random baseline between 0.8 and 2.8
            base = random.uniform(0.8, 2.8)
            # Each division has a specialty and a weakness
            if d == idx % 6:  # Specialty
                base = min(3.0, base + 0.8)
            if d == (idx + 3) % 6:  # Weakness
                base = max(0.0, base - 0.8)
            dim_biases.append(round(base, 1))
        
        for i in range(num_schools):
            school_id = str(school_id_counter + i)
            school_type = random.choice(SCHOOL_TYPES)
            school_name = generate_school_name(division_name, school_type)
            enrollment = generate_enrollment()
            lat, lng = generate_coordinates(sdo["lat"], sdo["lng"])
            assessment_date = generate_assessment_date()
            data_status = "Complete" if random.random() < 0.85 else "Pending"
            
            # If pending, we don't need scores (they will be empty)
            if data_status == "Pending":
                scores = [""] * len(INDICATORS)
            else:
                scores = generate_sbm_scores(dim_biases)
            
            # School Information row
            school_info = {
                "School ID": school_id,
                "School Name": school_name,
                "School Type": school_type,
                "Division": division_name,
                "Region": "Region X – Northern Mindanao",
                "Congressional District": f"{random.randint(1, 3)} District",
                "Latitude": lat,
                "Longitude": lng,
                "Enrollment": enrollment,
                "Data Status": data_status,
                "Assessment Date": assessment_date,
                "School Head Name": f"Dr. {random.choice(['Juan', 'Maria', 'Jose', 'Ana', 'Pedro', 'Elena'])} {random.choice(['Santos', 'Reyes', 'Cruz', 'Garcia', 'Fernandez'])}",
                "School Head Email": f"principal{school_id}@deped.gov.ph",
                "Urban/Rural": random.choice(["Urban", "Rural"]),
                "Last SBM Assessment": (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d") if random.random() < 0.5 else ""
            }
            all_schools.append(school_info)
            
            # Assessment rows (one per indicator)
            if data_status == "Complete":
                for j, indicator in enumerate(INDICATORS):
                    score = scores[j]
                    assessment = {
                        "School ID": school_id,
                        "Indicator ID": indicator["id"],
                        "Dimension": indicator["dimension"],
                        "Indicator Description": indicator["description"],
                        "Score": score,
                        "Degree of Manifestation": get_degree_of_manifestation(score) if score != "" else "",
                        "Remarks": f"Needs improvement" if score < 1.5 else "" if random.random() < 0.3 else "",
                        "Evidence/Supporting Docs": f"https://drive.google.com/file/d/{''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=15))}" if random.random() < 0.2 else "",
                        "Date Assessed": assessment_date
                    }
                    all_assessments.append(assessment)
            else:
                # Pending: still add rows but with empty scores
                for j, indicator in enumerate(INDICATORS):
                    assessment = {
                        "School ID": school_id,
                        "Indicator ID": indicator["id"],
                        "Dimension": indicator["dimension"],
                        "Indicator Description": indicator["description"],
                        "Score": "",
                        "Degree of Manifestation": "",
                        "Remarks": "",
                        "Evidence/Supporting Docs": "",
                        "Date Assessed": ""
                    }
                    all_assessments.append(assessment)
        
        school_id_counter += num_schools
    
    school_df = pd.DataFrame(all_schools)
    assessment_df = pd.DataFrame(all_assessments)
    
    return school_df, assessment_df

# ─── GENERATE AND SAVE ───
def generate_mock_excel(filename="mock_sbm_data.xlsx"):
    """Generate mock data and save to an Excel file."""
    school_df, assessment_df = generate_mock_data()
    
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        school_df.to_excel(writer, sheet_name="School Information", index=False)
        assessment_df.to_excel(writer, sheet_name="SBM Assessment", index=False)
        
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
    
    print(f"✅ Mock data generated and saved to: {filename}")
    print(f"   School Information: {len(school_df)} schools")
    print(f"   SBM Assessment: {len(assessment_df)} indicator scores")
    return school_df, assessment_df

# ─── RUN SCRIPT ───
if __name__ == "__main__":
    generate_mock_excel("mock_sbm_data.xlsx")
