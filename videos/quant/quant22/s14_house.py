from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from explainer.quant.house import macro as M
from videos.quant.quant22.common import BAD, BASIS, CARRY, GOOD, INFL, OIL, PART, house_lab, load


class House(VoiceoverScene):
    def construct(self):
        self.card()
        self.sheet(load("cip"), load("carry"), load("oil_public_example"), load("basis"), load("inflation"))
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
        rows = [
            (r"Sterling basis proxy, 2010--16 mean", rf"{c['mean_post_bp']:.0f}\ \text{{bp/year}}", BASIS),
            (r"Gross carry proxy: Sharpe, skew, worst", rf"{st['sharpe']:.2f},\ {st['skew']:.2f},\ {100*st['worst']:.1f}\%", CARRY),
            (r"Named WTI prices: positive days in contango", rf"{100*o['contango_share']:.0f}\%", OIL),
            (r"20 April 2020: May WTI settlement", r"-\$37.63", OIL),
            (r"2025 leveraged-fund net short, face value", rf"\${abs(b['lev_last'])/1000:.2f}\ \text{{trillion}}", BAD),
            (r"5-year breakeven minus CPI: sample mean", rf"{100*i['gap_mean']:+.2f}\ \text{{pp}}", INFL),
        ]
        tab = VGroup()
        for j, (name, value, color) in enumerate(rows):
            y = 2.15 - 0.7*j
            tab.add(VGroup(wrapped_label(name, 7.2, 20, color).move_to([-2.35,y,0]), MathTex(value,font_size=28).move_to([4.05,y,0])))
        title = label(r"The macro desk: conventions before conclusions",font_size=28).to_edge(UP,buff=0.4)
        foot = wrapped_label(r"Named EIA price illustrations; legacy roll performance unavailable. No forecast or strategy approval. State units, clocks, funding and sample.",12.0,18,GREY_A).to_edge(DOWN,buff=0.4)
        with self.voiceover("The macro desk's first sheet mixes dated descriptive prices and fixed illustrations. <bookmark mark='a'/> A sterling basis proxy has unmatched quote and funding clocks. Carry's saved gross statistics are not a point-in-time portfolio certificate. The named public oil data provide a positive-price contango share and the April 2020 settlement, while the legacy historical roll return is unavailable under its original raw-data pin. Treasury futures net shorts are face notionals, not the size or loss of a basis book. The breakeven-minus-realization gap mixes expectations errors and premia. Each number needs its unit, sample, convention and data clock before it can support a trading decision.") as vo:
            self.play(FadeIn(title), LaggedStart(*[FadeIn(row) for row in tab],lag_ratio=0.15),FadeIn(foot))
            vo.wait_until("a")
            self.play(Indicate(tab[0],scale_factor=1.03))
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
        rule = wrapped_label('Rule 22: every arbitrage that needs balance sheet is charged for it; every peg, floor and regime is stressed for its end; every commodity position is sized against the physical market that must take it (storage, delivery, a ship); every model is valid for every price the contract allows, negative ones included; and carry is stress-tested beyond its observed worst month; a Sharpe ratio does not bound losses.', 12.4, 20, QC.HOUSE).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "The macro desk opens with these tools. <bookmark mark='a'/> Covered parity and its basis; descriptive currency regressions and carry; FX options and quote conventions; storage, roll arithmetic, Treasury financing and inflation prices. <bookmark mark='b'/> Rule twenty-two: charge funding and balance sheet consistently; stress pegs and policy changes; size commodity positions against accessible storage, delivery and market liquidity; check the pricing model's domain against the contract. Stress carry beyond the observed worst month, because a historical extreme is not a loss bound. A source hash, a model assumption and a scenario are useful only when their scope is stated and no unavailable history is silently replaced."
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
            desk_question(r"the franc, 2015", "stress every floor for its end: a short option on the floor's removal, an explicit jump scenario can reveal possible losses without forecasting their date, magnitude or probability",
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
            "Apply the rule as a scenario discipline. <bookmark mark='a'/> For a currency floor, quantify losses under explicit abandonment jumps; a scenario reveals possible exposure without predicting a particular day. <bookmark mark='b'/> For a concentrated gas spread, stress liquidation costs, financing and the positions of other traders, rather than assuming quoted depth is available at scale. <bookmark mark='c'/> For physical oil, identify delivery obligations, accessible storage and a model domain that permits contractually possible prices. <bookmark mark='d'/> For the Treasury basis, stress haircuts, repo renewal, margin and the delivery choices. These checks can expose vulnerabilities; they do not prove that a rule would have prevented each historical loss."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c", "d")):
                if k:
                    vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.5)
        self.clear_scene()
