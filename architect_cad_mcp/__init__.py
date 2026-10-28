"""Dedicated 2D Architectural AutoCAD MCP Server (architect-cad-mcp)."""

from architect_cad_mcp.app import create_app
from architect_cad_mcp.core.constants import (
    BLONDEL_MAX_MM,
    BLONDEL_MIN_MM,
    FURNITURE_AND_FIXTURE_CATALOG,
    MIN_ROOM_SPECS,
)
from architect_cad_mcp.core.layers import (
    AIA_ARCHITECTURAL_LAYERS,
    LAYER_MAP,
    PLANE_CODES,
)
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
from architect_cad_mcp.server import mcp
from architect_cad_mcp.state import SESSION_STATE
from architect_cad_mcp.templates.registry import (
    TEMPLATES,
    get_template,
    list_templates,
    register_template,
)

__version__ = "1.0.0"

__all__ = [
    "create_app",
    "mcp",
    "SESSION_STATE",
    "AIA_ARCHITECTURAL_LAYERS",
    "LAYER_MAP",
    "PLANE_CODES",
    "FURNITURE_AND_FIXTURE_CATALOG",
    "MIN_ROOM_SPECS",
    "BLONDEL_MIN_MM",
    "BLONDEL_MAX_MM",
    "TEMPLATES",
    "get_template",
    "list_templates",
    "register_template",
    "audit_architecture_spec",
    "audit_ezdxf_document",
    "audit_dxf_file",
    "compute_geometry_digest",
    "generate_plane_dxf_and_svg",
    "generate_full_cd_package",
    "render_dxf_to_png",
    "render_dxf_file_to_png",
]
