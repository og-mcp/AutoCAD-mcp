"""MCP Prompt for generating a complete 6-plane Construction Document (CD) package."""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP


def register(mcp: FastMCP) -> None:
    @mcp.prompt()
    def generate_coordinated_cd_set(
        output_directory: str = "cad_output/construction_documents",
        dpi: int = 150,
        render_png_previews: bool = True,
    ) -> str:
        """Prompt template for orchestrating all 6 coordinated orthographic planes."""
        return f"""You are the Project Architect generating a complete, permit-ready 2D Construction Document package.

Deliverables Target:
- Destination Directory: '{output_directory}'
- Rendering: PNG Previews @ {dpi} DPI (Headless Agg backend, deterministic byte-stable output)

Required 6 Orthographic Drawing Sheets:
1. Sheet A-101: Ground Floor Plan (+1.20m horizontal cut, solid wall poché, door swings, fixture layout, 3-tier dimensions)
2. Sheet A-102: Reflected Ceiling Plan (mirror projection, ceiling grid, recessed LED luminaires, HVAC supply & return)
3. Sheet A-103: Roof & Drainage Plan (parapets, 2% slope direction arrows, roof drains RD Ø100, scuppers)
4. Sheet A-201: Exterior Elevations (South & North elevations with vertical level datums: Ground, FFL, Ceiling, Parapet)
5. Sheet A-301: Building Sections (Longitudinal A-A and Transverse B-B cut sections showing slabs, footings, clear heights)
6. Sheet S-101: Structural Framing & Foundation Plan (isolated RC column footings, structural grid, grade beams)

Execution Steps:
1. Run `arch_audit` (operation='validate_anthropometrics') to guarantee 0 DRC errors.
2. Run `drawing` (operation='deliver_package', output_directory='{output_directory}') to generate all DXF, SCR, SVG, and PNG files.
3. Review the generated `manifest.json` and verify handle-independent geometry SHA-256 digests.
"""
