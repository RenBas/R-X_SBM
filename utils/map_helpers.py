"""Helper functions for creating Folium map elements."""

import folium
from branca.element import Element
from .constants import DIMENSION_NAMES, SHIELD_COLORS, DEGREE_COLORS

def get_shield_color(score):
    """Return shield color based on lowest dimension score."""
    if score >= 2.5:
        return SHIELD_COLORS["high"]
    elif score >= 2.0:
        return SHIELD_COLORS["medium_high"]
    elif score >= 1.0:
        return SHIELD_COLORS["medium_low"]
    else:
        return SHIELD_COLORS["low"]

def get_school_dot_color(degree):
    """Return dot color based on SBM degree."""
    return DEGREE_COLORS.get(degree, "#9ca3af")

def get_school_dot_size(enrollment):
    """Return dot size based on enrollment."""
    if enrollment == 0:
        return 8
    elif enrollment < 500:
        return 10
    elif enrollment < 1500:
        return 14
    else:
        return 18

def create_shield_html(sdo):
    """Generate HTML for an SDO shield with pulse animation."""
    color = get_shield_color(sdo["lowest_dim_score"])
    urgency = sdo["urgency_factor"]
    duration = 0.6 + (1 - urgency) * 1.4  # 0.6s (critical) to 2.0s (stable)
    glow_size = 10 + urgency * 30
    glow_opacity = 0.2 + urgency * 0.6
    
    border_color = "#dc2626" if sdo["lowest_dim_score"] < 1.0 else (
        "#f97316" if sdo["lowest_dim_score"] < 2.0 else "rgba(255,255,255,0.4)"
    )
    
    # Shorten name for display on shield
    short_name = sdo["name"].replace("SDO ", "").split(" ")[:2]
    display_name = " ".join(short_name)
    
    html = f'''
    <div style="position:relative;width:44px;height:44px;display:flex;align-items:center;justify-content:center;">
        <!-- Glow layer -->
        <div style="position:absolute;width:{glow_size+30}px;height:{glow_size+30}px;border-radius:50%;
                    background:radial-gradient(circle, {color}66, transparent 70%);
                    animation: pulseGlow {duration}s ease-in-out infinite alternate;
                    pointer-events:none;z-index:0;">
        </div>
        <!-- Shield -->
        <div style="position:relative;z-index:1;width:44px;height:44px;
                    background:{color};
                    clip-path:polygon(50% 0%, 100% 20%, 90% 80%, 50% 100%, 10% 80%, 0% 20%);
                    display:flex;align-items:center;justify-content:center;
                    border:2px solid {border_color};
                    box-shadow:0 2px 8px rgba(0,0,0,0.2);
                    font-weight:700;font-size:10px;color:#fff;text-align:center;
                    text-shadow:0 1px 3px rgba(0,0,0,0.3);
                    line-height:1.1;padding:2px;">
            {display_name}
        </div>
    '''
    
    # Add ⚠ badge if score < 2.0
    if sdo["lowest_dim_score"] < 2.0:
        badge_duration = max(0.8, duration * 0.7)
        html += f'''
        <div style="position:absolute;top:-6px;right:-8px;z-index:2;
                    background:#dc2626;color:#fff;border-radius:50%;
                    width:18px;height:18px;font-size:10px;
                    display:flex;align-items:center;justify-content:center;
                    font-weight:700;border:2px solid #fff;
                    animation: badgePulse {badge_duration}s ease-in-out infinite alternate;">
            ⚠
        </div>
        '''
    
    # Add alert border if score < 1.0
    if sdo["lowest_dim_score"] < 1.0:
        html += '''
        <div style="position:absolute;inset:-4px;z-index:0;
                    border:2px dashed #dc2626;border-radius:8px;
                    animation: alertBorder 0.8s ease-in-out infinite alternate;
                    pointer-events:none;">
        </div>
        '''
    
    html += '</div>'
    return html

def create_school_dot_html(school):
    """Generate HTML for a school dot."""
    is_pending = school["data_status"] == "Pending"
    color = get_school_dot_color(school["degree"])
    size = get_school_dot_size(school["enrollment"])
    
    if is_pending:
        html = f'''
        <div style="width:{size}px;height:{size}px;border-radius:50%;
                    background:repeating-linear-gradient(45deg, #9ca3af, #9ca3af 3px, #d1d5db 3px, #d1d5db 6px);
                    border:2px solid #6b7280;box-shadow:0 1px 4px rgba(0,0,0,0.15);">
        </div>
        '''
    else:
        html = f'''
        <div style="width:{size}px;height:{size}px;border-radius:50%;
                    background:{color};border:2px solid rgba(255,255,255,0.8);
                    box-shadow:0 2px 6px rgba(0,0,0,0.2);">
        </div>
        '''
    
    return html

def get_pulse_css():
    """Return CSS keyframes for pulse animations."""
    return '''
    <style>
        @keyframes pulseGlow {
            0% { transform: scale(1); opacity: 0.6; }
            100% { transform: scale(1.4); opacity: 1; }
        }
        @keyframes badgePulse {
            0% { transform: scale(1); }
            100% { transform: scale(1.2); }
        }
        @keyframes alertBorder {
            0% { opacity: 0.3; transform: rotate(0deg) scale(1); }
            100% { opacity: 1; transform: rotate(4deg) scale(1.05); }
        }
    </style>
    '''

def get_sdo_popup_html(sdo):
    """Generate popup content for an SDO shield."""
    return f'''
    <div style="font-weight:600;font-size:15px;">{sdo["name"]}</div>
    <div style="font-size:12px;color:#4b5563;">{sdo["capital"]}</div>
    <hr style="margin:4px 0;">
    <div style="font-size:13px;">
        <b>Overall Index:</b> {sdo["overall_index"]:.1f} / 3.0<br>
        <b>Lowest Dimension:</b> {sdo["lowest_dim_name"]} ({sdo["lowest_dim_score"]:.1f})<br>
        <span style="color:#6b7280;font-size:11px;">Click to zoom in</span>
    </div>
    '''

def get_school_popup_html(school):
    """Generate popup content for a school dot."""
    if school["data_status"] == "Pending":
        return f'''
        <div style="font-weight:600;font-size:14px;">{school["name"]}</div>
        <div style="font-size:12px;color:#4b5563;">{school["type"]} · ⏳ Data Pending</div>
        <hr style="margin:4px 0;">
        <div style="color:#6b7280;font-size:13px;">No SBM assessment submitted yet.</div>
        '''
    
    return f'''
    <div style="font-weight:600;font-size:14px;">{school["name"]}</div>
    <div style="font-size:12px;color:#4b5563;">{school["type"]} · {school["enrollment"]:,} learners</div>
    <hr style="margin:4px 0;">
    <div style="font-size:13px;">
        <b>SBM Level:</b> {school["degree"]}<br>
        <b>Overall Index:</b> {school["overall_index"]:.1f} / 3.0<br>
        <b>Lowest Dim:</b> {DIMENSION_NAMES[school["lowest_dim_index"]]} ({school["lowest_dim_score"]:.1f})
    </div>
    '''
