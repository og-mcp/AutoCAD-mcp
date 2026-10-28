"""MCP Prompt for commercial office and creative studio design."""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP


def register(mcp: FastMCP) -> None:
    @mcp.prompt()
    def design_workplace(
        headcount: int = 32,
        footprint_width_m: float = 24.0,
        footprint_depth_m: float = 16.0,
        workplace_type: str = "open_office",
    ) -> str:
        """Prompt template for commercial workplace and design studio layouts."""
        return f"""You are a Workplace Strategist and Senior Architect specializing in modern collaborative environments.

Project Scope:
- Target Occupancy: {headcount} occupants
- Building Footprint: {footprint_width_m:.2f}m x {footprint_depth_m:.2f}m ({footprint_width_m * footprint_depth_m:.1f} m2)
- Typology: {workplace_type.replace('_', ' ').title()}

Spatial Zoning & Requirements:
1. Agile Desk Neighborhood:
   - Provide 4-person desk pods (3.20m x 1.50m) with 1.40m clear chair back clearance.
2. Meeting & Focus Realms:
   - Executive Boardroom for 10-12 persons with acoustic double-glazed walls.
   - Private focus booths / phone rooms for high-concentration work.
3. Social & Wet Core:
   - Townhall cafe / pantry with island counter and plumbing back-to-back with ADA restrooms.
4. Reflected Ceiling Plan (RCP A-102):
   - 2x2 LED troffers or recessed downlights aligned with workstation grid.
   - Balanced 400x400mm supply diffusers and linear slot returns.
5. Code & Ergonomics:
   - Main promenade corridor >= 1.50m clear.
   - Run Neufert anthropometrics and DRC audit.

Examine the workplace templates 'open_workplace_office' and 'architectural_atelier_studio' via the `template` tool to accelerate drafting.
"""
