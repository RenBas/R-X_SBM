"""Test script to diagnose import issues."""

print("Step 1: Starting import test...")

try:
    print("Step 2: Importing constants...")
    from utils.constants import DIMENSION_NAMES, SHIELD_COLORS, DEGREE_COLORS
    print("✅ constants imported successfully.")
except Exception as e:
    print(f"❌ constants import failed: {e}")
    import traceback
    traceback.print_exc()

try:
    print("Step 3: Importing folium...")
    import folium
    print("✅ folium imported successfully.")
except Exception as e:
    print(f"❌ folium import failed: {e}")
    import traceback
    traceback.print_exc()

try:
    print("Step 4: Importing from map_helpers...")
    from utils.map_helpers import add_sdo_shield, add_school_dot
    print("✅ map_helpers imported successfully.")
except Exception as e:
    print(f"❌ map_helpers import failed: {e}")
    import traceback
    traceback.print_exc()

print("Test complete.")
