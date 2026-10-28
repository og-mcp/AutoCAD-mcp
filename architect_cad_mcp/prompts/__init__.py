"""MCP Prompts registration package."""

from __future__ import annotations

from typing import Callable
from mcp.server.fastmcp import FastMCP

from architect_cad_mcp.prompts import (
    apartment,
    audit,
    cd_package,
    house,
    workplace,
)

PROMPT_MODULES: list[Callable[[FastMCP], None]] = [
    house.register,
    apartment.register,
    workplace.register,
    audit.register,
    cd_package.register,
]


def register_all_prompts(mcp: FastMCP) -> None:
    """Register all MCP architectural prompts with the FastMCP server."""
    for register_fn in PROMPT_MODULES:
        register_fn(mcp)
