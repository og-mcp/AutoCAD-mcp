"""Residential house templates package."""

from architect_cad_mcp.templates.houses.compact_townhouse import (
    SPEC as COMPACT_TOWNHOUSE_SPEC,
)
from architect_cad_mcp.templates.houses.courtyard_residence import (
    SPEC as COURTYARD_RESIDENCE_SPEC,
)
from architect_cad_mcp.templates.houses.modern_family_villa import (
    SPEC as MODERN_FAMILY_VILLA_SPEC,
)

__all__ = [
    "COURTYARD_RESIDENCE_SPEC",
    "MODERN_FAMILY_VILLA_SPEC",
    "COMPACT_TOWNHOUSE_SPEC",
]
