from __future__ import annotations

from explainer.quant import *  # noqa: F403
from explainer.quant.house import systematic as SY
from videos.quant.quant32.common import (BAD, BOND_C, GOOD, PART, PUT_C, RP_C, TREND_C, VT_C, comma, house_lab, load)


class House(VoiceoverScene):
    def construct(self):
        self.card()
        self.sheet(load("trend"), load("voltarget"), load("riskparity"), load("styles"), load("shortvol"),
                   load("theory"), load("envelope"))
        self.together(load("trend"), load("riskparity"))
        self.lab()
        self.lab2()
        self.lab3()
        self.module()
        self.test()

    def card(self):
        c = chapter_card(10, r"Rule 32: the macro books", r"What must a premium strategy show before the House holds it?",
                         part=PART)
        with self.voiceover("Chapter ten. The House's thirty-second rule: what a premium strategy must show before the "
                            "House will hold it. A premium is held for what it does in bad years, so the rule asks first about those "
                            "years, and only then about the average."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def sheet(self, t, v, r, s, sv, th, e):
        b = e["books"]
        n63 = [x for x in th["data"] if x["n"] == 63][0]
        rows = [(r"trend, 2007--20: Sharpe; 2008 against SPY", rf"{t['main']['sharpe']:.2f};\ "
                 rf"{100 * t['y2008']['trend']:+.0f}\%\ \text{{vs}}\ {100 * t['y2008']['spy']:+.0f}\%", TREND_C),
                (r"volatility targeting: Sharpe up, drawdown down (of 23)", rf"{v['better']},\ {v['dd_better']}", VT_C),
                (r"risk parity and 60/40, 2007--20: Sharpe", rf"{r['rp']['sharpe']:.2f},\ {r['sixty']['sharpe']:.2f}", RP_C),
                (r"stock--bond correlation: 1970s, 2010s", rf"{r['sb']['decades']['1970']:+.2f},\ "
                 rf"{r['sb']['decades']['2010']:+.2f}", BOND_C),
                (r"four styles combined, 1926--2020: Sharpe", rf"{s['styles']['Multi-style']['sharpe']:.2f}", GOOD),
                (r"selling puts: beta, skewness", rf"{sv['beta']:.2f},\ {sv['put']['skew']:.2f}", PUT_C),
                (r"linear trend, 63-day blocks: skewness, data and theory", rf"{n63['skew']:.2f},\ {n63['theory']:.2f}",
                 TREND_C),
                (r"2022: trend, risk parity", rf"{100 * b['trend']['y2022']:+.0f}\%,\ {100 * b['rp']['y2022']:+.0f}\%", BAD),
                (r"the trial counter", comma(e["trials"]), QC.HOUSE)]
        hx = [-2.4, 4.4]
        tab = VGroup()
        for j, (txt, val, col) in enumerate(rows):
            y = 2.5 - 0.56 * j
            tab.add(VGroup(label(txt, font_size=17, color=col).move_to([hx[0], y, 0]),
                           MathTex(val, font_size=24).move_to([hx[1], y, 0])))
        title = label(r"The macro desk's first sheet", font_size=28).to_edge(UP, buff=0.25)
        foot = wrapped_label(r"every number computed in this part from public fund prices, Kenneth French's and FRED's "
                             r"data, Cboe's index and AQR's published series; none is a forecast, and none is advice", 12.0,
                             15, GREY_A).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "The first sheet. <bookmark mark='a'/> Trend following earned a modest Sharpe ratio and made money in 2008. "
            "Volatility targeting cut drawdowns more often than it raised returns. Risk parity trailed sixty-forty in "
            "years when bonds hedged stocks, a sign that has flipped before. The four styles combined were far better "
            "than any one. Selling puts was market beta with a fat left tail. The trend rule's skewness matched its "
            "theory. And in 2022 the trend book made money as risk parity lost it."
        ) as vo:
            self.play(FadeIn(title))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in tab], lag_ratio=0.4), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()


    def together(self, t, r):
        import numpy as np

        def rets(months, cum):
            w = np.r_[1.0, 1 + np.asarray(cum, float)]
            return dict(zip([int(m) for m in months], (w[1:] / w[:-1] - 1).tolist()))
        a = rets(t["months"], t["cum"]["trend"])
        b = rets(r["months"], r["cum"]["rp"])
        c = rets(r["months"], r["cum"]["6040"])
        ks = sorted(set(a) & set(b) & set(c))
        X = np.array([[a[k], b[k], c[k]] for k in ks])
        C = np.corrcoef(X.T)
        names = [r"trend", r"risk parity", r"60/40"]
        cols = [TREND_C, RP_C, QC.CASH]
        cells = VGroup()
        for i in range(3):
            for j in range(3):
                sq = Square(1.3, fill_color=interpolate_color(ManimColor(BLUE_D), ManimColor(RED_D), (C[i, j] + 1) / 2),
                            fill_opacity=0.85 if i != j else 0.3, stroke_color=GREY_D, stroke_width=1)
                sq.move_to([-1.4 + 1.35 * j, 1.3 - 1.35 * i, 0])
                cells.add(VGroup(sq, MathTex(f"{C[i, j]:+.2f}", font_size=26).move_to(sq)))
        rl = VGroup(*[label(n, font_size=18, color=cols[i]).next_to(cells[3 * i][0], LEFT, buff=0.2) for i, n in
                      enumerate(names)])
        head = label(r"The macro books together, monthly, 2007--2020", font_size=28).to_edge(UP, buff=0.4)
        g = VGroup(cells, rl).move_to(DOWN * 0.2)
        tr, rc = C[0, 2], C[1, 2]
        with self.voiceover(
            "How the books sit together. <bookmark mark='a'/> Risk parity is closely correlated with sixty-forty, "
            f"{rc:+.2f}: a different weighting of the same assets. <bookmark mark='b'/> The trend book is nearly "
            f"uncorrelated with both, {tr:+.2f} with sixty-forty. That is why the House's macro desk holds trend beside "
            "the balanced books rather than instead of them: one is a premium for owning assets, the other a premium for "
            "following them, and they fail in different years."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rl))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(x) for x in cells], lag_ratio=0.05))
            vo.wait_until("b")
            self.play(Indicate(VGroup(cells[2], cells[6]), color=WHITE, scale_factor=1.05))
        self.wait(0.4)
        self.clear_scene()

    def lab(self):
        card = house_lab(r"Time-series momentum, as the House runs it", SY.tsmom_positions, "for t in range(T):", 11,
                         width=10.6)
        card.move_to(ORIGIN)
        with self.voiceover(
            "Chapter one's rule in eleven lines. At each month end, and only then, look back over the lookback window; "
            "require nine tenths of the days to be present; take the sign of the trailing return, or its size against "
            "volatility; divide the forty percent risk budget by the asset's volatility; and hold that until the next "
            "month end. Nothing in it knows what the asset is."
        ):
            self.play(FadeIn(card))
            self.wait(1.5)
        self.clear_scene()

    def lab2(self):
        card = house_lab(r"The straddle inside the trend rule", SY.linear_trend_blocks, "k = len(r) // n", 7,
                         extra=((SY.trend_skew_theory, "return 2 ** 1.5", 1),), width=10.6)
        card.move_to(ORIGIN)
        with self.voiceover(
            "And the research chapter's identity: cut the returns into blocks, hold the return so far, and the profit "
            "equals half the squared block return minus half the sum of squares, to the last digit. The line below is "
            "the skewness the chapter proves for it."
        ):
            self.play(FadeIn(card))
            self.wait(1.5)
        self.clear_scene()


    def lab3(self):
        card = house_lab(r"Risk parity, at one rebalance", SY.risk_parity, "for g in set(groups):", 12, width=10.6)
        card.move_to(ORIGIN)
        with self.voiceover(
            "And Chapter four's risk parity at one rebalance. For each asset class, inverse-volatility weights within "
            "it; then the class is divided by its own volatility, so every class carries the same risk; then the whole "
            "book is scaled to the target on the trailing year's covariance, and the leverage cap is the last line of "
            "defence. The correlation assumption is the covariance estimate itself, which is why a year of new "
            "correlations can undo it."
        ):
            self.play(FadeIn(card))
            self.wait(1.5)
        self.clear_scene()

    def module(self):
        chart = house_chart(PART, lit=("macro", "portfolio")).scale(0.62).to_edge(UP, buff=0.2)
        rows = [
            (r"\texttt{ewma\_vol}, \texttt{month\_ends}, \texttt{tsmom\_positions}, \texttt{book}", r"trend"),
            (r"\texttt{vol\_target}, \texttt{inverse\_vol\_weights}, \texttt{risk\_parity}", r"risk budgeting"),
            (r"\texttt{linear\_trend\_blocks}, \texttt{trend\_skew\_theory}, \texttt{trend\_mean\_theory}, "
             r"\texttt{autocov}", r"the identity"),
            (r"\texttt{sharpe}, \texttt{max\_drawdown}, \texttt{skewness}", r"scores"),
            (r"\texttt{data.yahoo\_total}", r"total-return fund prices"),
        ]
        tab = VGroup(*[VGroup(label(a_, font_size=15, color=QC.HOUSE), label(b_, font_size=15, color=GREY_A)).arrange(
            RIGHT, buff=0.4) for a_, b_ in rows]).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        for r_ in tab:
            r_[1].align_to(tab, LEFT).shift(RIGHT * 9.6)
        tab.next_to(chart, DOWN, buff=0.25)
        if tab.width > 13.0:
            tab.scale_to_fit_width(13.0)
        rule = wrapped_label(r"Rule 32: a premium strategy enters the House only with its crisis behaviour shown, year by "
                             r"year, in the worst years of the assets it is meant to diversify; its skewness and its worst "
                             r"month stated next to its Sharpe ratio; its leverage path and the correlation assumption "
                             r"that leverage rests on written down; and its premium explained by who pays it and why they "
                             r"would keep paying.", 12.4, 17, QC.HOUSE).to_edge(DOWN, buff=0.2)
        with self.voiceover(
            "The tools this part adds. <bookmark mark='a'/> Trend; risk budgeting; the identity and its theory; scores; "
            "and a loader for total-return fund prices. <bookmark mark='b'/> And the thirty-second rule. A premium "
            "strategy enters the House only with its behaviour shown in the worst years of the assets it is meant to "
            "diversify; its skewness and worst month stated beside its Sharpe ratio; its leverage, and the correlation "
            "that leverage rests on, written down; and its premium explained by who pays it, and why they would keep "
            "paying."
        ) as vo:
            self.play(FadeIn(chart))
            self.play(Indicate(chart.desk["macro"], color=QC.HOUSE, scale_factor=1.05))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab], lag_ratio=0.4, run_time=4))
            vo.wait_until("b")
            self.play(FadeIn(rule))
        self.wait(0.4)
        self.clear_scene()

    def test(self):
        cards = VGroup(
            desk_question(r"the income fund that sells volatility", r"ask for its worst month and its skewness, then "
                          r"for 2008, 2018 and 2020; a Sharpe ratio alone hides the trade (Chapter 7)", width=12.0,
                          font_size=19),
            desk_question(r"the risk-parity pitch with a backtest from 2000", r"ask what the stock--bond correlation was "
                          r"in the backtest, and what the book loses if it is +0.3 (Chapter 4, Chapter 9)", width=12.0,
                          font_size=19),
            desk_question(r"the CTA with three flat years", r"ask whether there was a slow crisis in them; a straddle "
                          r"bought in a calm market is expected to lose its premium (the research chapter)", width=12.0,
                          font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "The rule against three cases. <bookmark mark='a'/> An income fund that sells volatility: ask for its worst "
            "month, its skewness, and its 2008, 2018 and 2020. <bookmark mark='b'/> A risk-parity pitch with a backtest "
            "from 2000: ask what the stock-bond correlation was, and what happens if it turns positive. "
            "<bookmark mark='c'/> A trend follower with three flat years: ask whether there was a slow crisis in them. "
            "A straddle bought in a calm market is supposed to lose its premium."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()
