"""Helpers shared by the scenes of Part 6 (Financial Econometrics)."""

from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403

from .compute import load  # noqa: F401

PART = 6

DATA_C = QC.SPOT       # data
EST = QC.IDEA          # estimates
GOOD = QC.GAIN         # correct inference
BAD = QC.LOSS          # misleading inference
ALT = QC.OPTION        # alternatives


def real_data(text: str, corner=DR):
    return note(text, font_size=18, color=GREY_B).to_corner(corner, buff=0.25)


def tbar(ax, x, t, color, width=0.5, lo=0.0):
    """A bar from ``lo`` to ``t`` at position ``x`` on axes ``ax``."""
    top, bot = ax.c2p(x, max(t, lo)), ax.c2p(x, min(t, lo))
    w = ax.c2p(width, 0)[0] - ax.c2p(0, 0)[0]
    return Rectangle(width=w, height=max(abs(top[1] - bot[1]), 0.01), stroke_width=0, fill_color=color,
                     fill_opacity=0.85).move_to((top + bot) / 2)


def show_card(scene, card):
    scene.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))


def hist_bars(ax, values, edges, color, opacity=0.8, density=True, cap=None):
    """Histogram bars standing on the x axis of ``ax``."""
    h, _ = np.histogram(np.clip(values, edges[0], edges[-1]), edges, density=density)
    if cap is not None:
        h = np.minimum(h, cap)
    w = ax.c2p(edges[1] - edges[0], 0)[0] - ax.c2p(0, 0)[0]
    return VGroup(*[Rectangle(width=max(w - 0.01, 0.005), height=max(ax.c2p(0, v)[1] - ax.c2p(0, 0)[1], 0.001),
                              stroke_width=0, fill_color=color, fill_opacity=opacity).move_to(
        ax.c2p((edges[i] + edges[i + 1]) / 2, 0), aligned_edge=DOWN) for i, v in enumerate(h)])


def ellipse_curve(ax, center, V, color, k2=5.991, stroke_width=3, clip=None):
    """The ``k2`` (chi-square) contour of a 2x2 covariance ``V`` around ``center`` on 2D axes."""
    w, U = np.linalg.eigh(np.asarray(V, float))
    th = np.linspace(0, 2 * np.pi, 120)
    pts = (U @ (np.sqrt(k2) * np.sqrt(np.maximum(w, 0))[:, None] * np.vstack([np.cos(th), np.sin(th)]))).T
    pts += np.asarray(center, float)
    if clip is not None:
        (x0, x1), (y0, y1) = clip
        pts = np.column_stack([np.clip(pts[:, 0], x0, x1), np.clip(pts[:, 1], y0, y1)])
    return VMobject(stroke_color=color, stroke_width=stroke_width).set_points_smoothly([ax.c2p(a, b) for a, b in pts])


def predict(question: str, width=11.6):
    """The pause-and-predict prompt."""
    tag = label(r"Pause and predict", font_size=22, color=QC.IDEA)
    q = wrapped_label(question, width, 26, WHITE)
    g = VGroup(tag, q).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
    box = SurroundingRectangle(g, buff=0.25, corner_radius=0.12, color=QC.IDEA, stroke_width=1.5)
    return VGroup(box, g)


def fmt_t(t: float, d=2) -> str:
    """A number with no negative zero."""
    s = f"{t:.{d}f}"
    return s[1:] if s.startswith("-") and float(s) == 0 else s
