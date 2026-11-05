"""The statistics instruments of *Statistics, Built* (videos/stats/SYLLABUS.md, §1, "New instruments").

Built on *AI, Built*'s plotting helpers (``axes``, ``curve``, ``legend``) and drawn in the series' colours
(``explainer.stats.style.S``):

* :func:`hist_bars` / :func:`histogram`: histogram rectangles on an ``Axes`` (counts or density);
* :func:`dot_plot`: a stacked dot plot, one dot per observation;
* :func:`ecdf_steps`: the empirical CDF as a staircase;
* :func:`box_plot`: Tukey's box plot (box, median, whiskers, outliers) along an axis;
* :class:`NSpace`: vectors, lines and planes in R^3 drawn by projection with a turning view, for the geometry of a
  sample of three (the mean as a projection onto 1, residuals, Pythagoras, correlation as a cosine);
* :class:`SamplingMachine`: the World's population as a field of dots, samples drawn out of it, and each sample's
  statistic dropped into a growing histogram, so a sampling distribution builds itself;
* :func:`die_face`, :func:`dice_row`, :func:`prob_tree` and :func:`icon_array`: dice with pips, probability trees
  drawn left to right (paths lit in order), and one-square-per-person arrays for natural frequencies (Part 2).
"""

from __future__ import annotations

import numpy as np
from manim import *  # noqa: F403

from explainer.stats.style import S


# ---------------------------------------------------------------------------
# Histograms, dot plots, ECDFs, box plots
# ---------------------------------------------------------------------------
def hist_bars(ax, edges, heights, color=None, opacity=0.75, stroke_width=1.2, stroke_color=None) -> VGroup:
    """Rectangles on ``ax`` for bins ``edges`` (k + 1 values) with ``heights`` (k values, in the axes' y units)."""
    color = color or S.EST
    g = VGroup()
    for a, b, h in zip(edges[:-1], edges[1:], heights):
        p0, p1 = ax.c2p(a, 0), ax.c2p(b, max(h, 0.0))
        w, ht = max(p1[0] - p0[0], 1e-4), max(p1[1] - p0[1], 1e-4)
        r = Rectangle(width=w, height=ht, stroke_width=stroke_width, stroke_color=stroke_color or BACKGROUND_DARK,
                      fill_color=color, fill_opacity=opacity)
        r.move_to([p0[0] + w / 2, p0[1] + ht / 2, 0])
        g.add(r)
    return g


BACKGROUND_DARK = "#0E1117"


def histogram(ax, values, edges, density=False, color=None, opacity=0.75, stroke_width=1.2) -> VGroup:
    """Histogram of ``values`` with bin ``edges``: counts, or densities (area = proportion) if ``density``."""
    counts, edges = np.histogram(np.asarray(values, float), bins=np.asarray(edges, float))
    h = counts / (counts.sum() * np.diff(edges)) if density else counts.astype(float)
    g = hist_bars(ax, edges, h, color=color, opacity=opacity, stroke_width=stroke_width)
    g.counts, g.edges, g.heights = counts, edges, h
    return g


def bounds(ax):
    """``(x_lo, x_hi, y_lo, y_hi)`` of ``ax`` in data coordinates.  ``CornerAxes`` stores its ranges shifted to start
    at 0 (its ``c2p`` takes the original coordinates), so ``ax.x_range`` alone is not the data range."""
    ox, oy = getattr(ax, "_off", (0.0, 0.0))
    return ax.x_range[0] + ox, ax.x_range[1] + ox, ax.y_range[0] + oy, ax.y_range[1] + oy


def dot_plot(ax, values, step: float, radius=0.06, color=None, gap=1.0) -> VGroup:
    """One dot per value, values rounded to ``step``; dots at the same rounded value stack upward (``gap`` dot
    diameters apart, in screen units)."""
    color = color or S.DATA
    v = np.round(np.asarray(values, float) / step) * step
    seen: dict = {}
    g = VGroup()
    for x in v:
        k = seen.get(x, 0)
        seen[x] = k + 1
        p = ax.c2p(x, bounds(ax)[2])
        g.add(Dot([p[0], p[1] + radius * (1 + 2 * gap * k) + 0.02, 0], radius=radius, color=color))
    return g


def ecdf_steps(ax, values, color=None, stroke_width=3, x_lo=None, x_hi=None) -> VMobject:
    """The empirical CDF: a staircase rising 1/n at each sorted observation."""
    color = color or S.EST
    x = np.sort(np.asarray(values, float))
    n = len(x)
    lo = bounds(ax)[0] if x_lo is None else x_lo
    hi = bounds(ax)[1] if x_hi is None else x_hi
    pts = [ax.c2p(lo, 0)]
    for i, xi in enumerate(x):
        pts += [ax.c2p(xi, i / n), ax.c2p(xi, (i + 1) / n)]
    pts.append(ax.c2p(hi, 1.0))
    m = VMobject(color=color, stroke_width=stroke_width)
    m.set_points_as_corners(pts)
    return m


def five_numbers(values) -> dict:
    """Tukey's summary with the 1.5 IQR fences: quartiles by linear interpolation (numpy's default), whiskers at
    the most extreme observations inside the fences, and the outliers beyond them."""
    x = np.sort(np.asarray(values, float))
    q1, med, q3 = np.quantile(x, [0.25, 0.5, 0.75])
    iqr = q3 - q1
    lo_f, hi_f = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    inside = x[(x >= lo_f) & (x <= hi_f)]
    return {"min": float(x[0]), "q1": float(q1), "median": float(med), "q3": float(q3), "max": float(x[-1]),
            "iqr": float(iqr), "lo_whisker": float(inside.min()), "hi_whisker": float(inside.max()),
            "outliers": [float(v) for v in x[(x < lo_f) | (x > hi_f)]], "fences": (float(lo_f), float(hi_f))}


def box_plot(ax, summary: dict, y: float = 0.0, height: float = 0.5, color=None, outlier_color=None,
             stroke_width=2.5) -> VGroup:
    """Tukey's box plot along the x axis of ``ax`` at screen height ``y`` (axis units on x): box from Q1 to Q3,
    median line, whiskers to the most extreme points within the fences, outliers as dots."""
    color = color or S.EST
    outlier_color = outlier_color or S.RESID
    X = lambda v: ax.c2p(v, bounds(ax)[2])[0]  # noqa: E731
    box = Rectangle(width=X(summary["q3"]) - X(summary["q1"]), height=height, stroke_color=color,
                    stroke_width=stroke_width, fill_color=color, fill_opacity=0.2)
    box.move_to([(X(summary["q1"]) + X(summary["q3"])) / 2, y, 0])
    med = Line([X(summary["median"]), y - height / 2, 0], [X(summary["median"]), y + height / 2, 0], color=WHITE,
               stroke_width=stroke_width + 1)
    wl = Line([X(summary["lo_whisker"]), y, 0], [X(summary["q1"]), y, 0], color=color, stroke_width=stroke_width)
    wh = Line([X(summary["q3"]), y, 0], [X(summary["hi_whisker"]), y, 0], color=color, stroke_width=stroke_width)
    cl = Line([X(summary["lo_whisker"]), y - height / 4, 0], [X(summary["lo_whisker"]), y + height / 4, 0],
              color=color, stroke_width=stroke_width)
    ch = Line([X(summary["hi_whisker"]), y - height / 4, 0], [X(summary["hi_whisker"]), y + height / 4, 0],
              color=color, stroke_width=stroke_width)
    outs = VGroup(*[Dot([X(v), y, 0], radius=0.05, color=outlier_color) for v in summary["outliers"]
                    if bounds(ax)[0] <= v <= bounds(ax)[1]])
    g = VGroup(box, med, wl, wh, cl, ch, outs)
    g.box, g.median, g.whiskers, g.outliers = box, med, VGroup(wl, wh, cl, ch), outs
    return g


# ---------------------------------------------------------------------------
# NSpace: the geometry of a sample of three
# ---------------------------------------------------------------------------
class NSpace(VGroup):
    """R^3 drawn by projection, turning about the vertical axis (``ns.angle``, a ValueTracker) and tilted
    (``ns.tilt``).  Objects added with :meth:`vector`, :meth:`segment`, :meth:`line`, :meth:`plane` and
    :meth:`point_label` keep their 3D coordinates and are redrawn every frame, so turning the view (``ns.turn``)
    shows the geometry from all sides.  Coordinates are data units; ``scale`` maps one unit to screen units.

    The axes are the three observations' axes ("observation 1, 2, 3"): a sample (x1, x2, x3) is one point."""

    def __init__(self, scale=1.0, center=ORIGIN, angle=-0.55, tilt=0.35, axis_len=3.2, axis_labels=None,
                 axis_color=GREY_D, depth_fade=True):
        super().__init__()
        self.scale_, self.center_ = scale, np.asarray(center, float)
        self.angle, self.tilt = ValueTracker(angle), ValueTracker(tilt)
        self.depth_fade = depth_fade
        self.axes3 = VGroup()
        labels = axis_labels if axis_labels is not None else [r"$x_1$", r"$x_2$", r"$x_3$"]
        from explainer.analysis import label

        for k in range(3):
            e = np.zeros(3)
            e[k] = axis_len
            ax_line = self.segment(-0.15 * e, e, color=axis_color, stroke_width=1.6, register=False)
            lab = label(labels[k], font_size=24, color=GREY_B)
            lab.add_updater(self._follow(1.08 * e))
            self.axes3.add(ax_line, lab)
        self.add(self.axes3)

    # -- projection --------------------------------------------------------
    def project(self, p) -> np.ndarray:
        # data (x1, x2, x3): x1 to the right, x3 up, x2 into the screen (before turning)
        x, y, z = np.asarray(p, float)
        X, Y, Z = x, z, y
        a, t = self.angle.get_value(), self.tilt.get_value()
        X, Z = X * np.cos(a) + Z * np.sin(a), -X * np.sin(a) + Z * np.cos(a)
        Y, Z = Y * np.cos(t) - Z * np.sin(t), Y * np.sin(t) + Z * np.cos(t)
        return self.center_ + self.scale_ * np.array([X, Y, 0.0])

    def _follow(self, p):
        def upd(m):
            m.move_to(self.project(p))
        return upd

    def turn(self, by: float, run_time=4.0, rate_func=smooth):
        return self.angle.animate(run_time=run_time, rate_func=rate_func).increment_value(by)

    @staticmethod
    def _faded(make, alpha):
        def wrapped():
            m = make()
            a = alpha.get_value()
            if a < 0.999:
                m.set_stroke(opacity=m.get_stroke_opacity() * a)
                m.set_fill(opacity=m.get_fill_opacity() * a)
            return m
        return wrapped

    def _redraw(self, make):
        """An always-redrawn object with its own opacity tracker ``.alpha`` (FadeIn cannot animate a mobject whose
        family is rebuilt every frame; :meth:`reveal` can)."""
        alpha = ValueTracker(1.0)
        m = always_redraw(self._faded(make, alpha))
        m.alpha = alpha
        return m

    @staticmethod
    def reveal(*objs, run_time=1.0):
        """Fade redrawn objects in: their trackers go from 0 to 1 (add the objects to the scene first)."""
        for o in objs:
            o.alpha.set_value(0.0)
        return AnimationGroup(*[o.alpha.animate(run_time=run_time).set_value(1.0) for o in objs])

    # -- objects -----------------------------------------------------------
    def segment(self, a, b, color=WHITE, stroke_width=3, dashed=False, register=True) -> VMobject:
        a, b = np.asarray(a, float), np.asarray(b, float)

        def make():
            if dashed:
                return DashedLine(self.project(a), self.project(b), color=color, stroke_width=stroke_width,
                                  dash_length=0.08)
            return Line(self.project(a), self.project(b), color=color, stroke_width=stroke_width)

        return self._redraw(make)

    def vector(self, v, color=WHITE, stroke_width=5, origin=(0, 0, 0)) -> VMobject:
        o, v = np.asarray(origin, float), np.asarray(v, float)

        def make():
            p0, p1 = self.project(o), self.project(o + v)
            if np.linalg.norm(p1 - p0) < 1e-3:
                return Dot(p0, radius=0.04, color=color)
            return Arrow(p0, p1, buff=0, color=color, stroke_width=stroke_width, tip_length=0.2,
                         max_tip_length_to_length_ratio=0.25, max_stroke_width_to_length_ratio=12)

        return self._redraw(make)

    def dot(self, p, color=WHITE, radius=0.07) -> Dot:
        d = Dot(radius=radius, color=color)
        d.add_updater(self._follow(np.asarray(p, float)))
        d.update()
        return d

    def line(self, direction, extent=3.4, color=GREY_B, stroke_width=2, dashed=True) -> VMobject:
        u = np.asarray(direction, float)
        u = u / np.linalg.norm(u)
        return self.segment(-0.25 * extent * u, extent * u, color=color, stroke_width=stroke_width, dashed=dashed)

    def plane(self, u, w, extent=2.6, color=GREY_B, opacity=0.14, origin=(0, 0, 0)) -> VMobject:
        u, w, o = (np.asarray(v, float) for v in (u, w, origin))
        corners = [o + s * extent * u + t * extent * w for s, t in ((-1, -1), (1, -1), (1, 1), (-1, 1))]

        def make():
            return Polygon(*[self.project(c) for c in corners], stroke_width=1, stroke_color=color,
                           stroke_opacity=0.4, fill_color=color, fill_opacity=opacity)

        return self._redraw(make)

    def right_angle(self, corner, u, w, size=0.22, color=GREY_A) -> VMobject:
        c, u, w = (np.asarray(v, float) for v in (corner, u, w))
        u, w = u / np.linalg.norm(u), w / np.linalg.norm(w)

        def make():
            pts = [c + size * u, c + size * (u + w), c + size * w]
            m = VMobject(color=color, stroke_width=2)
            m.set_points_as_corners([self.project(p) for p in pts])
            return m

        return self._redraw(make)

    def polyline(self, pts, color=WHITE, stroke_width=2, opacity=1.0, fill=None, fill_opacity=0.0) -> VMobject:
        """A path through 3D points (a curve on a surface, or a filled slice if ``fill`` is given)."""
        pts = [np.asarray(q, float) for q in pts]

        def make():
            m = VMobject(stroke_color=color, stroke_width=stroke_width, stroke_opacity=opacity)
            m.set_points_as_corners([self.project(q) for q in pts])
            if fill is not None:
                m.set_fill(fill, opacity=fill_opacity)
            return m

        return self._redraw(make)

    def cloud(self, pts, color=WHITE, radius=0.02, opacity=0.8) -> VGroup:
        """Many points at once: one updater projects all of them each frame (cheaper than one ``dot`` each)."""
        P = np.asarray(pts, float)
        g = VGroup(*[Dot(radius=radius, color=color, fill_opacity=opacity) for _ in range(len(P))])

        def upd(m):
            a, t = self.angle.get_value(), self.tilt.get_value()
            X, Y, Z = P[:, 0], P[:, 2], P[:, 1]
            X, Z = X * np.cos(a) + Z * np.sin(a), -X * np.sin(a) + Z * np.cos(a)
            Y = Y * np.cos(t) - Z * np.sin(t)
            xy = self.center_[:2] + self.scale_ * np.c_[X, Y]
            for d_, (u, v) in zip(m, xy):
                d_.move_to([u, v, 0])
        upd(g)
        g.add_updater(upd)
        return g

    def point_label(self, mob: Mobject, p, offset=(0.25, 0.2)) -> Mobject:
        p = np.asarray(p, float)
        off = np.array([offset[0], offset[1], 0])
        mob.add_updater(lambda m: m.move_to(self.project(p) + off))
        mob.update()
        return mob


# ---------------------------------------------------------------------------
# The sampling machine
# ---------------------------------------------------------------------------
class SamplingMachine(VGroup):
    """The World as a field of ``n_dots`` dots (each standing for a resident) in a panel on the left; samples are
    drawn out of it onto a number line (their values), and each sample's statistic drops into a histogram on the
    right.  ``values`` are the population values the dots stand for (only their positions in the field are
    decorative: the value a sampled dot carries is its own).

    Usage (in a scene)::

        m = SamplingMachine(values, value_range=(140, 200), stat_range=(165, 175), bins=24)
        self.play(FadeIn(m))
        m.draw(self, idx, stat)          # one sample, slowly: dots fly out, the statistic falls into the histogram
        m.add_stats(self, stats)         # many statistics at once (the histogram fills)
    """

    def __init__(self, values, value_range, stat_range, bins=24, n_dots=900, seed=0, field_center=(-4.6, 0.3, 0),
                 field_size=(3.6, 4.4), line_center=(1.4, 2.3, 0), line_width=5.4, hist_center=(1.4, -1.4, 0),
                 hist_size=(5.4, 2.6), value_label=r"value", stat_label=r"statistic", dot_color=None,
                 stat_color=None, max_count=None, ticks=None, stat_ticks=None, fmt=lambda v: f"{v:g}"):
        super().__init__()
        from explainer.analysis import label
        from explainer.ai.viz import axes

        g = np.random.Generator(np.random.PCG64(seed))
        self.values = np.asarray(values, float)
        self.dot_color = dot_color or S.POP
        self.stat_color = stat_color or S.EST
        k = min(n_dots, len(self.values))
        self.idx = g.choice(len(self.values), size=k, replace=False)  # which residents the dots stand for
        w, h = field_size
        pos = np.column_stack([g.uniform(-w / 2, w / 2, k), g.uniform(-h / 2, h / 2, k), np.zeros(k)])
        self.field_pos = pos + np.asarray(field_center, float)
        self.frame = RoundedRectangle(width=w + 0.4, height=h + 0.4, corner_radius=0.15, stroke_color=S.WORLD,
                                      stroke_width=1.5).move_to(field_center)
        self.field_title = label(r"the population", font_size=22, color=S.WORLD).next_to(self.frame, UP, buff=0.12)
        self.dots = VGroup(*[Dot(p, radius=0.03, color=self.dot_color, fill_opacity=0.8) for p in self.field_pos])
        self.line = axes(list(value_range), [0, 1], x_length=line_width, y_length=0.4, xlabel=value_label,
                         xticks=ticks, xfmt=fmt, center=line_center, font_size=18)
        self.line[0].y_axis.set_opacity(0)
        self.hist_ax = axes(list(stat_range), [0, 1], x_length=hist_size[0], y_length=hist_size[1],
                            xlabel=stat_label, xticks=stat_ticks, xfmt=fmt, center=hist_center, font_size=18)
        self.hist_ax[0].y_axis.set_opacity(0.4)
        self.edges = np.linspace(stat_range[0], stat_range[1], bins + 1)
        self.counts = np.zeros(bins)
        self.max_count = max_count
        self.bars = VGroup()
        self.add(self.frame, self.field_title, self.dots, self.line, self.hist_ax, self.bars)

    def _ensure_scale(self):
        top = self.max_count or max(4.0, self.counts.max() * 1.15)
        self.hist_ax[0].y_range = [0, top, 1]
        return top

    def _bars_mob(self):
        top = self.max_count or max(4.0, self.counts.max() * 1.15)
        ax = self.hist_ax[0]
        h = self.counts / top
        g = VGroup()
        for a, b, hh in zip(self.edges[:-1], self.edges[1:], h):
            if hh <= 0:
                continue
            p0, p1 = ax.c2p(a, 0), ax.c2p(b, hh)
            r = Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], stroke_width=1, stroke_color=BACKGROUND_DARK,
                          fill_color=self.stat_color, fill_opacity=0.8)
            r.move_to([(p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2, 0])
            g.add(r)
        return g

    def draw(self, scene, sample_values, stat, run_time=2.4, keep=False, stat_tex=None):
        """Animate one sample: ``len(sample_values)`` dots leave the field and land on the number line at their
        values; the statistic appears as a blue tick and falls into the histogram."""
        from explainer.analysis import label

        ax = self.line[0]
        m = len(sample_values)
        g = np.random.Generator(np.random.PCG64(int(1e6 * abs(stat)) % 2**31))
        src = self.field_pos[g.choice(len(self.field_pos), size=m, replace=False)]
        movers = VGroup(*[Dot(p, radius=0.045, color=S.DATA) for p in src])
        ends = [ax.c2p(v, 0) + UP * 0.12 for v in sample_values]
        scene.play(LaggedStart(*[d.animate.move_to(e) for d, e in zip(movers, ends)], lag_ratio=0.6 / max(m, 1)),
                   run_time=run_time * 0.55)
        tick = Line(ax.c2p(stat, 0) + DOWN * 0.15, ax.c2p(stat, 0) + UP * 0.45, color=self.stat_color,
                    stroke_width=5)
        tl = label(stat_tex, font_size=22, color=self.stat_color).next_to(tick, UP, buff=0.06) if stat_tex else None
        scene.play(Create(tick), *([FadeIn(tl)] if tl else []), run_time=run_time * 0.15)
        target = self.hist_ax[0].c2p(stat, 0)
        drop = Dot(tick.get_center(), radius=0.06, color=self.stat_color)
        self.counts[np.clip(np.searchsorted(self.edges, stat) - 1, 0, len(self.counts) - 1)] += 1
        new_bars = self._bars_mob()
        scene.play(ReplacementTransform(tick, drop), *([FadeOut(tl)] if tl else []), run_time=run_time * 0.1)
        scene.play(drop.animate.move_to(target), run_time=run_time * 0.12)
        scene.play(FadeOut(drop), Transform(self.bars, new_bars), *([] if keep else [FadeOut(movers)]),
                   run_time=run_time * 0.08)
        return movers if keep else None

    def add_stats(self, scene, stats, run_time=2.0, steps=6):
        """Many statistics at once: the histogram fills in ``steps`` stages."""
        stats = np.asarray(stats, float)
        chunks = np.array_split(stats, steps)
        for c in chunks:
            for s_ in c:
                self.counts[np.clip(np.searchsorted(self.edges, s_) - 1, 0, len(self.counts) - 1)] += 1
            scene.play(Transform(self.bars, self._bars_mob()), run_time=run_time / steps)


# ---------------------------------------------------------------------------
# Chance: dice, trees, icon arrays (Part 2 onward)
# ---------------------------------------------------------------------------
_PIPS = {1: [(0, 0)], 2: [(-1, 1), (1, -1)], 3: [(-1, 1), (0, 0), (1, -1)],
         4: [(-1, 1), (1, 1), (-1, -1), (1, -1)], 5: [(-1, 1), (1, 1), (0, 0), (-1, -1), (1, -1)],
         6: [(-1, 1), (1, 1), (-1, 0), (1, 0), (-1, -1), (1, -1)]}


def die_face(value: int, size=0.6, color="#EDEDED", pip_color="#14161C", stroke_color=None) -> VGroup:
    """A die showing ``value`` (1-6) as pips; other values (Sicherman's 8, say) as a numeral."""
    sq = RoundedRectangle(width=size, height=size, corner_radius=size * 0.16, fill_color=color, fill_opacity=1,
                          stroke_color=stroke_color or color, stroke_width=1.5)
    g = VGroup(sq)
    if value in _PIPS:
        r, off = size * 0.085, size * 0.27
        for dx, dy in _PIPS[value]:
            g.add(Dot(sq.get_center() + np.array([dx * off, dy * off, 0]), radius=r, color=pip_color))
    else:
        g.add(MathTex(str(value), font_size=size * 60, color=pip_color).move_to(sq))
    g.value = value
    return g


def dice_row(values, size=0.5, buff=0.08, **kw) -> VGroup:
    return VGroup(*[die_face(v, size=size, **kw) for v in values]).arrange(RIGHT, buff=buff)


def prob_tree(levels, x0=-5.5, dx=3.2, height=5.4, font_size=24, edge_color=GREY_B, label_buff=0.12):
    """A probability tree drawn left to right.  ``levels`` is a nested list: each node is
    (label_tex, prob_tex, color, children); the root is a single node with prob_tex ignored.  Returns a VGroup with
    ``.nodes`` (dict path -> mobject), ``.edges`` (path -> line), ``.probs`` (path -> label) and ``.leaves`` (paths
    of leaves, top to bottom), so scenes can light paths in order."""
    root_label, _, root_color, kids = levels
    g = VGroup()
    nodes, edges, probs = {}, {}, {}

    def n_leaves(node):
        return 1 if not node[3] else sum(n_leaves(c) for c in node[3])

    total = n_leaves(levels)
    step = height / max(total, 1)

    def place(node, path, depth, top):
        lab, pr, col, ch = node
        k = n_leaves(node)
        y = top - step * k / 2
        m = MathTex(lab, font_size=font_size, color=col) if lab else Dot(radius=0.06, color=col)
        m.move_to([x0 + depth * dx, y, 0])
        nodes[path] = m
        g.add(m)
        t = top
        for i, c in enumerate(ch):
            cp = path + (i,)
            child = place(c, cp, depth + 1, t)
            t -= step * n_leaves(c)
            e = Line(m.get_right() + RIGHT * 0.08, child.get_left() + LEFT * 0.08, color=edge_color,
                     stroke_width=2)
            edges[cp] = e
            pl = MathTex(c[1], font_size=font_size - 4, color=GREY_A)
            pl.move_to(e.point_from_proportion(0.5)).shift(UP * (0.22 if child.get_y() >= m.get_y() else -0.22))
            probs[cp] = pl
            g.add(e, pl)
        return m

    place(levels, (), 0, height / 2)
    g.nodes, g.edges, g.probs = nodes, edges, probs
    g.leaves = sorted([p for p in nodes if p not in [q[:-1] for q in nodes if q]], key=lambda p: -nodes[p].get_y())
    return g


def icon_array(colors, cols=50, size=0.1, buff=0.035, shape="square") -> VGroup:
    """One small square (or dot) per person, row by row: natural frequencies at a glance."""
    g = VGroup()
    for c in colors:
        if shape == "dot":
            g.add(Dot(radius=size / 2, color=c))
        else:
            g.add(Square(side_length=size, stroke_width=0, fill_color=c, fill_opacity=1))
    rows = int(np.ceil(len(colors) / cols))
    g.arrange_in_grid(rows, cols, buff=buff)
    return g


# ---------------------------------------------------------------------------
# The family tree of distributions (Part 3 onward; after Leemis & McQueston 2008)
# ---------------------------------------------------------------------------
FAMILY_NODES = {
    "bernoulli": (r"Bernoulli", (-6.0, 2.7), "d"), "binomial": (r"binomial", (-3.4, 2.7), "d"),
    "hyper": (r"hypergeometric", (-6.0, 3.65), "d"), "betabin": (r"beta-binomial", (5.6, -3.45), "d"),
    "poisson": (r"Poisson", (-3.4, 0.8), "d"), "geometric": (r"geometric", (-6.0, 0.8), "d"),
    "negbin": (r"negative binomial", (-5.6, -1.1), "d"), "normal": (r"normal", (0.4, 0.8), "c"),
    "uniform": (r"uniform", (0.4, -1.1), "c"), "exponential": (r"exponential", (-2.9, -1.1), "c"),
    "gamma": (r"gamma", (-1.4, -2.7), "c"), "beta": (r"beta", (3.0, -2.7), "c"),
    "lognormal": (r"log-normal", (2.8, 2.7), "c"), "chisq": (r"$\chi^2$", (3.0, 0.8), "c"),
    "t": (r"$t$", (5.7, 2.0), "c"), "f": (r"$F$", (5.7, 0.2), "c"), "cauchy": (r"Cauchy", (5.6, -1.5), "c"),
    "pareto": (r"Pareto", (-4.4, -3.3), "c"),
}
FAMILY_EDGES = {  # key: (from, to, label, arc angle)
    "sum_bern": ("bernoulli", "binomial", r"sum of $n$", 0.0),
    "hyper_bin": ("hyper", "binomial", r"$N \to \infty$", 0.0),
    "rare": ("binomial", "poisson", r"$n \to \infty,\ np = \lambda$", 0.0),
    "first": ("bernoulli", "geometric", r"wait for the first", 0.0),
    "sum_geo": ("geometric", "negbin", r"sum of $r$", 0.0),
    "gaps": ("poisson", "exponential", r"gaps", 0.0),
    "sum_exp": ("exponential", "gamma", r"sum of $k$", 0.0),
    "geo_exp": ("geometric", "exponential", r"continuous limit", 0.0),
    "gp": ("gamma", "negbin", r"Poisson, gamma rate", -0.35),
    "demoivre": ("binomial", "normal", r"de Moivre", 0.0),
    "pois_norm": ("poisson", "normal", r"$\lambda \to \infty$", 0.0),
    "exp_log": ("normal", "lognormal", r"$e^X$", 0.0),
    "squares": ("normal", "chisq", r"sum of squares", 0.0),
    "gamma_chi": ("gamma", "chisq", r"special case", 0.55),
    "student": ("chisq", "t", r"$Z/\sqrt{V/\nu}$", 0.0),
    "ratio": ("chisq", "f", r"ratio", 0.0),
    "t1": ("t", "cauchy", r"$\nu = 1$", -0.7),
    "tinf": ("t", "normal", r"$\nu \to \infty$", 0.35),
    "neglog": ("uniform", "exponential", r"$-\log U$", 0.0),
    "order": ("uniform", "beta", r"order statistics", 0.0),
    "gamma_beta": ("gamma", "beta", r"$X/(X+Y)$", 0.0),
    "pareto": ("exponential", "pareto", r"$e^X$", 0.0),
    "mix_p": ("beta", "betabin", r"mix $p$", 0.0),
    "box_muller": ("uniform", "normal", r"Box--Muller", 0.0),
}


def _paint(arr, color=None, opacity=1.0):
    """Colour an arrow's line (stroke only, so curved arrows stay unfilled) and its tip."""
    arr.set_fill(opacity=0)
    if color is not None:
        arr.set_stroke(color=color)
    arr.set_stroke(opacity=opacity)
    tip = getattr(arr, "tip", None)
    if tip is not None:
        tip.set_fill(color if color is not None else tip.get_fill_color(), opacity=opacity)
        tip.set_stroke(color if color is not None else tip.get_stroke_color(), opacity=opacity)
    return arr


class FamilyTree(VGroup):
    """The family of distributions as a graph: discrete laws (blue) on the left, continuous (green) on the right; each
    arrow a derivation.  Everything starts dim; ``light_nodes`` and ``light_edges`` return the animations that switch
    nodes and arrows on, so each chapter adds the arrows it has derived."""

    D_COL, C_COL, DIM = "#7EC8F5", "#7BD88F", "#3A4658"

    def __init__(self, font_size=22, scale=1.0):
        from explainer.analysis import label

        super().__init__()
        self.nodes, self.edges = {}, {}
        for key, (name, (x, y), kind) in FAMILY_NODES.items():
            t = label(name, font_size=font_size, color=WHITE)
            box = RoundedRectangle(width=t.width + 0.36, height=t.height + 0.26, corner_radius=0.12,
                                   stroke_color=self.D_COL if kind == "d" else self.C_COL, stroke_width=2,
                                   fill_color="#0E141D", fill_opacity=1)
            g = VGroup(box, t.move_to(box))
            g.move_to([x * scale, y * scale, 0])
            g.kind = kind
            self.nodes[key] = g
        for key, (a, b, lab, angle) in FAMILY_EDGES.items():
            A, B = self.nodes[a], self.nodes[b]
            p, q = A.get_center(), B.get_center()
            d = (q - p) / max(np.linalg.norm(q - p), 1e-9)
            start = self._exit(A, d)
            end = self._exit(B, -d)
            if abs(angle) > 1e-6:
                arr = CurvedArrow(start, end, angle=angle, color=GREY_B, stroke_width=2.2, tip_length=0.16)
            else:
                arr = Arrow(start, end, buff=0.02, color=GREY_B, stroke_width=2.2, tip_length=0.16,
                            max_tip_length_to_length_ratio=0.2)
            mid = arr.point_from_proportion(0.5)
            nrm = np.array([-d[1], d[0], 0])
            bulge = mid - (start + end) / 2
            if np.linalg.norm(bulge) > 0.05:  # a curved arrow: put the label outside its bulge
                nrm = bulge / np.linalg.norm(bulge)
            tl = label(lab, font_size=font_size - 6, color=GREY_A)
            tl.move_to(mid + nrm * (0.12 + 0.5 * abs(nrm[0]) * tl.width / 2 + 0.5 * abs(nrm[1]) * tl.height))
            self.edges[key] = VGroup(arr, tl)
        for e in self.edges.values():
            self.add(e)
        for n in self.nodes.values():
            self.add(n)
        self.dim_all()

    @staticmethod
    def _exit(box, d):
        """Where a ray from the box centre in direction d leaves the box."""
        w, h = box.width / 2, box.height / 2
        tx = w / abs(d[0]) if abs(d[0]) > 1e-9 else np.inf
        ty = h / abs(d[1]) if abs(d[1]) > 1e-9 else np.inf
        return box.get_center() + d * (min(tx, ty) + 0.04)

    def dim_all(self):
        for n in self.nodes.values():
            n[0].set_stroke(opacity=0.35)
            n[1].set_opacity(0.35)
        for e in self.edges.values():
            _paint(e[0], self.DIM, 0.5)
            e[1].set_opacity(0.0)
        return self

    def lit_state(self, nodes=(), edges=()):
        """Set (without animating) these nodes and edges to their lit look."""
        for k in nodes:
            self.nodes[k][0].set_stroke(opacity=1)
            self.nodes[k][1].set_opacity(1)
        for k in edges:
            _paint(self.edges[k][0], S.ACCENT, 1.0)
            self.edges[k][1].set_opacity(1)
        return self

    def light_nodes(self, *keys):
        return [a for k in keys for a in (self.nodes[k][0].animate.set_stroke(opacity=1),
                                          self.nodes[k][1].animate.set_opacity(1))]

    def light_edges(self, *keys, color=None):
        color = color or S.ACCENT
        anims = []
        for k in keys:
            a, b = FAMILY_EDGES[k][:2]
            anims += self.light_nodes(a, b)
            target = _paint(self.edges[k][0].copy(), color, 1.0)
            anims += [Transform(self.edges[k][0], target), self.edges[k][1].animate.set_opacity(1)]
        return anims


# ---------------------------------------------------------------------------
# The Gaussian slicer (Part 5): a bivariate normal density as a wireframe, sliced and renormalized
# ---------------------------------------------------------------------------
class GaussianSlicer:
    """A bivariate normal density drawn as a wireframe surface in an ``NSpace`` (x across, y into the screen,
    density up), with a vertical slice at x = x0: the slice's curve f(x0, y), and the renormalized conditional density
    f(y | x0) = f(x0, y) / f_X(x0).  Coordinates are standardized internally so the picture fits; ``lines`` sets the
    wireframe density."""

    def __init__(self, mean, cov, xr, yr, scale=0.9, center=(-2.6, -1.6, 0), angle=-0.75, tilt=0.42, lines=17,
                 height=3.2, axis_labels=None):
        self.mu, self.S = np.asarray(mean, float), np.asarray(cov, float)
        self.xr, self.yr = xr, yr
        self.Si = np.linalg.inv(self.S)
        self.norm = 1 / (2 * np.pi * np.sqrt(np.linalg.det(self.S)))
        self.h = height / self.norm  # density scale: peak at ``height``
        self.ns = NSpace(scale=scale, center=center, angle=angle, tilt=tilt, axis_len=0.0001,
                         axis_labels=axis_labels or ["", "", ""])
        self.ns.axes3.set_opacity(0)
        self.sx = 6.0 / (xr[1] - xr[0])
        self.sy = 6.0 / (yr[1] - yr[0])
        g = VGroup()
        for xv in np.linspace(*xr, lines):
            g.add(self.ns.polyline([self.p3(xv, yv) for yv in np.linspace(*yr, 60)], color=GREY_B, stroke_width=1.2,
                                   opacity=0.55))
        for yv in np.linspace(*yr, lines):
            g.add(self.ns.polyline([self.p3(xv, yv) for xv in np.linspace(*xr, 60)], color=GREY_B, stroke_width=1.2,
                                   opacity=0.55))
        self.wire = g
        self.floor = self.ns.polyline([self.p3(xr[0], yr[0], 0), self.p3(xr[1], yr[0], 0), self.p3(xr[1], yr[1], 0),
                                       self.p3(xr[0], yr[1], 0), self.p3(xr[0], yr[0], 0)], color=GREY_D, stroke_width=1.5)

    def f(self, x, y):
        d = np.array([x, y]) - self.mu
        return self.norm * np.exp(-0.5 * d @ self.Si @ d)

    def p3(self, x, y, z=None):
        z = self.f(x, y) * self.h if z is None else z
        return np.array([(x - (self.xr[0] + self.xr[1]) / 2) * self.sx, (y - (self.yr[0] + self.yr[1]) / 2) * self.sy, z])

    def slice(self, x0, color=None, renorm=False, fill_opacity=0.35):
        """The curve y -> f(x0, y) on the surface; with ``renorm``, rescaled to the conditional density f(y | x0),
        drawn so every conditional density has the same peak (1.5 x the joint peak): the slices of a Gaussian differ
        only in where they sit."""
        color = color or S.ACCENT
        ys = np.linspace(*self.yr, 80)
        vals = np.array([self.f(x0, yv) for yv in ys])
        k = 1.5 * self.norm / vals.max() if renorm else 1.0
        pts = [self.p3(x0, ys[0], 0)] + [self.p3(x0, yv, v * k * self.h) for yv, v in zip(ys, vals)] + \
              [self.p3(x0, ys[-1], 0)]
        return self.ns.polyline(pts, color=color, stroke_width=3.5, fill=color, fill_opacity=fill_opacity)

    def marginal_x(self, x0):
        s = np.sqrt(self.S[0, 0])
        return np.exp(-0.5 * ((x0 - self.mu[0]) / s) ** 2) / (s * np.sqrt(2 * np.pi))

    def cond(self, x0):
        m = self.mu[1] + self.S[0, 1] / self.S[0, 0] * (x0 - self.mu[0])
        v = self.S[1, 1] - self.S[0, 1] ** 2 / self.S[0, 0]
        return m, np.sqrt(v)

    def objects(self):
        return [self.floor, *self.wire]

    def stop(self, *extra):
        for m in [*self.objects(), *extra]:
            m.clear_updaters()


class GaltonBoard:
    """Galton's quincunx (1873; *Natural Inheritance*, 1889): balls fall through ``rows`` rows of pegs, bouncing left
    or right at each, and pile up in ``rows + 1`` bins.  The bin a ball reaches is the number of rightward bounces,
    so the pile is a binomial histogram, and with many rows it takes the shape of the normal curve.

    ``board.mobjects()`` gives the pegs, the funnel and the bins; ``board.drops(scene, bits)`` animates balls whose
    bounces are the rows of ``bits`` (0 = left, 1 = right), stacking each where it lands; ``board.bars(counts)``
    draws the pile as bars, for when there are too many balls to animate one by one."""

    def __init__(self, rows: int = 12, center=ORIGIN, dx: float = 0.42, dy: float = 0.3, bin_height: float = 2.6,
                 peg_color=GREY_B, ball_color=None, ball_radius: float = 0.055):
        self.rows, self.dx, self.dy, self.bin_height = rows, dx, dy, bin_height
        self.ball_color = ball_color or S.EST
        self.r = ball_radius
        c = np.asarray(center, float)
        height = rows * dy + bin_height
        self.top = c + UP * (height / 2 - 0.2)
        self.pegs = VGroup(*[Dot(self.peg(i, j), radius=0.035, color=peg_color) for i in range(rows) for j in range(i + 1)])
        self.floor = self.top[1] - rows * dy - bin_height
        self.bin_top = self.top[1] - rows * dy + 0.05
        xs = [self.bin_x(k) - dx / 2 for k in range(rows + 2)]
        self.walls = VGroup(*[Line([x, self.floor, 0], [x, self.bin_top, 0], color=GREY_D, stroke_width=1.5) for x in xs])
        self.base = Line([xs[0], self.floor, 0], [xs[-1], self.floor, 0], color=GREY_C, stroke_width=2)
        f = self.top + UP * 0.45
        self.funnel = VGroup(Line(f + LEFT * 0.5 + UP * 0.3, f + LEFT * 0.12, color=GREY_C, stroke_width=2),
                             Line(f + RIGHT * 0.5 + UP * 0.3, f + RIGHT * 0.12, color=GREY_C, stroke_width=2))
        self.heights = [0] * (rows + 1)

    def peg(self, i: int, j: int) -> np.ndarray:
        return self.top + RIGHT * (j - i / 2) * self.dx + DOWN * i * self.dy

    def bin_x(self, k: int) -> float:
        return float(self.top[0] + (k - self.rows / 2) * self.dx)

    def mobjects(self) -> VGroup:
        return VGroup(self.funnel, self.pegs, self.walls, self.base)

    def path(self, bits) -> VMobject:
        """The zig-zag a ball follows: over each peg it meets, then down into its bin, onto the current pile."""
        pts = [self.top + UP * 0.45]
        j = 0
        for i, b in enumerate(bits):
            pts.append(self.peg(i, j) + UP * (self.r + 0.04))
            j += int(b)
        k = j
        h = self.heights[k]
        self.heights[k] += 1
        pts.append(np.array([self.bin_x(k), self.bin_top, 0]))
        pts.append(np.array([self.bin_x(k), self.floor + self.r * (2 * h + 1), 0]))
        m = VMobject()
        m.set_points_as_corners(pts)
        return m

    def drops(self, scene, bits, run_time: float = 1.6, lag: float = 0.25) -> VGroup:
        """Animate one ball per row of ``bits``, released ``lag`` seconds apart; returns the balls, left in place."""
        balls, anims = VGroup(), []
        for b in bits:
            p = self.path(b)
            ball = Dot(p.get_start(), radius=self.r, color=self.ball_color)
            balls.add(ball)
            anims.append(MoveAlongPath(ball, p, rate_func=linear, run_time=run_time))
        if anims:
            scene.play(LaggedStart(*anims, lag_ratio=lag / run_time))
        return balls

    def bars(self, counts, scale: float | None = None, color=None, opacity: float = 0.75) -> VGroup:
        """The pile as bars (one per bin); ``scale`` is screen height per ball (default: tallest bar fills the bin)."""
        counts = np.asarray(counts, float)
        scale = scale or (self.bin_height * 0.92 / max(1.0, counts.max()))
        g = VGroup()
        for k, c in enumerate(counts):
            h = max(1e-3, c * scale)
            g.add(Rectangle(width=self.dx * 0.82, height=h, stroke_width=0, fill_color=color or self.ball_color,
                            fill_opacity=opacity).move_to([self.bin_x(k), self.floor + h / 2, 0]))
        g.scale_per_ball = scale
        return g

    def curve(self, values, scale: float, color=None, stroke_width: float = 3) -> VMobject:
        """A smooth curve over the bins: ``values`` is a function of the bin index k (float), in balls."""
        ks = np.linspace(-0.5, self.rows + 0.5, 200)
        pts = [np.array([self.top[0] + (k - self.rows / 2) * self.dx, self.floor + values(k) * scale, 0]) for k in ks]
        return VMobject(stroke_color=color or S.TRUTH, stroke_width=stroke_width).set_points_smoothly(pts)


class TankFactory(VGroup):
    """The German tank problem as a picture (Part 9): ``N`` tanks with serial numbers 1..N in a grid, of which the
    ``captured`` serials are lit and labelled.  ``hidden`` dims the tanks we cannot see (all but the captured ones);
    ``reveal(scene)`` brightens the whole factory, the answer the estimators were guessing."""

    def __init__(self, N: int, captured, cols: int = 30, cell: float = 0.2, center=ORIGIN, color=None, lit=None,
                 show_numbers: bool = True, font_size: int = 18):
        super().__init__()
        from explainer.analysis import label

        self.N, self.cols, self.cell = N, cols, cell
        self.color = color or GREY_D
        self.lit_color = lit or S.ACCENT
        rows = int(np.ceil(N / cols))
        self.tanks = VGroup()
        for k in range(N):
            r, c = divmod(k, cols)
            body = RoundedRectangle(width=cell * 0.86, height=cell * 0.56, corner_radius=cell * 0.12, stroke_width=0,
                                    fill_color=self.color, fill_opacity=0.35)
            body.move_to([(c - (cols - 1) / 2) * cell, ((rows - 1) / 2 - r) * cell, 0])
            self.tanks.add(body)
        self.tanks.move_to(center)
        self.captured = list(captured)
        self.marks, self.numbers = VGroup(), VGroup()
        for s_ in self.captured:
            t = self.tanks[s_ - 1]
            self.marks.add(t.copy().set_fill(self.lit_color, opacity=1.0))
            if show_numbers:
                self.numbers.add(label(str(s_), font_size=font_size, color=self.lit_color).next_to(t, UP, buff=0.04))
        self.add(self.tanks, self.marks, self.numbers)

    def capture_anims(self, lag=0.2):
        if len(self.numbers) == 0:
            return LaggedStart(*[FadeIn(m, scale=1.6) for m in self.marks], lag_ratio=lag)
        return LaggedStart(*[AnimationGroup(FadeIn(m, scale=1.6), FadeIn(n)) for m, n in zip(self.marks, self.numbers)],
                           lag_ratio=lag)

    def reveal(self, opacity=0.9):
        return self.tanks.animate.set_fill(self.color, opacity=opacity)


class PermutationMachine(VGroup):
    """The permutation test as a machine (Part 10): ``values`` sit as numbered tokens in two rows, group A on top and
    group B below.  ``shuffle(scene, perm)`` deals the tokens into new slots, so they take the colour of the row they
    land in; ``reset`` deals them back.  ``drop(scene, stat)`` stacks the shuffled statistic as a dot on ``ax``, the
    null distribution growing one shuffle at a time; ``mark(stat)`` draws the observed statistic there."""

    def __init__(self, values, in_a, colors=None, center=ORIGIN, width=7.0, radius=0.2, font_size=18, fmt="{:.0f}",
                 row_gap=1.3):
        super().__init__()
        from explainer.analysis import label

        self.values = np.asarray(values, float)
        self.in_a = np.asarray(in_a, bool)
        self.colors = colors or (S.TREAT, S.CTRL)
        na, nb = int(self.in_a.sum()), int((~self.in_a).sum())
        cx, cy = center[0], center[1]

        def row(k, y):
            xs = np.linspace(-width / 2, width / 2, max(k, 2))[:k] if k > 1 else np.array([0.0])
            return [np.array([cx + x, cy + y, 0.0]) for x in xs]

        self.slots_a, self.slots_b = row(na, row_gap / 2), row(nb, -row_gap / 2)
        self.slots = self.slots_a + self.slots_b  # slot j < na is in group A
        order = list(np.flatnonzero(self.in_a)) + list(np.flatnonzero(~self.in_a))
        self.home = {int(i): j for j, i in enumerate(order)}  # token i's starting slot
        self.where = dict(self.home)
        self.tokens = VGroup()
        for i, v in enumerate(self.values):
            j = self.home[i]
            c = self.colors[0] if j < na else self.colors[1]
            disc = Circle(radius=radius, stroke_width=0, fill_color=c, fill_opacity=0.9)
            txt = label(fmt.format(v), font_size=font_size, color="#101418")
            if txt.width > 1.7 * radius:
                txt.width = 1.7 * radius
            self.tokens.add(VGroup(disc, txt).move_to(self.slots[j]))
        self.na = na
        self.add(self.tokens)
        self.stack: dict[int, int] = {}
        self.dots = VGroup()

    def _goto(self, assignment, run_time):
        anims = []
        for i, j in assignment.items():
            c = self.colors[0] if j < self.na else self.colors[1]
            target = self.tokens[i].copy().move_to(self.slots[j])
            target[0].set_fill(c)
            anims.append(Transform(self.tokens[i], target))
        self.where = dict(assignment)
        return AnimationGroup(*anims, run_time=run_time)

    def shuffle(self, perm, run_time=1.0):
        """Animation dealing token i into slot perm[i] (perm: a permutation of range(n))."""
        return self._goto({i: int(perm[i]) for i in range(len(self.values))}, run_time)

    def reset(self, run_time=0.8):
        return self._goto(dict(self.home), run_time)

    def groups(self):
        a = np.array([self.values[i] for i, j in self.where.items() if j < self.na])
        b = np.array([self.values[i] for i, j in self.where.items() if j >= self.na])
        return a, b

    def drop(self, ax, stat, bin_width, radius=0.05, color=None, gap=1.0):
        """A dot for ``stat`` stacked in its bin on ``ax`` (returned, already added to ``self.dots``)."""
        k = int(np.floor(stat / bin_width + 0.5))
        h = self.stack.get(k, 0)
        self.stack[k] = h + 1
        base = ax.c2p(k * bin_width, bounds(ax)[2])
        d = Dot(base + UP * (radius * (2 * h + 1) * gap), radius=radius, color=color or S.NULL)
        self.dots.add(d)
        return d

    def mark(self, ax, stat, color=None, height=None):
        x0, x1, y0, y1 = bounds(ax)
        return DashedLine(ax.c2p(stat, y0), ax.c2p(stat, y1 if height is None else height), color=color or S.ACCENT,
                          stroke_width=3)


class IntervalRain(VGroup):
    """Neyman's promise as weather (Part 11): intervals fall one per sample onto axes ``ax`` (estimate on the x-axis,
    sample index up the y-axis), green if they catch ``truth`` and red if they miss, with a running tally.
    ``rain(scene, intervals)`` animates a batch; ``tally`` is the counter mobject (hits of total)."""

    def __init__(self, ax, truth, y_top=None, dy=None, hit=None, miss=None, stroke_width=2.5, font_size=26, tally_pos=None):
        super().__init__()
        from explainer.analysis import label

        self.ax, self.truth = ax, truth
        x0, x1, y0, y1 = bounds(ax)
        self.y_top = y1 if y_top is None else y_top
        self.dy = dy
        self.hit, self.miss = hit or S.KEPT, miss or S.BROKEN
        self.sw = stroke_width
        self.n = self.k = 0
        self.line = DashedLine(ax.c2p(truth, y0), ax.c2p(truth, y1), color=S.TRUTH, stroke_width=2)
        self.drops = VGroup()
        self.tally = label(r"0 of 0", font_size=font_size)
        self.tally.move_to(tally_pos if tally_pos is not None else ax.c2p(x1, y1) + UP * 0.3 + LEFT * 1.0)
        self.font_size = font_size
        self.add(self.line, self.drops, self.tally)

    def _seg(self, lo, hi, i):
        x0, x1, y0, y1 = bounds(self.ax)
        dy = self.dy or (y1 - y0) / 50
        y = self.y_top - dy * (i + 0.5)
        ok = lo <= self.truth <= hi
        seg = Line(self.ax.c2p(max(lo, x0), y), self.ax.c2p(min(hi, x1), y), color=self.hit if ok else self.miss,
                   stroke_width=self.sw)
        return seg, ok

    def rain(self, scene, intervals, run_time=2.0, lag=0.1):
        from explainer.analysis import label

        segs = VGroup()
        for lo, hi in intervals:
            s_, ok = self._seg(lo, hi, self.n)
            self.n += 1
            self.k += ok
            segs.add(s_)
        self.drops.add(*segs)
        new_tally = label(rf"{self.k} of {self.n} \ ({100 * self.k / max(self.n, 1):.0f}\%)", font_size=self.font_size)
        new_tally.move_to(self.tally)
        scene.play(LaggedStart(*[FadeIn(s_, shift=DOWN * 0.3) for s_ in segs], lag_ratio=lag),
                   Transform(self.tally, new_tally), run_time=run_time)
        return segs


class InfluenceProbe(VGroup):
    """Drag one point and watch least squares respond (Part 12).  ``xs, ys`` are the data on axes ``ax``; the point
    ``index`` follows the trackers ``px, py``, and the fitted line, the point's leverage and its Cook's distance are
    redrawn every frame.  ``readout`` is a VGroup of MathTex to place; call ``stop()`` before clearing the scene."""

    def __init__(self, ax, xs, ys, index=-1, color=None, line_color=None, font_size=26, x_span=None):
        super().__init__()
        from explainer.stats.kit.ols import design, fit

        self.ax = ax
        self.xs, self.ys = np.asarray(xs, float).copy(), np.asarray(ys, float).copy()
        self.i = index % len(self.xs)
        self.px, self.py = ValueTracker(self.xs[self.i]), ValueTracker(self.ys[self.i])
        x0, x1, _, _ = bounds(ax)
        span = x_span or (x0, x1)
        col, lcol = color or S.DATA, line_color or S.FIT
        self.others = VGroup(*[Dot(ax.c2p(a, b), radius=0.07, color=col) for j, (a, b) in enumerate(zip(self.xs, self.ys)) if j != self.i])
        self._fit = lambda: fit(design(self._x()), self._y())

        def line():
            r = self._fit()
            a, b = r.coef
            return Line(ax.c2p(span[0], a + b * span[0]), ax.c2p(span[1], a + b * span[1]), color=lcol, stroke_width=4)

        def probe():
            return Dot(ax.c2p(self.px.get_value(), self.py.get_value()), radius=0.11, color=S.ACCENT)

        def readout():
            r = self._fit()
            return VGroup(MathTex(rf"\text{{slope}} = {r.coef[1]:.2f}", font_size=font_size, color=lcol),
                          MathTex(rf"h_{{ii}} = {r.leverage[self.i]:.2f}", font_size=font_size),
                          MathTex(rf"D_i = {r.cooks[self.i]:.2f}", font_size=font_size, color=S.ACCENT)).arrange(DOWN, aligned_edge=LEFT, buff=0.2)

        self.readout_pos = np.array([4.8, 1.5, 0])
        self.line = always_redraw(line)
        self.dot = always_redraw(probe)
        self.readout = always_redraw(lambda: readout().move_to(self.readout_pos))
        self.add(self.others, self.line, self.dot)

    def _x(self):
        x = self.xs.copy()
        x[self.i] = self.px.get_value()
        return x

    def _y(self):
        y = self.ys.copy()
        y[self.i] = self.py.get_value()
        return y

    def move_to_point(self, x, y, run_time=2.0):
        return AnimationGroup(self.px.animate.set_value(x), self.py.animate.set_value(y), run_time=run_time)

    def stop(self):
        for m in (self.line, self.dot, self.readout):
            m.clear_updaters()


class FieldPlot(VGroup):
    """A field trial seen from above (Part 13): ``rows x cols`` plots drawn as squares, row 0 at the top and column 0
    on the west.  ``paint(values)`` colours every plot by a number (fertility, a yield) from bare soil to deep green;
    ``tags(alloc)`` writes a treatment's letter in each plot; ``outline(r0, r1, c0, c1)`` frames a block.  ``cells[r][c]``
    is one plot's square."""

    SOIL, LEAF = "#5B4632", "#7BD88F"

    def __init__(self, rows: int, cols: int, cell: float = 0.38, gap: float = 0.04, center=ORIGIN):
        super().__init__()
        self.rows, self.cols, self.cell, self.gap = rows, cols, cell, gap
        self.cells = []
        for r in range(rows):
            line = []
            for c in range(cols):
                sq = Square(side_length=cell, stroke_width=0.8, stroke_color=GREY_D, fill_color=self.SOIL, fill_opacity=0.9)
                sq.move_to([(c - (cols - 1) / 2) * (cell + gap), ((rows - 1) / 2 - r) * (cell + gap), 0])
                line.append(sq)
                self.add(sq)
            self.cells.append(line)
        self.move_to(center)

    @classmethod
    def colour(cls, v, lo, hi):
        t = float(np.clip((v - lo) / max(hi - lo, 1e-12), 0, 1))
        return interpolate_color(ManimColor(cls.SOIL), ManimColor(cls.LEAF), t)

    def paint(self, values, lo=None, hi=None, run_time=1.5):
        """An animation colouring each plot by ``values[r, c]`` (lo, hi default to the values' range)."""
        v = np.asarray(values, float)
        lo = v.min() if lo is None else lo
        hi = v.max() if hi is None else hi
        return AnimationGroup(*[self.cells[r][c].animate.set_fill(self.colour(v[r, c], lo, hi), opacity=0.95)
                                for r in range(self.rows) for c in range(self.cols)], run_time=run_time)

    def painted(self, values, lo=None, hi=None):
        """Colour the plots immediately (no animation); returns self."""
        v = np.asarray(values, float)
        lo = v.min() if lo is None else lo
        hi = v.max() if hi is None else hi
        for r in range(self.rows):
            for c in range(self.cols):
                self.cells[r][c].set_fill(self.colour(v[r, c], lo, hi), opacity=0.95)
        return self

    def tags(self, alloc, names="ABCDEFGH", colors=None, font_size=None) -> VGroup:
        """A letter in each plot for the treatment ``alloc[r, c]`` (an integer; negative leaves the plot blank)."""
        from explainer.analysis import label

        colors = colors or [S.TREAT, S.CTRL, S.ALT, S.PRIOR, S.POST, S.TRUTH, S.LIK, WHITE]
        fs = font_size or max(12, int(self.cell * 52))
        g = VGroup()
        for r in range(self.rows):
            for c in range(self.cols):
                k = int(alloc[r][c])
                if k < 0:
                    continue
                t = label(names[k], font_size=fs, color=colors[k % len(colors)])
                disc = Circle(radius=self.cell * 0.36, stroke_width=0, fill_color="#101418", fill_opacity=0.72)
                g.add(VGroup(disc, t).move_to(self.cells[r][c]))
        return g

    def outline(self, r0, r1, c0, c1, color=None, stroke_width=3.0) -> Rectangle:
        """A frame around plots rows r0..r1, columns c0..c1 (inclusive)."""
        a, b = self.cells[r0][c0], self.cells[r1][c1]
        w = b.get_right()[0] - a.get_left()[0] + self.gap
        h = a.get_top()[1] - b.get_bottom()[1] + self.gap
        return Rectangle(width=w, height=h, color=color or S.ACCENT, stroke_width=stroke_width).move_to(
            [(a.get_left()[0] + b.get_right()[0]) / 2, (a.get_top()[1] + b.get_bottom()[1]) / 2, 0])


class ChallengerDashboard(VGroup):
    """Risk as a function of temperature (Part 14).  ``x, y`` are the flights (temperature, 0/1 distress) on axes ``ax``
    whose y-axis runs 0-1; ``fit`` is a ``statkit.glm`` logistic fit on (1, x).  Draws the data as dots at 0 and 1 (ties
    stacked), the fitted curve and its 95% Wald band, and a probe: a dashed line at the tracker ``tx`` with the fitted
    probability and its interval read out.  ``slide_to(x)`` moves the probe; call ``stop()`` before clearing."""

    def __init__(self, ax, x, y, fit, x0=None, color=None, band_color=None, font_size=26, stack=0.045, readout_pos=None):
        super().__init__()
        from explainer.analysis import label

        self.ax, self.fit = ax, fit
        x, y = np.asarray(x, float), np.asarray(y, float)
        x_lo, x_hi, _, _ = bounds(ax)
        col = color or S.FIT
        seen: dict = {}
        self.dots = VGroup()
        for a, b in zip(x, y):
            k = seen.get((a, b), 0)
            seen[(a, b)] = k + 1
            off = (k * stack) * (-1 if b > 0.5 else 1)
            self.dots.add(Dot(ax.c2p(a, b + off), radius=0.07, color=S.BROKEN if b > 0.5 else S.DATA))
        xs = np.linspace(x_lo, x_hi, 240)
        Xg = np.column_stack([np.ones_like(xs), xs])
        lo, mid, hi = fit.predict_ci(Xg)
        self.curve = VMobject(stroke_color=col, stroke_width=4).set_points_smoothly([ax.c2p(a, b) for a, b in zip(xs, mid)])
        pts = [ax.c2p(a, b) for a, b in zip(xs, hi)] + [ax.c2p(a, b) for a, b in zip(xs[::-1], lo[::-1])]
        self.band = Polygon(*pts, stroke_width=0, fill_color=band_color or col, fill_opacity=0.18)
        self.tx = ValueTracker(x0 if x0 is not None else float(np.mean(x)))
        self.readout_pos = np.array(readout_pos if readout_pos is not None else [4.6, 1.2, 0])

        def probe():
            t = self.tx.get_value()
            p = float(fit.predict(np.array([1.0, t])))
            return VGroup(DashedLine(ax.c2p(t, 0), ax.c2p(t, 1), color=S.ACCENT, stroke_width=2.5),
                          Dot(ax.c2p(t, p), radius=0.1, color=S.ACCENT))

        def readout():
            t = self.tx.get_value()
            lo_, p, hi_ = (float(v[0]) for v in fit.predict_ci(np.array([[1.0, t]])))
            return VGroup(label(rf"{t:.0f}$^\circ$F", font_size=font_size, color=S.ACCENT),
                          MathTex(rf"\hat p = {p:.4f}", font_size=font_size, color=col),
                          MathTex(rf"[{lo_:.3f},\ {min(hi_, 0.9999):.4f}]", font_size=font_size - 4, color=GREY_A)
                          ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to(self.readout_pos)

        self.probe = always_redraw(probe)
        self.readout = always_redraw(readout)
        self.add(self.band, self.curve, self.dots)

    def slide_to(self, x, run_time=2.0):
        return self.tx.animate(run_time=run_time).set_value(x)

    def stop(self):
        for m in (self.probe, self.readout):
            m.clear_updaters()


class BilliardTable(VGroup):
    """Bayes's table (Part 15): a square of felt seen from above, with coordinates (u, v) in [0, 1]^2.  The hidden ball
    W stops at some u; each later ball counts as a success if it stops left of W's line.  ``point(u, v)`` maps table
    coordinates to the scene; ``line(u)`` draws W's line; ``roll(u, v)`` returns a ball and the animation that sends it
    from the near cushion to (u, v) along a gentle arc."""

    FELT, CUSHION = "#1F4D3A", "#6B4A2B"

    def __init__(self, width: float = 6.0, height: float = 3.6, center=ORIGIN):
        super().__init__()
        self.w, self.h = width, height
        self.felt = Rectangle(width=width, height=height, stroke_width=0, fill_color=self.FELT, fill_opacity=1.0)
        self.cushion = Rectangle(width=width + 0.24, height=height + 0.24, stroke_color=self.CUSHION, stroke_width=10)
        self.add(self.cushion, self.felt)
        self.move_to(center)

    def point(self, u, v):
        c = self.felt.get_center()
        return np.array([c[0] + (u - 0.5) * self.w, c[1] + (v - 0.5) * self.h, 0.0])

    def line(self, u, color=None, stroke_width=3.0):
        return DashedLine(self.point(u, 0), self.point(u, 1), color=color or S.TRUTH, stroke_width=stroke_width)

    def roll(self, u, v, color=None, radius=0.09, run_time=0.8):
        ball = Dot(self.point(0.5, -0.02), radius=radius, color=color or WHITE)
        start, end = self.point(0.5, 0.02), self.point(u, v)
        mid = (start + end) / 2 + np.array([0, 0.25, 0])
        path = VMobject().set_points_smoothly([start, mid, end])
        return ball, MoveAlongPath(ball, path, run_time=run_time, rate_func=rate_functions.ease_out_cubic)
