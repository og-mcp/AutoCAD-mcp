"""Deterministic Headless PNG Renderer for ezdxf Drawings via Matplotlib + Pillow."""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

import ezdxf


def render_dxf_to_png(
    doc: ezdxf.document.Drawing,
    out_path: str | Path,
    dpi: int = 150,
    background: str = "#FFFFFF",
    force: bool = True,
    color_mode: str = "color",
) -> dict[str, Any]:
    """Render an ezdxf document deterministically to a PNG file without AutoCAD.

    color_mode: "color" keeps AIA layer colors (ACI 7 plots black on white paper);
    "monochrome" emulates a monochrome.ctb plot style (all linework black).
    """
    output = Path(out_path).expanduser().resolve()
    if output.suffix.lower() != ".png":
        output = output.with_suffix(".png")
    dpi = max(72, min(int(dpi), 600))
    if output.exists() and not force:
        raise FileExistsError(f"Preview PNG already exists: {output}")

    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from ezdxf.addons.drawing import Frontend, RenderContext
    from ezdxf.addons.drawing.config import BackgroundPolicy, ColorPolicy, Configuration
    from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
    from PIL import Image

    cfg = Configuration(
        background_policy=BackgroundPolicy.WHITE,
        color_policy=ColorPolicy.MONOCHROME_LIGHT_BG if color_mode == "monochrome" else ColorPolicy.COLOR,
        lineweight_scaling=1.6,
        min_lineweight=0.12,
    )

    # Fixed figure geometry, full-figure axes, Agg backend and stripped PNG
    # metadata => byte-stable output for identical geometry and library versions.
    fig = plt.figure(figsize=(16, 10), dpi=dpi)
    try:
        fig.patch.set_facecolor(background)
        ax = fig.add_axes((0.0, 0.0, 1.0, 1.0))
        ax.set_facecolor(background)
        ax.set_aspect("equal")
        ax.set_axis_off()

        ctx = RenderContext(doc)
        out = MatplotlibBackend(ax, adjust_figure=False)
        Frontend(ctx, out, config=cfg).draw_layout(doc.modelspace(), finalize=True)

        output.parent.mkdir(parents=True, exist_ok=True)
        if force:
            output.unlink(missing_ok=True)
        fig.savefig(
            str(output),
            format="png",
            dpi=dpi,
            facecolor=background,
            metadata={"Software": None},
        )
    finally:
        plt.close(fig)

    raw_bytes = output.read_bytes()
    with Image.open(output) as img:
        width, height = img.size

    return {
        "ok": True,
        "path": str(output),
        "format": "png",
        "renderer": "ezdxf-matplotlib",
        "color_mode": color_mode,
        "dpi": dpi,
        "background": background,
        "width": width,
        "height": height,
        "bytes": len(raw_bytes),
        "sha256": hashlib.sha256(raw_bytes).hexdigest(),
    }


def render_dxf_file_to_png(
    dxf_path: str | Path,
    png_path: str | Path,
    dpi: int = 150,
    background: str = "#FFFFFF",
    force: bool = True,
    color_mode: str = "color",
) -> dict[str, Any]:
    """Read a DXF file from disk and render it to a PNG."""
    input_path = Path(dxf_path).expanduser().resolve()
    if not input_path.exists():
        raise FileNotFoundError(f"Input DXF does not exist: {input_path}")
    doc = ezdxf.readfile(str(input_path))
    return render_dxf_to_png(
        doc,
        png_path,
        dpi=dpi,
        background=background,
        force=force,
        color_mode=color_mode,
    )
