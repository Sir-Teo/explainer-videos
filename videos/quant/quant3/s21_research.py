from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant3.common import PART, load

OLS_C, ARM_C, X_C = QC.LOSS, QC.GAIN, QC.IDEA


class Research(VoiceoverScene):
    def construct(self):
        t = load("predreg_theory")
        self.card()
        self.model()
        self.bias()
        self.kendall(t)
        self.unit_root()
        self.size(t)
        self.fix(t)
        self.shiller(t)
        self.open_problems()
        self.question()

    def card(self):
        c = research_card(r"Predicting with a persistent predictor", r"Why does a dividend yield look more predictive "
                          r"than it is?", part=PART)
        with self.voiceover("For the researcher: the statistics behind Chapter 9's warning. Why does a valuation ratio, "
                            "regressed on next year's return, look more predictive than it is?"):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def model(self):
        rows = [cmath(r"r_{t+1}", r"=", r"\alpha + \beta x_t + u_{t+1}", font_size=34, colors={r"r_{t+1}": QC.SPOT}),
                cmath(r"x_{t+1}", r"=", r"\mu + \rho x_t + v_{t+1},\quad \rho \approx 1", font_size=34,
                      colors={r"x_{t+1}": X_C}),
                cmath(r"\operatorname{corr}(u_{t+1}, v_{t+1})", r"=", r"\phi \approx -0.9", font_size=34,
                      colors={r"\operatorname{corr}(u_{t+1}, v_{t+1})": OLS_C})]
        whys = [why(r"the predictive regression: next year's return on this year's log dividend yield $x_t$"),
                why(r"the yield is a slow-moving AR(1): its annual autocorrelation is near one"),
                why(r"and its surprises move against returns: when prices jump, the yield falls in the same year, so the "
                    r"two shocks are strongly negatively correlated")]
        step = ladder(self, rows, whys, keep=3, top=2.7, x=-0.3, buff=0.48, edge=6.9)
        with self.voiceover(
            "The model is two equations. <bookmark mark='a'/> Next year's return on this year's dividend yield. "
            "<bookmark mark='b'/> The yield itself follows a slow autoregression, with an autocorrelation close to "
            "one. <bookmark mark='c'/> And the two surprises are tied together: when prices jump, returns are high and "
            "the yield falls at once, so the correlation between the shocks is near minus one. That last fact is the "
            "whole problem."
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
        rows = [cmath(r"u_{t+1}", r"=", r"\tfrac{\sigma_{uv}}{\sigma_v^2}\,v_{t+1} + e_{t+1},\quad e \perp v", font_size=32,
                      colors={r"u_{t+1}": OLS_C}),
                cmath(r"\hat\beta - \beta", r"=", r"\tfrac{\sigma_{uv}}{\sigma_v^2}\,(\hat\rho - \rho) + \frac{\sum (x_t - \bar x)"
                      r"e_{t+1}}{\sum (x_t - \bar x)^2}", font_size=32, colors={r"\hat\beta - \beta": OLS_C}),
                cmath(r"\mathbb E[\hat\beta - \beta]", r"=", r"\tfrac{\sigma_{uv}}{\sigma_v^2}\,\mathbb E[\hat\rho - \rho]",
                      font_size=32, colors={r"\mathbb E[\hat\beta - \beta]": OLS_C}),
                cmath(r"\mathbb E[\hat\rho - \rho]", r"\approx", r"-\frac{1 + 3\rho}{T}", font_size=32,
                      colors={r"\mathbb E[\hat\rho - \rho]": X_C})]
        whys = [why(r"project the return shock on the yield shock; the remainder $e$ is uncorrelated with every $v$, "
                    r"hence with the whole path of $x$"),
                why(r"substitute into OLS: the regressor is the same $x_t$ in both regressions, so the first term is "
                    r"exactly the AR(1) estimation error, scaled"),
                why(r"the second term has mean zero given the path of $x$: Stambaugh (1999)"),
                why(r"Kendall (1954): the AR(1) coefficient is biased down by about $(1 + 3\rho)/T$. With $\sigma_{uv} < 0$, "
                    r"$\hat\beta$ is biased up: the predictor looks better than it is")]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-0.3, buff=0.42, edge=6.9)
        with self.voiceover(
            "Stambaugh's argument takes four lines. <bookmark mark='a'/> Project the return shock on the yield shock: "
            "a multiple of v, plus a remainder e that is uncorrelated with every v, and so with the whole path of the "
            "yield. <bookmark mark='b'/> Substitute into least squares. Because the regressor is the same lagged yield "
            "in both equations, the first term is exactly the error in estimating rho, scaled. <bookmark mark='c'/> "
            "The second term has mean zero. So the bias in beta is the bias in rho, times the regression of one shock "
            "on the other. <bookmark mark='d'/> And Kendall showed in 1954 that rho is biased down by about one plus "
            "three rho over T. With a negative covariance, beta is biased up: the dividend yield looks more predictive "
            "than it is, by a calculable amount."
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

    def kendall(self, t):
        rhos = [0.8, 0.9, 0.95, 0.99, 1.0]
        g = axes([0.78, 1.01], [0, 0.06], x_length=8.0, y_length=4.0, xlabel=r"persistence $\rho$",
                 ylabel=r"mean $\hat\beta - \beta$, $T = 100$, $\phi = -0.95$", xticks=[0.8, 0.9, 1.0],
                 yticks=[0, 0.02, 0.04, 0.06], font_size=13).move_to(LEFT * 1.4 + DOWN * 0.3)
        ax = g.ax
        sim = [t["grid"][f"100_{r}"]["bias"] for r in rhos]
        frm = [t["grid"][f"100_{r}"]["formula"] for r in rhos]
        cor = [t["grid"][f"100_{r}"]["bias_c"] for r in rhos]
        ls = curve(ax, rhos, sim, OLS_C, stroke_width=3)
        lf = DashedLine(ax.c2p(rhos[0], frm[0]), ax.c2p(rhos[-1], frm[-1]), color=WHITE, stroke_width=2)
        lc = curve(ax, rhos, cor, ARM_C, stroke_width=3)
        dots = VGroup(*[Dot(ax.c2p(r, v), radius=0.06, color=OLS_C) for r, v in zip(rhos, sim)])
        leg = legend([(OLS_C, r"OLS, simulated"), (WHITE, r"Stambaugh--Kendall formula"), (ARM_C, r"augmented regression")],
                     font_size=17).to_edge(RIGHT, buff=0.3).shift(UP * 1.4)
        fit_right(leg)
        side = wrapped_label(rf"{t['M']} samples per point. The formula is first order in $1/T$: exact enough at "
                             r"$\rho = 0.8$, too small near one, where the AR(1) estimate is biased by more", 3.4, 15,
                             GREY_A).next_to(leg, DOWN, buff=0.35)
        fit_right(side)
        with self.voiceover(
            "Check it by simulation, a hundred years at a time. <bookmark mark='a'/> The simulated bias in beta, in "
            "red, rises with persistence. <bookmark mark='b'/> The formula, in white, matches it at rho of point "
            "eight, and falls short near one, because Kendall's expansion is first order and the true bias of rho "
            "grows faster as the root approaches unity. <bookmark mark='c'/> The green line is the repair this "
            "chapter ends with, which removes most of the bias at every persistence."
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg))
            vo.wait_until("a")
            self.play(Create(ls), LaggedStart(*[FadeIn(d_) for d_ in dots], lag_ratio=0.2))
            vo.wait_until("b")
            self.play(Create(lf), FadeIn(side))
            vo.wait_until("c")
            self.play(Create(lc))
        self.wait(0.4)
        self.clear_scene()

    def unit_root(self):
        rows = [cmath(r"\rho", r"=", r"1 + \tfrac{c}{T}", font_size=34, colors={r"\rho": X_C}),
                cmath(r"t_{\hat\beta}", r"\Rightarrow", r"\phi\,\frac{\int J_c\,dW_v}{\sqrt{\int J_c^2}} + \sqrt{1 - \phi^2}\;Z",
                      font_size=34, colors={r"t_{\hat\beta}": OLS_C}),
                cmath(r"c = 0", r":", r"\phi\,\tau_{DF} + \sqrt{1 - \phi^2}\,Z,\quad \mathbb E\,\tau_{DF} \approx -1.5",
                      font_size=34, colors={r"c = 0": OLS_C})]
        whys = [why(r"local to unity (Phillips 1987; Elliott and Stock 1994): let persistence approach one as the sample "
                    r"grows, so the root stays 'near one' in every sample size"),
                why(r"the $t$-statistic does not tend to $N(0, 1)$: it mixes a Dickey--Fuller-type functional of the "
                    r"Ornstein--Uhlenbeck process $J_c$ with an independent normal, weighted by $\phi$"),
                why(r"at a unit root, $\tau_{DF}$ is skewed left with mean near $-1.5$; with $\phi < 0$ the $t$-statistic is "
                    r"shifted right. More data do not help: the distortion does not shrink with $T$")]
        step = ladder(self, rows, whys, keep=3, top=2.7, x=-0.3, buff=0.48, edge=6.9)
        with self.voiceover(
            "Near one, the bias is not even the main problem. <bookmark mark='a'/> Let the root approach one as the "
            "sample grows, the local-to-unity device, so that it stays near one at every sample size. <bookmark "
            "mark='b'/> Then the t-statistic of beta does not tend to a standard normal. It tends to a mixture: phi "
            "times a Dickey-Fuller-type ratio of integrals of an Ornstein-Uhlenbeck process, plus an independent "
            "normal for the rest. <bookmark mark='c'/> At a unit root the Dickey-Fuller part is skewed left with a mean "
            "near minus one and a half, so with phi negative the whole t-statistic is shifted right, and the shift does "
            "not shrink with more data."
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
            wrapped_label(r"red: the OLS $t$-test; green: Amihud and Hurvich's augmented regression. $T$ = 100 unless "
                          r"marked; $\phi = -0.95$", 3.2, 15, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.3).shift(UP * 1.0)
        fit_right(side)
        with self.voiceover(
            "Here is what that does to a test. <bookmark mark='a'/> With no predictability at all, a five percent "
            "one-sided t-test rejects one time in ten at rho of point eight, one in five at point nine five, a third of "
            "the time at point nine nine, and more than two times in five at a unit root. <bookmark mark='b'/> And "
            "five hundred years instead of one hundred cure it only away from one: at point nine five the size falls to "
            "nine percent, but at a unit root it stays above forty. <bookmark mark='c'/> The green bars are the "
            "repair, at five to nine percent everywhere."
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

    def fix(self, t):
        rows = [cmath(r"\hat\rho^c", r"=", r"\hat\rho + \frac{1 + 3\hat\rho}{T} + \frac{3(1 + 3\hat\rho)}{T^2}", font_size=32,
                      colors={r"\hat\rho^c": X_C}),
                cmath(r"r_{t+1}", r"=", r"\alpha + \beta x_t + \gamma\,\hat v^c_{t+1} + \epsilon_{t+1}", font_size=32,
                      colors={r"r_{t+1}": QC.SPOT}),
                cmath(r"\widehat{\operatorname{se}}^2(\hat\beta^c)", r"=", r"\widehat{\operatorname{se}}^2_{\text{OLS}} + "
                      r"\hat\gamma^2\,\widehat{\operatorname{Var}}(\hat\rho^c)", font_size=32,
                      colors={r"\widehat{\operatorname{se}}^2(\hat\beta^c)": ARM_C})]
        whys = [why(r"correct the AR(1) coefficient for Kendall's bias, to second order"),
                why(r"Amihud and Hurvich (2004): add the corrected yield shock as a regressor; it absorbs the part of the "
                    r"return shock that moves with $v$, the source of the bias"),
                why(r"and carry the remaining uncertainty in $\hat\rho^c$ into the standard error")]
        step = ladder(self, rows, whys, keep=3, top=2.7, x=-0.3, buff=0.48, edge=6.9)
        with self.voiceover(
            "The repair Amihud and Hurvich proposed in 2004 is short. <bookmark mark='a'/> Correct rho for Kendall's "
            "bias. <bookmark mark='b'/> Compute the yield shocks with the corrected rho and add them to the "
            "regression, so they absorb the part of the return shock that moves with the yield, which is where the "
            "bias came from. <bookmark mark='c'/> And add the remaining uncertainty in rho to the standard error. In "
            "the same simulations, its size stays between five and nine percent at every persistence."
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

    def shiller(self, t):
        s = t["shiller"]
        hx = [-3.2, 1.6, 4.6]
        head = VGroup(label(rf"Shiller, {s['first']}--{s['last']}, annual", font_size=18, color=GREY_B),
                      label(r"OLS", font_size=20, color=OLS_C), label(r"augmented", font_size=20, color=ARM_C))
        data = [(r"slope on the log dividend yield", rf"{s['b']:.3f}", rf"{s['b_c']:.3f}"),
                (r"$t$-statistic", rf"{s['t']:.2f}", rf"{s['t_c']:.2f}"),
                (r"Stambaugh's bias, estimated", rf"{s['stambaugh_bias']:.3f}", r"")]
        tab = VGroup()
        for j, row in enumerate([head] + [VGroup(label(a, font_size=18, color=GREY_A), MathTex(b, font_size=26),
                                                 MathTex(c if c else r"\cdot", font_size=26)) for a, b, c in data]):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 1.6 - 0.7 * j, 0])
            row[0].align_to(np.array([hx[0] - 3.2, 0, 0]), LEFT)
            tab.add(row)
        sub = MathTex(rf"\hat\rho = {s['rho']:.2f},\quad \hat\phi = {s['phi']:.2f},\quad T = {s['T']}", font_size=26,
                      color=X_C).next_to(tab, DOWN, buff=0.5)
        foot = wrapped_label(r"next year's real log return with dividends, on last year's dividend over this January's price. "
                             r"Chapter 9's long horizons pool overlapping years, which makes the problem worse, not better",
                             11.6, 16, GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "On Shiller's century and a half of data. <bookmark mark='a'/> Least squares gives a slope of point zero "
            "four six with a t of one point four, already short of significance. The yield's persistence is point "
            "nine, and the shocks' correlation minus point eight. <bookmark mark='b'/> The augmented regression trims "
            "the slope by a third and the t to about one. A year ahead, the dividend yield's evidence is weaker than it "
            "looks, and Chapter 9's ten-year horizons, which overlap, make the problem worse, not better."
        ) as vo:
            self.play(FadeIn(tab[0]))
            vo.wait_until("a")
            self.play(FadeIn(tab[1][:2]), FadeIn(tab[2][:2]), FadeIn(tab[3]), FadeIn(sub))
            vo.wait_until("b")
            self.play(FadeIn(tab[1][2]), FadeIn(tab[2][2]), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def open_problems(self):
        cards = VGroup(
            desk_question(r"open: uniformly valid inference", r"tests that are right whether $\rho$ is 0.9 or 1: "
                          r"Campbell and Yogo's (2006) Bonferroni intervals and the IVX estimator (Kostakis, Magdalinos and "
                          r"Stamatogiannakis 2015) trade power for robustness differently; no test is best for every $\rho$",
                          width=12.4, font_size=18),
            desk_question(r"open: breaks in the predictor", r"the dividend yield's mean may have shifted (Lettau and Van "
                          r"Nieuwerburgh 2008): a break looks like a near-unit root, and the two are hard to tell apart",
                          width=12.4, font_size=18),
            desk_question(r"open: in sample against out of sample", r"in-sample $t$-tests and out-of-sample $R^2$ "
                          r"disagree (Welch and Goyal 2008; Part 6); which is the right test of predictability is argued",
                          width=12.4, font_size=18),
        ).arrange(DOWN, buff=0.22)
        with self.voiceover(
            "Three open questions. <bookmark mark='a'/> A test that is right whether the root is point nine or one: "
            "Campbell and Yogo's Bonferroni intervals and the IVX estimator do it in different ways, and neither is "
            "best everywhere. <bookmark mark='b'/> A break in the yield's mean looks just like a root near one, and "
            "the two are hard to tell apart. <bookmark mark='c'/> And in-sample tests and out-of-sample forecasts "
            "disagree, as Part 6 will show; which of them is the right test of predictability is still argued."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"$T = 60$, $\hat\rho = 0.95$, $\hat\sigma_{uv}/\hat\sigma_v^2 = -1.1$, $\hat\beta = 0.10$ with "
                       r"standard error 0.05. Estimate Stambaugh's bias and a corrected $\hat\beta$. Is it still significant?")
        with self.voiceover(
            "Pause and predict. Sixty years, an estimated persistence of point nine five, a shock regression of minus "
            "one point one, and a slope of point one with a standard error of point zero five. Estimate the bias and "
            "a corrected slope. Is it still significant?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
