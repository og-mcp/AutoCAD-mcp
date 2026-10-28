"""MCP Prompt for guided multi-unit apartment floor plate design."""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP


def register(mcp: FastMCP) -> None:
    @mcp.prompt()
    def design_apartment_floor(
        footprint_width_m: float = 24.0,
        footprint_depth_m: float = 14.4,
        unit_count: int = 5,
        floor_to_floor_h: float = 3.15,
    ) -> str:
        """Prompt template for designing a typical multi-unit residential apartment floor plate."""
        return f"""You are a Senior Project Architect coordinating a multi-unit residential building floor plate.

Building Dimensions:
- Floor Plate: {footprint_width_m:.2f}m x {footprint_depth_m:.2f}m (Gross Area = {footprint_width_m * footprint_depth_m:.1f} m2)
- Target Units: {unit_count} residential apartments
- Floor-to-Floor Height: {floor_to_floor_h:.2f}m

Core Life-Safety and Code Requirements:
1. Central Pressurized Core:
   - Provide dual passenger elevator shafts (cab size >= 2.1m x 2.1m).
   - Pressurized fire egress stair with minimum 1.20m clear run and Blondel compliant risers/treads.
   - Dedicated MEP riser chase and back-to-back plumbing wet walls.
2. Egress & ADA Corridors:
   - Central double-loaded circulation corridor minimum 1.50m - 1.80m clear width.
   - Entry doors 1.00m leaf with 90-degree swing arcs into individual unit vestibules.
3. Residential Typology Mix:
   - Corner 2-Bedroom Units with dual-aspect fenestration.
   - Central 1-Bedroom / Studio Units with efficient linear kitchen casework.
4. Coordinated Drawing Set:
   - Deliver all 6 planes: Floor Plan (A-101), RCP (A-102), Roof (A-103), Elevations (A-201), Sections (A-301), and Structural Framing (S-101).

Use the `template` tool to inspect 'multi_unit_apartment_floor' or customize it for this site footprint.
"""
