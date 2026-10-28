#!/usr/bin/env python3
"""
Generate a standards-compliant AutoCAD 2D Floor Plan (.dxf), AutoCAD Script (.scr),
and high-precision architectural sheet (.svg) with AIA layers, lineweights,
45-degree architectural dimension ticks, structural grids, door swing arcs,
and section callouts from a declarative building specification JSON.
"""

import argparse
import json
import math
from pathlib import Path

AIA_LAYERS = [
    ("A-GRID", 8, "CENTER2", 9),
    ("A-GRID-IDEN", 7, "CONTINUOUS", 25),
    ("A-COLS", 7, "CONTINUOUS", 50),
    ("A-WALL-FULL", 7, "CONTINUOUS", 50),
    ("A-WALL-PATT", 253, "CONTINUOUS", 9),
    ("A-DOOR", 3, "CONTINUOUS", 20),
    ("A-DOOR-SWNG", 8, "CONTINUOUS", 13),
    ("A-GLAZ", 4, "CONTINUOUS", 25),
    ("A-GLAZ-SILL", 8, "CONTINUOUS", 13),
    ("A-STAIR", 3, "CONTINUOUS", 20),
    ("A-OVER", 1, "HIDDEN2", 15),
    ("A-ANNO-DIMS", 6, "CONTINUOUS", 13),
    ("A-ANNO-TEXT", 7, "CONTINUOUS", 20),
    ("A-ANNO-SYMB", 7, "CONTINUOUS", 25),
    ("A-TTLB", 7, "CONTINUOUS", 35),
]


class DXFBuilder:
    """Minimal, zero-dependency AutoCAD R12/LT2 compatible DXF writer with AIA layers."""

    def __init__(self) -> None:
        self.entities: list[str] = []

    def add_line(self, layer: str, x1: float, y1: float, x2: float, y2: float) -> None:
        self.entities.append(
            f"0\nLINE\n8\n{layer}\n10\n{x1:.4f}\n20\n{y1:.4f}\n30\n0.0\n11\n{x2:.4f}\n21\n{y2:.4f}\n31\n0.0"
        )

    def add_rect(self, layer: str, x: float, y: float, w: float, h: float) -> None:
        self.add_line(layer, x, y, x + w, y)
        self.add_line(layer, x + w, y, x + w, y + h)
        self.add_line(layer, x + w, y + h, x, y + h)
        self.add_line(layer, x, y + h, x, y)

    def add_circle(self, layer: str, cx: float, cy: float, r: float) -> None:
        self.entities.append(
            f"0\nCIRCLE\n8\n{layer}\n10\n{cx:.4f}\n20\n{cy:.4f}\n30\n0.0\n40\n{r:.4f}"
        )

    def add_arc(
        self, layer: str, cx: float, cy: float, r: float, start_deg: float, end_deg: float
    ) -> None:
        self.entities.append(
            f"0\nARC\n8\n{layer}\n10\n{cx:.4f}\n20\n{cy:.4f}\n30\n0.0\n40\n{r:.4f}\n50\n{start_deg:.2f}\n51\n{end_deg:.2f}"
        )

    def add_text(
        self, layer: str, x: float, y: float, height: float, text: str, rotation: float = 0.0
    ) -> None:
        self.entities.append(
            f"0\nTEXT\n8\n{layer}\n10\n{x:.4f}\n20\n{y:.4f}\n30\n0.0\n40\n{height:.4f}\n1\n{text}\n50\n{rotation:.2f}"
        )

    def add_arch_dim_h(
        self, layer: str, x1: float, x2: float, y_dim: float, y_ext_origin: float, label: str
    ) -> None:
        tick = 0.16
        # Extension lines
        sign = 1.0 if y_dim >= y_ext_origin else -1.0
        self.add_line(layer, x1, y_ext_origin + 0.15 * sign, x1, y_dim + 0.18 * sign)
        self.add_line(layer, x2, y_ext_origin + 0.15 * sign, x2, y_dim + 0.18 * sign)
        # Dimension line
        self.add_line(layer, x1, y_dim, x2, y_dim)
        # 45-degree architectural slash ticks
        self.add_line(layer, x1 - tick, y_dim - tick, x1 + tick, y_dim + tick)
        self.add_line(layer, x2 - tick, y_dim - tick, x2 + tick, y_dim + tick)
        # Dimension text
        self.add_text(layer, (x1 + x2) * 0.5 - 0.35, y_dim + 0.12, 0.20, label)

    def add_arch_dim_v(
        self, layer: str, y1: float, y2: float, x_dim: float, x_ext_origin: float, label: str
    ) -> None:
        tick = 0.16
        sign = 1.0 if x_dim >= x_ext_origin else -1.0
        self.add_line(layer, x_ext_origin + 0.15 * sign, y1, x_dim + 0.18 * sign, y1)
        self.add_line(layer, x_ext_origin + 0.15 * sign, y2, x_dim + 0.18 * sign, y2)
        self.add_line(layer, x_dim, y1, x_dim, y2)
        self.add_line(layer, x_dim - tick, y1 - tick, x_dim + tick, y1 + tick)
        self.add_line(layer, x_dim - tick, y2 - tick, x_dim + tick, y2 + tick)
        self.add_text(layer, x_dim - 0.15, (y1 + y2) * 0.5 - 0.35, 0.20, label, rotation=90.0)

    def to_dxf_string(self) -> str:
        lines = [
            "0", "SECTION", "2", "HEADER",
            "9", "$INSUNITS", "70", "6",  # 6 = Meters
            "0", "ENDSEC",
            "0", "SECTION", "2", "TABLES",
            "0", "TABLE", "2", "LAYER", "70", str(len(AIA_LAYERS)),
        ]
        for name, color, ltype, lw in AIA_LAYERS:
            lines.extend([
                "0", "LAYER",
                "2", name,
                "70", "0",
                "62", str(color),
                "6", "CONTINUOUS",
                "370", str(lw),
            ])
        lines.extend(["0", "ENDTAB", "0", "ENDSEC"])
        lines.extend(["0", "SECTION", "2", "ENTITIES"])
        lines.extend(self.entities)
        lines.extend(["0", "ENDSEC", "0", "EOF"])
        return "\n".join(lines) + "\n"


def build_drawings(spec: dict, out_dir: Path) -> dict[str, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    dxf = DXFBuilder()
    scr_lines: list[str] = [
        "; AutoCAD 2D Architectural Plan Script generated by professional-architect-2d-cad",
        "-UNITS 2 2 1 2 0 N",
    ]
    for name, color, ltype, _ in AIA_LAYERS:
        scr_lines.append(f"-LAYER M {name} C {color} {name} ")

    project = spec["project"]
    W = float(project["footprintWidth"])
    D = float(project["footprintDepth"])
    overhang = float(project.get("roofOverhang", 0.75))

    # 1. Structural Grid & Grid Bubbles (A-GRID, A-GRID-IDEN)
    for vg in spec["grid"]["vertical"]:
        x = float(vg["x"])
        dxf.add_line("A-GRID", x, -1.6, x, D + 1.6)
        dxf.add_circle("A-GRID-IDEN", x, D + 2.0, 0.32)
        dxf.add_text("A-GRID-IDEN", x - 0.09, D + 1.90, 0.22, vg["id"])
    for hg in spec["grid"]["horizontal"]:
        y = float(hg["y"])
        dxf.add_line("A-GRID", -1.6, y, W + 1.6, y)
        dxf.add_circle("A-GRID-IDEN", -2.0, y, 0.32)
        dxf.add_text("A-GRID-IDEN", -2.09, y - 0.10, 0.22, hg["id"])

    # 2. Structural Columns (A-COLS)
    for col in spec.get("columns", []):
        cx, cy, sz = float(col["x"]), float(col["y"]), float(col["size"])
        dxf.add_rect("A-COLS", cx - sz * 0.5, cy - sz * 0.5, sz, sz)

    # 3. Full-Height Walls (A-WALL-FULL)
    for wall in spec.get("walls", []):
        x1, y1, x2, y2 = float(wall["x1"]), float(wall["y1"]), float(wall["x2"]), float(wall["y2"])
        t = float(wall["thickness"])
        if abs(y2 - y1) < 1e-4:
            dxf.add_rect("A-WALL-FULL", min(x1, x2), y1 - t * 0.5, abs(x2 - x1), t)
            scr_lines.append(f"-LAYER S A-WALL-FULL  RECTANG {min(x1,x2):.3f},{y1-t*0.5:.3f} {max(x1,x2):.3f},{y1+t*0.5:.3f}")
        else:
            dxf.add_rect("A-WALL-FULL", x1 - t * 0.5, min(y1, y2), t, abs(y2 - y1))
            scr_lines.append(f"-LAYER S A-WALL-FULL  RECTANG {x1-t*0.5:.3f},{min(y1,y2):.3f} {x1+t*0.5:.3f},{max(y1,y2):.3f}")

    # 4. Doors & 90-Degree Swing Arcs (A-DOOR, A-DOOR-SWNG)
    for door in spec.get("doors", []):
        dx, dy, dw = float(door["x"]), float(door["y"]), float(door["width"])
        orient = door.get("orientation", "north")
        if orient == "north":
            dxf.add_rect("A-DOOR", dx, dy, 0.05, dw)
            dxf.add_arc("A-DOOR-SWNG", dx, dy, dw, 0.0, 90.0)
        else:
            dxf.add_rect("A-DOOR", dx, dy - dw, 0.05, dw)
            dxf.add_arc("A-DOOR-SWNG", dx, dy, dw, 270.0, 360.0)

    # 5. Windows & Sills (A-GLAZ, A-GLAZ-SILL)
    for win in spec.get("windows", []):
        x1, y1, x2, y2 = float(win["x1"]), float(win["y1"]), float(win["x2"]), float(win["y2"])
        dxf.add_line("A-GLAZ-SILL", x1, y1, x2, y2)
        if abs(y2 - y1) < 1e-4:
            dxf.add_line("A-GLAZ", x1, y1 - 0.03, x2, y2 - 0.03)
            dxf.add_line("A-GLAZ", x1, y1 + 0.03, x2, y2 + 0.03)
        else:
            dxf.add_line("A-GLAZ", x1 - 0.03, y1, x2 - 0.03, y2)
            dxf.add_line("A-GLAZ", x1 + 0.03, y1, x2 + 0.03, y2)

    # 6. Overhead Roof Canopy Perimeter (A-OVER)
    dxf.add_rect("A-OVER", -overhang, -overhang, W + 2 * overhang, D + 2 * overhang)

    # 7. Room Identification Tags & Area Labels (A-ANNO-TEXT)
    for room in spec.get("rooms", []):
        rx, ry = float(room["x"]), float(room["y"])
        rw, rd = float(room["width"]), float(room["depth"])
        cx, cy = rx + rw * 0.5, ry + rd * 0.5
        area = rw * rd
        dxf.add_text("A-ANNO-TEXT", cx - 1.1, cy + 0.15, 0.22, f"{room['id']} {room['name']}")
        dxf.add_text(
            "A-ANNO-TEXT",
            cx - 1.1,
            cy - 0.20,
            0.16,
            f"{rw:.2f}m x {rd:.2f}m ({area:.1f} m2) | {room['zone']}",
        )

    # 8. Three-Tier Exterior Dimensioning with 45° Architectural Ticks (A-ANNO-DIMS)
    v_grids = spec["grid"]["vertical"]
    for i in range(len(v_grids) - 1):
        gx1, gx2 = float(v_grids[i]["x"]), float(v_grids[i + 1]["x"])
        dxf.add_arch_dim_h("A-ANNO-DIMS", gx1, gx2, D + 1.05, D, f"{gx2 - gx1:.2f}m")
    dxf.add_arch_dim_h("A-ANNO-DIMS", 0.0, W, D + 1.65, D, f"{W:.2f}m OVERALL")

    h_grids = spec["grid"]["horizontal"]
    for i in range(len(h_grids) - 1):
        gy1, gy2 = float(h_grids[i]["y"]), float(h_grids[i + 1]["y"])
        dxf.add_arch_dim_v("A-ANNO-DIMS", gy1, gy2, -1.05, 0.0, f"{gy2 - gy1:.2f}m")
    dxf.add_arch_dim_v("A-ANNO-DIMS", 0.0, D, -1.65, 0.0, f"{D:.2f}m OVERALL")

    # 9. Section Cut Callouts & Title Block (A-ANNO-SYMB, A-TTLB)
    for sec in spec.get("sections", []):
        sx1, sy1, sx2, sy2 = float(sec["x1"]), float(sec["y1"]), float(sec["x2"]), float(sec["y2"])
        dxf.add_line("A-ANNO-SYMB", sx1, sy1, sx2, sy2)
        dxf.add_circle("A-ANNO-SYMB", sx2, sy2, 0.28)
        dxf.add_text("A-ANNO-SYMB", sx2 - 0.18, sy2 - 0.08, 0.18, sec["id"])

    dxf.add_rect("A-TTLB", -3.2, -2.6, W + 6.4, D + 5.8)
    dxf.add_text(
        "A-TTLB",
        0.0,
        -2.2,
        0.26,
        f"{project['sheetNumber']} | {project['title']} | SCALE {project['scale']} | NORTH UP",
    )

    dxf_path = out_dir / "floor_plan_a101.dxf"
    scr_path = out_dir / "floor_plan_a101.scr"
    svg_path = out_dir / "floor_plan_a101.svg"
    dxf_path.write_text(dxf.to_dxf_string(), encoding="utf-8")
    scr_path.write_text("\n".join(scr_lines) + "\nZOOM E\n", encoding="utf-8")
    svg_path.write_text(build_svg_sheet(spec), encoding="utf-8")

    return {"dxf": dxf_path, "scr": scr_path, "svg": svg_path}


def build_svg_sheet(spec: dict) -> str:
    """Render a high-contrast architectural 2D floor plan SVG sheet with AIA lineweights."""
    project = spec["project"]
    W = float(project["footprintWidth"])
    D = float(project["footprintDepth"])
    overhang = float(project.get("roofOverhang", 0.75))
    scale = 48.0  # px per meter
    pad_x, pad_y = 180.0, 160.0
    svg_w = int(W * scale + pad_x * 2)
    svg_h = int(D * scale + pad_y * 2)

    def sx(x: float) -> float:
        return pad_x + x * scale

    def sy(y: float) -> float:
        return svg_h - pad_y - y * scale

    el: list[str] = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_w} {svg_h}" width="{svg_w}" height="{svg_h}" style="background:#F8FAFC;font-family:\'Inter\',\'Helvetica Neue\',monospace;">',
        f'<rect x="18" y="18" width="{svg_w - 36}" height="{svg_h - 36}" fill="none" stroke="#0F172A" stroke-width="2.2"/>',
        f'<rect x="24" y="24" width="{svg_w - 48}" height="{svg_h - 48}" fill="none" stroke="#334155" stroke-width="0.7"/>',
    ]

    # Grid lines & bubbles (A-GRID: 0.09mm)
    for vg in spec["grid"]["vertical"]:
        gx = sx(float(vg["x"]))
        el.append(f'<line x1="{gx:.1f}" y1="{sy(-1.5):.1f}" x2="{gx:.1f}" y2="{sy(D + 1.5):.1f}" stroke="#94A3B8" stroke-width="0.75" stroke-dasharray="10,4,2,4"/>')
        el.append(f'<circle cx="{gx:.1f}" cy="{sy(D + 1.95):.1f}" r="13" fill="#FFFFFF" stroke="#0F172A" stroke-width="1.2"/>')
        el.append(f'<text x="{gx:.1f}" y="{sy(D + 1.95) + 4:.1f}" text-anchor="middle" font-size="11" font-weight="700" fill="#0F172A">{vg["id"]}</text>')

    for hg in spec["grid"]["horizontal"]:
        gy = sy(float(hg["y"]))
        el.append(f'<line x1="{sx(-1.5):.1f}" y1="{gy:.1f}" x2="{sx(W + 1.5):.1f}" y2="{gy:.1f}" stroke="#94A3B8" stroke-width="0.75" stroke-dasharray="10,4,2,4"/>')
        el.append(f'<circle cx="{sx(-1.95):.1f}" cy="{gy:.1f}" r="13" fill="#FFFFFF" stroke="#0F172A" stroke-width="1.2"/>')
        el.append(f'<text x="{sx(-1.95):.1f}" y="{gy + 4:.1f}" text-anchor="middle" font-size="11" font-weight="700" fill="#0F172A">{hg["id"]}</text>')

    # Overhead roof canopy (A-OVER: dashed)
    el.append(
        f'<rect x="{sx(-overhang):.1f}" y="{sy(D + overhang):.1f}" width="{(W + 2 * overhang) * scale:.1f}" height="{(D + 2 * overhang) * scale:.1f}" fill="none" stroke="#64748B" stroke-width="1.0" stroke-dasharray="6,5"/>'
    )

    # Room zones & labels
    for room in spec.get("rooms", []):
        rx, ry = float(room["x"]), float(room["y"])
        rw, rd = float(room["width"]), float(room["depth"])
        cx, cy = sx(rx + rw * 0.5), sy(ry + rd * 0.5)
        area = rw * rd
        el.append(f'<text x="{cx:.1f}" y="{cy - 6:.1f}" text-anchor="middle" font-size="11" font-weight="700" fill="#0F172A">{room["id"]} {room["name"]}</text>')
        el.append(f'<text x="{cx:.1f}" y="{cy + 10:.1f}" text-anchor="middle" font-size="9.5" fill="#475569">{rw:.2f}m × {rd:.2f}m · {area:.1f} m²</text>')

    # Cut walls with poché (A-WALL-FULL: 0.50mm)
    for wall in spec.get("walls", []):
        x1, y1, x2, y2 = float(wall["x1"]), float(wall["y1"]), float(wall["x2"]), float(wall["y2"])
        t = float(wall["thickness"])
        if abs(y2 - y1) < 1e-4:
            wx = sx(min(x1, x2))
            wy = sy(y1 + t * 0.5)
            ww = abs(x2 - x1) * scale
            wh = t * scale
        else:
            wx = sx(x1 - t * 0.5)
            wy = sy(max(y1, y2))
            ww = t * scale
            wh = abs(y2 - y1) * scale
        el.append(f'<rect x="{wx:.1f}" y="{wy:.1f}" width="{ww:.1f}" height="{wh:.1f}" fill="#334155" stroke="#0F172A" stroke-width="2.1"/>')

    # Structural columns (A-COLS: solid black poché)
    for col in spec.get("columns", []):
        cx, cy, sz = float(col["x"]), float(col["y"]), float(col["size"])
        el.append(
            f'<rect x="{sx(cx - sz * 0.5):.1f}" y="{sy(cy + sz * 0.5):.1f}" width="{sz * scale:.1f}" height="{sz * scale:.1f}" fill="#0F172A"/>'
        )

    # Doors with 90-degree swing arcs (A-DOOR, A-DOOR-SWNG)
    for door in spec.get("doors", []):
        dx, dy, dw = float(door["x"]), float(door["y"]), float(door["width"])
        hx, hy = sx(dx), sy(dy)
        r = dw * scale
        if door.get("orientation", "north") == "north":
            el.append(f'<line x1="{hx:.1f}" y1="{hy:.1f}" x2="{hx:.1f}" y2="{hy - r:.1f}" stroke="#0F172A" stroke-width="1.8"/>')
            el.append(f'<path d="M {hx + r:.1f} {hy:.1f} A {r:.1f} {r:.1f} 0 0 0 {hx:.1f} {hy - r:.1f}" fill="none" stroke="#64748B" stroke-width="1.0" stroke-dasharray="3,2"/>')
        else:
            el.append(f'<line x1="{hx:.1f}" y1="{hy:.1f}" x2="{hx:.1f}" y2="{hy + r:.1f}" stroke="#0F172A" stroke-width="1.8"/>')
            el.append(f'<path d="M {hx + r:.1f} {hy:.1f} A {r:.1f} {r:.1f} 0 0 1 {hx:.1f} {hy + r:.1f}" fill="none" stroke="#64748B" stroke-width="1.0" stroke-dasharray="3,2"/>')

    # Title block footer
    el.append(
        f'<text x="42" y="{svg_h - 36}" font-size="12" font-weight="700" fill="#0F172A">{project["sheetNumber"]} · {project["title"]} · SCALE {project["scale"]} · ↑ N</text>'
    )
    el.append("</svg>")
    return "\n".join(el)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate AIA-layered AutoCAD DXF and SCR from building spec.")
    parser.add_argument("spec", type=Path, help="Path to building spec JSON.")
    parser.add_argument("--out-dir", type=Path, default=Path("cad_output"), help="Output folder.")
    args = parser.parse_args()

    spec = json.loads(args.spec.read_text(encoding="utf-8"))
    outputs = build_drawings(spec, args.out_dir)
    for kind, path in outputs.items():
        print(f"Generated {kind.upper()}: {path.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
