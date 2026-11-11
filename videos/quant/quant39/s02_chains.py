from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant39.common import prediction_card
from videos.quant.quant39.common import (
    BAD,
    PART,
    PERP_C,
    POOL_C,
    SPOT_C,
    STABLE_C,
    load,
)


class Chains(VoiceoverScene):
    def construct(self):
        s = load("stable")
        self.card()
        self.ledger()
        self.consensus()
        self.two_venues()
        self.always_open()
        self.clearing()
        self.ftx_chart(s)
        self.ftx_lessons()
        self.cash_leg()
        self.question()

    def card(self):
        c = chapter_card(1, r"Blockchains and exchanges", r"What is a market with no closing bell and, sometimes, no "
                         r"exchange?", part=PART)
        with self.voiceover("Chapter one. Crypto markets trade on two kinds of venue at once: exchanges that look like "
                            "the ones of Parts thirty-five to thirty-eight, and programs on a public ledger that need no "
                            "exchange at all. Both run every hour of every day."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def ledger(self):
        blocks = VGroup()
        for i in range(5):
            b = RoundedRectangle(width=2.0, height=1.3, corner_radius=0.12, stroke_color=POOL_C, stroke_width=2,
                                 fill_color=POOL_C, fill_opacity=0.08)
            t = VGroup(label(rf"block {100 + i}", font_size=18, color=POOL_C),
                       label(r"transactions", font_size=15, color=GREY_A),
                       label(r"hash of the last", font_size=15, color=GREY_B)).arrange(DOWN, buff=0.08).move_to(b)
            blocks.add(VGroup(b, t))
        blocks.arrange(RIGHT, buff=0.5).move_to(UP * 0.6)
        links = VGroup(*[Arrow(blocks[i].get_right(), blocks[i + 1].get_left(), buff=0.05, stroke_width=3,
                               color=GREY_B, tip_length=0.15) for i in range(4)])
        notes = VGroup(why(r"a public ledger: anyone can read it, and anyone can propose transactions"),
                       why(r"each block commits to the one before it, so changing history means redoing everything since"),
                       why(r"programs (smart contracts) live on it too: a pool is a contract that holds tokens and "
                           r"follows its formula")).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "A blockchain is a public ledger. <bookmark mark='a'/> Anyone can read it and anyone can propose "
            "transactions, which are gathered into blocks. <bookmark mark='b'/> Each block commits to the one before "
            "it, so changing the past means redoing everything since. <bookmark mark='c'/> And programs live on it "
            "too. A trading pool is a contract that holds tokens and follows its formula, with no one in between."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(b_) for b_ in blocks], lag_ratio=0.2), run_time=2)
            vo.wait_until("a")
            self.play(FadeIn(notes[0]), LaggedStart(*[GrowArrow(l_) for l_ in links], lag_ratio=0.2))
            vo.wait_until("b")
            self.play(FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()

    def consensus(self):
        rows = [cmath(r"\text{Bitcoin}", r":", r"\text{proof of work, a block every} \sim 10\ \text{minutes}", font_size=34,
                      colors={r"\text{Bitcoin}": SPOT_C}),
                cmath(r"\text{Ethereum}", r":", r"\text{proof of stake since 2022, a slot every } 12\ \text{s}", font_size=34,
                      colors={r"\text{Ethereum}": POOL_C}),
                cmath(r"\text{gas}", r":", '\\text{computation units; base and priority fees}', font_size=34),
                cmath(r"\text{who orders}", r":", r"\text{the block's producer}", font_size=34, colors={r"\text{who orders}": BAD})]
        whys = [why(r"Satoshi Nakamoto's 2008 design: miners compete in proof of work; valid-chain selection follows cumulative work"),
                why(r"validators who stake ether take turns proposing blocks, with finality after about two epochs"),
                why(r"every transaction pays for its space in the block: a market for being included"),
                why(r"whoever builds the block decides the order of its transactions: the root of Chapter 5")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "Who writes the ledger. <bookmark mark='a'/> Bitcoin targets a block about every ten minutes; proof-of-work chain selection follows cumulative work among valid chains. <bookmark mark='b'/> Since the September twenty twenty-two Merge, Ethereum uses proof of stake and twelve-second slots, some of which can be missed. Finality requires validator votes and can be delayed. <bookmark mark='c'/> Gas measures computation. Inclusion pays a protocol base fee and priority fees under the applicable rules, rather than one undifferentiated auction. <bookmark mark='d'/> Builders and proposers influence inclusion and order, subject to transaction validity and their arrangements."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c", "d")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def two_venues(self):
        cards = VGroup(
            desk_question(r"centralised exchanges", r"Binance, Coinbase, OKX: custodial accounts, order books matched "
                          r"off chain, perpetual futures with leverage; most price discovery happens here", width=12.4,
                          font_size=19),
            desk_question(r"decentralised exchanges", r"Uniswap and Curve: AMM contracts hold pooled assets; other DEX designs can use order books; "
                          r"prices set by formulas and moved by arbitrageurs", width=12.4, font_size=19),
            desk_question(r"between them", r"bridges, stablecoins and arbitrageurs who trade both, all day: the House's "
                          r"digital-assets desk will live here", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        self.add(cards[0])
        with self.voiceover(
            "Two venue families. <bookmark mark='a'/> Centralized venues generally hold customer assets and match orders in off-chain books; products and custody arrangements vary. <bookmark mark='b'/> Decentralized venues execute through contracts. Automated market makers are one design, but on-chain order books and hybrid designs also exist. Users retain keys until execution while pooled assets remain exposed to contracts and any administrative controls. <bookmark mark='c'/> Stablecoins, bridges and arbitrageurs connect venues. Public settlement does not eliminate custody, oracle, contract or execution risk."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def always_open(self):
        rows = [cmath(r"\text{hours a year}", r"=", r"8{,}760\ \text{against about } 1{,}640", font_size=36),
                cmath(r"\text{weekends}", r":", r"\text{varies with venue, period and product}", font_size=36),
                cmath(r"\sigma_{\text{year}}", r"=", r"\sigma_{\text{day}}\sqrt{365}", font_size=40, colors={r"\sigma_{\text{year}}": SPOT_C})]
        whys = [why(r"every hour of every day, against a stock exchange's six and a half hours on about 252 days"),
                why('a historical comparison is sample-specific; weekends change bank access and liquidity, without a constant volume ratio'),
                why('square-root calendar scaling assumes comparable independent increments; dependence and liquidity changes require a richer model')]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.6, edge=6.9)
        with self.voiceover(
            "A market with continuous calendar time. <bookmark mark='a'/> A non-leap year has eight thousand seven hundred sixty hours; a six-and-a-half-hour stock session over two hundred fifty-two days gives about sixteen hundred thirty-eight. Actual venues can halt or become inaccessible. <bookmark mark='b'/> Weekend liquidity varies by venue, period and product; a historical comparison does not establish a constant half-volume rule. <bookmark mark='c'/> For comparable independent daily increments, volatility scales with the square root of three hundred sixty-five calendar days. Serial dependence, jumps and changing liquidity require a richer model. A calendar convention alone does not predict when the largest move will occur."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def clearing(self):
        rows = [cmath(r"\text{the exchange}", r"=", r"\text{broker} + \text{venue} + \text{clearing house}", font_size=36,
                      colors={r"\text{the exchange}": PERP_C}),
                cmath(r"\text{margin}", r":", r"\text{marked continuously, liquidated by machine}", font_size=34),
                cmath(r"\text{shortfall}", r"\to", r"\text{insurance fund} \to \text{auto-deleveraging}", font_size=34,
                      colors={r"\text{shortfall}": BAD})]
        whys = [why(r"a centralised crypto exchange holds the assets, runs the book and stands between buyer and seller, "
                    r"roles that Parts 21 and 35 kept apart"),
                why(r"Part 2's margin account: positions are closed automatically when equity falls below maintenance"),
                why(r"if a liquidation cannot be filled above the bankruptcy price, the exchange's insurance fund pays; "
                    r"when that runs out, winning positions are cut")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.6, edge=6.9)
        with self.voiceover(
            "And the plumbing. <bookmark mark='a'/> A centralised crypto exchange is broker, venue and clearing house at "
            "once, roles that Parts twenty-one and thirty-five kept apart. <bookmark mark='b'/> Margin is marked "
            "continuously and positions are liquidated by machine, Part two's margin account. <bookmark mark='c'/> If a "
            "liquidation cannot be filled, the exchange's insurance fund pays; when it runs out, profitable positions "
            "on the other side are cut, which is called auto-deleveraging."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def ftx_chart(self, s):
        f = s["FTTUSDT"]
        t = (np.asarray(f["t"], float) - f["t"][0]) / 86400
        p = np.asarray(f["p"], float)
        g = axes([0, float(t[-1])], [0, 30], x_length=7.6, y_length=4.0, xlabel=r"November 2022, days",
                 ylabel=r"FTT on Binance, dollars", xticks=[0, 5, 10, 14], yticks=[0, 10, 20, 30],
                 xfmt=lambda v: f"{int(v) + 1}", font_size=16).move_to(LEFT * 1.2 + DOWN * 0.2)
        ax = g.ax
        line = curve(ax, t, p, BAD, stroke_width=2.5)
        notes = VGroup(label(r"2 Nov: a report on Alameda's balance sheet", font_size=17, color=GREY_A),
                       label(r"6 Nov: Binance says it will sell its FTT", font_size=17, color=GREY_A),
                       label(r"8 Nov: withdrawals stop", font_size=17, color=BAD),
                       label(r"11 Nov: bankruptcy filing", font_size=17, color=BAD))
        notes.arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(RIGHT, buff=0.3).shift(UP * 1.6)
        with self.voiceover(
            "The failure that defined the risk: FTX, in November twenty twenty-two, as reported and as later established "
            f"at trial. <bookmark mark='a'/> FTX's own token, FTT, opened the month at about {f['first']:.0f} dollars on "
            "Binance. A news report questioned the balance sheet of its affiliated trading firm, Alameda, much of it "
            "held in FTT; Binance said it would sell its own FTT. <bookmark mark='b'/> Withdrawals stopped on the "
            f"eighth, and the token fell to about {f['low']:.2f} dollars. Customer assets had been used by the affiliate; "
            "its founder was convicted of fraud in November twenty twenty-three."
        ) as vo:
            self.play(FadeIn(g), Create(line), run_time=2)
            vo.wait_until("a")
            self.play(FadeIn(notes[:2]))
            vo.wait_until("b")
            self.play(FadeIn(notes[2:]))
        self.wait(0.4)
        self.clear_scene()

    def ftx_lessons(self):
        cards = VGroup(
            desk_question(r"venue risk is not in the returns", r"a strategy run on FTX showed nothing unusual until the day "
                          r"it showed everything lost; no backtest contains that day", width=12.4, font_size=19),
            desk_question(r"collateral is the exposure", r"what is held at a venue, margin and spot alike, is lost with "
                          r"it: the House caps it by venue, the way Part 21 priced counterparty exposure", width=12.4,
                          font_size=19),
            desk_question(r"a token as capital", r"a balance sheet built on the issuer's own token is worth what the "
                          r"token fetches in a fire sale, which is very little", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        self.add(cards[0])
        with self.voiceover(
            "Three lessons. <bookmark mark='a'/> Venue risk is not in the returns: a strategy run on FTX looked normal "
            "until the day it was gone, and no backtest contains that day. <bookmark mark='b'/> Collateral is the "
            "exposure: margin and spot held at a venue are lost with it, so the House caps them by venue, the way Part "
            "twenty-one priced counterparty exposure. <bookmark mark='c'/> And a balance sheet built on the issuer's own "
            "token is worth what that token fetches in a fire sale."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def cash_leg(self):
        rows = [cmath(r"\text{USDT, USDC}", r":", r"\text{tokens redeemable for a dollar}", font_size=36,
                      colors={r"\text{USDT, USDC}": STABLE_C}),
                cmath(r"\text{backed by}", r":", r"\text{bank deposits, Treasury bills, repo}", font_size=36),
                cmath(r"\text{the quote currency}", r":", r"\text{BTCUSDT means bitcoin in tether}", font_size=34)]
        whys = [why(r"the issuer mints a token for each dollar received and burns it on redemption"),
                why('reserve-backed tokens have issuer, reserve and redemption risks; their legal structure differs from an insured bank deposit'),
                why(r"almost every crypto price in this part is quoted in a stablecoin, not in dollars")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.6, edge=6.9)
        with self.voiceover(
            "The cash leg needs its own exposure map. <bookmark mark='a'/> Reserve-backed tokens such as tether and USD coin offer specified redemption rights, usually subject to customer eligibility and issuer terms. <bookmark mark='b'/> Deposits, bills and repo can support reserves, but legal claims, access timing and other liabilities matter. The token is not automatically an insured bank deposit. <bookmark mark='c'/> BTCUSDT is a bitcoin quote in tether, not directly in dollars. Treat quote-currency exposure separately from the token being traded and verify the actual issuer's terms."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def question(self):
        q = prediction_card(r"a pool holds 5,000 ether and \$10 million, so its price is \$2,000. A trader buys 500 ether from "
                       r"it, with a 0.3\% fee. What is the average price paid?")
        with self.voiceover(
            "Pause and predict. A pool holds five thousand ether and ten million dollars, so its price is two thousand. "
            "A trader buys five hundred ether from it, paying a fee of three tenths of a percent. What is the average "
            "price paid?"
        ):
            self.play(FadeIn(q))
        self.wait(6)
        self.clear_scene()
