from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant6.common import BAD, EST, GOOD, PART, load

OLS_C, ARM_C, X_C = BAD, GOOD, EST


class Research(VoiceoverScene):
    def construct(self):
        t = load("predreg_theory")
        self.card()
        self.recall()
        self.unit_root()
        self.laws(t)
        self.size(t)
        self.open_problems()
        self.question()

    def card(self):
        c = research_card(r"Predictive regressions near a unit root", r"Why doesn't more data fix the predictive "
                          r"$t$-test?", part=PART)
        with self.voiceover("For the researcher: Chapter 5 corrected the predictive regression's bias. Here is why the "
                            "t-test itself fails near a unit root, and why a longer sample does not save it."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def recall(self):
        rows = [cmath(r"r_{t+1}", r"=", r"\alpha + \beta x_t + u_{t+1},\quad x_{t+1} = \mu + \rho x_t + v_{t+1}", font_size=32,
                      colors={r"r_{t+1}": QC.SPOT}),
                cmath(r"\hat\beta - \beta", r"=", r"\tfrac{\sigma_{uv}}{\sigma_v^2}(\hat\rho - \rho) + \frac{\sum (x_t - \bar x)"
                      r"e_{t+1}}{\sum (x_t - \bar x)^2}", font_size=32, colors={r"\hat\beta - \beta": OLS_C})]
        whys = [why(r"Chapter 5's predictive system: a persistent predictor, shocks correlated at $\phi \approx -0.9$"),
                why(r"Chapter 5's decomposition: the slope's error is the persistence error, scaled, plus a well-behaved "
                    r"term. Stambaugh's bias is its mean; this chapter is about its distribution")]
        step = ladder(self, rows, whys, keep=2, top=2.4, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "Recall Chapter 5. <bookmark mark='a'/> The predictive system: returns on a persistent predictor, with "
            "correlated shocks. <bookmark mark='b'/> And the decomposition: the slope's error is the persistence "
            "error, scaled, plus a term that behaves. Stambaugh's bias is the mean of that first term. The question "
            "now is its whole distribution, because a test lives in the tails."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
        self.wait(0.5)
        self.clear_scene()

    def unit_root(self):
        rows = [cmath(r"\rho", r"=", r"1 + \tfrac{c}{T}", font_size=34, colors={r"\rho": X_C}),
                cmath(r"T(\hat\rho - \rho)", r"\Rightarrow", r"\frac{\int J_c^\mu\,dW_v}{\int (J_c^\mu)^2}", font_size=34,
                      colors={r"T(\hat\rho - \rho)": X_C}),
                cmath(r"t_{\hat\beta}", r"\Rightarrow", r"\phi\,\frac{\int J_c^\mu\,dW_v}{\sqrt{\int (J_c^\mu)^2}} + "
                      r"\sqrt{1 - \phi^2}\;Z", font_size=34, colors={r"t_{\hat\beta}": OLS_C}),
                cmath(r"c = 0", r":", r"\phi\,\tau_{DF} + \sqrt{1 - \phi^2}\,Z,\quad \mathbb E\,\tau_{DF} \approx -1.5",
                      font_size=34, colors={r"c = 0": OLS_C})]
        whys = [why(r"For this law: zero predictor drift and initial value, iid shocks, no trend; an intercept is fitted. "
                    r"Local to unity: $\rho=1+c/T$ (Phillips; Chan--Wei 1987)."),
                why(r"the persistence estimate converges at rate $T$, not $\sqrt T$, to a ratio of stochastic integrals of "
                    r"the demeaned Ornstein--Uhlenbeck process $J_c^\mu$, a non-normal law (Dickey and Fuller at $c = 0$)"),
                why(r"Elliott and Stock (1994); Cavanagh, Elliott and Stock (1995): the slope's $t$ mixes that law, weighted "
                    r"by $\phi$, with an independent normal for the part of $u$ unrelated to $v$"),
                why(r"at a unit root $\tau_{DF}$ is skewed left with mean near $-1.5$; with $\phi < 0$ the $t$-statistic is "
                    r"shifted right, and nothing in the limit depends on $T$")]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-0.3, buff=0.42, edge=6.9)
        with self.voiceover(
            "The tool is the local-to-unity device. For the displayed law, assume zero predictor drift and initial "
            "value, iid shocks and no trend, while fitting an intercept. <bookmark mark='a'/> Let the root approach one as the sample "
            "grows, so that it stays near one at every sample size. <bookmark mark='b'/> Then the persistence estimate "
            "converges faster than usual, at rate T, and to a law that is not normal: a ratio of stochastic integrals "
            "of an Ornstein-Uhlenbeck process, the Dickey-Fuller law when the root is exactly one. <bookmark "
            "mark='c'/> The slope's t-statistic inherits it: phi times that ratio, plus an independent normal for the "
            "rest of the return shock. <bookmark mark='d'/> At a unit root the Dickey-Fuller part is skewed left with a "
            "mean near minus one and a half, so with phi negative the t-statistic is shifted right. And nothing in this "
            "limit depends on the sample size: more data do not cure it."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
        self.wait(0.5)
        self.clear_scene()

    def laws(self, t):
        e = np.linspace(-4, 6, 41)
        c = (e[:-1] + e[1:]) / 2
        g = axes([-4, 6], [0, 0.45], x_length=8.2, y_length=3.8, xlabel=r"$t$-statistic of $\hat\beta$, $\beta = 0$",
                 ylabel=r"density", xticks=[-2, 0, 1.645, 4], yticks=[], font_size=13).move_to(LEFT * 1.4 + DOWN * 0.3)
        ax = g.ax
        xs = np.linspace(-4, 6, 300)
        nrm = curve(ax, xs, np.exp(-xs ** 2 / 2) / np.sqrt(2 * np.pi), WHITE, stroke_width=2.5)
        crit = DashedLine(ax.c2p(1.645, 0), ax.c2p(1.645, 0.45), color=GREY_B, stroke_width=1.5)
        lines = VGroup()
        for key, col in (("ols", OLS_C), ("c", ARM_C)):
            h = np.asarray(t["t_hist"][key], float)
            h = h / t["M"] / (e[1] - e[0])
            lines.add(curve(ax, c, h, col, stroke_width=3))
        th = t["t_hist"]
        leg = legend([(WHITE, r"$N(0, 1)$"), (OLS_C, rf"OLS $t$, mean {th['mean_ols']:.2f}"),
                      (ARM_C, rf"augmented $t$, mean {th['mean_c']:.2f}")], font_size=17).to_edge(RIGHT, buff=0.3).shift(UP * 1.4)
        fit_right(leg)
        side = wrapped_label(rf"{t['M']} samples of 100 years, $\rho = 0.99$, $\phi = {t['phi']}$; grey: the one-sided 5\% "
                             r"critical value", 3.2, 15, GREY_A).next_to(leg, DOWN, buff=0.35)
        fit_right(side)
        with self.voiceover(
            "Here are the two laws, simulated at a persistence of point nine nine. <bookmark mark='a'/> The OLS "
            "t-statistic, with no predictability at all, is centred well to the right of zero, and a third of it lies "
            "beyond the one-sided critical value. <bookmark mark='b'/> The augmented regression's t, with Chapter 5's "
            "correction, sits much closer to the standard normal."
        ) as vo:
            self.play(FadeIn(g), Create(nrm), Create(crit), FadeIn(leg), FadeIn(side))
            vo.wait_until("a")
            self.play(Create(lines[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(lines[1]), run_time=1.5)
        self.wait(0.4)
        self.clear_scene()

    def size(self, t):
        rhos = [0.8, 0.9, 0.95, 0.99, 1.0]
        g = axes([-0.6, len(rhos) - 0.4], [0, 0.5], x_length=8.4, y_length=4.0, xlabel=r"persistence $\rho$",
                 ylabel=r"rejection rate of a nominal 5\% one-sided test, $\beta = 0$", xticks=[],
                 yticks=[0, 0.05, 0.2, 0.4], yfmt=lambda v: rf"{100 * v:.0f}\%", font_size=13).move_to(LEFT * 1.4 + DOWN * 0.3)
        ax = g.ax
        bars, labs = VGroup(), VGroup()
        for i, r in enumerate(rhos):
            d = t["grid"][f"100_{r}"]
            for j, (k, col) in enumerate((("size_ols", OLS_C), ("size_c", ARM_C))):
                v = d[k]
                y0, y1 = ax.c2p(0, 0)[1], ax.c2p(0, v)[1]
                bars.add(Rectangle(width=0.32 * (ax.c2p(1, 0)[0] - ax.c2p(0, 0)[0]), height=max(y1 - y0, 0.01),
                                   stroke_width=0, fill_color=col, fill_opacity=0.85).move_to(
                    [ax.c2p(i + (j - 0.5) * 0.36, 0)[0], (y0 + y1) / 2, 0]))
            labs.add(MathTex(rf"{r}", font_size=18, color=GREY_B).next_to(ax.c2p(i, 0), DOWN, buff=0.12))
        nom = DashedLine(ax.c2p(-0.6, 0.05), ax.c2p(len(rhos) - 0.4, 0.05), color=WHITE, stroke_width=1.5)
        g5 = t["grid"]
        side = VGroup(
            MathTex(rf"T = 500,\ \rho = 1:\ {100 * g5['500_1.0']['size_ols']:.0f}\%", font_size=24, color=OLS_C),
            MathTex(rf"T = 500,\ \rho = 0.95:\ {100 * g5['500_0.95']['size_ols']:.0f}\%", font_size=24, color=OLS_C),
            wrapped_label(r"red: the OLS $t$-test; green: Amihud and Hurvich's augmented regression (Chapter 5). "
                          r"$T$ = 100 unless marked; $\phi = -0.95$", 3.2, 15, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.3).shift(UP * 1.0)
        fit_right(side)
        with self.voiceover(
            "Across persistence. <bookmark mark='a'/> With no predictability, a five percent one-sided t-test rejects "
            "one time in ten at rho of point eight, one in five at point nine five, a third of the time at point nine "
            "nine, and more than two times in five at a unit root. <bookmark mark='b'/> Five hundred years instead of "
            "one hundred help only away from one: at point nine five the size falls to nine percent, but at a unit "
            "root it stays above forty, as the theorem says. <bookmark mark='c'/> The augmented regression holds "
            "between five and nine percent everywhere; IVX, from Chapter 5, is built to be right at every rho at once."
        ) as vo:
            self.play(FadeIn(g), FadeIn(labs), Create(nom))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars[0::2]], lag_ratio=0.12))
            vo.wait_until("b")
            self.play(FadeIn(side[:2]))
            vo.wait_until("c")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars[1::2]], lag_ratio=0.12), FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()

    def open_problems(self):
        cards = VGroup(
            desk_question(r"open: uniformly valid and powerful", r"Campbell and Yogo's (2006) Bonferroni intervals and IVX "
                          r"(Kostakis, Magdalinos and Stamatogiannakis 2015) are valid across $\rho$; which is more "
                          r"powerful depends on the true $\rho$, and no test is best for all", width=12.4, font_size=18),
            desk_question(r"open: many predictors at once", r"several persistent predictors with correlated shocks, or a "
                          r"high-dimensional set (Part 27): the local-to-unity theory for joint tests is incomplete",
                          width=12.4, font_size=18),
            desk_question(r"open: breaks against near unit roots", r"a shift in the predictor's mean looks like a root near "
                          r"one (Lettau and Van Nieuwerburgh 2008), and the two are hard to tell apart in a century of data",
                          width=12.4, font_size=18),
        ).arrange(DOWN, buff=0.22)
        with self.voiceover(
            "Three open questions. <bookmark mark='a'/> Bonferroni intervals and IVX are both valid whatever the "
            "persistence; which is more powerful depends on the persistence you cannot know, and no test is best for "
            "all. <bookmark mark='b'/> Several persistent predictors at once, or the hundreds of Part 27, have no "
            "complete local-to-unity theory. <bookmark mark='c'/> And a break in the predictor's mean looks like a "
            "root near one; in a century of data the two are hard to tell apart."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"with $\phi = -1$ and $\rho = 1$, the OLS $t$ of $\hat\beta$ is exactly minus the Dickey--Fuller $t$ "
                       r"of $\hat\rho$. Roughly how often does a nominal 5\% one-sided test then reject?")
        with self.voiceover(
            "Pause and predict. When the shocks are perfectly negatively correlated and the root is one, the slope's t "
            "is exactly minus the Dickey-Fuller t of the persistence. Roughly how often does a nominal five percent "
            "one-sided test then reject?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
