"""Architectural Design Rule Check (DRC), Neufert Anthropometrics & Code Validator.

Backward-compatibility shim re-exporting from `architect_cad_mcp.domain.drc.validator`.
"""

from architect_cad_mcp.core.constants import MIN_DOOR_WIDTHS, MIN_ROOM_SPECS
from architect_cad_mcp.domain.drc.validator import audit_architecture_spec

__all__ = [
    "MIN_ROOM_SPECS",
    "MIN_DOOR_WIDTHS",
    "audit_architecture_spec",
]
