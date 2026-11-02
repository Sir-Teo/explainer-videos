from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant2.common import GAIN, LOSS, PART, TRADE, OrderBookLadder, load

C_ = {r"a": LOSS, r"m": GREY_A, r"\delta": QC.IDEA, r"Q": TRADE, r"d": GAIN}


def row(*parts, fs=38):
    return cmath(*parts, colors=C_, font_size=fs)


class Orders(VoiceoverScene):
    def construct(self):
        bk = load("book")
        self.card()
        self.types()
        self.live(bk)
        self.walk(bk)
        self.tick(bk)

    def card(self):
        c = chapter_card(3, r"The order book", r"How does a buyer find a seller, and what does impatience cost?",
                         lit=(2005,), part=PART)
        with self.voiceover("Chapter three. The order book."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def types(self):
        cards = VGroup(
            definition_card(r"Market order", r"Buy or sell now, at whatever the book offers. Certain to trade; "
                            r"the price is not certain.", width=4.2, color=LOSS, font_size=21),
            definition_card(r"Limit order", r"Buy at this price or lower, sell at this price or higher. The price is "
                            r"certain; trading is not. It waits in the book.", width=4.2, color=GAIN, font_size=21),
            definition_card(r"Stop order", r"Becomes a market order once the price reaches a trigger: used to cut "
                            r"losses, and, in a crash, adds to the selling.", width=4.2, color=QC.IDEA, font_size=21),
        ).arrange(RIGHT, buff=0.3, aligned_edge=UP).move_to(UP * 1.3)
        more = VGroup(
            label(r"validity: DAY (until the close), GTC (good till cancelled), IOC (fill what you can now, cancel "
                  r"the rest), FOK (all now or nothing)", font_size=21),
            label(r"hidden and iceberg orders show part or none of their size; at the same price they wait behind "
                  r"displayed orders", font_size=21),
            label(r"precedence: price first, then visibility, then time", font_size=24, color=QC.HOUSE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(cards, DOWN, buff=0.5)
        if more.width > 13.0:
            more.scale_to_fit_width(13.0)
        with self.voiceover(
            "A market order trades now, at whatever price is there. <bookmark mark='a'/> A limit order names its price and "
            "waits; a stop order waits for a trigger, then becomes a market order. <bookmark mark='b'/> Orders also say how "
            "long they live: the day, until cancelled, immediate-or-cancel, fill-or-kill. Icebergs show part of their size, "
            "hidden orders none, and queue behind displayed orders at their price: price first, then visibility, then time."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=UP * 0.2), FadeIn(cards[2], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(m) for m in more], lag_ratio=0.5))
        self.wait(0.4)
        self.clear_scene()

    def live(self, bk):
        t = ValueTracker(0)
        lad = OrderBookLadder(bk["frames"], t, bk["kinds"])
        lad.shift(LEFT * 3.0 + DOWN * 0.2)
        hdr = VGroup(label(r"asks: sellers waiting", font_size=22, color=LOSS).next_to(lad, UP, buff=0.2),
                     label(r"bids: buyers waiting", font_size=22, color=GAIN).next_to(lad, DOWN, buff=0.2))
        names = {0: (r"limit buy joins a queue", GAIN), 1: (r"limit sell joins a queue", LOSS),
                 2: (r"market buy takes the best ask", TRADE), 3: (r"market sell takes the best bid", TRADE),
                 4: (r"a bid is cancelled", GREY_B), 5: (r"an ask is cancelled", GREY_B)}
        ev = {k: label(v[0], font_size=24, color=v[1]) for k, v in names.items()}
        for m in ev.values():
            m.to_edge(RIGHT, buff=0.8).shift(UP * 2.5)
        cur = ev[int(bk["kinds"][0])].copy()
        model = VGroup(
            label(r"Zero intelligence (Smith, Farmer, Gillemot and Krishnamurthy, 2003):", font_size=21,
                  color=QC.IDEA),
            label(r"limit orders arrive at random prices near the best quote,", font_size=21),
            label(r"market orders arrive at random, resting orders are cancelled at random.", font_size=21),
            label(r"No one thinks. The book still has a spread, queues and depth.", font_size=21, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_edge(RIGHT, buff=0.4).shift(DOWN * 0.4)
        hist = np.asarray(bk["spread_hist"], float)
        hg = axes([0, 11], [0, 1.05], x_length=4.2, y_length=1.6, xlabel=r"spread, ticks", xticks=[1, 5, 10],
                  font_size=15).to_corner(DR, buff=0.5)
        hb = VGroup(*[Rectangle(width=0.3, height=max(hg.ax.c2p(0, h / hist.max())[1] - hg.ax.c2p(0, 0)[1], 0.01),
                                stroke_width=0, fill_color=QC.IDEA, fill_opacity=0.8)
                      .move_to(hg.ax.c2p(i, 0), aligned_edge=DOWN) for i, h in enumerate(hist) if h > 0])
        with self.voiceover(
            "Here is a book running: one row per price, asks above and bids below, each block one share waiting. It is "
            "simulated, by the zero-intelligence model of Smith, Farmer, Gillemot and Krishnamurthy: orders arrive at random "
            "prices, market orders at random times, and resting orders are cancelled at random. <bookmark mark='a'/> Watch "
            "a level: a new order joins the back of its queue, a cancel pulls a block out of the middle, a market order bites "
            "the front, and the spread, in yellow, breathes. <bookmark mark='b'/> Nobody in this model thinks, and the book "
            "still has a spread of one to four ticks and thin queues at the front: much of a book's shape is plumbing, not "
            "strategy."
        ) as vo:
            self.play(FadeIn(lad), FadeIn(hdr), FadeIn(model))
            self.add(cur)
            vo.wait_until("a")
            for k in range(1, 90):
                nk = ev[int(bk["kinds"][k])].copy()
                self.play(t.animate.set_value(k), Transform(cur, nk), run_time=0.12, rate_func=linear)
            vo.wait_until("b")
            self.play(FadeIn(hg), LaggedStart(*[GrowFromEdge(r_, DOWN) for r_ in hb], lag_ratio=0.1),
                      t.animate.set_value(len(bk["frames"]) - 1), run_time=3)
        self.wait(0.4)
        self.clear_scene()

    def walk(self, bk):
        rows = [
            row(r"\text{fills}", r"=", r"a,\ a+\delta,\ \dots,\ a + (Q/d - 1)\,\delta"),
            row(r"\bar p", r"=", r"a + \frac{\delta}{2}\Big(\frac{Q}{d} - 1\Big)"),
            row(r"\bar p - m", r"=", r"\frac{s}{2} + \frac{\delta}{2}\Big(\frac{Q}{d} - 1\Big)"),
        ]
        whys = [why(r"depth $d$ at every tick $\delta$ above the best ask $a$: price priority", font_size=20),
                why(r"the average of an arithmetic series", font_size=20),
                why(r"cost against the mid $m$: half the spread, plus the walk; effective spread $2|\bar p - m|$",
                    font_size=20)]
        for r_ in rows:
            r_.scale(0.85)
        step = ladder(self, rows, whys, keep=3, top=3.3, x=-3.2, buff=0.5, edge=6.9)
        Q = np.asarray(bk["Q"], float)
        W = np.asarray(bk["walk"], float)
        uni = np.asarray(bk["walk_uniform"], float)
        g = axes([0, 40], [0, 9.5], x_length=6.2, y_length=3.0, xlabel=r"market buy size $Q$, shares",
                 ylabel=r"average price above the best ask, ticks", xticks=[0, 20, 40], yticks=[0, 4, 8],
                 font_size=17).to_edge(DOWN, buff=0.4).to_edge(LEFT, buff=0.8)
        ax = g.ax
        sb = seed_band(ax, Q, W, QC.IDEA)
        ul = DashedLine(ax.c2p(Q[0], uni[0]), ax.c2p(Q[-1], uni[-1]), color=GREY_B, stroke_width=2.5)
        leg = legend([(QC.IDEA, r"zero-intelligence book, 4 seeds"),
                      (GREY_B, rf"uniform depth $d = {float(bk['depth'][0]):.1f}$ (the formula)")], font_size=19)
        leg.next_to(g, RIGHT, buff=0.3).shift(UP * 0.4)
        concave = W.mean(0)[-1] < uni[-1]
        walk_note = ("the front is thin and deeper levels thicker, so cost bends: impact is concave, as in real books."
                     if concave else "the formula understates the cost: the book thins out behind the front.")
        verdict = label(r"real books thicken behind the best quote: impact is concave (Part 37)" if concave else
                        r"this book is thin behind the best quote: impact is steeper than linear", font_size=21,
                        color=QC.IDEA).next_to(leg, DOWN, buff=0.35).align_to(leg, LEFT)
        with self.voiceover(
            "What does impatience cost? Say each tick above the best ask holds d shares. A buy of Q shares eats the levels in "
            "order. <bookmark mark='a'/> Its average price is an arithmetic series. <bookmark mark='b'/> Against the mid, "
            "the cost is half the spread plus the walk; twice it is the effective spread. <bookmark mark='c'/> In the "
            f"simulated book, four seeds, against the formula: {walk_note}"
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            self.play(FadeIn(g), FadeIn(leg))
            self.play(Create(ul), FadeIn(sb[0]), Create(sb[1]), run_time=2)
            self.play(FadeIn(verdict))
        self.wait(0.4)
        self.clear_scene()

    def tick(self, bk):
        ratios = [0.5, 1.0, 2.0]
        g = axes([0.3, 2.3], [0, 7], x_length=4.6, y_length=3.2, xlabel=r"market-order rate / limit-order rate",
                 ylabel=r"mean spread, ticks", xticks=[0.5, 1, 2], yticks=[0, 3, 6], font_size=16)
        g.to_edge(LEFT, buff=0.7).shift(DOWN * 0.6)
        ax = g.ax
        sp = bk["mean_spread"]
        pts = VGroup()
        for r_ in ratios:
            for v in sp[str(r_)]:
                pts.add(Dot(ax.c2p(r_, v), radius=0.05, color=QC.IDEA))
        mean_line = curve(ax, ratios, [float(np.mean(sp[str(r_)])) for r_ in ratios], QC.IDEA)
        head = label(r"More impatient flow, wider spreads (simulated, 4 seeds each)", font_size=22,
                     color=QC.IDEA).next_to(g, UP, buff=0.3).align_to(g, LEFT)
        rule = VGroup(
            label(r"SEC Rule 612 amendments (adopted 18 September 2024)", font_size=24, color=QC.HOUSE),
            label(r"a half-penny tick for stocks whose time-weighted", font_size=21),
            label(r"quoted spread is \$0.015 or less", font_size=21),
            label(r"exchange access-fee cap cut from 30 to 10 mils", font_size=21),
            label(r"compliance: November 2025, then 2026 by exemptive relief;", font_size=21),
            label(r"on 11 June 2026 delayed again, to November 2027", font_size=21, color=QC.IDEA),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_edge(RIGHT, buff=0.4).shift(UP * 0.6)
        q = desk_question(r"Halve the tick on a stock that always trades at a one-tick spread with long queues. "
                          r"What happens to the spread and the queues?", width=6.0, font_size=21)
        q.next_to(rule, DOWN, buff=0.35).align_to(rule, LEFT)
        src = note(r"SEC Release 34-101070 (2024); exemptive orders 34-104172 (2025) and 34-105656 (2026)",
                   font_size=16).to_edge(DOWN, buff=0.15)
        with self.voiceover(
            f"More market orders relative to limit orders widen the spread: about {np.mean(sp['0.5']):.0f}, "
            f"{np.mean(sp['1.0']):.0f}, then {np.mean(sp['2.0']):.0f} ticks. <bookmark mark='a'/> The tick itself is a rule. "
            "In 2024 the SEC amended Rule 612: stocks with average spreads of a cent and a half or less would quote in "
            "half-pennies, and access fees were cut from thirty to ten hundredths of a cent. Compliance was due today, in "
            "November 2026; in June the SEC moved it to November 2027. <bookmark mark='b'/> Pause and predict: halve the "
            "tick on a stock with a one-tick spread and long queues. What happens?"
        ) as vo:
            self.play(FadeIn(g), FadeIn(head), LaggedStart(*[FadeIn(p) for p in pts], lag_ratio=0.1))
            self.play(Create(mean_line))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in rule], lag_ratio=0.3), FadeIn(src))
            vo.wait_until("b")
            self.play(FadeIn(q))
        self.wait(1.0)
        self.clear_scene()
