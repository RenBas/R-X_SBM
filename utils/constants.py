"""Constant definitions for the SBM Dashboard."""

DIMENSION_NAMES = [
    "Leadership & Governance",
    "Curriculum & Instruction",
    "Learning Environment",
    "Accountability & Continuous Improvement",
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

# Full 30 SBM Indicators (6 dimensions x 5 indicators each) - Updated to match actual data file
INDICATORS = [
    {"id": "LG_Indicator1", "dimension": "Leadership & Governance"},
    {"id": "LG_Indicator2", "dimension": "Leadership & Governance"},
    {"id": "LG_Indicator3", "dimension": "Leadership & Governance"},
    {"id": "LG_Indicator4", "dimension": "Leadership & Governance"},
    {"id": "LG_Indicator5", "dimension": "Leadership & Governance"},
    {"id": "CI_Indicator1", "dimension": "Curriculum & Instruction"},
    {"id": "CI_Indicator2", "dimension": "Curriculum & Instruction"},
    {"id": "CI_Indicator3", "dimension": "Curriculum & Instruction"},
    {"id": "CI_Indicator4", "dimension": "Curriculum & Instruction"},
    {"id": "CI_Indicator5", "dimension": "Curriculum & Instruction"},
    {"id": "LE_Indicator1", "dimension": "Learning Environment"},
    {"id": "LE_Indicator2", "dimension": "Learning Environment"},
    {"id": "LE_Indicator3", "dimension": "Learning Environment"},
    {"id": "LE_Indicator4", "dimension": "Learning Environment"},
    {"id": "LE_Indicator5", "dimension": "Learning Environment"},
    {"id": "AC_Indicator1", "dimension": "Accountability & Continuous Improvement"},
    {"id": "AC_Indicator2", "dimension": "Accountability & Continuous Improvement"},
    {"id": "AC_Indicator3", "dimension": "Accountability & Continuous Improvement"},
    {"id": "AC_Indicator4", "dimension": "Accountability & Continuous Improvement"},
    {"id": "AC_Indicator5", "dimension": "Accountability & Continuous Improvement"},
    {"id": "MR_Indicator1", "dimension": "Management of Resources"},
    {"id": "MR_Indicator2", "dimension": "Management of Resources"},
    {"id": "MR_Indicator3", "dimension": "Management of Resources"},
    {"id": "MR_Indicator4", "dimension": "Management of Resources"},
    {"id": "MR_Indicator5", "dimension": "Management of Resources"},
    {"id": "FR_Indicator1", "dimension": "Finance & Resource Management"},
    {"id": "FR_Indicator2", "dimension": "Finance & Resource Management"},
    {"id": "FR_Indicator3", "dimension": "Finance & Resource Management"},
    {"id": "FR_Indicator4", "dimension": "Finance & Resource Management"},
    {"id": "FR_Indicator5", "dimension": "Finance & Resource Management"},
]
