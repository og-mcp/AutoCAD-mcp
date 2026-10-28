"""Multi-Plane 2D Orthographic CAD Engine (ezdxf + AutoCAD .scr + Architectural SVG).

Backward-compatibility shim re-exporting from `architect_cad_mcp.domain.engines.multi_plane`.
"""

from architect_cad_mcp.domain.engines.multi_plane import (
    build_autocad_scr,
    build_plane_svg,
    generate_full_cd_package,
    generate_plane_dxf_and_svg,
    setup_ezdxf_document,
)

__all__ = [
    "setup_ezdxf_document",
    "generate_plane_dxf_and_svg",
    "generate_full_cd_package",
    "build_autocad_scr",
    "build_plane_svg",
]
