"""Compact Urban Townhouse Template (7.2m x 14.0m = 100.8 m2).

High-density narrow-lot urban residence with central daylighting lightwell.
"""

from __future__ import annotations

from typing import Any

SPEC: dict[str, Any] = {
    "id": "compact_urban_townhouse",
    "category": "house",
    "summary": "Narrow-lot urban townhouse with central lightwell courtyard, open social living/dining front bay, galley wet core, and quiet rear master suite.",
    "project": {
        "title": "COMPACT URBAN COURTYARD TOWNHOUSE",
        "category": "house",
        "sheetNumber": "A-101",
        "scale": "1:50",
        "units": "meters",
        "northAngleDeg": 90,
        "footprintWidth": 7.2,
        "footprintDepth": 14.0,
        "roofOverhang": 0.50,
        "plinthElevation": 0.30,
        "floorToFloorHeight": 3.00,
        "parapetHeight": 0.40,
    },
    "grid": {
        "vertical": [
            {"id": "A", "x": 0.0},
            {"id": "B", "x": 3.6},
            {"id": "C", "x": 7.2},
        ],
        "horizontal": [
            {"id": "1", "y": 0.0},
            {"id": "2", "y": 5.0},
            {"id": "3", "y": 9.0},
            {"id": "4", "y": 14.0},
        ],
    },
    "walls": [
        {"id": "W-SOUTH", "x1": 0.0, "y1": 0.0, "x2": 7.2, "y2": 0.0, "thickness": 0.25, "type": "exterior"},
        {"id": "W-NORTH", "x1": 0.0, "y1": 14.0, "x2": 7.2, "y2": 14.0, "thickness": 0.25, "type": "exterior"},
        {"id": "W-WEST", "x1": 0.0, "y1": 0.0, "x2": 0.0, "y2": 14.0, "thickness": 0.25, "type": "exterior"},
        {"id": "W-EAST", "x1": 7.2, "y1": 0.0, "x2": 7.2, "y2": 14.0, "thickness": 0.25, "type": "exterior"},
        {"id": "W-Z1", "x1": 0.0, "y1": 5.0, "x2": 7.2, "y2": 5.0, "thickness": 0.15, "type": "interior"},
        {"id": "W-Z2", "x1": 0.0, "y1": 9.0, "x2": 7.2, "y2": 9.0, "thickness": 0.20, "type": "wet-wall"},
        {"id": "W-MID", "x1": 3.6, "y1": 5.0, "x2": 3.6, "y2": 14.0, "thickness": 0.15, "type": "interior"},
    ],
    "rooms": [
        {
            "id": "01",
            "name": "LIVING & DINING SALON",
            "type": "living",
            "zone": "SOCIAL PAVILION",
            "habitable": True,
            "wetRoom": False,
            "x": 0.0,
            "y": 0.0,
            "width": 7.2,
            "depth": 5.0,
            "ceilingHeight": 3.00,
            "furniture": [
                {"item": "sofa_3seat", "x": 0.8, "y": 2.5},
                {"item": "dining_table_6p", "x": 4.4, "y": 2.4},
            ],
        },
        {
            "id": "02",
            "name": "GALLEY KITCHEN",
            "type": "kitchen",
            "zone": "WET CORE",
            "habitable": True,
            "wetRoom": True,
            "sharedWetWall": "W-Z2",
            "kitchenTriangleSum": 5.4,
            "x": 0.0,
            "y": 5.0,
            "width": 3.6,
            "depth": 4.0,
            "ceilingHeight": 2.85,
            "furniture": [],
        },
        {
            "id": "03",
            "name": "LIGHTWELL & BATH CORE",
            "type": "bathroom",
            "zone": "WET CORE",
            "habitable": False,
            "wetRoom": True,
            "sharedWetWall": "W-Z2",
            "x": 3.6,
            "y": 5.0,
            "width": 3.6,
            "depth": 4.0,
            "ceilingHeight": 2.60,
            "furniture": [
                {"item": "vanity_double", "x": 4.2, "y": 8.1},
                {"item": "wc_toilet", "x": 6.2, "y": 8.0},
            ],
        },
        {
            "id": "04",
            "name": "GARDEN MASTER BEDROOM",
            "type": "primary_bedroom",
            "zone": "PRIVATE SANCTUARY",
            "habitable": True,
            "wetRoom": False,
            "x": 0.0,
            "y": 9.0,
            "width": 3.6,
            "depth": 5.0,
            "ceilingHeight": 2.85,
            "furniture": [
                {"item": "queen_bed", "x": 1.0, "y": 11.4},
            ],
        },
        {
            "id": "05",
            "name": "STUDY / BEDROOM 02",
            "type": "bedroom",
            "zone": "PRIVATE SANCTUARY",
            "habitable": True,
            "wetRoom": False,
            "x": 3.6,
            "y": 9.0,
            "width": 3.6,
            "depth": 5.0,
            "ceilingHeight": 2.85,
            "furniture": [
                {"item": "study_desk", "x": 4.6, "y": 11.4},
            ],
        },
    ],
    "doors": [
        {"id": "D-01", "room": "01", "x": 5.4, "y": 0.0, "width": 1.05, "swingDeg": 90, "orientation": "north", "type": "entry"},
        {"id": "D-02", "room": "02", "x": 1.4, "y": 5.0, "width": 0.90, "swingDeg": 90, "orientation": "north", "type": "interior"},
        {"id": "D-03", "room": "03", "x": 4.2, "y": 5.0, "width": 0.80, "swingDeg": 90, "orientation": "north", "type": "bathroom"},
        {"id": "D-04", "room": "04", "x": 1.4, "y": 9.0, "width": 0.85, "swingDeg": 90, "orientation": "north", "type": "interior"},
        {"id": "D-05", "room": "05", "x": 4.4, "y": 9.0, "width": 0.85, "swingDeg": 90, "orientation": "north", "type": "interior"},
    ],
    "windows": [
        {"id": "WIN-01", "room": "01", "wall": "south", "x1": 0.8, "y1": 0.0, "x2": 4.6, "y2": 0.0, "sill": 0.30, "head": 2.40},
        {"id": "WIN-02", "room": "02", "wall": "west", "x1": 0.0, "y1": 5.8, "x2": 0.0, "y2": 8.2, "sill": 0.90, "head": 2.40},
        {"id": "WIN-03", "room": "04", "wall": "north", "x1": 0.8, "y1": 14.0, "x2": 2.8, "y2": 14.0, "sill": 0.60, "head": 2.40},
        {"id": "WIN-04", "room": "05", "wall": "north", "x1": 4.4, "y1": 14.0, "x2": 6.4, "y2": 14.0, "sill": 0.60, "head": 2.40},
    ],
    "stairs": [
        {"id": "ST-TH", "name": "Townhouse Straight Flight", "riserMm": 165, "treadMm": 285, "riserCount": 18, "widthM": 1.00, "x": 5.8, "y": 1.0}
    ],
    "sections": [
        {"id": "A-A", "type": "longitudinal", "x1": 3.6, "y1": -1.2, "x2": 3.6, "y2": 15.2, "lookDirection": "west"},
        {"id": "B-B", "type": "transverse", "x1": -1.2, "y1": 7.0, "x2": 8.4, "y2": 7.0, "lookDirection": "north"},
    ],
}
