"""Orthographic plane generation MCP tool (Floor Plan, RCP, Roof, Elevations, Sections, Framing)."""

from __future__ import annotations

from pathlib import Path

from mcp.server.fastmcp import FastMCP

from architect_cad_mcp.core.layers import PLANE_CODES
from architect_cad_mcp.domain.engines.multi_plane import (
    generate_full_cd_package,
    generate_plane_dxf_and_svg,
)
from architect_cad_mcp.state import SESSION_STATE, error_response, ok_response


def register(mcp: FastMCP) -> None:
    @mcp.tool()
    def orthographic_plane(
        operation: str = "generate_all_planes",
        plane: str = "floor_plan",
        plane_key: str | None = None,
        output_dir: str = "cad_output/active_drawing",
        output_directory: str | None = None,
    ) -> str:
        """Generate one or all 6 coordinated 2D orthographic planes (.dxf, .scr, .svg).

        Supported `plane` values:
        - floor_plan: A-101 Ground Floor Plan (+1.20m horizontal cut plane)
        - rcp: A-102 Reflected Ceiling Plan (mirror projection with lighting & HVAC)
        - roof_plan: A-103 Roof & Drainage Plan (2% slope arrows & roof drains)
        - elevations: A-201 Exterior Elevations (South & North facades with level datums)
        - sections: A-301 Longitudinal (A-A) & Transverse (B-B) Building Sections
        - structural_plan: S-101 Structural Grid, Footing & Grade Beam Framing Plan
        """
        target_plane = plane_key or plane
        out = Path(output_directory or output_dir)
        spec = SESSION_STATE.spec

        if operation == "generate_plane":
            if target_plane not in PLANE_CODES:
                return error_response(
                    "E_INVALID_PLANE_KEY",
                    f"Unknown plane: '{target_plane}'.",
                    f"Choose from: {list(PLANE_CODES.keys())}",
                )
            result = generate_plane_dxf_and_svg(spec, target_plane, out)
            return ok_response({"plane_output": result})

        if operation == "generate_all_planes":
            pkg = generate_full_cd_package(spec, out)
            return ok_response({"package": pkg, "manifest": pkg})

        return error_response("E_INVALID_OPERATION", f"Unknown orthographic_plane operation: {operation}")
