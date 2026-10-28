"""Health Check and Diagnostic Service for Docker, Kubernetes, and MCP Clients.

Validates the complete headless architectural CAD pipeline:
- MCP server tools, resources, and prompts registration
- Architectural template availability
- ezdxf document creation & modelspace setup
- Headless Matplotlib Agg rendering backend
- Neufert architectural DRC validation engine
- Handle-independent SHA-256 geometry digest calculation
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from typing import Any

logging.getLogger("ezdxf").setLevel(logging.WARNING)


def check_health() -> dict[str, Any]:
    """Execute a comprehensive runtime health audit of all server components."""
    diagnostics: dict[str, Any] = {
        "status": "healthy",
        "server": "architect-cad-mcp",
        "version": "1.0.0",
        "checks": {},
    }

    # 1. Verify Server Assembler & FastMCP Instance
    try:
        from architect_cad_mcp.server import mcp

        tool_count = len(mcp._tool_manager._tools)
        resource_count = len(mcp._resource_manager._resources)
        prompt_count = len(mcp._prompt_manager._prompts)
        template_res_count = len(mcp._resource_manager._templates)

        diagnostics["checks"]["mcp_server"] = {
            "status": "PASS",
            "tools_registered": tool_count,
            "resources_registered": resource_count,
            "prompts_registered": prompt_count,
            "resource_templates_registered": template_res_count,
        }
        if tool_count < 8:
            diagnostics["status"] = "degraded"
    except Exception as exc:
        diagnostics["status"] = "unhealthy"
        diagnostics["checks"]["mcp_server"] = {"status": "FAIL", "error": str(exc)}

    # 2. Verify Architectural Templates Registry
    try:
        from architect_cad_mcp.templates.registry import TEMPLATES, get_template

        sample_tpl = get_template("courtyard_residence")
        diagnostics["checks"]["templates"] = {
            "status": "PASS",
            "templates_loaded": len(TEMPLATES),
            "sample_verified": sample_tpl["project"]["title"],
        }
    except Exception as exc:
        diagnostics["status"] = "unhealthy"
        diagnostics["checks"]["templates"] = {"status": "FAIL", "error": str(exc)}

    # 3. Verify Neufert DRC Validator
    try:
        from architect_cad_mcp.domain.drc.validator import audit_architecture_spec

        report = audit_architecture_spec(sample_tpl)
        diagnostics["checks"]["drc_validator"] = {
            "status": "PASS" if report["drc_status"] == "PASS" else "FAIL",
            "checks_passed": report["counts"]["passed"],
            "errors": report["counts"]["errors"],
        }
    except Exception as exc:
        diagnostics["status"] = "unhealthy"
        diagnostics["checks"]["drc_validator"] = {"status": "FAIL", "error": str(exc)}

    # 4. Verify ezdxf Headless Engine & Geometric Digest
    try:
        from architect_cad_mcp.domain.audit.dxf_audit import audit_ezdxf_document
        from architect_cad_mcp.domain.engines.multi_plane import setup_ezdxf_document

        doc, msp = setup_ezdxf_document()
        msp.add_line((0, 0), (10, 0), dxfattribs={"layer": "A-WALL-FULL"})
        audit = audit_ezdxf_document(doc)

        diagnostics["checks"]["ezdxf_engine"] = {
            "status": "PASS",
            "dxf_version": audit["dxf_version"],
            "insunits": audit["units"],
            "geometry_digest": audit["geometry_digest"][:16] + "...",
        }
    except Exception as exc:
        diagnostics["status"] = "unhealthy"
        diagnostics["checks"]["ezdxf_engine"] = {"status": "FAIL", "error": str(exc)}

    # 5. Verify Headless Matplotlib Agg Backend
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        backend = matplotlib.get_backend()
        fig = plt.figure(figsize=(2, 2))
        plt.close(fig)

        diagnostics["checks"]["matplotlib_agg"] = {
            "status": "PASS",
            "backend": backend,
            "headless_compatible": True,
        }
    except Exception as exc:
        diagnostics["status"] = "unhealthy"
        diagnostics["checks"]["matplotlib_agg"] = {"status": "FAIL", "error": str(exc)}

    return diagnostics


def main() -> None:
    """CLI runner for Docker HEALTHCHECK and monitoring probes."""
    parser = argparse.ArgumentParser(description="Architect-CAD-MCP Health Check")
    parser.add_argument(
        "--quiet", "-q", action="store_true", help="Suppress JSON output, exit code only"
    )
    args = parser.parse_args()

    results = check_health()
    if not args.quiet:
        print(json.dumps(results, indent=2))

    if results["status"] == "unhealthy":
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
