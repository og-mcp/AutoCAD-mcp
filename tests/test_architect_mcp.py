"""Test suite for architect-cad-mcp server, templates, validator, and multi-plane engine."""

from __future__ import annotations

import json
from pathlib import Path

from architect_cad_mcp.server import (
    arch_audit,
    arch_element,
    autocad_live,
    drawing,
    orthographic_plane,
    system,
    template,
)
from architect_cad_mcp.templates import TEMPLATES, get_template
from architect_cad_mcp.validator import audit_architecture_spec


def test_all_six_templates_pass_neufert_drc() -> None:
    assert len(TEMPLATES) == 6
    for tid in TEMPLATES:
        spec = get_template(tid)
        drc = audit_architecture_spec(spec)
        assert drc["drc_status"] == "PASS", f"Template {tid} failed DRC: {drc['errors']}"
        assert drc["counts"]["errors"] == 0


def test_mcp_tools_end_to_end(tmp_path: Path) -> None:
    sys_status = json.loads(system("status"))
    assert sys_status["ok"] is True
    assert sys_status["aia_layer_count"] == 25

    tpl_list = json.loads(template("list_templates", category="workplace"))
    assert tpl_list["ok"] is True
    assert len(tpl_list["templates"]) == 2

    inst = json.loads(
        template(
            "instantiate_template",
            template_id="open_workplace_office",
            output_dir=str(tmp_path / "workplace_out"),
        )
    )
    assert inst["ok"] is True
    assert inst["package"]["ok"] is True
    assert len(inst["package"]["planes"]) == 6

    for plane_key, plane_info in inst["package"]["planes"].items():
        assert Path(plane_info["dxf_path"]).exists(), f"Missing DXF for {plane_key}"
        assert Path(plane_info["scr_path"]).exists(), f"Missing SCR for {plane_key}"
        assert Path(plane_info["svg_path"]).exists(), f"Missing SVG for {plane_key}"
        assert plane_info["entity_count"] > 10

    audit_res = json.loads(arch_audit("validate_anthropometrics"))
    assert audit_res["ok"] is True
    assert audit_res["audit"]["drc_status"] == "PASS"

    lisp_res = json.loads(autocad_live("get_lisp_dispatcher_path"))
    assert lisp_res["ok"] is True
    assert lisp_res["exists"] is True


def test_custom_drawing_and_arch_elements(tmp_path: Path) -> None:
    created = json.loads(drawing("create", title="TEST PAVILION", width=12.0, depth=8.0))
    assert created["ok"] is True

    r = json.loads(
        arch_element(
            "add_room",
            {
                "id": "01",
                "name": "STUDIO SALON",
                "type": "living",
                "zone": "SOCIAL PAVILION",
                "habitable": True,
                "wetRoom": False,
                "x": 0.0,
                "y": 0.0,
                "width": 12.0,
                "depth": 8.0,
            },
        )
    )
    assert r["ok"] is True

    w = json.loads(
        arch_element(
            "punch_window",
            {
                "id": "W-1",
                "room": "01",
                "wall": "north",
                "x1": 1.0,
                "y1": 8.0,
                "x2": 9.0,
                "y2": 8.0,
                "sill": 0.4,
                "head": 2.4,
            },
        )
    )
    assert w["ok"] is True

    plane_res = json.loads(
        orthographic_plane("generate_plane", plane="floor_plan", output_dir=str(tmp_path / "custom"))
    )
    assert plane_res["ok"] is True
    assert Path(plane_res["plane_output"]["dxf_path"]).exists()
