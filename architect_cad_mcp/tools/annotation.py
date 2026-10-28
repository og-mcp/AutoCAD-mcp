"""Architectural drafting annotations, section markers, and title block metadata MCP tool."""

from __future__ import annotations

from typing import Any
from mcp.server.fastmcp import FastMCP

from architect_cad_mcp.state import SESSION_STATE, error_response, ok_response


def register(mcp: FastMCP) -> None:
    @mcp.tool()
    def annotation(
        operation: str = "add_section_cut",
        data: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> str:
        """Manage architectural annotations, section cut lines, and title block metadata.

        Operations:
        - add_section_cut: Add a section cut callout (`id`, `type`, `x1`, `y1`, `x2`, `y2`, `lookDirection`).
        - update_project_metadata: Update title block fields (`title`, `sheetNumber`, `scale`, `northAngleDeg`).
        """
        payload: dict[str, Any] = {}
        if data and isinstance(data, dict):
            payload.update(data)
        payload.update(kwargs)

        spec, rev = SESSION_STATE.mutate_spec()

        if operation == "add_section_cut":
            sec = {
                "id": str(payload.get("id", "C-C")),
                "type": str(payload.get("type", "transverse")),
                "x1": float(payload["x1"]),
                "y1": float(payload["y1"]),
                "x2": float(payload["x2"]),
                "y2": float(payload["y2"]),
                "lookDirection": str(payload.get("lookDirection", "north")),
            }
            spec.setdefault("sections", []).append(sec)
            return ok_response({"sections": spec["sections"]}, revision=rev)

        if operation == "update_project_metadata":
            spec.setdefault("project", {}).update(payload)
            return ok_response({"project": spec["project"]}, revision=rev)

        return error_response("E_INVALID_OPERATION", f"Unknown annotation operation: {operation}")
