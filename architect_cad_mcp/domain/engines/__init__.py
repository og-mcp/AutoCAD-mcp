"""Domain package for 2D architectural drafting, poché generation, and orthographic projections."""

from architect_cad_mcp.domain.engines.annotations import (
    add_common_grid_and_frame,
    add_dxf_arch_dim_h,
    add_dxf_arch_dim_v,
    add_dxf_poche,
    add_dxf_rect,
)
from architect_cad_mcp.domain.engines.multi_plane import (
    build_autocad_scr,
    build_plane_svg,
    generate_full_cd_package,
    generate_plane_dxf_and_svg,
    setup_ezdxf_document,
)
from architect_cad_mcp.domain.engines.walls import wall_segments_with_openings

__all__ = [
    "setup_ezdxf_document",
    "generate_plane_dxf_and_svg",
    "generate_full_cd_package",
    "build_autocad_scr",
    "build_plane_svg",
    "add_dxf_rect",
    "add_dxf_poche",
    "add_dxf_arch_dim_h",
    "add_dxf_arch_dim_v",
    "add_common_grid_and_frame",
    "wall_segments_with_openings",
]
