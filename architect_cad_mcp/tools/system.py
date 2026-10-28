"""System information, AIA CAD layer definitions, and Neufert furniture catalog tool."""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from architect_cad_mcp.core.constants import FURNITURE_AND_FIXTURE_CATALOG
from architect_cad_mcp.core.layers import AIA_ARCHITECTURAL_LAYERS, PLANE_CODES
from architect_cad_mcp.state import SESSION_STATE, error_response, ok_response
from architect_cad_mcp.templates.registry import TEMPLATES


def register(mcp: FastMCP) -> None:
    @mcp.tool()
    def system(operation: str = "status") -> str:
        """Server status, supported orthographic planes, 24 AIA layers, and Neufert fixture catalog.

        Operations:
        - status: Return server version, active project title, revision, and template count.
        - capabilities: Return supported 2D orthographic planes and CAD output formats.
        - list_aia_layers: Return all 24 AIA architectural, structural, RCP, and MEP layers with plot lineweights.
        - list_furniture_catalog: Return standard Neufert furniture and sanitary fixture dimensions.
        """
        if operation == "status":
            spec = SESSION_STATE.get_raw_spec()
            return ok_response({
                "server": "architect-cad-mcp",
                "version": "1.0.0",
                "backend": "ezdxf",
                "runtime": "Any platform",
                "requires_autocad": False,
                "validation_feedback": "Structured audit + deterministic PNG",
                "active_project": spec.get("project", {}).get("title"),
                "category": spec.get("project", {}).get("category", "house"),
                "template_count": len(TEMPLATES),
                "aia_layer_count": len(AIA_ARCHITECTURAL_LAYERS),
                "supported_planes": list(PLANE_CODES.keys()),
            })
        elif operation == "capabilities":
            return ok_response({
                "planes": PLANE_CODES,
                "outputs": ["dxf (R2013 ezdxf)", "scr (AutoCAD/LT command script)", "svg (2D sheet preview)", "json (DRC & SHA-256 manifest)"],
                "categories": ["house", "floor_building", "workplace"],
                "standards": [
                    "AIA CAD Layer Guidelines (25 layers)",
                    "Ernst Neufert Anthropometrics (Architects' Data)",
                    "François Blondel Stair Law (2R+T = 600-630mm)",
                    "IBC Natural Light & Ventilation Glazing Ratio (>= 10%)",
                    "Three-tier metric exterior dimensions with 45-degree architectural slash ticks",
                    "Handle-independent geometry digest (SHA-256)",
                    "Deterministic headless PNG rendering (Matplotlib Agg)",
                ],
            })
        elif operation == "list_aia_layers":
            return ok_response({
                "layer_count": len(AIA_ARCHITECTURAL_LAYERS),
                "layers": list(AIA_ARCHITECTURAL_LAYERS),
            })
        elif operation == "list_furniture_catalog":
            return ok_response({
                "catalog_count": len(FURNITURE_AND_FIXTURE_CATALOG),
                "catalog": FURNITURE_AND_FIXTURE_CATALOG,
                "items": FURNITURE_AND_FIXTURE_CATALOG,
            })
        return error_response(
            "E_INVALID_OPERATION",
            f"Unknown system operation: '{operation}'.",
            "Use 'status', 'capabilities', 'list_aia_layers', or 'list_furniture_catalog'.",
        )
