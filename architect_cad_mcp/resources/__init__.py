"""MCP Resources registration package."""

from __future__ import annotations

from typing import Callable
from mcp.server.fastmcp import FastMCP

from architect_cad_mcp.resources import drawings, standards, templates

RESOURCE_MODULES: list[Callable[[FastMCP], None]] = [
    standards.register,
    templates.register,
    drawings.register,
]


def register_all_resources(mcp: FastMCP) -> None:
    """Register all MCP architectural resources with the FastMCP server."""
    for register_fn in RESOURCE_MODULES:
        register_fn(mcp)
