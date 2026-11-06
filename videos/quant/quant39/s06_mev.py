from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant39.common import (
    ARB_C,
    BAD,
    GOOD,
    HURDLE,
    PART,
    POOL_C,
    SPOT_C,
    comma,
    load,
)


class MEV(VoiceoverScene):
    def construct(self):
        m = load("mev")
        self.card(m)
        self.pipeline()
        self.sandwich_steps(m)
        self.limit()
        self.table(m)
        self.kinds()
        self.lvr_is_mev()
        self.defences()
        self.question()

    def _row(self, m, size, slip):
        return [r for r in m["rows"] if abs(r["size"] - size) < 1 and abs(r["slip"] - slip) < 1e-9][0]

    def card(self, m):
        r = self._row(m, 100_000.0, 0.01)
        c = chapter_card(5, r"Order is worth money", r"Who decides the order of trades, and what is it worth?", part=PART)
        with self.voiceover(
            f"Chapter five, and the answer to the pause: about {r['profit']:,.0f} dollars for the attacker, while the "
            f"trader receives about {r['victim_loss']:,.0f} dollars less ether than quoted; the difference goes to the "
            "pool as fees. On a public ledger, whoever orders the transactions can trade around them."
        ):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def pipeline(self):
        steps = [(r"user", r"signs a swap"), (r"mempool", r"public, waiting"), (r"searchers", r"bundle trades around it"),
                 (r"builders", r"assemble a block, bid for it"), (r"proposer", r"takes the highest bid")]
        boxes = VGroup()
        for nm, what in steps:
            b = RoundedRectangle(width=2.2, height=1.2, corner_radius=0.12, stroke_color=POOL_C, stroke_width=2,
                                 fill_color=POOL_C, fill_opacity=0.08)
            t = VGroup(label(nm, font_size=20, color=POOL_C), label(what, font_size=14, color=GREY_A)).arrange(DOWN, buff=0.1)
            boxes.add(VGroup(b, t.move_to(b)))
        boxes.arrange(RIGHT, buff=0.35).move_to(UP * 0.8)
        arrows = VGroup(*[Arrow(boxes[i].get_right(), boxes[i + 1].get_left(), buff=0.04, stroke_width=3, color=GREY_B,
                                tip_length=0.14) for i in range(4)])
        notes = VGroup(why(r"since 2022 most Ethereum blocks are built this way, through Flashbots' MEV-Boost relay and "
                           r"its successors, as reported: proposer-builder separation"),
                       why(r"maximal extractable value (MEV): what can be earned by choosing which transactions go in a "
                           r"block, and in what order")).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "How a trade reaches the ledger. <bookmark mark='a'/> A user signs a swap; it waits in a public pool of "
            "pending transactions; searchers write bundles of trades around it; builders assemble whole blocks and bid "
            "for the right to have them included; the proposer takes the highest bid. <bookmark mark='b'/> Since twenty "
            "twenty-two most Ethereum blocks have been built this way, as reported. <bookmark mark='c'/> The value of "
            "choosing what goes in a block, and in what order, is called maximal extractable value."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(b_) for b_ in boxes], lag_ratio=0.2), run_time=2)
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowArrow(a_) for a_ in arrows], lag_ratio=0.2))
            vo.wait_until("b")
            self.play(FadeIn(notes[0]))
            vo.wait_until("c")
            self.play(FadeIn(notes[1]))
        self.wait(0.4)
        self.clear_scene()

    def sandwich_steps(self, m):
        x0, y0 = m["x"] / 1000, m["y"] / 1e6
        k = x0 * y0
        g = axes([3.5, 5.5], [1.8, 2.9], x_length=6.4, y_length=4.4, xlabel=r"ETH in the pool, thousands",
                 ylabel=r"USDC in the pool, millions", xticks=[4, 5], yticks=[2.0, 2.5], font_size=16)
        # zoom the curve: plot y in units of 10^7 / 4 so the steps are visible
        g.move_to(LEFT * 2.6 + DOWN * 0.2)
        ax = g.ax
        sc = 1 / 4.0                                # 10m USDC shown as 2.5
        xs = np.linspace(3.6, 5.4, 120)
        hyp = curve(ax, xs, sc * k / xs, POOL_C, stroke_width=3)
        r = self._row(m, 1_000_000.0, 0.01)        # a large victim, so the steps can be seen
        a = r["front"] / 1e6
        v = 1.0
        f = 0.003

        def buy(xx, yy, dy):
            y1 = yy + (1 - f) * dy
            return k / y1, y1
        x1, y1 = buy(x0, y0, a)
        x2, y2 = buy(x1, y1, v)
        got = x1 - (k / (y1 + 0))                  # attacker's ether, for the back-run (approximately the step size)
        pts = [(x0, y0), (x1, y1), (x2, y2)]
        dots = [Dot(ax.c2p(px, sc * py), radius=0.09, color=c) for (px, py), c in zip(pts, (SPOT_C, BAD, ARB_C))]
        labs = VGroup(label(r"1. attacker buys first", font_size=19, color=BAD),
                      label(r"2. victim buys at a worse price, within its limit", font_size=19, color=ARB_C),
                      label(r"3. attacker sells back at the higher price", font_size=19, color=GOOD))
        labs.arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.3).shift(UP * 1.0)
        del got
        with self.voiceover(
            "A sandwich, step by step, for a million-dollar purchase with one percent of slippage allowed. "
            "<bookmark mark='a'/> The attacker buys ether first, moving the pool up the curve. <bookmark mark='b'/> The "
            "victim's purchase executes next, at a worse price, but just within its limit, so it does not fail. "
            "<bookmark mark='c'/> Then the attacker sells its ether back into the pool at the higher price the victim "
            f"created. Profit: about {r['profit']:,.0f} dollars, from a victim who received about "
            f"{r['victim_loss']:,.0f} dollars less than quoted."
        ) as vo:
            self.play(FadeIn(g), Create(hyp), FadeIn(dots[0]))
            vo.wait_until("a")
            self.play(FadeIn(dots[1]), FadeIn(labs[0]))
            vo.wait_until("b")
            self.play(FadeIn(dots[2]), FadeIn(labs[1]))
            vo.wait_until("c")
            self.play(FadeIn(labs[2]), Indicate(dots[1], color=GOOD))
        self.wait(0.4)
        self.clear_scene()

    def limit(self):
        rows = [cmath(r"\text{victim receives}", r"\ge", r"(1 - s) \times \text{quote}", font_size=38),
                cmath(r"\text{front-run}", r"=", r"\max\{a : \text{victim still} \ge (1 - s)\,\text{quote}\}", font_size=34,
                      colors={r"\text{front-run}": BAD}),
                cmath(r"\text{profit}", r"\approx", r"s \times \text{size} - \text{fees on two legs}", font_size=38,
                      colors={r"\text{profit}": GOOD})]
        whys = [why(r"every swap on a pool names a minimum it will accept, a slippage tolerance $s$"),
                why(r"the attacker front-runs by exactly as much as keeps the victim inside its limit: the House's "
                    r"\texttt{sandwich} solves for it by bisection"),
                why(r"roughly the tolerance times the trade, minus the pool's fee on both of the attacker's legs, so "
                    r"small trades are not worth attacking")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.6, edge=6.9)
        with self.voiceover(
            "What limits it. <bookmark mark='a'/> Every swap names the least it will accept: a slippage tolerance. "
            "<bookmark mark='b'/> The attacker front-runs by exactly as much as keeps the victim just inside it. "
            "<bookmark mark='c'/> So the take is roughly the tolerance times the trade, minus the pool's fee on both of "
            "the attacker's legs. The victim's own setting is the size of the prize."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def table(self, m):
        sizes = (10_000.0, 100_000.0, 1_000_000.0)
        slips = (0.001, 0.005, 0.01, 0.03)
        hx = [-4.4, -1.8, 0.8, 3.4, 5.8]
        head = VGroup(label(r"trade, slippage allowed", font_size=15, color=GREY_B),
                      *[label(rf"{100 * s_:g}\%", font_size=18, color=GREY_B) for s_ in slips])
        tab = VGroup(head)
        for sz in sizes:
            cells = [label(rf"\${comma(sz)}", font_size=18)]
            for s_ in slips:
                r = self._row(m, sz, s_)
                p = r["profit"]
                cells.append(MathTex(rf"{comma(p)}" if p > 0 else r"\text{none}", font_size=26,
                                     color=GOOD if p > 0 else GREY_D))
            tab.add(VGroup(*cells))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 1.6 - 0.9 * j, 0])
        foot = wrapped_label(r"the attacker's profit in dollars, in Chapter 2's pool (5,000 ETH, \$10m, 0.3\% fee); "
                             r"``none'' means the fees exceed the gain, so no sandwich is worth making", 11.4, 16,
                             GREY_A).to_edge(DOWN, buff=0.6)
        r3 = self._row(m, 1_000_000.0, 0.03)
        r1 = self._row(m, 100_000.0, 0.01)
        with self.voiceover(
            "The prize, in Chapter two's pool. <bookmark mark='a'/> A ten-thousand-dollar trade is safe at any tolerance "
            "here: the fees on the attacker's two legs exceed what it could take. <bookmark mark='b'/> A hundred "
            "thousand dollars at one percent gives about "
            f"{r1['profit']:,.0f}; <bookmark mark='c'/> a million at three percent, about "
            f"{r3['profit']:,.0f}. The profit is nearly proportional to tolerance times size, and the fee sets the "
            "threshold below which no one bothers."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(foot))
            vo.wait_until("a")
            self.play(FadeIn(tab[1]))
            vo.wait_until("b")
            self.play(FadeIn(tab[2]))
            vo.wait_until("c")
            self.play(FadeIn(tab[3]))
        self.wait(0.4)
        self.clear_scene()

    def kinds(self):
        cards = VGroup(
            desk_question(r"arbitrage", r"between pools, and between pools and centralised exchanges: the largest "
                          r"kind, as studies of on-chain data reported", width=12.4, font_size=19),
            desk_question(r"liquidations", r"lending protocols pay a bonus to whoever repays an under-collateralised loan "
                          r"first; the race for it is an ordering race", width=12.4, font_size=19),
            desk_question(r"sandwiches and just-in-time liquidity", r"trading around someone else's swap: a pure transfer "
                          r"from the user", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        head = label(r"Three kinds of extractable value (Daian et al., Flash Boys 2.0, 2020)", font_size=28).to_edge(UP, buff=0.4)
        if cards.height > 6.0:
            cards.scale_to_fit_height(6.0)
        cards.next_to(head, DOWN, buff=0.3)
        with self.voiceover(
            "Three kinds of extractable value, first catalogued by Philip Daian and coauthors in Flash Boys two point "
            "oh, in twenty twenty. <bookmark mark='a'/> Arbitrage, between pools and against centralised exchanges, the "
            "largest kind, as studies of on-chain data reported. <bookmark mark='b'/> Liquidations: "
            "lending protocols pay a bonus to whoever first repays an under-collateralised loan, and the race for it is a "
            "race for position in the block. <bookmark mark='c'/> And sandwiches and just-in-time liquidity: trading "
            "around another user's swap, a pure transfer from that user."
        ) as vo:
            self.play(FadeIn(head))
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def lvr_is_mev(self):
        rows = [cmath(r"\text{LVR}", r"=", r"\text{arbitrage profit} + \text{fees on arbitrage}", font_size=38,
                      colors={r"\text{LVR}": ARB_C}),
                cmath(r"\text{arbitrage profit}", r"\to", r"\text{searchers} \to \text{builders} \to \text{proposers}",
                      font_size=34),
                cmath(r"\text{competition}", r"\Rightarrow", r"\text{most of it is bid away}", font_size=36,
                      colors={r"\text{competition}": HURDLE})]
        whys = [why(r"Chapter 3's loss is the largest source of extractable value: every stale pool price is a trade"),
                why(r"searchers compete to include it, builders compete to include them, and the proposer sells the block"),
                why(r"so the providers' loss ends up largely with whoever controls the block, as Part 38's sniping rents "
                    r"went to the venue that sold speed")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.6, edge=6.9)
        with self.voiceover(
            "Chapter three's loss, seen from the block. <bookmark mark='a'/> LVR is arbitrage profit plus the fees on "
            "arbitrage trades: the largest source of extractable value. <bookmark mark='b'/> Searchers compete to capture "
            "it, builders compete for searchers, and the proposer sells the block. <bookmark mark='c'/> With enough "
            "competition, most of it is bid away to whoever controls the block, as Part thirty-eight's sniping rents "
            "went to the venues that sold speed."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def defences(self):
        cards = VGroup(
            desk_question(r"tight limits and private routes", r"a low slippage tolerance shrinks the prize; sending the "
                          r"swap straight to a builder keeps it out of the public mempool", width=12.4, font_size=19),
            desk_question(r"batch auctions", r"CoW Swap clears orders in batches at one price, so order within a batch "
                          r"does not matter: Part 38's remedy, on chain", width=12.4, font_size=19),
            desk_question(r"pools that sell their own arbitrage", r"auctioning the right to make the first trade of each "
                          r"block, or raising fees with volatility, returns part of LVR to providers", width=12.4,
                          font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Defences. <bookmark mark='a'/> Tight slippage limits shrink the prize, and private routes to builders keep "
            "a swap out of the public mempool. <bookmark mark='b'/> Batch auctions, such as CoW Swap's, clear orders at "
            "one price, so order inside a batch does not matter: Part thirty-eight's remedy, on chain. "
            "<bookmark mark='c'/> And pools that sell the right to make each block's first trade, or raise their fees "
            "with volatility, can return part of the loss to their providers."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"a perpetual future never expires, so nothing forces its price to converge to spot. What keeps "
                       r"Bitcoin's perpetual within a few basis points of spot, and who pays for it?")
        with self.voiceover(
            "Pause and predict. A perpetual future never expires, so nothing forces its price to meet spot at a date. "
            "What keeps Bitcoin's perpetual within a few basis points of spot, and who pays for it?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
