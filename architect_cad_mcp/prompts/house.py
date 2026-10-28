"""MCP Prompt for guided residential house design."""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP


def register(mcp: FastMCP) -> None:
    @mcp.prompt()
    def design_house(
        site_width_m: float = 16.0,
        site_depth_m: float = 12.0,
        bedroom_count: int = 3,
        include_courtyard: bool = True,
        style: str = "contemporary",
    ) -> str:
        """Prompt template for designing a residential house grounded in Ching and Alexander principles."""
        courtyard_note = (
            "Incorporate a central private courtyard adhering to Christopher Alexander Pattern 115 (Courtyards Which Live)."
            if include_courtyard
            else "Ensure bilateral daylighting following Alexander Pattern 159 (Light on Two Sides)."
        )
        return f"""You are a licensed Senior Architect tasked with designing a {style} single-family residence.

Site Boundaries:
- Width: {site_width_m:.2f} meters
- Depth: {site_depth_m:.2f} meters
- Program: {bedroom_count} Bedrooms, Living Pavilion, Island Kitchen & Dining, and Consolidated Wet Core.

Architectural Design Directives:
1. {courtyard_note}
2. Ground the spatial composition using a clear structural column grid (Francis D.K. Ching).
3. Ensure every room meets or exceeds Ernst Neufert minimum anthropometric areas:
   - Primary Bedroom: >= 12.0 m2 (min width 3.20m)
   - Secondary Bedrooms: >= 9.5 m2 (min width 2.70m)
   - Living Room: >= 16.0 m2 (min width 3.60m)
   - Kitchen: >= 7.5 m2 (work triangle between 4.0m and 7.9m)
   - Corridors: clear width >= 1.0m, circulation ratio <= 18% of gross floor area
4. Check stair riser and tread dimensions against François Blondel's comfort law: 600mm <= 2R + T <= 630mm.
5. Provide cut wall poché on layer A-WALL-PATT with door/window openings subtracted.
6. Generate 3-tier exterior metric dimensions with 45-degree architectural slash ticks.

Begin by inspecting the existing house templates using the `template` tool, or instantiate 'courtyard_residence' or 'modern_family_villa' as a starting armature.
"""
