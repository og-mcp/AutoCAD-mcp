#!/usr/bin/env python3
"""
Build complete 6-plane 2D AutoCAD Construction Document package (.dxf, .scr, .svg, DRC report)
for Multi-Unit Residential Floor Building ('multi_unit_apartment_floor').
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from architect_cad_mcp import generate_full_cd_package, get_template


def main() -> int:
    parser = argparse.ArgumentParser(description="Build 2D Multi-Unit Floor Building CAD Plan.")
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path("cad_output/floor_buildings/multi_unit_apartment_floor"),
        help="Output folder for generated CAD package.",
    )
    args = parser.parse_args()

    spec = get_template("multi_unit_apartment_floor")
    pkg = generate_full_cd_package(spec, args.out_dir)
    drc = pkg["drc_report"]
    print(
        f"[FLOOR BUILDING] {spec['project']['title']} -> DRC: {drc['drc_status']} "
        f"({drc['counts']['passed']} passed, {drc['counts']['errors']} errors) | "
        f"6 Planes written to: {args.out_dir.resolve()}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
