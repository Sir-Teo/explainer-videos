from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant1.common import GAUSS, PART, REAL, TAIL, VOL, load, real_data

T3 = QC.IDEA
CAU = QC.GAMMA


class Mandelbrot(VoiceoverScene):
    def construct(self):
        m = load("mandelbrot")
        self.card()
        self.cotton()
        self.running_sd(m)
        self.running_kurt(m)
        self.lesson(m)

    def card(self):
        c = chapter_card(8, r"Does the variance exist?", r"Can you trust a standard deviation?", lit=(1963,), part=PART)
        with self.voiceover("Chapter eight. Does the variance exist?"):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def cotton(self):
        c1 = history_card(1963, r"Benoit Mandelbrot, \textit{Journal of Business}",
                          r"``The variation of certain speculative prices'': changes in cotton prices fit a "
                          r"\emph{stable} law with tail exponent $\alpha \approx 1.7$, a distribution whose variance "
                          r"is infinite", width=6.4, font_size=23)
        c2 = definition_card(r"Stable law", r"A sum of independent copies has the same shape as one copy, rescaled. "
                             r"The bell curve is the only one with a finite variance ($\alpha = 2$); for $\alpha < 2$ "
                             r"the tails fall like $u^{-\alpha}$ and the variance is infinite.", width=6.4,
                             color=TAIL, font_size=22)
        pair = VGroup(c1, c2).arrange(DOWN, buff=0.4, aligned_edge=LEFT).to_edge(LEFT, buff=0.6)
        pts = VGroup(
            label(r"If he were right:", font_size=26, color=GREY_A),
            label(r"a standard deviation is a number that never settles", font_size=24),
            label(r"tails stay heavy at every horizon", font_size=24),
            label(r"Markowitz, Black--Scholes and every variance-based tool break", font_size=24),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(RIGHT, buff=0.5)
        if pts.width > 6.0:
            pts.scale_to_fit_width(6.0).to_edge(RIGHT, buff=0.5)
        with self.voiceover(
            "In 1963 Benoit Mandelbrot, then at IBM, looked at the history of cotton prices and made a "
            "radical claim. Their changes fit not a bell curve but a stable law, with a tail exponent of about one "
            "point seven. <bookmark mark='a'/> A stable law keeps its shape when you add copies of it, as the bell "
            "curve does. But every stable law except the bell curve has an infinite variance. "
            "<bookmark mark='b'/> If Mandelbrot was right, the standard deviation of returns is a number that never "
            "settles down, tails never thin with the horizon, and the whole toolkit of modern finance, built on "
            "variances, is built on sand. Eugene Fama, then a doctoral student at Chicago, found support for him "
            "in his thesis, and for a decade the question was open."
        ) as vo:
            self.play(FadeIn(c1, shift=RIGHT * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(c2, shift=RIGHT * 0.2))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(p) for p in pts], lag_ratio=0.5, run_time=3))
        self.wait(0.4)
        self.clear_scene()

    def _axes(self, m, ylabel, yr, yticks, yfmt):
        t = np.asarray(m["t"])
        g = axes([1926, 2021], yr, x_length=8.0, y_length=4.6, xlabel=r"data used: from July 1926 up to\dots",
                 ylabel=ylabel, xticks=[1930, 1950, 1970, 1990, 2010], yticks=yticks, xfmt=lambda v: f"{int(v)}",
                 yfmt=yfmt, font_size=18).to_edge(LEFT, buff=0.7).shift(DOWN * 0.3)
        return g, t

    def running_sd(self, m):
        g, t = self._axes(m, r"running standard deviation, annualized (log scale)", [np.log10(0.05), np.log10(300)],
                          [np.log10(0.1), 0, 1, 2], lambda v: f"{100 * 10 ** v:,.0f}\\%".replace(",", "{,}"))
        ax = g.ax
        lines = {}
        for key, col, sw in (("gauss", GAUSS, 2.5), ("t3", T3, 2.5), ("cauchy", CAU, 2.5), ("real", REAL, 3.5)):
            y = np.log10(np.clip(np.asarray(m[f"sd_{key}"]), 0.051, 299))
            lines[key] = curve(ax, t, y, col, stroke_width=sw)
        leg = legend([(REAL, r"the US market"), (GAUSS, r"bell curve"), (T3, r"Student $t$, 3 degrees of freedom "
                                                                              r"($\alpha = 3$)"),
                      (CAU, r"Cauchy, a stable law ($\alpha = 1$)")], font_size=21)
        leg.to_edge(RIGHT, buff=0.35).shift(UP * 1.8)
        note_ = wrapped_label(r"each simulated series: the market's length, scale and mean; the same random seed "
                              r"every render", 3.6, 18, GREY_B).next_to(leg, DOWN, buff=0.4).align_to(leg, LEFT)
        end = MathTex(rf"{100 * m['sd_real'][-1]:.1f}\%", font_size=30, color=REAL)
        end.next_to(ax.c2p(2021, np.log10(m["sd_real"][-1])), RIGHT, buff=0.1)
        with self.voiceover(
            "Here is the test he proposed. Estimate the standard deviation from more and more data, and watch "
            "whether it settles. <bookmark mark='a'/> For a bell curve, the grey line, it settles almost at once. "
            "<bookmark mark='b'/> For a stable law with infinite variance, a Cauchy distribution, in pink, it never "
            "does: every so often a single draw is so large that it resets the estimate, and it climbs forever. "
            "<bookmark mark='c'/> The market, in blue, behaves like the bell curve here: after the turbulence of "
            f"the 1930s its standard deviation settles near {100 * m['sd_real'][-1]:.0f} percent a year and stays "
            "there. This supports a finite variance, rather than proving one from a finite sample. Later studies, "
            "measuring a tail exponent near three and thinning tails at longer horizons, also favoured finite "
            "variance over Mandelbrot's stable-law model."
        ) as vo:
            self.play(FadeIn(g), FadeIn(note_))
            vo.wait_until("a")
            self.play(Create(lines["gauss"]), FadeIn(leg[1]))
            vo.wait_until("b")
            self.play(Create(lines["cauchy"]), FadeIn(leg[3]), run_time=2)
            self.play(Create(lines["t3"]), FadeIn(leg[2]))
            vo.wait_until("c")
            self.play(Create(lines["real"]), FadeIn(leg[0]), run_time=3)
            self.play(FadeIn(end))
        self.wait(0.4)
        self.clear_scene()

    def running_kurt(self, m):
        g, t = self._axes(m, r"running excess kurtosis", [-2, 90], [0, 20, 40, 60, 80], lambda v: f"{v:g}")
        ax = g.ax
        lines = {}
        for key, col, sw in (("gauss", GAUSS, 2.5), ("t3", T3, 2.5), ("real", REAL, 3.5)):
            lines[key] = curve(ax, t, np.clip(np.asarray(m[f"kurt_{key}"]), -2, 89), col, stroke_width=sw)
        leg = legend([(REAL, r"the US market"), (GAUSS, r"bell curve"), (T3, r"Student $t$ ($\alpha = 3$)")],
                     font_size=21).to_edge(RIGHT, buff=0.4).shift(UP * 1.8)
        jump = Arrow(ax.c2p(1981, 40), ax.c2p(1987.8, 22), buff=0.05, color=TAIL, stroke_width=3,
                     max_tip_length_to_length_ratio=0.15)
        jl = label(r"19 October 1987", font_size=22, color=TAIL).next_to(jump.get_start(), UP, buff=0.05)
        kr = np.asarray(m["kurt_real"])
        i87 = int(np.searchsorted(t, 1987.8))
        k_before, k_after = float(kr[i87 - 1]), float(kr[i87])
        with self.voiceover(
            "The kurtosis is another story. Here is the same experiment for the fourth moment. "
            "<bookmark mark='a'/> The bell curve's settles at zero. The Student t with three degrees of freedom, "
            "whose tails fall like the cube, as the market's do, has a variance but no fourth moment, and its "
            "kurtosis never settles: it jumps up with each extreme draw. <bookmark mark='b'/> The market's looks "
            "the same: calm decades, and then a step. In October 1987 a single day lifted the kurtosis of sixty "
            f"years of data from {k_before:.0f} to {k_after:.0f}."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(Create(lines["gauss"]), FadeIn(leg[1]))
            self.play(Create(lines["t3"]), FadeIn(leg[2]), run_time=2)
            vo.wait_until("b")
            self.play(Create(lines["real"]), FadeIn(leg[0]), run_time=3)
            self.play(GrowArrow(jump), FadeIn(jl))
        self.wait(0.4)
        self.clear_scene()

    def lesson(self, m):
        big = MathTex(rf"{100 * m['share87']:.0f}\%", font_size=110, color=TAIL)
        cap = wrapped_label(r"of the fourth-power mass of 94 years, $\sum (r_t - \bar r)^4$, comes from one day: "
                            r"19 October 1987", 9.0, 30, GREY_A)
        grp = VGroup(big, cap).arrange(DOWN, buff=0.3).shift(UP * 1.4)
        nums = MathTex(rf"\text{{kurtosis}}\ {m['kurt_all']:.1f}\ \longrightarrow\ {m['kurt_no87']:.1f}\ "
                       rf"\text{{without that day}}", font_size=36).next_to(grp, DOWN, buff=0.5)
        take = VGroup(
            label(r"finite variance: supported by the evidence; volatility still moves (Part 7)", font_size=26, color=REAL),
            label(r"kurtosis: unreliable; measure tails with an exponent, or directly (Part 40)", font_size=26,
                  color=TAIL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(nums, DOWN, buff=0.6)
        with self.voiceover(
            "How much can one day weigh? The kurtosis is built from fourth powers of returns. Add up the fourth "
            f"powers of all ninety-four years: {100 * m['share87']:.0f} percent of the total comes from a single "
            "day, the 19th of October 1987. <bookmark mark='a'/> Remove that day and the kurtosis drops from "
            f"{m['kurt_all']:.1f} to {m['kurt_no87']:.1f}. A statistic that one day can move by a fifth is a "
            "description of that day, not of the market. <bookmark mark='b'/> So the verdict on Mandelbrot is "
            "split. The evidence supports using a finite variance, carefully, because volatility moves over time. The "
            "fourth moment is a different matter: tails should be measured as tails, with an exponent or directly, "
            "and that is how Part forty will measure risk."
            " If returns are this hard to pin down, can anyone predict them? Next: efficient markets."
        ) as vo:
            self.play(FadeIn(big, scale=1.2), FadeIn(cap))
            vo.wait_until("a")
            self.play(FadeIn(nums))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(x) for x in take], lag_ratio=0.5))
        self.wait(0.5)
        self.clear_scene()
