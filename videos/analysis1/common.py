"""Helpers shared by the scenes of Part 1 ("The Real Numbers and the Shape of Space").

The series' instruments live in ``explainer/analysis`` (chapter cards and the timeline strip, museum cards, the
ledger, the rational ruler, the dictionary card).  Here:

* :class:`Window`, a zoomable view of the real line: a center and a log-width driven by ValueTrackers, the
  rationals redrawn as a ruler at every frame (exactly enumerated, so a zoom to width 1e-10 still shows the right
  fractions), and decimal labels that adapt to the scale;
* the hero sawtooth and its Fourier partial sums;
* intervals, open/closed endpoint markers, and the Cantor set.
"""

from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from explainer.analysis import rational_dust, segments_points  # noqa: F401

from .compute import cantor_function, cantor_intervals, load, saw, saw_partial  # noqa: F401

SQRT2 = math.sqrt(2)


# ---------------------------------------------------------------------------
# A zoomable window on the real line
# ---------------------------------------------------------------------------
class Window:
    """A view of [c - W/2, c + W/2] drawn on the screen segment [x_left, x_right] at height y, where the center c
    and log10 W are ValueTrackers (so `self.c.animate.set_value(...)` pans and `self.logw.animate...` zooms)."""

    def __init__(self, center: float, width: float, x_left=-6.6, x_right=6.6, y=-0.5):
        self.c = ValueTracker(center)
        self.logw = ValueTracker(math.log10(width))
        self.L, self.R, self.y = x_left, x_right, y

    # -- geometry ------------------------------------------------------------
    @property
    def width(self) -> float:
        return 10 ** self.logw.get_value()

    def bounds(self) -> tuple[float, float]:
        c, w = self.c.get_value(), self.width
        return c - w / 2, c + w / 2

    def X(self, v: float) -> float:
        a, b = self.bounds()
        return self.L + (v - a) / (b - a) * (self.R - self.L)

    def P(self, v: float, dy: float = 0.0) -> np.ndarray:
        return np.array([self.X(v), self.y + dy, 0.0])

    def visible(self, v: float, margin: float = 0.0) -> bool:
        return self.L - margin <= self.X(v) <= self.R + margin

    def zoom_to(self, center: float, width: float):
        """Animations that pan and zoom (use inside self.play with a run_time)."""
        return [self.c.animate.set_value(center), self.logw.animate.set_value(math.log10(width))]

    # -- drawing -------------------------------------------------------------
    def axis(self, color=GREY_C) -> VMobject:
        return always_redraw(lambda: Line([self.L - 0.15, self.y, 0], [self.R + 0.15, self.y, 0], color=color,
                                          stroke_width=2))

    def dust(self, height=1.1, target=1300, split=None, color=None, color_hi=None, exponent=0.6,
             nonneg=True) -> VMobject:
        def draw():
            a, b = self.bounds()
            lo = max(a, 0.0) if nonneg else a
            if b <= lo:
                return VGroup()
            L = self.X(lo)
            return rational_dust(lo, b, L, self.R, self.y, height=height, target=target, split=split, color=color,
                                 color_hi=color_hi, exponent=exponent, qref=0.55 / math.sqrt(b - a), hmax=1.6)

        return always_redraw(draw)

    def labels(self, font_size=22, color=GREY_B, n_max=7, dy=-0.38) -> VMobject:
        """Decimal labels at round values, as many decimals as the scale needs."""

        def draw():
            a, b = self.bounds()
            w = b - a
            step = 10 ** math.floor(math.log10(w / 2))
            for mult in (1, 2, 5):
                if w / (step * mult) <= n_max:
                    step *= mult
                    break
            else:
                step *= 10
            dec = max(0, -math.floor(math.log10(step) + 1e-9))
            # widen the step until the labels (about 0.13 units per character at size 22) have room
            est = (len(f"{abs(b):.{dec}f}") + 1) * 0.13 * font_size / 22
            while (b - a) / step * (est + 0.5) > (self.R - self.L):
                for mult in (2, 2.5, 2):
                    step *= mult
                    if (b - a) / step * (est + 0.5) <= (self.R - self.L):
                        break
            k0, k1 = math.ceil(a / step), math.floor(b / step)
            g = VGroup()
            for k in range(k0, k1 + 1):
                v = k * step
                x = self.X(v)
                if x < self.L + 0.2 or x > self.R - 0.2:
                    continue
                t = Text(f"{v:.{dec}f}", font_size=font_size, color=color)
                t.move_to([x, self.y + dy, 0])
                if abs(x) + t.width / 2 > 6.95:
                    continue
                g.add(t)
            return g

        return always_redraw(draw)

    def marker(self, value_fn, color=C.SEQ, radius=0.08, dy=0.0, hollow=False) -> VMobject:
        """A dot that stays at ``value_fn()`` (a number or a callable) as the window moves."""

        def draw():
            v = value_fn() if callable(value_fn) else value_fn
            p = self.P(v, dy)
            if hollow:
                return Circle(radius=radius, color=color, stroke_width=3).move_to(p)
            return Dot(p, radius=radius, color=color)

        return always_redraw(draw)


def pin(mob: Mobject, win: "Window", value, dy: float = 0.0, margin: float = 0.4, fade=True) -> Mobject:
    """Keep ``mob`` centered at the window position of ``value`` (shifted up by dy) as the window pans and zooms;
    it fades out while its point is off-screen."""
    base = mob.get_fill_opacity() if hasattr(mob, "get_fill_opacity") else 1.0

    def upd(m):
        v = value() if callable(value) else value
        m.move_to(win.P(v, dy))
        if fade:
            x = win.X(v)
            vis = 1.0 if win.L - margin <= x <= win.R + margin else 0.0
            m.set_opacity(vis)

    mob.add_updater(upd)
    upd(mob)
    return mob


# ---------------------------------------------------------------------------
# Intervals on a line
# ---------------------------------------------------------------------------
def endpoint(p, closed: bool, color, radius=0.075) -> VMobject:
    """A filled dot (endpoint included) or a hollow ring (endpoint excluded)."""
    if closed:
        return Dot(p, radius=radius, color=color)
    return Circle(radius=radius, color=color, stroke_width=3).set_fill(BACKGROUND, 1).move_to(p)


def interval_bar(x0, x1, y, color, left_closed=True, right_closed=True, stroke_width=6, ends=True) -> VGroup:
    g = VGroup(Line([x0, y, 0], [x1, y, 0], color=color, stroke_width=stroke_width))
    if ends:
        g.add(endpoint([x0, y, 0], left_closed, color), endpoint([x1, y, 0], right_closed, color))
    return g


def cantor_mob(depth: int, x_left: float, x_right: float, y: float, height=0.22, color=WHITE) -> VMobject:
    """The depth-n stage of the Cantor set as filled bars (one VMobject per stage, cheap at any depth)."""
    iv = cantor_intervals(depth)
    L, R = x_left, x_right
    m = VGroup()
    for a, b in iv:
        xa, xb = L + a * (R - L), L + b * (R - L)
        if xb - xa < 0.003:
            xb = xa + 0.003
        m.add(Rectangle(width=xb - xa, height=height, stroke_width=0, fill_color=color, fill_opacity=1)
              .move_to([(xa + xb) / 2, y, 0]))
    return m


# ---------------------------------------------------------------------------
# The hero sawtooth
# ---------------------------------------------------------------------------
def saw_axes(x_length=12.0, y_length=4.2, y_range=(-2.2, 2.2)) -> Axes:
    ax = Axes(x_range=[-np.pi, 3 * np.pi, np.pi], y_range=[y_range[0], y_range[1], 1], x_length=x_length,
              y_length=y_length, tips=False, axis_config={"stroke_color": GREY_C, "include_ticks": True,
                                                          "tick_size": 0.06})
    return ax


def saw_graph(ax: Axes, color=C.FUNC, stroke_width=4) -> VGroup:
    """The sawtooth (pi - x)/2 on (0, 2 pi) and its periodic copies, with hollow ends and the value 0 at the jumps."""
    g = VGroup()
    for k in (-1, 0, 1):
        x0, x1 = 2 * np.pi * k, 2 * np.pi * (k + 1)
        lo, hi = max(x0, -np.pi), min(x1, 3 * np.pi)
        if hi <= lo:
            continue
        seg = Line(ax.c2p(lo, saw(np.array([lo + 1e-9]))[0]), ax.c2p(hi, saw(np.array([hi - 1e-9]))[0]),
                   color=color, stroke_width=stroke_width)
        g.add(seg)
    ends = VGroup()
    for xj in (0, 2 * np.pi):
        ends.add(endpoint(ax.c2p(xj, np.pi / 2), False, color), endpoint(ax.c2p(xj, -np.pi / 2), False, color),
                 Dot(ax.c2p(xj, 0), radius=0.07, color=color))
    g.add(ends)
    g.ends = ends
    return g


def partial_curve(ax: Axes, n: int, color=C.APPROX, stroke_width=3.5, x_range=(-np.pi, 3 * np.pi), samples=1600):
    x = np.linspace(x_range[0], x_range[1], samples)
    return polyline(ax, x, saw_partial(x, n), color=color, stroke_width=stroke_width)


def polyline(ax: Axes, xs, ys, color=WHITE, stroke_width=3, **kw) -> VMobject:
    pts = np.array([ax.c2p(float(a), float(b)) for a, b in zip(xs, ys)])
    m = VMobject(color=color, stroke_width=stroke_width, **kw)
    m.set_points_as_corners(pts)
    return m
