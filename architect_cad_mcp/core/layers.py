"""AIA CAD Layer Guidelines, Lineweights, Linetypes, and Sheet Codes.

Reference: AIA CAD Layer Guidelines (U.S. National CAD Standard v6 / ISO 13567).
"""

from __future__ import annotations

from typing import Any

# Complete 25-layer AIA Architectural, Structural, RCP, and MEP Layer Standard.
# Lineweight (dxf_lw) is in AutoCAD DXF hundredths of a millimeter (e.g. 50 = 0.50mm).
AIA_ARCHITECTURAL_LAYERS: tuple[dict[str, Any], ...] = (
    {"name": "A-GRID", "color": 8, "hex": "#64748B", "linetype": "CENTER2", "lineweight_mm": 0.09, "dxf_lw": 9, "plane": "all", "description": "Structural column grid axes"},
    {"name": "A-GRID-IDEN", "color": 7, "hex": "#0F172A", "linetype": "CONTINUOUS", "lineweight_mm": 0.25, "dxf_lw": 25, "plane": "all", "description": "Grid bubbles and alphanumeric axis tags"},
    {"name": "A-COLS", "color": 7, "hex": "#0F172A", "linetype": "CONTINUOUS", "lineweight_mm": 0.50, "dxf_lw": 50, "plane": "floor,structural", "description": "Structural RC/steel columns and load-bearing piers"},
    {"name": "A-WALL-FULL", "color": 7, "hex": "#0F172A", "linetype": "CONTINUOUS", "lineweight_mm": 0.50, "dxf_lw": 50, "plane": "floor,rcp,section", "description": "Full-height exterior and interior cut walls"},
    {"name": "A-WALL-PRHT", "color": 2, "hex": "#334155", "linetype": "CONTINUOUS", "lineweight_mm": 0.25, "dxf_lw": 25, "plane": "floor", "description": "Partial-height walls, parapets, balustrades (<1.20m)"},
    {"name": "A-WALL-PATT", "color": 253, "hex": "#94A3B8", "linetype": "CONTINUOUS", "lineweight_mm": 0.09, "dxf_lw": 9, "plane": "floor,section", "description": "Cut wall poche fill and masonry diagonal hatch"},
    {"name": "A-DOOR", "color": 3, "hex": "#1E293B", "linetype": "CONTINUOUS", "lineweight_mm": 0.20, "dxf_lw": 20, "plane": "floor,elevation", "description": "Door jambs, thresholds, and open door leaves"},
    {"name": "A-DOOR-SWNG", "color": 8, "hex": "#64748B", "linetype": "CONTINUOUS", "lineweight_mm": 0.13, "dxf_lw": 13, "plane": "floor", "description": "90-degree quarter-circle door swing clearance arcs"},
    {"name": "A-GLAZ", "color": 4, "hex": "#0284C7", "linetype": "CONTINUOUS", "lineweight_mm": 0.25, "dxf_lw": 25, "plane": "floor,elevation,section", "description": "Window frames, double-line glazing panes, curtain walls"},
    {"name": "A-GLAZ-SILL", "color": 8, "hex": "#475569", "linetype": "CONTINUOUS", "lineweight_mm": 0.13, "dxf_lw": 13, "plane": "floor,elevation", "description": "Exterior and interior window sill projections"},
    {"name": "A-STAIR", "color": 3, "hex": "#334155", "linetype": "CONTINUOUS", "lineweight_mm": 0.20, "dxf_lw": 20, "plane": "floor,section", "description": "Stair treads, handrails, 45-degree break line, UP direction arrow"},
    {"name": "A-FIXT", "color": 5, "hex": "#334155", "linetype": "CONTINUOUS", "lineweight_mm": 0.18, "dxf_lw": 18, "plane": "floor", "description": "Sanitary plumbing fixtures (WC, basin, shower, bath) and kitchen casework"},
    {"name": "A-FURN", "color": 252, "hex": "#64748B", "linetype": "CONTINUOUS", "lineweight_mm": 0.13, "dxf_lw": 13, "plane": "floor", "description": "Scaled furniture layouts proving ergonomic clearances"},
    {"name": "A-FLOR-PATT", "color": 254, "hex": "#CBD5E1", "linetype": "CONTINUOUS", "lineweight_mm": 0.05, "dxf_lw": 5, "plane": "floor", "description": "Wet-zone tile grids, timber decking, and plinth paving"},
    {"name": "A-OVER", "color": 1, "hex": "#64748B", "linetype": "HIDDEN2", "lineweight_mm": 0.15, "dxf_lw": 15, "plane": "floor", "description": "Overhead roof overhangs, beams, and skylights above +1.20m cut"},
    {"name": "A-ROOF", "color": 7, "hex": "#1E293B", "linetype": "CONTINUOUS", "lineweight_mm": 0.30, "dxf_lw": 30, "plane": "roof,elevation,section", "description": "Roof parapet coping, drainage crickets, slopes, and roof drains"},
    {"name": "A-ELEV-PROF", "color": 7, "hex": "#0F172A", "linetype": "CONTINUOUS", "lineweight_mm": 0.50, "dxf_lw": 50, "plane": "elevation,section", "description": "Primary foreground elevation profiles and ground datum line"},
    {"name": "E-LITE", "color": 2, "hex": "#D97706", "linetype": "CONTINUOUS", "lineweight_mm": 0.18, "dxf_lw": 18, "plane": "rcp", "description": "Recessed downlights, linear LED coves, and pendant luminaires"},
    {"name": "M-HVAC", "color": 4, "hex": "#0284C7", "linetype": "CONTINUOUS", "lineweight_mm": 0.18, "dxf_lw": 18, "plane": "rcp", "description": "Supply and return air ceiling diffusers and linear slot grilles"},
    {"name": "S-FOOT", "color": 6, "hex": "#475569", "linetype": "HIDDEN2", "lineweight_mm": 0.25, "dxf_lw": 25, "plane": "structural,section", "description": "Reinforced concrete isolated pad footings and strip foundations"},
    {"name": "S-BEAM", "color": 3, "hex": "#1E293B", "linetype": "CENTER2", "lineweight_mm": 0.30, "dxf_lw": 30, "plane": "structural,section", "description": "Grade beams, structural framing beams, and two-way slab spans"},
    {"name": "A-ANNO-DIMS", "color": 6, "hex": "#334155", "linetype": "CONTINUOUS", "lineweight_mm": 0.13, "dxf_lw": 13, "plane": "all", "description": "Three-tier exterior metric dimensions with 45-degree architectural ticks"},
    {"name": "A-ANNO-TEXT", "color": 7, "hex": "#0F172A", "linetype": "CONTINUOUS", "lineweight_mm": 0.20, "dxf_lw": 20, "plane": "all", "description": "Room tags, net floor areas, ceiling heights, and notes"},
    {"name": "A-ANNO-SYMB", "color": 7, "hex": "#0F172A", "linetype": "CONTINUOUS", "lineweight_mm": 0.25, "dxf_lw": 25, "plane": "all", "description": "Section cut markers (A-A, B-B), elevation datums, and North arrow"},
    {"name": "A-TTLB", "color": 7, "hex": "#0F172A", "linetype": "CONTINUOUS", "lineweight_mm": 0.35, "dxf_lw": 35, "plane": "all", "description": "Sheet border, title block, scale bar, and drawing metadata"},
)

LAYER_MAP: dict[str, dict[str, Any]] = {layer["name"]: layer for layer in AIA_ARCHITECTURAL_LAYERS}

from architect_cad_mcp.core.constants import FURNITURE_AND_FIXTURE_CATALOG

PLANE_CODES: dict[str, dict[str, str]] = {
    "floor_plan": {"sheet_prefix": "A-101", "title": "GROUND FLOOR PLAN (+1.20m CUT)"},
    "rcp": {"sheet_prefix": "A-102", "title": "REFLECTED CEILING PLAN (MIRROR PROJECTION)"},
    "roof_plan": {"sheet_prefix": "A-103", "title": "ROOF & DRAINAGE PLAN"},
    "elevations": {"sheet_prefix": "A-201", "title": "EXTERIOR ELEVATIONS (NORTH, SOUTH, EAST, WEST)"},
    "sections": {"sheet_prefix": "A-301", "title": "LONGITUDINAL & TRANSVERSE BUILDING SECTIONS"},
    "structural_plan": {"sheet_prefix": "S-101", "title": "STRUCTURAL GRID, FOUNDATION & FRAMING PLAN"},
}
