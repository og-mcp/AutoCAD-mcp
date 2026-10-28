"""Structured ezdxf drawing audit, entity normalization, geometry digest, and topology DRC."""

from __future__ import annotations

from collections import Counter
import hashlib
import json
import math
from pathlib import Path
from typing import Any

import ezdxf

INSUNITS_NAMES: dict[int, str] = {
    0: "unitless",
    1: "inches",
    2: "feet",
    4: "millimeters",
    5: "centimeters",
    6: "meters",
    7: "kilometers",
}


def _round_num(value: Any) -> float | int | None:
    try:
        num = float(value)
    except (TypeError, ValueError):
        return None
    r = round(num, 6)
    return int(r) if r.is_integer() else r


def _point2d(pt: Any) -> list[float | int] | None:
    try:
        coords = list(pt)
    except (TypeError, ValueError):
        return None
    if len(coords) < 2:
        return None
    x, y = _round_num(coords[0]), _round_num(coords[1])
    if x is None or y is None:
        return None
    return [x, y]


def normalize_ezdxf_entity(entity: Any) -> dict[str, Any]:
    """Normalize an ezdxf entity into deterministic, handle-independent JSON."""
    etype = entity.dxftype()
    data: dict[str, Any] = {
        "type": etype,
        "handle": str(entity.dxf.get("handle", "")),
        "layer": str(entity.dxf.get("layer", "0")),
    }
    if etype == "LINE":
        data["start"] = _point2d(entity.dxf.start)
        data["end"] = _point2d(entity.dxf.end)
    elif etype in ("CIRCLE", "ARC"):
        data["center"] = _point2d(entity.dxf.center)
        data["radius"] = _round_num(entity.dxf.radius)
        if etype == "ARC":
            data["start_angle"] = _round_num(entity.dxf.start_angle)
            data["end_angle"] = _round_num(entity.dxf.end_angle)
    elif etype == "LWPOLYLINE":
        pts = list(entity.get_points(format="xyb"))
        data["points"] = [[_round_num(x), _round_num(y)] for x, y, _ in pts]
        data["closed"] = bool(entity.closed) or (len(pts) >= 3 and pts[0][:2] == pts[-1][:2])
    elif etype in ("TEXT", "MTEXT"):
        data["insert"] = _point2d(entity.dxf.get("insert"))
        data["text"] = str(entity.dxf.get("text", ""))
        h_attr = "char_height" if etype == "MTEXT" else "height"
        data["height"] = _round_num(entity.dxf.get(h_attr, 0.2))
        data["rotation"] = _round_num(entity.dxf.get("rotation", 0.0))
    elif etype == "HATCH":
        data["pattern"] = str(entity.dxf.get("pattern_name", ""))
        data["solid"] = bool(entity.dxf.get("solid_fill", 0))
        data["path_count"] = len(entity.paths)
        verts: list[list[float | int]] = []
        for path in entity.paths:
            for v in getattr(path, "vertices", []):
                p = _point2d(v)
                if p:
                    verts.append(p)
        if verts:
            data["points"] = verts
    return {k: v for k, v in data.items() if v is not None}


def compute_modelspace_bounds(
    entities: list[dict[str, Any]],
) -> dict[str, list[float] | None]:
    """Compute 2D bounding box from normalized entities."""
    xs: list[float] = []
    ys: list[float] = []

    def _feed(pt: Any) -> None:
        if isinstance(pt, (list, tuple)) and len(pt) >= 2:
            try:
                xs.append(float(pt[0]))
                ys.append(float(pt[1]))
            except (TypeError, ValueError):
                pass

    for ent in entities:
        _feed(ent.get("start"))
        _feed(ent.get("end"))
        _feed(ent.get("insert"))
        center = ent.get("center")
        radius = ent.get("radius")
        if center and radius is not None:
            _feed([center[0] - radius, center[1] - radius])
            _feed([center[0] + radius, center[1] + radius])
        for pt in ent.get("points", []):
            _feed(pt)

    if not xs or not ys:
        return {"min": None, "max": None, "size": None}

    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    return {
        "min": [round(min_x, 4), round(min_y, 4)],
        "max": [round(max_x, 4), round(max_y, 4)],
        "size": [round(max_x - min_x, 4), round(max_y - min_y, 4)],
    }


def compute_geometry_digest(entities: list[dict[str, Any]]) -> str:
    """Compute a deterministic SHA-256 geometry digest independent of entity handles."""
    signatures = []
    for ent in entities:
        sig = {k: v for k, v in ent.items() if k != "handle"}
        signatures.append(sig)
    encoded = json.dumps(
        sorted(signatures, key=lambda item: json.dumps(item, sort_keys=True)),
        sort_keys=True,
        separators=(",", ":"),
    )
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def audit_geometry_drc(entities: list[dict[str, Any]]) -> dict[str, Any]:
    """Check geometric validity (zero-length lines, degenerate polylines)."""
    zero_lines = []
    deg_polys = []
    for ent in entities:
        etype = ent.get("type")
        if etype == "LINE":
            s, e = ent.get("start"), ent.get("end")
            if s and e and math.hypot(e[0] - s[0], e[1] - s[1]) < 1e-6:
                zero_lines.append(ent.get("handle", ""))
        elif etype == "LWPOLYLINE":
            pts = ent.get("points", [])
            if len(pts) < 2:
                deg_polys.append(ent.get("handle", ""))
    return {
        "status": "PASS" if not zero_lines and not deg_polys and len(entities) > 0 else "FAIL",
        "zero_length_line_count": len(zero_lines),
        "degenerate_polyline_count": len(deg_polys),
        "zero_length_handles": zero_lines,
        "degenerate_polyline_handles": deg_polys,
    }


def audit_ezdxf_document(
    doc: ezdxf.document.Drawing,
    limit: int = 50,
    include_entities: bool = False,
) -> dict[str, Any]:
    """Run structured geometry and layer audit on an in-memory ezdxf Drawing."""
    msp = doc.modelspace()
    entities = [normalize_ezdxf_entity(e) for e in msp]

    counts_by_type = dict(sorted(Counter(e["type"] for e in entities).items()))
    counts_by_layer = dict(sorted(Counter(e["layer"] for e in entities).items()))

    xs: list[float] = []
    ys: list[float] = []
    zero_length_lines: list[str] = []
    degenerate_polylines: list[str] = []

    for ent in entities:
        etype = ent["type"]
        if etype == "LINE":
            s, e = ent.get("start"), ent.get("end")
            if s and e:
                xs.extend([float(s[0]), float(e[0])])
                ys.extend([float(s[1]), float(e[1])])
                if math.hypot(float(e[0]) - float(s[0]), float(e[1]) - float(s[1])) < 1e-6:
                    zero_length_lines.append(ent["handle"])
        elif etype in ("CIRCLE", "ARC"):
            c = ent.get("center")
            r = float(ent.get("radius", 0.0))
            if c:
                xs.extend([float(c[0]) - r, float(c[0]) + r])
                ys.extend([float(c[1]) - r, float(c[1]) + r])
        elif etype == "LWPOLYLINE":
            pts = ent.get("points", [])
            if len(pts) < 2:
                degenerate_polylines.append(ent["handle"])
            for pt in pts:
                xs.append(float(pt[0]))
                ys.append(float(pt[1]))
        elif etype in ("TEXT", "MTEXT"):
            ins = ent.get("insert")
            if ins:
                xs.append(float(ins[0]))
                ys.append(float(ins[1]))

    bounds = (
        {
            "min": [round(min(xs), 4), round(min(ys), 4)],
            "max": [round(max(xs), 4), round(max(ys), 4)],
            "size": [round(max(xs) - min(xs), 4), round(max(ys) - min(ys), 4)],
        }
        if xs and ys
        else None
    )

    units_code = int(doc.header.get("$INSUNITS", 0) or 0)
    drc_issues = len(zero_length_lines) + len(degenerate_polylines)
    drc_status = "PASS" if drc_issues == 0 and len(entities) > 0 else "FAIL"

    result: dict[str, Any] = {
        "backend": "ezdxf",
        "dxf_version": doc.dxfversion,
        "entity_count": len(entities),
        "total_entities": len(entities),
        "layer_count": len(doc.layers),
        "counts_by_type": counts_by_type,
        "entities_by_type": counts_by_type,
        "counts_by_layer": counts_by_layer,
        "entities_by_layer": counts_by_layer,
        "bounds": bounds,
        "units": {
            "code": units_code,
            "name": INSUNITS_NAMES.get(units_code, "unknown"),
        },
        "geometry_digest": compute_geometry_digest(entities),
        "geometry_drc": {
            "status": drc_status,
            "zero_length_line_count": len(zero_length_lines),
            "degenerate_polyline_count": len(degenerate_polylines),
            "zero_length_handles": zero_length_lines,
            "degenerate_polyline_handles": degenerate_polylines,
        },
    }
    if include_entities:
        result["entities"] = entities[: max(1, min(limit, 500))]
    return result


def audit_dxf_file(
    path: str | Path,
    limit: int = 50,
    include_entities: bool = False,
) -> dict[str, Any]:
    """Read a DXF file from disk headlessly and return its structured audit report."""
    dxf_path = Path(path).expanduser().resolve()
    doc = ezdxf.readfile(str(dxf_path))
    report = audit_ezdxf_document(doc, limit=limit, include_entities=include_entities)
    raw_bytes = dxf_path.read_bytes()
    report["path"] = str(dxf_path)
    report["file_path"] = str(dxf_path)
    report["file_bytes"] = len(raw_bytes)
    report["file_sha256"] = hashlib.sha256(raw_bytes).hexdigest()
    return report
