"""The convergence dashboard and the function-as-a-point camera (instruments 2 and 3 of the series plan).

The dashboard watches one sequence of functions f_n through several lenses at once:

    point   a vertical probe at x0:          |f_n(x0) - f(x0)|
    sup     the tube around the limit:       sup |f_n - f|
    L1      the shaded area between:         int |f_n - f|
    L2      the energy:                      (int |f_n - f|^2)^(1/2)
    test    against a fixed bump phi:        int (f_n - f) phi

Each lens has a live number and a lamp; the lamps are lit (green: converges, red: does not) only when the scene
reveals the verdicts, which the caller asserts in its compute step.  The index n is a ValueTracker, so n may be
animated continuously for families defined for real n (x^n, n x (1 - x^2)^n, ...).
"""

from __future__ import annotations

import numpy as np
from manim import (DOWN, LEFT, RIGHT, UP, Axes, Circle, DashedLine, DecimalNumber, Dot, Line, MathTex, Polygon,
                   Rectangle, ValueTracker, VGroup, VMobject, always_redraw)

from explainer.style import C

LENS_TEX = {
    "point": r"|f_n(x_0) - f(x_0)|",
    "sup": r"\sup |f_n - f|",
    "L1": r"\int |f_n - f|",
    "L2": r"\big(\int |f_n - f|^2\big)^{1/2}",
    "test": r"\int (f_n - f)\,\varphi",
}
LENS_NAME = {"point": "pointwise", "sup": "uniform", "L1": "in area", "L2": "in energy", "test": "tested"}
LENS_COLOR = {"point": C.SEQ, "sup": C.EPS, "L1": C.MEASURE, "L2": C.INNER, "test": C.TEST_FN}


def runs(ax: Axes, x, y, color, stroke_width=3.0) -> VGroup:
    """The graph of y over x drawn only inside the axes' y-range (pieces that leave it are cut, not flattened)."""
    lo, hi = ax.y_range[0], ax.y_range[1]
    ok = (y >= lo) & (y <= hi)
    g, start = VGroup(), None
    for i in range(len(x) + 1):
        if i < len(x) and ok[i]:
            start = i if start is None else start
        elif start is not None:
            if i - start > 1:
                m = VMobject(color=color, stroke_width=stroke_width)
                m.set_points_as_corners(np.array([ax.c2p(a, b) for a, b in zip(x[start:i], y[start:i])]))
                g.add(m)
            start = None
    return g


def fast_graph(ax: Axes, x, y, color, stroke_width=3.0) -> VMobject:
    """A polyline through (x, y) on ax, clipped vertically to the axes (fast, single VMobject)."""
    lo, hi = ax.y_range[0], ax.y_range[1]
    yc = np.clip(y, lo, hi)
    pts = np.array([ax.c2p(a, b) for a, b in zip(x, yc)])
    m = VMobject(color=color, stroke_width=stroke_width)
    m.set_points_as_corners(pts)
    return m


class Dashboard:
    """One sequence of functions f_n on [a, b] with pointwise limit f, under several lenses."""

    def __init__(self, ax: Axes, seq, limit, n=1.0, x0=None, lenses=("point", "sup", "L1", "L2"), phi=None,
                 samples=1200, domain=None, sup_domain=None, exact=None):
        self.ax, self.seq, self.limit = ax, seq, limit
        self.n = n if isinstance(n, ValueTracker) else ValueTracker(n)
        a, b = domain or (ax.x_range[0], ax.x_range[1])
        self.x = np.linspace(a, b, samples)
        self.x0 = x0 if x0 is not None else (a + b) / 2
        self.lenses = list(lenses)
        self.phi = phi
        # the sup is taken over sup_domain (e.g. [0, 1) for x^n, where the limit's jump at 1 is excluded)
        sa, sb = sup_domain or (a, b)
        self.sup_mask = (self.x >= sa) & (self.x <= sb)
        # lens -> callable(n): an exact value to show instead of the sampled one (e.g. a supremum not attained)
        self.exact = exact or {}

    # -- values -----------------------------------------------------------------------------------------------
    def values(self, n=None):
        n = self.n.get_value() if n is None else n
        return self.seq(n, self.x)

    def lens_value(self, lens: str, n=None) -> float:
        if lens in self.exact:
            return float(self.exact[lens](self.n.get_value() if n is None else n))
        fx, gx = self.values(n), self.limit(self.x)
        d = fx - gx
        dx = np.diff(self.x)
        if lens == "point":
            return float(abs(self.seq(self.n.get_value() if n is None else n, np.array([self.x0]))[0]
                             - self.limit(np.array([self.x0]))[0]))
        if lens == "sup":
            return float(np.abs(d[self.sup_mask]).max())
        if lens == "L1":
            a = np.abs(d)
            return float(np.sum((a[1:] + a[:-1]) * dx) / 2)
        if lens == "L2":
            a = d * d
            return float(np.sqrt(np.sum((a[1:] + a[:-1]) * dx) / 2))
        if lens == "test":
            a = d * self.phi(self.x)
            return float(np.sum((a[1:] + a[:-1]) * dx) / 2)
        raise ValueError(lens)

    # -- pictures ---------------------------------------------------------------------------------------------
    def graph(self, color=C.FUNC, stroke_width=3.5) -> VMobject:
        return always_redraw(lambda: runs(self.ax, self.x, self.values(), color, stroke_width))

    def tube(self, color=C.EPS, opacity=0.18) -> VMobject:
        """The band of half-width sup |f_n - f| around the limit's graph."""
        def draw():
            r = self.lens_value("sup")
            gx = self.limit(self.x)
            lo, hi = self.ax.y_range[0], self.ax.y_range[1]
            top = np.clip(gx + r, lo, hi)
            bot = np.clip(gx - r, lo, hi)
            pts = [self.ax.c2p(a, b) for a, b in zip(self.x[::6], top[::6])]
            pts += [self.ax.c2p(a, b) for a, b in zip(self.x[::-6], bot[::-6])]
            band = Polygon(*pts, stroke_width=0, fill_color=color, fill_opacity=opacity)
            edges = VGroup(fast_graph(self.ax, self.x[::4], top[::4], color, 1.5),
                           fast_graph(self.ax, self.x[::4], bot[::4], color, 1.5))
            for e in edges:
                e.set_stroke(opacity=0.8)
            return VGroup(band, edges)

        return always_redraw(draw)

    def area(self, color=C.MEASURE, opacity=0.35) -> VMobject:
        """The region between f_n and f."""
        def draw():
            fx = np.clip(self.values(), self.ax.y_range[0], self.ax.y_range[1])
            gx = np.clip(self.limit(self.x), self.ax.y_range[0], self.ax.y_range[1])
            step = 4
            pts = [self.ax.c2p(a, b) for a, b in zip(self.x[::step], fx[::step])]
            pts += [self.ax.c2p(a, b) for a, b in zip(self.x[::-step], gx[::-step])]
            return Polygon(*pts, stroke_width=0, fill_color=color, fill_opacity=opacity)

        return always_redraw(draw)

    def probe(self, color=C.SEQ) -> VMobject:
        def draw():
            x0 = self.x0
            fv = float(self.seq(self.n.get_value(), np.array([x0]))[0])
            gv = float(self.limit(np.array([x0]))[0])
            lo, hi = self.ax.y_range[0], self.ax.y_range[1]
            line = DashedLine(self.ax.c2p(x0, lo), self.ax.c2p(x0, hi), color=color, stroke_width=1.5)
            d1 = Dot(self.ax.c2p(x0, np.clip(fv, lo, hi)), radius=0.07, color=color)
            d2 = Dot(self.ax.c2p(x0, gv), radius=0.06, color=C.LIMIT)
            return VGroup(line, d1, d2)

        return always_redraw(draw)

    def panel(self, font_size=26, width=4.6, row_h=0.62, show_names=True) -> VGroup:
        """The lens readouts: name, formula, live number and a lamp (off until verdicts are revealed)."""
        rows = VGroup()
        self.lamps, self.numbers = {}, {}
        for lens in self.lenses:
            col = LENS_COLOR[lens]
            name = MathTex(r"\text{" + LENS_NAME[lens] + "}", font_size=font_size - 4, color=col)
            tex = MathTex(LENS_TEX[lens], font_size=font_size, color=col)
            num = DecimalNumber(self.lens_value(lens), num_decimal_places=3, font_size=font_size, color=col)
            num.add_updater(lambda m, lens=lens: m.set_value(self.lens_value(lens)))
            lamp = Circle(radius=0.11, stroke_color=col, stroke_width=2).set_fill(col, 0.0)
            left = VGroup(name, tex).arrange(DOWN, aligned_edge=LEFT, buff=0.06) if show_names else VGroup(tex)
            row = VGroup(left, num, lamp)
            left.move_to([0, 0, 0], aligned_edge=LEFT)
            num.move_to([width - 1.1, 0, 0])
            lamp.move_to([width - 0.2, 0, 0])
            rows.add(row)
            self.lamps[lens], self.numbers[lens] = lamp, num
        rows.arrange(DOWN, aligned_edge=LEFT, buff=row_h - 0.4)
        for lens, row in zip(self.lenses, rows):
            row[1].set_x(rows.get_left()[0] + width - 1.1)
            row[2].set_x(rows.get_left()[0] + width - 0.2)
        return rows

    def light(self, verdicts: dict):
        """Animations that light the lamps: green if the lens converges, red if not."""
        from manim import FadeIn
        out = []
        for lens, ok in verdicts.items():
            lamp = self.lamps[lens]
            dot = Dot(lamp.get_center(), radius=0.1, color=C.CONNECTED_SET if ok else C.PATHOLOGY)
            out.append(FadeIn(dot, scale=1.6))
            lamp.verdict = dot
        return out

    def freeze(self):
        for num in self.numbers.values():
            num.clear_updaters()


class FunctionCamera:
    """The function-as-a-point camera: each function becomes one dot on a map whose coordinates are two numbers
    read off the function (sampled values or coefficients).  A sequence becomes a trail of dots."""

    def __init__(self, map_ax: Axes, coords):
        self.ax = map_ax
        self.coords = coords  # f -> (u, v)

    def dot(self, f, color=C.SEQ, radius=0.07) -> Dot:
        u, v = self.coords(f)
        return Dot(self.ax.c2p(u, v), radius=radius, color=color)

    def trail(self, fs, color=C.SEQ, radius=0.05) -> VGroup:
        dots = VGroup(*[self.dot(f, color=color, radius=radius) for f in fs])
        if len(dots) > 1:
            path = VMobject(color=color, stroke_width=1.5, stroke_opacity=0.6)
            path.set_points_as_corners([d.get_center() for d in dots])
            return VGroup(path, dots)
        return VGroup(VMobject(), dots)

    def square(self, center_f, r, color=C.EPS) -> Rectangle:
        """The shadow of the sup-norm ball of radius r around center_f, when the coordinates are two sampled values:
        a square of half-width r (every function in the ball lands inside it)."""
        u, v = self.coords(center_f)
        p0, p1 = self.ax.c2p(u - r, v - r), self.ax.c2p(u + r, v + r)
        return Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], stroke_color=color, stroke_width=2,
                         fill_color=color, fill_opacity=0.08).move_to((p0 + p1) / 2)


__all__ = ["Dashboard", "FunctionCamera", "runs", "fast_graph", "LENS_TEX", "LENS_NAME", "LENS_COLOR"]
