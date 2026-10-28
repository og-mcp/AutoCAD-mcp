"""MCP Resources for Architectural and CAD Standards."""

from __future__ import annotations

import json
from mcp.server.fastmcp import FastMCP

from architect_cad_mcp.core.constants import (
    BLONDEL_MAX_MM,
    BLONDEL_MIN_MM,
    FURNITURE_AND_FIXTURE_CATALOG,
    MAX_CIRCULATION_RATIO_PCT,
    MIN_DOOR_WIDTHS,
    MIN_GLAZING_RATIO_PCT,
    MIN_ROOM_SPECS,
)
from architect_cad_mcp.core.layers import AIA_ARCHITECTURAL_LAYERS, PLANE_CODES


def register(mcp: FastMCP) -> None:
    @mcp.resource("cad://standards/layers")
    def get_layers_resource() -> str:
        """25-layer AIA CAD Architectural, Structural, RCP, and MEP Standard with Lineweights."""
        return json.dumps({
            "standard": "AIA CAD Layer Guidelines (U.S. National CAD Standard / ISO 13567)",
            "layer_count": len(AIA_ARCHITECTURAL_LAYERS),
            "layers": list(AIA_ARCHITECTURAL_LAYERS),
        }, indent=2)

    @mcp.resource("cad://standards/furniture-catalog")
    def get_furniture_catalog_resource() -> str:
        """Standard Neufert Anthropometric Furniture and Sanitary Fixture Footprints."""
        return json.dumps({
            "standard": "Ernst Neufert Architects' Data (Metric Dimensions in Meters)",
            "item_count": len(FURNITURE_AND_FIXTURE_CATALOG),
            "items": FURNITURE_AND_FIXTURE_CATALOG,
        }, indent=2)

    @mcp.resource("cad://standards/drc-rules")
    def get_drc_rules_resource() -> str:
        """Architectural Design Rule Check (DRC) Code Limits and Formulas."""
        return json.dumps({
            "room_minimum_areas_and_widths": MIN_ROOM_SPECS,
            "door_clear_widths": MIN_DOOR_WIDTHS,
            "stair_ergonomics": {
                "formula": "François Blondel: 2 * Riser + Tread",
                "min_mm": BLONDEL_MIN_MM,
                "max_mm": BLONDEL_MAX_MM,
                "target_residential": "2 * 160mm + 290mm = 610mm",
            },
            "daylighting": {
                "min_glazing_ratio_pct": MIN_GLAZING_RATIO_PCT,
                "rule": "Glazed window area / Net room floor area >= 10%",
                "bilateral_bonus": "Alexander Pattern 159 (Light on Two Sides)",
            },
            "circulation": {
                "max_corridor_ratio_pct": MAX_CIRCULATION_RATIO_PCT,
                "rule": "Corridor circulation area / Gross floor area <= 18%",
            },
            "planes": PLANE_CODES,
        }, indent=2)
