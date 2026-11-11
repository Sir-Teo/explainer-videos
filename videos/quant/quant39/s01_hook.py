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
        self.claims(load("lvr"), load("fees"))
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
        self.add(rows[0])
        with self.voiceover(
            "A desk question. <bookmark mark='a'/> Supply equal initial values of ether and dollars to a fee-free constant-product pool, continuously arbitraged to an external price. <bookmark mark='b'/> The ether price doubles. <bookmark mark='c'/> Relative to holding the initial assets, the pool is about five point seven percent behind. That is a valid endpoint comparison. Loss-versus-rebalancing answers a different question: how much value the pool loses against a self-financing portfolio that follows its token holdings at external market prices."
        ) as vo:
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.wait(0.4)
        self.clear_scene()

    def claims(self, lv, fe):
        f3 = next(x for x in fe["eth"] if abs(x["fee"] - 0.003) < 1e-9)
        cards = VGroup(
            desk_question(r"a sum of local loss fractions", rf"ETH 2023 minute grid: exact sum {lv['lvr_pct']:.2f}\%; squared log increments / 8: {lv['rv8_pct']:.2f}\%; changing pool-value denominators", width=12.4, font_size=19),
            desk_question(r"a descriptive simulator comparison", rf"at 0.3\% fee, arb profit / fee-free discrete LVR = {f3['arb_lvr']:.2f}; compare a leading-order Poisson/log-Brownian benchmark, without identifying a tail mechanism", width=12.4, font_size=19),
            desk_question(r"carry has a cash-flow ledger", r"funding plus changes in the spot-perpetual basis, less costs; chosen margin and venue stresses, without historical strategy outcomes", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(f"Three questions organize the part. <bookmark mark='a'/> On ether's twenty twenty-three minute grid, the sum of exact losses divided by each step's starting pool value is {lv['lvr_pct']:.2f} percent; squared log increments over eight give {lv['rv8_pct']:.2f}. These are local normalized sums, not a return on fixed initial capital. <bookmark mark='b'/> With a fee, the simulator reports arbitrage profit relative to fee-free discrete LVR. Its real-price comparison is descriptive, without proving that fat tails caused a discrepancy from a Brownian approximation. <bookmark mark='c'/> Finally, carry has a funding and basis ledger, but margin, custody and venue stresses survive a price hedge. We use chosen accounting examples, without historical carry strategy results.") as vo:
            self.play(FadeIn(cards[0]))
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            self.play(FadeIn(cards[1]))
            vo.wait_until("c")
            self.play(FadeIn(cards[2]))
        self.wait(0.4)
        self.clear_scene()

    def stakes(self):
        cards = VGroup(
            desk_question('linked markets and instruments', 'spot tokens, leveraged contracts, stablecoins and investment funds connect prices, collateral and redemption risks', width=12.4,
                          font_size=19),
            desk_question(r"a laboratory", 'public-chain transactions and contract state are observable; private orders, off-chain quotes and economic identities may remain hidden', width=12.4, font_size=19),
            desk_question(r"why the House cares", 'a proposed digital-assets research desk must connect market risk with custody, collateral, contracts and redemption access', width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        self.add(cards[0])
        with self.voiceover(
            "Why it matters. <bookmark mark='a'/> Crypto links spot tokens, leveraged contracts, stablecoins and investment funds, so failures can cross instruments and venues. <bookmark mark='b'/> Public blockchains expose transactions and contract state, but private order flow, off-chain exchange quotes and economic identities can remain hidden. This is a useful laboratory with incomplete observations. <bookmark mark='c'/> The House's proposed desk needs to connect market risk with custody, smart contracts, collateral and redemption access. A public ledger does not make all of those risks observable or remove intermediaries."
        ) as vo:
            for k, mk_ in enumerate(("a", "b", "c")):
                vo.wait_until(mk_)
                if k:
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
                   (2016, r"the perpetual", I), (2018, r"Uniswap", I), (2020, r"DeFi summer", I),
                   (2021, r"concentrated liquidity", I), (2022, r"Terra, FTX, the Merge", I), (2023, r"USDC and SVB", I),
                   (2024, r"spot ETFs", I), (2025, r"GENIUS Act; v4", I)]
        strip = era_strip(entries, y0=2006, y1=2027, font_size=12, step=5).move_to(DOWN * 0.3)
        head = label(r"Seventeen years of crypto markets", font_size=34).to_edge(UP, buff=0.6)
        groups = [(0, 4), (4, 7), (7, 11)]
        with self.voiceover(
            "A selected timeline through twenty twenty-five. Nakamoto's Bitcoin paper appeared in twenty oh eight; Mt. Gox failed in twenty fourteen; Ethereum launched in twenty fifteen; BitMEX introduced its perpetual in twenty sixteen. <bookmark mark='a'/> Uniswap launched in twenty eighteen. Flash Boys two point oh appeared as a preprint in twenty nineteen and at the security conference in twenty twenty, when decentralized finance expanded. Concentrated liquidity arrived in twenty twenty-one. <bookmark mark='b'/> Terra and FTX failed in twenty twenty-two, when Ethereum also moved to proof of stake. USD coin lost its peg during the Silicon Valley Bank failure in twenty twenty-three. American spot Bitcoin exchange-traded products were approved in January twenty twenty-four; the GENIUS Act became law in July twenty twenty-five. Dates describe selected historical events, not a current regulatory certification."
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
            r"Perpetuals and funding; carry accounting, collateral and venue stresses",
            r"Stablecoins and runs: USDC in 2023, Terra in 2022",
            r"For the researcher: LVR and arbitrage with fees, proved and tested",
        ], color=QC.IDEA)
        with self.voiceover(
            'The plan: blockchains, venues and custody; pools and two loss benchmarks; concentrated liquidity and a contextual-bandit simulation; ordering and transaction attacks; perpetual funding and carry accounting; stablecoin redemption and run mechanisms; then the assumptions and proof of loss-versus-rebalancing. We will distinguish exact accounting identities, continuous-price limits, simulated policies and descriptive market observations, because their evidence supports different conclusions.'
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
