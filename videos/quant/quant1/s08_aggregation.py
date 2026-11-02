from __future__ import annotations

import numpy as np
from scipy import stats as sstats

from explainer.quant import *  # noqa: F403
from videos.quant.quant1.common import GAUSS, PART, REAL, TAIL, load, real_data


class Aggregation(VoiceoverScene):
    def construct(self):
        a = load("aggregation")
        self.card()
        self.shapes(a)
        self.kurtosis(a)

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
                             r"days move together in size", 5.2, 21, GREY_A).next_to(pts, DOWN, buff=0.4).align_to(leg, LEFT)
        with self.voiceover(
            "The kurtosis, horizon by horizon. <bookmark mark='a'/> "
            f"{k[0]:.1f} for a day, {k[4]:.1f} for a month, {k[7]:.1f} for half a year. It falls, as the central "
            "limit theorem promises. <bookmark mark='b'/> But slowly. For independent days it would fall in "
            "proportion to the horizon: a month should have one twenty-first of the daily kurtosis, under one. "
            "Volatility clustering is why it doesn't: neighbouring days are wild together, so a month is not "
            "twenty-one independent draws. <bookmark mark='c'/> The red dots drop a single day, the 19th of "
            "October 1987, and the short-horizon kurtosis falls by a fifth. One day out of twenty-five thousand. "
            "That should make you suspicious of the number itself, which is where Mandelbrot comes in."
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
