from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from explainer.quant.house import statarb as SA
from videos.quant.quant33.common import (BAD, COST_C, GOOD, KAL_C, NET_C, OU_C, PART, RES_C, SPREAD_C, comma, house_lab,
                                         load)


class House(VoiceoverScene):
    def construct(self):
        self.card()
        self.sheet(load("pairs"), load("coint"), load("kalman"), load("lomac"), load("pca"), load("deep"), load("nagel"))
        self.lab()
        self.lab2()
        self.lab3()
        self.lab4()
        self.module()
        self.capacity()
        self.monitor()
        self.test()

    def card(self):
        c = chapter_card(11, r"Rule 33: the stat-arb book", r"What must a reversion strategy show before the House trades "
                         r"it?", part=PART)
        with self.voiceover("Chapter eleven. The House's thirty-third rule: what a reversion strategy must show before "
                            "the House trades it. Reversion is easy to find before costs and hard to keep after them, so "
                            "the rule is mostly about costs, and about the trials it took to find the rule."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def sheet(self, pr, co, ka, lm, p, dp, ng):
        frac = float(np.mean(co["frac"]))
        th = p["configs"]["5f/60d/theory"]
        rows = [(r"distance pairs on the industries, 1964--2020: Sharpe", rf"{pr['all']['sharpe']:.2f}", SPREAD_C),
                (r"pairs passing Engle--Granger a year; false-positive rate", rf"{100 * frac:.1f}\%,\ "
                 rf"{100 * co['false_positive']:.1f}\%", SPREAD_C),
                (r"BTC/ETH: ADF of the fixed and the Kalman spread", rf"{ka['adf_static']:.2f},\ {ka['adf_kalman']:.1f}",
                 KAL_C),
                (r"size portfolios: own and cross terms, bp per five-observation block", rf"{1e4 * lm['size']['own']:+.2f},\ "
                 rf"{1e4 * lm['size']['cross']:+.2f}", OU_C),
                (r"residual book, Avellaneda--Lee bands: gross, net Sharpe", rf"{p['al']['gross']['sharpe']:.2f},\ "
                 rf"{p['al']['net']['sharpe']:.2f}", RES_C),
                (r"residual book, research band: gross, net Sharpe", rf"{th['gross']['sharpe']:.2f},\ {th['sharpe']:.2f}",
                 RES_C),
                (r"the network, 2017--20: IC; net Sharpe", rf"{dp['ic']:.4f};\ {dp['net_after_costs']['sharpe']:.1f}",
                 NET_C),
                (r"industry contrarian on the VIX: $t$", rf"{ng['t']:.2f}", COST_C),
]
        hx = [-2.4, 4.6]
        tab = VGroup()
        for j, (txt, val, col) in enumerate(rows):
            y = 2.6 - 0.52 * j
            tab.add(VGroup(label(txt, font_size=17, color=col).move_to([hx[0], y, 0]),
                           MathTex(val, font_size=24).move_to([hx[1], y, 0])))
        title = label(r"The stat-arb desk's first sheet", font_size=28).to_edge(UP, buff=0.2)
        foot = wrapped_label(r"every number computed in this part from Kenneth French's daily portfolios, Binance's bars "
                             r"and Cboe's VIX; none is a forecast, and none is advice", 12.0, 15,
                             GREY_A).to_edge(DOWN, buff=0.2)
        self.add(title, tab[0], foot)
        with self.voiceover(
            "The research sheet gathers verified ordinary outputs. <bookmark mark='a'/> The distance proxy has a negative sample mean. Annual cointegration pass rates exceed the simulated control rate, with limited persistence. The adaptive Kalman innovation looks stationary, which is not a fixed cointegrating portfolio. Lo and MacKinlay's covariance terms describe own and cross dependence. Residual and network results use synthetic residual P and L with incomplete cost accounting. The VIX regression is a descriptive industry comparison with conventional errors. No row on this sheet establishes an executable portfolio or a sealed-year verdict."
        ) as vo:
            self.play(FadeIn(title))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in tab], lag_ratio=0.4), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def lab(self):
        card = house_lab(r"The Ornstein--Uhlenbeck fit, as the House runs it", SA.ou_fit, "x = np.asarray(x, float)", 12,
                         width=10.6)
        card.move_to(ORIGIN)
        with self.voiceover(
            'The OU fit regresses the next observation on the previous one with an intercept. A slope outside zero to one is incompatible with this stationary mean-reverting OU mapping. For a valid slope and positive regular sampling interval, speed is minus log slope divided by the interval; the fitted mean divides the intercept by one minus slope. Innovation variation determines equilibrium width. This helper first removes nonfinite observations, compressing any time gaps, and estimates innovation deviation with two regression degrees of freedom. Fitted speed and width remain uncertain.'
        ):
            self.play(FadeIn(card))
            self.wait(1.5)
        self.clear_scene()

    def lab2(self):
        card = house_lab(r"The band rule's profit rate", SA.band_rate, "return (m - c)", 1,
                         extra=((SA.ou_time_to_mean, "k2 = kappa", 2), (SA.ou_time_to_band, "k2 = kappa", 2)), width=10.6)
        card.move_to(ORIGIN)
        with self.voiceover(
            'The band-rate code divides the fixed reward m minus c by mean waiting plus mean holding time. The first-passage formulas assume a known OU process with positive kappa and sigma, continuous monitoring, unit exposure and a fixed round-trip cost in spread units. Simpson quadrature evaluates the integrals. The optimizer searches a bounded grid and refines once; it is a numerical approximation within this policy family. It does not solve financing, risk budgets, a changing factor model, or general optimal stopping.'
        ):
            self.play(FadeIn(card))
            self.wait(1.5)
        self.clear_scene()

    def lab3(self):
        card = house_lab(r"Lo and MacKinlay's decomposition", SA.lo_mackinlay, "R = np.asarray(R, float)", 13,
                         width=10.6)
        card.move_to(ORIGIN)
        with self.voiceover(
            'The decomposition code returns three moment terms and a realized sample profit. In the population, expected contrarian profit is a weighted own covariance term plus off-diagonal covariance, minus the cross-sectional variance of means. That last term is subtracted. In this finite implementation the full-sample centering mean and lagged endpoint means differ, leaving a boundary correction. The notes derive it explicitly; equality to the last digit is not asserted. A covariance identity also does not identify why prices moved.'
        ):
            self.play(FadeIn(card))
            self.wait(1.5)
        self.clear_scene()

    def lab4(self):
        card = house_lab(r"The s-score, at every day", SA.s_score, "x = np.asarray(x, float)", 9, width=10.6)
        card.move_to(ORIGIN)
        with self.voiceover(
            "And the s-score itself. At every day, fit the Ornstein-Uhlenbeck process to the last sixty values of the "
            "cumulative residual; if the fit is mean-reverting, the score is today's distance from the fitted mean in "
            "equilibrium deviations, and the fitted speed is kept beside it. A residual that does not revert gets no "
            "score at all, and is not traded."
        ):
            self.play(FadeIn(card))
            self.wait(1.5)
        self.clear_scene()

    def module(self):
        chart = house_chart(PART, lit=("research", "portfolio")).scale(0.62).to_edge(UP, buff=0.2)
        rows = [
            (r"\texttt{ou\_fit}, \texttt{s\_score}, \texttt{kalman\_beta}", r"spreads"),
            (r"\texttt{norm\_prices}, \texttt{distance\_pairs}, \texttt{trade\_pair}", r"pairs"),
            (r"\texttt{lo\_mackinlay}", r"the decomposition"),
            (r"\texttt{ou\_time\_to\_mean}, \texttt{ou\_time\_to\_band}, \texttt{band\_rate}, \texttt{optimal\_band}",
             r"the theorem"),
            (r"\texttt{simulate\_band}, \texttt{band\_curve}", r"its check"),
        ]
        tab = VGroup(*[VGroup(label(a_, font_size=15, color=QC.HOUSE), label(b_, font_size=15, color=GREY_A)).arrange(
            RIGHT, buff=0.4) for a_, b_ in rows]).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        for r_ in tab:
            r_[1].align_to(tab, LEFT).shift(RIGHT * 9.6)
        tab.next_to(chart, DOWN, buff=0.25)
        if tab.width > 13.0:
            tab.scale_to_fit_width(13.0)
        rule = wrapped_label(r"Rule 33: a reversion strategy enters the House only with its profit shown after the costs "
                             r"of every leg, hedges included; its bands derived from those costs, not from habit; every "
                             r"pair, window and band it was chosen from counted as a trial; its spread tested out of "
                             r"sample on profit, not on stationarity; and its crowding risk stated: who else holds the "
                             r"same residuals.", 12.4, 17, QC.HOUSE).to_edge(DOWN, buff=0.2)
        with self.voiceover(
            "The tools this part adds. <bookmark mark='a'/> Spreads; pairs; the decomposition; the theorem; and its "
            "check by simulation. <bookmark mark='b'/> And the thirty-third rule. A reversion strategy enters the House "
            "only with its profit shown after the costs of every leg, hedges included; its bands derived from those "
            "costs, not from habit; every pair, window and band it was chosen from counted as a trial; its spread tested "
            "out of sample on profit, not on stationarity; and its crowding risk stated: who else holds the same "
            "residuals."
        ) as vo:
            self.play(FadeIn(chart))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab], lag_ratio=0.4, run_time=4))
            vo.wait_until("b")
            self.play(FadeIn(rule))
        self.wait(0.4)
        self.clear_scene()

    def capacity(self):
        cards = VGroup(
            desk_question(r"capacity", r"a residual book's return falls with its size: its own trades move the prices it "
                          r"is trying to buy cheap; Part 31's square-root law says the cost per dollar grows with the root "
                          r"of the trade's share of volume", width=12.0, font_size=19),
            desk_question(r"leverage", r"leverage can magnify losses and liquidity needs; a "
                          r"week like August 2007 may create margin stress as well as a drawdown", width=12.0, font_size=19),
            desk_question(r"what the House holds", r"no live allocation is established; size needs audited holdings, funding and "
                          r"measured execution and impact", width=12.0, font_size=19),
        ).arrange(DOWN, buff=0.25)
        self.add(cards[0])
        with self.voiceover(
            "Capacity and leverage remain design constraints, not outputs certified by this research proxy. <bookmark mark='a'/> Trading larger quantities can raise impact and erode a small edge; the impact model needs data and units appropriate to actual instruments. <bookmark mark='b'/> Leverage increases both opportunities and margin risk, and is never compelled merely by low reported volatility. <bookmark mark='c'/> This lesson establishes no live capital allocation. A trading decision would require audited holdings, financing, liquidity and an independent evaluation under a fixed risk mandate."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def monitor(self):
        cards = VGroup(
            desk_question(r"every day", r"turnover against its budget; the cost actually paid against the 5 bp assumed; "
                          r"the book's factor exposures, which a residual book should not have", width=12.0, font_size=19),
            desk_question(r"every week", r"the dispersion of residuals and the share that pass the OU fit: a falling share "
                          r"is a diagnostic with several possible causes", width=12.0, font_size=19),
            desk_question(r"the stop", r"an illustrative weekly loss beyond three daily volatilities would cut size "
                          r"by half; this trigger is not calibrated or implemented here", width=12.0, font_size=19),
        ).arrange(DOWN, buff=0.25)
        self.add(cards[0])
        with self.voiceover(
            "A proposed monitoring design must also be explicit. <bookmark mark='a'/> Measure actual turnover, execution cost, financing and factor exposures, allowing for model error rather than expecting exact neutrality. <bookmark mark='b'/> Track residual dispersion and fit failures as diagnostics; a lower OU pass rate does not uniquely identify factor-model failure. <bookmark mark='c'/> A loss limit, liquidity reserve or size cut is a prospective policy choice requiring calibration and funding analysis. The illustrative three-daily-volatility weekly trigger is not computed or validated by the stored strategy and is not adopted here."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def test(self):
        cards = VGroup(
            desk_question(r"the pairs fund with a Sharpe of 3", r"ask whether it is before costs, how many pairs were "
                          r"screened to find the ones it shows, and whether the hedge ratio was fitted on the same days "
                          r"(Chapters 2, 3, 6)", width=12.0, font_size=19),
            desk_question(r"the cointegrated basket with a half-life of a day", r"ask whether the spread is a filter's "
                          r"forecast error; a residual that reverts in a day may be noise (Chapter 6)", width=12.0,
                          font_size=19),
            desk_question(r"the residual book that lost in August 2007", r"ask who else held the same residuals, and "
                          r"whether the fund could hold on for a week (Chapter 9)", width=12.0, font_size=19),
        ).arrange(DOWN, buff=0.25)
        self.add(cards[0])
        with self.voiceover(
            "The rule against three cases. <bookmark mark='a'/> A pairs fund showing a Sharpe ratio of three: ask "
            "whether that is before costs, how many pairs were screened, and whether the hedge ratio was fitted on the "
            "same days. <bookmark mark='b'/> A basket with a half-life of one day: ask whether its spread is a filter's "
            "forecast error. <bookmark mark='c'/> A residual book that lost in August 2007: ask who else held the same "
            "residuals, and whether the fund could have held on for a week."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()
