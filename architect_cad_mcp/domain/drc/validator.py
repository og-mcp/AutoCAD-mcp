"""Architectural Design Rule Check (DRC), Neufert Anthropometrics & Code Validator.

References:
- Ernst Neufert, Architects' Data, 4th/5th Ed.
- International Building Code (IBC) 2024 / National Building Code (NBC).
- François Blondel, Cours d'Architecture (Stair Law).
- Christopher Alexander, A Pattern Language (Pattern 159).
"""

from __future__ import annotations

import math
from typing import Any

from architect_cad_mcp.core.constants import (
    BLONDEL_MAX_MM,
    BLONDEL_MIN_MM,
    MAX_CIRCULATION_RATIO_PCT,
    MIN_DOOR_WIDTHS,
    MIN_GLAZING_RATIO_PCT,
    MIN_ROOM_SPECS,
)


def audit_architecture_spec(spec: dict[str, Any]) -> dict[str, Any]:
    """Run comprehensive Neufert anthropometric, Ching circulation, and IBC/NBC code checks."""
    passed: list[str] = []
    warnings: list[str] = []
    errors: list[str] = []

    project = spec.get("project", {})
    rooms = spec.get("rooms", [])
    doors = spec.get("doors", [])
    windows = spec.get("windows", [])
    stairs = spec.get("stairs", [])
    sections = spec.get("sections", [])

    total_area = 0.0
    corridor_area = 0.0
    habitable_area = 0.0
    wet_area = 0.0

    for room in rooms:
        rid = str(room.get("id", "?"))
        rname = str(room.get("name", "Unnamed"))
        rtype = str(room.get("type", "other"))
        w = float(room.get("width", 0))
        d = float(room.get("depth", 0))
        short_side = min(w, d)
        area = w * d
        total_area += area
        if rtype == "corridor":
            corridor_area += area
        if room.get("habitable"):
            habitable_area += area
        if room.get("wetRoom"):
            wet_area += area

        if rtype in MIN_ROOM_SPECS:
            req = MIN_ROOM_SPECS[rtype]
            if short_side < req["min_width"] - 1e-4:
                errors.append(
                    f"[Room {rid} {rname}] Short side {short_side:.2f}m < Neufert min {req['min_width']:.2f}m for '{rtype}'."
                )
            elif area < req["min_area"] - 1e-4:
                errors.append(
                    f"[Room {rid} {rname}] Area {area:.2f}m2 < Neufert min {req['min_area']:.2f}m2 for '{rtype}'."
                )
            else:
                passed.append(
                    f"[Room {rid} {rname}] {w:.2f}m x {d:.2f}m ({area:.1f}m2) satisfies '{rtype}' standard."
                )

        if rtype == "kitchen" and "kitchenTriangleSum" in room:
            tri = float(room["kitchenTriangleSum"])
            if not (4.0 <= tri <= 7.9):
                errors.append(
                    f"[Room {rid} {rname}] Kitchen work triangle {tri:.2f}m outside [4.0m, 7.9m]."
                )
            else:
                passed.append(
                    f"[Room {rid} {rname}] Kitchen work triangle ({tri:.2f}m) within [4.0m, 7.9m]."
                )

        if room.get("wetRoom") and not room.get("sharedWetWall"):
            warnings.append(
                f"[Room {rid} {rname}] Wet room lacks 'sharedWetWall' consolidation reference."
            )

    circ_ratio = (corridor_area / total_area * 100.0) if total_area > 0 else 0.0
    if circ_ratio > (MAX_CIRCULATION_RATIO_PCT + 2.0):
        warnings.append(
            f"[Circulation Efficiency] Corridor ratio {circ_ratio:.1f}% exceeds target (<= {MAX_CIRCULATION_RATIO_PCT}%)."
        )
    else:
        passed.append(
            f"[Circulation Efficiency] Corridor ratio {circ_ratio:.1f}% of {total_area:.1f}m2 gross area (optimal <= {MAX_CIRCULATION_RATIO_PCT}%)."
        )

    for room in rooms:
        if not room.get("habitable", False):
            continue
        rid = str(room["id"])
        rname = str(room["name"])
        area = float(room["width"]) * float(room["depth"])
        room_wins = [w for w in windows if str(w.get("room")) == rid]
        glazed_area = 0.0
        walls_with_win = set()
        for win in room_wins:
            length = math.hypot(
                float(win["x2"]) - float(win["x1"]),
                float(win["y2"]) - float(win["y1"]),
            )
            height = float(win.get("head", 2.4)) - float(win.get("sill", 0.6))
            glazed_area += length * max(height, 0.0)
            if "wall" in win:
                walls_with_win.add(str(win["wall"]))

        ratio = (glazed_area / area * 100.0) if area > 0 else 0.0
        if ratio < MIN_GLAZING_RATIO_PCT:
            errors.append(
                f"[Daylight Code - Room {rid} {rname}] Glazing ratio {ratio:.1f}% < {MIN_GLAZING_RATIO_PCT:.1f}% minimum."
            )
        else:
            two_sides = " (Pattern 159: Light on Two Sides)" if len(walls_with_win) >= 2 else ""
            passed.append(
                f"[Daylight Code - Room {rid} {rname}] Glazing ratio {ratio:.1f}% >= {MIN_GLAZING_RATIO_PCT:.1f}%{two_sides}."
            )

    for door in doors:
        did = str(door.get("id", "?"))
        dtype = str(door.get("type", "interior"))
        dw = float(door.get("width", 0))
        min_dw = MIN_DOOR_WIDTHS.get(dtype, 0.80)
        if dw < min_dw - 1e-4:
            errors.append(
                f"[Door {did}] Width {dw:.2f}m < minimum {min_dw:.2f}m for '{dtype}'."
            )
        else:
            passed.append(f"[Door {did}] Width {dw:.2f}m meets '{dtype}' clearance.")

    for stair in stairs:
        sid = str(stair.get("id", "?"))
        r_mm = float(stair.get("riserMm", 0))
        t_mm = float(stair.get("treadMm", 0))
        blondel = 2.0 * r_mm + t_mm
        if not (BLONDEL_MIN_MM <= blondel <= BLONDEL_MAX_MM):
            errors.append(
                f"[Stair {sid}] Blondel 2R+T = {blondel:.0f}mm (R={r_mm:.0f}, T={t_mm:.0f}) outside [{BLONDEL_MIN_MM:.0f}, {BLONDEL_MAX_MM:.0f}]mm."
            )
        else:
            passed.append(
                f"[Stair {sid}] Blondel 2R+T = {blondel:.0f}mm (R={r_mm:.0f}mm, T={t_mm:.0f}mm) is ergonomic."
            )

    if len(sections) < 2:
        warnings.append("[Orthographic Planes] Fewer than 2 section cuts defined.")
    else:
        passed.append(f"[Orthographic Planes] {len(sections)} section cuts coordinated.")

    return {
        "drc_status": "PASS" if not errors else "FAIL",
        "project_title": project.get("title", "Untitled"),
        "metrics": {
            "gross_area_m2": round(total_area, 2),
            "habitable_area_m2": round(habitable_area, 2),
            "wet_core_area_m2": round(wet_area, 2),
            "corridor_area_m2": round(corridor_area, 2),
            "circulation_ratio_pct": round(circ_ratio, 2),
            "room_count": len(rooms),
            "door_count": len(doors),
            "window_count": len(windows),
        },
        "counts": {
            "passed": len(passed),
            "warnings": len(warnings),
            "errors": len(errors),
        },
        "passed": passed,
        "warnings": warnings,
        "errors": errors,
    }
