"""Data loading and generation utilities."""

import json
import random
import os
from pathlib import Path
import pandas as pd
from .constants import DIMENSION_NAMES, DEGREE_COLORS

def load_sdo_data():
    """Load SDO master data from JSON file."""
    data_path = Path(__file__).parent.parent / "data" / "sdo_master.json"
    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # Calculate derived fields for each SDO
    for sdo in data["sdo_list"]:
        dims = sdo["dimension_scores"]
        sdo["lowest_dim_index"] = dims.index(min(dims))
        sdo["lowest_dim_score"] = min(dims)
        sdo["lowest_dim_name"] = DIMENSION_NAMES[sdo["lowest_dim_index"]]
        sdo["overall_index"] = round(sum(dims) / len(dims), 1)
    
    # Compute relative urgency (for pulse system)
    all_lowest = [s["lowest_dim_score"] for s in data["sdo_list"]]
    min_score = min(all_lowest)
    max_score = max(all_lowest)
    range_val = max_score - min_score or 0.001
    
    for sdo in data["sdo_list"]:
        raw = (sdo["lowest_dim_score"] - min_score) / range_val
        sdo["urgency_factor"] = round(1 - raw, 3)  # 1 = most urgent
    
    return data["sdo_list"]

def generate_schools_for_sdo(sdo_id, sdo_lat, sdo_lng, count=5):
    """Generate mock schools for a given SDO."""
    school_statuses = ["Complete"] * 7 + ["Pending"]
    schools = []
    
    for i in range(count):
        status = random.choice(school_statuses)
        is_pending = status == "Pending"
        
        if is_pending:
            overall = 0
            dims = [0, 0, 0, 0, 0, 0]
            degree = "Pending"
        else:
            overall = round(random.uniform(0.4, 2.9), 1)
            dims = [round(random.uniform(0.5, 2.9), 1) for _ in range(6)]
            # Ensure finance is sometimes low
            dims[5] = min(dims[5], round(random.uniform(0.3, 2.2), 1))
            if overall >= 2.5:
                degree = "Always Manifested"
            elif overall >= 2.0:
                degree = "Frequently Manifested"
            elif overall >= 1.0:
                degree = "Rarely Manifested"
            else:
                degree = "Not Yet Manifested"
        
        # Scatter around SDO capital
        lat_offset = (random.random() - 0.5) * 0.3
        lng_offset = (random.random() - 0.5) * 0.3
        
        school_types = ["Elementary", "Secondary", "Integrated"]
        school_names = [
            f"School {chr(65+i)} {sdo_id}",
            f"Central {school_types[i%3]}",
            f"Memorial {school_types[(i+1)%3]}",
            f"National {school_types[(i+2)%3]}"
        ]
        
        schools.append({
            "id": f"{sdo_id}{str(i+1).zfill(3)}",
            "name": random.choice(school_names),
            "type": random.choice(school_types),
            "sdo_id": sdo_id,
            "lat": sdo_lat + lat_offset,
            "lng": sdo_lng + lng_offset,
            "enrollment": 0 if is_pending else random.randint(150, 3200),
            "overall_index": overall,
            "degree": degree,
            "dimension_scores": dims,
            "data_status": status,
            "lowest_dim_index": None if is_pending else dims.index(min(dims)),
            "lowest_dim_score": None if is_pending else min(dims)
        })
    
    return schools

def load_all_schools(sdo_list):
    """Generate schools for all SDOs and return as list."""
    all_schools = []
    for sdo in sdo_list:
        count = random.randint(3, 7)
        schools = generate_schools_for_sdo(sdo["id"], sdo["lat"], sdo["lng"], count)
        all_schools.extend(schools)
    return all_schools

def get_schools_by_sdo(schools, sdo_id):
    """Filter schools by SDO ID."""
    return [s for s in schools if s["sdo_id"] == sdo_id]

def compute_dimension_averages(schools):
    """Compute average dimension scores across schools."""
    if not schools:
        return [0, 0, 0, 0, 0, 0]
    
    complete_schools = [s for s in schools if s["data_status"] != "Pending"]
    if not complete_schools:
        return [0, 0, 0, 0, 0, 0]
    
    dim_avgs = [0, 0, 0, 0, 0, 0]
    for s in complete_schools:
        for i, val in enumerate(s["dimension_scores"]):
            dim_avgs[i] += val
    
    return [round(v / len(complete_schools), 1) for v in dim_avgs]
