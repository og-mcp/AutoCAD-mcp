"""Domain package for structured DXF geometric audit and SHA-256 geometry digest."""

from architect_cad_mcp.domain.audit.dxf_audit import (
    INSUNITS_NAMES,
    audit_dxf_file,
    audit_ezdxf_document,
    audit_geometry_drc,
    compute_geometry_digest,
    compute_modelspace_bounds,
    normalize_ezdxf_entity,
)

__all__ = [
    "INSUNITS_NAMES",
    "normalize_ezdxf_entity",
    "compute_geometry_digest",
    "compute_modelspace_bounds",
    "audit_geometry_drc",
    "audit_ezdxf_document",
    "audit_dxf_file",
]
