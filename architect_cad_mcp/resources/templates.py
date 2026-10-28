"""MCP Resources for Architectural Templates Catalog and Full Specifications."""

from __future__ import annotations

import json
from mcp.server.fastmcp import FastMCP

from architect_cad_mcp.templates.registry import TEMPLATES, get_template, list_templates


def register(mcp: FastMCP) -> None:
    @mcp.resource("cad://templates/catalog")
    def get_template_catalog_resource() -> str:
        """Catalog of ready-to-use architectural building templates across Houses, Buildings, and Workplaces."""
        return json.dumps({
            "total_templates": len(TEMPLATES),
            "templates": list_templates(),
        }, indent=2)

    @mcp.resource("cad://templates/{category}/{template_id}")
    def get_template_spec_resource(category: str, template_id: str) -> str:
        """Full architectural specification JSON for a specific template."""
        try:
            tpl = get_template(template_id)
            return json.dumps(tpl, indent=2)
        except KeyError as err:
            return json.dumps({"error": str(err)}, indent=2)
