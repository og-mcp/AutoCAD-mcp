#!/usr/bin/env python3
"""Headless demo: build an architectural floor plan, audit it, and render a deterministic PNG.

No AutoCAD required. Runs on Windows, macOS, Linux, or WSL using ezdxf + matplotlib.

    python examples/headless_demo.py
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from architect_cad_mcp import (
    audit_architecture_spec,
    audit_dxf_file,
    generate_plane_dxf_and_svg,
    get_template,
)


def main() -> int:
    out_root = Path(os.environ.get("ARCHITECT_CAD_MCP_OUTPUT_ROOT", "demo-output")).resolve()
    spec = get_template(sys.argv[1] if len(sys.argv) > 1 else "courtyard_residence")

    # 1. Architectural DRC (Neufert / Blondel / daylight / circulation)
    arch = audit_architecture_spec(spec)

    # 2. Generate floor plan DXF + PNG + structured geometry audit (in-memory ezdxf)
    plane = generate_plane_dxf_and_svg(spec, "floor_plan", out_root)

    # 3. Re-audit the exported DXF from disk and confirm the geometry digest round-trips
    reaudit = audit_dxf_file(plane["dxf_path"])
    digest_match = reaudit["geometry_digest"] == plane["geometry_digest"]

    ok = arch["drc_status"] == "PASS" and plane["geometry_drc"]["status"] == "PASS" and digest_match
    print(json.dumps({
        "ok": ok,
        "backend": "ezdxf",
        "requires_autocad": False,
        "project": spec["project"]["title"],
        "entity_count": plane["entity_count"],
        "units": plane["units"]["name"],
        "bounds": plane["bounds"],
        "geometry_drc": plane["geometry_drc"]["status"],
        "architectural_drc": arch["drc_status"],
        "architectural_checks_passed": arch["counts"]["passed"],
        "geometry_digest": plane["geometry_digest"],
        "exported_dxf_digest_match": digest_match,
        "dxf": plane["dxf_path"],
        "png": plane["png_preview"]["path"],
        "png_size": [plane["png_preview"]["width"], plane["png_preview"]["height"]],
        "png_sha256": plane["png_preview"]["sha256"],
    }, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
