from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from explainer.quant.house import statarb as SA
from videos.quant.quant33.common import (BAD, COST_C, GOOD, KAL_C, NET_C, OU_C, PART, RES_C, SPREAD_C, comma, house_lab,
                                         load)


class House(VoiceoverScene):
    def construct(self):
        self.card()
        self.sheet(load("pairs"), load("coint"), load("kalman"), load("lomac"), load("pca"), load("deep"), load("nagel"),
                   load("envelope"))
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

    def sheet(self, pr, co, ka, lm, p, dp, ng, e):
        frac = float(np.mean(co["frac"]))
        th = p["configs"]["5f/60d/theory"]
        rows = [(r"distance pairs on the industries, 1964--2020: Sharpe", rf"{pr['all']['sharpe']:.2f}", SPREAD_C),
                (r"pairs passing Engle--Granger a year; false-positive rate", rf"{100 * frac:.1f}\%,\ "
                 rf"{100 * co['false_positive']:.1f}\%", SPREAD_C),
                (r"BTC/ETH: ADF of the fixed and the Kalman spread", rf"{ka['adf_static']:.2f},\ {ka['adf_kalman']:.1f}",
                 KAL_C),
                (r"size portfolios: own and cross terms, bp a day", rf"{1e4 * lm['size']['own']:+.2f},\ "
                 rf"{1e4 * lm['size']['cross']:+.2f}", OU_C),
                (r"residual book, Avellaneda--Lee bands: gross, net Sharpe", rf"{p['al']['gross']['sharpe']:.2f},\ "
                 rf"{p['al']['net']['sharpe']:.2f}", RES_C),
                (r"residual book, research band: gross, net Sharpe", rf"{th['gross']['sharpe']:.2f},\ {th['sharpe']:.2f}",
                 RES_C),
                (r"the network, 2017--20: IC; net Sharpe", rf"{dp['ic']:.4f};\ {dp['net_after_costs']['sharpe']:.1f}",
                 NET_C),
                (r"industry contrarian on the VIX: $t$", rf"{ng['t']:.2f}", COST_C),
                (r"the registered book, 2021--25: net Sharpe", rf"{e['hold']['sharpe']:.2f}", GOOD),
                (r"the trial counter", comma(e["trials"]), QC.HOUSE)]
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
        with self.voiceover(
            "The first sheet. <bookmark mark='a'/> Distance pairs on industries lost money. Cointegration tests passed "
            "about twice as many pairs as chance would, and almost none passed again a year later. The Kalman spread "
            "looked perfect and was a forecast error. Reversal across portfolios came from cross terms, not from each "
            "portfolio's own past. The residual book reverted strongly before costs and lost after them with the "
            "standard bands; the research chapter's band kept a little. The network learned almost nothing. The "
            "liquidity story did not show on industries. And the registered book's sealed years are the last line but "
            "one."
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
            "Chapter four's fit in twelve lines. Regress tomorrow's spread on today's; if the slope is not between zero "
            "and one, the spread is not mean-reverting and the function says so instead of inventing a speed. "
            "Otherwise the speed is minus the log of the slope, the mean is the intercept over one minus the slope, and "
            "the equilibrium deviation comes from the residuals. The s-score divides by that last number."
        ):
            self.play(FadeIn(card))
            self.wait(1.5)
        self.clear_scene()

    def lab2(self):
        card = house_lab(r"The band rule's profit rate", SA.band_rate, "return (m - c)", 1,
                         extra=((SA.ou_time_to_mean, "k2 = kappa", 2), (SA.ou_time_to_band, "k2 = kappa", 2)), width=10.6)
        card.move_to(ORIGIN)
        with self.voiceover(
            "The research chapter's theorem, as code. The profit rate is the band minus the round-trip cost, divided by "
            "the expected length of a cycle: the time from the band back to the mean, plus the time from the mean out "
            "to the band. Each is a double integral from Dynkin's formula, computed by Simpson's rule. Four lines, and "
            "the band the House trades comes from them."
        ):
            self.play(FadeIn(card))
            self.wait(1.5)
        self.clear_scene()

    def lab3(self):
        card = house_lab(r"Lo and MacKinlay's decomposition", SA.lo_mackinlay, "R = np.asarray(R, float)", 13,
                         width=10.6)
        card.move_to(ORIGIN)
        with self.voiceover(
            "And Chapter seven's decomposition. The contrarian's expected profit splits exactly into minus each "
            "asset's own autocovariance, plus the cross terms where one asset's past predicts another's future, plus "
            "the spread of mean returns. The function returns all three and the profit actually earned, so the identity "
            "is checked every time it runs."
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
            desk_question(r"leverage", r"a 3\% volatility book is levered several times to be worth running, so a "
                          r"week like August 2007 is a margin call, not a drawdown", width=12.0, font_size=19),
            desk_question(r"what the House holds", r"the registered book at its tested size and costs; it grows only when "
                          r"the measured cost of trading (Part 37) shows room", width=12.0, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Before it is traded, three practical limits. <bookmark mark='a'/> Capacity: a residual book's own trades move "
            "the prices it wants to buy cheaply, and Part thirty-one's square-root law makes the cost per dollar grow "
            "with size. <bookmark mark='b'/> Leverage: a book with three percent volatility must be levered several times "
            "to be worth running, so a week like August 2007 becomes a margin call. <bookmark mark='c'/> So the House "
            "holds the registered book at its tested size, and lets it grow only when measured costs show room."
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
                          r"means the factor model no longer describes the market", width=12.0, font_size=19),
            desk_question(r"the stop", r"a loss beyond three times the book's daily volatility over a week cuts its size "
                          r"by half, decided now, before a crowd makes the decision for it", width=12.0, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "And how the desk watches it. <bookmark mark='a'/> Every day: turnover against its budget, the cost actually "
            "paid against the five basis points assumed, and the book's factor exposures, which should be zero. "
            "<bookmark mark='b'/> Every week: the spread of the residuals and the share that still fit a mean-reverting "
            "model; a falling share means the factor model has stopped describing the market. <bookmark mark='c'/> And a "
            "stop written in advance: a weekly loss beyond three daily volatilities halves the book, decided now, "
            "before a crowd decides it in August."
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
