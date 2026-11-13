"""Helpers shared by the scenes of Part 2 of *Psychology, Built* ("The Experiment")."""

from __future__ import annotations

import numpy as np

from explainer.psychology import *  # noqa: F403
from explainer.psychology import archive, ledger  # noqa: F401

from .compute import load  # noqa: F401

PART = 2

# one meaning per colour, for this part
HORSE = "#D9A066"  # Hans
KNOWS = P.ACCENT  # the questioner knows the answer
BLIND = "#8FA3BF"  # ... or does not: a blind
TREAT, CTRL = P.TREAT, P.CTRL  # the treated group and the comparison group
TRUTH = "#5BD18B"  # the true effect, where the Pool lets us know it
BIAS = P.ERR  # an estimate that is wrong for a reason
RED_CARD, BLACK_CARD = "#E8736B", "#B9C2D0"
KANT = P.KANT
COND = ("#7EC8F5", "#F2C14E", "#F28FB8", "#7BD88F")  # four conditions of a within-person design


def horse(height: float = 2.2, color=HORSE) -> VGroup:
    """Hans, in profile, facing right.  ``.leg`` is the right foreleg (the one that taps), ``.pivot`` its shoulder,
    ``.eye`` the eye."""
    body = Ellipse(width=2.3, height=1.05, stroke_width=0, fill_color=color, fill_opacity=1)
    neck = Polygon([0.4, 0.2, 0], [1.2, 1.3, 0], [1.8, 1.08, 0], [1.2, -0.2, 0], stroke_width=0,
                   fill_color=color, fill_opacity=1)
    head = Polygon([1.2, 1.3, 0], [1.75, 1.42, 0], [2.3, 0.82, 0], [2.18, 0.62, 0], [1.6, 0.95, 0], stroke_width=0,
                   fill_color=color, fill_opacity=1).round_corners(0.08)
    ear = Polygon([1.3, 1.34, 0], [1.38, 1.68, 0], [1.52, 1.4, 0], stroke_width=0, fill_color=color, fill_opacity=1)
    mane = ArcBetweenPoints(np.array([0.62, 0.35, 0]), np.array([1.3, 1.3, 0]), angle=-0.5, color="#8A5A2B",
                            stroke_width=7)
    tail = ArcBetweenPoints(np.array([-1.1, 0.2, 0]), np.array([-1.55, -0.75, 0]), angle=0.9, color="#8A5A2B",
                            stroke_width=8)
    eye = Dot([1.72, 1.17, 0], radius=0.045, color=BLACK)

    def leg(x, lean=0.0):
        return Polygon([x - 0.1, -0.3, 0], [x + 0.1, -0.3, 0], [x + 0.07 + lean, -1.45, 0], [x - 0.07 + lean, -1.45, 0],
                       stroke_width=0, fill_color=color, fill_opacity=1)

    back = VGroup(leg(-0.85, -0.05), leg(-0.6, 0.05)).set_fill(opacity=0.8)
    hind_front = leg(0.55, -0.03).set_fill(opacity=0.8)
    tap = leg(0.8, 0.03)
    hoof = Rectangle(width=0.2, height=0.12, stroke_width=0, fill_color="#3A2A1A", fill_opacity=1)
    hoof.move_to([0.85, -1.5, 0])
    tapper = VGroup(tap, hoof)
    g = VGroup(tail, back, hind_front, body, neck, mane, head, ear, eye, tapper)
    pivot = Dot([0.8, -0.3, 0], radius=0.001, fill_opacity=0)
    g.add(pivot)
    g.scale(height / g.height)
    g.leg, g.pivot, g.eye = tapper, pivot, eye
    return g.move_to(ORIGIN)


def questioner(height: float = 2.0, color=None) -> VGroup:
    """A standing figure whose head can move: ``.head`` and ``.body``."""
    color = color or P.HUMAN
    body = RoundedRectangle(width=0.5 * height * 0.62, height=height * 0.62, corner_radius=0.12 * height * 0.5,
                            stroke_width=0, fill_color=color, fill_opacity=0.9)
    head = Circle(radius=height * 0.14, stroke_width=0, fill_color=color, fill_opacity=0.9)
    head.next_to(body, UP, buff=height * 0.05)
    g = VGroup(body, head)
    g.body, g.head = body, head
    return g.move_to(ORIGIN)


def share_bars(rows, width: float = 1.3, height: float = 3.4, gap: float = 0.9, font_size=26, show_n=True) -> VGroup:
    """Vertical bars for shares between 0 and 1 with their intervals.  ``rows``: (label, share, lo, hi, n, color).
    ``.bars``, ``.values``, ``.labels``, ``.whiskers``, ``.base``."""
    g, bars, values, labels, whiskers = VGroup(), VGroup(), VGroup(), VGroup(), VGroup()
    x = 0.0
    for name, share, lo, hi, n, color in rows:
        h = max(share * height, 0.03)
        bar = Rectangle(width=width, height=h, stroke_width=0, fill_color=color, fill_opacity=0.9)
        bar.move_to([x, h / 2, 0])
        val = label(rf"{100 * share:.0f}\%", font_size=font_size + 12, color=color)
        w = VGroup()
        if lo is not None:
            w = VGroup(Line([x, lo * height, 0], [x, hi * height, 0], color=WHITE, stroke_width=3),
                       Line([x - 0.12, lo * height, 0], [x + 0.12, lo * height, 0], color=WHITE, stroke_width=3),
                       Line([x - 0.12, hi * height, 0], [x + 0.12, hi * height, 0], color=WHITE, stroke_width=3))
        val.next_to([x, max(h, (hi or share) * height), 0], UP, buff=0.14)
        text = VGroup(wrapped_label(name, width + gap - 0.15, font_size, WHITE))
        if show_n and n:
            text.add(label(rf"{n} tests", font_size=font_size - 6, color=GREY_B))
        text.arrange(DOWN, buff=0.08).next_to([x, 0, 0], DOWN, buff=0.18)
        bars.add(bar), values.add(val), labels.add(text), whiskers.add(w)
        x += width + gap
    base = Line([-width / 2 - 0.2, 0, 0], [x - gap - width / 2 + 0.2, 0, 0], color=GREY_B, stroke_width=2)
    g.add(base, bars, whiskers, values, labels)
    g.base, g.bars, g.values, g.labels, g.whiskers = base, bars, values, labels, whiskers
    return g


def effect_rail(lo: float, hi: float, length: float = 8.0, ticks=None, unit: str = "ms", font_size=22,
                zero_label: str = r"the truth: \ 0") -> VGroup:
    """A horizontal axis for effects, with the truth marked.  ``.x(v)`` gives the frame x of a value, ``.axis`` the
    line, ``.zero`` the vertical line at the truth (None if 0 is outside)."""
    axis = NumberLine(x_range=[lo, hi, (hi - lo) / 8], length=length, include_ticks=False, color=GREY_B,
                      stroke_width=2)
    g = VGroup(axis)
    for t in (ticks if ticks is not None else np.linspace(lo, hi, 5)):
        p = axis.n2p(t)
        g.add(Line(p + UP * 0.07, p + DOWN * 0.07, color=GREY_B, stroke_width=2))
        g.add(label(rf"{t:+.0f}" if t else "0", font_size=font_size, color=GREY_A).next_to(p, DOWN, buff=0.14))
    g.add(label(rf"effect reported ({unit})", font_size=font_size, color=GREY_A).next_to(axis, DOWN, buff=0.55))
    g.axis = axis
    g.x = lambda v: axis.n2p(v)[0]
    return g


def estimate_mark(rail, y: float, effect: float, lo: float, hi: float, color, radius: float = 0.09) -> VGroup:
    """A point estimate with its interval, on ``rail`` at height ``y``."""
    a, b = max(lo, rail.axis.x_range[0]), min(hi, rail.axis.x_range[1])
    bar = Line([rail.x(a), y, 0], [rail.x(b), y, 0], color=color, stroke_width=5)
    dot = Dot([rail.x(effect), y, 0], radius=radius, color=color)
    return VGroup(bar, dot)


def card(color, width: float = 0.5, height: float = 0.72) -> RoundedRectangle:
    """A playing card, face up: red or black."""
    return RoundedRectangle(width=width, height=height, corner_radius=0.07, stroke_color=WHITE, stroke_width=1.5,
                            fill_color=color, fill_opacity=0.95)


def people_row(n: int, colors, height: float = 0.5, buff: float = 0.12, per_row: int | None = None) -> VGroup:
    """``n`` little people coloured by ``colors`` (a colour, or one per person)."""
    cols = colors if isinstance(colors, (list, tuple, np.ndarray)) else [colors] * n
    g = VGroup(*[little_person(height, color=c) for c in cols])
    if per_row:
        g.arrange_in_grid(rows=int(np.ceil(n / per_row)), cols=per_row, buff=buff)
    else:
        g.arrange(RIGHT, buff=buff)
    return g


def code_block(lines, font_size=24, width: float | None = None) -> VGroup:
    """A few lines of code on a dark panel (monospace through TeX)."""
    rows = VGroup(*[label(rf"\texttt{{{ln}}}", font_size=font_size, color=WHITE) for ln in lines])
    rows.arrange(DOWN, aligned_edge=LEFT, buff=0.16)
    box = panel((width or rows.width + 0.8), rows.height + 0.6, color=P.PSYCHE)
    rows.move_to(box).align_to(box, LEFT).shift(RIGHT * 0.35)
    g = VGroup(box, rows)
    g.rows = rows
    return g
