"""Architectural Design Rule Checking (DRC) and area schedule MCP tool."""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from architect_cad_mcp.domain.drc.validator import audit_architecture_spec
from architect_cad_mcp.state import SESSION_STATE, error_response, ok_response


def register(mcp: FastMCP) -> None:
    @mcp.tool()
    def arch_audit(operation: str = "validate_anthropometrics") -> str:
        """Validate the active building design against Neufert anthropometrics, Blondel stair law, and building codes.

        Operations:
        - validate_anthropometrics: Run full DRC audit (room sizes, door widths, daylight glazing >=10%, corridor <=18%, stair 2R+T).
        - compute_area_schedule: Return room-by-room area schedule and programmatic zone breakdown.
        """
        spec = SESSION_STATE.spec

        if operation == "validate_anthropometrics":
            report = audit_architecture_spec(spec)
            return ok_response({"audit": report, "drc_report": report})

        if operation == "compute_area_schedule":
            schedule = []
            zone_totals: dict[str, float] = {}
            for r in spec.get("rooms", []):
                area = round(float(r["width"]) * float(r["depth"]), 2)
                zone = str(r.get("zone", "OTHER"))
                zone_totals[zone] = round(zone_totals.get(zone, 0.0) + area, 2)
                schedule.append({
                    "id": r["id"],
                    "name": r["name"],
                    "zone": zone,
                    "dimensions_m": f"{float(r['width']):.2f} x {float(r['depth']):.2f}",
                    "area_m2": area,
                    "ceiling_height_m": r.get("ceilingHeight", 2.85),
                })
            return ok_response({
                "room_schedule": schedule,
                "zone_totals_m2": zone_totals,
                "circulation_efficiency": f"{(zone_totals.get('CIRCULATION SPINE', 0.0) / max(sum(zone_totals.values()), 1.0) * 100):.1f}%",
            })

        return error_response("E_INVALID_OPERATION", f"Unknown arch_audit operation: {operation}")
