"""Hands-on labs: one per part of a course, ``videos/<series>/labs/labNN.py``.

    python -m videos.coursekit.labs stats 12          # run Lab 12 of Statistics, Built: its table, its figure
    python -m videos.coursekit.labs stats 12 --show   # ... and open the figure
    python -m videos.coursekit.labs cs --all
    python -m videos.coursekit.labs philosophy --list

A lab is a module with a docstring that starts ``Lab N:``, ``TITLE``, ``GOAL``, ``TASKS`` (three things to change
next) and ``run(seed=0) -> Lab``.  Every lab is seeded, runs in seconds with no downloads, asserts its own result
against the theory it illustrates, and draws one figure in the films' palette::

    from videos.coursekit import labs
    from explainer.stats.kit import ols          # the series' own library, where it has one

    def run(seed=0):
        lab = labs.Lab()
        lab.row("slope", f"{slope:.3f}")
        assert abs(slope - 2) < 0.1
        fig, ax = labs.figure()
        ...
        lab.fig = fig
        lab.note = "One line saying what the numbers mean."
        return lab

The labs need numpy, scipy and matplotlib, not manim.  The series' libraries (statkit and the World, Pebble, the
Reasoner, the AI series' autodiff) do not import manim either, but the packages above them do; where manim is not
installed (a laptop, Colab, the site's CI), importing this module registers ``explainer`` and the series' packages
as bare namespaces so those libraries import on their own.
"""

from __future__ import annotations

import importlib
import importlib.util
import sys
import types
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
_NAMESPACES = ("explainer", "explainer.ai", "explainer.analysis", "explainer.stats", "explainer.cs",
               "explainer.philosophy", "explainer.quant", "explainer.music")


def _standalone() -> None:
    """Without manim, let ``explainer.stats.kit``, ``explainer.cs.pebble``, ... import on their own."""
    if importlib.util.find_spec("manim") is not None or getattr(sys.modules.get("explainer"), "__file__", None):
        return  # the films' toolkit is installed (or already imported): nothing to stand in for
    for name in _NAMESPACES:
        if name in sys.modules:  # Quant, Built's labs registered theirs first
            continue
        module = types.ModuleType(name)
        module.__path__ = [str(ROOT.joinpath(*name.split(".")))]
        sys.modules[name] = module
        if "." in name:
            setattr(sys.modules[name.rpartition(".")[0]], name.rpartition(".")[2], module)


_standalone()

# The films' palette (explainer.style), repeated here so a lab needs no manim.
BG = "#0E1117"
PANEL = "#151B26"
INK = "#E6EDF3"
MUTED = "#8B98A9"
GRID = "#263041"
BLUE = "#58A6FF"
GOLD = "#F7D154"
GREEN = "#4ADE80"
RED = "#F87171"
PURPLE = "#A78BFA"
ORANGE = "#FB923C"
TEAL = "#2DD4BF"
PINK = "#E879F9"
SAND = "#E2C08D"
GREY = "#94A3B8"
CYCLE = (BLUE, GOLD, GREEN, RED, PURPLE, ORANGE, TEAL, PINK)


@dataclass
class Lab:
    """What a lab returns: rows of (label, value) to print, its figure, and one line on what the numbers mean."""

    rows: list = field(default_factory=list)
    fig: object = None
    note: str = ""
    audio: object = None  # Music, Built: a sound to go with the figure (anything with ``write_pcm16(path)``)

    def row(self, label: str, value, fmt: str = "") -> None:
        self.rows.append((label, format(value, fmt) if fmt else str(value)))

    def table(self) -> str:
        width = max((len(a) for a, _ in self.rows), default=0)
        lines = [f"{a:<{width}}  {b}" for a, b in self.rows]
        if self.note:
            lines += ["", self.note]
        return "\n".join(lines)


def figure(ncols: int = 1, nrows: int = 1, size=(9.6, 4.6), **kw):
    """A figure in the films' look.  Returns (fig, axes) as ``plt.subplots`` does."""
    import matplotlib

    matplotlib.use("Agg", force=False)
    import matplotlib.pyplot as plt
    from cycler import cycler

    plt.rcParams.update({
        "figure.facecolor": BG, "axes.facecolor": BG, "savefig.facecolor": BG, "axes.edgecolor": GRID,
        "axes.labelcolor": MUTED, "text.color": INK, "xtick.color": MUTED, "ytick.color": MUTED,
        "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.6, "axes.spines.top": False,
        "axes.spines.right": False, "font.size": 10, "axes.titlesize": 11, "axes.titleweight": "bold",
        "axes.titlecolor": INK, "legend.frameon": False, "legend.fontsize": 9, "lines.linewidth": 1.8,
        "font.family": "DejaVu Sans", "axes.titlelocation": "left", "figure.dpi": 100,
        "axes.prop_cycle": cycler(color=CYCLE),
    })
    fig, ax = plt.subplots(nrows, ncols, figsize=size, constrained_layout=True, **kw)
    return fig, ax


def path(series: str, part: int) -> Path:
    return ROOT / "videos" / series / "labs" / f"lab{part:02d}.py"


def available(series: str) -> list:
    """The parts of ``series`` that have a lab."""
    return sorted(int(p.stem[3:]) for p in (ROOT / "videos" / series / "labs").glob("lab[0-9][0-9].py"))


def load(series: str, part: int):
    """The module of Lab ``part`` of ``series``."""
    return importlib.import_module(f"videos.{series}.labs.lab{part:02d}")


def source(series: str, part: int) -> str:
    return path(series, part).read_text()


def run(series: str, part: int, seed: int = 0) -> Lab:
    return load(series, part).run(seed=seed)


def save(lab: Lab, out) -> Path:
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    lab.fig.savefig(out, dpi=160)
    import matplotlib.pyplot as plt

    plt.close(lab.fig)
    return out


def main(series: str | None = None) -> None:
    import argparse
    import time

    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    if series is None:
        ap.add_argument("series", help="ai, stats, cs, philosophy, analysis or music")
    ap.add_argument("parts", nargs="*", type=int, help="part numbers")
    ap.add_argument("--all", action="store_true", help="run every lab")
    ap.add_argument("--list", action="store_true", help="list the labs and exit")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--show", action="store_true", help="open the figure in a window")
    ap.add_argument("--out", default=None, help="where figures are saved (default renders/labs/<series>)")
    args = ap.parse_args()
    series = series or args.series
    parts = available(series) if (args.all or args.list) else args.parts
    if not parts:
        ap.error("give a part number, --all or --list")
    for part in parts:
        module = load(series, part)
        if args.list:
            print(f"{part:>2}  {module.TITLE}")
            continue
        start = time.time()
        lab = module.run(seed=args.seed)
        print(f"Lab {part} · {module.TITLE}\n{module.GOAL}\n\n{lab.table()}")
        if args.show:
            import matplotlib.pyplot as plt

            plt.show()
        out = save(lab, Path(args.out or ROOT / "renders" / "labs" / series) / f"lab{part:02d}.png")
        if lab.audio is not None:
            lab.audio.write_pcm16(out.with_suffix(".wav"))
            print(f"\nsound:  {out.with_suffix('.wav')}")
        print(f"\nfigure: {out}   ({time.time() - start:.1f} s)\n\nNow change it:")
        for task in module.TASKS:
            print(f"  - {task}")
        print()


if __name__ == "__main__":
    main()
