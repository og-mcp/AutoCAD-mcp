"""MCP Resources for Active Drawing Inspection, Metrics, and DRC Compliance."""

from __future__ import annotations

import json
from mcp.server.fastmcp import FastMCP

from architect_cad_mcp.core.layers import PLANE_CODES
from architect_cad_mcp.domain.drc.validator import audit_architecture_spec
from architect_cad_mcp.state import SESSION_STATE


def register(mcp: FastMCP) -> None:
    @mcp.resource("cad://drawing/active/spec")
    def get_active_drawing_spec_resource() -> str:
        """Active in-memory architectural specification JSON."""
        return json.dumps({
            "revision": SESSION_STATE.revision,
            "spec": SESSION_STATE.spec,
        }, indent=2)

    @mcp.resource("cad://drawing/active/drc")
    def get_active_drawing_drc_resource() -> str:
        """Real-time Neufert anthropometrics and code compliance audit for the active drawing."""
        report = audit_architecture_spec(SESSION_STATE.spec)
        return json.dumps({
            "revision": SESSION_STATE.revision,
            "drc_report": report,
        }, indent=2)

    @mcp.resource("cad://drawing/active/planes")
    def get_active_drawing_planes_resource() -> str:
        """Coordinated 2D orthographic planes and sheet metadata for the active drawing."""
        proj = SESSION_STATE.spec.get("project", {})
        return json.dumps({
            "project_title": proj.get("title", "Untitled"),
            "scale": proj.get("scale", "1:100"),
            "sheet_count": len(PLANE_CODES),
            "planes": PLANE_CODES,
        }, indent=2)
