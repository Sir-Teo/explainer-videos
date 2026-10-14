"""Helpers shared by the scenes of Part 5 ("Measure: The Lebesgue Integral").

Part 5 draws sets on a line as bands of intervals, functions sliced into horizontal layers, and the three ways mass
can escape a sequence of functions.
"""

from __future__ import annotations

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis1.common import polyline  # noqa: F401
from videos.analysis2.common import plain_axes  # noqa: F401
from videos.analysis4.common import heatmap, square_axes  # noqa: F401

from .compute import load  # noqa: F401


def interval_band(ax: Axes, intervals, y, color, height=0.12, opacity=0.85, min_width=0.012) -> VGroup:
    """Intervals [a, b] (data coordinates on ax's x-axis) drawn as bars at scene height y."""
    g = VGroup()
    for a, b in intervals:
        pa, pb = ax.c2p(a, 0)[0], ax.c2p(b, 0)[0]
        g.add(Rectangle(width=max(pb - pa, min_width), height=height, stroke_width=0, fill_color=color,
                        fill_opacity=opacity).move_to([(pa + pb) / 2, y, 0]))
    return g


def area_under(ax: Axes, x, y, color, opacity=0.4) -> Polygon:
    pts = [ax.c2p(x[0], 0)] + [ax.c2p(a, b) for a, b in zip(x, y)] + [ax.c2p(x[-1], 0)]
    return Polygon(*pts, stroke_width=0, fill_color=color, fill_opacity=opacity)


def step_graph(ax: Axes, edges, heights, color, stroke_width=3) -> VGroup:
    """A step function: horizontal segments of the given heights over [edges[i], edges[i+1]]."""
    return VGroup(*[Line(ax.c2p(a, h), ax.c2p(b, h), color=color, stroke_width=stroke_width)
                    for a, b, h in zip(edges[:-1], edges[1:], heights)])


# ---------------------------------------------------------------------------
# Helpers added in the polish pass (used only by Part 5's scenes)
# ---------------------------------------------------------------------------
def level_runs(x, mask) -> list:
    """The maximal runs of consecutive samples where ``mask`` holds, as intervals (x[first], x[last])."""
    out, st = [], None
    for i in range(len(x) + 1):
        o = i < len(x) and mask[i]
        if o and st is None:
            st = i
        elif not o and st is not None:
            out.append((float(x[st]), float(x[i - 1])))
            st = None
    return out


def layer_cake(ax: Axes, x, f, dt, t0=0.0, n=None, mask=None, opacity=0.55, floor=0.0) -> VGroup:
    """Lebesgue's horizontal layers under the graph of f >= 0, the series' one convention for the picture.

    Layer k spans the heights [t0 + k dt, t0 + (k + 1) dt] (cut below at ``floor``) over the level set of its
    *midpoint*, {f > t0 + (k + 1/2) dt}, so the cake hugs the graph and its area is a midpoint sum for the integral
    (an upper sum from t = 0 would lay a full-width slab under every dip of f).  Colors run SEQ -> MEASURE, black
    hairline separators.  The result carries ``runs`` (each layer's intervals), ``lo``, ``hi``, ``mids``, ``widths``
    (the measure of each level set), ``cols`` and ``area`` (the sum of height times width)."""
    x, f = np.asarray(x, float), np.asarray(f, float)
    sel = np.ones_like(f, bool) if mask is None else np.asarray(mask, bool)
    if n is None:
        n = int(np.ceil((f[sel].max() - t0) / dt))
    g = VGroup()
    g.runs, g.lo, g.hi, g.mids, g.widths, g.cols = [], [], [], [], [], []
    for k in range(n):
        lo, hi, mid = max(floor, t0 + k * dt), t0 + (k + 1) * dt, t0 + (k + 0.5) * dt
        col = interpolate_color(ManimColor(C.SEQ), ManimColor(C.MEASURE), k / max(1, n - 1))
        rr = level_runs(x, (f > mid) & sel)
        g.add(VGroup(*[Rectangle(width=ax.c2p(b, 0)[0] - ax.c2p(a, 0)[0], height=ax.c2p(0, hi)[1] - ax.c2p(0, lo)[1],
                                 stroke_width=0.5, stroke_color=BLACK, fill_color=col, fill_opacity=opacity)
                       .move_to(ax.c2p((a + b) / 2, (lo + hi) / 2)) for a, b in rr]))
        g.runs.append(rr)
        g.lo.append(lo)
        g.hi.append(hi)
        g.mids.append(mid)
        g.widths.append(sum(b - a for a, b in rr))
        g.cols.append(col)
    g.area = float(sum((h - l_) * w for l_, h, w in zip(g.lo, g.hi, g.widths)))
    return g


def rationals_upto(qmax: int, a: float = 0.0, b: float = 1.0) -> list:
    """All p/q in [a, b] in lowest terms with q <= qmax, as sorted (p, q) pairs."""
    import math as _m
    out = sorted({(p // _m.gcd(p, q), q // _m.gcd(p, q)) for q in range(1, qmax + 1)
                  for p in range(int(np.ceil(a * q)), int(np.floor(b * q)) + 1)}, key=lambda t: t[0] / t[1])
    return out


def dirichlet_graph(ax: Axes, qmax=40, color=None, r0=0.06, a=0.0, b=1.0) -> VGroup:
    """The graph of Dirichlet's function on [a, b], the series' one convention: a dot at height 1 over every p/q with
    q <= qmax, its radius and opacity shrinking with q (so the dots never fuse into a solid line at 1, which would
    read as "D = 1 everywhere"), and its zero part as a thin line at opacity 0.6.  Returns VGroup(zero, dots)."""
    color = color or C.PATHOLOGY
    fr = rationals_upto(qmax, a, b)
    dots = VGroup(*[Dot(ax.c2p(p / q, 1), radius=r0 * q ** -0.75, color=color,
                        fill_opacity=max(0.45, 1.0 - 0.012 * q)) for p, q in fr])
    zero = Line(ax.c2p(a, 0), ax.c2p(b, 0), color=color, stroke_width=2.5, stroke_opacity=0.6)
    g = VGroup(zero, dots)
    g.zero, g.dots, g.fracs = zero, dots, fr
    return g


def cut_graph(ax: Axes, x, y, color, stroke_width=3.0, top=None, bottom=None) -> VGroup:
    """The graph of y over x drawn only inside [bottom, top] (default: the axes' y-range).  Each piece ends exactly on
    the boundary line (the crossing is interpolated), so a curve that leaves the window is cut, never flattened into a
    false plateau.  Pair it with :func:`escape_arrow` where it leaves."""
    top = ax.y_range[1] if top is None else top
    bottom = ax.y_range[0] if bottom is None else bottom
    x, y = np.asarray(x, float), np.asarray(y, float)
    ins = (y >= bottom) & (y <= top)
    pieces, cur = [], []

    def cross(i, j):  # the point where the segment i -> j meets the boundary it crosses
        lim = top if max(y[i], y[j]) > top else bottom
        s = (lim - y[i]) / (y[j] - y[i])
        return x[i] + s * (x[j] - x[i]), lim

    for i in range(len(x)):
        if ins[i]:
            if not cur and i > 0 and not ins[i - 1]:
                cur.append(cross(i - 1, i))
            cur.append((x[i], y[i]))
        elif cur:
            cur.append(cross(i - 1, i))
            pieces.append(cur)
            cur = []
    if cur:
        pieces.append(cur)
    g = VGroup()
    for p in pieces:
        if len(p) > 1:
            m = VMobject(color=color, stroke_width=stroke_width)
            m.set_points_as_corners([ax.c2p(a, b) for a, b in p])
            g.add(m)
    return g


def escape_arrow(ax: Axes, x0, color, top=None, length=0.42, stroke_width=3.0) -> Arrow:
    """A small up-arrow at x0 rising from the top of the axes: the graph goes on up, out of the window."""
    top = ax.y_range[1] if top is None else top
    p = ax.c2p(x0, top)
    return Arrow(p + DOWN * 0.08, p + UP * length, buff=0, color=color, stroke_width=stroke_width, tip_length=0.15,
                 max_stroke_width_to_length_ratio=20, max_tip_length_to_length_ratio=0.45)
