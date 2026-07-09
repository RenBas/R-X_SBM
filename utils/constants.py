"""Constant definitions for the SBM Dashboard."""

DIMENSION_NAMES = [
    "Leadership and Governance",
    "Curriculum and Instruction",
    "Learning Environment",
    "Accountability and Continuous Improvement",
    "Management of Resources",
    "Finance & Resource Management"
]

DEGREE_COLORS = {
    "Always Manifested": "#22c55e",
    "Frequently Manifested": "#eab308",
    "Rarely Manifested": "#f97316",
    "Not Yet Manifested": "#9ca3af",
    "Pending": "#9ca3af"
}

SHIELD_COLORS = {
    "high": "#0d9488",      # >= 2.5
    "medium_high": "#eab308",  # 2.0 - 2.4
    "medium_low": "#f97316",   # 1.0 - 1.9
    "low": "#dc2626"        # < 1.0
}

# Full 42 SBM Indicators (from DO No. 007, s. 2024) - Updated to match new dimension names
INDICATORS = [
    {"id": 1, "dimension": "Leadership and Governance", "description": "Development plan collaboratively developed by stakeholders"},
    {"id": 2, "dimension": "Leadership and Governance", "description": "Leadership network facilitates data-driven decisions"},
    {"id": 3, "dimension": "Leadership and Governance", "description": "School head demonstrates transformational leadership"},
    {"id": 4, "dimension": "Leadership and Governance", "description": "Functional school governance structures"},
    {"id": 5, "dimension": "Leadership and Governance", "description": "Strategic planning and implementation"},
    {"id": 6, "dimension": "Leadership and Governance", "description": "Stakeholder engagement and partnership"},
    {"id": 7, "dimension": "Leadership and Governance", "description": "Resource mobilization and management"},
    {"id": 8, "dimension": "Curriculum and Instruction", "description": "Grade 3 learners achieve proficiency in early literacy and numeracy"},
    {"id": 9, "dimension": "Curriculum and Instruction", "description": "Grade 6, 10, and 12 learners achieve proficiency in 21st-century skills"},
    {"id": 10, "dimension": "Curriculum and Instruction", "description": "School-based ALS learners attain certification"},
    {"id": 11, "dimension": "Curriculum and Instruction", "description": "Teachers prepare contextualized learning materials"},
    {"id": 12, "dimension": "Curriculum and Instruction", "description": "Teachers conduct remediation activities"},
    {"id": 13, "dimension": "Curriculum and Instruction", "description": "Teachers integrate peace and DepEd core values"},
    {"id": 14, "dimension": "Curriculum and Instruction", "description": "School conducts test item analysis"},
    {"id": 15, "dimension": "Curriculum and Instruction", "description": "School engages local industries for TLE-TVL"},
    {"id": 16, "dimension": "Learning Environment", "description": "Zero bullying incidence"},
    {"id": 17, "dimension": "Learning Environment", "description": "Zero child abuse incidence"},
    {"id": 18, "dimension": "Learning Environment", "description": "Reduced drop-out incidence"},
    {"id": 19, "dimension": "Learning Environment", "description": "Conducts culture-sensitive activities"},
    {"id": 20, "dimension": "Learning Environment", "description": "Provides access to learning for disadvantaged learners"},
    {"id": 21, "dimension": "Learning Environment", "description": "Functional school-based ALS program"},
    {"id": 22, "dimension": "Learning Environment", "description": "Functional child-protection committee"},
    {"id": 23, "dimension": "Learning Environment", "description": "Functional DRRM plan"},
    {"id": 24, "dimension": "Learning Environment", "description": "Functional mental wellness support mechanism"},
    {"id": 25, "dimension": "Learning Environment", "description": "SPED- and PWD-friendly facilities"},
    {"id": 26, "dimension": "Accountability and Continuous Improvement", "description": "Roles and responsibilities clearly defined"},
    {"id": 27, "dimension": "Accountability and Continuous Improvement", "description": "Performance monitoring and evaluation system"},
    {"id": 28, "dimension": "Accountability and Continuous Improvement", "description": "Data-driven decision making processes"},
    {"id": 29, "dimension": "Accountability and Continuous Improvement", "description": "Continuous improvement planning"},
    {"id": 30, "dimension": "Accountability and Continuous Improvement", "description": "Quality assurance mechanisms"},
    {"id": 31, "dimension": "Management of Resources", "description": "Regular resource inventory"},
    {"id": 32, "dimension": "Management of Resources", "description": "Efficient resource allocation"},
    {"id": 33, "dimension": "Management of Resources", "description": "Maintenance of facilities and equipment"},
    {"id": 34, "dimension": "Management of Resources", "description": "Technology integration in operations"},
    {"id": 35, "dimension": "Finance & Resource Management", "description": "Functional SBM committee"},
    {"id": 36, "dimension": "Finance & Resource Management", "description": "Annual Procurement Plan developed"},
    {"id": 37, "dimension": "Finance & Resource Management", "description": "Infrastructure inspection conducted"},
    {"id": 38, "dimension": "Finance & Resource Management", "description": "Facility improvement initiatives"},
    {"id": 39, "dimension": "Finance & Resource Management", "description": "Functional library"},
    {"id": 40, "dimension": "Finance & Resource Management", "description": "Functional water, electric, and internet facilities"},
    {"id": 41, "dimension": "Finance & Resource Management", "description": "Functional computer laboratory"},
    {"id": 42, "dimension": "Finance & Resource Management", "description": "MOOE utilization and liquidation"}
]
