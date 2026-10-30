"""Helpers shared by the scenes of Part 7 ("Statistical ML")."""

from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403

from .compute import load  # noqa: F401

PART = 7
MONO = "DejaVu Sans Mono"
AUSTEN, DICKENS = "#E86F8A", "#58A6FF"  # as in Part 6
HIDDEN = "#B39DDB"  # hidden variables, latent states
SEEN = C.TRUE_P  # observed variables
VOWEL, CONSONANT = C.BITS, "#58A6FF"
MODEL = C.MODEL_Q  # a fitted model, an approximation q
BOUND = C.INTERVAL  # lower bounds: Jensen's, the ELBO
LIKE = C.BITS  # the log-likelihood
VOICE1, VOICE2 = "#FF9F45", "#5BD17A"  # the cocktail party's two sources
CAUSE = "#FF6B8B"  # interventions, do(x)
GPC = HIDDEN  # the unknown function of a Gaussian process
TOPIC_COLORS = ["#FF9F45", "#58A6FF", "#5BD17A", "#E86F8A", "#F7D154", "#B39DDB", "#4FD1C5", "#F6AD55",
                "#9BE37B", "#D4A5FF", "#FC8181", "#90CDF4"]


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
    """Updaters on a ``pca_picture``: the line points at angle ``theta`` and the bar shows the variance along it."""
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


# ---------------------------------------------------------------------------
# Small instruments
# ---------------------------------------------------------------------------
def card_in(scene, k, title, question, voice, lit=()):
    """The chapter card under its one-line voiceover."""
    card = chapter_card(k, title, question, lit=lit, part=PART)
    with scene.voiceover(voice):
        scene.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
    scene.play(FadeOut(card))


def node(tex, pos, hidden=True, r=0.36, font_size=30, color=None) -> VGroup:
    """A graphical model's circle: empty and lilac if hidden, shaded blue if observed."""
    col = color or (HIDDEN if hidden else SEEN)
    c = Circle(radius=r, color=col, stroke_width=3, fill_color=BACKGROUND if hidden else col,
               fill_opacity=1 if hidden else 0.35).move_to(pos)
    return VGroup(c, MathTex(tex, font_size=font_size).move_to(pos))


def edge(a, b, color=GREY_B, stroke_width=3) -> Arrow:
    d = b[0].get_center() - a[0].get_center()
    d = d / np.linalg.norm(d)
    return Arrow(a[0].get_center() + d * a[0].width / 2, b[0].get_center() - d * b[0].width / 2, buff=0.04,
                 color=color, stroke_width=stroke_width, max_tip_length_to_length_ratio=0.25)


def heat_grid(M, cell=0.4, lo=0.0, hi=1.0, color=C.BITS, dark="#121826", stroke=GREY_D) -> VGroup:
    """A matrix as coloured squares (row 0 at the top), values mapped from [lo, hi] to dark ... color."""
    M = np.asarray(M, float)
    g = VGroup()
    for i in range(M.shape[0]):
        for j in range(M.shape[1]):
            t = float(np.clip((M[i, j] - lo) / max(hi - lo, 1e-12), 0, 1))
            g.add(Square(cell, stroke_width=1, stroke_color=stroke, fill_color=mix(dark, color, t ** 0.8),
                         fill_opacity=1).move_to([j * cell, -i * cell, 0]))
    return g.move_to(ORIGIN)


def recolor_grid(grid: VGroup, M, lo=0.0, hi=1.0, color=C.BITS, dark="#121826") -> list:
    """Animations that recolour a ``heat_grid`` to new values."""
    M = np.asarray(M, float)
    out = []
    k = 0
    for i in range(M.shape[0]):
        for j in range(M.shape[1]):
            t = float(np.clip((M[i, j] - lo) / max(hi - lo, 1e-12), 0, 1))
            out.append(grid[k].animate.set_fill(mix(dark, color, t ** 0.8), opacity=1))
            k += 1
    return out


def bars(values, width=0.3, gap=0.08, height=2.0, vmax=None, colors=None, base=ORIGIN) -> VGroup:
    """Plain bars from a common baseline (left to right)."""
    v = np.asarray(values, float)
    vmax = vmax or float(v.max())
    g = VGroup()
    for i, x in enumerate(v):
        h = max(height * x / vmax, 0.01)
        col = colors[i] if colors is not None else C.BITS
        g.add(Rectangle(width=width, height=h, stroke_width=0, fill_color=col, fill_opacity=0.9)
              .move_to(np.asarray(base) + RIGHT * i * (width + gap) + UP * h / 2))
    return g


def era_strip(events, y0=1900, y1=2026, width=12.6, y=0.0, font_size=19) -> VGroup:
    """A timeline from y0 to y1 with (year, text, row) events; row +1 above the line, -1 below.  Returns the line
    group and a list of (dot, label) pairs to reveal one by one."""
    x0 = -width / 2

    def X(yr):
        return x0 + width * (yr - y0) / (y1 - y0)

    base = VGroup(Line([X(y0), y, 0], [X(y1), y, 0], color=GREY_C, stroke_width=2))
    for yr in range(1900, y1 + 1, 25):
        base.add(Text(str(yr), font_size=14, color=GREY_C).next_to([X(yr), y, 0], DOWN, buff=0.1))
    items = []
    for yr, text, row in events:
        d = Dot([X(yr), y, 0], radius=0.06, color=C.HUMAN)
        t = label(rf"{yr}\\ {text}", font_size=font_size, color=WHITE)
        stem = Line([X(yr), y, 0], [X(yr), y + np.sign(row) * (0.45 + 1.0 * (abs(row) - 1)), 0], color=GREY_D, stroke_width=1.5)
        t.next_to(stem.get_end(), UP if row > 0 else DOWN, buff=0.06)
        items.append(VGroup(d, stem, t))
    return base, items
