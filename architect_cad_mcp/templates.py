"""Ready-to-use 2D Architectural Building Templates (Houses, Floor Buildings, Workplaces).

Backward-compatibility shim re-exporting from `architect_cad_mcp.templates`.
"""

from architect_cad_mcp.templates.registry import (
    TEMPLATES,
    get_template,
    list_templates,
    make_grid_columns,
    register_template,
)

__all__ = [
    "TEMPLATES",
    "get_template",
    "list_templates",
    "register_template",
    "make_grid_columns",
]
