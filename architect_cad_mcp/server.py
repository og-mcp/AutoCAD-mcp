"""Dedicated 2D Architectural AutoCAD FastMCP Server.

Assembles modular architectural tools, resources, and prompts following SOLID principles.
Maintains full backward-compatible imports for direct script and test invocation.
"""

from __future__ import annotations

from architect_cad_mcp.app import create_app
from architect_cad_mcp.core.layers import (
    AIA_ARCHITECTURAL_LAYERS,
    FURNITURE_AND_FIXTURE_CATALOG,
    PLANE_CODES,
)
from architect_cad_mcp.domain.audit.dxf_audit import audit_dxf_file, audit_ezdxf_document
from architect_cad_mcp.domain.drc.validator import audit_architecture_spec
from architect_cad_mcp.domain.engines.multi_plane import (
    generate_full_cd_package,
    generate_plane_dxf_and_svg,
)
from architect_cad_mcp.domain.rendering.png_renderer import (
    render_dxf_file_to_png,
    render_dxf_to_png,
)
from architect_cad_mcp.state import SESSION_STATE
from architect_cad_mcp.templates.registry import TEMPLATES, get_template, list_templates

# Initialize application instance with all modular tools, resources, and prompts
mcp = create_app("architect-cad-mcp")

# Re-export the tool functions directly for backwards compatibility with tests and scripts
# We retrieve the actual decorated functions registered on the mcp instance or modules
from architect_cad_mcp.tools.annotation import register as _reg_anno  # noqa
from architect_cad_mcp.tools.arch_audit import register as _reg_audit  # noqa
from architect_cad_mcp.tools.arch_element import register as _reg_elem  # noqa
from architect_cad_mcp.tools.autocad_live import register as _reg_live  # noqa
from architect_cad_mcp.tools.drawing import register as _reg_draw  # noqa
from architect_cad_mcp.tools.orthographic_plane import register as _reg_plane  # noqa
from architect_cad_mcp.tools.system import register as _reg_sys  # noqa
from architect_cad_mcp.tools.template import register as _reg_tpl  # noqa


# Helper wrappers matching exact original signatures
def system(operation: str = "status") -> str:
    from architect_cad_mcp.tools.system import register
    # Extract registered tool or delegate
    return mcp._tool_manager.get_tool("system").fn(operation=operation)


def template(
    operation: str = "list_templates",
    template_id: str | None = None,
    category: str | None = None,
    overrides: dict | None = None,
    customizations_json: str | None = None,
    output_dir: str | None = None,
) -> str:
    return mcp._tool_manager.get_tool("template").fn(
        operation=operation,
        template_id=template_id,
        category=category,
        overrides=overrides,
        customizations_json=customizations_json,
        output_dir=output_dir,
    )


def drawing(
    operation: str = "get_spec",
    title: str | None = None,
    category: str = "house",
    width: float = 15.6,
    depth: float = 11.2,
    scale: str = "1:100",
    output_dir: str = "cad_output/active_drawing",
    output_directory: str | None = None,
    dxf_path: str | None = None,
    png_path: str | None = None,
    plane: str = "floor_plan",
    dpi: int = 150,
    include_entities: bool = False,
    color_mode: str = "color",
) -> str:
    return mcp._tool_manager.get_tool("drawing").fn(
        operation=operation,
        title=title,
        category=category,
        width=width,
        depth=depth,
        scale=scale,
        output_dir=output_dir,
        output_directory=output_directory,
        dxf_path=dxf_path,
        png_path=png_path,
        plane=plane,
        dpi=dpi,
        include_entities=include_entities,
        color_mode=color_mode,
    )


def arch_element(
    operation: str,
    data: dict | None = None,
    **kwargs,
) -> str:
    return mcp._tool_manager.get_tool("arch_element").fn(
        operation=operation,
        data=data,
        **kwargs,
    )


def orthographic_plane(
    operation: str = "generate_all_planes",
    plane: str = "floor_plan",
    plane_key: str | None = None,
    output_dir: str = "cad_output/active_drawing",
    output_directory: str | None = None,
) -> str:
    return mcp._tool_manager.get_tool("orthographic_plane").fn(
        operation=operation,
        plane=plane,
        plane_key=plane_key,
        output_dir=output_dir,
        output_directory=output_directory,
    )


def annotation(
    operation: str = "add_section_cut",
    data: dict | None = None,
    **kwargs,
) -> str:
    return mcp._tool_manager.get_tool("annotation").fn(
        operation=operation,
        data=data,
        **kwargs,
    )


def arch_audit(operation: str = "validate_anthropometrics") -> str:
    return mcp._tool_manager.get_tool("arch_audit").fn(operation=operation)


def autocad_live(
    operation: str = "export_scr_script",
    plane: str = "floor_plan",
    output_dir: str = "cad_output/active_drawing",
) -> str:
    return mcp._tool_manager.get_tool("autocad_live").fn(
        operation=operation,
        plane=plane,
        output_dir=output_dir,
    )


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(
        description="Dedicated 2D Architectural AutoCAD FastMCP Server (architect-cad-mcp)"
    )
    parser.add_argument(
        "--transport",
        choices=["stdio", "sse", "streamable-http"],
        default="stdio",
        help="MCP transport protocol (default: stdio)",
    )
    parser.add_argument(
        "--host",
        default="0.0.0.0",
        help="Host address for SSE / HTTP transport (default: 0.0.0.0)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port for SSE / HTTP transport (default: 8000)",
    )
    parser.add_argument(
        "--health",
        "--check-health",
        action="store_true",
        help="Run server diagnostics and exit with code 0 (healthy) or 1 (unhealthy)",
    )
    parser.add_argument(
        "--version",
        action="version",
        version="architect-cad-mcp 1.0.0",
    )
    args = parser.parse_args()

    if args.health:
        import json
        import sys
        from architect_cad_mcp.health import check_health

        results = check_health()
        print(json.dumps(results, indent=2))
        sys.exit(0 if results["status"] != "unhealthy" else 1)

    if args.transport in ("sse", "streamable-http"):
        mcp.settings.host = args.host
        mcp.settings.port = args.port

    mcp.run(transport=args.transport)


if __name__ == "__main__":
    main()
