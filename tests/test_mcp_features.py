"""Test suite for MCP Resources, MCP Prompts, and Modular Tool Extensibility."""

from __future__ import annotations

import json
from pathlib import Path

from mcp.server.fastmcp import FastMCP

from architect_cad_mcp.app import create_app
from architect_cad_mcp.server import mcp
from architect_cad_mcp.tools import register_all_tools


def test_mcp_resources_are_registered_and_readable() -> None:
    """Verify all static architectural resources return valid JSON."""
    resource_mgr = mcp._resource_manager
    expected_uris = [
        "cad://standards/layers",
        "cad://standards/furniture-catalog",
        "cad://standards/drc-rules",
        "cad://templates/catalog",
        "cad://drawing/active/spec",
        "cad://drawing/active/drc",
        "cad://drawing/active/planes",
    ]
    for uri in expected_uris:
        assert uri in resource_mgr._resources, f"Missing resource: {uri}"
        res_obj = resource_mgr._resources[uri]
        payload = json.loads(res_obj.fn())
        assert isinstance(payload, dict)

    # Test template dynamic URI resource
    assert "cad://templates/{category}/{template_id}" in resource_mgr._templates
    tpl_res = resource_mgr._templates["cad://templates/{category}/{template_id}"]
    courtyard_json = json.loads(tpl_res.fn(category="house", template_id="courtyard_residence"))
    assert courtyard_json["project"]["title"] == "TRAVERTINE COURTYARD RESIDENCE"


def test_mcp_prompts_are_registered_and_callable() -> None:
    """Verify all architectural prompts generate rich instructions."""
    prompt_mgr = mcp._prompt_manager
    expected_prompts = [
        "design_house",
        "design_apartment_floor",
        "design_workplace",
        "audit_floor_plan",
        "generate_coordinated_cd_set",
    ]
    for name in expected_prompts:
        assert name in prompt_mgr._prompts, f"Missing prompt: {name}"

    # Test invoking design_house prompt
    house_prompt = prompt_mgr._prompts["design_house"].fn(
        site_width_m=20.0, site_depth_m=15.0, bedroom_count=4, include_courtyard=True
    )
    assert "Pattern 115" in house_prompt
    assert "20.00 meters" in house_prompt

    # Test invoking audit_floor_plan prompt
    audit_prompt = prompt_mgr._prompts["audit_floor_plan"].fn(
        strict_neufert=True, check_daylight=True, check_blondel_stairs=True
    )
    assert "Blondel" in audit_prompt
    assert "Neufert" in audit_prompt


def test_easy_custom_tool_extensibility() -> None:
    """Demonstrate how easily a new architectural tool can be added following Open/Closed Principle."""
    custom_server = create_app("custom-architect-server")

    # Define a custom 9th tool in 5 lines
    def custom_solar_analysis_tool(mcp_app: FastMCP) -> None:
        @mcp_app.tool()
        def solar_analysis(azimuth_deg: float = 180.0, latitude_deg: float = 37.77) -> str:
            """Compute passive solar exposure for South/North fenestrations."""
            return json.dumps({
                "ok": True,
                "solar_exposure": "Optimal South solar gain",
                "azimuth": azimuth_deg,
                "latitude": latitude_deg,
            })

    # Register the new tool
    custom_solar_analysis_tool(custom_server)

    # Verify tool exists and executes
    assert "solar_analysis" in custom_server._tool_manager._tools
    tool_fn = custom_server._tool_manager.get_tool("solar_analysis").fn
    result = json.loads(tool_fn(azimuth_deg=180.0, latitude_deg=37.77))
    assert result["ok"] is True
    assert result["solar_exposure"] == "Optimal South solar gain"
