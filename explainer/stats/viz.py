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
        p = ax.c2p(x, ax.y_range[0])
        g.add(Dot([p[0], p[1] + radius * (1 + 2 * gap * k) + 0.02, 0], radius=radius, color=color))
    return g


def ecdf_steps(ax, values, color=None, stroke_width=3, x_lo=None, x_hi=None) -> VMobject:
    """The empirical CDF: a staircase rising 1/n at each sorted observation."""
    color = color or S.EST
    x = np.sort(np.asarray(values, float))
    n = len(x)
    lo = ax.x_range[0] if x_lo is None else x_lo
    hi = ax.x_range[1] if x_hi is None else x_hi
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
    X = lambda v: ax.c2p(v, ax.y_range[0])[0]  # noqa: E731
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
                    if ax.x_range[0] <= v <= ax.x_range[1]])
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
