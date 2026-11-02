from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant4.common import DRIFT, MART, P_C, PART, load, real_data


class Doob(VoiceoverScene):
    def construct(self):
        d = load("doob")
        self.card()
        self.theorem(d)
        self.market(d)
        self.square(d)

    def card(self):
        c = chapter_card(5, r"Doob's decomposition", r"How much of a price is predictable?", part=PART)
        with self.voiceover("Chapter five. Doob's decomposition."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def theorem(self, d):
        th = theorem_card(r"Doob decomposition",
                          r"Any adapted process with finite means splits, uniquely, as $X_n = X_0 + A_n + M_n$: $A$ is "
                          r"predictable (each step known one period ahead), $A_n = \sum_{k \le n} \mathbb{E}[X_k - X_{k-1} "
                          r"\mid \mathcal{F}_{k-1}]$, and $M$ is a martingale.", who=r"Doob (1953)", color=DRIFT,
                          width=9.6, font_size=24).to_edge(UP, buff=0.4)
        x, A, M = (np.asarray(d[k]) for k in ("coin_x", "coin_A", "coin_M"))
        n = np.arange(len(x))
        g = axes([0, 400], [-20, 60], x_length=8.0, y_length=3.4, xlabel=r"tosses of a coin that lands heads 55\% of "
                 r"the time", xticks=[0, 100, 200, 300, 400], yticks=[-20, 0, 20, 40, 60], font_size=18)
        g.next_to(th, DOWN, buff=0.45).to_edge(LEFT, buff=0.8)
        ax = g.ax
        lx = curve(ax, n, x, P_C, stroke_width=3)
        la = curve(ax, n, A, DRIFT, stroke_width=3)
        lm = curve(ax, n, M, MART, stroke_width=2.5)
        leg = legend([(P_C, r"the walk $X_n$"), (DRIFT, r"its drift $A_n = 0.1\,n$"), (MART, r"the martingale "
                      r"$M_n = X_n - A_n$")], font_size=21).next_to(g, RIGHT, buff=0.4).align_to(g, UP)
        with self.voiceover(
            "Most processes are not martingales: prices drift. Doob showed that any process with finite means splits, "
            "in exactly one way, into a predictable part and a martingale. The predictable part adds up, step by "
            "step, the expected change given what was known the step before. What is left over is a fair game. "
            "<bookmark mark='a'/> Take a coin that lands heads fifty-five percent of the time, and a walk that steps "
            "up on heads and down on tails. <bookmark mark='b'/> Its expected step is a tenth, so the predictable part "
            "is a straight line of slope a tenth. <bookmark mark='c'/> And the walk minus that line is a martingale: "
            "all of the surprise, none of the drift."
        ) as vo:
            self.play(FadeIn(th, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(g), Create(lx), FadeIn(leg[0]), run_time=2)
            vo.wait_until("b")
            self.play(Create(la), FadeIn(leg[1]))
            vo.wait_until("c")
            self.play(Create(lm), FadeIn(leg[2]))
        self.wait(0.4)
        self.clear_scene()

    def market(self, d):
        t = np.asarray(d["t"])
        X, A, M = (np.asarray(d[k]) for k in ("X", "A", "M"))
        g = axes([1926, 2021], [-2, 10], x_length=8.0, y_length=4.6, ylabel=r"log of wealth from \$1 in the US market",
                 xticks=[1930, 1960, 1990, 2020], xfmt=lambda u: f"{int(u)}", yticks=[-2, 0, 2, 4, 6, 8, 10],
                 font_size=18).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        lx = curve(ax, t, X, P_C, stroke_width=3)
        la = curve(ax, t, A, DRIFT, stroke_width=3)
        lm = curve(ax, t, M, MART, stroke_width=2.5)
        side = VGroup(
            legend([(P_C, r"log wealth $X$"), (DRIFT, r"predictable drift $A$"), (MART, r"martingale $M$")], font_size=21),
            MathTex(rf"{d['X_end']:.2f}", r"=", rf"{d['A_end']:.2f}", r"+", rf"{d['M_end']:.2f}", font_size=36),
            label(rf"\$1 became \${np.exp(d['X_end']):,.0f}".replace(",", "{,}"), font_size=22, color=GREY_A),
            wrapped_label(r"drift as known each day: the average daily return up to the day before", 4.2, 20, GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.5)
        side[1][0].set_color(P_C)
        side[1][2].set_color(DRIFT)
        side[1][4].set_color(MART)
        src = real_data(r"Kenneth French's daily US market (value-weighted, with dividends), July 1926 -- December 2020")
        with self.voiceover(
            "Now the market. Here is the logarithm of a dollar invested in the American market in 1926, with "
            "dividends reinvested. <bookmark mark='a'/> Split it the way Doob says. For the predictable part, use "
            "what an investor could have known each day: the average daily return up to the day before. Add those "
            "forecasts up. <bookmark mark='b'/> What's left is the martingale, the market's surprises. "
            f"<bookmark mark='c'/> By the end of 2020 a dollar had become about {np.exp(d['X_end']):,.0f}. Of the "
            "nine log points it gained, a little over seven were the predictable drift, and under two were luck. "
            "Over decades the drift dominates; over a day or a year, the martingale does, which is why the drift is so "
            "hard to see."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), Create(lx), FadeIn(side[0][0]), run_time=2)
            vo.wait_until("a")
            self.play(Create(la), FadeIn(side[0][1]), FadeIn(side[3]))
            vo.wait_until("b")
            self.play(Create(lm), FadeIn(side[0][2]))
            vo.wait_until("c")
            self.play(FadeIn(side[1]), FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()

    def square(self, d):
        t = np.asarray(d["t"])
        M2, A2, qv = (np.asarray(d[k]) for k in ("M2", "A2", "qv"))
        g = axes([1926, 2021], [0, 5], x_length=8.0, y_length=4.4, ylabel=r"squared martingale and its compensator",
                 xticks=[1930, 1960, 1990, 2020], xfmt=lambda u: f"{int(u)}", yticks=[0, 1, 2, 3, 4, 5], font_size=18)
        g.to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        lm = curve(ax, t, M2, MART, stroke_width=2.5)
        la = curve(ax, t, A2, DRIFT, stroke_width=3.5)
        lq = DashedVMobject(curve(ax, t, qv, WHITE, stroke_width=2), num_dashes=80)
        side = VGroup(
            legend([(MART, r"$M_n^2$"), (DRIFT, r"$\sum$ each day's variance forecast"),
                    (WHITE, r"$\sum$ realized squared surprises")], font_size=21),
            MathTex(rf"{d['A2_end']:.3f}\ \text{{vs}}\ {d['qv_end']:.3f}", font_size=34),
            wrapped_label(r"$M^2$ minus its compensator is a martingale: the variance is the predictable part of the "
                          r"square. Part 5 calls the realized sum the quadratic variation, and builds It\^o's calculus "
                          r"on it.", 4.4, 21, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "Doob's decomposition has a second use. Square the martingale. A squared fair game is not fair: it drifts "
            "up, because surprises of either sign add to it. <bookmark mark='a'/> Its predictable part is the sum of "
            "each day's variance forecast, here a simple weighted average of recent squared surprises, known the day "
            "before. <bookmark mark='b'/> And the sum of the squared surprises that actually happened, day by day, "
            "lands almost exactly on it: two point eight nine against two point eight nine. <bookmark mark='c'/> The "
            "variance is the predictable part of the square. Part five calls that realized sum the quadratic "
            "variation, and builds the whole of Itô's calculus on it."
        ) as vo:
            self.play(FadeIn(g), Create(lm), FadeIn(side[0][0]), run_time=2)
            vo.wait_until("a")
            self.play(Create(la), FadeIn(side[0][1]))
            vo.wait_until("b")
            self.play(Create(lq), FadeIn(side[0][2]), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()
