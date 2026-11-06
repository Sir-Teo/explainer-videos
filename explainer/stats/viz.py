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


class BootstrapResampler(VGroup):
    """The bootstrap as a machine (Part 16): the sample sits as labelled tokens in a top row; ``resample(idx)``
    copies the tokens idx[0], idx[1], ... into a bottom row (so some appear twice and some not at all), and
    ``clear()`` removes them; ``drop(ax, stat, bin_width)`` stacks each replicate's statistic as a dot on ``ax``."""

    def __init__(self, labels, center=ORIGIN, width=10.0, radius=0.22, font_size=18, row_gap=1.4, color=None, copy_color=None):
        super().__init__()
        from explainer.analysis import label

        self.n = len(labels)
        cx, cy = center[0], center[1]
        xs = np.linspace(-width / 2, width / 2, self.n) if self.n > 1 else np.array([0.0])
        self.top = [np.array([cx + x, cy + row_gap / 2, 0.0]) for x in xs]
        self.bottom = [np.array([cx + x, cy - row_gap / 2, 0.0]) for x in xs]
        col = color or S.DATA
        self.copy_color = copy_color or S.EST
        self.tokens = VGroup()
        for i, t in enumerate(labels):
            disc = Circle(radius=radius, stroke_width=0, fill_color=col, fill_opacity=0.9)
            txt = label(str(t), font_size=font_size, color="#101418")
            if txt.width > 1.7 * radius:
                txt.width = 1.7 * radius
            self.tokens.add(VGroup(disc, txt).move_to(self.top[i]))
        self.add(self.tokens)
        self.copies = VGroup()
        self.stack: dict[int, int] = {}
        self.dots = VGroup()

    def resample(self, idx, run_time=1.2, lag=0.04):
        """Animation: copy token idx[j] to bottom slot j, for every j."""
        new = VGroup()
        anims = []
        for j, i in enumerate(idx):
            c = self.tokens[int(i)].copy()
            c[0].set_fill(self.copy_color)
            target = c.copy().move_to(self.bottom[j])
            anims.append(TransformFromCopy(self.tokens[int(i)], target))
            new.add(target)
        self.copies = new
        return LaggedStart(*anims, lag_ratio=lag, run_time=run_time)

    def clear(self, run_time=0.4):
        return FadeOut(self.copies, run_time=run_time)

    def drop(self, ax, stat, bin_width, radius=0.05, color=None):
        k = int(np.floor(stat / bin_width + 0.5))
        h = self.stack.get(k, 0)
        self.stack[k] = h + 1
        base = ax.c2p(k * bin_width, bounds(ax)[2])
        d = Dot(base + UP * (radius * (2 * h + 1)), radius=radius, color=color or S.EST)
        self.dots.add(d)
        return d


class KernelSum(VGroup):
    """A kernel density estimate as a sum of bumps (Part 16): one Gaussian bump of width ``h`` and area 1/n under
    each observation on axes ``ax``, and their sum.  ``bumps`` and ``total`` are the curves; ``rug`` marks the data."""

    def __init__(self, ax, x, h, grid=None, bump_color=None, total_color=None, rug_color=None):
        super().__init__()
        x = np.asarray(x, float)
        x0, x1, y0, _ = bounds(ax)
        g = np.linspace(x0, x1, 300) if grid is None else np.asarray(grid, float)
        n = len(x)
        self.bumps = VGroup()
        for xi in x:
            f = np.exp(-0.5 * ((g - xi) / h) ** 2) / (np.sqrt(2 * np.pi) * h * n)
            self.bumps.add(VMobject(stroke_color=bump_color or GREY_B, stroke_width=1.5, stroke_opacity=0.8)
                           .set_points_smoothly([ax.c2p(a, b) for a, b in zip(g, f)]))
        tot = np.exp(-0.5 * ((g[:, None] - x[None, :]) / h) ** 2).sum(1) / (np.sqrt(2 * np.pi) * h * n)
        self.values = tot
        self.total = VMobject(stroke_color=total_color or S.EST, stroke_width=4).set_points_smoothly([ax.c2p(a, b) for a, b in zip(g, tot)])
        self.rug = VGroup(*[Line(ax.c2p(xi, y0), ax.c2p(xi, y0) + UP * 0.18, color=rug_color or S.DATA, stroke_width=2) for xi in x])
        self.add(self.rug, self.bumps, self.total)


class Correlogram(VGroup):
    """A correlogram (Part 17): one bar per lag k = 1..K for the autocorrelations ``r`` (r[0] = 1 is skipped) on axes
    ``ax`` (x: lag, y: correlation), with dashed bands at +-``band`` (2/sqrt n) and, optionally, the theoretical values
    as dots.  ``bars`` and ``bands`` are the parts; bars outside the bands are drawn in ``hot``."""

    def __init__(self, ax, r, band=None, theory=None, color=None, hot=None, width=0.5, start=1):
        super().__init__()
        r = np.asarray(r, float)
        x0, x1, y0, y1 = bounds(ax)
        self.bars = VGroup()
        w = ax.c2p(width, 0)[0] - ax.c2p(0, 0)[0]
        for k in range(start, len(r)):
            v = r[k]
            out = band is not None and abs(v) > band
            top, bot = ax.c2p(k, max(v, 0)), ax.c2p(k, min(v, 0))
            h = max(1e-3, top[1] - bot[1])
            self.bars.add(Rectangle(width=w, height=h, stroke_width=0, fill_color=(hot or S.ACCENT) if out else (color or S.EST),
                                    fill_opacity=0.9).move_to((top + bot) / 2))
        self.zero = Line(ax.c2p(x0, 0), ax.c2p(x1, 0), color=GREY_C, stroke_width=1.5)
        self.bands = VGroup()
        if band is not None:
            for s in (band, -band):
                self.bands.add(DashedLine(ax.c2p(x0, s), ax.c2p(x1, s), color=GREY_B, stroke_width=1.5, dash_length=0.08))
        self.theory = VGroup()
        if theory is not None:
            for k in range(start, min(len(theory), len(r))):
                self.theory.add(Dot(ax.c2p(k, theory[k]), radius=0.05, color=S.TRUTH))
        self.add(self.zero, self.bands, self.bars, self.theory)


class RootPlane(VGroup):
    """The complex plane for ARMA roots (Part 17): the unit circle, the real and imaginary axes, and ``roots`` as
    dots, coloured ``inside``/``outside`` by whether they lie inside the circle (non-stationary) or outside (fine).
    ``mark(roots)`` returns new root dots; ``circle`` and ``dots`` are the parts.  ``scale`` (stored as ``unit``) is the
    screen length of one unit."""

    def __init__(self, roots=(), center=ORIGIN, scale=1.2, extent=2.2, inside=None, outside=None, font_size=20):
        super().__init__()
        from explainer.analysis import label

        self.c = np.asarray(center, float)
        self.unit = scale
        self.inside, self.outside = inside or S.RESID, outside or S.KEPT
        e = extent * scale
        self.axes_ = VGroup(Line(self.c + LEFT * e, self.c + RIGHT * e, color=GREY_C, stroke_width=1.5),
                            Line(self.c + DOWN * e, self.c + UP * e, color=GREY_C, stroke_width=1.5))
        self.circle = Circle(radius=scale, color=GREY_A, stroke_width=2.5).move_to(self.c)
        self.labels = VGroup(label(r"Re", font_size=font_size, color=GREY_B).next_to(self.c + RIGHT * e, DOWN, buff=0.1),
                             label(r"Im", font_size=font_size, color=GREY_B).next_to(self.c + UP * e, LEFT, buff=0.1),
                             MathTex(r"1", font_size=font_size, color=GREY_B).next_to(self.c + RIGHT * scale, DR, buff=0.05))
        self.dots = self.mark(roots)
        self.add(self.axes_, self.circle, self.labels, self.dots)

    def point(self, z) -> np.ndarray:
        z = complex(z)
        return self.c + self.unit * np.array([z.real, z.imag, 0.0])

    def mark(self, roots, radius=0.09) -> VGroup:
        g = VGroup()
        for z in roots:
            z = complex(z[0], z[1]) if isinstance(z, (list, tuple)) else complex(z)
            col = self.outside if abs(z) > 1 else self.inside
            g.add(Dot(self.point(z), radius=radius, color=col))
        return g


class YulePendulum(VGroup):
    """Yule's (1927) picture of an AR(2): a pendulum, left to itself a damped swing, bombarded by boys with
    pea-shooters.  The bob's displacement follows a series ``x`` (scaled so max |x| swings ``max_angle``); ``at(t)``
    places it at step t; ``pea(t)`` returns a pea flying in from the side the shock e_t pushes."""

    def __init__(self, x, pivot=ORIGIN, length=2.6, max_angle=0.6, color=None, bob_radius=0.18):
        super().__init__()
        self.x = np.asarray(x, float)
        self.k = max_angle / max(1e-9, np.max(np.abs(self.x)))
        self.pivot = np.asarray(pivot, float)
        self.length = length
        self.mount = Line(self.pivot + LEFT * 0.6, self.pivot + RIGHT * 0.6, color=GREY_B, stroke_width=4)
        self.rod = Line(self.pivot, self.pivot + DOWN * length, color=GREY_A, stroke_width=3)
        self.bob = Dot(self.pivot + DOWN * length, radius=bob_radius, color=color or S.EST)
        self.add(self.mount, self.rod, self.bob)
        self.at(0)

    def tip(self, t) -> np.ndarray:
        a = self.k * self.x[int(t)]
        return self.pivot + self.length * np.array([np.sin(a), -np.cos(a), 0.0])

    def at(self, t):
        p = self.tip(t)
        self.rod.put_start_and_end_on(self.pivot, p)
        self.bob.move_to(p)
        return self

    def pea(self, t, shock: float, color=None) -> Dot:
        p = self.tip(t)
        side = LEFT if shock > 0 else RIGHT
        return Dot(p + side * 1.6, radius=0.06, color=color or S.ACCENT)


class IslandMap(VGroup):
    """The World's island (Part 18): its coastline, and its 200 towns as dots sized by population and tinted by
    region.  ``towns`` is ``World().towns``.  ``highlight(idx, color)`` returns an animation lighting some towns (a
    cluster sample); ``point(i)`` is town i's position on screen."""

    def __init__(self, towns: dict, center=ORIGIN, scale=0.62, colors=None, max_radius=0.22, min_radius=0.03, coast=True):
        super().__init__()
        self.c = np.asarray(center, float)
        self.unit = scale
        xy, w, reg = np.asarray(towns["xy"]), np.asarray(towns["weight"]), np.asarray(towns["region"])
        palette = colors or [S.CTRL, S.TREAT, S.ALT, S.PRIOR, S.POST, S.EST, S.FIT, S.TRUTH, S.ACCENT, S.WORLD]
        r = min_radius + (max_radius - min_radius) * np.sqrt(w / w.max())
        self.radii = r
        self.dots = VGroup(*[Dot(self.point_xy(p), radius=float(rr), color=palette[int(k) % len(palette)], fill_opacity=0.8)
                             for p, rr, k in zip(xy, r, reg)])
        self.coast = VMobject()
        if coast:
            th = np.linspace(0, 2 * np.pi, 240)
            wob = 0.86 + 0.1 * np.sin(3 * th + 0.7) + 0.05 * np.cos(5 * th)
            c, s = np.cos(th), np.sin(th)
            rr = wob / (np.abs(c) ** 2.6 + np.abs(s * 5 / 3.4) ** 2.6) ** (1 / 2.6) * 1.04
            pts = [self.point_xy((5 * rk * ck / 5, 5 * rk * sk / 5)) for rk, ck, sk in zip(rr * 5, c, s)]
            self.coast = VMobject(stroke_color=GREY_C, stroke_width=2).set_points_smoothly(pts + [pts[0]])
        self.add(self.coast, self.dots)

    def point_xy(self, p) -> np.ndarray:
        return self.c + self.unit * np.array([p[0], p[1], 0.0])

    def point(self, i: int) -> np.ndarray:
        return self.dots[int(i)].get_center()

    def highlight(self, idx, color=None, scale=1.4):
        idx = set(int(i) for i in idx)
        anims = []
        for i, d in enumerate(self.dots):
            if i in idx:
                anims.append(d.animate.set_color(color or S.ACCENT).set_opacity(1).scale(scale))
            else:
                anims.append(d.animate.set_opacity(0.15))
        return AnimationGroup(*anims)


class L1Geometry(VGroup):
    """Ridge and lasso as geometry (Parts 19, 32): the (beta1, beta2) plane with the least-squares estimate ``ols``,
    elliptical contours of the loss (b - ols)' Q (b - ols), and constraint balls |b|_q <= t.  ``ball(q, t)`` draws a
    diamond (q = 1) or circle (q = 2); ``touch(q, t)`` is the constrained minimum (a corner, for the diamond, more often
    than not); ``contour(c)`` the loss level set through value c."""

    def __init__(self, ols, Q=None, center=ORIGIN, unit=1.0, extent=3.0, font_size=22):
        super().__init__()
        from explainer.analysis import label

        self.c = np.asarray(center, float)
        self.unit = unit
        self.ols = np.asarray(ols, float)
        self.Q = np.eye(2) if Q is None else np.asarray(Q, float)
        e = extent * unit
        self.axes_ = VGroup(Line(self.c + LEFT * e, self.c + RIGHT * e, color=GREY_C, stroke_width=1.5),
                            Line(self.c + DOWN * e, self.c + UP * e, color=GREY_C, stroke_width=1.5))
        self.labels = VGroup(MathTex(r"\beta_1", font_size=font_size, color=GREY_B).next_to(self.c + RIGHT * e, DOWN, buff=0.1),
                             MathTex(r"\beta_2", font_size=font_size, color=GREY_B).next_to(self.c + UP * e, LEFT, buff=0.1))
        self.ols_dot = Dot(self.p(self.ols), radius=0.08, color=S.FIT)
        self.add(self.axes_, self.labels, self.ols_dot)

    def p(self, b) -> np.ndarray:
        return self.c + self.unit * np.array([b[0], b[1], 0.0])

    def loss(self, b) -> float:
        d = np.asarray(b, float) - self.ols
        return float(d @ self.Q @ d)

    def contour(self, level: float, color=None, stroke_width=2.0) -> VMobject:
        w, V = np.linalg.eigh(self.Q)
        th = np.linspace(0, 2 * np.pi, 160)
        pts = [self.ols + V @ (np.sqrt(level / w) * np.array([np.cos(t), np.sin(t)])) for t in th]
        return VMobject(stroke_color=color or S.FIT, stroke_width=stroke_width, stroke_opacity=0.8).set_points_smoothly(
            [self.p(q) for q in pts])

    def _boundary(self, q: float, t: float, m: int = 4000) -> np.ndarray:
        th = np.linspace(0, 2 * np.pi, m, endpoint=False)
        c, s = np.cos(th), np.sin(th)
        r = t / (np.abs(c) ** q + np.abs(s) ** q) ** (1 / q)
        return np.column_stack([r * c, r * s])

    def ball(self, q: float, t: float, color=None, fill=0.15) -> VMobject:
        if q == 1:
            return Polygon(*[self.p(v) for v in ((t, 0), (0, t), (-t, 0), (0, -t))], color=color or S.ACCENT, stroke_width=2.5,
                           fill_color=color or S.ACCENT, fill_opacity=fill)
        pts = self._boundary(q, t, 240)
        return Polygon(*[self.p(v) for v in pts], color=color or S.ACCENT, stroke_width=2.5, fill_color=color or S.ACCENT,
                       fill_opacity=fill)

    def touch(self, q: float, t: float) -> np.ndarray:
        if np.sum(np.abs(self.ols) ** q) ** (1 / q) <= t:
            return self.ols.copy()
        pts = self._boundary(q, t)
        if q == 1:
            pts = np.vstack([pts, [[t, 0], [0, t], [-t, 0], [0, -t]]])
        L = np.einsum("ij,jk,ik->i", pts - self.ols, self.Q, pts - self.ols)
        return pts[int(np.argmin(L))]


def marching_squares(Z, xs, ys, level):
    """Line segments of the level set {Z = level} on the grid (xs[j], ys[i]) -> Z[i, j], by marching squares (the
    two ambiguous saddle cases split by the cell's mean).  Returns a list of ((x0, y0), (x1, y1))."""
    Z = np.asarray(Z, float)
    segs = []
    for i in range(len(ys) - 1):
        for j in range(len(xs) - 1):
            v = [Z[i, j], Z[i, j + 1], Z[i + 1, j + 1], Z[i + 1, j]]  # corners: bottom-left, bottom-right, top-right, top-left
            c = [(xs[j], ys[i]), (xs[j + 1], ys[i]), (xs[j + 1], ys[i + 1]), (xs[j], ys[i + 1])]
            above = [a > level for a in v]
            if all(above) or not any(above):
                continue
            cuts = []
            for e in range(4):
                a, b = e, (e + 1) % 4
                if above[a] != above[b]:
                    t = (level - v[a]) / (v[b] - v[a])
                    cuts.append((c[a][0] + t * (c[b][0] - c[a][0]), c[a][1] + t * (c[b][1] - c[a][1])))
            if len(cuts) == 2:
                segs.append((cuts[0], cuts[1]))
            elif len(cuts) == 4:
                if (np.mean(v) > level) == above[0]:
                    segs += [(cuts[0], cuts[1]), (cuts[2], cuts[3])]
                else:
                    segs += [(cuts[3], cuts[0]), (cuts[1], cuts[2])]
    return segs


class Landscape(VGroup):
    """Level sets of a function of two parameters on ``ax`` (an objective, a likelihood), and the paths optimizers
    take across it.  ``f(X, Y)`` must accept arrays, or ``f`` may be a precomputed grid ``Z[i, j]`` at
    ``(x_j, y_i)`` spanning the ranges.  ``levels`` are drawn from the first (brightest) on."""

    def __init__(self, ax, f, x_range, y_range, levels, n: int = 90, color=None, stroke_width: float = 2.0, **kw):
        super().__init__(**kw)
        self.ax = ax
        if callable(f):
            xs = np.linspace(x_range[0], x_range[1], n)
            ys = np.linspace(y_range[0], y_range[1], n)
            Xg, Yg = np.meshgrid(xs, ys)
            self.Z = np.asarray(f(Xg, Yg), float)
        else:  # a precomputed grid: Z[i, j] at (x_j, y_i) over the ranges
            self.Z = np.asarray(f, float)
            ys = np.linspace(y_range[0], y_range[1], self.Z.shape[0])
            xs = np.linspace(x_range[0], x_range[1], self.Z.shape[1])
        self.xs, self.ys = xs, ys
        color = color or S.EST
        self.levels = VGroup()
        for k, lv in enumerate(levels):
            vm = VMobject(stroke_color=color, stroke_width=stroke_width, stroke_opacity=max(0.25, 0.95 - 0.08 * k))
            for p0, p1 in marching_squares(self.Z, xs, ys, lv):
                vm.start_new_path(ax.c2p(*p0))
                vm.add_line_to(ax.c2p(*p1))
            self.levels.add(vm)
        self.add(self.levels)

    def path(self, pts, color=None, radius: float = 0.06, stroke_width: float = 3.0) -> VGroup:
        """An optimizer's iterates as dots joined by segments (one Line per step, so steps can be animated)."""
        color = color or S.ACCENT
        pts = [self.ax.c2p(float(a), float(b)) for a, b in np.asarray(pts, float)]
        dots = VGroup(*[Dot(p, radius=radius, color=color) for p in pts])
        steps = VGroup(*[Line(p, q, color=color, stroke_width=stroke_width) for p, q in zip(pts, pts[1:])])
        return VGroup(steps, dots)


class LikelihoodLandscape(Landscape):
    """A two-parameter log likelihood as contours (a ``Landscape``), with its peak, the profile ridge (the best second
    parameter for each value of the first) and likelihood-ratio confidence regions.  ``levels_below`` are drops from
    the maximum: 1.92 and 3.0 give the 95% profile cut and the 95% joint region (chi^2_1 / 2 and chi^2_2 / 2)."""

    def __init__(self, ax, ll, x_range, y_range, levels_below=(0.5, 1.92, 3.0, 8, 20, 50), color=None, **kw):
        ll = np.asarray(ll, float)
        self.ll_max = float(np.nanmax(ll))
        super().__init__(ax, ll, x_range, y_range, [self.ll_max - d for d in levels_below], color=color, **kw)
        i, j = np.unravel_index(int(np.nanargmax(ll)), ll.shape)
        self.peak_xy = (self.xs[j], self.ys[i])

    def peak(self, color=None, radius: float = 0.09) -> Dot:
        return Dot(self.ax.c2p(*self.peak_xy), radius=radius, color=color or S.ACCENT)

    def ridge(self, color=None, stroke_width: float = 3.0) -> VMobject:
        """The profile ridge: for each column (first parameter), the row (second parameter) of highest likelihood."""
        rows = np.nanargmax(self.Z, axis=0)
        pts = [self.ax.c2p(x, self.ys[r]) for x, r in zip(self.xs, rows)]
        m = VMobject(stroke_color=color or S.ACCENT, stroke_width=stroke_width)
        m.set_points_smoothly(pts[::3] + [pts[-1]])
        return m

    def profile(self) -> tuple:
        """(first parameter values, profile log likelihood)."""
        return self.xs, np.nanmax(self.Z, axis=0)


class DigitsBoard(VGroup):
    """How many digits are right (Part 23): one row per coefficient, one column per method; each cell is a bar of
    ``max_digits`` ticks, lit up to the number of correct significant digits (green when most are right, amber
    in between, red when almost none are).  ``column(j)`` is method j's cells, for revealing one method at a time."""

    def __init__(self, names, methods, digits, max_digits: int = 15, cell_w: float = 1.9, row_h: float = 0.5,
                 font_size: int = 22, center=ORIGIN):
        super().__init__()
        from explainer.analysis import label

        digits = np.asarray(digits, float)  # methods x coefficients
        self.max = max_digits
        self.heads = VGroup(*[label(m, font_size=font_size, color=GREY_A) for m in methods])
        self.names = VGroup(*[label(n, font_size=font_size, color=GREY_B) for n in names])
        self.cells = VGroup()
        name_w = max(n.width for n in self.names) + 0.35
        for j in range(len(methods)):
            col = VGroup()
            for i in range(len(names)):
                col.add(self._cell(digits[j, i], cell_w, row_h * 0.5, font_size - 4))
            self.cells.add(col)
        for i, n in enumerate(self.names):
            n.move_to([-name_w / 2, -i * row_h, 0], aligned_edge=RIGHT).shift(RIGHT * (name_w / 2 - 0.2))
        for j, col in enumerate(self.cells):
            x = name_w + j * (cell_w + 0.35) + cell_w / 2
            self.heads[j].move_to([x, row_h * 0.95, 0])
            for i, c in enumerate(col):
                c.move_to([x, -i * row_h, 0])
        self.add(self.names, self.heads, self.cells)
        self.move_to(center)

    def _cell(self, d, w, h, font_size):
        from explainer.analysis import label

        k = int(np.floor(d + 1e-9))
        color = S.KEPT if d >= 9 else (S.ACCENT if d >= 3 else S.BROKEN)
        tw = (w - 0.55) / self.max
        ticks = VGroup(*[Rectangle(width=tw * 0.8, height=h, stroke_width=0, fill_opacity=0.9 if t < k else 0.12,
                                   fill_color=color if t < k else GREY_D) for t in range(self.max)]).arrange(RIGHT, buff=tw * 0.2)
        num = label(f"{k}", font_size=font_size, color=color).next_to(ticks, RIGHT, buff=0.1)
        return VGroup(ticks, num)

    def column(self, j: int) -> VGroup:
        return VGroup(self.heads[j], self.cells[j])


class DoseResponse(VGroup):
    """Dose against response probability (Part 24): ``points`` are the observed proportions k/n, each a dot whose area
    grows with its trials n, with a binomial 95% interval bar; ``curve(ginv, coef)`` draws a fitted inverse link
    p = ginv(a + b x) across the dose range; ``mark(x, p)`` drops guide lines to the axes (an LD50)."""

    def __init__(self, x, n, k, x_range, x_length=8.0, y_length=4.4, center=ORIGIN, xlabel=r"dose", xticks=None,
                 color=None, font_size=20):
        super().__init__()
        from explainer.ai.viz import axes as _axes
        from scipy import stats as _st

        self.A = _axes(list(x_range), [0, 1], x_length=x_length, y_length=y_length, xlabel=xlabel,
                       ylabel=r"proportion responding", xticks=xticks, yticks=[0, 0.25, 0.5, 0.75, 1], center=center,
                       font_size=font_size)
        self.ax = self.A.ax
        self.x_range = x_range
        x, n, k = (np.asarray(v, float) for v in (x, n, k))
        p = k / n
        self.dots, self.bars = VGroup(), VGroup()
        for xi, ni, ki, pi in zip(x, n, k, p):
            lo = _st.beta.ppf(0.025, ki, ni - ki + 1) if ki > 0 else 0.0
            hi = _st.beta.ppf(0.975, ki + 1, ni - ki) if ki < ni else 1.0
            self.bars.add(Line(self.ax.c2p(xi, lo), self.ax.c2p(xi, hi), color=GREY_B, stroke_width=2))
            self.dots.add(Dot(self.ax.c2p(xi, pi), radius=0.05 + 0.012 * np.sqrt(ni), color=color or S.DATA))
        self.add(self.A, self.bars, self.dots)

    def curve(self, ginv, coef, color=None, stroke_width=3.5) -> VMobject:
        xs = np.linspace(self.x_range[0], self.x_range[1], 200)
        ps = np.clip(ginv(coef[0] + coef[1] * xs), 0, 1)
        m = VMobject(stroke_color=color or S.FIT, stroke_width=stroke_width)
        m.set_points_smoothly([self.ax.c2p(a, b) for a, b in zip(xs, ps)])
        return m

    def mark(self, x, p, color=None) -> VGroup:
        c = color or S.ACCENT
        return VGroup(DashedLine(self.ax.c2p(self.x_range[0], p), self.ax.c2p(x, p), color=c, stroke_width=2),
                      DashedLine(self.ax.c2p(x, p), self.ax.c2p(x, 0), color=c, stroke_width=2),
                      Dot(self.ax.c2p(x, p), radius=0.07, color=c))


class ShrinkagePlot(VGroup):
    """Efron & Morris's picture of shrinkage (Part 25): one horizontal scale; the raw estimates as dots on an upper
    line, the shrunk estimates on a middle line, and (optionally) the truths on a lower line, with arrows from each
    raw estimate to its shrunk value and thin lines on to its truth.  ``arrows`` and ``truth_links`` are VGroups for
    animating; ``x_of(v)`` maps a value to the screen."""

    def __init__(self, raw, shrunk, truth=None, x_range=(0, 1), width=11.0, center=ORIGIN, gap=1.4, labels=None,
                 ticks=None, fmt=None, font_size=20, colors=None):
        super().__init__()
        from explainer.analysis import label

        raw, shrunk = np.asarray(raw, float), np.asarray(shrunk, float)
        c = np.asarray(center, float)
        lo, hi = x_range
        self.x_of = lambda v: c[0] - width / 2 + width * (np.asarray(v, float) - lo) / (hi - lo)
        cols = colors or {"raw": S.EST, "shrunk": S.KEPT, "truth": S.TRUTH}
        ys = {"raw": c[1] + gap, "shrunk": c[1], "truth": c[1] - gap}
        names = labels or {"raw": "raw", "shrunk": "shrunk", "truth": "truth"}
        self.lines = VGroup()
        self.names = VGroup()
        rows = ["raw", "shrunk"] + (["truth"] if truth is not None else [])
        for r in rows:
            self.lines.add(Line([c[0] - width / 2, ys[r], 0], [c[0] + width / 2, ys[r], 0], color=GREY_D, stroke_width=1.5))
            self.names.add(label(names[r], font_size=font_size, color=cols[r]).next_to([c[0] - width / 2, ys[r], 0], LEFT, buff=0.25))
        self.raw = VGroup(*[Dot([self.x_of(v), ys["raw"], 0], radius=0.07, color=cols["raw"]) for v in raw])
        self.shrunk = VGroup(*[Dot([self.x_of(v), ys["shrunk"], 0], radius=0.07, color=cols["shrunk"]) for v in shrunk])
        self.arrows = VGroup(*[Line([self.x_of(a), ys["raw"] - 0.08, 0], [self.x_of(b), ys["shrunk"] + 0.08, 0], color=GREY_B,
                                    stroke_width=1.5) for a, b in zip(raw, shrunk)])
        self.add(self.lines, self.names)
        if truth is not None:
            truth = np.asarray(truth, float)
            self.truth = VGroup(*[Dot([self.x_of(v), ys["truth"], 0], radius=0.07, color=cols["truth"]) for v in truth])
            self.truth_links = VGroup(*[DashedLine([self.x_of(b), ys["shrunk"] - 0.08, 0], [self.x_of(t), ys["truth"] + 0.08, 0],
                                                   color=GREY_C, stroke_width=1) for b, t in zip(shrunk, truth)])
        if ticks is not None:
            f = fmt or (lambda v: f"{v:g}")
            yb = ys["truth"] if truth is not None else ys["shrunk"]
            self.ticks = VGroup(*[label(f(t), font_size=font_size - 2, color=GREY_B).move_to([self.x_of(t), yb - 0.4, 0]) for t in ticks])
            self.add(self.ticks)


class TauExplorer(VGroup):
    """Rubin's eight schools as a function of the between-school SD (Part 26): on top, each school's conditional
    posterior mean E(theta_j | tau, y) against tau, fanning out from the pooled mean at tau = 0 to the school's own
    estimate as tau grows; below, the marginal posterior p(tau | y) on the same tau axis.  ``line_at(t)`` is a vertical
    cursor through both panels, and ``dots_at(t)`` the schools' estimates at that tau, for animating with a
    ValueTracker."""

    def __init__(self, tau, cond_mean, post_tau, labels, y=None, tau_max=30.0, width=8.6, top_h=3.6, bottom_h=1.4,
                 center=ORIGIN, y_range=(-5, 30), colors=None, font_size=20):
        super().__init__()
        from explainer.ai.viz import axes
        from explainer.analysis import label

        tau = np.asarray(tau, float)
        cm = np.asarray(cond_mean, float)
        pt = np.asarray(post_tau, float)
        keep = tau <= tau_max
        tau, cm, pt = tau[keep], cm[keep], pt[keep]
        c = np.asarray(center, float)
        top_c = c + np.array([0, bottom_h / 2 + 0.55, 0])
        bot_c = c - np.array([0, top_h / 2 + 0.35, 0])
        step = 10 if tau_max > 15 else 5
        self.top = axes([0, tau_max], list(y_range), x_length=width, y_length=top_h, ylabel=r"E($\theta_j \mid \tau, y$)",
                        yticks=list(range(int(np.ceil(y_range[0] / 10) * 10), int(y_range[1]) + 1, 10)), font_size=font_size,
                        center=top_c)
        ymax = float(pt.max()) * 1.1
        self.bottom = axes([0, tau_max], [0, ymax], x_length=width, y_length=bottom_h, xlabel=r"$\tau$, \ the SD of the true effects",
                           xticks=list(range(0, int(tau_max) + 1, step)), font_size=font_size, center=bot_c)
        self.bottom.ylabel = label(r"p($\tau \mid y$)", font_size=font_size + 2, color=GREY_A).next_to(self.bottom.ax, LEFT, buff=0.2)
        self.bottom.add(self.bottom.ylabel)
        ax, bx = self.top.ax, self.bottom.ax
        cols = colors or [S.EST] * cm.shape[1]
        self.curves = VGroup()
        self.names = VGroup()
        for j in range(cm.shape[1]):
            m = VMobject(stroke_color=cols[j], stroke_width=2.5)
            m.set_points_smoothly([ax.c2p(t, v) for t, v in zip(tau[::4], cm[::4, j])])
            self.curves.add(m)
            self.names.add(label(labels[j], font_size=font_size, color=cols[j]).next_to(ax.c2p(tau[-1], cm[-1, j]), RIGHT, buff=0.12))
        _spread(self.names, 0.24)
        self.density = VMobject(stroke_color=S.POST, stroke_width=3)
        self.density.set_points_smoothly([bx.c2p(t, v) for t, v in zip(tau[::4], pt[::4])])
        pts = [bx.c2p(tau[0], 0)] + [bx.c2p(t, v) for t, v in zip(tau[::4], pt[::4])] + [bx.c2p(tau[::4][-1], 0)]
        self.area = Polygon(*pts, stroke_width=0, fill_color=S.POST, fill_opacity=0.25)
        self.raw = VGroup()
        if y is not None:
            self.raw = VGroup(*[Dot(ax.c2p(tau_max, v), radius=0.06, color=cols[j]).shift(RIGHT * 0.0)
                                for j, v in enumerate(np.asarray(y, float)) if y_range[0] <= v <= y_range[1]])
        self._tau, self._cm, self._cols = tau, cm, cols
        self.add(self.top, self.bottom, self.curves, self.names, self.area, self.density)

    def line_at(self, t: float) -> VGroup:
        ax, bx = self.top.ax, self.bottom.ax
        top = ax.c2p(t, bounds(ax)[3])
        bot = bx.c2p(t, 0)
        return DashedLine(bot, top, color=GREY_A, stroke_width=1.8)

    def dots_at(self, t: float) -> VGroup:
        ax = self.top.ax
        return VGroup(*[Dot(ax.c2p(t, float(np.interp(t, self._tau, self._cm[:, j]))), radius=0.07, color=self._cols[j])
                        for j in range(self._cm.shape[1])])


def _spread(labels: VGroup, gap: float) -> None:
    """Nudge a column of labels apart vertically so that neighbours are at least ``gap`` apart (keeps their order)."""
    order = sorted(range(len(labels)), key=lambda k: labels[k].get_center()[1])
    ys = [labels[k].get_center()[1] for k in order]
    for i in range(1, len(ys)):
        ys[i] = max(ys[i], ys[i - 1] + gap)
    shift = (np.mean([labels[k].get_center()[1] for k in order]) - np.mean(ys))
    for k, yv in zip(order, ys):
        labels[k].set_y(yv + shift)


class PuckSurface(VGroup):
    """Hamiltonian Monte Carlo's picture (Part 27): the potential energy U(x, y) = -log density drawn as a wireframe
    bowl in an oblique projection (azimuth ``az``, elevation ``el``), with ``to_screen(x, y)`` placing a point on the
    surface, so that a puck's leapfrog path can be drawn sliding over it.  Heights are capped at ``z_cap``; lines
    farther from the viewer are drawn fainter."""

    def __init__(self, U, x_range, y_range, n: int = 18, width: float = 7.0, height: float = 4.2, z_cap: float = None,
                 az: float = 0.65, el: float = 0.55, center=ORIGIN, color=None, stroke_width: float = 1.4):
        super().__init__()
        self.U = U
        self.x0, self.x1 = x_range
        self.y0, self.y1 = y_range
        xs = np.linspace(self.x0, self.x1, 60)
        ys = np.linspace(self.y0, self.y1, 60)
        X, Y = np.meshgrid(xs, ys)
        Z = np.asarray(U(X, Y), float)
        self.z_min = float(Z.min())
        self.z_cap = float(np.quantile(Z, 0.9)) if z_cap is None else float(z_cap)
        self.az, self.el = az, el
        # normalized coordinates in [-1, 1]
        self._raw = lambda x, y, z: self._project(2 * (x - self.x0) / (self.x1 - self.x0) - 1,
                                                  2 * (y - self.y0) / (self.y1 - self.y0) - 1,
                                                  (min(z, self.z_cap) - self.z_min) / (self.z_cap - self.z_min))
        corners = [self._raw(a, b, c) for a in (self.x0, self.x1) for b in (self.y0, self.y1) for c in (self.z_min, self.z_cap)]
        cx = [p[0] for p in corners]
        cy = [p[1] for p in corners]
        self._sx = width / (max(cx) - min(cx))
        self._sy = height / (max(cy) - min(cy))
        self._off = np.array([(max(cx) + min(cx)) / 2, (max(cy) + min(cy)) / 2])
        self._c = np.asarray(center, float)
        col = color or S.EST
        self.wire = VGroup()
        for k, xv in enumerate(np.linspace(self.x0, self.x1, n)):
            pts = [self.to_screen(xv, yv) for yv in np.linspace(self.y0, self.y1, 50)]
            m = VMobject(stroke_color=col, stroke_width=stroke_width, stroke_opacity=0.25 + 0.5 * k / (n - 1))
            m.set_points_as_corners(pts)
            self.wire.add(m)
        for k, yv in enumerate(np.linspace(self.y0, self.y1, n)):
            pts = [self.to_screen(xv, yv) for xv in np.linspace(self.x0, self.x1, 50)]
            m = VMobject(stroke_color=col, stroke_width=stroke_width, stroke_opacity=0.75 - 0.5 * k / (n - 1))
            m.set_points_as_corners(pts)
            self.wire.add(m)
        self.add(self.wire)

    def _project(self, x, y, z):
        ca, sa = np.cos(self.az), np.sin(self.az)
        X = x * ca - y * sa
        depth = x * sa + y * ca
        return np.array([X, depth * np.sin(self.el) + z * 1.6 * np.cos(self.el)])

    def to_screen(self, x, y, lift: float = 0.0):
        z = float(self.U(np.asarray(x, float), np.asarray(y, float)))
        p = self._raw(x, y, z)
        return np.array([(p[0] - self._off[0]) * self._sx + self._c[0], (p[1] - self._off[1]) * self._sy + self._c[1] + lift, 0.0])

    def path(self, points, color=None, stroke_width: float = 3.0) -> VMobject:
        m = VMobject(stroke_color=color or S.ACCENT, stroke_width=stroke_width)
        m.set_points_as_corners([self.to_screen(a, b, 0.03) for a, b in points])
        return m

    def puck(self, x, y, color=None, radius: float = 0.1) -> Dot:
        return Dot(self.to_screen(x, y, 0.05), radius=radius, color=color or S.ACCENT)


class CriterionBench(VGroup):
    """The model-selection bench (Part 28): one column per candidate model, a stacked bar of misfit (the deviance
    above the best model's) and penalty, a dot at their sum, and the winner ringed.  ``bars(penalty)`` rebuilds the
    stack for another penalty (AIC's 2k, BIC's k log n), so the change of winner can be animated."""

    def __init__(self, misfit, k, labels, penalty_per_k: float = 2.0, width: float = 8.0, height: float = 4.0,
                 center=ORIGIN, y_max: float | None = None, colors=None, font_size=20):
        super().__init__()
        from explainer.ai.viz import axes
        from explainer.analysis import label

        self.misfit = np.asarray(misfit, float) - np.min(misfit)
        self.k = np.asarray(k, float)
        n = len(self.misfit)
        top = y_max if y_max is not None else float(np.max(self.misfit + self.k * penalty_per_k)) * 1.05
        self.axes_ = axes([-0.6, n - 0.4], [0, top], x_length=width, y_length=height, xlabel=r"", ylabel=r"criterion",
                          xticks=[], yticks=[], font_size=font_size, center=center)
        self.ax = self.axes_.ax
        self.cols = colors or {"misfit": S.EST, "penalty": S.RESID, "total": S.ACCENT}
        self.names = VGroup(*[label(t, font_size=font_size, color=GREY_A).next_to(self.ax.c2p(i, 0), DOWN, buff=0.15)
                              for i, t in enumerate(labels)])
        self.add(self.axes_, self.names)
        self.stack = self.bars(penalty_per_k)
        self.add(self.stack)

    def bars(self, penalty_per_k: float) -> VGroup:
        ax = self.ax
        w = (ax.c2p(1, 0)[0] - ax.c2p(0, 0)[0]) * 0.55
        top_y = bounds(ax)[3]
        g = VGroup()
        fit = VGroup()
        pen = VGroup()
        dots = VGroup()
        totals = self.misfit + self.k * penalty_per_k
        for i, (m, t) in enumerate(zip(self.misfit, totals)):
            m_c, t_c = min(m, top_y), min(t, top_y)
            y0, y1, y2 = ax.c2p(i, 0)[1], ax.c2p(i, m_c)[1], ax.c2p(i, t_c)[1]
            fit.add(Rectangle(width=w, height=max(y1 - y0, 1e-3), stroke_width=0, fill_color=self.cols["misfit"], fill_opacity=0.8)
                    .move_to([ax.c2p(i, 0)[0], (y0 + y1) / 2, 0]))
            pen.add(Rectangle(width=w, height=max(y2 - y1, 1e-3), stroke_width=0, fill_color=self.cols["penalty"], fill_opacity=0.7)
                    .move_to([ax.c2p(i, 0)[0], (y1 + y2) / 2, 0]))
            dots.add(Dot(ax.c2p(i, t_c), radius=0.06, color=self.cols["total"]))
        best = int(np.argmin(totals))
        ring = Circle(radius=0.16, stroke_color=self.cols["total"], stroke_width=3).move_to(dots[best])
        g.fit, g.pen, g.dots, g.ring, g.best = fit, pen, dots, ring, best
        g.add(fit, pen, dots, ring)
        return g


class SplineSpectrum(VGroup):
    """A smoother's spectrum (Part 29): the Demmler--Reinsch basis of a smoothing spline, its first ``k`` eigenvectors
    drawn as small curves stacked down the left (smoothest at the top), and on the right one bar per eigenvector
    showing the shrinkage factor 1/(1 + lam d_j) the spline applies to that component.  ``bars(lam)`` rebuilds the bars
    for another lambda, so the dial can be turned; the null-space components (constants, lines) always pass at 1."""

    def __init__(self, t, U, d, lam: float, k: int = 8, width: float = 9.0, height: float = 5.2, center=ORIGIN,
                 curve_color=None, bar_color=None, font_size=20):
        super().__init__()
        from explainer.analysis import label

        t = np.asarray(t, float)
        self.d = np.asarray(d, float)
        self.k = k
        self.U = np.asarray(U, float)
        c = np.asarray(center, float)
        row_h = height / k
        cw = width * 0.55
        self.curves = VGroup()
        self.tags = VGroup()
        t0, t1 = t.min(), t.max()
        for j in range(k):
            u = self.U[:, j]
            u = u / (np.max(np.abs(u)) + 1e-12)
            y_mid = c[1] + height / 2 - (j + 0.5) * row_h
            x = c[0] - width / 2 + (t - t0) / (t1 - t0) * cw
            pts = [[a, y_mid + 0.38 * row_h * b, 0] for a, b in zip(x, u)]
            m = VMobject(stroke_color=curve_color or S.FIT, stroke_width=2.5).set_points_as_corners(pts)
            self.curves.add(m)
            self.tags.add(label(rf"$u_{{{j + 1}}}$", font_size=font_size, color=GREY_B).next_to([x[0], y_mid, 0], LEFT, buff=0.15))
        self.bar_x0 = c[0] - width / 2 + cw + 0.6
        self.bar_w = width - cw - 0.8
        self.row_h = row_h
        self.top = c[1] + height / 2
        self.bar_color = bar_color or S.ACCENT
        self.frame = VGroup(*[Line([self.bar_x0, self.top - (j + 0.5) * row_h, 0],
                                   [self.bar_x0 + self.bar_w, self.top - (j + 0.5) * row_h, 0], color=GREY_D, stroke_width=1)
                              for j in range(k)])
        self.head = VGroup(label(r"basis function", font_size=font_size, color=GREY_A).next_to([c[0] - width / 2 + cw / 2, self.top, 0], UP, buff=0.12),
                           label(r"kept: \ $1/(1 + \lambda d_j)$", font_size=font_size, color=GREY_A).next_to([self.bar_x0 + self.bar_w / 2, self.top, 0], UP, buff=0.12))
        self.add(self.head, self.tags, self.curves, self.frame)
        self.stack = self.bars(lam)
        self.add(self.stack)

    def bars(self, lam: float) -> VGroup:
        g = VGroup()
        for j in range(self.k):
            s = 1 / (1 + lam * max(self.d[j], 0.0))
            y = self.top - (j + 0.5) * self.row_h
            r = Rectangle(width=max(self.bar_w * s, 1e-3), height=self.row_h * 0.5, stroke_width=0, fill_color=self.bar_color,
                          fill_opacity=0.85)
            r.move_to([self.bar_x0 + self.bar_w * s / 2, y, 0])
            g.add(r)
        return g


class EstimatorRail(VGroup):
    """The estimator rail (Part 30): a sample as dots on a number line, and below it one marker per location
    estimator (mean, median, Hodges--Lehmann, Huber, ...), each on its own track.  One observation follows the tracker
    ``z``; every marker is recomputed each frame, so dragging a point out to sea shows which estimators follow it.
    ``estimators``: list of (name, function, colour).  Call ``stop()`` before clearing the scene."""

    def __init__(self, x, estimators, x_range, index: int = -1, width: float = 10.0, center=ORIGIN, track_gap=0.42,
                 font_size=20, dot_color=None):
        super().__init__()
        from explainer.analysis import label

        self.x = np.asarray(x, float).copy()
        self.i = index % len(self.x)
        self.z = ValueTracker(self.x[self.i])
        self.x0, self.x1 = x_range
        self.rail_w = width
        c = np.asarray(center, float)
        self.left = c[0] - width / 2
        self.y_data = c[1] + track_gap * (len(estimators) + 1) / 2
        self.axis = NumberLine(x_range=[self.x0, self.x1, (self.x1 - self.x0) / 10], length=width, include_numbers=False,
                               color=GREY_C).move_to([c[0], self.y_data - 0.25, 0])
        self.ticks = VGroup(*[label(f"{v:g}", font_size=font_size - 4, color=GREY_B).next_to(self.axis.n2p(v), DOWN, buff=0.1)
                              for v in np.linspace(self.x0, self.x1, 6)])
        col = dot_color or S.DATA
        jitter = np.random.default_rng(3).uniform(-0.08, 0.08, len(self.x))
        self.others = VGroup(*[Dot([self.X(v), self.y_data + jitter[k], 0], radius=0.05, color=col, fill_opacity=0.7)
                               for k, v in enumerate(self.x) if k != self.i])
        self.probe = always_redraw(lambda: Dot([self.X(self.z.get_value()), self.y_data, 0], radius=0.09, color=S.ACCENT))
        self.tracks, self.markers, self.names = VGroup(), VGroup(), VGroup()
        self.estimators = estimators
        for k, (name, fn, colr) in enumerate(estimators):
            y = self.y_data - 0.75 - k * track_gap
            self.tracks.add(Line([self.left, y, 0], [self.left + self.rail_w, y, 0], color=GREY_D, stroke_width=1))
            self.names.add(label(name, font_size=font_size, color=colr).next_to([self.left, y, 0], LEFT, buff=0.2))
            self.markers.add(always_redraw(lambda fn=fn, y=y, colr=colr: Triangle(color=colr, fill_opacity=1, stroke_width=0)
                                           .scale(0.09).rotate(PI).move_to([self.X(fn(self.data())), y, 0])))
        self.add(self.axis, self.ticks, self.others, self.probe, self.tracks, self.names, self.markers)

    def X(self, v):
        v = min(max(v, self.x0), self.x1)
        return self.left + (v - self.x0) / (self.x1 - self.x0) * self.rail_w

    def data(self):
        y = self.x.copy()
        y[self.i] = self.z.get_value()
        return y

    def drag(self, value, run_time=3.0):
        return self.z.animate(run_time=run_time).set_value(value)

    def stop(self):
        for m in [self.probe, *self.markers]:
            m.clear_updaters()


class DistanceMap(VGroup):
    """The map from distances (Part 31): true positions as hollow rings and, after classical MDS and a Procrustes
    alignment, the rebuilt positions as dots joined to their rings by residual segments.  ``truth``, ``rebuilt``,
    ``residuals`` and ``roads`` (optional edge list) are the parts; ``labels`` names chosen points.  Coordinates are
    data units mapped into a box of the given width centred at ``center`` (aspect kept)."""

    def __init__(self, truth, rebuilt, width: float = 7.0, height: float = 5.0, center=ORIGIN, edges=None, names=None,
                 label_idx=(), truth_color=None, dot_color=None, font_size=18, dot_radius=0.05, sizes=None):
        super().__init__()
        from explainer.analysis import label

        T, Rb = np.asarray(truth, float), np.asarray(rebuilt, float)
        allp = np.vstack([T, Rb])
        lo, hi = allp.min(0), allp.max(0)
        s = min(width / (hi[0] - lo[0] + 1e-9), height / (hi[1] - lo[1] + 1e-9))
        mid = (lo + hi) / 2
        c = np.asarray(center, float)

        def P(v):
            return np.array([c[0] + s * (v[0] - mid[0]), c[1] + s * (v[1] - mid[1]), 0.0])

        self.P = P
        rad = (np.full(len(T), dot_radius) if sizes is None else dot_radius * (0.6 + 2.5 * np.sqrt(np.asarray(sizes) / np.max(sizes))))
        self.roads = VGroup(*[Line(P(T[i]), P(T[j]), color=GREY_D, stroke_width=1) for i, j in (edges or [])])
        self.truth = VGroup(*[Circle(radius=r * 1.6, stroke_color=truth_color or S.TRUTH, stroke_width=1.5).move_to(P(v))
                              for v, r in zip(T, rad)])
        self.rebuilt = VGroup(*[Dot(P(v), radius=r, color=dot_color or S.EST) for v, r in zip(Rb, rad)])
        self.residuals = VGroup(*[Line(P(a), P(b), color=S.RESID, stroke_width=1.2) for a, b in zip(T, Rb)])
        self.labels = VGroup(*[label(names[i], font_size=font_size, color=GREY_A).next_to(P(Rb[i]), UP, buff=0.06)
                               for i in label_idx]) if names is not None else VGroup()
        self.add(self.roads, self.truth, self.residuals, self.rebuilt, self.labels)


class PhantomPanel(Group):
    """The phantom (Part 32): an image (a 2-D array, such as the Shepp--Logan phantom or a reconstruction of it) drawn
    as greyscale pixels at nearest-neighbour resampling, in a thin frame with a caption.  ``lo``/``hi`` fix the grey
    scale so that panels can be compared; ``tint`` maps the scale from the background to a colour instead of white.
    ``image``, ``frame`` and ``caption`` are the parts; ``panel_for(arr)`` builds a matching image for a Transform."""

    def __init__(self, arr, size: float = 2.6, caption: str | None = None, lo: float | None = None,
                 hi: float | None = None, tint=None, font_size: int = 20, center=ORIGIN, frame_color=None,
                 caption_color=None):
        super().__init__()
        from explainer.analysis import label

        self.size, self.lo, self.hi, self.tint = size, lo, hi, tint
        self.image = self.panel_for(arr)
        self.image.move_to(center)
        self.frame = SurroundingRectangle(self.image, buff=0.03, stroke_color=frame_color or GREY_D, stroke_width=1.5)
        self.add(self.image, self.frame)
        self.caption = VGroup()
        if caption:
            self.caption = label(caption, font_size=font_size, color=caption_color or GREY_A).next_to(self.frame, DOWN, buff=0.15)
            self.add(self.caption)

    def panel_for(self, arr) -> ImageMobject:
        a = np.asarray(arr, float)
        lo = float(np.min(a)) if self.lo is None else self.lo
        hi = float(np.max(a)) if self.hi is None else self.hi
        v = np.clip((a - lo) / max(hi - lo, 1e-12), 0, 1)
        bg = np.array([0x0b, 0x0e, 0x13], float) / 255
        top = np.array(ManimColor(self.tint).to_rgb()) if self.tint is not None else np.ones(3)
        rgb = bg[None, None, :] * (1 - v[..., None]) + top[None, None, :] * v[..., None]
        img = ImageMobject((rgb * 255).astype(np.uint8))
        img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
        img.height = self.size
        if hasattr(self, "image"):
            img.move_to(self.image)
        return img


class PValueSea(VGroup):
    """The p-value sea (Part 33): many p-values sorted against their rank, on axes zoomed to the smallest ranks,
    with the Benjamini--Hochberg line p = q i / m sweeping through them.  ``bh_line(q)`` draws the line (clipped to
    the box); ``k(q)`` is the number BH rejects; ``mark(q, color)`` returns the dots BH rejects, recoloured;
    ``grid(...)`` (a static helper) draws every p-value as a cell of a grid, brighter for smaller p."""

    def __init__(self, p, width: float = 7.0, height: float = 4.6, center=ORIGIN, ranks: int | None = None,
                 pmax: float | None = None, dot_color=None, dot_radius: float = 0.03, font_size: int = 20):
        super().__init__()
        from explainer.analysis import label

        self.p = np.sort(np.asarray(p, float))
        self.m = len(self.p)
        self.R = ranks or self.m
        self.pmax = pmax if pmax is not None else float(self.p[self.R - 1])
        self.w, self.h = width, height
        self.c = np.asarray(center, float)
        o = self.c + np.array([-width / 2, -height / 2, 0])
        self.origin = o
        self.axes_ = VGroup(Line(o, o + RIGHT * width, color=GREY_C, stroke_width=2),
                            Line(o, o + UP * height, color=GREY_C, stroke_width=2))
        self.xlabel = label(rf"rank $i$ \ (of {self.m:,})", font_size=font_size, color=GREY_A).next_to(self.axes_[0], DOWN, buff=0.15)
        self.ylabel = label(r"$p_{(i)}$", font_size=font_size, color=GREY_A).next_to(self.axes_[1], UP, buff=0.12)
        self.ticks = VGroup(
            label(r"0", font_size=font_size - 2, color=GREY_B).next_to(o, DL, buff=0.06),
            label(rf"{self.R:,}", font_size=font_size - 2, color=GREY_B).next_to(o + RIGHT * width, DOWN, buff=0.1),
            label(rf"{self.pmax:.3g}", font_size=font_size - 2, color=GREY_B).next_to(o + UP * height, LEFT, buff=0.1))
        idx = np.arange(self.R)
        if self.R > 1500:
            idx = np.unique(np.r_[np.arange(300), np.linspace(0, self.R - 1, 1200).astype(int)])
        self.idx = idx
        self.dots = VGroup(*[Dot(self.P(i + 1, min(self.p[i], self.pmax)), radius=dot_radius, color=dot_color or GREY_B)
                             for i in idx])
        self.add(self.axes_, self.xlabel, self.ylabel, self.ticks, self.dots)

    def P(self, rank, pv) -> np.ndarray:
        return self.origin + np.array([self.w * rank / self.R, self.h * pv / self.pmax, 0.0])

    def k(self, q: float) -> int:
        ok = np.flatnonzero(self.p <= q * np.arange(1, self.m + 1) / self.m)
        return int(ok.max() + 1) if len(ok) else 0

    def bh_line(self, q: float, color=None, stroke_width: float = 3) -> Line:
        r_end = min(self.R, self.pmax * self.m / q)
        return Line(self.P(0, 0), self.P(r_end, q * r_end / self.m), color=color or S.ACCENT, stroke_width=stroke_width)

    def mark(self, q: float, color=None) -> VGroup:
        k = self.k(q)
        return VGroup(*[d.copy().set_color(color or S.ACCENT).scale(1.4) for d, i in zip(self.dots, self.idx) if i < k])

    @staticmethod
    def grid(p, cols: int, cell: float = 0.06, center=ORIGIN, lo: float = 1e-6) -> VGroup:
        p = np.asarray(p, float)
        g = VGroup()
        rows = int(np.ceil(len(p) / cols))
        for i, v in enumerate(p):
            r, c = divmod(i, cols)
            t = float(np.clip(-np.log10(max(v, lo)) / -np.log10(lo), 0, 1))
            g.add(Square(cell * 0.9, stroke_width=0, fill_opacity=1,
                         fill_color=interpolate_color(ManimColor("#141a26"), ManimColor(S.ACCENT), t ** 0.6))
                  .move_to(np.asarray(center) + np.array([(c - cols / 2) * cell, (rows / 2 - r) * cell, 0])))
        return g


class ScoreLadder(VGroup):
    """The score ladder (Part 34): n calibration scores, sorted, as a row of bars; the conformal rank
    k = ceil((n + 1)(1 - alpha)) picked out, and the threshold q drawn across the ladder.  ``new_slot(s)`` is where a
    new score s would land among the n + 1 (its rank, which is uniform under exchangeability); ``threshold(color)``
    the dashed line at q; ``kept()`` the bars at or below q, recoloured; ``rung(k)`` one bar."""

    def __init__(self, scores, alpha: float = 0.1, width: float = 8.0, height: float = 3.2, center=ORIGIN,
                 smax: float | None = None, bar_color=None, font_size: int = 20, show_ranks: bool = True):
        super().__init__()
        from explainer.analysis import label

        self.s = np.sort(np.asarray(scores, float))
        self.n = len(self.s)
        self.alpha = alpha
        self.kq = int(np.ceil((self.n + 1) * (1 - alpha)))
        self.q = float(self.s[self.kq - 1]) if self.kq <= self.n else float("inf")
        self.smax = smax if smax is not None else float(self.s[-1]) * 1.08
        self.w, self.h = width, height
        self.c = np.asarray(center, float)
        self.origin = self.c + np.array([-width / 2, -height / 2, 0])
        self.slot = width / (self.n + 1)
        self.base = Line(self.origin, self.origin + RIGHT * width, color=GREY_C, stroke_width=2)
        self.bars = VGroup(*[self._bar(i, v, bar_color or GREY_B) for i, v in enumerate(self.s)])
        self.add(self.base, self.bars)
        self.ranks = VGroup()
        if show_ranks and self.n <= 40:
            for i in range(self.n):
                self.ranks.add(label(rf"{i + 1}", font_size=font_size - 4, color=GREY_B)
                               .next_to(self.base.point_from_proportion((i + 0.5) / (self.n + 1)), DOWN, buff=0.1))
            self.add(self.ranks)

    def x_of(self, i: float) -> float:
        return float(self.origin[0] + self.slot * (i + 0.5))

    def y_of(self, v: float) -> float:
        return float(self.origin[1] + self.h * min(v, self.smax) / self.smax)

    def _bar(self, i, v, color):
        h = max(1e-3, self.h * min(v, self.smax) / self.smax)
        return Rectangle(width=self.slot * 0.72, height=h, stroke_width=0, fill_color=color, fill_opacity=0.85) \
            .move_to([self.x_of(i), self.origin[1], 0], aligned_edge=DOWN)

    def rung(self, k: int | None = None, color=None) -> Rectangle:
        k = self.kq if k is None else k
        return self.bars[k - 1].copy().set_fill(color or S.ACCENT, 1.0)

    def kept(self, color=None) -> VGroup:
        return VGroup(*[b.copy().set_fill(color or S.KEPT, 0.9) for b, v in zip(self.bars, self.s) if v <= self.q])

    def threshold(self, color=None, stroke_width: float = 3) -> DashedLine:
        y = self.y_of(self.q) if np.isfinite(self.q) else self.origin[1] + self.h
        return DashedLine([self.origin[0], y, 0], [self.origin[0] + self.w, y, 0], color=color or S.ACCENT,
                          stroke_width=stroke_width, dash_length=0.12)

    def rank_of(self, s_new: float) -> int:
        """Where a new score lands: the number of calibration scores below it (0..n)."""
        return int(np.sum(self.s < s_new))

    def new_slot(self, s_new: float, color=None) -> Rectangle:
        """A bar for a new score, placed in the gap it falls into (between bar r and bar r + 1)."""
        r = self.rank_of(s_new)
        h = max(1e-3, self.h * min(s_new, self.smax) / self.smax)
        return Rectangle(width=self.slot * 0.28, height=h, stroke_width=0, fill_color=color or S.TREAT,
                         fill_opacity=0.95).move_to([self.origin[0] + self.slot * r, self.origin[1], 0], aligned_edge=DOWN)


class ScienceTable(VGroup):
    """The science table (Part 35): one row per unit, with both potential outcomes Y(0) and Y(1) and the unit's own
    effect tau = Y(1) - Y(0), which the World can show and no real study can.  ``mask(z)`` returns the grey '?'
    patches that an assignment z puts over the outcomes it hides (Holland's fundamental problem): Y(1) for units
    with z = 0, Y(0) for z = 1, and every tau; ``observed(z)`` the revealed cells, recoloured; ``column(name)`` one
    column ('y0', 'y1', 'tau' or an extra column's name)."""

    def __init__(self, y0, y1, labels=None, extra=None, center=ORIGIN, font_size: int = 24, fmt: str = "{:.0f}",
                 col_buff: float = 0.55, row_buff: float = 0.16, colors=None):
        super().__init__()
        from explainer.analysis import label

        self.y0, self.y1 = np.asarray(y0, float), np.asarray(y1, float)
        n = len(self.y0)
        labels = labels or [rf"{i + 1}" for i in range(n)]
        extra = extra or []
        colors = colors or {"y0": S.CTRL, "y1": S.TREAT, "tau": S.ACCENT}
        heads = [r"unit"] + [e[0] for e in extra] + [r"$Y_i(0)$", r"$Y_i(1)$", r"$\tau_i$"]
        self.names = ["unit"] + [e[0] for e in extra] + ["y0", "y1", "tau"]
        rows = [heads]
        for i in range(n):
            r = [labels[i]] + [e[1][i] if isinstance(e[1][i], str) else fmt.format(e[1][i]) for e in extra]
            r += [fmt.format(self.y0[i]), fmt.format(self.y1[i]), ("{:+.0f}" if fmt == "{:.0f}" else "{:+.1f}").format(self.y1[i] - self.y0[i])]
            rows.append(r)
        cells = [[label(c, font_size=font_size) for c in r] for r in rows]
        ncol = len(heads)
        widths = [max(cells[i][j].width for i in range(len(cells))) for j in range(ncol)]
        y = 0.0
        self.rows = VGroup()
        for i, r in enumerate(cells):
            row = VGroup()
            x = 0.0
            for j, c in enumerate(r):
                c.move_to([x + widths[j] / 2, y, 0])
                if i == 0:
                    c.set_color(GREY_A)
                elif self.names[j] in colors:
                    c.set_color(colors[self.names[j]])
                row.add(c)
                x += widths[j] + col_buff
            self.rows.add(row)
            y -= max(c.height for c in r) + row_buff
        self.add(self.rows)
        self.move_to(center)
        self.cell_w = [w + col_buff * 0.6 for w in widths]

    def column(self, name: str) -> VGroup:
        j = self.names.index(name)
        return VGroup(*[r[j] for r in self.rows])

    def _patch(self, cell, j, color=GREY_D):
        from explainer.analysis import label

        box = Rectangle(width=self.cell_w[j], height=cell.height + 0.12, stroke_width=0, fill_color=color, fill_opacity=0.95)
        box.move_to(cell)
        q = label(r"?", font_size=22, color=GREY_B).move_to(box)
        return VGroup(box, q)

    def mask(self, z) -> VGroup:
        z = np.asarray(z, bool)
        j0, j1, jt = self.names.index("y0"), self.names.index("y1"), self.names.index("tau")
        g = VGroup()
        for i, zi in enumerate(z):
            r = self.rows[i + 1]
            g.add(self._patch(r[j0] if zi else r[j1], j0 if zi else j1))
            g.add(self._patch(r[jt], jt))
        return g

    def observed(self, z, color=None) -> VGroup:
        z = np.asarray(z, bool)
        j0, j1 = self.names.index("y0"), self.names.index("y1")
        return VGroup(*[self.rows[i + 1][j1 if zi else j0].copy().set_color(color or WHITE) for i, zi in enumerate(z)])


class CausalGraph(VGroup):
    """A causal diagram (Part 36): named nodes at given positions, arrows for direct causes, and the kit's DAG for
    d-separation.  ``path(nodes, color)`` returns the arrows along a path, recoloured (a back-door path, say);
    ``condition(names)`` the boxes that mark conditioned-on nodes; ``node(name)`` one node; ``open(path, Z)`` whether a
    path is open given Z."""

    def __init__(self, positions: dict, edges, center=ORIGIN, scale: float = 1.0, font_size: int = 26, radius: float = 0.36,
                 colors: dict | None = None, labels: dict | None = None):
        super().__init__()
        from explainer.analysis import label
        from explainer.stats.kit.causal import DAG

        self.dag = DAG(edges)
        self.edges = [tuple(e) for e in edges]
        colors = colors or {}
        labels = labels or {}
        c = np.asarray(center, float)
        self.pos = {k: c + scale * np.array([v[0], v[1], 0.0]) for k, v in positions.items()}
        self.radius = radius
        self.nodes = {}
        for k, p in self.pos.items():
            col = colors.get(k, GREY_A)
            circ = Circle(radius=radius, stroke_color=col, stroke_width=3, fill_color="#141a26", fill_opacity=1).move_to(p)
            t = label(labels.get(k, rf"${k}$" if len(k) <= 2 else k), font_size=font_size, color=col).move_to(p)
            if t.width > 1.7 * radius:
                t.width = 1.7 * radius
            self.nodes[k] = VGroup(circ, t)
        self.arrows = {}
        for a, b in self.edges:
            pa, pb = self.pos[a], self.pos[b]
            d = (pb - pa) / np.linalg.norm(pb - pa)
            self.arrows[(a, b)] = Arrow(pa + d * radius, pb - d * radius, buff=0.02, color=GREY_B, stroke_width=3,
                                        max_tip_length_to_length_ratio=0.18)
        self.add(*self.arrows.values(), *self.nodes.values())

    def node(self, name):
        return self.nodes[name]

    def path(self, nodes, color=None, stroke_width: float = 6) -> VGroup:
        g = VGroup()
        for a, b in zip(nodes[:-1], nodes[1:]):
            arr = self.arrows.get((a, b)) or self.arrows.get((b, a))
            if arr is not None:
                g.add(arr.copy().set_color(color or S.ACCENT).set_stroke(width=stroke_width))
        return g

    def condition(self, names, color=None) -> VGroup:
        return VGroup(*[Square(side_length=2.5 * self.radius, stroke_color=color or S.KEPT, stroke_width=3)
                        .move_to(self.pos[n]) for n in names])

    def open(self, path, Z=()) -> bool:
        return self.dag.is_open(path, Z)


class CutoffLens(VGroup):
    """The regression-discontinuity lens (Part 37) on axes ``ax``: binned means of the outcome against the running
    variable (left of the cutoff in ``left_color``, right in ``right_color``) and the cutoff as a dashed line.
    ``window(h)`` shades the kernel's reach [c - h, c + h] with the triangular weights drawn along the floor;
    ``fit(coef, h, side)`` draws a local polynomial (coefficients in powers of (x - c)/h, as statkit.quasi returns them)
    on one side; ``jump(a_left, a_right)`` the gap between the two intercepts at c, with a label."""

    def __init__(self, ax, mids, means, c: float, left_color=None, right_color=None, radius: float = 0.05,
                 opacity: float = 0.85):
        super().__init__()
        self.ax, self.c = ax, float(c)
        self.lc, self.rc = left_color or S.CTRL, right_color or S.TREAT
        mids, means = np.asarray(mids, float), np.asarray(means, float)
        ok = np.isfinite(means)
        self.dots = VGroup(*[Dot(ax.c2p(x, y), radius=radius, color=self.lc if x < c else self.rc, fill_opacity=opacity)
                             for x, y in zip(mids[ok], means[ok])])
        self._y0 = bounds(ax)[2:]
        self.line = DashedLine(ax.c2p(c, self._y0[0]), ax.c2p(c, self._y0[1]), color=GREY_B, stroke_width=2)
        self.add(self.line, self.dots)

    def window(self, h: float, color=None, opacity: float = 0.12) -> VGroup:
        col = color or S.ACCENT
        y0, y1 = self._y0
        x0, x1 = bounds(self.ax)[:2]
        a, b = self.ax.c2p(max(self.c - h, x0), y0), self.ax.c2p(min(self.c + h, x1), y1)
        box = Rectangle(width=b[0] - a[0], height=b[1] - a[1], stroke_width=0, fill_color=col, fill_opacity=opacity)
        box.move_to([(a[0] + b[0]) / 2, (a[1] + b[1]) / 2, 0])
        peak = 0.18 * (b[1] - a[1])
        us = np.linspace(max(self.c - h, x0), min(self.c + h, x1), 41)
        pts = [self.ax.c2p(u, y0) + np.array([0, peak * max(0.0, 1 - abs(u - self.c) / h), 0]) for u in us]
        tri = Polygon(self.ax.c2p(us[0], y0), *pts, self.ax.c2p(us[-1], y0), stroke_color=col, stroke_width=2,
                      fill_color=col, fill_opacity=0.35)
        return VGroup(box, tri)

    def fit(self, coef, h: float, side: str = "right", color=None, stroke_width: float = 4, n: int = 60):
        coef = np.asarray(coef, float)
        x0, x1 = bounds(self.ax)[:2]
        xs = np.linspace(self.c, min(self.c + h, x1), n) if side == "right" else np.linspace(max(self.c - h, x0), self.c, n)
        u = (xs - self.c) / h
        ys = sum(cf * u ** k for k, cf in enumerate(coef))
        y0, y1 = self._y0
        keep = (ys >= y0) & (ys <= y1)
        m = VMobject(stroke_color=color or (self.rc if side == "right" else self.lc), stroke_width=stroke_width)
        m.set_points_smoothly([self.ax.c2p(a, b) for a, b in zip(xs[keep], ys[keep])])
        return m

    def jump(self, a_left: float, a_right: float, text: str | None = None, color=None, font_size: int = 22):
        from explainer.analysis import label

        col = color or S.ACCENT
        p, q = self.ax.c2p(self.c, a_left), self.ax.c2p(self.c, a_right)
        arr = DoubleArrow(p, q, buff=0, color=col, stroke_width=4, tip_length=0.14, max_tip_length_to_length_ratio=0.4)
        g = VGroup(Dot(p, radius=0.07, color=self.lc), Dot(q, radius=0.07, color=self.rc), arr)
        if text:
            g.add(label(text, font_size=font_size, color=col).next_to(arr, RIGHT, buff=0.15))
        return g


class KalmanEllipses(VGroup):
    """The Kalman filter as moving Gaussian ellipses (Part 38), on axes ``ax`` whose x and y are two state coordinates
    (position and velocity, say).  ``ellipse(m, P)`` is the k-sigma ellipse of N(m, P) (filled, outlined);
    ``observation(y, r, coord)`` the band y +- k sqrt(r) in one coordinate, what a measurement of that coordinate says;
    ``arrow(m_from, m_to)`` the move of the mean."""

    def __init__(self, ax, k: float = 2.0):
        super().__init__()
        self.ax, self.k = ax, k

    def ellipse(self, m, P, color=None, opacity: float = 0.18, stroke_width: float = 2.5, n: int = 72) -> VMobject:
        m = np.asarray(m, float)
        P = np.asarray(P, float)
        L = np.linalg.cholesky(P + 1e-12 * np.eye(2))
        th = np.linspace(0, 2 * np.pi, n, endpoint=False)
        pts = m[:, None] + self.k * L @ np.vstack([np.cos(th), np.sin(th)])
        x0, x1, y0, y1 = bounds(self.ax)
        pts[0] = np.clip(pts[0], x0, x1)
        pts[1] = np.clip(pts[1], y0, y1)
        col = color or S.EST
        return Polygon(*[self.ax.c2p(a, b) for a, b in pts.T], stroke_color=col, stroke_width=stroke_width,
                       fill_color=col, fill_opacity=opacity)

    def observation(self, y: float, r: float, coord: int = 0, color=None, opacity: float = 0.15) -> VMobject:
        x0, x1, y0, y1 = bounds(self.ax)
        h = self.k * np.sqrt(r)
        col = color or S.DATA
        if coord == 0:
            a, b = self.ax.c2p(max(y - h, x0), y0), self.ax.c2p(min(y + h, x1), y1)
        else:
            a, b = self.ax.c2p(x0, max(y - h, y0)), self.ax.c2p(x1, min(y + h, y1))
        r_ = Rectangle(width=abs(b[0] - a[0]), height=abs(b[1] - a[1]), stroke_width=0, fill_color=col, fill_opacity=opacity)
        return r_.move_to([(a[0] + b[0]) / 2, (a[1] + b[1]) / 2, 0])

    def arrow(self, m_from, m_to, color=None) -> Arrow:
        return Arrow(self.ax.c2p(*m_from), self.ax.c2p(*m_to), buff=0.02, color=color or GREY_B, stroke_width=3,
                     max_tip_length_to_length_ratio=0.2)

    def dot(self, m, color=None, radius: float = 0.06) -> Dot:
        return Dot(self.ax.c2p(*m), radius=radius, color=color or S.EST)


class FieldSurface(VGroup):
    """A kriging or GP surface (Part 39): coloured cells at grid nodes (xs, ys, values; flattened), mapped into a box
    of the given ``width`` centred at ``center`` with equal x and y scales.  Colours run through a five-stop
    perceptual ramp (deep blue to yellow).  ``uncertainty(sd)`` returns an overlay that greys cells in proportion to
    their standard deviation; ``dots(px, py)`` places points (stations, samples) in the same coordinates;
    ``key(text)`` a colour bar."""

    RAMP = ["#1b2a6b", "#2c7fb8", "#41b6a4", "#a6d96a", "#fde725"]

    def __init__(self, xs, ys, values, cell: float, width: float = 8.0, center=ORIGIN, lo=None, hi=None,
                 opacity: float = 0.95):
        super().__init__()
        xs, ys, v = (np.asarray(a, float).ravel() for a in (xs, ys, values))
        self.x0, self.x1, self.y0, self.y1 = xs.min() - cell / 2, xs.max() + cell / 2, ys.min() - cell / 2, ys.max() + cell / 2
        self.s = width / (self.x1 - self.x0)
        self.c = np.asarray(center, float)
        self.lo = float(np.nanmin(v)) if lo is None else lo
        self.hi = float(np.nanmax(v)) if hi is None else hi
        self.xs, self.ys, self.cell = xs, ys, cell
        self.cells = VGroup(*[Square(side_length=cell * self.s * 1.02, stroke_width=0, fill_color=self.colour(val),
                                     fill_opacity=opacity).move_to(self.p(x, y)) for x, y, val in zip(xs, ys, v)])
        self.add(self.cells)

    def p(self, x, y):
        cx, cy = (self.x0 + self.x1) / 2, (self.y0 + self.y1) / 2
        return self.c + np.array([(x - cx) * self.s, (y - cy) * self.s, 0.0])

    def colour(self, v):
        t = float(np.clip((v - self.lo) / max(self.hi - self.lo, 1e-12), 0, 1)) * (len(self.RAMP) - 1)
        i = min(int(t), len(self.RAMP) - 2)
        return interpolate_color(ManimColor(self.RAMP[i]), ManimColor(self.RAMP[i + 1]), t - i)

    def uncertainty(self, sd, smax=None, max_opacity: float = 0.75) -> VGroup:
        sd = np.asarray(sd, float).ravel()
        smax = float(np.nanmax(sd)) if smax is None else smax
        return VGroup(*[Square(side_length=self.cell * self.s * 1.02, stroke_width=0, fill_color="#0b0f17",
                               fill_opacity=float(np.clip(s / smax, 0, 1)) * max_opacity).move_to(self.p(x, y))
                        for x, y, s in zip(self.xs, self.ys, sd)])

    def dots(self, px, py, color=WHITE, radius: float = 0.04, opacity: float = 1.0) -> VGroup:
        return VGroup(*[Dot(self.p(x, y), radius=radius, color=color, fill_opacity=opacity) for x, y in zip(px, py)])

    def key(self, text: str = "", width: float = 2.6, font_size: int = 20, fmt="{:.0f}") -> VGroup:
        from explainer.analysis import label

        n = 30
        bar = VGroup(*[Rectangle(width=width / n, height=0.18, stroke_width=0, fill_opacity=1,
                                 fill_color=self.colour(self.lo + (self.hi - self.lo) * (k + 0.5) / n)) for k in range(n)])
        bar.arrange(RIGHT, buff=0)
        a = label(fmt.format(self.lo), font_size=font_size, color=GREY_B).next_to(bar, LEFT, buff=0.12)
        b = label(fmt.format(self.hi), font_size=font_size, color=GREY_B).next_to(bar, RIGHT, buff=0.12)
        g = VGroup(bar, a, b)
        if text:
            g.add(label(text, font_size=font_size, color=GREY_B).next_to(bar, UP, buff=0.1))
        return g


class KMStaircase(VGroup):
    """The Kaplan--Meier staircase (Part 40) on axes ``ax`` (time, survival): ``curve()`` the step function, drawn
    from the KM table; ``ticks()`` the censoring marks on it; ``people(y, x0, x1)`` a row of dots, one per subject in
    order of their times (red: an event; grey: censored), to show the risk set shrinking; ``drop(k)`` the vertical
    piece at the k-th event time with a label of n_k and d_k; ``band(lo, hi)`` a pointwise interval as a shaded
    staircase."""

    def __init__(self, ax, time, event, color=None):
        super().__init__()
        from explainer.stats.kit import survival as SV

        self.ax = ax
        self.time, self.event = np.asarray(time, float), np.asarray(event, int)
        self.km = SV.kaplan_meier(self.time, self.event)
        self.color = color or S.EST
        self.t_end = float(bounds(ax)[1])

    def _steps(self, ys, t0=0.0):
        t = self.km["t"]
        pts = [(t0, 1.0)]
        prev = 1.0
        for tk, s in zip(t, ys):
            pts += [(tk, prev), (tk, s)]
            prev = s
        last = min(self.t_end, max(float(self.time.max()), float(t[-1]) if len(t) else 0.0))
        pts.append((last, prev))
        return pts

    def curve(self, stroke_width: float = 4.0, color=None) -> VMobject:
        m = VMobject(stroke_color=color or self.color, stroke_width=stroke_width)
        m.set_points_as_corners([self.ax.c2p(a, b) for a, b in self._steps(self.km["surv"])])
        return m

    def ticks(self, color=None, size: float = 0.09) -> VGroup:
        from explainer.stats.kit import survival as SV

        g = VGroup()
        for t in self.time[self.event == 0]:
            if t > self.t_end:
                continue
            s = float(SV.km_at(self.km, [t])[0])
            p = self.ax.c2p(t, s)
            g.add(Line(p + DOWN * size, p + UP * size, color=color or GREY_A, stroke_width=2.5))
        return g

    def band(self, lo, hi, color=None, opacity: float = 0.25) -> VMobject:
        up = self._steps(np.asarray(hi, float))
        dn = self._steps(np.asarray(lo, float))
        pts = [self.ax.c2p(a, b) for a, b in up] + [self.ax.c2p(a, b) for a, b in dn[::-1]]
        return Polygon(*pts, stroke_width=0, fill_color=color or self.color, fill_opacity=opacity)

    def people(self, y: float, x0: float, x1: float, radius: float = 0.07) -> VGroup:
        o = np.lexsort((1 - self.event, self.time))
        xs = np.linspace(x0, x1, len(o))
        g = VGroup(*[Dot([x, y, 0], radius=radius, color=S.RESID if self.event[i] else GREY_B) for x, i in zip(xs, o)])
        g.order = o
        return g

    def drop(self, k: int, font_size: int = 20) -> VGroup:
        t = self.km["t"][k]
        s0 = 1.0 if k == 0 else self.km["surv"][k - 1]
        s1 = self.km["surv"][k]
        ln = Line(self.ax.c2p(t, s0), self.ax.c2p(t, s1), color=S.ACCENT, stroke_width=6)
        from explainer.analysis import label

        lab = label(rf"$n = {int(self.km['n'][k])}$, \ $d = {int(self.km['d'][k])}$", font_size=font_size, color=S.ACCENT)
        lab.next_to(ln, RIGHT, buff=0.12)
        return VGroup(ln, lab)


class MaskGrid(VGroup):
    """A data table as a grid of cells (Part 41): rows are units, columns variables.  ``mark(mask, color)`` greys
    out the missing cells of one column (True = missing); ``fill(col, rows, color)`` paints imputed cells; ``copies(k)``
    stacks k offset copies, the m completed data sets of multiple imputation.  Cells keep their order, so the same
    respondent can be followed across mechanisms."""

    def __init__(self, n_rows: int, names, cell_w: float = 0.9, cell_h: float = 0.16, center=ORIGIN, font_size: int = 18):
        super().__init__()
        from explainer.analysis import label

        self.n_rows, self.n_cols = n_rows, len(names)
        self.cell_w, self.cell_h = cell_w, cell_h
        x0 = -self.n_cols * cell_w / 2
        y0 = n_rows * cell_h / 2
        self.cells = [[Rectangle(width=cell_w * 0.94, height=cell_h * 0.82, stroke_width=0, fill_color=S.EST, fill_opacity=0.8)
                       .move_to([x0 + (j + 0.5) * cell_w, y0 - (i + 0.5) * cell_h, 0]) for j in range(self.n_cols)]
                      for i in range(n_rows)]
        self.grid = VGroup(*[c for row in self.cells for c in row])
        self.heads = VGroup(*[label(nm, font_size=font_size, color=GREY_A).move_to([x0 + (j + 0.5) * cell_w, y0 + 0.25, 0])
                              for j, nm in enumerate(names)])
        self.add(self.grid, self.heads)
        self.move_to(center)

    def column(self, j: int) -> VGroup:
        return VGroup(*[self.cells[i][j] for i in range(self.n_rows)])

    def mark(self, j: int, mask, color=None, opacity: float = 0.9):
        """Animations that turn the masked cells of column j to the 'missing' colour."""
        return [self.cells[i][j].animate.set_fill(color or "#141821", opacity=opacity).set_stroke(GREY_B, width=1.2) for i, m in enumerate(mask) if m]

    def fill(self, j: int, rows, color=None, opacity: float = 0.85):
        return [self.cells[i][j].animate.set_fill(color or S.ACCENT, opacity=opacity) for i in rows]

    def copies(self, k: int, dx: float = 0.18, dy: float = -0.12) -> VGroup:
        g = VGroup()
        for c in range(1, k):
            g.add(self.grid.copy().set_opacity(0.25).shift(RIGHT * dx * c + DOWN * dy * -c))
        return g


class ExamCard(VGroup):
    """An exam problem as a card (Part 42): a header strip with the problem's number and topic, the parts it draws on
    and its marks; the question beneath; and a pause clock at the right.  ``sweep(run_time)`` turns the clock's hand
    once (the viewer's time to try it), ``stamp(text)`` returns a 'solved' seal for the header, and ``shrink()`` an
    animation that lifts the card to the top of the frame so the solution can be worked beneath it."""

    def __init__(self, number: int, topic: str, parts: str, question, marks: int = 10, width: float = 12.8,
                 font_size: int = 24, color=None):
        super().__init__()
        from explainer.analysis import label

        self.color = color or S.ACCENT
        lines = [question] if isinstance(question, str) else list(question)
        q = VGroup(*[label(s, font_size=font_size) for s in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        if q.width > width - 1.6:
            q.width = width - 1.6
        strip = Rectangle(width=width, height=0.62, stroke_width=0, fill_color=self.color, fill_opacity=0.22)
        num = label(rf"Problem {number}" if number else r"Example", font_size=26, color=self.color)
        top = label(topic, font_size=26)
        right = label(rf"{parts} \ \textbullet\ \ {marks} marks" if marks else parts, font_size=20, color=GREY_A)
        num.move_to(strip.get_left() + RIGHT * (0.25 + num.width / 2))
        top.next_to(num, RIGHT, buff=0.35)
        right.move_to(strip.get_right() + LEFT * (0.25 + right.width / 2))
        body = Rectangle(width=width, height=q.height + 0.5, stroke_color=self.color, stroke_width=1.5, fill_color="#10141d",
                         fill_opacity=0.92)
        body.next_to(strip, DOWN, buff=0)
        q.move_to(body.get_left() + RIGHT * (0.3 + q.width / 2)).set_y(body.get_y())
        r = 0.3
        face = Circle(radius=r, stroke_color=GREY_B, stroke_width=2).move_to(body.get_right() + LEFT * 0.6)
        face.set_y(body.get_y())
        self.clock_center, self.clock_r = face.get_center(), r
        self.hand = AnnularSector(inner_radius=0, outer_radius=r * 0.92, angle=-1e-3, start_angle=PI / 2, stroke_width=0,
                                  fill_color=self.color, fill_opacity=0.65).shift(self.clock_center)
        self.frame = VGroup(body, strip)
        self.strip, self.question, self.face = strip, q, face
        self.add(body, strip, num, top, right, q, face, self.hand)

    def sweep(self, run_time: float = 5.0) -> Animation:
        c, r, col = self.clock_center.copy(), self.clock_r * 0.92, self.color
        start = self.hand.copy()

        def upd(m, a):
            if a <= 1e-3:
                m.become(start)
                return
            sc = self.face.width / (2 * self.clock_r)
            m.become(AnnularSector(inner_radius=0, outer_radius=r * sc, angle=-a * TAU, start_angle=PI / 2, stroke_width=0,
                                   fill_color=col, fill_opacity=0.65).shift(self.face.get_center()))

        return UpdateFromAlphaFunc(self.hand, upd, run_time=run_time, rate_func=linear)

    def stamp(self, text: str = r"solved") -> VGroup:
        from explainer.analysis import label

        t = label(text, font_size=22, color=S.KEPT)
        box = SurroundingRectangle(t, buff=0.1, color=S.KEPT, stroke_width=2.5, corner_radius=0.08)
        g = VGroup(box, t).rotate(0.12)
        g.move_to(self.face.get_center())
        return g

    def shrink(self, scale: float = 0.78, buff: float = 0.25) -> Animation:
        return self.animate.scale(scale).to_edge(UP, buff=buff)


class ConvergenceLab(VGroup):
    """The weak-convergence lab (Part 43) on CDF axes ``ax``: a law F_n against its limit G.  ``curve_F()`` /
    ``curve_G()`` draw them (F as a staircase when built from atoms); ``kolmogorov_bar(x)`` the vertical gap at x, the
    Kolmogorov distance where it is largest; ``levy_box(x, eps)`` the eps-by-eps box that Lévy's metric fits between
    the graphs; ``area()`` the region between them, whose area is the Wasserstein-1 distance."""

    def __init__(self, ax, G, F=None, atoms=None, probs=None, x_range=None, color_F=None, color_G=None, m: int = 600):
        super().__init__()
        self.ax = ax
        b = bounds(ax)
        self.x0, self.x1 = (b[0], b[1]) if x_range is None else x_range
        self.G = G
        self.atoms = None if atoms is None else np.asarray(atoms, float)
        self.probs = None if probs is None else np.asarray(probs, float)
        if F is None and self.atoms is not None:
            c = np.cumsum(self.probs)
            a = self.atoms

            def F(x):
                i = np.searchsorted(a, np.asarray(x, float), side="right")
                return np.where(i > 0, c[np.maximum(i - 1, 0)], 0.0)
        self.F = F
        self.cF, self.cG = color_F or S.EST, color_G or S.TRUTH
        self.xs = np.linspace(self.x0, self.x1, m)

    def _pts_F(self):
        if self.atoms is None:
            return [(x, float(self.F(np.array([x]))[0])) for x in self.xs]
        pts, prev = [(self.x0, float(self.F(np.array([self.x0]))[0]))], float(self.F(np.array([self.x0]))[0])
        for a in self.atoms:
            if self.x0 < a < self.x1:
                nxt = float(self.F(np.array([a]))[0])
                pts += [(a, prev), (a, nxt)]
                prev = nxt
        pts.append((self.x1, prev))
        return pts

    def curve_F(self, stroke_width: float = 4.0) -> VMobject:
        m = VMobject(stroke_color=self.cF, stroke_width=stroke_width)
        m.set_points_as_corners([self.ax.c2p(a, b) for a, b in self._pts_F()])
        return m

    def curve_G(self, stroke_width: float = 3.5) -> VMobject:
        m = VMobject(stroke_color=self.cG, stroke_width=stroke_width)
        m.set_points_smoothly([self.ax.c2p(x, float(self.G(np.array([x]))[0])) for x in self.xs])
        return m

    def kolmogorov_bar(self, x: float, top: float | None = None, bottom: float | None = None, color=None) -> VGroup:
        g = float(self.G(np.array([x]))[0])
        f = float(self.F(np.array([x]))[0]) if top is None else top
        lo = g if bottom is None else bottom
        line = Line(self.ax.c2p(x, lo), self.ax.c2p(x, f), color=color or S.ACCENT, stroke_width=6)
        dots = VGroup(Dot(self.ax.c2p(x, lo), radius=0.06, color=color or S.ACCENT), Dot(self.ax.c2p(x, f), radius=0.06, color=color or S.ACCENT))
        return VGroup(line, dots)

    def levy_box(self, x: float, eps: float, y: float | None = None, color=None) -> Rectangle:
        y = float(self.G(np.array([x]))[0]) if y is None else y
        p0, p1 = self.ax.c2p(x - eps / 2, y - eps / 2), self.ax.c2p(x + eps / 2, y + eps / 2)
        return Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], stroke_color=color or S.PRIOR, stroke_width=3,
                         fill_color=color or S.PRIOR, fill_opacity=0.25).move_to((p0 + p1) / 2)

    def area(self, color=None, opacity: float = 0.35) -> VGroup:
        """The region between the two CDFs, as thin vertical strips (its area is the Wasserstein-1 distance)."""
        g = VGroup()
        xs = np.linspace(self.x0, self.x1, 240)
        w = (xs[1] - xs[0])
        for x in xs:
            a = float(self.F(np.array([x]))[0])
            b = float(self.G(np.array([x]))[0])
            if abs(a - b) < 1e-4:
                continue
            p0, p1 = self.ax.c2p(x - w / 2, min(a, b)), self.ax.c2p(x + w / 2, max(a, b))
            g.add(Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], stroke_width=0, fill_color=color or S.ALT,
                            fill_opacity=opacity).move_to((p0 + p1) / 2))
        return g
