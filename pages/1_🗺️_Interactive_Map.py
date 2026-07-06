import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration
st.set_page_config(page_title="Region X SBM Map", layout="wide", page_icon="🗺️")

st.title("🗺️ Interactive SBM Geospatial Map: Northern Mindanao (Region X)")
st.caption("Visualizing the 'Community of Schools' and SBM Manifestation. Select a Division to drill down.")

# 2. Load the Data
@st.cache_data
def load_data():
    # Load the CSV from the data folder
    df = pd.read_csv("data/region_x_sbm_data.csv")
    return df

df = load_data()

# 3. Create the Sidebar for Drill-Down
st.sidebar.header("📍 Drill-Down Controls")

# Get unique divisions and add an "All" option
divisions = ["All Region X"] + sorted(df[df['Type'] == 'SDO']['Division'].unique().tolist())

selected_division = st.sidebar.selectbox(
    "Select School Division Office (SDO):",
    divisions,
    help="Select a division to zoom in and view individual schools."
)

# 4. Filter Data based on Selection
if selected_division == "All Region X":
    map_data = df
    map_title = "Northern Mindanao (Region X) - All Divisions"
    zoom_level = 7
else:
    # Filter to show only the selected division's SDO and its schools
    map_data = df[df['Division'] == selected_division]
    map_title = f"Drill-Down: {selected_division} Division"
    zoom_level = 10 # Zoom in closer when a specific division is selected

# 5. Define Colors for SBM Status (Mapped to DO 007 Terminology)
color_discrete_map = {
    "Always Manifested": "#2ca02c",    # Green
    "Frequently Manifested": "#ff7f0e", # Orange
    "Rarely Manifested": "#d62728",     # Red
    "Not Yet Manifested": "#7f7f7f"     # Gray
}

# 6. Create the Plotly Map
# We use open-street-map style so you don't need a Mapbox API token
fig = px.scatter_mapbox(
    map_data,
    lat="Latitude",
    lon="Longitude",
    hover_name="School_Name",
    hover_data={
        "Division": True,
        "SBM_Status": True,
        "Key_Indicator_Gap": True,
        "Latitude": False,
        "Longitude": False,
        "Type": False
    },
    color="SBM_Status",
    color_discrete_map=color_discrete_map,
    size_max=15,
    zoom=zoom_level,
    mapbox_style="open-street-map",
    title=map_title
)

# Update layout for better UI
fig.update_layout(
    margin={"r":0,"t":40,"l":0,"b":0},
    hoverlabel_bgcolor="#2E4053",
    hoverlabel_font_color="#FFFFFF"
)

# 7. Render in Streamlit
st.plotly_chart(fig, use_container_width=True)

# 8. Add a Data Table below the map for detailed viewing
st.divider()
st.subheader(f"📋 SBM Status Details: {selected_division}")

if selected_division == "All Region X":
    st.dataframe(df[df['Type'] == 'SDO'][['Division', 'SBM_Status', 'Key_Indicator_Gap']], use_container_width=True)
else:
    st.dataframe(map_data[map_data['Type'] == 'School'][['School_Name', 'SBM_Status', 'Key_Indicator_Gap']], use_container_width=True)

st.info("💡 **Policy Link (DO 007, s. 2024):** This map operationalizes Section III.2 (Community of schools/cluster). By hovering over the red/gray dots, the SDO can instantly identify schools with specific indicator gaps (e.g., Indicator 39: Internet) to deploy the Division Field Technical Assistance Team (DFTAT) equitably and contextually.")
