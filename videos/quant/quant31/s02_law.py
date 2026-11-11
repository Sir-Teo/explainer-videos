from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant31.common import BAD, GOOD, HURDLE, IC_C, PART, REAL_C, fit_right, load


class Law(VoiceoverScene):
    def construct(self):
        l = load("law")
        self.card()
        self.derive()
        self.table(l)
        self.transfer(l)
        self.breadth()
        self.scale()
        self.limits()
        self.question()

    def card(self):
        c = chapter_card(1, r"The fundamental law", r"How much information ratio does a forecast's skill buy?", part=PART)
        with self.voiceover("Chapter one. In 1989 Richard Grinold wrote down the most quoted formula in active management. "
                            "How much information ratio does a forecast's skill buy, and how many bets does it need?"):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def derive(self):
        rows = [cmath(r"\alpha_i", r"=", r"IC\cdot\omega_i\cdot z_i", font_size=36, colors={r"\alpha_i": IC_C}),
                cmath(r"h_i", r"=", r"\frac{\alpha_i}{\lambda\,\omega_i^2}", font_size=36),
                cmath(r"IR^2", r"=", r"\frac{(h^\top\alpha)^2}{h^\top\Omega h} = \textstyle\sum_i \frac{\alpha_i^2}{\omega_i^2} = "
                      r"IC^2 \sum_i z_i^2", font_size=32),
                cmath(r"IR", r"=", r"IC\sqrt{BR}", font_size=40, colors={r"IR": GOOD})]
        whys = [why(r"Grinold's rule for a forecast: the information coefficient times the asset's residual volatility "
                    r"times its standardised score"),
                why(r"the optimal residual holdings for independent residuals of variance $\omega_i^2$"),
                why(r"conditional gross active return over risk; the fixed scores have $\sum_i z_i^2=BR$"),
                why(r"under this diagonal-risk calibration, with nonnegative $IC$: skill times the square root of breadth")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.42, edge=6.9)
        with self.voiceover(
            "A conditional benchmark takes four lines. Assume a fixed score vector, diagonal positive residual covariance, and nonnegative signal strength IC. <bookmark mark='a'/> Assume the expected residual return is IC times the specified residual-risk scale times the score. That calibration is a modelling input, not a consequence of a rank correlation estimate. <bookmark mark='b'/> Unconstrained mean-variance holdings are proportional to the forecast divided by residual variance. <bookmark mark='c'/> Their conditional gross information ratio squared is alpha transpose inverse covariance alpha, or IC squared times the squared-score norm. <bookmark mark='d'/> If that norm is BR, the result is IC times root BR. Unconditional realized returns, correlated risks, constraints and annualization require further assumptions."
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

    def table(self, l):
        rows = [r for r in l["rows"] if r["N"] in (10, 100, 500)]
        hx = [-4.2, -2.2, 0.2, 2.6, 4.9]
        head = VGroup(label(r"$N$", font_size=18, color=GREY_B), label(r"latent sd", font_size=18, color=GREY_B),
                      label(r"$IC\sqrt N$", font_size=18, color=IC_C), label(r"simulated IR", font_size=18, color=REAL_C),
                      label(r"saved helper approx.", font_size=18, color=GOOD))
        tab = VGroup(head)
        for r in rows:
            tab.add(VGroup(MathTex(f"{r['N']}", font_size=24), MathTex(f"{r['ic_sd']:.2f}", font_size=24),
                           MathTex(f"{r['naive']:.2f}", font_size=24), MathTex(f"{r['sim']:.2f}", font_size=24),
                           MathTex(f"{r['formula']:.2f}", font_size=24)))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 2.6 - 0.5 * j, 0])
        foot = wrapped_label(r"latent correlation mean 0.05 before clipping; 8 saved simulations of 1{,}000 periods; normalized scores; per-period IR",
                             11.0, 16, GREY_A).to_edge(DOWN, buff=0.4)
        r500 = [r for r in rows if r["N"] == 500]
        with self.voiceover(
            f"""The saved simulations use normalized score cross sections and a latent correlation drawn each period, clipped to stay between minus point nine nine and point nine nine. <bookmark mark='a'/> With constant small correlation, simulated information ratios are close to the familiar IC root N approximation. Even the exact constant-correlation toy has a small finite-correlation adjustment. <bookmark mark='b'/> At five hundred assets, increasing latent dispersion reduces the saved simulated ratio from about {r500[0]['naive']:.2f} to {r500[-1]['sim']:.2f}. The last column retains the original helper's approximation. The research chapter distinguishes it from the exact finite-N identity and from measured sample correlations."""
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(tab[1]), FadeIn(foot))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[4::3]], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r_) for k, r_ in enumerate(tab[1:]) if k % 3], lag_ratio=0.2))
        self.wait(0.4)
        self.clear_scene()

    def transfer(self, l):
        rows = [cmath(r"IR", r"=", r"TC\cdot IC\sqrt{BR}", font_size=38, colors={r"IR": GOOD}),
                cmath(r"TC", r"=", r"\operatorname{Corr}\big(h^{\text{actual}}_i\omega_i,\ \alpha_i/\omega_i\big)", font_size=32,
                      colors={r"TC": HURDLE}),
                cmath(r"\text{positive-score illustration, }N=500", r":", rf"TC \approx {l['tc_long_only']:.2f}", font_size=32)]
        whys = [why(r"Clarke, de Silva and Thorley (2002): constraints keep the portfolio from expressing the forecasts "
                    r"fully"),
                why(r"the transfer coefficient: the correlation of the risk-adjusted holdings with the risk-adjusted "
                    r"forecasts"),
                why(r"200 saved Gaussian score vectors; equal residual risk; positive-score holdings relative to equal weights")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            f"""Constraints change the direction of the active portfolio. <bookmark mark='a'/> Clarke, de Silva and Thorley express that effect through a transfer coefficient under their signal and risk assumptions. <bookmark mark='b'/> In the equal-risk, centered-active-weight illustration, it is the correlation of the chosen active weights with the forecast direction. With a general covariance, the appropriate object is an angle in the risk metric, not an arbitrary raw-weight correlation. <bookmark mark='c'/> The saved example holds positive Gaussian scores in a long-only portfolio relative to equal weights. Across two hundred score vectors its average correlation is {l['tc_long_only']:.2f}. This is a specific construction, not a universal optimum or a fixed fraction of skill lost by every constrained manager."""
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

    def breadth(self):
        n, rho = 100, 0.2
        eff = n / (1 + (n - 1) * rho)
        rows = [cmath(r"BR_{\text{eff}}", r"=", r"\frac{N}{1 + (N - 1)\bar\rho}", font_size=40, colors={r"BR_{\text{eff}}": HURDLE}),
                cmath(r"N = 100,\ \bar\rho = 0.2", r":", rf"BR_{{\text{{eff}}}} = {eff:.1f}", font_size=34),
                cmath(r"\text{time breadth}", r":", r"\text{only new information counts}", font_size=32)]
        whys = [why(r"for the equally weighted mean of equal-variance bets, common expected payoff and average correlation $\bar\rho$: the "
                    r"variance-equivalent count, not a universal optimized-portfolio breadth"),
                why(r"under those equal-variance/equal-weight assumptions, 100 bets at average correlation 0.2 have count 4.8"),
                why(r"trading frequency alone does not establish independent time bets; inspect return dependence and "
                    r"overlap before annualizing")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            f"""Breadth needs a definition. <bookmark mark='a'/> For an equally weighted average of equal-variance bets with the same expected payoff, its variance-equivalent count is N over one plus N minus one times average pairwise correlation. This is not a general formula for the best correlated-signal portfolio. <bookmark mark='b'/> Under those assumptions, a hundred bets at average correlation point two have effective count {eff:.1f}. Different expected payoffs, risk scales or portfolio weights can give a different comparison. <bookmark mark='c'/> Across time, trading frequency alone supplies no independent breadth. Overlapping forecasts and return dependence must be accounted for before multiplying a per-period information ratio by a square root of time."""
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

    def scale(self):
        items = [(r"0.5", r"good: top quartile of active managers, before fees", GOOD),
                 (r"0.75", r"very good", HURDLE),
                 (r"1.0", r"exceptional, and rare over long periods", BAD)]
        rows = VGroup()
        for v, d, col in items:
            rows.add(VGroup(MathTex(rf"IR = {v}", font_size=34, color=col), label(d, font_size=20, color=GREY_A)).arrange(
                RIGHT, buff=0.5))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to(UP * 0.4)
        foot = wrapped_label('historical annual IR scale; signal IC depends on horizon, universe and correlation definition; the toy benchmark calls for an audit of calibration and independence',
                             11.4, 18, GREY_A).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "For historical perspective, Grinold and Kahn use annual information ratios of one half, three quarters and one as rules of thumb for good, very good and exceptional active performance. These labels depend on the benchmark, period and fees. <bookmark mark='a'/> ICs quoted for equity signals also depend on horizon, universe and whether correlation is linear or rank based. The toy value near three point nine therefore invites an audit of calibration, independence, risk and costs. It is not evidence that every real manager falls short of a universal attainable bound."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows], lag_ratio=0.4))
            vo.wait_until("a")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def limits(self):
        cards = VGroup(
            desk_question(r"breadth is not the number of assets", r"bets must be independent: a hundred stocks in one "
                          r"industry, or a signal rebalanced daily that barely changes, are few bets", width=12.4, font_size=19),
            desk_question(r"the IC is not constant", 'in the bounded-latent toy, variation adds nondiversifiable variance; observed IC dispersion also needs measurement analysis', width=12.4,
                          font_size=19),
            desk_question(r"costs are not in it", r"the law is gross: breadth bought by trading often is paid for, and "
                          r"Chapters 4 and 5 price it", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Three restrictions of the benchmark matter. <bookmark mark='a'/> Asset count alone does not establish independent breadth; correlations and shared exposures matter. <bookmark mark='b'/> The latent correlation varies in the research chapter's toy, and that variation contributes nondiversifiable return variance. Observed sample IC variability requires a separate measurement analysis. <bookmark mark='c'/> The simple law is gross of trading costs. None of these observations turns it into a universal upper bound for every possible forecasting and portfolio model."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                if k:
                    self.play(FadeIn(cards[k], shift=UP * 0.2))
                else:
                    self.play(Indicate(cards[0], color=HURDLE, scale_factor=1.02))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"IC 0.05, 500 stocks, rebalanced monthly. What annual information ratio does $IC\sqrt{BR}$ "
                       r"promise?")
        with self.voiceover(
            "Pause and predict. An IC of point zero five, five hundred stocks, rebalanced monthly. What annual "
            "information ratio does the fundamental law promise?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
