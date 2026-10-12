"""The epsilon-delta game board: quantifiers as moves in a two-player game.

Player epsilon (yellow) picks a horizontal band around the target value; player delta (teal) answers with a
vertical strip around the point (or, for sequences, a threshold N).  The responder wins if the graph inside the
strip stays inside the band.  The order of the moves is the whole content of a definition: a limit, continuity,
uniform continuity (delta chosen before x is revealed), uniform convergence (N before x), equicontinuity.

    board = FunctionBoard(ax, f, a=3.0, L=9.0, eps=0.1)
    self.play(FadeIn(board.eps_band()), ...)
    board.delta.animate.set_value(board.largest_delta())

Everything here is computed: ``largest_delta`` finds, by bisection on a dense grid, the largest delta for which
every sampled x in (a - delta, a + delta) has |f(x) - L| < eps, and scenes quote (and assert) that number.
"""

from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403

EPS_FILL = 0.16
DELTA_FILL = 0.14


def largest_delta(f, a: float, L: float, eps: float, delta_max: float = 1.0, samples: int = 20001,
                  domain=(-np.inf, np.inf), iters: int = 60) -> float:
    """The largest delta <= delta_max such that |f(x) - L| < eps for every sampled x with |x - a| < delta (x in the
    domain).  Bisection on delta; each test samples the open interval densely."""

    def ok(d):
        x = a + np.linspace(-d, d, samples)[1:-1]
        x = x[(x > domain[0]) & (x < domain[1])]
        if len(x) == 0:
            return True
        return bool(np.all(np.abs(f(x) - L) < eps))

    if ok(delta_max):
        return delta_max
    lo, hi = 0.0, delta_max
    for _ in range(iters):
        mid = (lo + hi) / 2
        if ok(mid):
            lo = mid
        else:
            hi = mid
    return lo


class FunctionBoard:
    """A game board on an Axes for the statement |x - a| < delta  =>  |f(x) - L| < eps.

    ``eps`` and ``delta`` are ValueTrackers; ``a`` can be a ValueTracker too (to slide the point, for uniform
    continuity).  ``L`` defaults to f(a)."""

    def __init__(self, ax: Axes, f, a, L=None, eps=0.5, delta=0.5, domain=(-np.inf, np.inf), samples=600):
        self.ax, self.f, self.domain, self.samples = ax, f, domain, samples
        self.a = a if isinstance(a, ValueTracker) else ValueTracker(a)
        self.eps = eps if isinstance(eps, ValueTracker) else ValueTracker(eps)
        self.delta = delta if isinstance(delta, ValueTracker) else ValueTracker(delta)
        self._L = L

    @property
    def L(self) -> float:
        return float(self._L) if self._L is not None else float(self.f(np.array([self.a.get_value()]))[0])

    # -- the two moves ----------------------------------------------------------
    def eps_band(self, color=C.EPS, label_tex=r"\varepsilon") -> VMobject:
        ax = self

        def draw():
            A = ax.ax
            L, e = ax.L, ax.eps.get_value()
            x0, x1 = A.x_range[0], A.x_range[1]
            lo, hi = max(L - e, A.y_range[0]), min(L + e, A.y_range[1])  # the band stays inside the axes
            p0, p1 = A.c2p(x0, lo), A.c2p(x1, hi)
            band = Rectangle(width=p1[0] - p0[0], height=max(0.004, p1[1] - p0[1]), stroke_width=0, fill_color=color,
                             fill_opacity=EPS_FILL).move_to((p0 + p1) / 2)
            edges = VGroup(*[DashedLine(A.c2p(x0, v), A.c2p(x1, v), color=color, stroke_width=2)
                             for v in (L + e, L - e) if A.y_range[0] <= v <= A.y_range[1]])
            return VGroup(band, edges)

        return always_redraw(draw)

    def delta_band(self, color=C.DELTA) -> VMobject:
        ax = self

        def draw():
            A = ax.ax
            a, d = ax.a.get_value(), ax.delta.get_value()
            y0, y1 = A.y_range[0], A.y_range[1]
            lo, hi = max(a - d, A.x_range[0]), min(a + d, A.x_range[1])  # the strip stays inside the axes
            p0, p1 = A.c2p(lo, y0), A.c2p(hi, y1)
            band = Rectangle(width=max(0.004, p1[0] - p0[0]), height=p1[1] - p0[1], stroke_width=0, fill_color=color,
                             fill_opacity=DELTA_FILL).move_to((p0 + p1) / 2)
            edges = VGroup(*[DashedLine(A.c2p(v, y0), A.c2p(v, y1), color=color, stroke_width=2)
                             for v in (a - d, a + d) if A.x_range[0] <= v <= A.x_range[1]])
            return VGroup(band, edges)

        return always_redraw(draw)

    def piece(self, good=C.CONNECTED_SET, bad=C.PATHOLOGY, stroke_width=6) -> VMobject:
        """The graph over the strip (a - delta, a + delta): green where it stays in the band, red where it escapes."""
        ax = self

        def draw():
            A = ax.ax
            a, d, e, L = ax.a.get_value(), ax.delta.get_value(), ax.eps.get_value(), ax.L
            lo, hi = max(a - d, ax.domain[0] + 1e-9), min(a + d, ax.domain[1] - 1e-9)
            lo, hi = max(lo, A.x_range[0]), min(hi, A.x_range[1])
            g = VGroup()
            if hi <= lo:
                return g
            x = np.linspace(lo, hi, ax.samples)
            y = ax.f(x)
            inside = np.abs(y - L) < e
            shown = (y >= A.y_range[0]) & (y <= A.y_range[1])  # parts beyond the axes are cut, not flattened
            key = np.where(shown, inside.astype(int), -1)
            start = 0
            for i in range(1, len(x) + 1):
                if i == len(x) or key[i] != key[start]:
                    end = i + 1 if i < len(x) and key[start] >= 0 and key[i] >= 0 else i
                    seg = x[start:end], y[start:end]
                    if key[start] >= 0 and len(seg[0]) >= 2:
                        m = VMobject(color=good if inside[start] else bad, stroke_width=stroke_width)
                        m.set_points_as_corners(np.array([A.c2p(u, v) for u, v in zip(*seg)]))
                        g.add(m)
                    start = i
            return g

        return always_redraw(draw)

    def point_marks(self, color=WHITE) -> VMobject:
        ax = self

        def draw():
            A = ax.ax
            a = ax.a.get_value()
            return VGroup(Dot(A.c2p(a, ax.L), radius=0.06, color=color),
                          DashedLine(A.c2p(a, A.y_range[0]), A.c2p(a, ax.L), color=GREY_B, stroke_width=1.5),
                          DashedLine(A.c2p(A.x_range[0], ax.L), A.c2p(a, ax.L), color=GREY_B, stroke_width=1.5))

        return always_redraw(draw)

    def largest_delta(self, delta_max=None) -> float:
        dm = delta_max if delta_max is not None else (self.ax.x_range[1] - self.ax.x_range[0])
        return largest_delta(self.f, self.a.get_value(), self.L, self.eps.get_value(), dm, domain=self.domain)


class SequenceBoard:
    """A game board for sequences: |a_n - L| < eps for every n > N.  Dots at (n, a_n); the dots past N are green
    inside the band and red outside."""

    def __init__(self, ax: Axes, seq, L: float, eps=0.2, N=1, n_max=None):
        self.ax, self.seq, self.Lv = ax, np.asarray(seq, float), L
        self.eps = eps if isinstance(eps, ValueTracker) else ValueTracker(eps)
        self.N = N if isinstance(N, ValueTracker) else ValueTracker(N)
        self.n_max = n_max or len(seq)

    def eps_band(self, color=C.EPS) -> VMobject:
        b = self

        def draw():
            A = b.ax
            e = b.eps.get_value()
            x0, x1 = A.x_range[0], A.x_range[1]
            p0, p1 = A.c2p(x0, b.Lv - e), A.c2p(x1, b.Lv + e)
            band = Rectangle(width=p1[0] - p0[0], height=max(0.004, p1[1] - p0[1]), stroke_width=0, fill_color=color,
                             fill_opacity=EPS_FILL).move_to((p0 + p1) / 2)
            edges = VGroup(DashedLine(A.c2p(x0, b.Lv + e), A.c2p(x1, b.Lv + e), color=color, stroke_width=2),
                           DashedLine(A.c2p(x0, b.Lv - e), A.c2p(x1, b.Lv - e), color=color, stroke_width=2))
            return VGroup(band, edges)

        return always_redraw(draw)

    def threshold(self, color=C.DELTA, label_tex=r"N", font_size=30) -> VMobject:
        b = self

        def draw():
            A = b.ax
            N = b.N.get_value()
            return VGroup(DashedLine(A.c2p(N + 0.5, A.y_range[0]), A.c2p(N + 0.5, A.y_range[1]), color=color,
                                     stroke_width=3),
                          MathTex(label_tex, font_size=font_size, color=color).next_to(A.c2p(N + 0.5, A.y_range[1]),
                                                                                      UP, buff=0.08))

        return always_redraw(draw)

    def dots(self, radius=0.045, base=C.SEQ, good=C.CONNECTED_SET, bad=C.PATHOLOGY) -> VMobject:
        b = self

        def draw():
            A = b.ax
            N, e = b.N.get_value(), b.eps.get_value()
            g = VGroup()
            for n in range(1, b.n_max + 1):
                v = b.seq[n - 1]
                if n <= N:
                    col = base
                else:
                    col = good if abs(v - b.Lv) < e else bad
                g.add(Dot(A.c2p(n, np.clip(v, A.y_range[0], A.y_range[1])), radius=radius, color=col))
            return g

        return always_redraw(draw)

    def smallest_N(self, eps=None) -> int:
        e = self.eps.get_value() if eps is None else eps
        bad = np.where(np.abs(self.seq - self.Lv) >= e)[0]
        return int(bad.max() + 1) if len(bad) else 0
