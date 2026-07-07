"""Synopsis generator for SBM Dashboard – creates narrative reports for decision-makers."""

import streamlit as st
from datetime import datetime
from utils.constants import DIMENSION_NAMES


def generate_synopsis(user_role, user_name, selected_sdo, schools_in_sdo, complete_schools, dim_avgs, overall_avg, max_dim_idx, min_dim_idx, is_dark_mode=False):
    """
    Generate a narrative synopsis based on the user's role and the data.
    Returns a formatted HTML string.
    """
    if not complete_schools:
        return _no_data_message(is_dark_mode)
    
    # Get dimension names
    strongest_dim = DIMENSION_NAMES[max_dim_idx]
    weakest_dim = DIMENSION_NAMES[min_dim_idx]
    strongest_score = dim_avgs[max_dim_idx]
    weakest_score = dim_avgs[min_dim_idx]
    total_schools = len(schools_in_sdo)
    pending_count = len(schools_in_sdo) - len(complete_schools)
    
    # Determine overall performance level
    if overall_avg >= 2.5:
        overall_level = "High"
        overall_color = "#22c55e"
        overall_emoji = "🟢"
    elif overall_avg >= 2.0:
        overall_level = "Medium-High"
        overall_color = "#eab308"
        overall_emoji = "🟡"
    elif overall_avg >= 1.0:
        overall_level = "Medium-Low"
        overall_color = "#f97316"
        overall_emoji = "🟠"
    else:
        overall_level = "Low"
        overall_color = "#dc2626"
        overall_emoji = "🔴"
    
    # Determine urgency level for weakest dimension
    if weakest_score < 1.0:
        urgency_level = "Critical"
        urgency_color = "#dc2626"
        urgency_emoji = "🔴"
    elif weakest_score < 2.0:
        urgency_level = "Warning"
        urgency_color = "#f97316"
        urgency_emoji = "🟠"
    elif weakest_score < 2.5:
        urgency_level = "Monitor"
        urgency_color = "#eab308"
        urgency_emoji = "🟡"
    else:
        urgency_level = "Stable"
        urgency_color = "#22c55e"
        urgency_emoji = "🟢"
    
    current_date = datetime.now().strftime('%B %d, %Y')
    
    # Generate role-specific content
    if user_role == "school":
        return _school_synopsis(
            user_name, selected_sdo, schools_in_sdo, complete_schools,
            strongest_dim, weakest_dim, strongest_score, weakest_score,
            overall_avg, overall_level, overall_color, overall_emoji,
            urgency_level, urgency_color, urgency_emoji, current_date,
            is_dark_mode
        )
    elif user_role == "division":
        return _division_synopsis(
            user_name, selected_sdo, schools_in_sdo, complete_schools,
            strongest_dim, weakest_dim, strongest_score, weakest_score,
            overall_avg, overall_level, overall_color, overall_emoji,
            urgency_level, urgency_color, urgency_emoji, total_schools, pending_count, current_date,
            is_dark_mode
        )
    elif user_role == "regional":
        return _regional_synopsis(
            user_name, selected_sdo, schools_in_sdo, complete_schools,
            strongest_dim, weakest_dim, strongest_score, weakest_score,
            overall_avg, overall_level, overall_color, overall_emoji,
            urgency_level, urgency_color, urgency_emoji, total_schools, pending_count, current_date,
            is_dark_mode
        )
    else:
        return _no_data_message(is_dark_mode)


def _get_theme_colors(is_dark_mode):
    """Return appropriate colors for light/dark mode."""
    if is_dark_mode:
        return {
            "bg_main": "#1A1C23",
            "bg_card": "#262730",
            "bg_strong": "#1A3A2A",   # dark green background
            "bg_weak": "#3A1A1A",      # dark red background
            "bg_analysis": "#1A1C23",
            "bg_interventions": "#2A2A1A",
            "bg_priority": "#1A2A3A",
            "text_main": "#FAFAFA",
            "text_secondary": "#B0B0B0",
            "text_muted": "#9CA3AF",
            "border_light": "#2A2C33",
            "border_strong": "#166534",
            "border_weak": "#991B1B",
            "gradient_start": "#1A1C23",
            "gradient_end": "#262730",
            "shadow": "rgba(255,255,255,0.05)"
        }
    else:
        return {
            "bg_main": "#FFFFFF",
            "bg_card": "#FFFFFF",
            "bg_strong": "#f0fdf4",   # light green
            "bg_weak": "#fef2f2",      # light red
            "bg_analysis": "#FFFFFF",
            "bg_interventions": "#fffbeb",
            "bg_priority": "#f0f4ff",
            "text_main": "#1A1A2E",
            "text_secondary": "#4B5563",
            "text_muted": "#6B7280",
            "border_light": "#E5E7EB",
            "border_strong": "#166534",
            "border_weak": "#991B1B",
            "gradient_start": "#f0f4ff",
            "gradient_end": "#e8eeff",
            "shadow": "rgba(0,0,0,0.05)"
        }


def _school_synopsis(user_name, selected_sdo, schools_in_sdo, complete_schools,
                     strongest_dim, weakest_dim, strongest_score, weakest_score,
                     overall_avg, overall_level, overall_color, overall_emoji,
                     urgency_level, urgency_color, urgency_emoji, current_date, is_dark_mode):
    """Synopsis for School Head level."""
    school = schools_in_sdo[0] if schools_in_sdo else None
    school_name = school["name"] if school else "Your School"
    colors = _get_theme_colors(is_dark_mode)
    
    html = f"""
    <div style="background:linear-gradient(135deg, {colors['gradient_start']} 0%, {colors['gradient_end']} 100%);padding:20px 24px;border-radius:12px;border-left:6px solid #0033A0;margin-bottom:20px;color:{colors['text_main']};box-shadow:0 2px 8px {colors['shadow']};">
        <h3 style="margin-top:0;color:#0033A0;">📋 Executive Summary: {school_name}</h3>
        <p style="font-size:14px;color:{colors['text_secondary']};margin-bottom:12px;">
            <b>Prepared for:</b> {user_name} · <b>Date:</b> {current_date}
        </p>
        
        <div style="background:{colors['bg_card']};padding:16px;border-radius:8px;margin:12px 0;border:1px solid {colors['border_light']};">
            <h4 style="margin-top:0;color:{colors['text_main']};">📊 Overall Performance: {overall_emoji} {overall_level}</h4>
            <p style="font-size:15px;margin-bottom:4px;color:{colors['text_main']};">
                <b>Overall SBM Index:</b> <span style="color:{overall_color};font-weight:700;">{overall_avg:.1f} / 3.0</span>
                <span style="font-size:13px;color:{colors['text_muted']};margin-left:12px;">({overall_level} performance)</span>
            </p>
        </div>
        
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;margin:12px 0;">
            <div style="background:{colors['bg_strong']};padding:14px;border-radius:8px;border-left:4px solid {colors['border_strong']};">
                <h4 style="margin:0 0 6px 0;font-size:14px;color:{colors['border_strong']};">✅ Strongest Dimension</h4>
                <p style="font-size:16px;font-weight:700;margin:0;color:{colors['border_strong']};">{strongest_dim}</p>
                <p style="font-size:13px;margin:4px 0 0 0;color:{colors['text_secondary']};">Score: <b>{strongest_score:.1f}</b> / 3.0</p>
            </div>
            <div style="background:{colors['bg_weak']};padding:14px;border-radius:8px;border-left:4px solid {colors['border_weak']};">
                <h4 style="margin:0 0 6px 0;font-size:14px;color:{colors['border_weak']};">⚠️ Weakest Dimension</h4>
                <p style="font-size:16px;font-weight:700;margin:0;color:{colors['border_weak']};">{weakest_dim}</p>
                <p style="font-size:13px;margin:4px 0 0 0;color:{colors['text_secondary']};">Score: <b>{weakest_score:.1f}</b> / 3.0</p>
            </div>
        </div>
        
        <div style="background:{colors['bg_analysis']};padding:16px;border-radius:8px;margin:12px 0;border:1px solid {colors['border_light']};">
            <h4 style="margin-top:0;color:{colors['text_main']};">💡 Analysis</h4>
            <p style="font-size:14px;color:{colors['text_secondary']};">
                <b>{weakest_dim}</b> is the weakest dimension. This area requires immediate attention and targeted interventions.
                <br><br>
                <b>{strongest_dim}</b> is the strongest dimension. Continue current practices and use this as a model for other areas.
            </p>
        </div>
        
        <div style="background:{colors['bg_interventions']};padding:16px;border-radius:8px;border:1px solid #fcd34d;margin:12px 0;">
            <h4 style="margin-top:0;color:#92400e;">🎯 Recommended Interventions</h4>
            <ul style="font-size:13px;color:{colors['text_secondary']};padding-left:20px;margin:4px 0;">
                <li><b>Immediate:</b> Conduct focused assessment and capacity building for {weakest_dim}.</li>
                <li><b>Short-Term:</b> Develop an improvement plan with specific, measurable targets.</li>
                <li><b>Medium-Term:</b> Implement interventions and monitor progress regularly.</li>
                <li><b>Sustain:</b> Maintain and enhance performance in {strongest_dim}.</li>
            </ul>
        </div>
        
        <p style="font-size:12px;color:{colors['text_muted']};margin-top:12px;text-align:right;">
            <i>Based on current SBM self-assessment data. For school-level planning and decision-making.</i>
        </p>
    </div>
    """
    return html


def _division_synopsis(user_name, selected_sdo, schools_in_sdo, complete_schools,
                       strongest_dim, weakest_dim, strongest_score, weakest_score,
                       overall_avg, overall_level, overall_color, overall_emoji,
                       urgency_level, urgency_color, urgency_emoji, total_schools, pending_count, current_date, is_dark_mode):
    """Synopsis for Division level."""
    colors = _get_theme_colors(is_dark_mode)
    
    html = f"""
    <div style="background:linear-gradient(135deg, {colors['gradient_start']} 0%, {colors['gradient_end']} 100%);padding:20px 24px;border-radius:12px;border-left:6px solid #0033A0;margin-bottom:20px;color:{colors['text_main']};box-shadow:0 2px 8px {colors['shadow']};">
        <h3 style="margin-top:0;color:#0033A0;">📋 Division Executive Summary</h3>
        <p style="font-size:14px;color:{colors['text_secondary']};margin-bottom:12px;">
            <b>Prepared for:</b> {user_name} · <b>Division:</b> {selected_sdo['name']} · <b>Date:</b> {current_date}
        </p>
        
        <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;margin:12px 0;">
            <div style="background:{colors['bg_card']};padding:12px;border-radius:8px;text-align:center;border:1px solid {colors['border_light']};">
                <div style="font-size:24px;font-weight:700;color:{colors['text_main']};">{total_schools}</div>
                <div style="font-size:12px;color:{colors['text_muted']};">Total Schools</div>
            </div>
            <div style="background:{colors['bg_card']};padding:12px;border-radius:8px;text-align:center;border:1px solid {colors['border_light']};">
                <div style="font-size:24px;font-weight:700;color:{overall_color};">{overall_avg:.1f}</div>
                <div style="font-size:12px;color:{colors['text_muted']};">Division SBM Index</div>
                <div style="font-size:11px;color:{overall_color};">{overall_level}</div>
            </div>
            <div style="background:{colors['bg_card']};padding:12px;border-radius:8px;text-align:center;border:1px solid {colors['border_light']};">
                <div style="font-size:24px;font-weight:700;color:{urgency_color};">{pending_count}</div>
                <div style="font-size:12px;color:{colors['text_muted']};">Schools with Pending Data</div>
            </div>
        </div>
        
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;margin:12px 0;">
            <div style="background:{colors['bg_strong']};padding:14px;border-radius:8px;border-left:4px solid {colors['border_strong']};">
                <h4 style="margin:0 0 6px 0;font-size:14px;color:{colors['border_strong']};">✅ Strongest Dimension</h4>
                <p style="font-size:16px;font-weight:700;margin:0;color:{colors['border_strong']};">{strongest_dim}</p>
                <p style="font-size:13px;margin:4px 0 0 0;color:{colors['text_secondary']};">Division Average: <b>{strongest_score:.1f}</b> / 3.0</p>
            </div>
            <div style="background:{colors['bg_weak']};padding:14px;border-radius:8px;border-left:4px solid {colors['border_weak']};">
                <h4 style="margin:0 0 6px 0;font-size:14px;color:{colors['border_weak']};">⚠️ Weakest Dimension</h4>
                <p style="font-size:16px;font-weight:700;margin:0;color:{colors['border_weak']};">{weakest_dim}</p>
                <p style="font-size:13px;margin:4px 0 0 0;color:{colors['text_secondary']};">Division Average: <b>{weakest_score:.1f}</b> / 3.0</p>
            </div>
        </div>
        
        <div style="background:{colors['bg_analysis']};padding:16px;border-radius:8px;margin:12px 0;border:1px solid {colors['border_light']};">
            <h4 style="margin-top:0;color:{colors['text_main']};">💡 Analysis</h4>
            <p style="font-size:14px;color:{colors['text_secondary']};">
                <b>{weakest_dim}</b> is the weakest dimension across the division. This requires division-wide attention and coordinated support.
                <br><br>
                <b>{strongest_dim}</b> is the division's strength. Document and share best practices across schools.
            </p>
        </div>
        
        <div style="background:{colors['bg_interventions']};padding:16px;border-radius:8px;border:1px solid #fcd34d;margin:12px 0;">
            <h4 style="margin-top:0;color:#92400e;">🎯 Recommended Interventions</h4>
            <ul style="font-size:13px;color:{colors['text_secondary']};padding-left:20px;margin:4px 0;">
                <li><b>Urgent:</b> Deploy division TA team to schools struggling with {weakest_dim}.</li>
                <li><b>Short-Term:</b> Conduct division-wide training for {weakest_dim}.</li>
                <li><b>Medium-Term:</b> Establish regular monitoring and reporting mechanisms.</li>
                <li><b>Sustain:</b> Scale up best practices from {strongest_dim} across all schools.</li>
            </ul>
        </div>
        
        <div style="background:{colors['bg_priority']};padding:12px;border-radius:8px;border:1px solid #93c5fd;margin:12px 0;">
            <h4 style="margin-top:0;color:#1e40af;font-size:14px;">📌 Priority Action Items</h4>
            <ul style="font-size:13px;color:{colors['text_secondary']};padding-left:20px;margin:4px 0;">
                <li><b>0-3 Months:</b> Address {weakest_dim} with targeted TA and capacity building.</li>
                <li><b>3-6 Months:</b> Strengthen monitoring and evaluation systems.</li>
                <li><b>6-12 Months:</b> Scale up best practices across the division.</li>
            </ul>
        </div>
        
        <p style="font-size:12px;color:{colors['text_muted']};margin-top:12px;text-align:right;">
            <i>Based on current SBM data. For division-level planning and decision-making.</i>
        </p>
    </div>
    """
    return html


def _regional_synopsis(user_name, selected_sdo, schools_in_sdo, complete_schools,
                       strongest_dim, weakest_dim, strongest_score, weakest_score,
                       overall_avg, overall_level, overall_color, overall_emoji,
                       urgency_level, urgency_color, urgency_emoji, total_schools, pending_count, current_date, is_dark_mode):
    """Synopsis for Regional level."""
    colors = _get_theme_colors(is_dark_mode)
    
    html = f"""
    <div style="background:linear-gradient(135deg, {colors['gradient_start']} 0%, {colors['gradient_end']} 100%);padding:20px 24px;border-radius:12px;border-left:6px solid #0033A0;margin-bottom:20px;color:{colors['text_main']};box-shadow:0 2px 8px {colors['shadow']};">
        <h3 style="margin-top:0;color:#0033A0;">📋 Regional Executive Summary</h3>
        <p style="font-size:14px;color:{colors['text_secondary']};margin-bottom:12px;">
            <b>Prepared for:</b> {user_name} · <b>Region:</b> X – Northern Mindanao · <b>Date:</b> {current_date}
        </p>
        
        <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;margin:12px 0;">
            <div style="background:{colors['bg_card']};padding:12px;border-radius:8px;text-align:center;border:1px solid {colors['border_light']};">
                <div style="font-size:24px;font-weight:700;color:{colors['text_main']};">14</div>
                <div style="font-size:12px;color:{colors['text_muted']};">Total Divisions</div>
            </div>
            <div style="background:{colors['bg_card']};padding:12px;border-radius:8px;text-align:center;border:1px solid {colors['border_light']};">
                <div style="font-size:24px;font-weight:700;color:{overall_color};">{overall_avg:.1f}</div>
                <div style="font-size:12px;color:{colors['text_muted']};">Division SBM Index</div>
                <div style="font-size:11px;color:{overall_color};">{overall_level}</div>
            </div>
            <div style="background:{colors['bg_card']};padding:12px;border-radius:8px;text-align:center;border:1px solid {colors['border_light']};">
                <div style="font-size:24px;font-weight:700;color:{urgency_color};">{urgency_level}</div>
                <div style="font-size:12px;color:{colors['text_muted']};">Urgency Level</div>
                <div style="font-size:11px;color:{urgency_color};">{urgency_emoji} {weakest_dim} ({weakest_score:.1f})</div>
            </div>
        </div>
        
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;margin:12px 0;">
            <div style="background:{colors['bg_strong']};padding:14px;border-radius:8px;border-left:4px solid {colors['border_strong']};">
                <h4 style="margin:0 0 6px 0;font-size:14px;color:{colors['border_strong']};">✅ Regional Strength</h4>
                <p style="font-size:16px;font-weight:700;margin:0;color:{colors['border_strong']};">{strongest_dim}</p>
                <p style="font-size:13px;margin:4px 0 0 0;color:{colors['text_secondary']};">Regional Average: <b>{strongest_score:.1f}</b> / 3.0</p>
            </div>
            <div style="background:{colors['bg_weak']};padding:14px;border-radius:8px;border-left:4px solid {colors['border_weak']};">
                <h4 style="margin:0 0 6px 0;font-size:14px;color:{colors['border_weak']};">⚠️ Critical Priority</h4>
                <p style="font-size:16px;font-weight:700;margin:0;color:{colors['border_weak']};">{weakest_dim}</p>
                <p style="font-size:13px;margin:4px 0 0 0;color:{colors['text_secondary']};">Regional Average: <b>{weakest_score:.1f}</b> / 3.0</p>
            </div>
        </div>
        
        <div style="background:{colors['bg_analysis']};padding:16px;border-radius:8px;margin:12px 0;border:1px solid {colors['border_light']};">
            <h4 style="margin-top:0;color:{colors['text_main']};">💡 Strategic Analysis</h4>
            <p style="font-size:14px;color:{colors['text_secondary']};">
                <b>{weakest_dim}</b> is the weakest dimension regionally. This requires urgent regional-level intervention and coordinated support across divisions.
                <br><br>
                <b>{strongest_dim}</b> is the region's strength. Document and share best practices across all divisions.
            </p>
        </div>
        
        <div style="background:{colors['bg_interventions']};padding:16px;border-radius:8px;border:1px solid #fcd34d;margin:12px 0;">
            <h4 style="margin-top:0;color:#92400e;">🎯 Regional Strategic Interventions</h4>
            <ul style="font-size:13px;color:{colors['text_secondary']};padding-left:20px;margin:4px 0;">
                <li><b>Short-Term (0-6 Months):</b> Deploy Regional Field Technical Assistance Team (RFTAT) to priority divisions.</li>
                <li><b>Medium-Term (6-12 Months):</b> Establish Regional SBM Monitoring and Evaluation System.</li>
                <li><b>Long-Term (12+ Months):</b> Integrate SBM improvement into Regional Education Development Plan.</li>
            </ul>
        </div>
        
        <div style="background:{colors['bg_priority']};padding:12px;border-radius:8px;border:1px solid #93c5fd;margin:12px 0;">
            <h4 style="margin-top:0;color:#1e40af;font-size:14px;">📌 Policy Recommendations</h4>
            <ul style="font-size:13px;color:{colors['text_secondary']};padding-left:20px;margin:4px 0;">
                <li><b>Immediate:</b> Prioritize {weakest_dim} in regional planning and resource allocation.</li>
                <li><b>Short-Term:</b> Develop region-wide capacity building programs for {weakest_dim}.</li>
                <li><b>Long-Term:</b> Build sustainable systems for continuous improvement across all dimensions.</li>
            </ul>
        </div>
        
        <p style="font-size:12px;color:{colors['text_muted']};margin-top:12px;text-align:right;">
            <i>Based on current SBM data. For regional-level strategic planning and decision-making.</i>
        </p>
    </div>
    """
    return html


def _no_data_message(is_dark_mode):
    """Return message when no data is available."""
    if is_dark_mode:
        return """
        <div style="background:#1A1C23;padding:20px;border-radius:12px;border-left:6px solid #f59e0b;margin-bottom:20px;color:#FAFAFA;">
            <h4 style="margin-top:0;color:#f59e0b;">ℹ️ No Data Available</h4>
            <p style="color:#B0B0B0;font-size:14px;">
                There is currently no complete SBM data available for your role or selected division. 
                Please ensure that schools have submitted their SBM self-assessment data.
            </p>
        </div>
        """
    else:
        return """
        <div style="background:#fef3c7;padding:20px;border-radius:12px;border-left:6px solid #f59e0b;margin-bottom:20px;">
            <h4 style="margin-top:0;color:#92400e;">ℹ️ No Data Available</h4>
            <p style="color:#4b5563;font-size:14px;">
                There is currently no complete SBM data available for your role or selected division. 
                Please ensure that schools have submitted their SBM self-assessment data.
            </p>
        </div>
        """
