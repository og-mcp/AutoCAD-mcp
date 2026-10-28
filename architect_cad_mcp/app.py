"""FastMCP Application Factory and Server Assembly.

Follows Single Responsibility and Dependency Inversion Principles:
Assembles MCP server instance, modular tools, resources, and prompts.
"""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from architect_cad_mcp.prompts import register_all_prompts
from architect_cad_mcp.resources import register_all_resources
from architect_cad_mcp.tools import register_all_tools


def create_app(name: str = "architect-cad-mcp") -> FastMCP:
    """Create and configure a FastMCP architectural CAD server instance."""
    mcp = FastMCP(name)

    # Register all modular tools (Open/Closed Principle)
    register_all_tools(mcp)

    # Register all URI-addressable MCP resources
    register_all_resources(mcp)

    # Register all interactive architectural prompt workflows
    register_all_prompts(mcp)

    return mcp
