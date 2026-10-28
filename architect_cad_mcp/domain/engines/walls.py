"""Wall geometry, opening interval subtraction, and solid poché generation."""

from __future__ import annotations

from typing import Any


def wall_segments_with_openings(
    wall: dict[str, Any], spec: dict[str, Any], tol: float = 1e-3
) -> list[tuple[float, float, float, float]]:
    """Split a wall into cut-wall rectangles, removing door and window openings on its axis.

    Returns a list of (x, y, width, height) bounding boxes for solid poché segments.
    """
    x1, y1, x2, y2 = float(wall["x1"]), float(wall["y1"]), float(wall["x2"]), float(wall["y2"])
    t = float(wall["thickness"])
    horizontal = abs(y2 - y1) < tol
    lo, hi = (min(x1, x2), max(x1, x2)) if horizontal else (min(y1, y2), max(y1, y2))
    axis = y1 if horizontal else x1

    openings: list[tuple[float, float]] = []
    for door in spec.get("doors", []):
        dx, dy, dw = float(door["x"]), float(door["y"]), float(door["width"])
        d_axis = dy if horizontal else dx
        d_pos = dx if horizontal else dy
        if abs(d_axis - axis) < 0.25 and (lo - 0.1) <= d_pos <= (hi + 0.1):
            openings.append((d_pos, min(hi, d_pos + dw)))

    for win in spec.get("windows", []):
        wx1, wy1, wx2, wy2 = float(win["x1"]), float(win["y1"]), float(win["x2"]), float(win["y2"])
        w_axis = wy1 if horizontal else wx1
        w_lo = min(wx1, wx2) if horizontal else min(wy1, wy2)
        w_hi = max(wx1, wx2) if horizontal else max(wy1, wy2)
        if abs(w_axis - axis) < 0.25 and not (w_hi < lo or w_lo > hi):
            openings.append((max(lo, w_lo), min(hi, w_hi)))

    if not openings:
        return [(min(x1, x2), min(y1, y2), abs(x2 - x1) if horizontal else t, t if horizontal else abs(y2 - y1))]

    # Sort and merge overlapping or adjacent opening intervals
    openings.sort(key=lambda o: o[0])
    merged: list[tuple[float, float]] = []
    for o_lo, o_hi in openings:
        if not merged:
            merged.append((max(lo, o_lo), min(hi, o_hi)))
        else:
            prev_lo, prev_hi = merged[-1]
            if o_lo <= prev_hi + tol:
                merged[-1] = (prev_lo, max(prev_hi, min(hi, o_hi)))
            else:
                merged.append((max(lo, o_lo), min(hi, o_hi)))

    # Compute remaining solid wall segments
    segments: list[tuple[float, float, float, float]] = []
    cur = lo
    for o_lo, o_hi in merged:
        if o_lo > cur + tol:
            seg_len = o_lo - cur
            if horizontal:
                segments.append((cur, axis - t / 2.0, seg_len, t))
            else:
                segments.append((axis - t / 2.0, cur, t, seg_len))
        cur = max(cur, o_hi)

    if hi > cur + tol:
        seg_len = hi - cur
        if horizontal:
            segments.append((cur, axis - t / 2.0, seg_len, t))
        else:
            segments.append((axis - t / 2.0, cur, t, seg_len))

    return segments
