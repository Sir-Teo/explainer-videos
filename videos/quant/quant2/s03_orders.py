from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant2.common import GAIN, LOSS, PART, TRADE, load


class Orders(VoiceoverScene):
    def construct(self):
        a = load("auction")
        self.card()
        self.types()
        self.book()
        self.auction(a)
        self.dealers()

    def card(self):
        c = chapter_card(2, r"Orders, books and auctions", r"How does a buyer find a seller?", lit=(2005,), part=PART)
        with self.voiceover("Chapter two. Orders, books and auctions."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def types(self):
        cards = VGroup(
            definition_card(r"Market order", r"Buy or sell now, at whatever the market offers. Certain to trade; "
                            r"the price is not certain.", width=4.2, color=LOSS, font_size=22),
            definition_card(r"Limit order", r"Buy at this price or lower, sell at this price or higher. The price is "
                            r"certain; trading is not. It waits in the book.", width=4.2, color=GAIN, font_size=22),
            definition_card(r"Stop order", r"Becomes a market order once the price reaches a trigger: used to cut "
                            r"losses, and, in a crash, to add to the selling.", width=4.2, color=QC.IDEA, font_size=22),
        ).arrange(RIGHT, buff=0.3, aligned_edge=UP).move_to(UP * 0.4)
        with self.voiceover(
            "Two kinds of order do almost all the work. A market order says: trade now, at whatever price is "
            "available. It is certain to trade, and uncertain about the price. <bookmark mark='a'/> A limit order "
            "says: buy at this price or lower, sell at this price or higher. The price is certain, the trade is not; "
            "it waits. <bookmark mark='b'/> And a stop order waits for a trigger price, then becomes a market order: "
            "a way to cut a loss, and, when many are triggered at once, a way to deepen a crash."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[2], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def book(self):
        asks = [(100.05, 300), (100.04, 500), (100.03, 200), (100.02, 400), (100.01, 150)]
        bids = [(100.00, 250), (99.99, 400), (99.98, 350), (99.97, 600), (99.96, 200)]
        rows = VGroup()
        W = 0.006
        for px, q in asks + bids:
            col = LOSS if px > 100.0 else GAIN
            bar = Rectangle(width=q * W, height=0.38, stroke_width=0, fill_color=col, fill_opacity=0.7)
            pt = MathTex(f"{px:.2f}", font_size=28, color=col)
            qt = MathTex(f"{q}", font_size=24, color=GREY_A)
            r_ = VGroup(pt, bar, qt).arrange(RIGHT, buff=0.25)
            bar.align_to(pt, LEFT).shift(RIGHT * 1.2)
            qt.next_to(bar, RIGHT, buff=0.15)
            rows.add(r_)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.1).to_edge(LEFT, buff=1.2).shift(DOWN * 0.2)
        spread = Brace(VGroup(rows[4], rows[5]), RIGHT, buff=1.8, color=QC.IDEA)
        sl = label(r"the spread: 1 cent", font_size=24, color=QC.IDEA).next_to(spread, RIGHT, buff=0.1)
        hdr = VGroup(label(r"asks: sellers waiting", font_size=24, color=LOSS),
                     label(r"bids: buyers waiting", font_size=24, color=GAIN))
        hdr[0].next_to(rows[0], UP, buff=0.25).align_to(rows, LEFT)
        hdr[1].next_to(rows[-1], DOWN, buff=0.25).align_to(rows, LEFT)
        rule = VGroup(label(r"Price-time priority:", font_size=26, color=GREY_A),
                      label(r"the best price trades first;", font_size=24),
                      label(r"at one price, the oldest order first.", font_size=24),
                      label(r"A market order to buy 600 takes", font_size=24, color=TRADE),
                      label(r"150 at 100.01 and 400 at 100.02,", font_size=24, color=TRADE),
                      label(r"then 50 at 100.03: average 100.017.", font_size=24, color=TRADE),
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).to_edge(RIGHT, buff=0.6)
        with self.voiceover(
            "Limit orders that haven't traded wait in the order book. Above, the asks: sellers and their prices. "
            "Below, the bids: buyers. The gap between the best bid and the best ask is the spread, here one cent. "
            "<bookmark mark='a'/> Exchanges match by price-time priority: the best price first, and at the same "
            "price, whoever came first. <bookmark mark='b'/> A market order to buy six hundred shares eats up the "
            "book: a hundred and fifty at 100.01, four hundred at 100.02, then fifty at 100.03. Its average price is "
            "a cent and three quarters above the best bid. That cost of trading, the spread and the walk up the "
            "book, is the subject of Parts thirty-six and thirty-seven."
        ) as vo:
            self.play(FadeIn(hdr), LaggedStart(*[FadeIn(r_) for r_ in rows], lag_ratio=0.1))
            self.play(GrowFromCenter(spread), FadeIn(sl))
            vo.wait_until("a")
            self.play(FadeIn(rule[:3]))
            vo.wait_until("b")
            self.play(FadeIn(rule[3:]))
            self.play(rows[4][1].animate.set_fill(opacity=0.12), run_time=0.6)
            self.play(rows[3][1].animate.set_fill(opacity=0.12), run_time=0.6)
            self.play(rows[2][1].animate.stretch(0.75, 0, about_edge=RIGHT), run_time=0.6)
        self.wait(0.4)
        self.clear_scene()

    def auction(self, a):
        c = np.asarray(a["candidates"])
        dm, sp = np.asarray(a["demand"]), np.asarray(a["supply"])
        m = (c >= 98.6) & (c <= 101.4)
        top = float(max(dm.max(), sp.max())) * 1.05
        g = axes([98.6, 101.4], [0, top], x_length=7.6, y_length=4.4, xlabel=r"price", ylabel=r"shares",
                 xticks=[99, 99.5, 100, 100.5, 101], yticks=[0, 10000, 20000, 30000],
                 yfmt=lambda v: f"{v / 1000:.0f}" + r"\text{k}", font_size=18).to_edge(LEFT, buff=0.7).shift(DOWN * 0.3)
        ax = g.ax
        dl = VMobject(color=QC.GAIN, stroke_width=3.5).set_points_as_corners([ax.c2p(x, y) for x, y in zip(c[m], dm[m])])
        sl = VMobject(color=QC.LOSS, stroke_width=3.5).set_points_as_corners([ax.c2p(x, y) for x, y in zip(c[m], sp[m])])
        px = DashedLine(ax.c2p(a["price"], 0), ax.c2p(a["price"], top), color=QC.IDEA, stroke_width=2.5)
        pl = MathTex(rf"{a['price']:.2f}", font_size=30, color=QC.IDEA).next_to(ax.c2p(a["price"], top), UP, buff=0.05)
        leg = legend([(QC.GAIN, r"buyers willing at this price or more"), (QC.LOSS, r"sellers willing at this price or less")],
                     font_size=21).to_edge(RIGHT, buff=0.4).shift(UP * 2.0)
        res = VGroup(
            label(r"the closing auction: every order at one price,", font_size=24),
            label(r"the price that trades the most", font_size=24),
            MathTex(rf"{a['volume']:,.0f}\ \text{{shares at}}\ {a['price']:.2f}".replace(",", "{,}"), font_size=30,
                    color=QC.IDEA),
            label(r"300 simulated limit orders", font_size=20, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).next_to(leg, DOWN, buff=0.5).align_to(leg, LEFT)
        with self.voiceover(
            "Continuous trading is not the only way. Most exchanges open and close the day with an auction: orders "
            "are collected for a few minutes, and then everything that can trade, trades at a single price. Here "
            "are three hundred simulated orders. The green curve counts the shares buyers want at each price or "
            "more; the red curve, the shares sellers offer at each price or less. <bookmark mark='a'/> The auction "
            "picks the price where the most shares change hands, where the curves cross. The closing auction "
            "matters: index funds trade there, because indices are computed from closing prices, and it has become "
            "one of the busiest moments of the trading day."
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg))
            self.play(Create(dl), Create(sl), run_time=2.5)
            vo.wait_until("a")
            self.play(Create(px), FadeIn(pl))
            self.play(LaggedStart(*[FadeIn(r_) for r_ in res], lag_ratio=0.3))
        self.wait(0.4)
        self.clear_scene()

    def dealers(self):
        cards = VGroup(
            definition_card(r"Exchange", r"A central limit order book, anyone's orders against anyone's: shares, "
                            r"futures, listed options.", width=4.2, color=TRADE, font_size=22),
            definition_card(r"Dealer market", r"You trade with a dealer, who quotes a bid and an ask from their own "
                            r"inventory: most bonds, currencies, swaps.", width=4.2, color=QC.IDEA, font_size=22),
            definition_card(r"Request for quote", r"You ask several dealers at once and take the best answer: the "
                            r"electronic form of a phone call.", width=4.2, color=QC.HOUSE, font_size=22),
        ).arrange(RIGHT, buff=0.3, aligned_edge=UP).move_to(UP * 0.5)
        foot = wrapped_label(r"in the US, a retail order is often filled not on an exchange but by a wholesaler, which "
                             r"pays the broker for the order flow (Part 35)", 12.0, 22, GREY_A).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Not every market is an exchange. Shares, futures and listed options trade in central order books. But "
            "most bonds, currencies and swaps trade with dealers, who quote a bid and an ask from their own "
            "inventory, or by request for quote: you ask several dealers at once and take the best answer, the "
            "electronic version of a phone call. <bookmark mark='a'/> And in America most retail share orders never "
            "reach an exchange. They are filled by wholesalers, who pay the broker for the flow. Who trades with "
            "whom, and why that matters, is Part thirty-five."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(c_, shift=UP * 0.2) for c_ in cards], lag_ratio=0.5, run_time=4))
            vo.wait_until("a")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()
