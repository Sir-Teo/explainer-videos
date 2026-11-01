"""The visual instruments of *Quant, Built*, in the manner of 3Blue1Brown (the language of ``explainer.ai.viz``,
which this module re-exports: one idea per frame, continuity, colour as meaning, a narrating camera, live
quantities, real numbers).

Finance-specific instruments:

* :func:`path_fan` and :func:`side_density`: many price paths, faint, with their distribution at the horizon drawn
  as a histogram standing on the right edge of the axes;
* :class:`HedgeLedger`: a hedged book's P&L split into its gamma and theta terms, as live bars and readouts that
  follow a ``ValueTracker`` (the step of the path being shown);
* :func:`binomial_tree`: a recombining tree from the House's ``trees.crr(..., keep=n)`` layers, with node values;
* :func:`price_surface`: an option's value (or any function of spot and time) as a 3D surface;
* :func:`smile_points3d`: the Surface's quotes as points over (log-moneyness, maturity, implied vol).

Colours follow ``explainer.style.QC``: spot blue, option magenta, delta yellow, gamma pink, theta light blue,
implied orange, realized teal, gains green, losses red, Q violet, P amber.
"""

from __future__ import annotations

import numpy as np

from explainer.ai.viz import *  # noqa: F401,F403
from explainer.analysis import label
from explainer.style import QC


# ---------------------------------------------------------------------------
# Paths and their distribution
# ---------------------------------------------------------------------------
def path_fan(ax, t, S, color=None, stroke_width=1.2, opacity=0.25, max_paths=200) -> VGroup:
    """Up to ``max_paths`` rows of ``S`` (paths over the times ``t``) as faint polylines on ``ax``."""
    color = color or QC.SPOT
    g = VGroup()
    for row in np.asarray(S)[:max_paths]:
        m = VMobject(stroke_width=stroke_width, stroke_color=color, stroke_opacity=opacity)
        m.set_points_as_corners([ax.c2p(x, y) for x, y in zip(t, row)])
        g.add(m)
    return g


def side_density(ax, values, y_range, bins=40, width=1.4, color=None, opacity=0.7, x=None) -> VGroup:
    """A histogram of ``values`` drawn sideways, its bars growing to the right from the vertical line at ``x``
    (default: the right end of the axes), with its tallest bar ``width`` long: the distribution at the horizon."""
    color = color or QC.SPOT
    lo, hi = y_range
    h, edges = np.histogram(np.clip(values, lo, hi), bins=bins, range=(lo, hi))
    h = h / max(h.max(), 1)
    x0 = ax.get_right()[0] + 0.12 if x is None else ax.c2p(x, lo)[0]
    g = VGroup()
    for k in range(bins):
        y0, y1 = ax.c2p(0, edges[k])[1], ax.c2p(0, edges[k + 1])[1]
        if h[k] <= 0:
            continue
        g.add(Rectangle(width=width * h[k], height=max(y1 - y0 - 0.01, 0.005), stroke_width=0, fill_color=color,
                        fill_opacity=opacity).move_to([x0 + width * h[k] / 2, (y0 + y1) / 2, 0]))
    return g


def series_line(ax, t, y, color, stroke_width=3) -> VMobject:
    m = VMobject(stroke_width=stroke_width, stroke_color=color)
    m.set_points_as_corners([ax.c2p(a, b) for a, b in zip(t, y)])
    return m


def tracing(ax, t, y, tracker: ValueTracker, color, stroke_width=3) -> VMobject:
    """A line that draws itself as far as ``tracker`` (a float index into ``t``)."""
    t, y = np.asarray(t, float), np.asarray(y, float)

    def make():
        i = tracker.get_value()
        n = int(np.clip(np.floor(i), 0, len(t) - 1))
        pts = [ax.c2p(a, b) for a, b in zip(t[:n + 1], y[:n + 1])]
        if n < len(t) - 1:
            f = i - n
            pts.append(ax.c2p(t[n] + f * (t[n + 1] - t[n]), y[n] + f * (y[n + 1] - y[n])))
        if len(pts) < 2:
            pts = pts + pts
        return VMobject(stroke_width=stroke_width, stroke_color=color).set_points_as_corners(pts)

    return always_redraw(make)


def at_index(arr, tracker: ValueTracker) -> float:
    """``arr`` linearly interpolated at the float index ``tracker``."""
    i = float(np.clip(tracker.get_value(), 0, len(arr) - 1))
    n = int(np.floor(i))
    if n >= len(arr) - 1:
        return float(arr[-1])
    return float(arr[n] + (i - n) * (arr[n + 1] - arr[n]))


# ---------------------------------------------------------------------------
# The hedging ledger
# ---------------------------------------------------------------------------
class HedgeLedger(VGroup):
    """A hedged book's running account: horizontal bars from a zero line for the gamma term (``gamma``, the gains
    from the path's squared moves), the theta term (``theta``, the decay the book pays or earns) and their sum,
    with the book's actual P&L (``book``) as a readout next to the sum, all following the float step index
    ``tracker``.  ``scale`` is the P&L that fills ``half_width`` on either side of zero."""

    def __init__(self, gamma, theta, book, tracker: ValueTracker, scale: float, half_width=2.4, bar_h=0.42,
                 font_size=24, names=(r"gamma: $\tfrac12\Gamma\,\Delta S^2$", r"theta: $\Theta\,\Delta t$",
                                      r"the book"), digits=2):
        super().__init__()
        self.tracker, self.pnl_scale, self.hw = tracker, scale, half_width
        # the redrawn bars and readouts are placed relative to this point, so the ledger can be moved as a whole
        self.anchor = VectorizedPoint(ORIGIN)
        self.add(self.anchor)
        series = [np.asarray(gamma, float), np.asarray(theta, float), np.asarray(book, float)]
        colors = [QC.GAMMA, QC.THETA, WHITE]
        self.zero = Line(UP * (1.5 * bar_h + 0.35), DOWN * (1.5 * bar_h + 0.75), color=GREY_C, stroke_width=1.5)
        self.add(self.zero)
        ys = [bar_h * 1.25, 0.0, -bar_h * 1.25 - 0.25]
        self.names = VGroup()
        self.values = VGroup()
        for k, (arr, col, y) in enumerate(zip(series, colors, ys)):
            nm = label(names[k], font_size=font_size, color=col)
            nm.move_to([-half_width - 0.25 - nm.width / 2, y, 0])
            self.names.add(nm)
            bar = always_redraw(self._bar(arr, col, y, bar_h, filled=(k < 2)))
            self.add(bar)
            d = DecimalNumber(0, num_decimal_places=digits, include_sign=True, font_size=font_size + 2, color=col)
            d.add_updater(self._readout(arr, y))
            self.values.add(d)
        if len(series[2]):
            self.rule = DashedLine([-half_width, ys[2] + bar_h * 0.85, 0], [half_width, ys[2] + bar_h * 0.85, 0],
                                   color=GREY_D, stroke_width=1, dash_length=0.06)
            self.add(self.rule)
        self.add(self.names, self.values)

    def _bar(self, arr, col, y, bar_h, filled=True):
        def make():
            v = at_index(arr, self.tracker)
            w = float(np.clip(v / self.pnl_scale, -1.05, 1.05)) * self.hw
            r = Rectangle(width=max(abs(w), 0.004), height=bar_h, stroke_width=0 if filled else 2.5, stroke_color=col,
                          fill_color=(QC.GAIN if v >= 0 else QC.LOSS) if not filled else col,
                          fill_opacity=0.85 if filled else 0.55)
            return r.move_to(self.anchor.get_center() + np.array([w / 2, y, 0]))
        return make

    def _readout(self, arr, y):
        def upd(d):
            d.set_value(at_index(arr, self.tracker))
            d.move_to(self.anchor.get_center() + np.array([self.hw * 1.05 + 0.3, y, 0]), aligned_edge=LEFT)
        return upd


# ---------------------------------------------------------------------------
# Trees
# ---------------------------------------------------------------------------
def binomial_tree(layers: dict, dx=2.0, dy=0.62, node_r=0.3, font_size=20, color=None, show=("values",),
                  value_color=None, digits=2) -> VGroup:
    """A recombining tree from ``trees.crr(..., keep=n)["layers"]`` (keys 0..n-1, each with ``spots`` and
    ``values``): node j of layer n sits at x = n dx, y = (2j - n) dy.  ``g.nodes[n][j]`` is a node (circle and its
    label), ``g.edges`` the lines; ``show`` picks the label: "values", "spots" or "delta"."""
    color = color or GREY_B
    value_color = value_color or QC.OPTION
    g = VGroup()
    nodes, edges = {}, VGroup()
    layer_keys = sorted(int(k) for k in layers)
    for n in layer_keys:
        L = layers[n] if n in layers else layers[str(n)]
        nodes[n] = VGroup()
        for j in range(n + 1):
            p = np.array([n * dx, (2 * j - n) * dy, 0.0])
            c = Circle(radius=node_r, stroke_color=color, stroke_width=2, fill_color=BACKGROUND, fill_opacity=1)
            c.move_to(p)
            key = show[0]
            val = L[key][j] if L.get(key) is not None and j < len(L[key]) else None
            t = MathTex(f"{val:.{digits}f}" if val is not None else "", font_size=font_size,
                        color=value_color if key == "values" else (QC.SPOT if key == "spots" else QC.DELTA))
            t.move_to(p)
            nodes[n].add(VGroup(c, t))
    for n in layer_keys[:-1]:
        for j in range(n + 1):
            a = nodes[n][j][0]
            for jj in (j, j + 1):
                b = nodes[n + 1][jj][0]
                edges.add(Line(a.get_center(), b.get_center(), buff=node_r, color=GREY_D, stroke_width=2))
    g.add(edges, *[nodes[n] for n in layer_keys])
    g.nodes, g.edges = nodes, edges
    return g


# ---------------------------------------------------------------------------
# Surfaces in 3D
# ---------------------------------------------------------------------------
PRICE_COLORS = ("#1B2A6B", "#3B3F9B", "#8B4FB8", "#D45FB0", "#F7A8D8")


def price_surface(ax3: ThreeDAxes, f, x_range, y_range, resolution=(36, 30), z_lo=None, z_hi=None,
                  colors=PRICE_COLORS, opacity=0.9) -> Surface:
    """``z = f(x, y)`` over a rectangle (spot x, time y), coloured by height in the option's magenta scale."""
    return loss_surface(ax3, f, x_range, y_range, resolution=resolution, z_lo=z_lo, z_hi=z_hi, colors=colors,
                        opacity=opacity)


def smile_points3d(ax3: ThreeDAxes, k, T, iv, color=None, radius=0.035) -> VGroup:
    """The Surface's quotes as small spheres at (log-moneyness, maturity, implied vol)."""
    color = color or QC.IMPLIED
    # low-resolution spheres: hundreds of full-resolution ones make a Cairo render crawl
    return VGroup(*[Dot3D(ax3.c2p(a, b, c), radius=radius, color=color, resolution=(4, 4)) for a, b, c in zip(k, T, iv)])


# ---------------------------------------------------------------------------
# Small readouts
# ---------------------------------------------------------------------------
def readout(tex_left: str, tracker_fn, digits=2, font_size=30, color=WHITE, unit: str = "") -> VGroup:
    """``tex_left`` followed by a live number (``tracker_fn()``), e.g. readout(r"\\Delta =", lambda: d.get_value())."""
    left = MathTex(tex_left, font_size=font_size, color=color)
    num_ = DecimalNumber(tracker_fn(), num_decimal_places=digits, font_size=font_size, color=color)
    g = VGroup(left, num_).arrange(RIGHT, buff=0.15)
    if unit:
        u = MathTex(unit, font_size=font_size, color=color)
        g.add(u)
        u.next_to(num_, RIGHT, buff=0.08)

    def upd(m):
        m.set_value(tracker_fn())
        m.next_to(left, RIGHT, buff=0.15)

    num_.add_updater(upd)
    g.num = num_
    return g
