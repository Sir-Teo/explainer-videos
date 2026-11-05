from __future__ import annotations

from explainer.quant import *  # noqa: F403
from explainer.quant.house import defi as D
from videos.quant.quant39.common import (
    ARB_C,
    BAD,
    HURDLE,
    PART,
    PERP_C,
    POOL_C,
    STABLE_C,
    house_lab,
    load,
)


class House(VoiceoverScene):
    def construct(self):
        self.answer()
        self.card()
        self.sheet(load("lvr"), load("fees"), load("v3"), load("funding"), load("carry"), load("stable"))
        self.venues()
        self.contracts()
        self.keys()
        self.lab()
        self.lab2()
        self.lab3()
        self.lab4()
        self.module()
        self.test()

    def answer(self):
        rows = [cmath(r"\text{1. venues}", r":", r"\text{a cap on collateral at any one exchange}", font_size=34,
                      colors={r"\text{1. venues}": BAD}),
                cmath(r"\text{2. dollars}", r":", r"\text{a cap on any one stablecoin}", font_size=34,
                      colors={r"\text{2. dollars}": STABLE_C}),
                cmath(r"\text{3. pools}", r":", r"\text{fees above measured LVR, hedged}", font_size=34,
                      colors={r"\text{3. pools}": POOL_C})]
        whys = [why(r"Chapter 7: the carry book's real tail is the venue, so the House limits what any exchange holds, "
                    r"and keeps spot in custody where it can"),
                why(r"Chapter 8: a stablecoin is a bank without insurance; the cash leg is spread across issuers and "
                    r"partly held in dollars"),
                why(r"Chapters 3 and 4 and the research chapter: provide liquidity only where fee income beats LVR at "
                    r"the arbitrage frequency, with the token exposure hedged")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "The answer to the pause. <bookmark mark='a'/> First, venues: a cap on the collateral any one exchange "
            "holds, because the carry book's real tail is the venue. <bookmark mark='b'/> Second, dollars: a cap on any "
            "one stablecoin, because each is a bank without insurance. <bookmark mark='c'/> Third, pools: provide "
            "liquidity only where fees beat the measured loss to arbitrage, with the token exposure hedged."
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

    def card(self):
        c = chapter_card(10, r"Rule 39: count the risks the returns do not show", r"What must a digital-assets desk "
                         r"measure that no backtest contains?", part=PART)
        with self.voiceover("Chapter ten. The House's thirty-ninth rule belongs to its new digital-assets desk. Its "
                            "strategies have the smoothest returns in the Track Record and the largest risks that never "
                            "appear in them."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def sheet(self, lv, fe, v3, fu, ca, st):
        f3 = [x for x in fe["eth"] if abs(x["fee"] - 0.003) < 1e-9][0]
        e5 = [r for r in v3["rows"] if abs(r["w"] - 1.05) < 1e-9][0]
        rows = [(r"ETH pool, 2023: loss to arbitrage, \% of value", rf"{lv['lvr_pct']:.2f}", ARB_C),
                (r"the same from realised variance over eight", rf"{lv['rv8_pct']:.2f}", HURDLE),
                (r"arbitrageurs' share of LVR at a 0.3\% fee, real minutes", rf"{f3['arb_lvr']:.2f}", ARB_C),
                (r"a $\pm 5\%$ range: liquidity per dollar; days the price left it", rf"{e5['eff']:.0f}\times,\ "
                 rf"{100 * e5['days_left']:.0f}\%", POOL_C),
                (r"BTC funding: average a year; at exactly 0.01\%", rf"{fu['BTCUSDT']['annual_pct']:.1f}\%,\ "
                 rf"{100 * fu['BTCUSDT']['at_base']:.0f}\%", PERP_C),
                (r"carry book: research, hold-out Sharpe", rf"{ca['res']['sharpe']:.1f},\ {ca['hold']['sharpe']:.1f}", PERP_C),
                (r"USDC's low against tether, March 2023", rf"{st['usdc']['low']:.3f}", STABLE_C)]
        hx = [-2.2, 4.8]
        tab = VGroup()
        for j, (txt, val, col) in enumerate(rows):
            y = 2.4 - 0.62 * j
            tab.add(VGroup(label(txt, font_size=16, color=col).move_to([hx[0], y, 0]),
                           MathTex(val, font_size=24).move_to([hx[1], y, 0])))
        title = label(r"The digital-assets desk's first sheet", font_size=28).to_edge(UP, buff=0.25)
        foot = wrapped_label(r"computed in this part from Binance's public archive (spot and perpetual candles, funding, "
                             r"USDC, UST, LUNA, FTT), Yahoo Finance's bars, and simulation; none is advice", 12.0, 15,
                             GREY_A).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "The first sheet. <bookmark mark='a'/> A pool that lost its variance over eight to arbitrage, to the second "
            "decimal, and arbitrageurs who kept far more of it than the Brownian theory allows. A concentrated range "
            "that multiplies both the fees and the loss. Funding pinned at the interest term most of the time. A carry "
            "book whose Sharpe ratio halved out of sample and still looks like free money. And a dollar token that "
            "traded at eighty-eight cents."
        ) as vo:
            self.play(FadeIn(title))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in tab], lag_ratio=0.4), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def venues(self):
        cards = VGroup(
            desk_question(r"spot in custody, margin minimal", r"the spot leg sits with a regulated custodian, posted to "
                          r"the exchange only as collateral it can recall; the short's margin is kept near its minimum",
                          width=12.0, font_size=19),
            desk_question(r"several venues, each capped", r"no exchange holds more than a set share of capital; a venue's "
                          r"withdrawals are tested regularly, and slow ones trigger a cut", width=12.0, font_size=19),
            desk_question(r"the counterparty file", r"Part 21's credit review for every exchange: ownership, audits, "
                          r"liabilities as well as reserves, and where the customers' assets legally sit", width=12.0,
                          font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Venues. <bookmark mark='a'/> Spot sits with a regulated custodian and is posted to an exchange only as "
            "collateral that can be recalled; the short's margin is kept near its minimum. <bookmark mark='b'/> No "
            "exchange holds more than a set share of capital, and withdrawals are tested regularly. "
            "<bookmark mark='c'/> And each exchange gets Part twenty-one's credit file: who owns it, who audits it, its "
            "liabilities as well as its reserves, and where customers' assets legally sit."
        ) as vo:
            for k_, mk_ in enumerate(("a", "b", "c")):
                vo.wait_until(mk_)
                self.play(FadeIn(cards[k_], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def contracts(self):
        cards = VGroup(
            desk_question(r"code is the counterparty", r"a pool or a lending protocol is only as safe as its contract; "
                          r"exploits of bridges and protocols have taken hundreds of millions at a time, as reported",
                          width=12.0, font_size=19),
            desk_question(r"audits and age", r"the House uses only audited contracts with long records and large "
                          r"deposits at stake, and caps exposure to each", width=12.0, font_size=19),
            desk_question(r"oracles", r"a protocol that reads a manipulable price can be drained by a flash loan "
                          r"(Chapter 2); the House checks what each one reads", width=12.0, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Contracts. <bookmark mark='a'/> On chain, the code is the counterparty, and exploits of bridges and "
            "protocols have taken hundreds of millions of dollars at a time, as reported. <bookmark mark='b'/> The House "
            "uses only audited contracts with long records and much at stake, and caps exposure to each. "
            "<bookmark mark='c'/> And it checks what price each protocol reads, because a manipulable oracle can be "
            "drained with a flash loan."
        ) as vo:
            for k_, mk_ in enumerate(("a", "b", "c")):
                vo.wait_until(mk_)
                self.play(FadeIn(cards[k_], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def keys(self):
        cards = VGroup(
            desk_question(r"keys", r"no single person can move funds: several signers, or keys split by multi-party "
                          r"computation, with limits per transaction", width=12.0, font_size=19),
            desk_question(r"always open", r"the market never closes, so neither do the limits: automated checks and an "
                          r"on-call trader every hour of the week", width=12.0, font_size=19),
            desk_question(r"compliance", r"Part 34's controls apply: sanctions screening of counterparties and "
                          r"addresses, and the record of every on-chain transaction", width=12.0, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Operations. <bookmark mark='a'/> No single person can move funds: several signers, or keys split by "
            "multi-party computation, with limits per transaction. <bookmark mark='b'/> The market never closes, so "
            "neither do the limits: automated checks and an on-call trader every hour of the week. "
            "<bookmark mark='c'/> And Part thirty-four's compliance applies on chain: sanctions screening of addresses, "
            "and a record of every transaction."
        ) as vo:
            for k_, mk_ in enumerate(("a", "b", "c")):
                vo.wait_until(mk_)
                self.play(FadeIn(cards[k_], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def lab(self):
        card = house_lab(r"A pool against arbitrageurs", D.arb_pool, "if g * P > p[t]:", 8, width=10.6)
        card.move_to(ORIGIN)
        with self.voiceover(
            "Chapter three's simulator at its core. In each block, if the pool's price net of the fee is above the "
            "market, an arbitrageur sells it the token until the band's edge; if below, buys; and inside the band, "
            "nothing happens."
        ):
            self.play(FadeIn(card))
            self.wait(1.5)
        self.clear_scene()

    def lab2(self):
        card = house_lab(r"Loss-versus-rebalancing, exact", D.lvr_step_cpmm, "return np.asarray(V0, float) / 2", 1,
                         extra=((D.lvr_rate_cpmm, "return sigma ** 2 / 8", 1),
                                (D.p_trade_theory, "return 1.0 / (1.0 + fee", 1)), width=10.6)
        card.move_to(ORIGIN)
        with self.voiceover(
            "The research chapter in three lines: the exact one-step loss, the continuous rate sigma squared over eight, "
            "and the probability that a block holds an arbitrage."
        ):
            self.play(FadeIn(card))
            self.wait(1.5)
        self.clear_scene()

    def lab3(self):
        card = house_lab(r"A sandwich", D.sandwich, "def run(a):", 5, width=10.6)
        card.move_to(ORIGIN)
        with self.voiceover(
            "Chapter five's attack: the attacker's purchase, the victim's, and the attacker's sale; the front-run is "
            "the largest that keeps the victim within its limit."
        ):
            self.play(FadeIn(card))
            self.wait(1.5)
        self.clear_scene()

    def lab4(self):
        card = house_lab(r"Funding and the perpetual's price", D.binance_funding_rule, "premium = np.asarray(premium", 2,
                         extra=((D.perp_multiplier, "return kappa / (kappa - (r - q))", 1),), width=10.6)
        card.move_to(ORIGIN)
        with self.voiceover(
            "And Chapter six: Binance's funding rule, the premium plus a clamped interest term, and the perpetual's "
            "no-arbitrage multiple of spot."
        ):
            self.play(FadeIn(card))
            self.wait(1.5)
        self.clear_scene()

    def module(self):
        chart = house_chart(PART, lit=("digital",)).scale(0.62).to_edge(UP, buff=0.2)
        rows = [
            (r"\texttt{cpmm\_swap}, \texttt{v3\_reserves}, \texttt{impermanent\_loss}", r"pools"),
            (r"\texttt{arb\_pool}, \texttt{lvr\_step\_cpmm}, \texttt{p\_trade\_theory}", r"what pools lose"),
            (r"\texttt{sandwich}, \texttt{binance\_funding\_rule}, \texttt{perp\_multiplier}", r"ordering and perpetuals"),
        ]
        tab = VGroup(*[VGroup(label(a_, font_size=15, color=QC.HOUSE), label(b_, font_size=15, color=GREY_A)).arrange(
            RIGHT, buff=0.4) for a_, b_ in rows]).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        for r_ in tab:
            r_[1].align_to(tab, LEFT).shift(RIGHT * 9.6)
        tab.next_to(chart, DOWN, buff=0.25)
        if tab.width > 13.0:
            tab.scale_to_fit_width(13.0)
        rule = wrapped_label(r"Rule 39: the House values every pool position against rebalancing, at the arbitrage "
                             r"frequency and with fat tails; caps the collateral at any one venue and the exposure to any "
                             r"one stablecoin; and sizes carry by the loss of a venue, not by its Sharpe ratio.", 12.4, 17,
                             QC.HOUSE).to_edge(DOWN, buff=0.2)
        with self.voiceover(
            "The tools this part adds. <bookmark mark='a'/> Pools, what pools lose, and ordering and perpetuals. "
            "<bookmark mark='b'/> And the thirty-ninth rule. The House values every pool position against rebalancing, "
            "at the frequency of arbitrage and with fat tails. It caps the collateral at any one venue and the exposure "
            "to any one stablecoin. And it sizes carry by the loss of a venue, not by its Sharpe ratio."
        ) as vo:
            self.play(FadeIn(chart))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab], lag_ratio=0.4, run_time=3))
            vo.wait_until("b")
            self.play(FadeIn(rule))
        self.wait(0.5)
        self.clear_scene()

    def test(self):
        cards = VGroup(
            desk_question(r"a liquidity pool advertised by its fee yield", r"ask for its LVR at the arbitrage frequency: "
                          r"fees without the loss are half the account (Chapter 3)", width=12.0, font_size=19),
            desk_question(r"a basis fund with a Sharpe ratio of four", r"ask where the collateral sits, in which stablecoin, "
                          r"and what one venue's failure would cost (Chapter 7)", width=12.0, font_size=19),
            desk_question(r"a stablecoin paying 20\%", r"ask what the reserves are and who pays the yield; Anchor's "
                          r"depositors learned the answer (Chapter 8)", width=12.0, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "The rule against three cases. <bookmark mark='a'/> A pool advertised by its fee yield: ask for its loss to "
            "arbitrage, because fees without it are half the account. <bookmark mark='b'/> A basis fund with a Sharpe "
            "ratio of four: ask where the collateral sits, in which stablecoin, and what one venue's failure would cost. "
            "<bookmark mark='c'/> A stablecoin paying twenty percent: ask what backs it and who pays the yield."
        ) as vo:
            for k_, mk_ in enumerate(("a", "b", "c")):
                vo.wait_until(mk_)
                self.play(FadeIn(cards[k_], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()
