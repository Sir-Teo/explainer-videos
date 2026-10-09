from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.trading.common import Ladder, Plot, fmt_int, label, load, mtex, note, person, real_tag, show_part, tagged


class TheJob(VoiceoverScene):
    def construct(self):
        show_part(self, 1, r"The game", r"what a market maker does, and what an exchange is")
        self.book()
        self.two_sides()
        self.adverse()
        self.consequence()

    # ------------------------------------------------------------------
    def book(self):
        b = load("book")
        s = b["snapshots"][0]
        assert s["clock"] == "10:30:00.000"
        bids, asks = s["bids"][:5], s["asks"][:5]
        bb, ba = bids[0][0], asks[0][0]
        assert (bb, ba) == (18385, 18386)
        lad = Ladder(bids, asks, row_h=0.42).shift(UP * 0.05)
        self.lad, self.bb, self.ba = lad, bb, ba
        ttl = label(r"Nvidia (NVDA) on Nasdaq at 10:30:00 a.m.", font_size=34).to_edge(UP, buff=0.3)
        tag = real_tag(r"real order book, rebuilt from the feed", corner=DR)
        bid_y = (lad.anchor("B", bids[0][0])[1] + lad.anchor("B", bids[-1][0])[1]) / 2
        ask_y = (lad.anchor("S", asks[0][0])[1] + lad.anchor("S", asks[-1][0])[1]) / 2
        bid_l = label(r"bids:\\waiting to buy", font_size=28, color=C.BID).move_to([-5.4, bid_y, 0])
        ask_l = label(r"asks: waiting to sell", font_size=28, color=C.ASK).next_to(lad.rows_bg, UP, buff=0.12).align_to(
            lad.rows_bg, RIGHT)
        n_orders = sum(len(q) for _, q in bids + asks)
        with self.voiceover(
            "This is what the market looks like to a trading machine. It's Nasdaq's order book for Nvidia, at 10:30 that "
            "morning, rebuilt from the exchange's own data feed. <bookmark mark='blk'/> Every block is one real order. "
            "Its width grows with the number of shares. <bookmark mark='b'/> Below the middle are bids: orders waiting "
            "to buy. <bookmark mark='a'/> Above are asks: orders waiting to sell. <bookmark mark='q'/> At each price "
            "the orders wait in a queue, and the queue is served first come, first served."
        ) as vo:
            self.play(FadeIn(ttl), FadeIn(tag))
            self.play(FadeIn(lad.rows_bg), FadeIn(lad.price_labels))
            vo.wait_until("blk")
            self.play(LaggedStart(*[FadeIn(g, shift=RIGHT * 0.1) for g in lad.blocks.values()], lag_ratio=0.05),
                      FadeIn(lad.totals), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(bid_l))
            vo.wait_until("a")
            self.play(FadeIn(ask_l))
            vo.wait_until("q")
            q = lad.blocks[("B", bb)]
            arrow = Arrow(q.get_left() + LEFT * 0.6, q.get_left() + LEFT * 0.05, buff=0, color=WHITE, stroke_width=3,
                          max_tip_length_to_length_ratio=0.3)
            front = label(r"front of the queue", font_size=22).next_to(lad.anchor("B", bb), UP, buff=0.05).shift(LEFT * 0.9)
            self.play(Indicate(q[0], color=WHITE), FadeIn(front))
            self.play(FadeOut(front))
        mid = (bb + ba) / 2 / 100
        spread_cents = b["tw_spread_cents"]
        assert abs(spread_cents - 1.108) < 0.01
        sp = VGroup(
            label(rf"best bid \${bb / 100:.2f} \quad best ask \${ba / 100:.2f}", font_size=28),
            label(r"spread: 1 cent, \enspace mid-price: \$" + f"{mid:.3f}", font_size=28, color=C.MID),
        ).arrange(DOWN, buff=0.1).to_corner(DL, buff=0.3)
        sp.add_background_rectangle(color=BACKGROUND, opacity=0.9, buff=0.1)
        day = note(rf"average spread over the day:\\{spread_cents:.2f} cents on a \$183 stock, about 0.6 basis points",
                   font_size=22, color=GREY_A).next_to(sp, UP, buff=0.1).align_to(sp, LEFT)
        brace = BraceBetweenPoints(lad.anchor("S", ba) + RIGHT * 0.05, lad.anchor("B", bb) + RIGHT * 0.05 + RIGHT * 1.5,
                                   direction=RIGHT, color=C.MID)
        with self.voiceover(
            "<bookmark mark='s'/> The best bid is 183.85 dollars, the best ask 183.86. The gap between them is the "
            "spread: one cent. Halfway between is the mid-price. <bookmark mark='d'/> Over the whole day Nvidia's "
            "spread on Nasdaq averaged 1.1 cents, on a 183-dollar stock. That's about six thousandths of a percent."
        ) as vo:
            vo.wait_until("s")
            self.play(FadeIn(sp))
            vo.wait_until("d")
            self.play(FadeIn(day))
        self.sp, self.day, self.bid_l, self.ask_l, self.ttl = sp, day, bid_l, ask_l, ttl

    # ------------------------------------------------------------------
    def two_sides(self):
        lad, bb, ba = self.lad, self.bb, self.ba
        a1, ours_b = lad.append_anim("B", bb, 100, color=C.OURS)
        a2, ours_a = lad.append_anim("S", ba, 100, color=C.OURS)
        mm = label(r"a market maker's quotes: buy 100 at the bid, sell 100 at the ask", font_size=26, color=C.OURS)
        mm.next_to(self.ttl, DOWN, buff=0.15)
        with self.voiceover(
            "A market maker's job is to always stand on both sides: <bookmark mark='q'/> willing to buy at the bid "
            "and to sell at the ask. Its orders join the back of the queues, like everyone else's. <bookmark "
            "mark='t'/> When a seller arrives, the bid queue is filled from the front, until it reaches us: we buy "
            "100 shares at 183.85. <bookmark mark='u'/> Later a buyer arrives and works through the ask queue: we sell "
            "100 shares at 183.86. <bookmark mark='p'/> Bought at 85, sold at 86. One cent per share, a dollar in "
            "total, for providing liquidity: for being there when someone wanted to trade."
        ) as vo:
            vo.wait_until("q")
            self.play(FadeOut(self.bid_l), FadeOut(self.ask_l), FadeIn(mm))
            self.play(a1, a2)
            vo.wait_until("t")
            n = len(lad.blocks[("B", bb)])
            seller = person(C.UNINFORMED).next_to(lad.anchor("B", bb), RIGHT, buff=2.4)
            sl = label(r"a seller", font_size=24, color=C.UNINFORMED).next_to(seller, DOWN, buff=0.1)
            self.play(FadeIn(seller), FadeIn(sl))
            for i in range(n - 1):
                self.play(lad.remove_anim("B", bb, 0, color=C.TRADE, run_time=0.25))
            self.play(Flash(ours_b, color=C.TRADE), ours_b.animate.set_fill(C.TRADE, 0.9))
            got = tagged(r"bought 100 @ 183.85", font_size=24, color=C.OURS).next_to(ours_b, LEFT, buff=0.25)
            self.play(FadeIn(got), FadeOut(ours_b))
            vo.wait_until("u")
            m = len(lad.blocks[("S", ba)])
            buyer = person(C.UNINFORMED).next_to(lad.anchor("S", ba), LEFT, buff=2.4)
            bl = label(r"a buyer", font_size=24, color=C.UNINFORMED).next_to(buyer, DOWN, buff=0.1)
            self.play(FadeOut(seller), FadeOut(sl), FadeIn(buyer), FadeIn(bl))
            for i in range(m - 1):
                self.play(lad.remove_anim("S", ba, 0, color=C.TRADE, run_time=0.25))
            self.play(Flash(ours_a, color=C.TRADE), ours_a.animate.set_fill(C.TRADE, 0.9))
            sold = tagged(r"sold 100 @ 183.86", font_size=24, color=C.OURS).next_to(ours_a, RIGHT, buff=0.25)
            self.play(FadeIn(sold), FadeOut(ours_a))
            vo.wait_until("p")
            pnl = VGroup(mtex(r"100 \times (\$183.86 - \$183.85) = +\$1.00", font_size=40, color=C.PNL_UP))
            pnl.move_to(RIGHT * 2.6 + DOWN * 2.75)
            pnl.add_background_rectangle(color=BACKGROUND, opacity=0.9, buff=0.12)
            self.play(FadeOut(buyer), FadeOut(bl), Write(pnl))
        self.wait(0.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def adverse(self):
        # a schematic price path: our quotes around the mid; uninformed flow vs one informed trade
        ch = Plot((0, 10), (183.80, 183.92), width=8.4, height=3.5, x_ticks=[], y_ticks=[183.82, 183.86, 183.90],
                  y_fmt=lambda v: f"{v:.2f}").move_to(LEFT * 2.2 + UP * 0.75)
        tl = label(r"time $\to$", font_size=24, color=GREY_B).next_to(ch.x_axis, DOWN, buff=0.15)
        mid_path = [(0, 183.855), (2.0, 183.855), (2.0, 183.855), (5.6, 183.855), (5.6, 183.895), (10, 183.895)]
        bid_l = ch.line([0, 5.6], [183.85, 183.85], C.OURS, 3)
        ask_l = ch.line([0, 5.6], [183.86, 183.86], C.OURS, 3)
        mid_l = ch.line([p[0] for p in mid_path], [p[1] for p in mid_path], C.MID, 3)
        qlab = VGroup(label(r"our ask", font_size=22, color=C.OURS).next_to(ch.c2p(0, 183.86), LEFT, buff=0.1),
                      label(r"our bid", font_size=22, color=C.OURS).next_to(ch.c2p(0, 183.85), LEFT, buff=0.1))
        qlab.shift(RIGHT * 1.2 + UP * 0.18)
        uninf = [(0.8, "S"), (1.5, "B"), (2.6, "B"), (3.3, "S"), (4.2, "S"), (4.9, "B")]
        dots_u = VGroup(*[Dot(ch.c2p(x, 183.85 if s == "S" else 183.86), radius=0.09, color=C.UNINFORMED) for x, s in uninf])
        inf_dot = Dot(ch.c2p(5.45, 183.86), radius=0.11, color=C.INFORMED)
        ledger = VGroup(
            label(r"random traders: we earn half the spread", font_size=26, color=C.UNINFORMED),
            mtex(r"+0.5\text{ cent per share, each}", font_size=32, color=C.PNL_UP),
            label(r"an informed trader buys just before a jump", font_size=26, color=C.INFORMED),
            mtex(r"183.86 - 183.895 = -3.5\text{ cents per share}", font_size=32, color=C.PNL_DOWN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(RIGHT, buff=0.35).shift(UP * 0.6)
        tag = note(r"schematic").to_corner(UR, buff=0.3)
        with self.voiceover(
            "If every trader were like those two, market making would be easy money. It isn't, because some of the "
            "people trading with you know something you don't. <bookmark mark='u'/> Most of the flow is uninformed: "
            "people buying and selling for their own reasons, at random as far as the price is concerned. Against "
            "them, the market maker earns half the spread on every trade. <bookmark mark='i'/> But now and then, "
            "someone buys from you just before the price jumps, because they saw it coming, perhaps because their "
            "information arrived a few microseconds before yours. <bookmark mark='j'/> That one trade costs three and "
            "a half cents a share, seven times what an uninformed trade earns."
        ) as vo:
            self.play(Create(ch), FadeIn(tl), FadeIn(tag))
            self.play(Create(bid_l), Create(ask_l), FadeIn(qlab))
            vo.wait_until("u")
            self.play(Create(mid_l), run_time=2.5, rate_func=linear)
            self.play(LaggedStart(*[GrowFromCenter(d) for d in dots_u], lag_ratio=0.25), FadeIn(ledger[:2]), run_time=2)
            vo.wait_until("i")
            self.play(GrowFromCenter(inf_dot), FadeIn(ledger[2]))
            vo.wait_until("j")
            jump = Arrow(ch.c2p(5.75, 183.86), ch.c2p(5.75, 183.895), buff=0, color=C.PNL_DOWN, stroke_width=4)
            self.play(GrowArrow(jump), FadeIn(ledger[3]))
        gm = VGroup(
            label(r"Glosten \& Milgrom (1985): the spread is an insurance premium", font_size=28),
            mtex(r"\underbrace{(1-\pi)\,\tfrac{s}{2}}_{\text{earned from the many}} = "
                 r"\underbrace{\pi\,\left(\Delta - \tfrac{s}{2}\right)}_{\text{lost to the few}}"
                 r"\quad\Longrightarrow\quad \frac{s}{2} = \pi\,\Delta", font_size=36),
            label(r"$\pi$ = share of informed traders, \enspace $\Delta$ = how far the price moves", font_size=24,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.3)
        gm.add_background_rectangle(color=BACKGROUND, opacity=0.95, buff=0.15)
        ex = mtex(r"\pi = 1/8,\ \ \Delta = 4\text{ cents} \;\Rightarrow\; \tfrac{s}{2} = 0.5\text{ cent}", font_size=30,
                  color=GREY_A)
        with self.voiceover(
            "<bookmark mark='g'/> In 1985, Lawrence Glosten and Paul Milgrom turned this into a theory of why spreads "
            "exist at all. If a fraction pi of the traders are informed, and they move the price by delta, the market "
            "maker breaks even only if what it earns from the many pays for what it loses to the few: <bookmark "
            "mark='e'/> half the spread must equal pi times delta. If one trader in eight knows the price is about to "
            "move four cents, the half-spread has to be half a cent. The spread is an insurance premium against being "
            "picked off."
        ) as vo:
            vo.wait_until("g")
            self.play(FadeIn(gm, shift=UP * 0.2))
            vo.wait_until("e")
            ex.next_to(ledger, DOWN, buff=0.35).align_to(ledger, LEFT).add_background_rectangle(color=BACKGROUND,
                                                                                                   opacity=0.95, buff=0.08)
            self.play(FadeIn(ex))
        self.clear_scene()

    # ------------------------------------------------------------------
    def consequence(self):
        two = VGroup(
            VGroup(label(r"be right", font_size=48, color=C.SIGNAL),
                   label(r"know where the price is going,\\so the spread you charge covers the risk", font_size=26,
                         color=GREY_A)).arrange(DOWN, buff=0.25),
            VGroup(label(r"be fast", font_size=48, color=C.LATENCY),
                   label(r"update your quotes before\\someone with faster news hits them", font_size=26,
                         color=GREY_A)).arrange(DOWN, buff=0.25),
        ).arrange(RIGHT, buff=1.6).shift(UP * 0.3)
        edge = label(r"edge per share: a fraction of a cent \quad$\Rightarrow$\quad the business is volume", font_size=30)
        edge.to_edge(DOWN, buff=0.8)
        hdr = label(r"the market maker's edge", font_size=40).to_edge(UP, buff=0.6)
        self.play(FadeIn(hdr), run_time=0.6)
        with self.voiceover(
            "So the market maker's edge is a fraction of a cent per share, and it lives or dies on two abilities. "
            "<bookmark mark='r'/> Be right: know where the price is going, so the spread you charge covers the risk. "
            "<bookmark mark='f'/> And be fast: update your quotes before someone with fresher information can trade "
            "against them. <bookmark mark='v'/> With an edge that thin, the business only works at enormous volume, "
            "which means a machine making millions of decisions a day, each one right, and each one fast."
        ) as vo:
            vo.wait_until("r")
            self.play(FadeIn(two[0], shift=UP * 0.2))
            vo.wait_until("f")
            self.play(FadeIn(two[1], shift=UP * 0.2))
            vo.wait_until("v")
            self.play(FadeIn(edge))
        self.clear_scene()
