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
                why(r"the ratio of expected active return to active risk, for those holdings; the $z_i$ have unit variance"),
                why(r"with $BR$ independent bets a period: skill times the square root of breadth")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.42, edge=6.9)
        with self.voiceover(
            "The derivation takes four lines. <bookmark mark='a'/> A forecast of residual return is the information "
            "coefficient, times the asset's residual volatility, times a standardised score: Grinold's rule. "
            "<bookmark mark='b'/> With independent residuals, the best holdings are the forecast over the variance. "
            "<bookmark mark='c'/> The information ratio of those holdings, squared, is the sum of each bet's squared "
            "forecast over its variance: IC squared times the sum of the squared scores. <bookmark mark='d'/> With BR "
            "independent bets, the information ratio is the IC times the square root of breadth."
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
        head = VGroup(label(r"$N$", font_size=18, color=GREY_B), label(r"sd of IC", font_size=18, color=GREY_B),
                      label(r"$IC\sqrt N$", font_size=18, color=IC_C), label(r"simulated IR", font_size=18, color=REAL_C),
                      label(r"time-varying formula", font_size=18, color=GOOD))
        tab = VGroup(head)
        for r in rows:
            tab.add(VGroup(MathTex(f"{r['N']}", font_size=24), MathTex(f"{r['ic_sd']:.2f}", font_size=24),
                           MathTex(f"{r['naive']:.2f}", font_size=24), MathTex(f"{r['sim']:.2f}", font_size=24),
                           MathTex(f"{r['formula']:.2f}", font_size=24)))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 2.6 - 0.5 * j, 0])
        foot = wrapped_label(r"mean IC 0.05 per period; 8 simulated strategies of 1{,}000 periods each; IR per period",
                             11.0, 16, GREY_A).to_edge(DOWN, buff=0.4)
        r500 = [r for r in rows if r["N"] == 500]
        with self.voiceover(
            "Simulate it: an IC of five percent, over ten, a hundred and five hundred assets. <bookmark mark='a'/> When "
            "the IC is the same every period, the simulated information ratio matches IC times root N. "
            f"<bookmark mark='b'/> But let the IC itself vary from period to period, and with five hundred assets the "
            f"information ratio falls from {r500[0]['naive']:.2f} to {r500[-1]['sim']:.2f}. The last column predicts it: a "
            "formula the research chapter proves."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(foot))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[1::3]], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r_) for k, r_ in enumerate(tab[1:]) if k % 3], lag_ratio=0.2))
        self.wait(0.4)
        self.clear_scene()

    def transfer(self, l):
        rows = [cmath(r"IR", r"=", r"TC\cdot IC\sqrt{BR}", font_size=38, colors={r"IR": GOOD}),
                cmath(r"TC", r"=", r"\operatorname{Corr}\big(h^{\text{actual}}_i\omega_i,\ \alpha_i/\omega_i\big)", font_size=32,
                      colors={r"TC": HURDLE}),
                cmath(r"\text{long only, 500 assets}", r":", rf"TC \approx {l['tc_long_only']:.2f}", font_size=32)]
        whys = [why(r"Clarke, de Silva and Thorley (2002): constraints keep the portfolio from expressing the forecasts "
                    r"fully"),
                why(r"the transfer coefficient: the correlation of the risk-adjusted holdings with the risk-adjusted "
                    r"forecasts"),
                why(r"simulated: holding only the positive scores, against an equal-weighted benchmark")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "A second correction. <bookmark mark='a'/> Roger Clarke, Harindra de Silva and Steven Thorley added a factor "
            "in 2002: constraints stop a portfolio from expressing its forecasts fully. <bookmark mark='b'/> The transfer "
            "coefficient is the correlation between the holdings the constraints allow and the holdings the forecasts "
            "want. <bookmark mark='c'/> A long-only portfolio of five hundred assets, holding only the positive scores, "
            f"transfers about {l['tc_long_only']:.2f}: the rest of the skill is lost to the constraint."
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

    def limits(self):
        cards = VGroup(
            desk_question(r"breadth is not the number of assets", r"bets must be independent: a hundred stocks in one "
                          r"industry, or a signal rebalanced daily that barely changes, are few bets", width=12.4, font_size=19),
            desk_question(r"the IC is not constant", r"a forecast that works brilliantly in some periods and not at all "
                          r"in others has a much lower IR than its average IC suggests (the research chapter)", width=12.4,
                          font_size=19),
            desk_question(r"costs are not in it", r"the law is gross: breadth bought by trading often is paid for, and "
                          r"Chapters 4 and 5 price it", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "And three limits that make the law an upper bound. <bookmark mark='a'/> Breadth counts independent bets, not "
            "assets: a hundred stocks in one industry are few bets. <bookmark mark='b'/> The IC is not constant, and its "
            "variation costs more than most users of the law expect. <bookmark mark='c'/> And the law is gross of costs: "
            "breadth bought by trading often is paid for."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
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
