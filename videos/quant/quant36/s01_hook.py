from __future__ import annotations

import math

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant36.common import (ASK_C, BID_C, MICRO_C, MID_C, PART, era_strip,
                                         load)


class Hook(VoiceoverScene):
    def construct(self):
        self.title_card()
        self.question()
        self.claims(load("micro"), load("ofi"), load("deep"))
        self.stakes()
        self.act()
        self.history()
        self.objectives()
        self.house()

    def title_card(self):
        card = part_title(PART, r"The Limit Order Book")
        disc = note(DISCLAIMER, font_size=18, color=GREY_C).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Part thirty-six. The limit order book: the queues of resting orders that every electronic market is made of, "
            "and what they say about the next price."
        ):
            self.play(FadeIn(card, shift=UP * 0.2), FadeIn(disc))
        self.play(FadeOut(card), FadeOut(disc))

    def question(self):
        bid = VGroup(Rectangle(width=5.0, height=0.6, fill_color=BID_C, fill_opacity=0.7, stroke_width=0),
                     label(r"bid \$100.00, 500 shares", font_size=20)).arrange(DOWN, buff=0.15)
        ask = VGroup(Rectangle(width=1.0, height=0.6, fill_color=ASK_C, fill_opacity=0.7, stroke_width=0),
                     label(r"ask \$100.01, 100 shares", font_size=20)).arrange(DOWN, buff=0.15)
        bid.move_to(LEFT * 3 + UP * 0.6)
        ask.move_to(RIGHT * 3 + UP * 0.6)
        I = 500 / 600
        wm = 100 + 0.01 * I
        p_up = 1 - 2 / math.pi * math.atan(100 / 500)
        ex = 100.005 + (2 * p_up - 1) * 0.005
        rows = VGroup(label(r"the mid: \$100.005", font_size=22, color=MID_C),
                      label(rf"the size-weighted mid: \${wm:.4f}", font_size=22, color=GREY_A),
                      label(rf"a queue model's next mid: \${ex:.4f}", font_size=22, color=MICRO_C))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to(DOWN * 1.7)
        with self.voiceover(
            "A question asked in trading interviews. <bookmark mark='a'/> The best bid is a hundred dollars for five "
            "hundred shares; the best offer a hundred dollars and one cent, for only a hundred. Where is fair value? "
            "<bookmark mark='b'/> The mid says a hundred and half a cent. But the small queue at the offer will probably "
            "be eaten first, and then the price ticks up. <bookmark mark='c'/> The size-weighted mid and a queue model "
            "both put fair value near the offer. This part measures which is right, on Bitcoin's book."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(bid), FadeIn(ask))
            vo.wait_until("b")
            self.play(FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1:]))
        self.wait(0.4)
        self.clear_scene()

    def claims(self, m, o, d):
        r = [x for x in m["rows"] if x["h"] == "10 s"]
        gain = 100 * np.mean([1 - x["emp"] / x["mid"] for x in r])
        lean = abs(m["g"][9] / m["tick"])
        r2 = o["fits"]["10 s"][0]["r2"]
        net = d["1 s"]["network"]["test_acc"]
        lin = d["1 s"]["linear"]["test_acc"]
        cards = VGroup(
            desk_question(r"the queues predict the next tick", rf"the probability that the next move is up rises from "
                          rf"{100 * m['p_up'][0]:.0f}\% to {100 * m['p_up'][-1]:.0f}\% with the bid's share of the best "
                          rf"queues; but Stoikov's microprice, built for large-tick books, leans {lean:.0f} ticks and "
                          rf"overshoots, while a table of mean moves cuts the ten-second error by {gain:.0f}\% on unseen "
                          r"days",
                          width=12.4, font_size=19),
            desk_question(r"order-flow imbalance moves the price", rf"over ten seconds it explains {100 * r2:.0f}\% of "
                          r"mid changes, with an impact that falls as one over depth", width=12.4, font_size=19),
            desk_question(r"deep models, honestly", rf"a network on recent book states predicts the next second's direction "
                          rf"{100 * net:.0f}\% of the time on unseen days, against {100 * lin:.0f}\% for a linear rule",
                          width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "What this part finds. <bookmark mark='a'/> The queues predict the next tick: the chance that the next move "
            f"is up rises from {100 * m['p_up'][0]:.0f} percent to {100 * m['p_up'][-1]:.0f} with the bid's share of the "
            f"best queues. But Stoikov's microprice, built for large-tick books, leans {lean:.0f} ticks on Bitcoin and "
            "overshoots, while a plain table of mean moves cuts the ten-second forecast error by "
            f"{gain:.0f} percent on days it never saw. <bookmark mark='b'/> Order-flow imbalance moves the price: over ten seconds it explains "
            f"{100 * r2:.0f} percent of mid changes. <bookmark mark='c'/> And deep learning, honestly measured: a "
            f"network gets the next second's direction right {100 * net:.0f} percent of the time on unseen days, a linear "
            f"rule {100 * lin:.0f}."
        ) as vo:
            for k_, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k_], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def stakes(self):
        cards = VGroup(
            desk_question(r"every strategy trades through a book", r"the monthly factor portfolios of Parts 24 to 33 "
                          r"still buy and sell at the bid and the offer; their costs in Part 31 were the book's prices",
                          width=12.4, font_size=19),
            desk_question(r"the fastest desks live in it", r"market makers and high-frequency traders earn or lose "
                          r"fractions of a tick, millions of times a day, on exactly the quantities this part measures",
                          width=12.4, font_size=19),
            desk_question(r"and it is where models meet reality", r"a fair price, a forecast, a simulator: each can be "
                          r"tested here within days, on millions of observations, which makes the book a laboratory "
                          r"for honest research", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Why it matters, even to a slow investor. <bookmark mark='a'/> Every strategy in this series trades through "
            "a book: the monthly factor portfolios still buy at the offer and sell at the bid, and Part thirty-one's "
            "costs were the book's prices. <bookmark mark='b'/> The fastest desks live in it, earning or losing "
            "fractions of a tick millions of times a day. <bookmark mark='c'/> And it is where models meet reality "
            "fastest: a fair price, a forecast or a simulator can be tested on millions of observations within days. "
            "That makes the book a laboratory for honest research, and this part uses it as one."
        ) as vo:
            for k_, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k_], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def act(self):
        smap = series_map(current=PART, done=PART - 1)
        with self.voiceover(
            "Where this sits. Part thirty-five asked who trades with whom. This part opens the mechanism they trade "
            "through: the order book, with its queues, ticks and cancellations. It builds the House's order-book "
            "simulator, which execution in Part thirty-seven and market making in Part thirty-eight will use."
        ):
            self.play(FadeIn(smap))
            self.wait(1.0)
        self.clear_scene()

    def history(self):
        I = QC.IDEA
        entries = [(2004, r"order-sign memory", I), (2010, r"queue models", I), (2013, r"near-critical Hawkes", I),
                   (2014, r"order-flow imbalance", I), (2015, r"queue-reactive model", I), (2018, r"the microprice", I),
                   (2019, r"DeepLOB; universal features", I), (2023, r"generative order books", I),
                   (2024, r"LOBCAST", I)]
        strip = era_strip(entries, y0=2000, y1=2027, font_size=12, step=5).move_to(DOWN * 0.3)
        head = label(r"Twenty years of order-book research", font_size=34).to_edge(UP, buff=0.6)
        groups = [(0, 3), (3, 6), (6, 9)]
        with self.voiceover(
            "Twenty years of the field. Fabrizio Lillo and Doyne Farmer found that order signs have long memory in 2004; "
            "Rama Cont and co-authors modelled queues in 2010; and the self-exciting arrivals of orders were found to be "
            "close to critical. <bookmark mark='a'/> Then the order-flow imbalance, the queue-reactive model, and Sasha "
            "Stoikov's microprice. <bookmark mark='b'/> And deep learning: DeepLOB, universal features, generative "
            "models of the book, and a benchmark that tested how well any of it generalises."
        ) as vo:
            self.play(FadeIn(head), Create(strip[0]), FadeIn(strip[1]))
            for (a, b), mk in zip(groups, [None, "a", "b"]):
                if mk:
                    vo.wait_until(mk)
                self.play(LaggedStart(*[FadeIn(strip.items[i], shift=UP * 0.1) for i in range(a, b)], lag_ratio=0.3),
                          run_time=1.6)
        self.wait(0.4)
        self.clear_scene()

    def objectives(self):
        card = objectives_card([
            r"The book: price-time priority, ticks and queues, measured on Bitcoin",
            r"Queues and the next tick: a model, and the data",
            r"Events that cause events: Hawkes clustering, order-sign memory, the signature plot",
            r"Order-flow imbalance and depth",
            r"The microprice, fitted and tested out of sample",
            r"Deep order books, and a generative book of our own with its scorecard",
            r"For the researcher: the microprice theorem, proved, and where it holds",
        ], color=QC.IDEA)
        with self.voiceover(
            "The plan: the book itself, measured on Bitcoin's perpetual future; queues and the next tick, in a model and "
            "in the data; the clustering of events and the memory of order signs; order-flow imbalance; the microprice, "
            "fitted and tested; deep models of the book, and a generative book of the House's own with a scorecard; "
            "trading in the queue; and the microprice theorem, proved."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in card.rows],
                                                     lag_ratio=0.5, run_time=12))
        self.play(FadeOut(card))

    def house(self):
        chart = house_chart(PART, lit=("data", "research"))
        with self.voiceover(
            "In the House, the data desk gains the best quotes on a hundred-millisecond grid, and the research desk an "
            "order-book simulator: the laboratory in which the next two parts will trade."
        ):
            self.play(FadeIn(chart))
        self.wait(0.3)
        self.clear_scene()
