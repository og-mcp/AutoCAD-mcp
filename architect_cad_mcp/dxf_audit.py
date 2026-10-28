"""Structured ezdxf drawing audit, entity normalization, geometry digest, and topology DRC.

Backward-compatibility shim re-exporting from `architect_cad_mcp.domain.audit.dxf_audit`.
"""

from architect_cad_mcp.domain.audit.dxf_audit import (
    INSUNITS_NAMES,
    audit_dxf_file,
    audit_ezdxf_document,
    compute_geometry_digest,
    normalize_ezdxf_entity,
)

__all__ = [
    "INSUNITS_NAMES",
    "normalize_ezdxf_entity",
    "compute_geometry_digest",
    "audit_ezdxf_document",
    "audit_dxf_file",
]
