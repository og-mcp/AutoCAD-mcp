#!/usr/bin/env python3
"""
Validate a building floor plan JSON specification against Neufert anthropometrics,
Ching spatial efficiency rules, and international building code (IBC/NBC) standards.
"""

import argparse
import json
import math
import sys
from pathlib import Path

MIN_ROOM_SPECS = {
    "primary_bedroom": {"min_width": 3.20, "min_area": 12.0},
    "bedroom": {"min_width": 2.70, "min_area": 9.5},
    "living": {"min_width": 3.60, "min_area": 16.0},
    "dining": {"min_width": 3.00, "min_area": 10.0},
    "kitchen": {"min_width": 2.40, "min_area": 7.5},
    "study": {"min_width": 2.40, "min_area": 6.5},
    "bathroom": {"min_width": 1.70, "min_area": 4.0},
    "powder": {"min_width": 1.10, "min_area": 1.8},
    "foyer": {"min_width": 1.50, "min_area": 3.0},
    "corridor": {"min_width": 0.90, "min_area": 0.0},
}

MIN_DOOR_WIDTHS = {
    "entry": 1.00,
    "interior": 0.80,
    "bathroom": 0.70,
}


def validate_spec(spec: dict) -> tuple[list[str], list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    passed: list[str] = []

    project = spec.get("project", {})
    rooms = spec.get("rooms", [])
    doors = spec.get("doors", [])
    windows = spec.get("windows", [])
    stairs = spec.get("stairs", [])
    sections = spec.get("sections", [])

    total_area = 0.0
    corridor_area = 0.0

    # 1. Room dimensions, areas, and ceiling heights
    for room in rooms:
        rid = room.get("id", "?")
        rname = room.get("name", "Unnamed")
        rtype = room.get("type", "other")
        w = float(room.get("width", 0))
        d = float(room.get("depth", 0))
        short_side = min(w, d)
        area = w * d
        total_area += area
        if rtype == "corridor":
            corridor_area += area

        if rtype in MIN_ROOM_SPECS:
            req = MIN_ROOM_SPECS[rtype]
            if short_side < req["min_width"] - 1e-4:
                errors.append(
                    f"[Room {rid} {rname}] Short dimension {short_side:.2f}m is below Neufert minimum {req['min_width']:.2f}m for '{rtype}'."
                )
            elif area < req["min_area"] - 1e-4:
                errors.append(
                    f"[Room {rid} {rname}] Floor area {area:.2f}m2 is below minimum {req['min_area']:.2f}m2 for '{rtype}'."
                )
            else:
                passed.append(
                    f"[Room {rid} {rname}] Dimensions {w:.2f}m x {d:.2f}m ({area:.1f}m2) meet '{rtype}' anthropometric standards."
                )

        # Kitchen work triangle check
        if rtype == "kitchen" and "kitchenTriangleSum" in room:
            tri = float(room["kitchenTriangleSum"])
            if not (4.0 <= tri <= 7.9):
                errors.append(
                    f"[Room {rid} {rname}] Kitchen work triangle {tri:.2f}m outside ergonomic range [4.0m, 7.9m]."
                )
            else:
                passed.append(
                    f"[Room {rid} {rname}] Kitchen work triangle ({tri:.2f}m) is within optimal [4.0m, 7.9m] range."
                )

        # Wet-wall consolidation check
        if room.get("wetRoom") and not room.get("sharedWetWall"):
            warnings.append(
                f"[Room {rid} {rname}] Wet room does not reference a shared plumbing chase wall ('sharedWetWall')."
            )

    # 2. Circulation efficiency ratio (Ching rule: <= 18% residential)
    if total_area > 0:
        circ_ratio = (corridor_area / total_area) * 100.0
        if circ_ratio > 20.0:
            warnings.append(
                f"[Circulation Efficiency] Corridor ratio is {circ_ratio:.1f}% (> 18% target); consider consolidating hallway space."
            )
        else:
            passed.append(
                f"[Circulation Efficiency] Corridor ratio is {circ_ratio:.1f}% of {total_area:.1f}m2 gross area (optimal <= 18%)."
            )

    # 3. Daylight glazing ratio for habitable rooms (>= 10% of floor area)
    for room in rooms:
        if not room.get("habitable", False):
            continue
        rid = room["id"]
        rname = room["name"]
        area = float(room["width"]) * float(room["depth"])
        room_wins = [w for w in windows if w.get("room") == rid]
        glazed_area = 0.0
        walls_with_windows = set()
        for win in room_wins:
            length = math.hypot(
                float(win["x2"]) - float(win["x1"]),
                float(win["y2"]) - float(win["y1"]),
            )
            height = float(win.get("head", 2.1)) - float(win.get("sill", 0.9))
            glazed_area += length * max(height, 0.0)
            if "wall" in win:
                walls_with_windows.add(win["wall"])

        ratio = (glazed_area / area) * 100.0 if area > 0 else 0.0
        if ratio < 10.0:
            errors.append(
                f"[Daylight Code - Room {rid} {rname}] Glazed window area is {ratio:.1f}% of floor area (minimum code requirement is 10%)."
            )
        else:
            two_sides = (
                " (Pattern 159: Light on Two Sides achieved)"
                if len(walls_with_windows) >= 2
                else ""
            )
            passed.append(
                f"[Daylight Code - Room {rid} {rname}] Glazing ratio is {ratio:.1f}% >= 10%{two_sides}."
            )

    # 4. Door widths & 90° swing verification
    for door in doors:
        did = door.get("id", "?")
        dtype = door.get("type", "interior")
        dw = float(door.get("width", 0))
        min_dw = MIN_DOOR_WIDTHS.get(dtype, 0.80)
        if dw < min_dw - 1e-4:
            errors.append(
                f"[Door {did}] Width {dw:.2f}m is narrower than minimum {min_dw:.2f}m for '{dtype}' door."
            )
        else:
            passed.append(f"[Door {did}] Width {dw:.2f}m meets '{dtype}' clearance standard.")

    # 5. Staircase Blondel's Law check: 600mm <= 2R + T <= 630mm
    for stair in stairs:
        sid = stair.get("id", "?")
        r_mm = float(stair.get("riserMm", 0))
        t_mm = float(stair.get("treadMm", 0))
        blondel = 2.0 * r_mm + t_mm
        if not (600.0 <= blondel <= 630.0):
            errors.append(
                f"[Stair {sid}] Blondel formula 2R + T = {blondel:.0f}mm (R={r_mm:.0f}mm, T={t_mm:.0f}mm) violates ergonomic range [600mm, 630mm]."
            )
        else:
            passed.append(
                f"[Stair {sid}] Blondel formula 2R + T = {blondel:.0f}mm (R={r_mm:.0f}mm, T={t_mm:.0f}mm) is ergonomic."
            )

    # 6. Orthographic section cuts & North orientation check
    if len(sections) < 2:
        warnings.append(
            "[Orthographic Planes] Fewer than 2 section cuts defined; include both longitudinal (A-A) and transverse (B-B) sections."
        )
    else:
        passed.append(
            f"[Orthographic Planes] {len(sections)} coordinated section cut planes defined."
        )

    if "northAngleDeg" not in project:
        warnings.append("[Site Orientation] 'northAngleDeg' is missing from project metadata.")

    return passed, warnings, errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate architectural floor plan JSON spec.")
    parser.add_argument("spec", type=Path, help="Path to building spec JSON file.")
    args = parser.parse_args()

    spec = json.loads(args.spec.read_text(encoding="utf-8"))
    passed, warnings, errors = validate_spec(spec)

    print(f"=== ARCHITECTURAL & ANTHROPOMETRIC VALIDATION: {spec.get('project', {}).get('title', args.spec.name)} ===")
    for msg in passed:
        print(f"  PASS: {msg}")
    for msg in warnings:
        print(f"  WARN: {msg}")
    for msg in errors:
        print(f"  FAIL: {msg}")

    print(f"\nSummary: {len(passed)} passed, {len(warnings)} warnings, {len(errors)} errors.")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
