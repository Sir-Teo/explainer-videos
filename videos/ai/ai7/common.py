"""Helpers shared by the scenes of Part 7 ("Statistical ML")."""

from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403

from .compute import load  # noqa: F401

MONO = "DejaVu Sans Mono"
AUSTEN, DICKENS = "#E86F8A", "#58A6FF"  # as in Part 6
HIDDEN = "#B39DDB"  # hidden variables, latent states
VOWEL, CONSONANT = C.BITS, "#58A6FF"


def mix(a, b, t) -> ManimColor:
    return interpolate_color(ManimColor(a), ManimColor(b), float(np.clip(t, 0, 1)))


def ellipse_2sd(ax, mean, cov, color, stroke_width=3, k=2.0) -> VMobject:
    """The k-standard-deviation ellipse of a 2D Gaussian, drawn on ``ax``."""
    vals, vecs = np.linalg.eigh(np.asarray(cov))
    ts = np.linspace(0, 2 * np.pi, 90)
    pts = [np.asarray(mean) + vecs @ (k * np.sqrt(np.maximum(vals, 1e-9)) * np.array([np.cos(t), np.sin(t)]))
           for t in ts]
    return VMobject(color=color, stroke_width=stroke_width).set_points_smoothly([ax.c2p(*p) for p in pts])


def pca_picture(Z2, words, size=1.5) -> VGroup:
    """A jargon-card picture of a principal component, from real data: the pages on two standardized word rates (equal
    scales, so angles are true), a line through their centre, and a bar for the spread of the pages along that line.
    Parts: frame, dots, centre (invisible), line, bar outline, bar, the bar's caption, the two axis words.  Turn it with
    ``spin_pca``."""
    P = np.clip(np.asarray(Z2), -3, 3) / 3 * size / 2
    frame = Square(size + 0.2, stroke_color=GREY_D, stroke_width=1)
    dots = VGroup(*[Dot([x, y, 0], radius=0.017, color=GREY_B, fill_opacity=0.7, stroke_width=0) for x, y in P])
    centre = Dot(ORIGIN, radius=0.01).set_opacity(0)
    line = Line(LEFT * size / 2, RIGHT * size / 2, color=C.MODEL_Q, stroke_width=3.5)
    bg = Rectangle(width=0.24, height=size, stroke_color=GREY_C, stroke_width=1).next_to(frame, RIGHT, buff=0.35)
    bar = Rectangle(width=0.24, height=size / 2, stroke_width=0, fill_color=C.MODEL_Q, fill_opacity=0.85)
    bar.align_to(bg, DOWN).set_x(bg.get_x())
    cap = label(r"spread of the \\ pages along \\ the line", font_size=18, color=C.MODEL_Q).next_to(bg, RIGHT, buff=0.15)
    wx = data_text(words[0], font=MONO, font_size=16, color=GREY_A).next_to(frame, DOWN, buff=0.06)
    wy = data_text(words[1], font=MONO, font_size=16, color=GREY_A).next_to(frame, LEFT, buff=0.06)
    return VGroup(frame, dots, centre, line, bg, bar, cap, VGroup(wx, wy))


def spin_pca(pic: VGroup, cov2, theta: ValueTracker):
    """Updaters on a ``pca_picture`` (wherever and however large it now is): the line points at angle ``theta`` and the
    bar shows the variance of the pages along it, u^T C u, full height at the largest."""
    cov2 = np.asarray(cov2)
    top = float(np.linalg.eigvalsh(cov2).max())
    half, H = pic[3].get_length() / 2, pic[4].height

    def line_upd(m):
        u = np.array([np.cos(theta.get_value()), np.sin(theta.get_value()), 0.0])
        c = pic[2].get_center()
        m.put_start_and_end_on(c - half * u, c + half * u)

    def bar_upd(m):
        u = np.array([np.cos(theta.get_value()), np.sin(theta.get_value())])
        h = max(H * float(u @ cov2 @ u) / top, 0.01)
        m.stretch_to_fit_height(h).align_to(pic[4], DOWN).set_x(pic[4].get_x())

    pic[3].add_updater(line_upd)
    pic[5].add_updater(bar_upd)
    return pic
