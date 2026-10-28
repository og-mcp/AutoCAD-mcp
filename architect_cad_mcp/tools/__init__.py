"""Tools package and modular tool registration.

Follows Open/Closed Principle: adding a new tool is as simple as adding a module
with a `register(mcp: FastMCP)` function.
"""

from __future__ import annotations

from typing import Callable
from mcp.server.fastmcp import FastMCP

from architect_cad_mcp.tools import (
    annotation,
    arch_audit,
    arch_element,
    autocad_live,
    drawing,
    orthographic_plane,
    system,
    template,
)

# Registry of modular tool installers
TOOL_MODULES: list[Callable[[FastMCP], None]] = [
    system.register,
    template.register,
    drawing.register,
    arch_element.register,
    orthographic_plane.register,
    annotation.register,
    arch_audit.register,
    autocad_live.register,
]


def register_all_tools(mcp: FastMCP) -> None:
    """Register all modular architectural CAD tools with the FastMCP server."""
    for register_fn in TOOL_MODULES:
        register_fn(mcp)
