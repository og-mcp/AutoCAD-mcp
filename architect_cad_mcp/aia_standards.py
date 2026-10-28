"""AIA CAD Layer Guidelines, Plot Lineweights, Linetypes, and Block Catalogs.

Backward-compatibility shim re-exporting from `architect_cad_mcp.core`.
"""

from architect_cad_mcp.core.constants import FURNITURE_AND_FIXTURE_CATALOG
from architect_cad_mcp.core.layers import (
    AIA_ARCHITECTURAL_LAYERS,
    LAYER_MAP,
    PLANE_CODES,
)

__all__ = [
    "AIA_ARCHITECTURAL_LAYERS",
    "LAYER_MAP",
    "PLANE_CODES",
    "FURNITURE_AND_FIXTURE_CATALOG",
]
