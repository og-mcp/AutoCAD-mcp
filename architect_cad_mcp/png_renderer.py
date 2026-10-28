"""Deterministic Headless PNG Renderer for ezdxf Drawings via Matplotlib + Pillow.

Backward-compatibility shim re-exporting from `architect_cad_mcp.domain.rendering.png_renderer`.
"""

from architect_cad_mcp.domain.rendering.png_renderer import (
    render_dxf_file_to_png,
    render_dxf_to_png,
)

__all__ = ["render_dxf_to_png", "render_dxf_file_to_png"]
