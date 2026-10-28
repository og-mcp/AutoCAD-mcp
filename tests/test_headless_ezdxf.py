"""Headless ezdxf workflow tests: structured audit, digest round-trip, deterministic PNG."""

from __future__ import annotations

import json
from pathlib import Path

from architect_cad_mcp.dxf_audit import audit_dxf_file
from architect_cad_mcp.multi_plane_engine import generate_plane_dxf_and_svg
from architect_cad_mcp.server import drawing, system, template
from architect_cad_mcp.templates import TEMPLATES, get_template


def test_status_reports_headless_backend() -> None:
    status = json.loads(system("status"))
    assert status["backend"] == "ezdxf"
    assert status["requires_autocad"] is False
    assert status["validation_feedback"] == "Structured audit + deterministic PNG"


def test_structured_audit_contents(tmp_path: Path) -> None:
    out = generate_plane_dxf_and_svg(get_template("courtyard_residence"), "floor_plan", tmp_path)
    assert out["backend"] == "ezdxf"
    assert out["units"]["name"] == "meters"
    assert out["geometry_drc"]["status"] == "PASS"
    assert out["counts_by_layer"]["A-WALL-FULL"] >= 10
    assert out["counts_by_layer"]["A-DOOR-SWNG"] == 7
    assert "ARC" in out["counts_by_type"]
    assert out["bounds"]["size"][0] > 15.6  # footprint plus dimensions/grid
    assert len(out["geometry_digest"]) == 64
    assert Path(out["audit_json_path"]).exists()


def test_exported_dxf_digest_round_trips(tmp_path: Path) -> None:
    out = generate_plane_dxf_and_svg(get_template("modern_family_villa"), "rcp", tmp_path)
    reaudit = audit_dxf_file(out["dxf_path"])
    assert reaudit["geometry_digest"] == out["geometry_digest"]
    assert reaudit["entity_count"] == out["entity_count"]
    assert reaudit["file_sha256"] == out["dxf_sha256"]


def test_png_is_deterministic(tmp_path: Path) -> None:
    spec = get_template("open_workplace_office")
    first = generate_plane_dxf_and_svg(spec, "floor_plan", tmp_path / "run1")
    second = generate_plane_dxf_and_svg(spec, "floor_plan", tmp_path / "run2")
    p1, p2 = first["png_preview"], second["png_preview"]
    assert p1["width"] > 500 and p1["height"] > 300
    assert p1["sha256"] == p2["sha256"], "PNG output must be byte-identical for identical geometry"
    assert first["geometry_digest"] == second["geometry_digest"]


def test_every_template_and_plane_renders_png(tmp_path: Path) -> None:
    for tid in TEMPLATES:
        result = json.loads(template("instantiate_template", template_id=tid, output_dir=str(tmp_path / tid)))
        assert result["package"]["ok"] is True
        for plane_key, info in result["package"]["planes"].items():
            assert info["geometry_drc"]["status"] == "PASS", f"{tid}/{plane_key}"
            assert Path(info["png_preview"]["path"]).stat().st_size > 5000, f"{tid}/{plane_key}"


def test_mcp_drawing_audit_and_render_operations(tmp_path: Path) -> None:
    template("instantiate_template", template_id="compact_urban_townhouse")
    audit = json.loads(drawing("audit", plane="floor_plan", output_dir=str(tmp_path)))
    assert audit["ok"] and audit["geometry_drc"]["status"] == "PASS"
    assert audit["architectural_drc"]["drc_status"] == "PASS"

    audit_dxf = json.loads(drawing("audit_dxf", dxf_path=audit["dxf_path"]))
    assert audit_dxf["audit_dxf"]["geometry_digest"] == audit["geometry_digest"]

    png = json.loads(drawing("render_preview", dxf_path=audit["dxf_path"], png_path=str(tmp_path / "re.png"), dpi=96))
    assert png["preview"]["dpi"] == 96 and Path(png["preview"]["path"]).exists()

    missing = json.loads(drawing("audit_dxf"))
    assert missing["ok"] is False and missing["error"]["code"] == "E_MISSING_DXF_PATH"
