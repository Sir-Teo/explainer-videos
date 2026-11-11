from __future__ import annotations

import numpy as np
from scipy import stats as sstats

from explainer.quant import *  # noqa: F403
from videos.quant.quant1.common import GAUSS, PART, REAL, TAIL, VOL, load, real_data


class Aggregation(VoiceoverScene):
    def construct(self):
        a = load("aggregation")
        self.card()
        self.shapes(a)
        self.kurtosis(a)
        self.theory(load("agg_theory"))

    def card(self):
        c = chapter_card(7, r"Slower clocks, thinner tails", r"Does the bell curve come back at longer horizons?",
                         part=PART)
        with self.voiceover("Chapter seven. Slower clocks, thinner tails."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def shapes(self, a):
        e = np.asarray(a["edges"])
        xs = np.linspace(-5, 5, 300)
        panels = VGroup()
        names = {"1": r"one day", "21": r"one month (21 days)", "252": r"one year (252 days)"}
        for h in ("1", "21", "252"):
            dens = np.asarray(a["hists"][h])
            g = axes([-5, 5], [-4, 0], x_length=3.9, y_length=3.4, xlabel=r"standard deviations",
                     xticks=[-4, 0, 4], yticks=[-4, -2, 0], yfmt=lambda v: f"10^{{{int(v)}}}", font_size=16)
            ax = g.ax
            bb = VGroup()
            for lo, hi, d in zip(e[:-1], e[1:], dens):
                if d <= 1e-4:
                    continue
                y = np.log10(d)
                p0, p1 = ax.c2p(lo, -4), ax.c2p(hi, y)
                bb.add(Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], stroke_width=0, fill_color=REAL,
                                 fill_opacity=0.8).move_to([(p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2, 0]))
            gc = curve(ax, xs, np.clip(np.log10(sstats.norm.pdf(xs)), -4, 0), GAUSS, stroke_width=3)
            t = label(names[h], font_size=24, color=QC.IDEA).next_to(g, UP, buff=0.12)
            panels.add(VGroup(g, bb, gc, t))
        panels.arrange(RIGHT, buff=0.45).shift(DOWN * 0.2)
        src = real_data(r"overlapping $h$-day log returns of the US market, 1926--2020, each scaled to unit variance")
        with self.voiceover(
            "A sum of many independent pieces with a finite variance tends towards a bell curve, whatever the "
            "pieces look like: the central limit theorem. A monthly return is a sum of about twenty-one daily "
            "returns, a yearly return of two hundred and fifty-two. So the tails should thin as the clock slows. "
            "<bookmark mark='a'/> Daily returns, on the left: heavy tails, far beyond the grey bell curve. "
            "<bookmark mark='b'/> Monthly: still heavier than the bell curve, but closer. <bookmark mark='c'/> "
            "Yearly: almost a bell curve, apart from a few years at the left edge, which are the early 1930s. "
            "Aggregational Gaussianity, in the jargon of stylized facts."
        ) as vo:
            self.play(FadeIn(src))
            self.play(FadeIn(panels[0][0]), FadeIn(panels[0][3]), LaggedStart(*[GrowFromEdge(b, DOWN) for b in panels[0][1]],
                                                                             lag_ratio=0.02), Create(panels[0][2]))
            vo.wait_until("a")
            self.wait(0.5)
            vo.wait_until("b")
            self.play(FadeIn(panels[1][0]), FadeIn(panels[1][3]), LaggedStart(*[GrowFromEdge(b, DOWN) for b in panels[1][1]],
                                                                             lag_ratio=0.02), Create(panels[1][2]))
            vo.wait_until("c")
            self.play(FadeIn(panels[2][0]), FadeIn(panels[2][3]), LaggedStart(*[GrowFromEdge(b, DOWN) for b in panels[2][1]],
                                                                             lag_ratio=0.02), Create(panels[2][2]))
        self.wait(0.4)
        self.clear_scene()

    def kurtosis(self, a):
        h = np.asarray(a["h"], float)
        k, kn, ko = np.asarray(a["kurt"]), np.asarray(a["kurt_no87"]), np.asarray(a["kurt_overlap"])
        g = axes([0, np.log10(300)], [0, 20], x_length=7.4, y_length=4.6, xlabel=r"horizon $h$, trading days (log scale)",
                 ylabel=r"excess kurtosis of $h$-day returns", xticks=[0, np.log10(5), np.log10(21), np.log10(63),
                                                                       np.log10(252)],
                 xfmt=lambda v: f"{10 ** v:.0f}", yticks=[0, 5, 10, 15, 20], font_size=18).to_edge(LEFT, buff=0.7)
        g.shift(DOWN * 0.3)
        ax = g.ax
        x = np.log10(h)
        d1 = VGroup(*[Dot(ax.c2p(a_, b_), radius=0.08, color=REAL) for a_, b_ in zip(x, k)])
        l1 = curve(ax, x, ko, REAL, stroke_width=2.5)
        d2 = VGroup(*[Dot(ax.c2p(a_, b_), radius=0.07, color=TAIL) for a_, b_ in zip(x, kn)])
        zero = DashedLine(ax.c2p(0, 0), ax.c2p(np.log10(300), 0), color=GAUSS, stroke_width=2)
        zl = label(r"bell curve", font_size=20, color=GAUSS).next_to(ax.c2p(np.log10(300), 0), UL, buff=0.08)
        leg = legend([(REAL, r"all days (dots: separate blocks; line: overlapping)"),
                      (TAIL, r"without 19 October 1987")], font_size=21)
        leg.to_edge(RIGHT, buff=0.4).shift(UP * 2.2)
        pts = VGroup(
            MathTex(rf"\text{{day}}\ {k[0]:.1f}", font_size=32, color=REAL),
            MathTex(rf"\text{{month}}\ {k[4]:.1f}", font_size=32, color=REAL),
            MathTex(rf"\text{{half-year}}\ {k[7]:.1f}", font_size=32, color=REAL),
            MathTex(rf"\text{{year}}\ {k[8]:.1f}\ \ (94\ \text{{years: a noisy number}})", font_size=28, color=REAL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).next_to(leg, DOWN, buff=0.5).align_to(leg, LEFT)
        why_ = wrapped_label(r"slower than independent sums would allow: the clusters of chapter 6 make neighbouring "
                             r"days move together in size", 4.3, 21, GREY_A).next_to(pts, DOWN, buff=0.4).align_to(leg, LEFT)
        with self.voiceover(
            "The kurtosis, horizon by horizon. <bookmark mark='a'/> "
            f"{k[0]:.1f} for a day, {k[4]:.1f} for a month, {k[7]:.1f} for half a year. It falls, as the central "
            "limit theorem promises. <bookmark mark='b'/> But slowly. For independent days it would fall in "
            "proportion to the horizon: a month should have one twenty-first of the daily kurtosis, under one. "
            "Volatility clustering is why it doesn't: neighbouring days are wild together, so a month is not "
            "twenty-one independent draws. <bookmark mark='c'/> The red dots drop a single day, the 19th of "
            "October 1987, and the short-horizon kurtosis falls by a fifth. One day out of twenty-five thousand. "
            "That should make you suspicious of the number itself; Mandelbrot will be. First, why the fall is so slow."
        ) as vo:
            self.play(FadeIn(g), Create(zero), FadeIn(zl), FadeIn(leg[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromCenter(d) for d in d1], lag_ratio=0.2), Create(l1), run_time=2)
            self.play(LaggedStart(*[FadeIn(p) for p in pts[:3]], lag_ratio=0.4))
            vo.wait_until("b")
            self.play(FadeIn(pts[3]), FadeIn(why_))
            vo.wait_until("c")
            self.play(LaggedStart(*[GrowFromCenter(d) for d in d2], lag_ratio=0.2), FadeIn(leg[1]))
        self.wait(0.4)
        self.clear_scene()

    def theory(self, t):
        rows = [
            cmath(r"S_h = \sum_{t=1}^{h} r_t", r"\Rightarrow", r"\mathbb{E}\,S_h^2 = h\sigma^2", font_size=34),
            cmath(r"\mathbb{E}\,S_h^4", r"=", r"\sum_t \mathbb{E}\,r_t^4 + 6\sum_{t<s}\mathbb{E}\,r_t^2 r_s^2"
                  r" + \text{other cross terms}", font_size=34),
            cmath(r"\kappa_h", r"=", r"\frac{\kappa_1 + 6(\kappa_1 + 2)\sum_{k<h}(1 - k/h)\,\rho_k(r^2)}{h}"
                  r" + \dots", font_size=34, colors={r"\kappa_h": VOL}),
            cmath(r"\text{independent days:}\ \ \kappa_h", r"=", r"\kappa_1 / h", font_size=34,
                  colors={r"\text{independent days:}\ \ \kappa_h": GAUSS}),
        ]
        whys = [why(r"returns are uncorrelated (chapter six), so their variances add"),
                why(r"expand the fourth power: the pairs of squares are where clustering lives"),
                why(r"divide by $(h\sigma^2)^2$; $\operatorname{Var}(r^2) = (\kappa_1 + 2)\sigma^4$ turns each "
                    r"covariance of squares into an autocorrelation $\rho_k(r^2)$"),
                why(r"with no clustering only the first term survives")]
        step = ladder(self, rows, whys, keep=4, top=3.2, x=0.0, align_index=None, buff=0.45, edge=6.9)
        with self.voiceover(
            "Why so slowly? Write the monthly return as a sum of daily ones. Because the days are uncorrelated, "
            "their variances add. <bookmark mark='a'/> Now the fourth power. Expand it, and among the terms are the "
            "pairs of squares: today's squared move times another day's. That is exactly where clustering lives. "
            "<bookmark mark='b'/> Divide by the squared variance, and those pairs become the autocorrelations of "
            "squared returns that chapter six measured, weighted by how many pairs sit at each distance. "
            "<bookmark mark='c'/> Without clustering only the first term survives: the daily kurtosis divided by "
            "the horizon. That is the central limit theorem's speed, and it is not the market's."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
        self.wait(0.4)
        self.clear_scene()

        h = np.asarray(t["h"], float)
        iid, pred, meas = (np.asarray(t[k], float) for k in ("iid", "pred", "meas"))
        lo, hi = -1.5, np.log10(30)
        g = axes([0, np.log10(260)], [lo, hi], x_length=8.0, y_length=4.8,
                 xlabel=r"horizon $h$, trading days (log scale)", ylabel=r"excess kurtosis (log scale)",
                 xticks=[0, np.log10(5), np.log10(21), np.log10(63), np.log10(252)], xfmt=lambda v: f"{10 ** v:.0f}",
                 yticks=[-1, 0, 1], yfmt=lambda v: f"{10 ** v:g}", font_size=18).to_edge(LEFT, buff=0.7)
        ax = g.ax
        x = np.log10(h)
        ly = lambda v: np.clip(np.log10(np.maximum(v, 10 ** lo)), lo, hi)  # noqa: E731
        c_iid = curve(ax, x, ly(iid), GAUSS, stroke_width=3)
        c_pred = curve(ax, x, ly(pred), VOL, stroke_width=3.5)
        dots = VGroup(*[Dot(ax.c2p(a_, b_), radius=0.06, color=REAL) for a_, b_ in zip(x, ly(meas))])
        i21 = int(np.argmin(np.abs(h - 21)))
        leg = legend([(GAUSS, r"independent days: $\kappa_1/h$"), (VOL, r"with the measured clustering"),
                      (REAL, r"the data, overlapping $h$-day returns")], font_size=20).to_edge(RIGHT, buff=0.4)
        leg.shift(UP * 2.0)
        nums = VGroup(
            MathTex(rf"h = {h[i21]:.0f}:", font_size=30),
            MathTex(rf"\text{{independent}}\ {iid[i21]:.2f}", font_size=30, color=GAUSS),
            MathTex(rf"\text{{clustering formula}}\ {pred[i21]:.1f}", font_size=30, color=VOL),
            MathTex(rf"\text{{data}}\ {meas[i21]:.1f}", font_size=30, color=REAL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).next_to(leg, DOWN, buff=0.45).align_to(leg, LEFT)
        src = real_data(r"US market, 1926--2020: $\kappa_1$ and $\rho_k(r^2)$ measured, then the formula")
        under = meas[i21] < pred[i21]
        verdict = ("Clustering accounts for the slow decay, and overshoots it: the other cross terms, which hold the "
                   "asymmetry of chapter six, add up to a negative number here. Independence misses by a factor of "
                   "ten; clustering lands within a factor of two." if under else
                   "Clustering accounts for the slow decay, and the remaining cross terms add a little more.")
        with self.voiceover(
            "Now feed the formula the measured clustering. In grey, independent days: the kurtosis would collapse "
            f"to {iid[i21]:.2f} at a month. <bookmark mark='a'/> In teal, the formula with the clustering: "
            f"{pred[i21]:.1f}. <bookmark mark='b'/> The dots are the data: {meas[i21]:.1f}. {verdict} Monthly returns "
            "are not the bell curve the central limit theorem promises, and they will not be at the horizons desks "
            "trade. So does the variance even exist? Mandelbrot asked that question next."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), Create(c_iid), FadeIn(leg[0]), FadeIn(nums[0]), FadeIn(nums[1]))
            vo.wait_until("a")
            self.play(Create(c_pred), FadeIn(leg[1]), FadeIn(nums[2]))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromCenter(d_) for d_ in dots], lag_ratio=0.05), FadeIn(leg[2]),
                      FadeIn(nums[3]))
        self.wait(0.5)
        self.clear_scene()

