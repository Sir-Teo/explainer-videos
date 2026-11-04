from __future__ import annotations

import math

import numpy as np

from explainer.quant import *  # noqa: F403
from explainer.quant.house import statarb as SA
from videos.quant.quant33.common import BAD, GOOD, HURDLE, OU_C, PART, RES_C, SPREAD_C, fit_right, illustration


class OU(VoiceoverScene):
    def construct(self):
        self.card()
        self.model()
        self.discrete()
        self.path()
        self.sscore()
        self.bias()
        self.rules()
        self.question()

    def card(self):
        c = chapter_card(4, r"The Ornstein--Uhlenbeck spread", r"How fast does a gap close, and how sure can we be?",
                         part=PART)
        with self.voiceover("Chapter four. A spread that reverts needs a model of how it reverts. The simplest, and the "
                            "one the industry uses, is Part five's Ornstein-Uhlenbeck process."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def model(self):
        rows = [cmath(r"dX_t", r"=", r"\kappa(\theta - X_t)\,dt + \sigma\,dW_t", font_size=40, colors={r"\kappa": OU_C}),
                cmath(r"X_t \mid X_0", r"\sim", r"N\Big(\theta + (X_0 - \theta)e^{-\kappa t},\ \frac{\sigma^2}{2\kappa}"
                      r"\big(1 - e^{-2\kappa t}\big)\Big)", font_size=30),
                cmath(r"s_{\text{eq}}", r"=", r"\frac{\sigma}{\sqrt{2\kappa}},\qquad t_{1/2} = \frac{\ln 2}{\kappa}",
                      font_size=36, colors={r"t_{1/2}": OU_C})]
        whys = [why(r"the spread is pulled toward $\theta$ at speed $\kappa$ and shaken by noise of size $\sigma$"),
                why(r"Part 5's exact solution: the expected gap decays exponentially, the variance settles"),
                why(r"the equilibrium standard deviation, and the half-life: the time for the expected gap to halve")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "The model. <bookmark mark='a'/> The spread is pulled toward its mean theta at speed kappa, and shaken by "
            "noise. <bookmark mark='b'/> Its distribution at any future time is exact: the expected gap decays "
            "exponentially, and the variance settles at sigma squared over two kappa. <bookmark mark='c'/> Two numbers "
            "describe a spread for a trader: its equilibrium standard deviation, which sets the size of the bets, and "
            "its half-life, which sets how long they last."
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

    def discrete(self):
        rows = [cmath(r"X_{t+1}", r"=", r"a + b\,X_t + \varepsilon_{t+1}", font_size=38),
                cmath(r"b", r"=", r"e^{-\kappa\Delta t},\quad a = \theta(1 - b),\quad \operatorname{Var}\varepsilon = "
                      r"s_{\text{eq}}^2(1 - b^2)", font_size=30),
                cmath(r"\hat\kappa", r"=", r"-\ln\hat b/\Delta t,\quad \hat t_{1/2} = \ln 2/\hat\kappa", font_size=34)]
        whys = [why(r"sampled at intervals $\Delta t$, the OU process is exactly an AR(1)"),
                why(r"so its parameters map one to one onto the regression's"),
                why(r"fit by least squares on the spread's own history: the House's \texttt{ou\_fit}")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "Estimation is a regression. <bookmark mark='a'/> Sampled daily, the OU process is exactly a first-order "
            "autoregression. <bookmark mark='b'/> Its slope is e to the minus kappa, its intercept and noise give theta "
            "and the equilibrium spread. <bookmark mark='c'/> So the House fits a spread by least squares on its own "
            "history, and reads the half-life off the slope."
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

    def path(self):
        rng = np.random.default_rng(5)
        T = 300
        b = math.exp(-math.log(2) / 10)
        x = np.zeros(T)
        for t in range(1, T):
            x[t] = b * x[t - 1] + math.sqrt(1 - b * b) * rng.standard_normal()
        g = axes([0, T], [-3.2, 3.2], x_length=8.6, y_length=4.2, xlabel=r"days", ylabel=r"spread, in $s_{\text{eq}}$",
                 xticks=[0, 100, 200, 300], yticks=[-2, 0, 2], font_size=15).move_to(LEFT * 0.8 + DOWN * 0.2)
        ax = g.ax
        c = curve(ax, np.arange(T), x, SPREAD_C, stroke_width=2.5)
        bands = VGroup(*[DashedLine(ax.c2p(0, k), ax.c2p(T, k), color=OU_C, stroke_width=1.5) for k in (-1.25, 1.25)])
        zero = DashedLine(ax.c2p(0, 0), ax.c2p(T, 0), color=GREY_C, stroke_width=1)
        f = SA.ou_fit(x)
        st = VGroup(label(r"true half-life 10 days", font_size=17, color=GREY_A),
                    label(rf"fitted on these 300 days: {f['half_life']:.1f}", font_size=17, color=OU_C))
        st.arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_edge(RIGHT, buff=0.4).shift(UP * 2.4)
        fit_right(st)
        ill = illustration(r"illustration: a simulated OU spread; dashed, $\pm 1.25\,s_{\text{eq}}$")
        with self.voiceover(
            "A simulated spread with a half-life of ten days. <bookmark mark='a'/> It crosses its mean often and "
            "rarely stays far for long. <bookmark mark='b'/> The dashed lines are one and a quarter equilibrium "
            "deviations, where Avellaneda and Lee open a trade. Fitted on these three hundred days, the half-life comes "
            f"out at {f['half_life']:.1f} days. Close, on a long sample. Next, on a short one."
        ) as vo:
            self.play(FadeIn(g), Create(zero), FadeIn(ill))
            vo.wait_until("a")
            self.play(Create(c), run_time=2.5)
            vo.wait_until("b")
            self.play(Create(bands), FadeIn(st))
        self.wait(0.4)
        self.clear_scene()

    def sscore(self):
        rows = [cmath(r"s_t", r"=", r"\frac{X_t - \hat\theta}{\hat s_{\text{eq}}}", font_size=40, colors={r"s_t": RES_C}),
                cmath(r"\text{open}", r":", r"|s_t| > 1.25;\quad \text{close long at } s > -0.5,\ \text{short at } s < 0.75",
                      font_size=30),
                cmath(r"\text{require}", r":", r"\hat t_{1/2} < \text{half the estimation window}", font_size=30)]
        whys = [why(r"the s-score: how many equilibrium deviations the spread sits from its fitted mean"),
                why(r"Avellaneda and Lee's (2010) thresholds, chosen by them on US stocks"),
                why(r"a spread that reverts too slowly to be estimated in the window is not traded")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "The trading signal is the s-score. <bookmark mark='a'/> The spread's distance from its fitted mean, in "
            "equilibrium deviations. <bookmark mark='b'/> Marco Avellaneda and Jeong-Hyun Lee opened at one and a "
            "quarter and closed near the mean, with thresholds they chose on American stocks. <bookmark mark='c'/> And "
            "they traded only spreads whose fitted half-life was short enough to be estimated at all. Why those "
            "thresholds, and not others, is the research chapter's question."
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

    def bias(self):
        rng = np.random.default_rng(55)
        b = math.exp(-math.log(2) / 10)
        out = {}
        for n in (30, 60, 250):
            hl = []
            for _ in range(1500):
                x = np.zeros(n)
                x[0] = rng.standard_normal()
                for t in range(1, n):
                    x[t] = b * x[t - 1] + math.sqrt(1 - b * b) * rng.standard_normal()
                f = SA.ou_fit(x)
                hl.append(f["half_life"])
            hl = np.array(hl)
            out[n] = (float(np.median(hl[np.isfinite(hl)])), float(np.mean(~np.isfinite(hl))))
        rows = [cmath(r"\mathbb E\,\hat b", r"\approx", r"b - \frac{1 + 3b}{T}", font_size=38, colors={r"\mathbb E\,\hat b": BAD}),
                cmath(r"T = 30,\ 60,\ 250", r":", rf"\text{{median }}\hat t_{{1/2}} = {out[30][0]:.1f},\ {out[60][0]:.1f},\ "
                      rf"{out[250][0]:.1f}\ \text{{days (true 10)}}", font_size=30),
                cmath(r"\text{selection}", r":", r"\text{fast-looking spreads are chosen, so the bias compounds}",
                      font_size=30, colors={r"\text{selection}": BAD})]
        whys = [why(r"the autoregressive slope is biased down in short samples (Kendall 1954), the same bias behind Part "
                    r"6's predictive regressions"),
                why(r"simulated, 1{,}500 samples each: a 60-day window makes a 10-day half-life look much shorter"),
                why(r"a screen that keeps the fastest spreads keeps the most biased estimates")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "On a short one, the estimate is biased. <bookmark mark='a'/> The autoregressive slope is pulled down in "
            "short samples, by about one plus three b over the sample length: Kendall's bias, the same one behind Part "
            "six's predictive regressions. <bookmark mark='b'/> Simulate a ten-day half-life: estimated on thirty days, "
            f"the median comes out at {out[30][0]:.1f}; on sixty, {out[60][0]:.1f}; on a year, {out[250][0]:.1f}. "
            "<bookmark mark='c'/> And a screen that keeps the fastest-looking spreads keeps the most biased estimates. "
            "Spreads look faster than they are."
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

    def rules(self):
        cards = VGroup(
            desk_question(r"Bertram (2010)", r"expected trade length of an OU spread in closed form, and the entry and exit "
                          r"levels that maximise return per unit time", width=12.4, font_size=19),
            desk_question(r"Leung and Li (2015)", r"optimal stopping for entering and leaving a mean-reverting position, "
                          r"with transaction costs and a stop-loss", width=12.4, font_size=19),
            desk_question(r"the House's version", r"the band rule, its exact profit rate, and a universal curve for the "
                          r"best band given costs: proved in the research chapter, from first-passage times", width=12.4,
                          font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Where should the bands be? <bookmark mark='a'/> William Bertram computed the expected length of a trade on "
            "an OU spread in closed form, and the bands that maximise the return per unit time. <bookmark mark='b'/> Tim "
            "Leung and Xin Li treated entry and exit as optimal stopping problems, with costs and a stop-loss. "
            "<bookmark mark='c'/> The research chapter proves a version of its own, from first-passage times, and finds "
            "that the best band, measured in equilibrium deviations, depends only on the cost."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"a spread's daily AR(1) slope is 0.95. What is its half-life, and roughly what would a 60-day "
                       r"sample estimate it as, on average?")
        with self.voiceover(
            "Pause and predict. A spread's daily autoregressive slope is point nine five. What is its half-life, and "
            "roughly what would a sixty-day sample estimate it as, on average?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
