"""Architectural Drafting Annotations: Dimensions, Grids, Bubbles, Datums, Title Block.

Adheres to AIA CAD Graphic Guidelines and Francis D.K. Ching drafting standards.
"""

from __future__ import annotations

from typing import Any

from architect_cad_mcp.core.layers import PLANE_CODES


def add_dxf_rect(msp: Any, layer: str, x: float, y: float, w: float, h: float) -> None:
    """Add a closed rectangular polyline boundary."""
    pts = [(x, y), (x + w, y), (x + w, y + h), (x, y + h), (x, y)]
    msp.add_lwpolyline(pts, dxfattribs={"layer": layer})


def add_dxf_poche(msp: Any, layer: str, x: float, y: float, w: float, h: float) -> None:
    """Solid-fill poché hatch for cut walls and structural columns."""
    hatch = msp.add_hatch(dxfattribs={"layer": layer, "color": 256})
    hatch.set_solid_fill(color=256)
    hatch.paths.add_polyline_path([(x, y), (x + w, y), (x + w, y + h), (x, y + h)], is_closed=True)


def add_dxf_arch_dim_h(
    msp: Any, layer: str, x1: float, x2: float, y_dim: float, y_origin: float, label: str
) -> None:
    """Add horizontal dimension line with 45-degree architectural slash ticks."""
    tick = 0.16
    sign = 1.0 if y_dim >= y_origin else -1.0
    msp.add_line((x1, y_origin + 0.12 * sign), (x1, y_dim + 0.16 * sign), dxfattribs={"layer": layer})
    msp.add_line((x2, y_origin + 0.12 * sign), (x2, y_dim + 0.16 * sign), dxfattribs={"layer": layer})
    msp.add_line((x1, y_dim), (x2, y_dim), dxfattribs={"layer": layer})
    # 45-degree architectural slash ticks
    msp.add_line((x1 - tick, y_dim - tick), (x1 + tick, y_dim + tick), dxfattribs={"layer": layer})
    msp.add_line((x2 - tick, y_dim - tick), (x2 + tick, y_dim + tick), dxfattribs={"layer": layer})
    msp.add_text(
        label,
        dxfattribs={
            "layer": layer,
            "height": 0.18,
            "insert": ((x1 + x2) * 0.5 - len(label) * 0.055, y_dim + 0.10),
        },
    )


def add_dxf_arch_dim_v(
    msp: Any, layer: str, y1: float, y2: float, x_dim: float, x_origin: float, label: str
) -> None:
    """Add vertical dimension line with 45-degree architectural slash ticks."""
    tick = 0.16
    sign = 1.0 if x_dim >= x_origin else -1.0
    msp.add_line((x_origin + 0.12 * sign, y1), (x_dim + 0.16 * sign, y1), dxfattribs={"layer": layer})
    msp.add_line((x_origin + 0.12 * sign, y2), (x_dim + 0.16 * sign, y2), dxfattribs={"layer": layer})
    msp.add_line((x_dim, y1), (x_dim, y2), dxfattribs={"layer": layer})
    msp.add_line((x_dim - tick, y1 - tick), (x_dim + tick, y1 + tick), dxfattribs={"layer": layer})
    msp.add_line((x_dim - tick, y2 - tick), (x_dim + tick, y2 + tick), dxfattribs={"layer": layer})
    msp.add_text(
        label,
        dxfattribs={
            "layer": layer,
            "height": 0.18,
            "rotation": 90.0,
            "insert": (x_dim - 0.12, (y1 + y2) * 0.5 - len(label) * 0.055),
        },
    )


def add_common_grid_and_frame(msp: Any, spec: dict[str, Any], plane_key: str) -> None:
    """Construct structural grid lines, axis bubbles, 3-tier dimensions, and title block."""
    project = spec["project"]
    W = float(project["footprintWidth"])
    D = float(project["footprintDepth"])
    meta = PLANE_CODES[plane_key]

    # Grid lines & bubbles (bubbles sit cleanly outside the 3-tier dimension strings)
    for vg in spec["grid"]["vertical"]:
        x = float(vg["x"])
        msp.add_line((x, -1.5), (x, D + 2.15), dxfattribs={"layer": "A-GRID"})
        msp.add_circle((x, D + 2.45), 0.30, dxfattribs={"layer": "A-GRID-IDEN"})
        msp.add_text(vg["id"], dxfattribs={"layer": "A-GRID-IDEN", "height": 0.22, "insert": (x - 0.08, D + 2.35)})

    for hg in spec["grid"]["horizontal"]:
        y = float(hg["y"])
        msp.add_line((-2.15, y), (W + 1.5, y), dxfattribs={"layer": "A-GRID"})
        msp.add_circle((-2.45, y), 0.30, dxfattribs={"layer": "A-GRID-IDEN"})
        msp.add_text(hg["id"], dxfattribs={"layer": "A-GRID-IDEN", "height": 0.22, "insert": (-2.53, y - 0.09)})

    # 3-tier exterior dimensions
    v_grids = spec["grid"]["vertical"]
    for i in range(len(v_grids) - 1):
        gx1, gx2 = float(v_grids[i]["x"]), float(v_grids[i + 1]["x"])
        add_dxf_arch_dim_h(msp, "A-ANNO-DIMS", gx1, gx2, D + 1.0, D, f"{gx2 - gx1:.2f}m")
    add_dxf_arch_dim_h(msp, "A-ANNO-DIMS", 0.0, W, D + 1.55, D, f"{W:.2f}m OVERALL")

    h_grids = spec["grid"]["horizontal"]
    for i in range(len(h_grids) - 1):
        gy1, gy2 = float(h_grids[i]["y"]), float(h_grids[i + 1]["y"])
        add_dxf_arch_dim_v(msp, "A-ANNO-DIMS", gy1, gy2, -1.0, 0.0, f"{gy2 - gy1:.2f}m")
    add_dxf_arch_dim_v(msp, "A-ANNO-DIMS", 0.0, D, -1.55, 0.0, f"{D:.2f}m OVERALL")

    # Sheet border & title block
    add_dxf_rect(msp, "A-TTLB", -3.4, -3.2, W + 6.6, D + 6.8)
    msp.add_text(
        f"{meta['sheet_prefix']} | {project['title']} - {meta['title']} | SCALE {project['scale']} | NORTH UP",
        dxfattribs={"layer": "A-TTLB", "height": 0.24, "insert": (-2.8, -2.85)},
    )
