"""Multi-Plane 2D Orthographic CAD Engine (ezdxf + AutoCAD .scr + Architectural SVG)."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import ezdxf

from architect_cad_mcp.core.constants import FURNITURE_AND_FIXTURE_CATALOG
from architect_cad_mcp.core.layers import AIA_ARCHITECTURAL_LAYERS, PLANE_CODES
from architect_cad_mcp.domain.audit.dxf_audit import audit_ezdxf_document
from architect_cad_mcp.domain.drc.validator import audit_architecture_spec
from architect_cad_mcp.domain.engines.annotations import (
    add_common_grid_and_frame,
    add_dxf_arch_dim_v,
    add_dxf_poche,
    add_dxf_rect,
)
from architect_cad_mcp.domain.engines.walls import wall_segments_with_openings
from architect_cad_mcp.domain.rendering.png_renderer import render_dxf_to_png


def setup_ezdxf_document() -> tuple[ezdxf.document.Drawing, Any]:
    """Create a new DXF document configured for metric meters with 25 AIA standard layers."""
    doc = ezdxf.new("R2013")
    doc.header["$INSUNITS"] = 6  # 6 = Meters
    for lyr in AIA_ARCHITECTURAL_LAYERS:
        name = lyr["name"]
        if name not in doc.layers:
            doc.layers.add(
                name=name,
                color=int(lyr["color"]),
                dxfattribs={"lineweight": int(lyr["dxf_lw"])},
            )
    return doc, doc.modelspace()


def generate_plane_dxf_and_svg(
    spec: dict[str, Any], plane_key: str, out_dir: Path
) -> dict[str, Any]:
    """Generate a single orthographic plane (.dxf, .scr, .svg) with SHA-256 verification."""
    if plane_key not in PLANE_CODES:
        raise ValueError(f"Unsupported plane '{plane_key}'. Valid planes: {list(PLANE_CODES.keys())}")

    out_dir.mkdir(parents=True, exist_ok=True)
    doc, msp = setup_ezdxf_document()
    project = spec["project"]
    W = float(project["footprintWidth"])
    D = float(project["footprintDepth"])
    H = float(project.get("floorToFloorHeight", 3.15))
    plinth = float(project.get("plinthElevation", 0.30))
    parapet = float(project.get("parapetHeight", 0.45))
    overhang = float(project.get("roofOverhang", 0.70))

    if plane_key in ("floor_plan", "rcp", "structural_plan", "roof_plan"):
        add_common_grid_and_frame(msp, spec, plane_key)

    if plane_key == "floor_plan":
        # Columns with solid poché
        for col in spec.get("columns", []):
            cx, cy, sz = float(col["x"]), float(col["y"]), float(col["size"])
            add_dxf_rect(msp, "A-COLS", cx - sz * 0.5, cy - sz * 0.5, sz, sz)
            add_dxf_poche(msp, "A-COLS", cx - sz * 0.5, cy - sz * 0.5, sz, sz)

        # Cut walls with solid poché and door/window opening intervals subtracted
        for wall in spec.get("walls", []):
            for rect in wall_segments_with_openings(wall, spec):
                add_dxf_rect(msp, "A-WALL-FULL", *rect)
                add_dxf_poche(msp, "A-WALL-PATT", *rect)

        # Doors with 90-degree swing arcs
        for door in spec.get("doors", []):
            dx, dy, dw = float(door["x"]), float(door["y"]), float(door["width"])
            if door.get("orientation", "north") == "north":
                add_dxf_rect(msp, "A-DOOR", dx, dy, 0.05, dw)
                msp.add_arc((dx, dy), dw, 0.0, 90.0, dxfattribs={"layer": "A-DOOR-SWNG"})
            else:
                add_dxf_rect(msp, "A-DOOR", dx, dy - dw, 0.05, dw)
                msp.add_arc((dx, dy), dw, 270.0, 360.0, dxfattribs={"layer": "A-DOOR-SWNG"})

        # Windows with glazing lines and exterior sill projections
        for win in spec.get("windows", []):
            x1, y1, x2, y2 = float(win["x1"]), float(win["y1"]), float(win["x2"]), float(win["y2"])
            msp.add_line((x1, y1), (x2, y2), dxfattribs={"layer": "A-GLAZ-SILL"})
            if abs(y2 - y1) < 1e-4:
                msp.add_line((x1, y1 - 0.04), (x2, y2 - 0.04), dxfattribs={"layer": "A-GLAZ"})
                msp.add_line((x1, y1 + 0.04), (x2, y2 + 0.04), dxfattribs={"layer": "A-GLAZ"})
            else:
                msp.add_line((x1 - 0.04, y1), (x2 - 0.04, y2), dxfattribs={"layer": "A-GLAZ"})
                msp.add_line((x1 + 0.04, y1), (x2 + 0.04, y2), dxfattribs={"layer": "A-GLAZ"})

        # Stairs with treads and UP label
        for stair in spec.get("stairs", []):
            sx, sy = float(stair["x"]), float(stair["y"])
            sw = float(stair["widthM"])
            rcount = int(stair["riserCount"])
            tread_m = float(stair["treadMm"]) / 1000.0
            run_len = max(rcount - 1, 1) * tread_m
            add_dxf_rect(msp, "A-STAIR", sx, sy, sw, run_len)
            for r_idx in range(1, rcount):
                ry = sy + r_idx * tread_m
                msp.add_line((sx, ry), (sx + sw, ry), dxfattribs={"layer": "A-STAIR"})
            msp.add_text(f"UP {rcount}R", dxfattribs={"layer": "A-STAIR", "height": 0.14, "insert": (sx + 0.15, sy + 0.15)})

        add_dxf_rect(msp, "A-OVER", -overhang, -overhang, W + 2 * overhang, D + 2 * overhang)

        # Rooms and scaled furniture footprints
        for room in spec.get("rooms", []):
            rx, ry = float(room["x"]), float(room["y"])
            rw, rd = float(room["width"]), float(room["depth"])
            cx, cy = rx + rw * 0.5, ry + rd * 0.5
            area = rw * rd
            msp.add_text(
                f"{room['id']} {room['name']}",
                dxfattribs={"layer": "A-ANNO-TEXT", "height": 0.20, "insert": (cx - 1.2, cy + 0.12)},
            )
            msp.add_text(
                f"{rw:.2f}m x {rd:.2f}m ({area:.1f}m2) | {room['zone']}",
                dxfattribs={"layer": "A-ANNO-TEXT", "height": 0.14, "insert": (cx - 1.2, cy - 0.18)},
            )
            for furn in room.get("furniture", []):
                item_def = FURNITURE_AND_FIXTURE_CATALOG.get(furn["item"])
                if item_def:
                    fx, fy = float(furn["x"]), float(furn["y"])
                    fw, fd = float(item_def["width"]), float(item_def["depth"])
                    add_dxf_rect(msp, item_def["layer"], fx, fy, fw, fd)
                    msp.add_text(
                        item_def["label"],
                        dxfattribs={"layer": item_def["layer"], "height": 0.11, "insert": (fx + 0.08, fy + fd * 0.45)},
                    )

        # Section Cut Callouts: Sit outside dimensions with arrow/circle heads
        for sec in spec.get("sections", []):
            sx1, sy1, sx2, sy2 = float(sec["x1"]), float(sec["y1"]), float(sec["x2"]), float(sec["y2"])
            msp.add_line((sx1, sy1), (sx2, sy2), dxfattribs={"layer": "A-ANNO-SYMB"})
            for bx, by in ((sx1, sy1), (sx2, sy2)):
                msp.add_circle((bx, by), 0.32, dxfattribs={"layer": "A-ANNO-SYMB"})
                msp.add_text(sec["id"], dxfattribs={"layer": "A-ANNO-SYMB", "height": 0.18, "insert": (bx - 0.15, by - 0.08)})

    elif plane_key == "rcp":
        # Reflected Ceiling Plan
        for wall in spec.get("walls", []):
            x1, y1, x2, y2 = float(wall["x1"]), float(wall["y1"]), float(wall["x2"]), float(wall["y2"])
            t = float(wall["thickness"])
            if abs(y2 - y1) < 1e-4:
                add_dxf_rect(msp, "A-WALL-FULL", min(x1, x2), y1 - t * 0.5, abs(x2 - x1), t)
            else:
                add_dxf_rect(msp, "A-WALL-FULL", x1 - t * 0.5, min(y1, y2), t, abs(y2 - y1))

        for room in spec.get("rooms", []):
            rx, ry = float(room["x"]), float(room["y"])
            rw, rd = float(room["width"]), float(room["depth"])
            ch = float(room.get("ceilingHeight", 2.85))
            cx, cy = rx + rw * 0.5, ry + rd * 0.5
            add_dxf_rect(msp, "A-ANNO-SYMB", cx - 1.1, cy - 0.25, 2.2, 0.50)
            msp.add_text(
                f"{room['id']} CLG +{ch:.2f}m GYP",
                dxfattribs={"layer": "A-ANNO-TEXT", "height": 0.16, "insert": (cx - 0.95, cy - 0.06)},
            )
            for lx in (rx + rw * 0.28, rx + rw * 0.72):
                for ly in (ry + rd * 0.28, ry + rd * 0.72):
                    msp.add_circle((lx, ly), 0.12, dxfattribs={"layer": "E-LITE"})
            if room.get("habitable", True):
                hx, hy = rx + rw * 0.5 - 0.20, ry + rd * 0.78 - 0.20
                add_dxf_rect(msp, "M-HVAC", hx, hy, 0.40, 0.40)
                msp.add_line((hx, hy), (hx + 0.40, hy + 0.40), dxfattribs={"layer": "M-HVAC"})
                msp.add_line((hx + 0.40, hy), (hx, hy + 0.40), dxfattribs={"layer": "M-HVAC"})

    elif plane_key == "structural_plan":
        # Structural Foundation & Framing Plan
        for col in spec.get("columns", []):
            cx, cy, sz = float(col["x"]), float(col["y"]), float(col["size"])
            foot_sz = 1.40
            add_dxf_rect(msp, "S-FOOT", cx - foot_sz * 0.5, cy - foot_sz * 0.5, foot_sz, foot_sz)
            add_dxf_rect(msp, "A-COLS", cx - sz * 0.5, cy - sz * 0.5, sz, sz)
            msp.add_text(
                f"F1/{col['id']}",
                dxfattribs={"layer": "A-ANNO-TEXT", "height": 0.14, "insert": (cx + 0.22, cy + 0.22)},
            )

        for vg in spec["grid"]["vertical"]:
            gx = float(vg["x"])
            add_dxf_rect(msp, "S-BEAM", gx - 0.125, 0.0, 0.25, D)
        for hg in spec["grid"]["horizontal"]:
            gy = float(hg["y"])
            add_dxf_rect(msp, "S-BEAM", 0.0, gy - 0.125, W, 0.25)

        msp.add_text(
            "S1: 150mm TWO-WAY RCC SLAB OVER 230x450mm GRADE BEAMS",
            dxfattribs={"layer": "A-ANNO-TEXT", "height": 0.20, "insert": (W * 0.25, D * 0.50)},
        )

    elif plane_key == "roof_plan":
        # Roof & Drainage Plan
        add_dxf_rect(msp, "A-ROOF", -overhang, -overhang, W + 2 * overhang, D + 2 * overhang)
        add_dxf_rect(msp, "A-ROOF", 0.0, 0.0, W, D)
        for drain_x in (W * 0.25, W * 0.75):
            drain_y = D * 0.50
            msp.add_circle((drain_x, drain_y), 0.18, dxfattribs={"layer": "A-ROOF"})
            msp.add_text("RD Ø100", dxfattribs={"layer": "A-ANNO-TEXT", "height": 0.16, "insert": (drain_x + 0.24, drain_y - 0.06)})
            msp.add_line((drain_x, D - 0.6), (drain_x, drain_y + 0.3), dxfattribs={"layer": "A-ROOF"})
            msp.add_line((drain_x, 0.6), (drain_x, drain_y - 0.3), dxfattribs={"layer": "A-ROOF"})
            msp.add_text("2% SLOPE TO DRAIN", dxfattribs={"layer": "A-ANNO-TEXT", "height": 0.16, "insert": (drain_x - 0.85, D * 0.75)})

    elif plane_key == "elevations":
        # South & North Elevations
        total_h = plinth + H + parapet
        for idx, (elev_title, y_base) in enumerate([("SOUTH ELEVATION", 0.0), ("NORTH ELEVATION", total_h + 3.5)]):
            msp.add_line((-2.0, y_base), (W + 2.0, y_base), dxfattribs={"layer": "A-ELEV-PROF"})
            add_dxf_rect(msp, "A-ELEV-PROF", 0.0, y_base, W, plinth)
            add_dxf_rect(msp, "A-ELEV-PROF", 0.0, y_base + plinth, W, H)
            add_dxf_rect(msp, "A-ROOF", -overhang, y_base + plinth + H - 0.25, W + 2 * overhang, 0.25 + parapet)

            wall_filter = "south" if idx == 0 else "north"
            for win in spec.get("windows", []):
                if win.get("wall") == wall_filter:
                    wx1, wx2 = min(float(win["x1"]), float(win["x2"])), max(float(win["x1"]), float(win["x2"]))
                    sill = float(win.get("sill", 0.60))
                    head = float(win.get("head", 2.40))
                    add_dxf_rect(msp, "A-GLAZ", wx1, y_base + plinth + sill, wx2 - wx1, head - sill)
                    msp.add_line((wx1, y_base + plinth + sill), ((wx1 + wx2) * 0.5, y_base + plinth + head), dxfattribs={"layer": "A-GLAZ-SILL"})
                    msp.add_line(((wx1 + wx2) * 0.5, y_base + plinth + head), (wx2, y_base + plinth + sill), dxfattribs={"layer": "A-GLAZ-SILL"})

            for lvl_name, lvl_z in [
                ("±0.00 GROUND", 0.0),
                (f"+{plinth:.2f} FFL", plinth),
                (f"+{plinth + H:.2f} ROOF SLAB", plinth + H),
                (f"+{total_h:.2f} PARAPET", total_h),
            ]:
                msp.add_line((W + 0.6, y_base + lvl_z), (W + 2.4, y_base + lvl_z), dxfattribs={"layer": "A-ANNO-SYMB"})
                msp.add_text(lvl_name, dxfattribs={"layer": "A-ANNO-TEXT", "height": 0.16, "insert": (W + 0.7, y_base + lvl_z + 0.08)})

            msp.add_text(
                f"{elev_title} (SCALE {project['scale']})",
                dxfattribs={"layer": "A-ANNO-TEXT", "height": 0.24, "insert": (0.0, y_base - 0.65)},
            )

        add_dxf_rect(msp, "A-TTLB", -3.0, -2.0, W + 7.5, (total_h + 3.5) * 2 + 1.5)

    elif plane_key == "sections":
        # Sections A-A & B-B
        total_h = plinth + H + parapet
        for idx, (sec_title, span_w, y_base) in enumerate([
            ("LONGITUDINAL SECTION A-A", W, 0.0),
            ("TRANSVERSE SECTION B-B", D, total_h + 4.2),
        ]):
            msp.add_line((-2.0, y_base), (span_w + 2.0, y_base), dxfattribs={"layer": "A-ELEV-PROF"})
            add_dxf_rect(msp, "S-FOOT", -0.4, y_base - 0.90, 1.1, 0.90)
            add_dxf_rect(msp, "S-FOOT", span_w - 0.7, y_base - 0.90, 1.1, 0.90)
            add_dxf_rect(msp, "A-WALL-FULL", 0.0, y_base, span_w, plinth)
            add_dxf_rect(msp, "A-WALL-FULL", 0.0, y_base + plinth, 0.25, H)
            add_dxf_rect(msp, "A-WALL-FULL", span_w - 0.25, y_base + plinth, 0.25, H)
            add_dxf_rect(msp, "A-WALL-FULL", -overhang, y_base + plinth + H, span_w + 2 * overhang, 0.25)
            add_dxf_rect(msp, "A-WALL-FULL", 0.0, y_base + plinth + H + 0.25, 0.25, parapet)
            add_dxf_rect(msp, "A-WALL-FULL", span_w - 0.25, y_base + plinth + H + 0.25, 0.25, parapet)

            if idx == 0:
                for vg in spec["grid"]["vertical"][1:-1]:
                    gx = float(vg["x"])
                    add_dxf_rect(msp, "A-WALL-FULL", gx - 0.08, y_base + plinth, 0.16, H)
            else:
                for hg in spec["grid"]["horizontal"][1:-1]:
                    gy = float(hg["y"])
                    add_dxf_rect(msp, "A-WALL-FULL", gy - 0.08, y_base + plinth, 0.16, H)

            add_dxf_arch_dim_v(msp, "A-ANNO-DIMS", y_base + plinth, y_base + plinth + H, -1.0, 0.0, f"{H:.2f}m CLEAR")
            msp.add_text(
                f"{sec_title} (SCALE {project['scale']})",
                dxfattribs={"layer": "A-ANNO-TEXT", "height": 0.24, "insert": (0.0, y_base - 1.35)},
            )

        add_dxf_rect(msp, "A-TTLB", -3.0, -2.5, max(W, D) + 7.5, (total_h + 4.2) * 2 + 1.5)

    meta = PLANE_CODES[plane_key]
    stem = f"{meta['sheet_prefix'].lower().replace('-', '_')}_{plane_key}"
    dxf_path = out_dir / f"{stem}.dxf"
    png_path = out_dir / f"{stem}.png"
    scr_path = out_dir / f"{stem}.scr"
    svg_path = out_dir / f"{stem}.svg"
    audit_path = out_dir / f"{stem}_audit.json"

    doc.saveas(str(dxf_path))
    structured_audit = audit_ezdxf_document(doc)
    png_info = render_dxf_to_png(doc, png_path, dpi=150, background="#FFFFFF", force=True)
    audit_path.write_text(json.dumps(structured_audit, indent=2), encoding="utf-8")

    scr_content = build_autocad_scr(spec, plane_key)
    scr_path.write_text(scr_content, encoding="utf-8")
    svg_content = build_plane_svg(spec, plane_key)
    svg_path.write_text(svg_content, encoding="utf-8")

    dxf_bytes = dxf_path.read_bytes()
    return {
        "backend": "ezdxf",
        "plane": plane_key,
        "sheet_number": meta["sheet_prefix"],
        "title": meta["title"],
        "entity_count": structured_audit["entity_count"],
        "layer_count": structured_audit["layer_count"],
        "counts_by_type": structured_audit["counts_by_type"],
        "counts_by_layer": structured_audit["counts_by_layer"],
        "bounds": structured_audit["bounds"],
        "units": structured_audit["units"],
        "geometry_digest": structured_audit["geometry_digest"],
        "geometry_drc": structured_audit["geometry_drc"],
        "dxf_path": str(dxf_path.resolve()),
        "dxf_sha256": hashlib.sha256(dxf_bytes).hexdigest(),
        "dxf_size_bytes": len(dxf_bytes),
        "png_preview": png_info,
        "scr_path": str(scr_path.resolve()),
        "svg_path": str(svg_path.resolve()),
        "audit_json_path": str(audit_path.resolve()),
    }


def build_autocad_scr(spec: dict[str, Any], plane_key: str) -> str:
    """Generate an executable AutoCAD / AutoCAD LT .scr script for the specified plane."""
    project = spec["project"]
    W = float(project["footprintWidth"])
    D = float(project["footprintDepth"])
    lines = [
        f"; AutoCAD 2D Architectural Script - {project['title']} ({plane_key})",
        "-UNITS 2 2 1 2 0 N",
    ]
    for lyr in AIA_ARCHITECTURAL_LAYERS:
        lines.append(f"-LAYER M {lyr['name']} C {lyr['color']} {lyr['name']} ")

    for vg in spec["grid"]["vertical"]:
        x = float(vg["x"])
        lines.append(f"-LAYER S A-GRID  LINE {x:.3f},-1.500 {x:.3f},{D + 1.5:.3f} ")
    for hg in spec["grid"]["horizontal"]:
        y = float(hg["y"])
        lines.append(f"-LAYER S A-GRID  LINE -1.500,{y:.3f} {W + 1.5:.3f},{y:.3f} ")

    for wall in spec.get("walls", []):
        x1, y1, x2, y2 = float(wall["x1"]), float(wall["y1"]), float(wall["x2"]), float(wall["y2"])
        t = float(wall["thickness"])
        if abs(y2 - y1) < 1e-4:
            lines.append(f"-LAYER S A-WALL-FULL  RECTANG {min(x1,x2):.3f},{y1-t*0.5:.3f} {max(x1,x2):.3f},{y1+t*0.5:.3f}")
        else:
            lines.append(f"-LAYER S A-WALL-FULL  RECTANG {x1-t*0.5:.3f},{min(y1,y2):.3f} {x1+t*0.5:.3f},{max(y1,y2):.3f}")

    lines.append("ZOOM E")
    return "\n".join(lines) + "\n"


def build_plane_svg(spec: dict[str, Any], plane_key: str) -> str:
    """Render a crisp 2D CAD sheet SVG for instant visual inspection."""
    project = spec["project"]
    meta = PLANE_CODES[plane_key]
    W = float(project["footprintWidth"])
    D = float(project["footprintDepth"])
    H = float(project.get("floorToFloorHeight", 3.15))
    plinth = float(project.get("plinthElevation", 0.30))
    parapet = float(project.get("parapetHeight", 0.45))
    overhang = float(project.get("roofOverhang", 0.70))
    scale = 44.0
    pad_x, pad_y = 170.0, 150.0
    svg_w = int(W * scale + pad_x * 2)
    svg_h = int(D * scale + pad_y * 2)

    def sx(x: float) -> float:
        return pad_x + x * scale

    def sy(y: float) -> float:
        return svg_h - pad_y - y * scale

    el: list[str] = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_w} {svg_h}" width="{svg_w}" height="{svg_h}" style="background:#F8FAFC;font-family:\'Inter\',\'Helvetica Neue\',monospace;">',
        f'<rect x="16" y="16" width="{svg_w - 32}" height="{svg_h - 32}" fill="none" stroke="#0F172A" stroke-width="2.2"/>',
        f'<rect x="22" y="22" width="{svg_w - 44}" height="{svg_h - 44}" fill="none" stroke="#334155" stroke-width="0.7"/>',
    ]

    if plane_key in ("floor_plan", "rcp", "structural_plan", "roof_plan"):
        for vg in spec["grid"]["vertical"]:
            gx = sx(float(vg["x"]))
            el.append(f'<line x1="{gx:.1f}" y1="{sy(-1.4):.1f}" x2="{gx:.1f}" y2="{sy(D + 1.4):.1f}" stroke="#94A3B8" stroke-width="0.75" stroke-dasharray="10,4,2,4"/>')
            el.append(f'<circle cx="{gx:.1f}" cy="{sy(D + 1.85):.1f}" r="12" fill="#FFFFFF" stroke="#0F172A" stroke-width="1.2"/>')
            el.append(f'<text x="{gx:.1f}" y="{sy(D + 1.85) + 4:.1f}" text-anchor="middle" font-size="10.5" font-weight="700" fill="#0F172A">{vg["id"]}</text>')

        for hg in spec["grid"]["horizontal"]:
            gy = sy(float(hg["y"]))
            el.append(f'<line x1="{sx(-1.4):.1f}" y1="{gy:.1f}" x2="{sx(W + 1.4):.1f}" y2="{gy:.1f}" stroke="#94A3B8" stroke-width="0.75" stroke-dasharray="10,4,2,4"/>')
            el.append(f'<circle cx="{sx(-1.85):.1f}" cy="{gy:.1f}" r="12" fill="#FFFFFF" stroke="#0F172A" stroke-width="1.2"/>')
            el.append(f'<text x="{sx(-1.85):.1f}" y="{gy + 4:.1f}" text-anchor="middle" font-size="10.5" font-weight="700" fill="#0F172A">{hg["id"]}</text>')

        for wall in spec.get("walls", []):
            x1, y1, x2, y2 = float(wall["x1"]), float(wall["y1"]), float(wall["x2"]), float(wall["y2"])
            t = float(wall["thickness"])
            if abs(y2 - y1) < 1e-4:
                wx, wy, ww, wh = sx(min(x1, x2)), sy(y1 + t * 0.5), abs(x2 - x1) * scale, t * scale
            else:
                wx, wy, ww, wh = sx(x1 - t * 0.5), sy(max(y1, y2)), t * scale, abs(y2 - y1) * scale
            el.append(f'<rect x="{wx:.1f}" y="{wy:.1f}" width="{ww:.1f}" height="{wh:.1f}" fill="#334155" stroke="#0F172A" stroke-width="1.8"/>')

        for room in spec.get("rooms", []):
            rx, ry = float(room["x"]), float(room["y"])
            rw, rd = float(room["width"]), float(room["depth"])
            cx, cy = sx(rx + rw * 0.5), sy(ry + rd * 0.5)
            area = rw * rd
            sub = f"CLG +{float(room.get('ceilingHeight', 2.85)):.2f}m" if plane_key == "rcp" else f"{rw:.2f}m × {rd:.2f}m · {area:.1f} m²"
            el.append(f'<text x="{cx:.1f}" y="{cy - 5:.1f}" text-anchor="middle" font-size="10" font-weight="700" fill="#0F172A">{room["id"]} {room["name"]}</text>')
            el.append(f'<text x="{cx:.1f}" y="{cy + 10:.1f}" text-anchor="middle" font-size="9" fill="#475569">{sub}</text>')

    else:
        total_h = plinth + H + parapet
        el.append(f'<line x1="{sx(-1.5):.1f}" y1="{sy(2.0):.1f}" x2="{sx(W + 1.5):.1f}" y2="{sy(2.0):.1f}" stroke="#0F172A" stroke-width="3.0"/>')
        el.append(f'<rect x="{sx(0.0):.1f}" y="{sy(2.0 + total_h):.1f}" width="{W * scale:.1f}" height="{total_h * scale:.1f}" fill="#E2E8F0" stroke="#0F172A" stroke-width="2.0"/>')
        el.append(f'<text x="{sx(W * 0.5):.1f}" y="{sy(2.0 + total_h * 0.5):.1f}" text-anchor="middle" font-size="13" font-weight="700" fill="#0F172A">{meta["title"]} (H = {total_h:.2f}m)</text>')

    el.append(
        f'<text x="36" y="{svg_h - 32}" font-size="11.5" font-weight="700" fill="#0F172A">{meta["sheet_prefix"]} · {project["title"]} · {meta["title"]} · SCALE {project["scale"]} · ↑ N</text>'
    )
    el.append("</svg>")
    return "\n".join(el)


def generate_full_cd_package(spec: dict[str, Any], out_dir: Path) -> dict[str, Any]:
    """Generate all 6 coordinated orthographic planes + DRC validation report + SHA-256 manifest."""
    out_dir.mkdir(parents=True, exist_ok=True)
    drc_report = audit_architecture_spec(spec)
    planes_output: dict[str, Any] = {}
    for plane_key in PLANE_CODES:
        planes_output[plane_key] = generate_plane_dxf_and_svg(spec, plane_key, out_dir)

    spec_path = out_dir / "building_spec.json"
    spec_path.write_text(json.dumps(spec, indent=2), encoding="utf-8")

    manifest = {
        "ok": drc_report["drc_status"] == "PASS",
        "project": spec["project"],
        "drc_report": drc_report,
        "planes": planes_output,
        "spec_path": str(spec_path.resolve()),
    }
    manifest_path = out_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    manifest["manifest_path"] = str(manifest_path.resolve())
    return manifest
