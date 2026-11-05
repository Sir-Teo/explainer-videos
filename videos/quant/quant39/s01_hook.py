from __future__ import annotations

from explainer.quant import *  # noqa: F403
from videos.quant.quant39.common import (
    HURDLE,
    PART,
    era_strip,
    load,
)


class Hook(VoiceoverScene):
    def construct(self):
        self.title_card()
        self.question(load("amm"))
        self.claims(load("lvr"), load("fees"), load("carry"))
        self.stakes()
        self.act()
        self.history()
        self.objectives()
        self.house()

    def title_card(self):
        card = part_title(PART, r"Crypto and DeFi")
        disc = note(DISCLAIMER, font_size=18, color=GREY_C).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Part thirty-nine. Crypto and decentralised finance: markets that never close, exchanges that are programs, "
            "futures that never expire, and dollars that are tokens. The closing part of Act six."
        ):
            self.play(FadeIn(card, shift=UP * 0.2), FadeIn(disc))
        self.play(FadeOut(card), FadeOut(disc))

    def question(self, a):
        rows = VGroup(label(r"you supply ether and dollars to an $x \cdot y = k$ pool", font_size=26),
                      label(r"the price of ether doubles", font_size=26, color=GREY_A),
                      label(r"how much worse off are you than if you had just held?", font_size=26, color=HURDLE))
        rows.arrange(DOWN, buff=0.4).move_to(UP * 0.3)
        with self.voiceover(
            "A desk question. <bookmark mark='a'/> You supply ether and dollars to a constant-product pool. "
            "<bookmark mark='b'/> The price of ether doubles. <bookmark mark='c'/> How much worse off are you than if you "
            f"had simply held them? The textbook answer is {100 * abs(a['il2']):.1f} percent. This part shows why that "
            "number is the wrong one to ask for."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.wait(0.4)
        self.clear_scene()

    def claims(self, lv, fe, ca):
        f3 = [x for x in fe["eth"] if abs(x["fee"] - 0.003) < 1e-9][0]
        cards = VGroup(
            desk_question(r"pools lose their variance over eight", rf"on ether's 2023 minutes, a constant-product pool lost "
                          rf"{lv['lvr_pct']:.2f}\% of its value to arbitrage; $\sigma^2/8$ says {lv['rv8_pct']:.2f}\%",
                          width=12.4, font_size=19),
            desk_question(r"fat tails favour arbitrageurs", rf"at a 0.3\% fee, real prices let arbitrageurs keep "
                          rf"{f3['arb_lvr']:.2f} of that loss, about {f3['arb_lvr'] / f3['theory']:.1f} times the Brownian "
                          r"theorem proved here", width=12.4, font_size=19),
            desk_question(r"the carry is real, the risk is elsewhere", rf"a registered cash-and-carry book earned "
                          rf"{ca['hold']['ann_pct']:.0f}\% a year out of sample with a Sharpe ratio of "
                          rf"{ca['hold']['sharpe']:.1f}; one venue failure would erase years of it", width=12.4,
                          font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "What this part finds. <bookmark mark='a'/> A pool loses its variance over eight to arbitrageurs: on ether's "
            f"twenty twenty-three minutes, {lv['lvr_pct']:.2f} percent of its value, against {lv['rv8_pct']:.2f} from the "
            "formula. <bookmark mark='b'/> Fat tails favour arbitrageurs: on real prices they keep about "
            f"{f3['arb_lvr'] / f3['theory']:.1f} times the share of that loss that the Brownian theorem, proved here, "
            "predicts. <bookmark mark='c'/> And the carry trade is real but its risk is elsewhere: a registered "
            f"cash-and-carry book earned {ca['hold']['ann_pct']:.0f} percent a year in the sealed hold-out, and one "
            "exchange failure would have erased years of it."
        ) as vo:
            for k, mk_ in enumerate(("a", "b", "c")):
                vo.wait_until(mk_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def stakes(self):
        cards = VGroup(
            desk_question(r"a market the size of a major asset class", r"trillions of dollars of tokens, tens of billions "
                          r"traded a day, and the most traded futures contract in the world by some counts", width=12.4,
                          font_size=19),
            desk_question(r"a laboratory", r"every trade, quote and pool is public: microstructure that Parts 35--38 "
                          r"could only model is here in the data", width=12.4, font_size=19),
            desk_question(r"why the House cares", r"its funds now hold Bitcoin ETFs, its counterparties hold stablecoins, "
                          r"and its desks trade against the same arbitrageurs", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Why it matters. <bookmark mark='a'/> It is a market the size of a major asset class, with trillions of "
            "dollars of tokens and the most traded futures contracts in the world by some counts. <bookmark mark='b'/> "
            "It is a laboratory: every trade, quote and pool is public, so the microstructure that Parts thirty-five to "
            "thirty-eight modelled is in the data. <bookmark mark='c'/> And the House's world now touches it: funds hold "
            "Bitcoin ETFs, counterparties hold stablecoins, and its desks trade against the same arbitrageurs."
        ) as vo:
            for k, mk_ in enumerate(("a", "b", "c")):
                vo.wait_until(mk_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def act(self):
        smap = series_map(current=PART, done=PART - 1)
        with self.voiceover(
            "Where this sits. Parts thirty-five to thirty-eight built the dealer, the book, the executor and the market "
            "maker. This part finds each of them again in crypto, and closes Act six before Act seven turns to the "
            "system as a whole: risk, leverage and crises."
        ):
            self.play(FadeIn(smap))
            self.wait(1.0)
        self.clear_scene()

    def history(self):
        I = QC.IDEA
        entries = [(2008, r"Bitcoin's paper", I), (2014, r"Mt.\ Gox fails", I), (2015, r"Ethereum", I),
                   (2016, r"the perpetual", I), (2018, r"Uniswap", I), (2020, r"DeFi summer; MEV", I),
                   (2021, r"concentrated liquidity", I), (2022, r"Terra, FTX, the Merge", I), (2023, r"USDC and SVB", I),
                   (2024, r"spot ETFs", I), (2025, r"GENIUS Act; v4", I)]
        strip = era_strip(entries, y0=2006, y1=2027, font_size=12, step=5).move_to(DOWN * 0.3)
        head = label(r"Seventeen years of crypto markets", font_size=34).to_edge(UP, buff=0.6)
        groups = [(0, 4), (4, 7), (7, 11)]
        with self.voiceover(
            "Seventeen years. Satoshi Nakamoto's paper in twenty oh eight; the collapse of the Mt. Gox exchange in twenty "
            "fourteen; Ethereum in twenty fifteen; and BitMEX's perpetual in twenty sixteen. <bookmark mark='a'/> Then "
            "Uniswap's first pools, the decentralised-finance summer of twenty twenty, when MEV was named, and "
            "concentrated liquidity. <bookmark mark='b'/> And the crises and the institutions: Terra, FTX and Ethereum's "
            "move to proof of stake in twenty twenty-two; USD coin's depeg; spot ETFs; and America's stablecoin law."
        ) as vo:
            self.play(FadeIn(head), Create(strip[0]), FadeIn(strip[1]))
            for (a, b), mk_ in zip(groups, [None, "a", "b"]):
                if mk_:
                    vo.wait_until(mk_)
                self.play(LaggedStart(*[FadeIn(strip.items[i], shift=UP * 0.1) for i in range(a, b)], lag_ratio=0.3),
                          run_time=1.6)
        self.wait(0.4)
        self.clear_scene()

    def objectives(self):
        card = objectives_card([
            r"Blockchains, two kinds of venue, custody and FTX",
            r"Automated market makers, impermanent loss and loss-versus-rebalancing",
            r"Concentrated liquidity, and a learned liquidity provider",
            r"Ordering and MEV: the sandwich, worked",
            r"Perpetuals and funding; the cash-and-carry book, registered and opened",
            r"Stablecoins and runs: USDC in 2023, Terra in 2022",
            r"For the researcher: LVR and arbitrage with fees, proved and tested",
        ], color=QC.IDEA)
        with self.voiceover(
            "The plan: blockchains, venues and custody; pools and what they lose; concentrated liquidity and a learned "
            "provider; ordering and MEV; perpetuals, funding and a registered carry book; stablecoins and runs; and the "
            "theory of loss-versus-rebalancing, proved and tested on real prices."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in card.rows],
                                                     lag_ratio=0.5, run_time=12))
        self.play(FadeOut(card))

    def house(self):
        chart = house_chart(PART, lit=("digital",))
        with self.voiceover(
            "In the House, a digital-assets desk opens, the last of the trading desks. Its first task is to learn which "
            "of its risks its returns will never show."
        ):
            self.play(FadeIn(chart))
        self.wait(0.3)
        self.clear_scene()
