"""MCP Prompt for running comprehensive architectural DRC and code audits."""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP


def register(mcp: FastMCP) -> None:
    @mcp.prompt()
    def audit_floor_plan(
        strict_neufert: bool = True,
        check_daylight: bool = True,
        check_blondel_stairs: bool = True,
    ) -> str:
        """Prompt template for auditing an active architectural plan against canonical codes."""
        return f"""You are the Lead Code Compliance and Quality Assurance Architect.

Perform a rigorous multi-point Design Rule Check (DRC) on the active floor plan specification:

Audit Checklist:
1. Neufert Anthropometric Clearance:
   - Validate room widths and net floor areas against Ernst Neufert standards (strict={strict_neufert}).
   - Verify kitchen work triangle sum falls strictly between 4.0m and 7.9m.
2. Natural Light & Ventilation (IBC Section 1205):
   - Confirm habitable rooms have window glazing >= 10.0% of net floor area (enabled={check_daylight}).
   - Highlight rooms with bilateral daylighting (Alexander Pattern 159).
3. Stair Ergonomics:
   - Verify François Blondel's comfort formula 600mm <= 2R + T <= 630mm (enabled={check_blondel_stairs}).
   - Verify residential risers do not exceed 180mm.
4. Circulation & Plumbing Efficiency:
   - Verify corridor circulation ratio does not exceed 18% of gross floor area.
   - Confirm wet rooms (bathrooms, powder rooms, kitchens) share consolidated wet walls.

Execute the `arch_audit` tool with operation='validate_anthropometrics' and report all passed checks, warnings, and errors with specific remedial recommendations.
"""
