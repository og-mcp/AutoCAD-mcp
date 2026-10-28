"""Architectural Design Constants, Neufert Anthropometrics, and Code Limits.

References:
- Ernst Neufert, Architects' Data, 4th/5th Ed.
- International Building Code (IBC) 2024 / National Building Code (NBC).
- François Blondel, Cours d'Architecture (Stair Law).
"""

from __future__ import annotations

from typing import Any

# Standard Neufert Furniture & Sanitary Fixture Catalog (dimensions in meters)
FURNITURE_AND_FIXTURE_CATALOG: dict[str, dict[str, Any]] = {
    "king_bed": {"layer": "A-FURN", "width": 1.80, "depth": 2.05, "label": "KING BED"},
    "queen_bed": {"layer": "A-FURN", "width": 1.50, "depth": 2.00, "label": "QUEEN BED"},
    "wardrobe": {"layer": "A-FURN", "width": 2.40, "depth": 0.60, "label": "WARDROBE"},
    "sofa_3seat": {"layer": "A-FURN", "width": 2.40, "depth": 0.92, "label": "SOFA"},
    "coffee_table": {"layer": "A-FURN", "width": 1.40, "depth": 0.70, "label": "TABLE"},
    "dining_table_6p": {"layer": "A-FURN", "width": 2.00, "depth": 0.95, "label": "DINING 6P"},
    "study_desk": {"layer": "A-FURN", "width": 1.60, "depth": 0.75, "label": "DESK"},
    "workstation_cluster_4p": {"layer": "A-FURN", "width": 3.20, "depth": 1.50, "label": "4P DESK POD"},
    "boardroom_table_12p": {"layer": "A-FURN", "width": 4.20, "depth": 1.40, "label": "BOARDROOM 12P"},
    "drafting_table": {"layer": "A-FURN", "width": 1.80, "depth": 0.90, "label": "DRAFTING TABLE"},
    "reception_desk": {"layer": "A-FIXT", "width": 2.60, "depth": 0.80, "label": "RECEPTION"},
    "kitchen_island": {"layer": "A-FIXT", "width": 2.40, "depth": 0.95, "label": "ISLAND"},
    "kitchen_counter": {"layer": "A-FIXT", "width": 3.60, "depth": 0.60, "label": "COUNTER / SINK"},
    "wc_toilet": {"layer": "A-FIXT", "width": 0.42, "depth": 0.68, "label": "WC"},
    "vanity_double": {"layer": "A-FIXT", "width": 1.50, "depth": 0.58, "label": "VANITY"},
    "freestanding_tub": {"layer": "A-FIXT", "width": 1.75, "depth": 0.80, "label": "TUB"},
    "walk_in_shower": {"layer": "A-FIXT", "width": 1.20, "depth": 1.40, "label": "SHOWER"},
    "elevator_cab": {"layer": "A-FIXT", "width": 2.10, "depth": 2.10, "label": "LIFT"},
}

# Neufert minimum clear widths and floor areas (in meters and square meters)
MIN_ROOM_SPECS: dict[str, dict[str, float]] = {
    "primary_bedroom": {"min_width": 3.20, "min_area": 12.0},
    "bedroom": {"min_width": 2.70, "min_area": 9.5},
    "living": {"min_width": 3.60, "min_area": 16.0},
    "dining": {"min_width": 3.00, "min_area": 10.0},
    "kitchen": {"min_width": 2.40, "min_area": 7.5},
    "study": {"min_width": 2.40, "min_area": 6.5},
    "bathroom": {"min_width": 1.70, "min_area": 4.0},
    "powder": {"min_width": 1.10, "min_area": 1.8},
    "foyer": {"min_width": 1.50, "min_area": 3.0},
    "corridor": {"min_width": 0.90, "min_area": 0.0},
}

# Minimum clear door leaf widths (in meters)
MIN_DOOR_WIDTHS: dict[str, float] = {
    "entry": 1.00,
    "interior": 0.80,
    "bathroom": 0.70,
}

# François Blondel Ergonomic Stair Comfort Law: 600mm <= 2R + T <= 630mm
BLONDEL_MIN_MM: float = 600.0
BLONDEL_MAX_MM: float = 630.0
MAX_RESIDENTIAL_RISER_MM: float = 180.0
MIN_RESIDENTIAL_TREAD_MM: float = 280.0

# Natural Daylighting & Ventilation Ratio
MIN_GLAZING_RATIO_PCT: float = 10.0  # Glazing area / Room floor area >= 10%

# Maximum Circulation Efficiency Ratio (Corridor area / Total gross area)
MAX_CIRCULATION_RATIO_PCT: float = 18.0
