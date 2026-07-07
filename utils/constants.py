"""Constant definitions for the SBM Dashboard."""

DIMENSION_NAMES = [
    "Curriculum & Teaching",
    "Learning Environment",
    "Leadership",
    "Governance & Accountability",
    "Human Resource & Team Dev.",
    "Finance & Resource Mgmt."
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

# Full 42 SBM Indicators (from DO No. 007, s. 2024)
INDICATORS = [
    {"id": 1, "dimension": "Curriculum & Teaching", "description": "Grade 3 learners achieve proficiency in early literacy, language, and numeracy"},
    {"id": 2, "dimension": "Curriculum & Teaching", "description": "Grade 6, 10, and 12 learners achieve proficiency in 21st-century skills & NAT"},
    {"id": 3, "dimension": "Curriculum & Teaching", "description": "School-based ALS learners attain certification as completers"},
    {"id": 4, "dimension": "Curriculum & Teaching", "description": "Teachers prepare contextualized learning materials"},
    {"id": 5, "dimension": "Curriculum & Teaching", "description": "Teachers conduct remediation activities for learning gaps"},
    {"id": 6, "dimension": "Curriculum & Teaching", "description": "Teachers integrate peace and DepEd core values topics"},
    {"id": 7, "dimension": "Curriculum & Teaching", "description": "School conducts test item analysis to inform teaching"},
    {"id": 8, "dimension": "Curriculum & Teaching", "description": "School engages local industries for TLE-TVL courses"},
    {"id": 9, "dimension": "Learning Environment", "description": "Zero bullying incidence"},
    {"id": 10, "dimension": "Learning Environment", "description": "Zero child abuse incidence"},
    {"id": 11, "dimension": "Learning Environment", "description": "Reduced drop-out incidence"},
    {"id": 12, "dimension": "Learning Environment", "description": "Conducts culture-sensitive activities"},
    {"id": 13, "dimension": "Learning Environment", "description": "Provides access to learning for disadvantaged, OSYs, adults"},
    {"id": 14, "dimension": "Learning Environment", "description": "Functional school-based ALS program"},
    {"id": 15, "dimension": "Learning Environment", "description": "Functional child-protection committee"},
    {"id": 16, "dimension": "Learning Environment", "description": "Functional DRRM plan"},
    {"id": 17, "dimension": "Learning Environment", "description": "Functional mental wellness support mechanism"},
    {"id": 18, "dimension": "Learning Environment", "description": "SPED- and PWD-friendly facilities"},
    {"id": 19, "dimension": "Leadership", "description": "Develops a strategic plan"},
    {"id": 20, "dimension": "Leadership", "description": "Functional school-community planning team"},
    {"id": 21, "dimension": "Leadership", "description": "Functional Supreme Student/Pupil Government"},
    {"id": 22, "dimension": "Leadership", "description": "Innovates in frontline service provision"},
    {"id": 23, "dimension": "Governance & Accountability", "description": "Strategic plan operationalized through implementation plan"},
    {"id": 24, "dimension": "Governance & Accountability", "description": "Functional School Governance Council (SGC)"},
    {"id": 25, "dimension": "Governance & Accountability", "description": "Functional Parent-Teacher Association (PTA)"},
    {"id": 26, "dimension": "Governance & Accountability", "description": "Collaborates with stakeholders and other schools"},
    {"id": 27, "dimension": "Human Resource & Team Dev.", "description": "Functional HR committee"},
    {"id": 28, "dimension": "Human Resource & Team Dev.", "description": "Teachers complete required professional development hours"},
    {"id": 29, "dimension": "Human Resource & Team Dev.", "description": "School head completes required professional development"},
    {"id": 30, "dimension": "Human Resource & Team Dev.", "description": "School conducts regular team-building activities"},
    {"id": 31, "dimension": "Human Resource & Team Dev.", "description": "School provides mentoring and coaching to teachers"},
    {"id": 32, "dimension": "Human Resource & Team Dev.", "description": "School conducts performance evaluations"},
    {"id": 33, "dimension": "Human Resource & Team Dev.", "description": "School recognizes personnel performance and contributions"},
    {"id": 34, "dimension": "Finance & Resource Mgmt.", "description": "Functional School-Based Management (SBM) committee"},
    {"id": 35, "dimension": "Finance & Resource Mgmt.", "description": "School develops an Annual Procurement Plan"},
    {"id": 36, "dimension": "Finance & Resource Mgmt.", "description": "Inspects infrastructure and facilities"},
    {"id": 37, "dimension": "Finance & Resource Mgmt.", "description": "Initiates improvement of infrastructure and facilities"},
    {"id": 38, "dimension": "Finance & Resource Mgmt.", "description": "Functional library"},
    {"id": 39, "dimension": "Finance & Resource Mgmt.", "description": "Functional water, electric, and internet facilities"},
    {"id": 40, "dimension": "Finance & Resource Mgmt.", "description": "Functional computer laboratory/classroom"},
    {"id": 41, "dimension": "Finance & Resource Mgmt.", "description": "Achieves 75–100% MOOE utilization rate"},
    {"id": 42, "dimension": "Finance & Resource Mgmt.", "description": "Liquidates 100% of utilized MOOE"}
]
