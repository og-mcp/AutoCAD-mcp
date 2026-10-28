"""Domain logic layer: DRC compliance, headless geometric audits, engines, and rendering."""

from architect_cad_mcp.domain.audit.dxf_audit import (
    audit_dxf_file,
    audit_ezdxf_document,
    compute_geometry_digest,
)
from architect_cad_mcp.domain.drc.validator import audit_architecture_spec
from architect_cad_mcp.domain.engines.multi_plane import (
    generate_full_cd_package,
    generate_plane_dxf_and_svg,
)
from architect_cad_mcp.domain.rendering.png_renderer import (
    render_dxf_file_to_png,
    render_dxf_to_png,
)

__all__ = [
    "audit_architecture_spec",
    "audit_ezdxf_document",
    "audit_dxf_file",
    "compute_geometry_digest",
    "generate_plane_dxf_and_svg",
    "generate_full_cd_package",
    "render_dxf_to_png",
    "render_dxf_file_to_png",
]
