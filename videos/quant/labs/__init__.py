"""Quant, Built: one hands-on lab per part, on the House library (``explainer/quant/house``).

    python -m videos.quant.labs 10            # run Lab 10: print its table, save its figure to renders/labs/
    python -m videos.quant.labs 10 --show     # ... and open the figure
    python -m videos.quant.labs --all         # every lab (about a minute)
    python -m videos.quant.labs --list

A lab is ``labNN.py`` with ``TITLE``, ``GOAL``, ``TASKS`` (what to change next) and ``run(seed=0) -> Lab``.  Every
lab is seeded, runs in a few seconds on simulated data (no downloads), asserts its own result against the theory
it illustrates, and draws one figure in the films' palette.  The course site (``tools/course_site.py``) runs them
and prints their code, output and figure on each part's page; ``tests/test_quant_labs.py`` runs them all.

The House needs only numpy and scipy.  Where manim is not installed (a laptop, Colab, the site's CI), importing
this package registers ``explainer`` and ``explainer.quant`` as bare namespaces, so ``explainer.quant.house``
imports without the films' toolkit::

    pip install numpy scipy matplotlib numba
    python -m videos.quant.labs 10
"""

from __future__ import annotations

import importlib
import importlib.util
import sys
import types
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
N_PARTS = 43


def _standalone_house() -> None:
    """Without manim, let ``explainer.quant.house`` import on its own (it is numpy and scipy only)."""
    if "explainer" in sys.modules or importlib.util.find_spec("manim") is not None:
        return
    for name, path in (("explainer", ROOT / "explainer"), ("explainer.quant", ROOT / "explainer" / "quant")):
        module = types.ModuleType(name)
        module.__path__ = [str(path)]
        sys.modules[name] = module


_standalone_house()

# The films' palette (explainer.style: BACKGROUND and QC), repeated here so a lab needs no manim.
BG = "#0E1117"
PANEL = "#151B26"
INK = "#E6EDF3"
MUTED = "#8B98A9"
GRID = "#263041"
Q = "#A78BFA"  # risk-neutral: prices, implied quantities
P = "#FBBF24"  # real-world: forecasts, realized quantities
SPOT = "#58A6FF"
OPTION = "#E879F9"
GAIN = "#4ADE80"
LOSS = "#F87171"
IMPLIED = "#FB923C"
REALIZED = "#2DD4BF"
HOUSE = "#E2C08D"
CASH = "#94A3B8"


@dataclass
class Lab:
    """What a lab returns: rows of (label, value) to print, and its figure."""

    rows: list = field(default_factory=list)
    fig: object = None
    note: str = ""

    def row(self, label: str, value, fmt: str = "") -> None:
        self.rows.append((label, format(value, fmt) if fmt else str(value)))

    def table(self) -> str:
        width = max((len(a) for a, _ in self.rows), default=0)
        lines = [f"{a:<{width}}  {b}" for a, b in self.rows]
        if self.note:
            lines.append("")
            lines.append(self.note)
        return "\n".join(lines)


def figure(ncols: int = 1, nrows: int = 1, size=(9.6, 4.6), **kw):
    """A figure in the films' look.  Returns (fig, axes) as ``plt.subplots`` does."""
    import matplotlib

    matplotlib.use("Agg", force=False)
    import matplotlib.pyplot as plt

    plt.rcParams.update({
        "figure.facecolor": BG, "axes.facecolor": BG, "savefig.facecolor": BG, "axes.edgecolor": GRID,
        "axes.labelcolor": MUTED, "text.color": INK, "xtick.color": MUTED, "ytick.color": MUTED,
        "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.6, "axes.spines.top": False,
        "axes.spines.right": False, "font.size": 10, "axes.titlesize": 11, "axes.titleweight": "bold",
        "axes.titlecolor": INK, "legend.frameon": False, "legend.fontsize": 9, "lines.linewidth": 1.8,
        "font.family": "DejaVu Sans", "axes.titlelocation": "left", "figure.dpi": 100,
    })
    fig, ax = plt.subplots(nrows, ncols, figsize=size, constrained_layout=True, **kw)
    return fig, ax


def load(part: int):
    """The module of Lab ``part``."""
    return importlib.import_module(f"videos.quant.labs.lab{part:02d}")


def source(part: int) -> str:
    return (Path(__file__).parent / f"lab{part:02d}.py").read_text()


def run(part: int, seed: int = 0) -> Lab:
    return load(part).run(seed=seed)


def save(lab: Lab, path) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    lab.fig.savefig(path, dpi=160)
    import matplotlib.pyplot as plt

    plt.close(lab.fig)
    return path
