"""AutoCAD live replay scripts and AutoLISP dispatcher MCP tool."""

from __future__ import annotations

from pathlib import Path

from mcp.server.fastmcp import FastMCP

from architect_cad_mcp.domain.engines.multi_plane import generate_plane_dxf_and_svg
from architect_cad_mcp.state import SESSION_STATE, error_response, ok_response


def register(mcp: FastMCP) -> None:
    @mcp.tool()
    def autocad_live(
        operation: str = "export_scr_script",
        plane: str = "floor_plan",
        output_dir: str = "cad_output/active_drawing",
    ) -> str:
        """Generate AutoCAD/AutoCAD LT live command scripts (.scr) or inspect the AutoLISP dispatcher.

        Operations:
        - export_scr_script: Generate an AutoCAD `.scr` script for `plane` that can be run via `SCRIPT` in AutoCAD.
        - get_lisp_dispatcher_path: Return the path to `lisp-code/mcp_arch_dispatch.lsp` for AutoCAD APPLOAD.
        """
        spec = SESSION_STATE.spec

        if operation == "export_scr_script":
            res = generate_plane_dxf_and_svg(spec, plane, Path(output_dir))
            return ok_response({"scr_path": res["scr_path"], "dxf_path": res["dxf_path"]})

        if operation in ("get_lisp_dispatcher_path", "export_lisp_dispatcher"):
            # Locate lisp-code directory relative to project root or workspace
            lisp_path = Path(__file__).resolve().parents[2] / "lisp-code" / "mcp_arch_dispatch.lsp"
            if not lisp_path.exists():
                lisp_path = Path(__file__).resolve().parents[1] / "lisp-code" / "mcp_arch_dispatch.lsp"
            if not lisp_path.exists():
                lisp_path = Path("lisp-code/mcp_arch_dispatch.lsp").resolve()
            return ok_response({
                "lisp_dispatcher_path": str(lisp_path),
                "path": str(lisp_path),
                "exists": lisp_path.exists(),
                "instructions": "In AutoCAD, type (load \"mcp_arch_dispatch.lsp\") then type MCP-DISPATCH.",
            })

        return error_response("E_INVALID_OPERATION", f"Unknown autocad_live operation: {operation}")
