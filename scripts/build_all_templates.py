#!/usr/bin/env python3
"""
Batch-generate all 6 ready-to-use architectural templates across all 6 orthographic planes
(36 DXF files, 36 AutoCAD SCR scripts, 36 SVG sheets, plus DRC & SHA-256 manifests).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from architect_cad_mcp import TEMPLATES, generate_full_cd_package, get_template


def main() -> int:
    base_out = Path("cad_output/all_templates")
    print("=== BUILDING ALL 6 ARCHITECTURAL TEMPLATES x 6 ORTHOGRAPHIC PLANES ===")
    for tid in TEMPLATES:
        spec = get_template(tid)
        cat = spec["project"].get("category", "general")
        out_dir = base_out / cat / tid
        pkg = generate_full_cd_package(spec, out_dir)
        drc = pkg["drc_report"]
        if drc["drc_status"] != "PASS":
            print(f"FAIL: {tid} had DRC errors: {drc['errors']}")
            return 1
        print(
            f"  [PASS] {tid:28s} | {cat:14s} | {drc['metrics']['gross_area_m2']:6.1f} m2 | "
            f"{drc['counts']['passed']:2d} checks passed | 6 planes -> {out_dir}"
        )
    print("\nAll 6 templates (36 DXF + 36 SCR + 36 SVG sheets) built and verified with 0 DRC errors.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
