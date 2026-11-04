from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from explainer.quant.house import macro as M
from videos.quant.quant22.common import BAD, BASIS, CARRY, GOOD, INFL, OIL, PART, house_lab, load


class House(VoiceoverScene):
    def construct(self):
        self.card()
        self.sheet(load("cip"), load("carry"), load("oil"), load("basis"), load("inflation"))
        self.lab()
        self.module()
        self.test()

    def card(self):
        c = chapter_card(13, r"Rule 22: the macro desk", r"What does every macro trade need to be told?", part=PART)
        with self.voiceover("Chapter thirteen. The House's twenty-second rule, for its macro desk."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def sheet(self, c, k, o, b, i):
        st = k["stats"]
        rows = [(r"sterling CIP basis, 2010--16 average", rf"{c['mean_post_bp']:.0f}\ \text{{bp}}", BASIS),
                (r"carry: Sharpe, skew, worst month", rf"{st['sharpe']:.2f},\ {st['skew']:.2f},\ {100 * st['worst']:.1f}\%",
                 CARRY),
                (r"WTI: days in contango since 1986", rf"{100 * o['contango_share']:.0f}\%", OIL),
                (r"WTI: rolled futures against the price", rf"{100 * o['cagr_index']:.1f}\%\ \text{{vs}}\ "
                                                            rf"{100 * o['cagr_spot']:.1f}\%\ \text{{a year}}", OIL),
                (r"leveraged funds' Treasury futures, net", rf"\${b['lev_last'] / 1000:.2f}\ \text{{trillion}}", BAD),
                (r"5-year breakeven less realised CPI", rf"{100 * i['gap_mean']:+.2f}\ \text{{points}}", INFL)]
        hx = [-2.4, 3.6]
        tab = VGroup()
        for j, (a, v, c_) in enumerate(rows):
            y = 2.1 - 0.62 * j
            tab.add(VGroup(label(a, font_size=20, color=c_).move_to([hx[0], y, 0]), MathTex(v, font_size=28).move_to(
                [hx[1], y, 0])))
        title = label(r"The macro desk's first sheet", font_size=28).to_edge(UP, buff=0.4)
        foot = wrapped_label(r"every number computed in this part from public data; none is a forecast, and none is "
                             r"advice", 12.0, 18, GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The macro desk's first sheet, every number from this part. <bookmark mark='a'/> A riskless basis that "
            "stays open because balance sheet costs money. A carry trade with a good Sharpe ratio and a bad left tail. "
            "An oil curve that spends more than half its days in contango, and a futures index that earned half what "
            "the price did. A trillion dollars of leveraged Treasury shorts. And a breakeven that is a price, not a "
            "forecast. Each number is a warning as much as an opportunity."
        ) as vo:
            self.play(FadeIn(title))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in tab], lag_ratio=0.35), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def lab(self):
        card = house_lab(r"Covered interest parity, in the House", M.cip_basis, "return cc(r_usd", 1,
                         extra=((M.implied_convenience, "return r - np.log", 1), (M.implied_repo, "inv = invoice_price", 2)),
                         width=9.0)
        card.to_edge(UP, buff=0.6)
        with self.voiceover(
            "Three lines from the House's new module carry most of this part. The basis: the dollar rate, less the "
            "foreign rate, less the forward premium. The convenience yield: the financing rate, less the slope of the "
            "futures curve. And the implied repo rate of a bond delivered into its future. Each is an arbitrage "
            "relation turned into a measurement: what is left over is the price of something scarce. In currencies "
            "it is balance sheet; in oil, a tank; in Treasuries, a repo lender willing to roll the loan tomorrow. The "
            "desk's job is to know which, and what it costs today."
        ):
            self.play(FadeIn(card))
            self.wait(1.5)
        self.clear_scene()

    def module(self):
        chart = house_chart(PART, lit=("macro",)).scale(0.62).to_edge(UP, buff=0.2)
        rows = [
            (r"\texttt{cip\_forward}, \texttt{cip\_basis}", r"covered parity and the cross-currency basis"),
            (r"\texttt{fama\_regression}, \texttt{carry\_sort}, \texttt{crash\_stats}", r"uncovered parity and carry"),
            (r"\texttt{garman\_kohlhagen}, \texttt{fx\_delta}, \texttt{strike\_from\_delta}", r"FX options, four deltas"),
            (r"\texttt{carry\_forward}, \texttt{implied\_convenience}, \texttt{rolled\_front}", r"storage and the roll"),
            (r"\texttt{implied\_repo}, \texttt{gross\_basis}, \texttt{net\_basis}", r"the Treasury basis"),
            (r"\texttt{breakeven}, \texttt{attack\_model}", r"inflation; a peg's last day"),
        ]
        tab = VGroup(*[VGroup(label(a, font_size=16, color=QC.HOUSE), label(b_, font_size=16, color=GREY_A)).arrange(
            RIGHT, buff=0.4) for a, b_ in rows]).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        for r_ in tab:
            r_[1].align_to(tab, LEFT).shift(RIGHT * 7.4)
        tab.next_to(chart, DOWN, buff=0.25)
        if tab.width > 13.0:
            tab.scale_to_fit_width(13.0)
        rule = wrapped_label(r"Rule 22: every arbitrage that needs balance sheet is charged for it; every peg, floor and "
                             r"regime is stressed for its end; every commodity position is sized against the physical "
                             r"market that must take it (storage, delivery, a ship); every model is valid for every price "
                             r"the contract allows, negative ones included; and carry is sized for its worst month, not "
                             r"its Sharpe ratio.", 12.4, 20, QC.HOUSE).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "The macro desk opens with these tools. <bookmark mark='a'/> Covered parity and its basis; uncovered "
            "parity and carry; currency options with their four deltas; storage, the convenience yield and the roll; "
            "the Treasury basis; breakevens; and a model of a peg's last day. <bookmark mark='b'/> And the "
            "twenty-second rule. Every arbitrage that needs balance sheet is charged for it. Every peg, floor and "
            "regime is stressed for its end. Every commodity position is sized against the physical market that must "
            "take it: the storage, the delivery point, the ship. Every model is valid for every price the contract "
            "allows, negative ones included. And carry is sized for its worst month, not its Sharpe ratio."
        ) as vo:
            self.play(FadeIn(chart))
            self.play(Indicate(chart.desk["macro"], color=QC.HOUSE, scale_factor=1.05))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab], lag_ratio=0.4, run_time=5))
            vo.wait_until("b")
            self.play(FadeIn(rule))
        self.wait(0.4)
        self.clear_scene()


    def test(self):
        cards = VGroup(
            desk_question(r"the franc, 2015", r"stress every floor for its end: a short option on the floor's removal, "
                          r"sized as a jump, not a diffusion, would have shown FXCM-style losses before they happened",
                          width=12.0, font_size=19),
            desk_question(r"Amaranth, 2006", r"size against the physical market: positions that are a large share of a "
                          r"month's open interest have no exit price", width=12.0, font_size=19),
            desk_question(r"negative oil, 2020", r"a model valid for every price the contract allows, and a position that "
                          r"never holds a delivery month without storage to take it", width=12.0, font_size=19),
            desk_question(r"the basis trade, March 2020", r"charge for balance sheet and stress the financing: a trade "
                          r"financed overnight is sized for the day the repo lender raises the haircut", width=12.0,
                          font_size=19),
        ).arrange(DOWN, buff=0.22)
        if cards.height > 6.8:
            cards.scale_to_fit_height(6.8)
        with self.voiceover(
            "Hold the rule against this part's cases. <bookmark mark='a'/> The franc: a floor stressed for its end, "
            "priced as a jump rather than a diffusion, shows the losses before they happen. <bookmark mark='b'/> "
            "Amaranth: a position sized against the physical market would never have been a large share of a month's "
            "open interest. <bookmark mark='c'/> Negative oil: a model valid at every price, and no delivery month "
            "held without a tank. <bookmark mark='d'/> And the basis trade: balance sheet charged for, and financing "
            "stressed for the morning the haircut goes up. None of these rules needs hindsight; each needs only the "
            "contract's terms, and a little imagination about the day nobody wants to buy."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c", "d")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.5)
        self.clear_scene()
