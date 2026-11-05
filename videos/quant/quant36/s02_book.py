from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant36.common import (ASK_C, BAD, BID_C, GOOD, HURDLE, OFI_C, PART, illustration,
                                         load)


class Book(VoiceoverScene):
    def construct(self):
        b = load("book")
        self.card()
        self.rules()
        self.ladder()
        self.events()
        self.data_(b)
        self.minute(b)
        self.day(b)
        self.order_types()
        self.tick()
        self.question()

    def card(self):
        c = chapter_card(1, r"The book", r"What is an order book, and what does Bitcoin's look like?", part=PART)
        with self.voiceover("Chapter one. A limit order book is a list of everyone's standing offers to buy and to sell, "
                            "sorted by price. Every exchange in this act is one. Here are its rules, and one day of the "
                            "most traded book in crypto."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def rules(self):
        rows = [cmath(r"\text{limit order}", r":", r"\text{rest at a price until filled or cancelled}", font_size=32,
                      colors={r"\text{limit order}": BID_C}),
                cmath(r"\text{market order}", r":", r"\text{trade now against the best resting orders}", font_size=32,
                      colors={r"\text{market order}": ASK_C}),
                cmath(r"\text{priority}", r":", r"\text{best price first; at a price, first come first served}",
                      font_size=30, colors={r"\text{priority}": HURDLE}),
                cmath(r"\text{tick}", r":", r"\text{the smallest price step}", font_size=32)]
        whys = [why(r"the maker supplies liquidity: Part 35's dealer, now anyone"),
                why(r"the taker demands it, and pays the spread"),
                why(r"price-time priority: so a place in the queue is an asset, and arriving early is worth paying for"),
                why(r"0.1 dollars on Binance's BTCUSDT perpetual: at \$27{,}000, about four hundredths of a basis point")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.45, edge=6.9)
        with self.voiceover(
            "The rules. <bookmark mark='a'/> A limit order rests at a price until it is filled or cancelled: its owner "
            "supplies liquidity. <bookmark mark='b'/> A market order trades now against the best resting orders, and "
            "pays the spread. <bookmark mark='c'/> Priority: best price first, and at the same price, first come first "
            "served. So a place in the queue is an asset. <bookmark mark='d'/> And the tick, the smallest price step: on "
            "Bitcoin's perpetual future, ten cents, about four hundredths of a basis point."
        ) as vo:
            step(0)
            for k, mk in enumerate(("a", "b", "c", "d")):
                vo.wait_until(mk)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def ladder(self):
        prices = [100.04, 100.03, 100.02, 100.01, 100.00, 99.99, 99.98, 99.97]
        sizes = [6, 4, 5, 2, 7, 5, 8, 6]
        rows = VGroup()
        for p, s in zip(prices, sizes):
            col = ASK_C if p > 100.005 else BID_C
            bar = Rectangle(width=0.35 * s, height=0.42, fill_color=col, fill_opacity=0.7, stroke_width=0)
            lab = MathTex(f"{p:.2f}", font_size=24)
            row = VGroup(lab, bar).arrange(RIGHT, buff=0.3)
            bar.align_to(lab, LEFT).shift(RIGHT * 1.4)
            rows.add(row)
        rows.arrange(DOWN, buff=0.08, aligned_edge=LEFT).move_to(LEFT * 1.5)
        spread = Brace(VGroup(rows[3], rows[4]), RIGHT, color=HURDLE)
        st = label(r"the spread: one tick", font_size=18, color=HURDLE).next_to(spread, RIGHT, buff=0.15)
        lab_a = label(r"offers", font_size=18, color=ASK_C).next_to(rows[0], UP, buff=0.2)
        lab_b = label(r"bids", font_size=18, color=BID_C).next_to(rows[-1], DOWN, buff=0.2)
        ill = illustration(r"illustration: a stylised book, sizes in lots")
        with self.voiceover(
            "The picture. <bookmark mark='a'/> Offers above, bids below, each price with the size waiting there. "
            "<bookmark mark='b'/> The gap between the best bid and the best offer is the spread; on a liquid market it is "
            "usually one tick, so the price cannot get any closer, and the action is in the sizes of the two best queues."
        ) as vo:
            self.play(FadeIn(ill))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows], lag_ratio=0.1), FadeIn(lab_a),
                      FadeIn(lab_b))
            vo.wait_until("b")
            self.play(GrowFromCenter(spread), FadeIn(st))
        self.wait(0.4)
        self.clear_scene()

    def events(self):
        rows = [cmath(r"\text{add}", r":", r"\text{a new limit order joins the back of a queue}", font_size=32,
                      colors={r"\text{add}": GOOD}),
                cmath(r"\text{cancel}", r":", r"\text{a resting order leaves its queue}", font_size=32,
                      colors={r"\text{cancel}": GREY_B}),
                cmath(r"\text{trade}", r":", r"\text{a market order eats the front of the best queue}", font_size=32,
                      colors={r"\text{trade}": BAD}),
                cmath(r"\text{a tick}", r":", r"\text{a best queue empties, and the price moves}", font_size=32,
                      colors={r"\text{a tick}": HURDLE})]
        whys = [why(r"most messages to an exchange are adds and cancels; only a small fraction become trades"),
                why(r"cancellation is the market maker's defence against stale quotes (Part 35's sniping)"),
                why(r"the only event that moves cash and positions"),
                why(r"so the price is driven by a race between two queues, which Chapter 2 models")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.45, edge=6.9)
        with self.voiceover(
            "Four events change the book. <bookmark mark='a'/> A new limit order joins the back of a queue. "
            "<bookmark mark='b'/> A resting order is cancelled: the market maker's defence against stale quotes. "
            "<bookmark mark='c'/> A market order eats the front of the best queue. <bookmark mark='d'/> And when a best "
            "queue empties, the price moves. The price is the outcome of a race between two queues."
        ) as vo:
            step(0)
            for k, mk in enumerate(("a", "b", "c", "d")):
                vo.wait_until(mk)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def data_(self, b):
        days = b["days"]
        hx = [-4.6, -2.2, 0.0, 2.2, 4.6]
        head = VGroup(label(r"day", font_size=17, color=GREY_B), label(r"hours covered", font_size=17, color=GREY_B),
                      label(r"one-tick spread", font_size=17, color=HURDLE), label(r"median best queue, BTC", font_size=17,
                                                                                    color=GREY_B),
                      label(r"book updates a second", font_size=17, color=OFI_C))
        tab = VGroup(head)
        for d, r in days.items():
            tab.add(VGroup(label(d, font_size=18), MathTex(f"{r['hours']:.1f}", font_size=24),
                           MathTex(rf"{100 * r['one_tick']:.1f}\%", font_size=24),
                           MathTex(rf"{(r['bq_med'] + r['aq_med']) / 2:.1f}", font_size=24),
                           MathTex(f"{r['updates_per_s']:.0f}", font_size=24)))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 1.8 - 0.75 * j, 0])
        foot = wrapped_label(r"Binance's public best-bid/offer stream for the BTCUSDT perpetual; the first two days are "
                             r"the archive's first, partly covered; reduced here to a 100-millisecond grid", 11.4, 15,
                             GREY_A).to_edge(DOWN, buff=0.5)
        d0 = list(days.values())[1]
        with self.voiceover(
            "The data: Binance's public stream of best bids and offers for Bitcoin's perpetual future, four days in May "
            "2023. <bookmark mark='a'/> The spread is one tick more than ninety-nine percent of the time. The best queues "
            "hold a few bitcoin, one to three hundred thousand dollars. And the best quotes change about "
            f"{d0['updates_per_s']:.0f} times a second on a weekday, fewer at the weekend. The first two days fit the "
            "models, the weekend tests them."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(foot))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[1:]], lag_ratio=0.3))
        self.wait(0.4)
        self.clear_scene()

    def minute(self, b):
        sg = b["seg"]
        bid, ask = np.asarray(sg["bid"], float), np.asarray(sg["ask"], float)
        bq, aq = np.asarray(sg["bq"], float), np.asarray(sg["aq"], float)
        t = np.arange(len(bid)) / 10
        lo, hi = float(bid.min() - 0.2), float(ask.max() + 0.2)
        g = axes([0, 60], [lo, hi], x_length=8.0, y_length=2.6, xlabel="", ylabel=r"price, \$", xticks=[], yticks=[],
                 font_size=14).move_to(UP * 1.4)
        ax = g.ax
        c1 = curve(ax, t, bid, BID_C, stroke_width=2.5)
        c2 = curve(ax, t, ask, ASK_C, stroke_width=2.5)
        top = float(np.ceil(max(bq.max(), aq.max()) / 5) * 5)
        g2 = axes([0, 60], [-top, top], x_length=8.0, y_length=2.6, xlabel=r"seconds", ylabel=r"best queues, BTC",
                  xticks=[0, 30, 60], yticks=[-top, 0, top], yfmt=lambda v: f"{abs(v):.0f}", font_size=14)
        g2.move_to(DOWN * 1.8)
        ax2 = g2.ax
        c3 = curve(ax2, t, bq, BID_C, stroke_width=2)
        c4 = curve(ax2, t, -aq, ASK_C, stroke_width=2)
        with self.voiceover(
            "One minute of it. <bookmark mark='a'/> The best bid and offer, ten cents apart, step together. "
            "<bookmark mark='b'/> Below, the two best queues, the bid up and the offer down. Watch a queue drain toward "
            "zero just before the price steps through it. That race is the whole game of this part."
        ) as vo:
            self.play(FadeIn(g), FadeIn(g2))
            vo.wait_until("a")
            self.play(Create(c1), Create(c2), run_time=2)
            vo.wait_until("b")
            self.play(Create(c3), Create(c4), run_time=2)
        self.wait(0.4)
        self.clear_scene()

    def day(self, b):
        d = b["days"]["2023-05-20"]
        y = np.asarray(d["by_hour"], float)
        top = float(np.ceil(np.nanmax(y) / 20) * 20)
        g = axes([0, 23], [0, top], x_length=7.4, y_length=4.2, xlabel=r"hour, UTC (Saturday 20 May 2023)",
                 ylabel=r"book updates a second", xticks=[0, 6, 12, 18, 23], yticks=[0, top / 2, top],
                 yfmt=lambda v: f"{v:.0f}", font_size=15).move_to(LEFT * 1.0 + DOWN * 0.2)
        ax = g.ax
        bars = VGroup(*[Rectangle(width=0.22, height=max(1e-3, ax.c2p(0, v)[1] - ax.c2p(0, 0)[1]), fill_color=OFI_C,
                                  fill_opacity=0.8, stroke_width=0).move_to(ax.c2p(h, v / 2)) for h, v in enumerate(y)])
        hi_h = int(np.nanargmax(y))
        with self.voiceover(
            "Activity through a day. <bookmark mark='a'/> Even on a Saturday the book updates dozens of times a second "
            f"at every hour, peaking around {hi_h}:00 UTC. Crypto never closes, but it does sleep a little."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars], lag_ratio=0.03))
        self.wait(0.4)
        self.clear_scene()

    def order_types(self):
        cards = VGroup(
            desk_question(r"limit and market orders", r"a limit order waits in the queue at its price and supplies "
                          r"liquidity; a market order takes the best available prices at once and demands it",
                          width=12.4, font_size=19),
            desk_question(r"post-only and immediate-or-cancel", r"a post-only order is rejected rather than allowed to "
                          r"take; an immediate-or-cancel order takes what it can and leaves nothing behind", width=12.4,
                          font_size=19),
            desk_question(r"icebergs and stops", r"an iceberg shows only part of its size and refills from a hidden "
                          r"reserve, joining the back of the queue each time; a stop order becomes a market order when "
                          r"the price crosses a level, which is how falls feed on themselves", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "The vocabulary of orders. <bookmark mark='a'/> A limit order waits at its price and supplies liquidity; a "
            "market order takes the best prices at once and demands it. <bookmark mark='b'/> A post-only order is "
            "rejected rather than allowed to take, which is how makers protect their fees; an immediate-or-cancel order "
            "takes what it can and leaves nothing resting. <bookmark mark='c'/> An iceberg shows only part of its size "
            "and refills from a hidden reserve, losing its place each time. And a stop order turns into a market order "
            "when the price crosses a level: one reason falls feed on themselves."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def tick(self):
        mv = load("micro")["move_med"]
        cards = VGroup(
            desk_question(r"large tick", r"when the tick is wide relative to the natural spread and to the price's moves, "
                          r"the spread sits at one tick, queues are long, and the price moves rarely, one tick at a time: "
                          r"priority is everything", width=12.4, font_size=19),
            desk_question(r"small tick", r"when the tick is tiny, the price moves many ticks at a time, the best queues are "
                          r"a thin slice of the book, and traders compete by price; the half-cent US tick of Part 35 was "
                          r"aimed at the first kind of market", width=12.4, font_size=19),
            desk_question(r"Bitcoin's perpetual: both at once", rf"a one-tick spread like the first, but moves like the "
                          rf"second: when the mid changes between two snapshots a tenth of a second apart, the median "
                          rf"jump is {mv:.0f} ticks (Chapter 5 shows why that matters)", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Why the tick matters. <bookmark mark='a'/> When the tick is wide compared with the spread traders would "
            "accept and with the price's moves, the spread sits at one tick, the queues are long, and the price moves "
            "rarely, one tick at a time: priority is everything. <bookmark mark='b'/> When the tick is tiny, the price "
            "moves many ticks at once and traders compete on price. The American half-cent tick of Part thirty-five was "
            "aimed at the first kind of market. <bookmark mark='c'/> Bitcoin's perpetual is both at once: a one-tick "
            "spread, like the first, but when its mid changes between two snapshots a tenth of a second apart, the "
            f"median jump is {mv:.0f} ticks. Mathieu Rosenbaum and Khalil Dayri measured tick size by exactly this "
            "behaviour of the price, and by that measure the tick here is small. Chapter five shows why that matters."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"a queue of 5 BTC sits ahead of your new order of 1 BTC. Trades arrive at 0.2 BTC a second and "
                       r"cancellations remove 0.1 BTC a second from ahead of you. How long until you are filled?")
        with self.voiceover(
            "Pause and predict. Five bitcoin are queued ahead of your new one-bitcoin order. Trades eat two tenths of a "
            "bitcoin a second, and cancellations remove a tenth a second from ahead of you. How long until you are filled?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
