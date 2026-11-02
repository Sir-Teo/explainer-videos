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
            "Two kinds of order do almost all the work. A market order says: trade now, at whatever price is "
            "available. It is certain to trade, and uncertain about the price. <bookmark mark='a'/> A limit order "
            "says: buy at this price or lower, sell at this price or higher. The price is certain, the trade is not; "
            "it waits. A stop order waits for a trigger, then becomes a market order. <bookmark mark='b'/> Orders "
            "also say how long they live: for the day, until cancelled, immediate-or-cancel, or fill-or-kill. And "
            "some hide: an iceberg shows a slice of its size, a hidden order shows none, and for that privilege it "
            "queues behind every displayed order at the same price. The rule of the book is price first, then "
            "visibility, then time."
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
            "Here is a book running: one row per price, asks above and bids below, each block one share waiting. "
            "This one is simulated, by the zero-intelligence model of Smith, Farmer, Gillemot and Krishnamurthy: "
            "orders arrive at random prices, market orders at random times, resting orders are cancelled at "
            "random. <bookmark mark='a'/> Watch a level: a new order joins at the back of its queue; a "
            "cancellation pulls a block out of the middle; a market order bites from the front of the best queue. "
            "The yellow bracket is the spread, and it breathes as the front queues empty and refill. "
            "<bookmark mark='b'/> Nobody in this model thinks, and the book still has a spread that is usually one "
            "to four ticks, thin queues at the front and deeper ones behind: much of a book's shape is plumbing, "
            "not strategy."
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
        verdict = label(r"real books thicken behind the best quote: impact is concave (Part 37)" if concave else
                        r"this book is thin behind the best quote: impact is steeper than linear", font_size=21,
                        color=QC.IDEA).next_to(leg, DOWN, buff=0.35).align_to(leg, LEFT)
        with self.voiceover(
            "What does impatience cost? Say every tick above the best ask holds d shares. A market buy of Q shares "
            "takes the best level first, then the next: price priority. <bookmark mark='a'/> The average price is "
            "an arithmetic series: the best ask plus half a tick for every extra level it eats. "
            "<bookmark mark='b'/> Against the mid price, the cost is half the spread plus the walk. Twice that "
            "distance is the effective spread, the cost measure Parts thirty-six and thirty-seven use. "
            "<bookmark mark='c'/> Now measure it in the simulated book, four seeds, against the uniform formula. "
            + ("The book is thin at the front and thicker behind, so the cost rises fast for small orders and "
               "then bends: impact is concave, which is what real books show too."
               if concave else "Here the formula understates the cost: the book thins out behind the front.")
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
            f"Turn up the flow of market orders relative to limit orders and the spread widens: about "
            f"{np.mean(sp['0.5']):.0f} ticks, then {np.mean(sp['1.0']):.0f}, then {np.mean(sp['2.0']):.0f}, and at "
            "four times the book runs dry. <bookmark mark='a'/> The tick itself is a rule. In September 2024 the "
            "SEC amended Rule 612: stocks whose average quoted spread is a cent and a half or less would quote in "
            "half-pennies, and the fee an exchange may charge to take liquidity was cut from thirty to ten "
            "hundredths of a cent per share. The compliance date was moved to November 2026, and then, by an order "
            "of June 2026, to November 2027, while the Commission reviews the rules again. "
            "<bookmark mark='b'/> Pause and predict: halve the tick on a stock that always trades one tick wide "
            "with long queues. What happens to the spread, and to the queues?"
        ) as vo:
            self.play(FadeIn(g), FadeIn(head), LaggedStart(*[FadeIn(p) for p in pts], lag_ratio=0.1))
            self.play(Create(mean_line))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in rule], lag_ratio=0.3), FadeIn(src))
            vo.wait_until("b")
            self.play(FadeIn(q))
        self.wait(1.0)
        self.clear_scene()
