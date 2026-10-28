"""Architectural Template Registry and Discovery Service.

Follows Open/Closed Principle: new templates can be registered dynamically
or loaded from domain packages.
"""

from __future__ import annotations

import copy
from typing import Any

from architect_cad_mcp.templates.buildings import MULTI_UNIT_APARTMENT_FLOOR_SPEC
from architect_cad_mcp.templates.houses import (
    COMPACT_TOWNHOUSE_SPEC,
    COURTYARD_RESIDENCE_SPEC,
    MODERN_FAMILY_VILLA_SPEC,
)
from architect_cad_mcp.templates.workplaces import (
    ARCHITECTURAL_ATELIER_STUDIO_SPEC,
    OPEN_WORKPLACE_OFFICE_SPEC,
)


def make_grid_columns(
    v_grids: list[dict[str, Any]], h_grids: list[dict[str, Any]], size: float = 0.30
) -> list[dict[str, Any]]:
    """Compute structural RC columns at all orthogonal grid intersections."""
    cols: list[dict[str, Any]] = []
    for vg in v_grids:
        for hg in h_grids:
            cols.append({
                "id": f"C-{vg['id']}{hg['id']}",
                "x": float(vg["x"]),
                "y": float(hg["y"]),
                "size": size,
            })
    return cols


TEMPLATES: dict[str, dict[str, Any]] = {
    "courtyard_residence": copy.deepcopy(COURTYARD_RESIDENCE_SPEC),
    "modern_family_villa": copy.deepcopy(MODERN_FAMILY_VILLA_SPEC),
    "compact_urban_townhouse": copy.deepcopy(COMPACT_TOWNHOUSE_SPEC),
    "multi_unit_apartment_floor": copy.deepcopy(MULTI_UNIT_APARTMENT_FLOOR_SPEC),
    "open_workplace_office": copy.deepcopy(OPEN_WORKPLACE_OFFICE_SPEC),
    "architectural_atelier_studio": copy.deepcopy(ARCHITECTURAL_ATELIER_STUDIO_SPEC),
}

# Automatically populate structural RC column layout at grid intersections
for _tpl in TEMPLATES.values():
    if "columns" not in _tpl or not _tpl["columns"]:
        _tpl["columns"] = make_grid_columns(
            _tpl["grid"]["vertical"], _tpl["grid"]["horizontal"], size=0.30
        )


def register_template(template_id: str, spec: dict[str, Any]) -> None:
    """Register or replace an architectural template in the global registry."""
    cloned = copy.deepcopy(spec)
    if "columns" not in cloned or not cloned["columns"]:
        if "grid" in cloned and "vertical" in cloned["grid"] and "horizontal" in cloned["grid"]:
            cloned["columns"] = make_grid_columns(
                cloned["grid"]["vertical"], cloned["grid"]["horizontal"], size=0.30
            )
    TEMPLATES[template_id] = cloned


def list_templates(category: str | None = None) -> list[dict[str, Any]]:
    """List available architectural templates with geometric and spatial metrics."""
    items: list[dict[str, Any]] = []
    for tid, tpl in TEMPLATES.items():
        if category and tpl.get("category") != category:
            continue
        proj = tpl.get("project", {})
        w = float(proj.get("footprintWidth", 0))
        d = float(proj.get("footprintDepth", 0))
        items.append({
            "id": tid,
            "title": proj.get("title", "Untitled"),
            "category": tpl.get("category", "generic"),
            "scale": proj.get("scale", "1:100"),
            "footprint_m": f"{w:.2f}m x {d:.2f}m",
            "gross_area_m2": round(w * d, 2),
            "room_count": len(tpl.get("rooms", [])),
            "summary": tpl.get("summary", ""),
        })
    return items


def get_template(template_id: str) -> dict[str, Any]:
    """Retrieve an architectural template by its ID, returning an isolated deep copy."""
    if template_id not in TEMPLATES:
        available = ", ".join(sorted(TEMPLATES.keys()))
        raise KeyError(f"Unknown template '{template_id}'. Available: {available}")
    return copy.deepcopy(TEMPLATES[template_id])
