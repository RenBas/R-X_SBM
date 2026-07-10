"""Utilities package for SBM Dashboard."""

from .constants import DIMENSION_NAMES, SHIELD_COLORS, DEGREE_COLORS
from .data_loader import (
    load_sdo_data,
    load_all_schools,
    get_schools_by_sdo,
    compute_dimension_averages
)
from .map_helpers import add_sdo_shield, add_school_dot
from .chart_helpers import (
    create_radar_chart,
    create_trend_chart,
    create_indicators_table,
    render_school_dashboard
)
from .auth import (
    authenticate,
    login_status,
    logout,
    get_accessible_schools,
    get_accessible_divisions_summary,
    is_school_head
)
from .download_helpers import generate_report_data, generate_excel_template
from .export_helpers import generate_excel_report, generate_pdf_report
from .synopsis_generator import generate_synopsis
from .twin_ui import render_sandbox
