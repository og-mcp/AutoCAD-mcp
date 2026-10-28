"""Architectural templates catalog and registry."""

from architect_cad_mcp.templates.base import ArchitecturalTemplate
from architect_cad_mcp.templates.buildings import MULTI_UNIT_APARTMENT_FLOOR_SPEC
from architect_cad_mcp.templates.houses import (
    COMPACT_TOWNHOUSE_SPEC,
    COURTYARD_RESIDENCE_SPEC,
    MODERN_FAMILY_VILLA_SPEC,
)
from architect_cad_mcp.templates.registry import (
    TEMPLATES,
    get_template,
    list_templates,
    make_grid_columns,
    register_template,
)
from architect_cad_mcp.templates.workplaces import (
    ARCHITECTURAL_ATELIER_STUDIO_SPEC,
    OPEN_WORKPLACE_OFFICE_SPEC,
)

__all__ = [
    "ArchitecturalTemplate",
    "TEMPLATES",
    "get_template",
    "list_templates",
    "register_template",
    "make_grid_columns",
    "COURTYARD_RESIDENCE_SPEC",
    "MODERN_FAMILY_VILLA_SPEC",
    "COMPACT_TOWNHOUSE_SPEC",
    "MULTI_UNIT_APARTMENT_FLOOR_SPEC",
    "OPEN_WORKPLACE_OFFICE_SPEC",
    "ARCHITECTURAL_ATELIER_STUDIO_SPEC",
]
