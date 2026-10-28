"""Drawing lifecycle, specification inspection, delivery packages, and headless DXF/PNG operations."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from mcp.server.fastmcp import FastMCP

from architect_cad_mcp.domain.audit.dxf_audit import audit_dxf_file
from architect_cad_mcp.domain.drc.validator import audit_architecture_spec
from architect_cad_mcp.domain.engines.multi_plane import (
    generate_full_cd_package,
    generate_plane_dxf_and_svg,
)
from architect_cad_mcp.domain.rendering.png_renderer import render_dxf_file_to_png
from architect_cad_mcp.state import SESSION_STATE, error_response, ok_response


def register(mcp: FastMCP) -> None:
    @mcp.tool()
    def drawing(
        operation: str = "get_spec",
        title: str | None = None,
        category: str = "house",
        width: float = 15.6,
        depth: float = 11.2,
        scale: str = "1:100",
        output_dir: str = "cad_output/active_drawing",
        output_directory: str | None = None,
        dxf_path: str | None = None,
        png_path: str | None = None,
        plane: str = "floor_plan",
        dpi: int = 150,
        include_entities: bool = False,
        color_mode: str = "color",
    ) -> str:
        """Create, inspect, audit, render deterministic PNGs, or deliver a multi-plane 2D drawing package (headless ezdxf).

        Operations:
        - create: Initialize a new blank architectural building specification with structural perimeter walls.
        - get_spec: Return the active building specification JSON.
        - audit: Generate `plane` via headless ezdxf and return both Structured Geometry Audit + Neufert Architectural DRC.
        - audit_dxf: Parse and audit an existing `.dxf` file on disk (`dxf_path`) without AutoCAD.
        - render_preview: Render `plane` (or `dxf_path`) to a deterministic PNG with DPI, dimensions, and SHA-256 hash.
        - deliver_package: Validate the active spec and generate all 6 coordinated orthographic planes (.dxf, .png, .scr, .svg, manifest.json).
        """
        out_directory = output_directory or output_dir

        if operation == "create":
            w = float(width)
            d = float(depth)
            new_spec = {
                "id": "custom_drawing",
                "category": category,
                "summary": f"{title or 'CUSTOM ARCHITECTURAL PROJECT'} ({w:.1f}m x {d:.1f}m)",
                "project": {
                    "title": title or "CUSTOM ARCHITECTURAL PROJECT",
                    "category": category,
                    "sheetNumber": "A-101",
                    "scale": scale,
                    "units": "meters",
                    "northAngleDeg": 90,
                    "footprintWidth": w,
                    "footprintDepth": d,
                    "roofOverhang": 0.75,
                    "plinthElevation": 0.45,
                    "floorToFloorHeight": 3.15,
                    "parapetHeight": 0.45,
                },
                "grid": {
                    "vertical": [{"id": "A", "x": 0.0}, {"id": "B", "x": round(w * 0.5, 2)}, {"id": "C", "x": w}],
                    "horizontal": [{"id": "1", "y": 0.0}, {"id": "2", "y": round(d * 0.5, 2)}, {"id": "3", "y": d}],
                },
                "columns": [
                    {"id": "C-A1", "x": 0.0, "y": 0.0, "size": 0.30},
                    {"id": "C-C1", "x": w, "y": 0.0, "size": 0.30},
                    {"id": "C-A3", "x": 0.0, "y": d, "size": 0.30},
                    {"id": "C-C3", "x": w, "y": d, "size": 0.30},
                ],
                "walls": [
                    {"id": "W-SOUTH", "x1": 0.0, "y1": 0.0, "x2": w, "y2": 0.0, "thickness": 0.25, "type": "exterior"},
                    {"id": "W-NORTH", "x1": 0.0, "y1": d, "x2": w, "y2": d, "thickness": 0.25, "type": "exterior"},
                    {"id": "W-WEST", "x1": 0.0, "y1": 0.0, "x2": 0.0, "y2": d, "thickness": 0.25, "type": "exterior"},
                    {"id": "W-EAST", "x1": w, "y1": 0.0, "x2": w, "y2": d, "thickness": 0.25, "type": "exterior"},
                ],
                "rooms": [],
                "doors": [],
                "windows": [],
                "stairs": [],
                "sections": [
                    {"id": "A-A", "type": "longitudinal", "x1": -1.2, "y1": round(d * 0.5, 2), "x2": w + 1.2, "y2": round(d * 0.5, 2), "lookDirection": "north"},
                    {"id": "B-B", "type": "transverse", "x1": round(w * 0.5, 2), "y1": -1.2, "x2": round(w * 0.5, 2), "y2": d + 1.2, "lookDirection": "west"},
                ],
            }
            rev = SESSION_STATE.update_spec(new_spec)
            return ok_response({"created": new_spec["project"]}, revision=rev)

        if operation == "get_spec":
            return ok_response({"spec": SESSION_STATE.spec})

        if operation == "audit":
            active_spec = SESSION_STATE.spec
            plane_out = generate_plane_dxf_and_svg(active_spec, plane, Path(out_directory))
            arch_drc = audit_architecture_spec(active_spec)
            return ok_response({
                "backend": "ezdxf",
                "plane": plane,
                "entity_count": plane_out["entity_count"],
                "layer_count": plane_out["layer_count"],
                "counts_by_type": plane_out["counts_by_type"],
                "counts_by_layer": plane_out["counts_by_layer"],
                "bounds": plane_out["bounds"],
                "units": plane_out["units"],
                "geometry_digest": plane_out["geometry_digest"],
                "geometry_drc": plane_out["geometry_drc"],
                "architectural_drc": arch_drc,
                "dxf_path": plane_out["dxf_path"],
                "png_preview": plane_out["png_preview"],
            })

        if operation == "audit_dxf":
            if not dxf_path:
                return error_response("E_MISSING_DXF_PATH", "Provide 'dxf_path' to audit an existing DXF file.")
            try:
                report = audit_dxf_file(dxf_path, include_entities=include_entities)
            except Exception as err:
                return error_response("E_DXF_AUDIT_ERROR", str(err))
            return ok_response({"audit_dxf": report})

        if operation == "render_preview":
            if dxf_path:
                target_png = png_path or str(Path(dxf_path).with_suffix(".png"))
                png_info = render_dxf_file_to_png(dxf_path, target_png, dpi=dpi, color_mode=color_mode)
                return ok_response({"preview": png_info})
            active_spec = SESSION_STATE.spec
            plane_out = generate_plane_dxf_and_svg(active_spec, plane, Path(out_directory))
            return ok_response({"preview": plane_out["png_preview"], "dxf_path": plane_out["dxf_path"]})

        if operation == "deliver_package":
            pkg = generate_full_cd_package(SESSION_STATE.spec, Path(out_directory))
            return ok_response({"package": pkg, "manifest": pkg})

        return error_response("E_INVALID_OPERATION", f"Unknown drawing operation: {operation}")
