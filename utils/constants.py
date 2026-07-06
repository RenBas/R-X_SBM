"""Constant definitions for the SBM Dashboard."""

DIMENSION_NAMES = [
    "Curriculum & Teaching",
    "Learning Environment",
    "Leadership",
    "Governance & Accountability",
    "Human Resource & Team Dev.",
    "Finance & Resource Mgmt."
]

INDICATOR_MAPPING = {
    "Curriculum & Teaching": [1, 2, 3, 4, 5, 6, 7, 8],
    "Learning Environment": [9, 10, 11, 12, 13, 14, 15, 16, 17, 18],
    "Leadership": [19, 20, 21, 22],
    "Governance & Accountability": [23, 24, 25, 26],
    "Human Resource & Team Dev.": [27, 28, 29, 30, 31, 32, 33],
    "Finance & Resource Mgmt.": [34, 35, 36, 37, 38, 39, 40, 41, 42]
}

INDICATOR_DESCRIPTIONS = {
    1: "Grade 3 learners achieve proficiency in early literacy",
    2: "Grade 6/10/12 achieve proficiency in 21st-century skills & NAT",
    3: "School-based ALS learners attain certification as completers",
    4: "Teachers prepare contextualized learning materials",
    5: "Teachers conduct remediation activities for learning gaps",
    6: "Teachers integrate peace and DepEd core values topics",
    7: "School conducts test item analysis to inform teaching",
    8: "School engages local industries for TLE-TVL courses",
    9: "Zero bullying incidence",
    10: "Zero child abuse incidence",
    11: "Reduced drop-out incidence",
    12: "Conducts culture-sensitive activities",
    13: "Provides access to learning for disadvantaged, OSYs, adults",
    14: "Functional school-based ALS program",
    15: "Functional child-protection committee",
    16: "Functional DRRM plan",
    17: "Functional mental wellness support mechanism",
    18: "SPED- and PWD-friendly facilities",
    19: "Develops a strategic plan",
    20: "Functional school-community planning team",
    21: "Functional Supreme Student/Pupil Government",
    22: "Innovates in frontline service provision",
    23: "Strategic plan operationalized through implementation plan",
    24: "Functional School Governance Council (SGC)",
    25: "Functional Parent-Teacher Association (PTA)",
    26: "Collaborates with stakeholders and other schools",
    27: "Functional HR committee",
    28: "Teachers complete required professional development hours",
    29: "School head completes required professional development",
    30: "School conducts regular team-building activities",
    31: "School provides mentoring and coaching to teachers",
    32: "School conducts performance evaluations",
    33: "School recognizes personnel performance and contributions",
    34: "Functional School-Based Management (SBM) committee",
    35: "School develops an Annual Procurement Plan",
    36: "Inspects infrastructure and facilities",
    37: "Initiates improvement of infrastructure and facilities",
    38: "Functional library",
    39: "Functional water, electric, and internet facilities",
    40: "Functional computer laboratory/classroom",
    41: "Achieves 75–100% MOOE utilization rate",
    42: "Liquidates 100% of utilized MOOE"
}

# Color mapping for SBM degrees
DEGREE_COLORS = {
    "Always Manifested": "#22c55e",
    "Frequently Manifested": "#eab308",
    "Rarely Manifested": "#f97316",
    "Not Yet Manifested": "#9ca3af",
    "Pending": "#9ca3af"
}

# Shield color mapping for lowest dimension score
SHIELD_COLORS = {
    "high": "#0d9488",    # >= 2.5
    "medium_high": "#eab308",  # 2.0 - 2.4
    "medium_low": "#f97316",   # 1.0 - 1.9
    "low": "#dc2626"     # < 1.0
}
