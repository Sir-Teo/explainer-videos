from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant24.common import BAD, GOOD, MKT, PART, ask, fit_right, illustration


class Green(VoiceoverScene):
    def construct(self):
        self.card()
        self.model()
        self.worked()
        self.evidence()
        self.ratings()
        self.lesson()

    def card(self):
        c = chapter_card(9, r"Green returns", r"Should a stock investors like earn more, or less?", lit=(2021, 2022),
                         part=PART)
        with self.voiceover("Chapter nine. Environmental, social and governance investing, and the difference between "
                            "a factor's expected return and its realised one."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def model(self):
        rows = [cmath(r"\mathbb{E}[r^e_i]", r"=", r"\beta_i\,\mu_m - \frac{b}{\gamma}\,g_i", font_size=44,
                      colors={r"\mathbb{E}[r^e_i]": GOOD}),
                cmath(r"r^e_{i,t+1}", r"=", r"\mathbb{E}_t[r^e_i] + \beta_i\,\varepsilon_m + c\,g_i\,\Delta\text{concern}_{t+1} "
                      r"+ \dots", font_size=38, colors={r"r^e_{i,t+1}": MKT})]
        whys = [why(r"Pástor, Stambaugh and Taylor (2021): some investors get utility from holding green firms ($g_i > 0$) "
                    r"and dislike brown ones. In equilibrium they pay up for green, so green stocks have lower expected "
                    r"returns: the 'greenium' is negative, by an amount set by tastes $b$ and risk aversion $\gamma$"),
                why(r"but realised returns also include surprises: if concern about climate rises unexpectedly, investors "
                    r"bid green stocks up and brown ones down. Green can outperform for years while its expected return "
                    r"is lower")]
        step = ladder(self, rows, whys, keep=2, top=2.5, x=-0.6, buff=0.8, edge=6.9)
        with self.voiceover(
            "Lubos Pastor, Robert Stambaugh and Lucian Taylor built the equilibrium model. Some investors get "
            "satisfaction from holding green companies and dislike brown ones. They bid green stocks up until their "
            "expected returns are lower: investors accept less return to hold what they like. <bookmark mark='a'/> But "
            "realised returns include surprises. If concern about the climate rises by more than anyone expected, those "
            "investors bid green stocks up further and brown ones down. Green stocks can then outperform for years, "
            "while their expected return is lower all along."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
        self.wait(0.4)
        self.clear_scene()

    def worked(self):
        yrs = np.arange(0, 11)
        rng = np.random.default_rng(9)
        shocks = np.r_[0, np.full(10, 0.012) + rng.normal(0, 0.006, 10)]
        exp_g, exp_b = 0.05, 0.07
        green = np.cumprod(1 + np.r_[0, np.full(10, exp_g)] + 4 * shocks)
        brown = np.cumprod(1 + np.r_[0, np.full(10, exp_b)] - 2 * shocks)
        g = axes([0, 10], [0.9, 2.6], x_length=7.2, y_length=4.4, xlabel=r"years", ylabel=r"\$1 invested",
                 xticks=[0, 2, 4, 6, 8, 10], yticks=[1.0, 1.5, 2.0, 2.5], font_size=13).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        lg = curve(ax, yrs, green, GOOD, stroke_width=3)
        lb = curve(ax, yrs, brown, QC.IMPLIED, stroke_width=3)
        eg = DashedLine(ax.c2p(0, 1), ax.c2p(10, (1 + exp_g) ** 10), color=GOOD, stroke_width=1.5)
        eb = DashedLine(ax.c2p(0, 1), ax.c2p(10, (1 + exp_b) ** 10), color=QC.IMPLIED, stroke_width=1.5)
        side = VGroup(
            legend([(GOOD, r"green: expected 5\% a year"), (QC.IMPLIED, r"brown: expected 7\% a year")], font_size=16),
            wrapped_label(r"dashed: what each was expected to earn; solid: what it earned when concern about climate rose a "
                          r"little more than expected each year. Green wins the decade by a wide margin, and an investor "
                          r"who extrapolates it gets the sign of the future premium wrong. Illustrative numbers", 3.6, 16,
                          GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "A made-up decade shows the trap. Green stocks are priced to earn five percent a year and brown stocks "
            "seven: the dashed lines. <bookmark mark='a'/> Now let concern about the climate rise a little more than "
            "expected every year. Green stocks gain from each surprise, brown stocks lose, and green wins the decade by "
            "a wide margin. <bookmark mark='b'/> An analyst who looks at the backtest concludes that green stocks earn "
            "a premium. The model says the opposite: their expected return was lower the whole time, and the "
            "outperformance was a one-time repricing that cannot repeat unless concern keeps surprising upward."
        ) as vo:
            self.play(FadeIn(g), Create(eg), Create(eb), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(Create(lg), Create(lb), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
        self.wait(0.4)
        self.clear_scene()

    def evidence(self):
        cards = VGroup(
            desk_question(r"Pástor, Stambaugh and Taylor (2022)", r"in the US, green stocks outperformed brown ones over "
                          r"2012--2020; once unexpected increases in climate concern (measured from news coverage) are "
                          r"removed, the outperformance disappears", width=12.0, font_size=20),
            desk_question(r"Bolton and Kacperczyk (2021)", r"firms with higher carbon emissions earn higher returns, "
                          r"controlling for other factors: a carbon premium, the other side of the same coin", width=12.0,
                          font_size=20),
            desk_question(r"the implication", r"a green tilt is a bet on climate concern rising faster than prices "
                          r"already assume, not a source of extra expected return", width=12.0, font_size=20),
        ).arrange(DOWN, buff=0.3)
        if cards.height > 6.6:
            cards.scale_to_fit_height(6.6)
        with self.voiceover(
            "The evidence fits. <bookmark mark='a'/> Pastor, Stambaugh and Taylor found that green American stocks did "
            "beat brown ones from 2012 to 2020, and that once the months of unexpectedly rising climate concern, "
            "measured from news coverage, are accounted for, the outperformance disappears. <bookmark mark='b'/> "
            "Patrick Bolton and Marcin Kacperczyk found the other side: firms with higher emissions earn higher "
            "returns, a carbon premium. <bookmark mark='c'/> So a green tilt is not a source of extra expected return. "
            "It is a bet that concern will rise faster than prices already assume."
        ) as vo:
            for i, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[i], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def ratings(self):
        rows = [cmath(r"\rho(\text{rating}_A, \text{rating}_B)", r"\approx", r"0.4\text{--}0.7", font_size=44,
                      colors={r"\rho(\text{rating}_A, \text{rating}_B)": BAD})]
        whys = [why(r"Berg, Kölbel and Rigobon (2022), 'Aggregate confusion': six major ESG rating agencies agree with "
                    r"each other far less than credit rating agencies do (correlations near 0.99); most of the "
                    r"disagreement is in what they measure and how, not how much weight they give it")]
        step = ladder(self, rows, whys, keep=1, top=2.3, x=-0.4, buff=0.8, edge=6.9)
        with self.voiceover(
            "There is also a measurement problem. Florian Berg, Julian Koelbel and Roberto Rigobon compared six major "
            "ESG rating agencies. Their ratings of the same firms are correlated only about four to seven tenths, "
            "while credit ratings agree almost perfectly. Most of the disagreement is about what to measure and how. "
            "A factor built on one agency's scores is a different portfolio from one built on another's, and backtests "
            "on ratings that are revised with hindsight are a trap of the kind Part three warned about."
        ) as vo:
            step(0)
        self.wait(0.4)
        self.clear_scene()

    def lesson(self):
        cards = VGroup(
            desk_question(r"expected is not realised", r"a premium estimated from a period in which the characteristic "
                          r"became popular measures the repricing, not the premium", width=12.0, font_size=20),
            desk_question(r"the same applies elsewhere", r"growth in the 2010s, small stocks before 1981, any factor that "
                          r"attracted money: a backtest's average includes the change in its valuation", width=12.0,
                          font_size=20),
        ).arrange(DOWN, buff=0.35)
        with self.voiceover(
            "The lesson reaches beyond green investing. <bookmark mark='a'/> When a characteristic becomes popular, "
            "the period in which it becomes popular shows high returns, from the repricing alone, and the premium "
            "estimated from that period is the wrong sign. <bookmark mark='b'/> The same was true of growth stocks in "
            "the 2010s and of small stocks before 1981: a backtest's average includes the change in valuation, and "
            "valuations cannot keep changing in one direction for ever."
        ) as vo:
            for i, mk in enumerate(("a", "b")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[i], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()
        q = ask(r"a green fund beat the market by 3\% a year for five years. Its marketing says green stocks earn a "
                r"premium. What would you need to see before believing it?")
        with self.voiceover("A green fund beat the market by three percent a year for five years, and its marketing says "
                            "green stocks earn a premium. What would you need to see before believing it?"):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
