#!/usr/bin/env python3
"""
Build complete 6-plane 2D AutoCAD Construction Document packages (.dxf, .scr, .svg, DRC report)
for House templates ('courtyard_residence', 'modern_family_villa', 'compact_urban_townhouse').
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from architect_cad_mcp import generate_full_cd_package, get_template, list_templates


def main() -> int:
    parser = argparse.ArgumentParser(description="Build 2D Architectural House CAD Plans.")
    parser.add_argument(
        "--template",
        default="all",
        choices=["all", "courtyard_residence", "modern_family_villa", "compact_urban_townhouse"],
        help="House template to build.",
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path("cad_output/houses"),
        help="Output folder for generated CAD packages.",
    )
    args = parser.parse_args()

    house_ids = (
        [t["id"] for t in list_templates(category="house")]
        if args.template == "all"
        else [args.template]
    )

    for tid in house_ids:
        spec = get_template(tid)
        target_dir = args.out_dir / tid
        pkg = generate_full_cd_package(spec, target_dir)
        drc = pkg["drc_report"]
        print(
            f"[HOUSE: {tid}] {spec['project']['title']} -> DRC: {drc['drc_status']} "
            f"({drc['counts']['passed']} passed, {drc['counts']['errors']} errors) | "
            f"6 Planes written to: {target_dir.resolve()}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
