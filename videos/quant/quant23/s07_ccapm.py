from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant23.common import BAD, CONS, GOOD, MKT, PART, SDF, TAN, ask, fit_right, illustration, load


class CCAPM(VoiceoverScene):
    def construct(self):
        p = load("puzzle")
        self.card()
        self.lucas()
        self.euler()
        self.data(p)
        self.gmm_idea()
        self.gmm_result(p)

    def card(self):
        c = chapter_card(6, r"Consumption and GMM", r"Are assets priced by what they do to consumption?", lit=(1985,),
                         part=PART)
        with self.voiceover("Chapter six. Pricing assets by what they do to consumption, and testing it."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def lucas(self):
        rows = [cmath(r"\max\ \mathbb{E}\textstyle\sum_t \beta^t u(C_t)", r"\ \Rightarrow\ ",
                      r"u'(C_t)\,p_t = \mathbb{E}_t\big[\beta\,u'(C_{t+1})\,x_{t+1}\big]", font_size=36),
                cmath(r"m_{t+1}", r"=", r"\beta\,\frac{u'(C_{t+1})}{u'(C_t)} = \beta\Big(\frac{C_{t+1}}{C_t}\Big)^{-\gamma}",
                      font_size=40, colors={r"m_{t+1}": SDF})]
        whys = [why(r"an investor who can buy a little more of any asset today: the utility given up, $u'(C_t)p_t$, must "
                    r"equal the discounted expected utility of its payoff (Lucas, 1978; Breeden, 1979)"),
                why(r"so the discount factor is the marginal rate of substitution: with power utility $u = C^{1-\gamma}/"
                    r"(1-\gamma)$, dollars are worth most when consumption falls")]
        step = ladder(self, rows, whys, keep=2, top=2.5, x=-0.6, buff=0.8, edge=6.9)
        with self.voiceover(
            "Where does the discount factor come from in economics? From people. An investor who could buy a little "
            "more of an asset today gives up the utility of that money now, and gains the discounted expected utility "
            "of its payoff later. At the optimum the two are equal. <bookmark mark='a'/> So the discount factor is the "
            "ratio of marginal utilities, tomorrow's to today's: with power utility, consumption growth raised to minus "
            "gamma, the coefficient of relative risk aversion. A dollar is worth most in the states where consumption "
            "falls. That is Robert Lucas's and Douglas Breeden's consumption model."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
        self.wait(0.4)
        self.clear_scene()

    def euler(self):
        rows = [cmath(r"\mathbb{E}[R^e]", r"\approx", r"\gamma\,\text{cov}(\Delta c,\ R^e)", font_size=44,
                      colors={r"\mathbb{E}[R^e]": MKT}),
                cmath(r"r^f", r"\approx", r"\delta + \gamma\,\mathbb{E}[\Delta c] - \tfrac12\gamma^2\sigma^2(\Delta c)",
                      font_size=40, colors={r"r^f": TAN})]
        whys = [why(r"log-normal consumption: an asset's premium is risk aversion times its covariance with consumption "
                    r"growth. Stocks fall in recessions, so they must pay"),
                why(r"and the riskless rate: impatience $\delta$, plus the desire to smooth a growing consumption "
                    r"($\gamma$ again), less a precautionary term")]
        step = ladder(self, rows, whys, keep=2, top=2.5, x=-0.6, buff=0.8, edge=6.9)
        with self.voiceover(
            "With log-normal consumption the model gives two clean predictions. <bookmark mark='a'/> An asset's premium "
            "is risk aversion times its covariance with consumption growth: stocks do badly when people are cutting "
            "back, so they must pay. And the riskless rate is impatience, plus gamma times expected growth, less a "
            "small precautionary term. The same gamma has to explain both."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
        self.wait(0.4)
        self.clear_scene()

    def data(self, p):
        yrs, dc, rm = np.asarray(p["years"]), 100 * np.asarray(p["dc"]), 100 * np.asarray(p["rm"])
        g1 = axes([1947, 2026], [-4, 6], x_length=10.4, y_length=2.1, xlabel=r"", ylabel=r"$\Delta c$, \%",
                  xticks=[], yticks=[-2, 0, 2, 4], font_size=12).to_edge(UP, buff=0.7)
        g2 = axes([1947, 2026], [-50, 50], x_length=10.4, y_length=2.1, xlabel=r"year", ylabel=r"real return, \%",
                  xticks=[1950, 1970, 1990, 2010], yticks=[-40, 0, 40], font_size=12).next_to(g1, DOWN, buff=0.4)
        b1 = VGroup(*[Rectangle(width=0.08, height=max(abs(g1.ax.c2p(0, v)[1] - g1.ax.c2p(0, 0)[1]), 0.005),
                                stroke_width=0, fill_color=CONS, fill_opacity=0.9).move_to(
            [g1.ax.c2p(y, 0)[0], (g1.ax.c2p(0, v)[1] + g1.ax.c2p(0, 0)[1]) / 2, 0]) for y, v in zip(yrs, dc)])
        b2 = VGroup(*[Rectangle(width=0.08, height=max(abs(g2.ax.c2p(0, v)[1] - g2.ax.c2p(0, 0)[1]), 0.005),
                                stroke_width=0, fill_color=MKT, fill_opacity=0.9).move_to(
            [g2.ax.c2p(y, 0)[0], (g2.ax.c2p(0, v)[1] + g2.ax.c2p(0, 0)[1]) / 2, 0]) for y, v in zip(yrs, rm)])
        foot = VGroup(
            MathTex(rf"\sigma(\Delta c) = {100 * p['sd_dc']:.1f}\%,\ \ \sigma(r^m) = {100 * p['sd_rm']:.0f}\%,\ \ "
                    rf"\rho = {p['corr']:.2f}", font_size=26),
            wrapped_label(r"real per-capita consumption (the BEA's PCE), fourth quarter to fourth quarter, against the "
                          r"market's real December-to-December return, 1948--2024", 11.0, 16, GREY_A),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Now the data, every year since 1948. <bookmark mark='a'/> Real consumption per person grows about two "
            f"percent a year, with a volatility of only {100 * p['sd_dc']:.1f} percent: it is remarkably smooth. "
            "<bookmark mark='b'/> The stock market's real return has a volatility of "
            f"{100 * p['sd_rm']:.0f} percent, nine times as much, and the two are only loosely correlated, "
            f"{p['corr']:.2f}. Stocks do fall when consumption falls, but consumption hardly falls."
        ) as vo:
            self.play(FadeIn(g1), FadeIn(g2))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in b1], lag_ratio=0.01), run_time=2)
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in b2], lag_ratio=0.01), FadeIn(foot), run_time=2)
        self.add(illustration(r"FRED: A794RX0Q048SBEA, CPIAUCSL; Kenneth French: the market and bill"))
        self.wait(0.4)
        self.clear_scene()

    def gmm_idea(self):
        rows = [cmath(r"\mathbb{E}\Big[\Big(\beta\,g_{t+1}^{-\gamma} R_{t+1} - 1\Big)\,z_t\Big]", r"=", r"0", font_size=40,
                      colors={r"\mathbb{E}\Big[\Big(\beta\,g_{t+1}^{-\gamma} R_{t+1} - 1\Big)\,z_t\Big]": SDF}),
                cmath(r"\hat\theta", r"=", r"\arg\min_\theta\ \bar g(\theta)^\top W\,\bar g(\theta),\quad J = T\,\bar g^\top "
                      r"\hat S^{-1}\bar g \sim \chi^2_{q - p}", font_size=34, colors={r"\hat\theta": GOOD})]
        whys = [why(r"Hansen and Singleton (1982): the Euler equation holds for every return and every variable $z_t$ "
                    r"known at $t$: a set of moment conditions, with no need to model the whole economy"),
                why(r"Hansen's GMM (1982; Part 6): choose $(\beta, \gamma)$ to make the sample moments as close to zero "
                    r"as possible; with more moments than parameters, $J$ tests whether they can all hold at once")]
        step = ladder(self, rows, whys, keep=2, top=2.5, x=-0.6, buff=0.8, edge=6.9)
        with self.voiceover(
            "How do you estimate gamma without modelling the whole economy? Lars Hansen and Kenneth Singleton's insight "
            "in 1982: the Euler equation must hold for every return, and in every state known in advance. Multiply its "
            "error by anything known today, and the average should be zero. <bookmark mark='a'/> Hansen's generalised "
            "method of moments, from Part six, picks the parameters that bring those averages closest to zero, and "
            "with more conditions than parameters, its J statistic tests whether they can all hold at once."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
        self.wait(0.4)
        self.clear_scene()

    def gmm_result(self, p):
        gm = p["gmm"]
        (b, g), (sb, sg) = gm["theta"], gm["se"]
        rows = VGroup(
            label(r"returns: the market and the bill; instruments: a constant, last year's consumption growth and market "
                  r"return; annual, 1949--2024", font_size=19, color=GREY_A),
            MathTex(rf"\hat\gamma = {g:.1f}\ \ ({sg:.1f}),\qquad \hat\beta = {b:.2f}\ \ ({sb:.2f})", font_size=36, color=GOOD),
            MathTex(rf"J = {gm['J']:.1f},\ \ p = {gm['p_J']:.2f}", font_size=32),
            wrapped_label(r"a risk aversion in the tens, imprecisely measured, and a time discount factor above one: "
                          r"people would have to prefer the future to the present to explain why interest rates were so "
                          r"low with such high risk aversion. That second failure is Weil's (1989) risk-free rate puzzle",
                          12.0, 18, GREY_A),
        ).arrange(DOWN, buff=0.35)
        with self.voiceover(
            "Fit it to the data. <bookmark mark='a'/> Risk aversion comes out at about "
            f"{g:.0f}, with a standard error of {sg:.0f}: large, and barely pinned down. And beta, the time discount "
            f"factor, comes out at {b:.1f}: above one, as if people valued the future more than the present. "
            "<bookmark mark='b'/> That is no accident. A gamma this large makes people desperate to smooth a growing "
            "consumption, which should push interest rates far up; only an impatience below zero can hold them at the "
            "low levels we see. Philippe Weil called it the risk-free rate puzzle. The J test cannot reject the model "
            "with so few years of data, but no economist believes these numbers."
        ) as vo:
            self.play(FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(FadeIn(rows[1]), FadeIn(rows[2]))
            vo.wait_until("b")
            self.play(FadeIn(rows[3]))
        q = ask(r"why does the same $\gamma$ that explains a large equity premium predict a high riskless interest rate?")
        with self.voiceover("Why does the same gamma that explains a large equity premium predict a high riskless "
                            "interest rate?"):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
