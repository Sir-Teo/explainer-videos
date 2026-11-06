from __future__ import annotations

import numpy as np

from videos.stats.stats1.common import *  # noqa: F403
from videos.stats.stats1.compute import inverse_quantiles


class Quantiles(VoiceoverScene):
    def construct(self):
        self.card()
        self.ecdf()
        self.inverse()
        self.boxplot()
        self.regions()

    def card(self):
        card = chapter_card(6, r"Quantiles and the box plot", r"Where does each person stand?",
                            lit={1977: r"Tukey's \emph{Exploratory Data Analysis}"}, part=PART)
        with self.voiceover("Chapter six. Quantiles and the box plot."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def ecdf(self):
        d = load("quantiles")
        x = np.asarray(d["x"])
        A = axes([0, 180], [0, 1], x_length=10.4, y_length=4.4, xlabel=r"income (thousands)",
                 ylabel=r"share earning at most $x$", xticks=[0, 30, 60, 90, 120, 150, 180],
                 yticks=[0, 0.25, 0.5, 0.75, 1.0], yfmt=lambda v: f"{v:g}", center=[0, -0.3, 0])
        ax = A.ax
        rug = VGroup(*[Line(ax.c2p(v, 0) + DOWN * 0.08, ax.c2p(v, 0) + UP * 0.12, color=S.DATA, stroke_width=2)
                       for v in x])
        st = ecdf_steps(ax, x, color=S.EST, stroke_width=4, x_hi=180)
        dfn = definition_card(r"Empirical CDF", r"$\hat F(x)$ = the share of the sample at or below $x$. \ It rises "
                              r"by $1/n$ at each observation.", color=S.EST, width=4.4, font_size=22)
        dfn.move_to([3.9, 0.3, 0])
        tag = simulated_tag(r"simulated: 40 World incomes")
        probe = ValueTracker(20.0)
        pdot = always_redraw(lambda: Dot(ax.c2p(probe.get_value(), np.mean(x <= probe.get_value())), radius=0.08,
                                         color=S.ACCENT))
        pread = always_redraw(lambda: MathTex(
            rf"\hat F({probe.get_value():.0f}) = {int(np.sum(x <= probe.get_value()))}/{len(x)}", font_size=30,
            color=S.ACCENT).to_corner(UL, buff=0.5))
        with self.voiceover(
            "The mean and the standard deviation squeeze a whole distribution into two numbers. Here's a picture "
            "that squeezes nothing. <bookmark mark='a'/> Forty incomes from the World, marked along the axis. "
            "<bookmark mark='b'/> Now walk from left to right and keep count: at each income you pass, climb by one "
            "fortieth. The staircase you trace is the empirical cumulative distribution function. Its height above "
            "any income x is the share of the sample earning x or less. <bookmark mark='c'/> At twenty thousand, "
            "it's this many; slide along, and it climbs. Every observation is a step, so the staircase contains "
            "the data exactly, sorted. <bookmark mark='d'/> And it's the single most important estimator in the "
            "series: in Part 6 we'll prove that as the sample grows, this staircase converges to the true "
            "distribution, uniformly, everywhere at once. That theorem has been called the fundamental theorem of "
            "statistics."
        ) as vo:
            self.play(FadeIn(A), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(r) for r in rug], lag_ratio=0.04), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(st), run_time=4.0, rate_func=linear)
            self.play(FadeIn(dfn, shift=LEFT * 0.2))
            vo.wait_until("c")
            self.add(pdot, pread)
            self.play(probe.animate.set_value(60.0), run_time=3.0)
            vo.wait_until("d")
            self.play(probe.animate.set_value(170.0), run_time=2.0)
        pdot.clear_updaters()
        pread.clear_updaters()
        self.play(FadeOut(pdot), FadeOut(pread), FadeOut(dfn))
        self.A, self.st, self.rug, self.tag = A, st, rug, tag

    def inverse(self):
        d = load("quantiles")
        x = np.asarray(d["x"])
        q = inverse_quantiles(x)
        ax = self.A.ax
        qs = [(0.5, q["q50"], r"lower median", MEDIAN), (0.25, q["q25"], r"$Q_1$", MODE), (0.75, q["q75"], r"$Q_3$", MODE),
              (0.9, q["q90"], r"90th percentile", S.ACCENT)]
        reads = VGroup()
        for p, v, name, col in qs:
            h = DashedLine(ax.c2p(0, p), ax.c2p(v, p), color=col, stroke_width=2.5)
            vv = DashedLine(ax.c2p(v, p), ax.c2p(v, 0), color=col, stroke_width=2.5)
            t = label(rf"{name}: \ {v:.1f}", font_size=24, color=col).next_to(ax.c2p(v, p), RIGHT, buff=0.15)
            t.add_background_rectangle(color=BACKGROUND, opacity=0.8, buff=0.05)
            reads.add(VGroup(h, vv, t))
        eq = cmath(r"\hat Q(p)", r"=", r"\min\{x : \hat F(x) \ge p\},\quad 0 < p \le 1", font_size=36).to_edge(UP, buff=0.35)
        # the quantile function: the staircase reflected in the diagonal
        B = axes([0, 1], [0, 180], x_length=4.4, y_length=4.4, xlabel=r"$p$", ylabel=r"$\hat Q(p)$",
                 xticks=[0, 0.5, 1], yticks=[0, 60, 120, 180], center=[4.4, -0.3, 0])
        bx = B.ax
        xs = np.sort(x)
        pts = [bx.c2p(0, xs[0])]
        for i, xi in enumerate(xs):
            pts += [bx.c2p(i / len(xs), xi), bx.c2p((i + 1) / len(xs), xi)]
        qf = VMobject(color=S.EST, stroke_width=4).set_points_as_corners(pts)
        with self.voiceover(
            "Read the staircase the other way, and you get quantiles. <bookmark mark='a'/> Pick a share, say a "
            "half. Go across at height one half until you hit the staircase, then down. The income you land on is "
            f"the lower median: {q['q50']:.1f} thousand. Half the sample earns no more than this. <bookmark mark='b'/> At "
            f"one quarter, the first quartile, {q['q25']:.1f}; at three quarters, the third, {q['q75']:.1f}. "
            f"<bookmark mark='c'/> And at nine tenths, the ninetieth percentile, {q['q90']:.1f}. "
            "<bookmark mark='d'/> This rule, the smallest x whose share reaches p, is the quantile function: the "
            "inverse of the staircase, defined even where the staircase is flat or jumps. <bookmark mark='e'/> "
            "Geometrically it's the same staircase reflected in the diagonal, with the axes swapped. Quantiles are "
            "how growth charts, exam percentiles and income deciles are reported. Software also uses interpolated "
            "quantiles; we'll use that convention for the box plots next. Unlike the mean, quantiles "
            "say where a person stands."
        ) as vo:
            vo.wait_until("a")
            self.play(Create(reads[0][0]), Create(reads[0][1]), FadeIn(reads[0][2]))
            vo.wait_until("b")
            for r in reads[1:3]:
                self.play(Create(r[0]), Create(r[1]), FadeIn(r[2]), run_time=0.8)
            vo.wait_until("c")
            self.play(Create(reads[3][0]), Create(reads[3][1]), FadeIn(reads[3][2]))
            vo.wait_until("d")
            self.play(Write(eq))
            vo.wait_until("e")
            self.play(VGroup(self.A, self.st, self.rug, reads).animate.scale(0.62).move_to([-3.4, -0.3, 0]),
                      FadeOut(self.tag))
            self.play(FadeIn(B), TransformFromCopy(self.st, qf), run_time=2.0)
        self.clear_scene()

    def boxplot(self):
        d = load("quantiles")
        x = np.asarray(d["x"])
        five = d["five"]
        A = axes([0, 180], [0, 1], x_length=11.6, y_length=0.4, xlabel=r"income (thousands)",
                 xticks=[0, 30, 60, 90, 120, 150, 180], center=[0, -2.2, 0])
        A.ax.y_axis.set_opacity(0)
        ax = A.ax
        g = np.random.Generator(np.random.PCG64(8))
        pts = VGroup(*[Dot(ax.c2p(v, 0) + UP * (0.9 + 0.5 * g.random()), radius=0.06, color=S.DATA) for v in x])
        names = [("min", five["min"]), ("Q_1", five["q1"]), (r"\text{median}", five["median"]), ("Q_3", five["q3"]),
                 ("max", five["max"])]
        ticks = VGroup()
        for nm, v in names:
            t = VGroup(Line(ax.c2p(v, 0) + UP * 1.6, ax.c2p(v, 0) + UP * 2.0, color=GREY_A, stroke_width=2),
                       MathTex(rf"{nm}" if nm not in ("min", "max") else rf"\text{{{nm}}}", font_size=26,
                               color=GREY_A), MathTex(f"{v:.1f}", font_size=24, color=WHITE))
            t[1].next_to(t[0], UP, buff=0.08)
            t[2].next_to(t[1], UP, buff=0.06)
            if len(ticks) % 2 == 1:
                t[0].put_start_and_end_on(t[0].get_start(), t[0].get_end() + UP * 0.7)
                VGroup(t[1], t[2]).shift(UP * 0.7)
            ticks.add(t)
        bp = box_plot(ax, five, y=ax.c2p(0, 0)[1] + 3.6, height=0.7, color=S.EST)
        lo_f, hi_f = five["fences"]
        fence = DashedLine(ax.c2p(hi_f, 0) + UP * 3.0, ax.c2p(hi_f, 0) + UP * 4.2, color=S.RESID, stroke_width=2)
        flab = label(r"$Q_3 + 1.5\,\mathrm{IQR}$", font_size=24, color=S.RESID).next_to(fence, UP, buff=0.08)
        iqr = BraceBetweenPoints(ax.c2p(five["q1"], 0) + UP * 4.0, ax.c2p(five["q3"], 0) + UP * 4.0, direction=UP,
                                 color=MODE)
        iql = label(rf"IQR $= {five['iqr']:.1f}$", font_size=24, color=MODE).next_to(iqr, UP, buff=0.05)
        hc = history_card(1970, r"John W. Tukey", r"the ``box-and-whisker plot'': \ five numbers, \ and a rule for "
                          r"points worth a second look", color=S.MUSEUM, width=4.6, font_size=20).to_corner(UR, buff=0.3)
        with self.voiceover(
            "Five quantiles make a summary that fits on a line. <bookmark mark='a'/> The minimum, the first "
            "quartile, the median, the third quartile and the maximum: a five-number summary. Here the quartiles "
            "use linear interpolation between observations, and the median averages the two middle incomes. "
            "<bookmark mark='b'/> Tukey drew it as a box from the first to the third quartile, with the median "
            "inside: the box holds the middle half of the data, and its width is the interquartile range. "
            "<bookmark mark='c'/> Then whiskers reach out to the most extreme points that are within one and a half "
            "box widths of the box. <bookmark mark='d'/> Anything beyond, here "
            f"{len(five['outliers'])} incomes, is drawn as a separate point, an outlier. <bookmark mark='e'/> "
            "Tukey meant it as a flag, not a verdict: a point worth a second look. Here it isn't an error at all. "
            "The World's incomes have a long right tail, and these flagged values are simply the tail. A rule built for "
            "symmetric data calls the rich outliers."
        ) as vo:
            self.play(FadeIn(A), LaggedStart(*[FadeIn(p, shift=DOWN * 0.2) for p in pts], lag_ratio=0.02),
                      FadeIn(hc, shift=LEFT * 0.2))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.1) for t in ticks], lag_ratio=0.3), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeOut(ticks[0]), FadeOut(ticks[4]), FadeOut(hc))
            self.play(Create(bp.box), Create(bp.median), GrowFromCenter(iqr), FadeIn(iql), FadeOut(ticks[1:4]))
            vo.wait_until("c")
            self.play(Create(bp.whiskers), Create(fence), FadeIn(flab))
            vo.wait_until("d")
            self.play(LaggedStart(*[GrowFromCenter(o) for o in bp.outliers], lag_ratio=0.2))
            vo.wait_until("e")
            self.play(Indicate(bp.outliers, color=S.RESID, scale_factor=1.6))
        self.clear_scene()

    def regions(self):
        d = load("quantiles")
        A = axes([0, 140], [0, 11], x_length=10.0, y_length=5.6, xlabel=r"income (thousands), \ 300 adults per region",
                 xticks=[0, 35, 70, 105, 140], center=[0.6, -0.3, 0])
        A.ax.y_axis.set_opacity(0)
        ax = A.ax
        boxes, truths, names, overflow = VGroup(), VGroup(), VGroup(), VGroup()
        for k, five in enumerate(d["regions"]):
            y = ax.c2p(0, 10.5 - k)[1]
            bp = box_plot(ax, five, y=y, height=0.32, color=REGION_COLORS[k], stroke_width=2)
            boxes.add(bp)
            count = sum(v > 140 for v in five["outliers"])
            if count:
                overflow.add(label(rf"$\to {count}$", font_size=18, color=S.RESID)
                             .next_to(ax.c2p(140, 10.5 - k), RIGHT, buff=0.15))
            tv = d["region_median_true"][k]
            truths.add(Line([ax.c2p(tv, 0)[0], y - 0.22, 0], [ax.c2p(tv, 0)[0], y + 0.22, 0], color=S.TRUTH,
                            stroke_width=4))
            names.add(label(rf"region {k + 1}", font_size=20, color=REGION_COLORS[k])
                      .next_to([ax.c2p(0, 0)[0], y, 0], LEFT, buff=0.2))
        meds = [f["median"] for f in d["regions"]]
        tag = simulated_tag()
        key = note(r"right arrows count outliers beyond 140 thousand").to_edge(UP, buff=0.3)
        with self.voiceover(
            "Box plots are made for comparing groups. <bookmark mark='a'/> Here are three hundred adults from each "
            "of the World's ten regions. The medians wander, from "
            f"{min(meds):.1f} to {max(meds):.1f} thousand, and it's tempting to rank the regions, and to look for "
            f"reasons: why is region {int(np.argmax(meds)) + 1} so much richer than region {int(np.argmin(meds)) + 1}? "
            "<bookmark mark='b'/> But we know the truth. "
            "In the World, as built so far, income doesn't depend on region at all. The gold marks are the ten "
            "true regional medians, and they're all essentially the same. <bookmark mark='c'/> Every difference "
            "between those boxes is the luck of who was sampled. Learning to tell a real difference from this kind "
            "of noise takes up much of the bachelor's degree; Part 10 starts on it properly."
        ) as vo:
            self.play(FadeIn(A), FadeIn(names), FadeIn(tag), FadeIn(key))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b) for b in boxes], lag_ratio=0.12), FadeIn(overflow), run_time=3.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(t) for t in truths], lag_ratio=0.08))
            vo.wait_until("c")
            self.play(*[Indicate(b.median, color=WHITE, scale_factor=1.6) for b in boxes])
        self.clear_scene()
