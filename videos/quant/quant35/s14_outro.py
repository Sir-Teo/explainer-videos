from __future__ import annotations

import math

from explainer.quant import *  # noqa: F403
from explainer.quant.house import micro as M
from videos.quant.quant35.common import (BAD, DEALER_C, FLOW_C, GOOD, INF_C, PART, PRICE_C, comma, load)

DESK = [
    (r"Why is there a spread when dealers are competitive and risk-neutral?",
     r"adverse selection: the ask is $\mathbb E[V \mid \text{buy}]$; from an even prior the spread equals the share of "
     r"informed traders (Glosten and Milgrom)"),
    (r"What is Kyle's lambda, and what sets it?",
     r"the price impact of a unit of net order flow: $\sigma_v/(2\sigma_u)$ in one auction, rising with what is unknown "
     r"and falling with noise"),
    (r"Why does a dealer shade its quotes when it holds inventory?",
     r"to make the next trades unwind it; without shading, inventory is a random walk and ruins the dealer"),
    (r"When does Roll's spread estimator fail?",
     r"when the true bounce is tiny next to volatility and any reversal: daily data on liquid funds"),
    (r"What does VPIN measure?",
     r"order imbalance by bulk classification, which rises with volatility by construction; on Bitcoin it barely tracks "
     r"the true imbalance"),
    (r"What made the flash crash possible?",
     r"a volume-targeted sell program, intermediaries passing inventory among themselves, and liquidity that withdrew "
     r"when inventory risk spiked"),
]

PROBLEMS = [
    r"A dealer with 40 units shades its mid by 0.05 a unit: its quotes, for a spread of 1.",
    r"Glosten--Milgrom with $\mu = 0.4$, $p = 0.5$: the quotes after one buy.",
    r"Kyle, one auction: noise variance doubles. The new $\lambda$, insider order and profit.",
    r"Roll: an autocovariance of $-0.0004$ in dollars squared. The spread.",
    r"$\lambda = 4.6$ bp per \$1m, linear: the cost of buying \$10m in a minute; why less in practice.",
    r"Bulk classification: a $+2\sigma$ bar with 1{,}000 BTC. The buy and sell split.",
    r"Information shares: market A closes 90\% of the basis, market B 10\%. Which leads?",
    r"A \$20 stock: one-cent spread, natural spread a third of a cent, 0.2-cent rebate. The taker's cost.",
    r"News on 2\% of trades, each moving the value 3 ticks: the minimum sniping component of the spread.",
    r"A seller of 5\% of daily volume at 9\% participation; volume doubles from its own selling. The time taken.",
    r"(qual) In continuous Kyle, verify that $J(t,p) = [(v-p)^2 + \lambda^2\sigma_u^2(1-t)]/(2\lambda)$ solves the "
    r"HJB equation for every trading rate, and derive $\lambda = \sigma_v/\sigma_u$ and $\mathbb E\pi = \sigma_v\sigma_u$.",
    r"(qual) Derive Kyle's one-auction equilibrium, show the insider's profit equals the noise traders' loss, and show "
    r"that for horizon $T$ the continuous equilibrium has $\lambda = \sigma_v/(\sigma_u\sqrt T)$ and profit "
    r"$\sigma_v\sigma_u\sqrt T$.",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.recap(load("dealer"), load("gm"), load("kyle"), load("flow"), load("measures"), load("vpin"),
                   load("discovery"))
        self.desk()
        self.answers()
        self.problems()
        self.payoffs()
        self.references()
        self.house()

    def _rows(self, items, title):
        rows = VGroup()
        for j, (t, col) in items:
            rows.add(VGroup(MathTex(str(j), font_size=24, color=col), label(t, font_size=21)).arrange(RIGHT, buff=0.3))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        head = label(title, font_size=36).to_edge(UP, buff=0.3)
        rows.next_to(head, DOWN, buff=0.35)
        if rows.width > 13.0:
            rows.scale_to_fit_width(13.0)
        if rows.height > 6.4:
            rows.scale_to_fit_height(6.4)
        return head, rows

    def recap(self, dl, g, k, f, m, v, d):
        items = [
            (r"a dealer's inventory is a random walk unless it shades its quotes (Garman; Ho and Stoll)", DEALER_C),
            (r"the spread is insurance against the informed: ask $= \mathbb E[V \mid$ buy$]$", PRICE_C),
            (r"Kyle: $\lambda = \sigma_v/(2\sigma_u)$; half the information revealed in one auction", INF_C),
            (r"Roll and Corwin--Schultz fail on liquid funds; Amihud ranks liquidity", BAD),
            (rf"Bitcoin: $\lambda$ = {f['full']['lambda']:.1f} bp per \$1m, concave; $R^2$ {f['agg']['1']['r2']:.2f} to "
             rf"{f['agg']['60']['r2']:.2f}", FLOW_C),
            (rf"VPIN: correlation {v['corr_rv']:.2f} with volatility, {v['corr_true']:.2f} with true imbalance", INF_C),
            (rf"price discovery: one-minute bars cannot separate spot and perpetual (correlation {d['corr0']:.3f})", GOOD),
        ]
        items2 = [
            (r"Reg NMS, the NBBO, maker--taker, dark pools, wholesalers", PRICE_C),
            (r"the 2024 tick and fee amendments; T+1 from May 2024", PRICE_C),
            (r"high-frequency market makers: narrower spreads, faster discovery, sniping", DEALER_C),
            (r"6 May 2010 and 15 October 2014: liquidity withdrawn", BAD),
            (r"frequent batch auctions: compete on price, not speed", GOOD),
            (r"Rule 35: know who is on the other side", QC.HOUSE),
            (r"research: continuous Kyle, $\lambda = \sigma_v/\sigma_u$, profit $\sigma_v\sigma_u$, a Brownian bridge",
             INF_C),
        ]
        head, rows = self._rows(list(enumerate(items, 1)), r"Part 35 in fourteen lines")
        with self.voiceover(
            "Part thirty-five in fourteen lines. A dealer must shade its quotes or be ruined by its own inventory. The "
            "spread is insurance against informed traders. Kyle's insider trades half as hard as it could, and lambda is "
            "the price of flow. Daily spread estimators fail on liquid funds, while Amihud's ratio works. On Bitcoin the "
            "price of flow is measurable and concave. A famous toxicity measure is mostly volatility. And one-minute "
            "bars are too coarse to find where Bitcoin's price is discovered."
        ):
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows], lag_ratio=0.6,
                                                run_time=20))
        self.wait(0.5)
        self.clear_scene()
        head, rows = self._rows(list(enumerate(items2, 8)), r"Part 35 in fourteen lines")
        with self.voiceover(
            "American markets are one market assembled from many by rules, and the rules keep changing. High-frequency "
            "traders are today's dealers, and today's snipers. Liquidity vanished twice in minutes. Batch auctions would "
            "make traders compete on price rather than speed. And the research chapter proved that a continuous insider "
            "reveals everything and earns twice as much."
        ):
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows], lag_ratio=0.6,
                                                run_time=16))
        self.wait(0.5)
        self.clear_scene()

    def desk(self):
        def page(qs):
            cards = VGroup(*[desk_question(q_, a_, width=12.4, font_size=20) for q_, a_ in qs]).arrange(DOWN, buff=0.22)
            if cards.height > 7.4:
                cards.scale_to_fit_height(7.4)
            return cards
        cards = page(DESK[:3])
        with self.voiceover(
            "Six desk questions. Why is there a spread when dealers are competitive and risk-neutral? Adverse selection. "
            "<bookmark mark='a'/> What is Kyle's lambda? The price of a unit of flow. <bookmark mark='b'/> Why does a "
            "dealer shade its quotes? To unwind its inventory."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[2], shift=UP * 0.2))
        self.wait(0.5)
        self.clear_scene()
        cards = page(DESK[3:])
        with self.voiceover(
            "When does Roll's estimator fail? When the bounce is tiny. <bookmark mark='a'/> What does VPIN measure? "
            "Mostly volatility. <bookmark mark='b'/> And what made the flash crash possible? Liquidity that withdrew. "
            "Full solutions are in the notes."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[2], shift=UP * 0.2))
        self.wait(0.5)
        self.clear_scene()

    def answers(self):
        a1, b1 = M.gm_quotes(0.7, 0.4)
        roll = 2 * math.sqrt(0.0004)
        from scipy.stats import norm
        buy = 1000 * norm.cdf(2.0)
        pages = [
            [(r"Ch.~1: 40 units, shade 0.05", r"mid 2 below value: bid at $-2.5$, ask at $-1.5$; the dealer sells cheaply"),
             (r"Ch.~2: $\mu = 0.4$, a buy", rf"belief 0.7; bid {b1:.3f}, ask {a1:.3f}"),
             (r"Ch.~3: noise doubles", r"$\lambda$ falls by $\sqrt2$, the order rises by $\sqrt2$, the profit by $\sqrt2$")],
            [(r"Ch.~4: autocovariance $-0.0004$", rf"spread $2\sqrt{{0.0004}} = \${roll:.2f}$; trust it when the bounce "
              r"dominates daily noise"),
             (r"Ch.~5: \$10m in a minute", r"46 bp on the line; less, by concavity, for one large order; more per dollar "
              r"for small ones"),
             (r"Ch.~6: a $+2\sigma$ bar", rf"about {buy:.0f} BTC bought and {1000 - buy:.0f} sold; an even true split "
              r"is invisible to it")],
            [(r"Ch.~7: closes 90\% against 10\%", r"B, the market that hardly adjusts, leads, with a share near 0.9"),
             (r"Ch.~8 and Ch.~9", r"a taker pays half a cent plus a fee about the size of the rebate, three times the natural "
              r"half-spread; a half-cent tick helps takers; the sniping spread is 0.12 ticks"),
             (r"Ch.~10 and research", r"twice the volume halves the time; $\lambda = 2$, price volatility 2, profit 2; over "
              r"four years $\lambda = 1$ and profit 4")],
        ]

        def show(page):
            cards = VGroup(*[desk_question(q_, a_, width=12.4, font_size=19) for q_, a_ in page]).arrange(DOWN, buff=0.22)
            if cards.height > 7.2:
                cards.scale_to_fit_height(7.2)
            return cards

        cards = show(pages[0])
        with self.voiceover(
            "The pause questions, answered. A dealer holding forty units quotes two below value in the middle: it sells "
            f"cheaply to unload. <bookmark mark='a'/> After one buy with four in ten informed, the bid is {b1:.2f} and "
            f"the ask {a1:.2f}. <bookmark mark='b'/> And when noise doubles, lambda falls and the insider's order and "
            "profit rise, each by the root of two."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            for k_, mk in enumerate(("a", "b")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k_ + 1], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()
        cards = show(pages[1])
        with self.voiceover(
            f"Roll's spread is {roll:.2f} dollars, trustworthy only when the bounce dominates. <bookmark mark='a'/> Ten "
            "million dollars in a minute is forty-six basis points on a straight line, less in practice. "
            f"<bookmark mark='b'/> And a two-sigma bar is split about {buy:.0f} to {1000 - buy:.0f}, whatever the true "
            "split was."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            for k_, mk in enumerate(("a", "b")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k_ + 1], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()
        cards = show(pages[2])
        with self.voiceover(
            "The market that hardly adjusts leads. <bookmark mark='a'/> A half-cent tick helps takers, and the sniping "
            "spread is twelve hundredths of a tick. <bookmark mark='b'/> Twice the volume halves the time. And in "
            "continuous Kyle with sigma v of two, lambda, the price's volatility and the profit are all two; over four "
            "years, lambda halves and the profit doubles."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            for k_, mk in enumerate(("a", "b")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k_ + 1], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=18)
        with self.voiceover(
            "And twelve problems: a shaded dealer; Glosten and Milgrom after a buy; Kyle with more noise; Roll; lambda's "
            "cost; bulk classification; information shares; the true cost under maker-taker; the sniping spread; a "
            "volume-targeted seller. Then two qualifying-exam problems: continuous Kyle by the value function, and the "
            "one-auction equilibrium with its horizon scaling. Solutions, in English and Chinese, are in the notes."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r_) for r_ in ps.rows], lag_ratio=0.3, run_time=5))
            self.wait(3)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"the limit order book: queues, ticks and fill probabilities", [36]),
            (r"execution: slicing a Kyle insider's order, optimally", [37]),
            (r"market making: the dealer, with inventory and adverse selection together", [38]),
            (r"digital-asset markets: venues, perpetuals and funding", [39]),
        ])
        with self.voiceover(
            "Where this comes back. Part thirty-six opens the limit order book. Part thirty-seven slices an order the way "
            "Kyle's insider does, optimally. Part thirty-eight is the dealer again, with inventory and adverse selection "
            "together. And Part thirty-nine is the market Bitcoin trades in."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r_) for r_ in card.rows], lag_ratio=0.4, run_time=4))
        self.wait(0.4)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"O'Hara, \textit{Market Microstructure Theory} (1995); Hasbrouck, \textit{Empirical Market Microstructure} "
             r"(2007); Foucault, Pagano and R\"oell, \textit{Market Liquidity} (2013); Harris, \textit{Trading and "
             r"Exchanges} (2003)"],
            [r"Garman (1976); Ho and Stoll (1981); Roll (1984); Kyle (1985); Glosten and Milgrom (1985); Back (1992); "
             r"Holden and Subrahmanyam (1992); Hasbrouck (1995); Easley et al.\ (1996); Amihud (2002); Back and Baruch "
             r"(2004); Hendershott, Jones and Menkveld (2011); Corwin and Schultz (2012); Easley, Lopez de Prado and O'Hara "
             r"(2012); Menkveld (2013)",
             r"Andersen and Bondarenko (2014); Brogaard, Hendershott and Riordan (2014); Budish, Cramton and Shim (2015); "
             r"Kirilenko, Kyle, Samadi and Tuzun (2017); the CFTC--SEC report (2010); the joint staff report on 15 October "
             r"2014 (2015). Data: Binance's public archive; Yahoo Finance"])
        with self.voiceover(
            "The textbooks this part follows, and the papers it draws on, from Garman in 1976 to the flash-crash studies. "
            "Every number on screen was computed by the House's code from Binance's public archive, Yahoo Finance's bars "
            "and simulation, with illustrations labelled as such."
        ):
            self.play(FadeIn(card))
            self.wait(3)
        self.clear_scene()

    def house(self):
        chart = house_chart(PART, lit=("compliance", "data"))
        smap = series_map(current=PART + 1, done=PART)
        nxt = label(r"Next: Part 36, The Limit Order Book", font_size=30, color=QC.IDEA).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The House now knows who is on the other side of its trades: dealers protecting their inventory, informed "
            "traders hiding in noise, and other algorithms reading its orders. <bookmark mark='a'/> Next, Part "
            "thirty-six: the limit order book. The queue, the tick, and the probability that a resting order is filled "
            "before the price moves away."
        ) as vo:
            self.play(FadeIn(chart))
            vo.wait_until("a")
            self.play(FadeOut(chart), FadeIn(smap), FadeIn(nxt))
        self.wait(1.0)
        self.clear_scene()
