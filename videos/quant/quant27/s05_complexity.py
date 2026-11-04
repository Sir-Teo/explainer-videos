from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant27.common import (BAD, COMPLEX, GOOD, HURDLE, LINEAR, MKT, MOM, NET, PART, TREE, ask, comma,
                                         fit_right, illustration, load)


def _years(ym):
    ym = np.asarray(ym)
    return ym // 100 + (ym % 100 - 0.5) / 12


class Complexity(VoiceoverScene):
    def construct(self):
        k = load("kmz")
        self.card()
        self.setup_rff()
        self.sharpe(k)
        self.r2(k)
        self.descent(load("descent"))
        self.why()
        self.question()

    def card(self):
        c = chapter_card(4, r"The virtue of complexity", r"Can more parameters than data be better?", lit=(2019, 2025),
                         part=PART)
        with self.voiceover("Chapter four. The virtue of complexity: the claim that models with more parameters than "
                            "observations predict returns better than simple ones."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def setup_rff(self):
        rows = [cmath(r"z_j(x)", r"=", r"\sqrt{2/P}\,\big(\sin(w_j^{\top}x),\ \cos(w_j^{\top}x)\big),\quad w_j \sim "
                      r"\mathcal{N}(0, \gamma^2 I)", font_size=34, colors={r"z_j(x)": COMPLEX}),
                cmath(r"\hat\beta(\lambda)", r"=", r"\arg\min_\beta \textstyle\sum_{s = t-12}^{t-1}\big(r_s - "
                      r"\beta^{\top}z(x_{s-1})\big)^2 + \lambda T\,|\beta|^2", font_size=34,
                      colors={r"\hat\beta(\lambda)": COMPLEX}),
                cmath(r"c", r"=", r"P / T", font_size=40, colors={r"c": HURDLE})]
        whys = [why(r"random Fourier features (Rahimi and Recht 2007): a few predictors turned into $P$ random nonlinear "
                    r"functions of them; enough of them approximate any smooth function"),
                why(r"ridge regression on the last $T = 12$ months only, refitted every month, from 1931 to 2020; the "
                    r"forecast for next month times its return is the timing strategy"),
                why(r"the complexity: features per observation. Above 1 the regression can fit the training data exactly; "
                    r"ridge picks the smallest such fit (Kelly, Malamud and Zhou 2024)")]
        step = ladder(self, rows, whys, keep=3, top=2.9, x=-0.5, buff=0.42, edge=6.9)
        with self.voiceover(
            "Bryan Kelly, Semyon Malamud and Kaili Zhou set up a provocative experiment, published in 2024. "
            "<bookmark mark='a'/> Take the fifteen Welch-Goyal predictors and turn them into P random nonlinear "
            "functions: random Fourier features, sines and cosines of random combinations. With enough of them, a "
            "linear model in the features can approximate any smooth function of the predictors. "
            "<bookmark mark='b'/> Fit a ridge regression on only the last twelve months, every month, and use the "
            "forecast to time the market. <bookmark mark='c'/> The complexity is P over T, features per observation. "
            "Above one, the regression can fit its twelve training months exactly, and ridge picks the smallest such "
            "fit. The textbook says that should be a disaster."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def sharpe(self, k):
        c = np.log10(np.asarray(k["c"]))
        S = np.asarray(k["grid"]["sharpe"])
        zs = k["z"]
        g = axes([-1, 3.1], [-0.1, 0.6], x_length=7.4, y_length=4.2, xlabel=r"complexity $c = P/T$",
                 ylabel=r"timing strategy's Sharpe ratio, 1931--2020", xticks=[-1, 0, 1, 2, 3],
                 yticks=[0, 0.2, 0.4, 0.6], log_x=True, font_size=14).to_edge(LEFT, buff=0.5).shift(DOWN * 0.3)
        ax = g.ax
        pick = [(0, r"$\lambda = 10^{-3}$", NET), (2, r"$\lambda = 0.1$", COMPLEX), (4, r"$\lambda = 10$", TREE)]
        lines = [curve(ax, c, S[:, j], col, stroke_width=3) for j, _, col in pick]
        mk = DashedLine(ax.c2p(-1, k["sr_market"]), ax.c2p(3.1, k["sr_market"]), color=MKT, stroke_width=2)
        one = DashedLine(ax.c2p(0, -0.1), ax.c2p(0, 0.6), color=GREY_C, stroke_width=1.5)
        leg = legend([(col, nm) for _, nm, col in pick] + [(MKT, r"holding the market")], font_size=15)
        side = VGroup(leg, MathTex(rf"c = 1000:\ {S[-1, 2]:.2f}", font_size=26, color=COMPLEX),
                      MathTex(rf"c = 1:\ {S[2, 2]:.2f}", font_size=24, color=BAD),
                      wrapped_label(rf"{k['n']} months; 10 draws of the features averaged; positions on returns scaled "
                                    r"by their trailing volatility, as in the paper", 3.4, 15, GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.22).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "Here is the House's replication. <bookmark mark='a'/> At low complexity the timing strategy earns little. "
            "Around the point where the number of features equals the twelve observations, it is at its worst. "
            "<bookmark mark='b'/> And then, past that point, the Sharpe ratio keeps rising, to about a third at a "
            "complexity of a thousand: twelve thousand parameters fitted to twelve data points, doing better than any "
            "small model. That is the virtue of complexity. <bookmark mark='c'/> Notice also the line it does not "
            "reach: simply holding the market, with returns scaled by their volatility, earned point five two."
        ) as vo:
            self.play(FadeIn(g), Create(one))
            vo.wait_until("a")
            self.play(*[Create(l_) for l_ in lines], FadeIn(leg), run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(side[1]), FadeIn(side[2]), FadeIn(side[3]))
            vo.wait_until("c")
            self.play(Create(mk))
        self.add(illustration(r"Welch--Goyal predictors; the House's \texttt{ml.kmz\_timing}"))
        self.wait(0.4)
        self.clear_scene()

    def r2(self, k):
        c = np.log10(np.asarray(k["c"]))
        R = np.asarray(k["grid"]["r2"]) * 100
        g = axes([-1, 3.1], [-15, 2], x_length=7.4, y_length=4.2, xlabel=r"complexity $c = P/T$",
                 ylabel=r"out-of-sample $R^2$, \%", xticks=[-1, 0, 1, 2, 3], yticks=[-15, -10, -5, 0],
                 log_x=True, font_size=14).to_edge(LEFT, buff=0.5).shift(DOWN * 0.3)
        ax = g.ax
        lines = [curve(ax, c, np.clip(R[:, j], -15, 2), col, stroke_width=3) for j, col in ((0, NET), (2, COMPLEX))]
        zero = DashedLine(ax.c2p(-1, 0), ax.c2p(3.1, 0), color=GREY_C, stroke_width=1.5)
        side = VGroup(
            MathTex(rf"c = 1,\ \lambda = 10^{{-3}}:\ {R[2, 0]:.0f}\%", font_size=24, color=BAD),
            MathTex(rf"c = 1000,\ \lambda = 0.1:\ {R[-1, 2]:+.1f}\%", font_size=24, color=COMPLEX),
            wrapped_label(r"the error explodes where the model can just fit its twelve points, and falls again beyond: "
                          r"double descent. Past the peak, extra features spread the fit over more directions, and each "
                          r"forecast becomes smaller and calmer", 3.4, 15, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "The R squared tells the same story more violently. <bookmark mark='a'/> With almost no shrinkage, at a "
            "complexity of exactly one, the out-of-sample R squared is minus forty percent: a model that can just "
            "interpolate twelve points is wildly unstable. Past that peak the error falls again, and at a complexity "
            "of a thousand, with moderate ridge, it is about plus one percent. <bookmark mark='b'/> This shape, error "
            "rising to a peak where parameters equal observations and then falling, is double descent, the phenomenon "
            "AI, Built met in its eighth part. Beyond the peak, every extra feature spreads the fit over more directions, "
            "and each forecast becomes smaller and calmer."
        ) as vo:
            self.play(FadeIn(g), Create(zero))
            vo.wait_until("a")
            self.play(*[Create(l_) for l_ in lines], FadeIn(side[0]), FadeIn(side[1]), run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()

    def descent(self, d):
        c = np.log10(np.asarray(d["c"]))
        g = axes([-2.1, 1.6], [-0.3, 0.05], x_length=7.4, y_length=4.2, xlabel=rf"random features per observation "
                 rf"($N = {comma(d['N'])}$ coin-weeks)", ylabel=r"out-of-sample $R^2$, 2020", xticks=[-2, -1, 0, 1],
                 yticks=[-0.3, -0.2, -0.1, 0], log_x=True, font_size=14).to_edge(LEFT, buff=0.5).shift(DOWN * 0.3)
        ax = g.ax
        r0 = np.clip(np.asarray(d["r2"]["1e-08"]), -0.3, 0.05)
        r1 = np.clip(np.asarray(d["r2"]["0.01"]), -0.3, 0.05)
        l0, l1 = curve(ax, c, r0, NET, stroke_width=3), curve(ax, c, r1, COMPLEX, stroke_width=3)
        peak = DashedLine(ax.c2p(0, -0.3), ax.c2p(0, 0.05), color=GREY_C, stroke_width=1.5)
        leg = legend([(NET, r"ridgeless"), (COMPLEX, r"a little ridge")], font_size=16).next_to(ax, UP, buff=0.1).align_to(
            ax, RIGHT)
        side = wrapped_label(r"the same experiment across coins: next week's return on random features of the 15 "
                             r"characteristics, fitted on 1,000 coin-weeks of 2018--19, tested on 2020. The ridgeless "
                             r"error peaks where features equal observations; a little shrinkage removes the peak"
                             .replace("1,000", "1{,}000"), 3.4, 15, GREY_A).to_edge(RIGHT, buff=0.3)
        with self.voiceover(
            "Double descent is not special to the market's history. <bookmark mark='a'/> Run the same experiment across "
            "coins: next week's return on random features of fifteen characteristics, fitted on a thousand coin-weeks, "
            "tested on 2020. <bookmark mark='b'/> Without shrinkage, the error peaks exactly where the features equal "
            "the observations, and recedes beyond. With a little ridge, the peak disappears. The peak is a property "
            "of interpolation, not of finance; what remains to be shown is whether the far side of it beats the "
            "simple side for a reason."
        ) as vo:
            self.play(FadeIn(g), Create(peak), FadeIn(leg))
            vo.wait_until("a")
            self.play(FadeIn(side))
            vo.wait_until("b")
            self.play(Create(l0), Create(l1), run_time=2.5)
        self.add(illustration(r"Binance coin panel; the House's \texttt{ml.rff}, \texttt{ml.ridge\_dual}"))
        self.wait(0.4)
        self.clear_scene()

    def why(self):
        cards = VGroup(
            desk_question(r"why the far side can work", r"with $P \gg T$ the minimum-norm fit spreads its weight over "
                          r"many directions; its forecasts are biased toward zero but stable: implicit shrinkage",
                          width=12.2, font_size=20),
            desk_question(r"why the peak", r"at $P = T$ the fit is forced through every noisy point with no room to "
                          r"spare; tiny changes in the data swing it wildly", width=12.2, font_size=20),
            desk_question(r"what it does not say", r"that the complex model found something the simple ones missed. "
                          r"That is the next chapter's question", width=12.2, font_size=20),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Why can the far side work at all? <bookmark mark='a'/> With many more features than observations, the "
            "minimum-norm fit spreads its weight across many directions, so its forecasts are pulled toward zero and "
            "become stable: an implicit shrinkage. <bookmark mark='b'/> At the peak, the fit is forced through every "
            "noisy point with no room to spare, and tiny changes in the data swing it wildly. <bookmark mark='c'/> What "
            "the curve does not say is that the complex model found something the simple ones missed. That question "
            "belongs to the critics."
        ) as vo:
            for k_, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k_], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = ask(r"a ridge regression with 12 observations and 12 features has an out-of-sample $R^2$ of $-40\%$; with "
                r"12,000 features, $+1\%$. Which of the two has the larger coefficients, and why?".replace("12,000", "12{,}000"))
        with self.voiceover(
            "Pause and predict. A ridge regression with twelve observations and twelve features has an out-of-sample R "
            "squared of minus forty percent; with twelve thousand features, plus one percent. Which of the two has the "
            "larger coefficients, and why?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
