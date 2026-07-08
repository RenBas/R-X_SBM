from datetime import datetime, timedelta
import random
import numpy as np
import pandas as pd

# ─── SEED FOR REPRODUCIBILITY ───
random.seed(42)
np.random.seed(42)

# ─── MOCKED CONSTANTS (Replacing utils.constants) ───
DIMENSION_NAMES = [
    "Leadership and Governance",
    "Curriculum and Instruction",
    "Accountability and Continuous Improvement",
    "Management of Resources",
]

# Standard DepEd School-Based Management (SBM) Sample Indicators
INDICATORS = [
    {
        "id": "A.1",
        "dimension": "Leadership and Governance",
        "description": "Development plan collaboratively developed by stakeholders",
    },
    {
        "id": "A.2",
        "dimension": "Leadership and Governance",
        "description": "Leadership network facilitates data-driven decision making",
    },
    {
        "id": "B.1",
        "dimension": "Curriculum and Instruction",
        "description": "Curriculum is localized, contextualized, and implemented",
    },
    {
        "id": "B.2",
        "dimension": "Curriculum and Instruction",
        "description": "Learning environment is learner-centered, safe, and inclusive",
    },
    {
        "id": "C.1",
        "dimension": "Accountability and Continuous Improvement",
        "description": "Roles and responsibilities of stakeholders are clearly defined",
    },
    {
        "id": "D.1",
        "dimension": "Management of Resources",
        "description": "Regular resource inventory and collaborative allocation system",
    },
]

# ─── SDO DATA (14 Divisions) ───
SDO_DATA = [
    {
        "id": 1,
        "name": "SDO Bukidnon",
        "capital": "Malaybalay City",
        "lat": 8.1547,
        "lng": 125.0568,
    },
    {
        "id": 2,
        "name": "SDO Malaybalay City",
        "capital": "Malaybalay City",
        "lat": 8.1547,
        "lng": 125.0568,
    },
    {
        "id": 3,
        "name": "SDO Valencia City",
        "capital": "Valencia City",
        "lat": 7.9045,
        "lng": 125.0922,
    },
    {
        "id": 4,
        "name": "SDO Camiguin",
        "capital": "Mambajao",
        "lat": 9.2514,
        "lng": 124.7048,
    },
    {
        "id": 5,
        "name": "SDO Lanao del Norte",
        "capital": "Tubod",
        "lat": 8.0599,
        "lng": 123.7894,
    },
    {
        "id": 6,
        "name": "SDO Iligan City",
        "capital": "Iligan City",
        "lat": 8.23,
        "lng": 124.2435,
    },
    {
        "id": 7,
        "name": "SDO Misamis Occidental",
        "capital": "Oroquieta City",
        "lat": 8.4862,
        "lng": 123.805,
    },
    {
        "id": 8,
        "name": "SDO Oroquieta City",
        "capital": "Oroquieta City",
        "lat": 8.4862,
        "lng": 123.805,
    },
    {
        "id": 9,
        "name": "SDO Ozamiz City",
        "capital": "Ozamiz City",
        "lat": 8.1451,
        "lng": 123.8447,
    },
    {
        "id": 10,
        "name": "SDO Tangub City",
        "capital": "Tangub City",
        "lat": 8.0698,
        "lng": 123.7483,
    },
    {
        "id": 11,
        "name": "SDO Misamis Oriental",
        "capital": "Cagayan de Oro City",
        "lat": 8.478,
        "lng": 124.6341,
    },
    {
        "id": 12,
        "name": "SDO Cagayan de Oro City",
        "capital": "Cagayan de Oro City",
        "lat": 8.478,
        "lng": 124.6341,
    },
    {
        "id": 13,
        "name": "SDO Gingoog City",
        "capital": "Gingoog City",
        "lat": 8.7933,
        "lng": 125.124,
    },
    {
        "id": 14,
        "name": "SDO El Salvador City",
        "capital": "El Salvador City",
        "lat": 8.5622,
        "lng": 124.5508,
    },
]

# ─── SCHOOL NAME GENERATORS ───
SCHOOL_TYPES = ["Elementary", "Secondary", "Integrated"]
SCHOOL_PREFIXES = [
    "Central",
    "National",
    "Memorial",
    "Regional",
    "Provincial",
    "City",
    "North",
    "South",
    "East",
    "West",
    "San",
    "Santa",
    "Santo",
    "New",
    "Old",
    "Sto. Niño",
]
SCHOOL_SUFFIXES = [
    "Elementary School",
    "National High School",
    "Integrated School",
    "Central School",
]


def generate_school_name(division_name, school_type):
    if random.random() < 0.3:
        city = division_name.replace("SDO ", "").replace(" City", "")
        return f"{city} {random.choice(SCHOOL_SUFFIXES)}"
    return f"{random.choice(SCHOOL_PREFIXES)} {random.choice(SCHOOL_SUFFIXES)}"


def generate_coordinates(base_lat, base_lng, spread=0.15):
    lat = base_lat + (random.random() - 0.5) * spread * 2
    lng = base_lng + (random.random() - 0.5) * spread * 2
    return round(lat, 6), round(lng, 6)


def generate_enrollment():
    return random.randint(150, 2500)


def generate_assessment_date():
    days_ago = random.randint(1, 90)
    return (datetime.now() - timedelta(days=days_ago)).strftime("%Y-%m-%d")


def generate_sbm_scores(dimension_biases=None):
    scores = []
    for indicator in INDICATORS:
        dim_name = indicator["dimension"]
        dim_idx = (
            DIMENSION_NAMES.index(dim_name) if dim_name in DIMENSION_NAMES else 0
        )

        if dimension_biases and dim_idx < len(dimension_biases):
            base = dimension_biases[dim_idx]
            score = base + (random.random() - 0.5) * 0.8
        else:
            score = random.uniform(0.3, 2.9)

        score = round(max(0.0, min(3.0, score)), 1)
        scores.append(score)
    return scores


def get_degree_of_manifestation(score):
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
    if num_schools_per_division is None:
        num_schools_per_division = [random.randint(3, 8) for _ in SDO_DATA]

    all_schools = []
    all_assessments = []
    school_id_counter = 10000

    for idx, sdo in enumerate(SDO_DATA):
        num_schools = (
            num_schools_per_division[idx]
            if isinstance(num_schools_per_division, list)
            else num_schools_per_division
        )
        division_name = sdo["name"]

        dim_biases = []
        for d in range(len(DIMENSION_NAMES)):
            base = random.uniform(0.8, 2.8)
            if d == idx % len(DIMENSION_NAMES):
                base = min(3.0, base + 0.8)
            if d == (idx + 3) % len(DIMENSION_NAMES):
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

            if data_status == "Pending":
                scores = [""] * len(INDICATORS)
            else:
                scores = generate_sbm_scores(dim_biases)

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
                "School Head Name": f"Dr. {random.choice(['Juan', 'Maria', 'Jose', 'Ana'])} {random.choice(['Santos', 'Reyes', 'Cruz', 'Garcia'])}",
                "School Head Email": f"principal{school_id}@deped.gov.ph",
                "Urban/Rural": random.choice(["Urban", "Rural"]),
                "Last SBM Assessment": (
                    (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
                    if random.random() < 0.5
                    else ""
                ),
            }
            all_schools.append(school_info)

            for j, indicator in enumerate(INDICATORS):
                score = scores[j]
                is_complete = data_status == "Complete" and score != ""
                assessment = {
                    "School ID": school_id,
                    "Indicator ID": indicator["id"],
                    "Dimension": indicator["dimension"],
                    "Indicator Description": indicator["description"],
                    "Score": score if is_complete else "",
                    "Degree of Manifestation": (
                        get_degree_of_manifestation(score)
                        if is_complete
                        else ""
                    ),
                    "Remarks": (
                        "Needs improvement"
                        if is_complete and score < 1.5
                        else ""
                    ),
                    "Evidence/Supporting Docs": (
                        f"https://drive.google.com/file/d/{''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=15))}"
                        if is_complete and random.random() < 0.2
                        else ""
                    ),
                    "Date Assessed": assessment_date if is_complete else "",
                }
                all_assessments.append(assessment)

        school_id_counter += num_schools

    return pd.DataFrame(all_schools), pd.DataFrame(all_assessments)


def generate_mock_excel(filename="mock_sbm_data.xlsx"):
    school_df, assessment_df = generate_mock_data()

    with pd.ExcelWriter(filename, engine="openpyxl") as writer:
        school_df.to_excel(writer, sheet_name="School Information", index=False)
        assessment_df.to_excel(writer, sheet_name="SBM Assessment", index=False)

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
                worksheet.column_dimensions[column_letter].width = min(
                    max_length + 2, 80
                )

    print(f"✅ Mock file compiled and saved: '{filename}'")
    print(f"   ℹ️ Captured {len(school_df)} schools down to {len(assessment_df)} indicator data records.")


if __name__ == "__main__":
    generate_mock_excel()
