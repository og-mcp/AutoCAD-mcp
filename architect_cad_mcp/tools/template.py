"""Architectural template management MCP tool."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from mcp.server.fastmcp import FastMCP

from architect_cad_mcp.domain.drc.validator import audit_architecture_spec
from architect_cad_mcp.domain.engines.multi_plane import generate_full_cd_package
from architect_cad_mcp.state import SESSION_STATE, error_response, ok_response
from architect_cad_mcp.templates.registry import TEMPLATES, get_template, list_templates


def register(mcp: FastMCP) -> None:
    @mcp.tool()
    def template(
        operation: str = "list_templates",
        template_id: str | None = None,
        category: str | None = None,
        overrides: dict[str, Any] | None = None,
        customizations_json: str | None = None,
        output_dir: str | None = None,
    ) -> str:
        """Browse, inspect, and instantiate ready-to-use architectural building templates.

        Operations:
        - list_templates: List templates across 'house', 'floor_building', and 'workplace'.
        - inspect_template: Return full specification of a template without activating it.
        - instantiate_template: Replace active building specification with chosen template (and optionally build package to output_dir).
        - customize_template: Instantiate template with partial overrides supplied in overrides or customizations_json.
        """
        if operation == "list_templates":
            items = list_templates(category=category)
            return ok_response({"category": category or "all", "templates": items})

        if not template_id:
            return error_response("E_MISSING_TEMPLATE_ID", "Parameter 'template_id' is required.")

        try:
            tpl = get_template(template_id)
        except KeyError as err:
            return error_response("E_UNKNOWN_TEMPLATE", str(err), "Call operation='list_templates' to view valid IDs.")

        if operation == "inspect_template":
            drc = audit_architecture_spec(tpl)
            return ok_response({
                "template_id": template_id,
                "project": tpl["project"],
                "drc_summary": drc["counts"],
                "metrics": drc["metrics"],
                "spec": tpl,
            })

        if operation in ("instantiate_template", "customize_template"):
            applied_overrides: dict[str, Any] = {}
            if overrides and isinstance(overrides, dict):
                applied_overrides.update(overrides)
            if customizations_json:
                try:
                    c_dict = json.loads(customizations_json)
                    if isinstance(c_dict, dict):
                        applied_overrides.update(c_dict)
                except Exception:
                    pass

            if applied_overrides:
                if "project" in tpl and isinstance(tpl["project"], dict):
                    for k, v in applied_overrides.items():
                        if k in tpl["project"] or not isinstance(v, (dict, list)):
                            tpl["project"][k] = v
                        else:
                            tpl[k] = v
                else:
                    tpl.update(applied_overrides)

            rev = SESSION_STATE.update_spec(tpl)
            active_spec = SESSION_STATE.get_raw_spec()
            response: dict[str, Any] = {
                "active_template": template_id,
                "project": active_spec.get("project", {}),
                "drc": audit_architecture_spec(active_spec)["counts"],
            }
            if output_dir:
                pkg = generate_full_cd_package(active_spec, Path(output_dir))
                response["package"] = pkg

            return ok_response(response, revision=rev)

        return error_response("E_INVALID_OPERATION", f"Unknown template operation: '{operation}'.")
