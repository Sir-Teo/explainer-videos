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
            "In Pastor, Stambaugh and Taylor's conditional equilibrium, tastes for green holdings and climate-risk hedging can lower green expected returns relative to brown. This depends on preferences, risk exposures and prices, not a universal ranking of every green stock. <bookmark mark='a'/> Unexpected increases in climate concern can raise green realised returns through repricing while the model's conditional expected return is lower. A large realised return alone does not reveal that expectation."
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
            wrapped_label('dashed: what each was expected to earn; solid: what it earned when concern about climate rose a little more than expected each year. Fixed-seed additive simple-return shocks; extrapolation confuses assumed premia with this shock path. Illustrative numbers; not a universal sign reversal', 3.6, 16,
                          GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "This is a fixed-seed illustration, not market evidence. The dashed lines assume five-percent green and seven-percent brown expected returns; the solid lines add specified annual surprise shocks to those simple returns. <bookmark mark='a'/> In this toy green gains from the shocks and wins the decade. <bookmark mark='b'/> Extrapolating that realised difference confuses the assumed conditional premium with a particular shock sequence. This additive illustration differs from the multiplicative one-year shock convention used in the worked problem. Neither convention is a forecast of future shocks."
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
            desk_question(r"the implication", 'conditional preference/climate-risk models can lower green expected returns; observational news controls do not identify a universal premium or a unique cause', width=12.0, font_size=20),
        ).arrange(DOWN, buff=0.3)
        if cards.height > 6.6:
            cards.scale_to_fit_height(6.6)
        with self.voiceover(
            "The cited studies offer evidence, not a unique causal identification. <bookmark mark='a'/> Pastor, Stambaugh and Taylor relate green outperformance in 2012 through 2020 to unexpected climate-concern news under their measurement and controls. <bookmark mark='b'/> Bolton and Kacperczyk report an emissions-return association with a different design. <bookmark mark='c'/> Observational adjustments do not prove that all green expected premia are negative or that climate news is the only cause. Tastes, hedging, exposure definitions and data vintages matter alongside financial returns."
        ) as vo:
            for i, mk in enumerate(("a", "b", "c")):
                if i:
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
            desk_question(r"expected is not realised", 'a popularity shock can add repricing to a measured mean; this need not identify a stable expected premium or reverse its sign', width=12.0, font_size=20),
            desk_question(r"the same applies elsewhere", 'popularity may coexist with cash-flow and risk changes; one selected episode cannot identify the stable future premium', width=12.0,
                          font_size=20),
        ).arrange(DOWN, buff=0.35)
        with self.voiceover(
            "The lesson goes beyond green investing. <bookmark mark='a'/> Changing popularity can add repricing to a measured average return, so the historical mean need not estimate a stable future premium. The bias need not always reverse its sign. <bookmark mark='b'/> Distinguish expected cash flows, discount rates, unexpected demand and the chosen sample. Evidence from one selected popularity episode cannot by itself identify the expected return investors will earn next."
        ) as vo:
            for i, mk in enumerate(("a", "b")):
                if i:
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
