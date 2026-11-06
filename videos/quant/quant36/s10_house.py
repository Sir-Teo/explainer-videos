from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from explainer.quant.house import lob as L
from videos.quant.quant36.common import (BAD, GOOD, HURDLE, MICRO_C, NET_C, OFI_C, PART, SIM_C, house_lab, load)


class House(VoiceoverScene):
    def construct(self):
        self.answer()
        self.card()
        self.sheet(load("book"), load("micro"), load("memory"), load("ofi"), load("deep"), load("qr"), load("queue"))
        self.limits()
        self.lab()
        self.lab2()
        self.lab3()
        self.lab4()
        self.lab5()
        self.module()
        self.test()

    def answer(self):
        rows = [cmath(r"q^b \to 0,\ q^a\ \text{full}", r"\Rightarrow", r"I \approx 0", font_size=38),
                cmath(r"P^{\text{micro}}", r"<", r"M", font_size=42, colors={r"P^{\text{micro}}": MICRO_C}),
                cmath(r"\text{quote on } P^{\text{micro}}", r"\Rightarrow", r"\text{the bid steps back}", font_size=34,
                      colors={r"\text{the bid steps back}": GOOD})]
        whys = [why(r"an almost empty bid queue against a full offer: the imbalance is near zero"),
                why(r"the microprice leans down, toward the bid: about a third of a tick in a large-tick book, and "
                    r"by more on Bitcoin's"),
                why(r"a maker who centres quotes on the microprice lowers or cancels the bid before it is filled")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "The answer to the pause. <bookmark mark='a'/> An almost empty bid against a full offer is an imbalance "
            "near zero. <bookmark mark='b'/> The microprice leans down, toward the bid: about a third of a tick in a "
            "large-tick book, and more on Bitcoin's. <bookmark mark='c'/> It warned you. A maker who centres quotes on it would have lowered or "
            "cancelled the bid before the fill: that is the first defence against adverse selection."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def card(self):
        c = chapter_card(9, r"Rule 36: score the book against the spread", r"What must any order-book model show before "
                         r"the House uses it?", part=PART)
        with self.voiceover("Chapter nine. The House's thirty-sixth rule is about the book. Every signal from it is "
                            "small, fast and fragile, and a simulator of it can be wrong in ways that look like profit. "
                            "So the rule says what each must show."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def sheet(self, bk, m, me, o, d, q, z):
        days = bk["days"]
        one = min(x["one_tick"] for x in days.values())
        ups = [x["updates_per_s"] for x in days.values()]
        lo_u, hi_u = min(ups), max(ups)
        r10 = float(np.mean([r["r2"] for r in o["fits"]["10 s"]]))
        ten = [r for r in m["rows"] if r["h"] == "10 s"]
        st = float(np.mean([100 * (r["micro"] / r["mid"] - 1) for r in ten]))
        em = float(np.mean([100 * (1 - r["emp"] / r["mid"]) for r in ten]))
        h = me["hawkes"]
        rows = [(r"BTCUSDT perpetual: share of time at one tick; book updates a second",
                 rf"{100 * one:.1f}\%;\ {lo_u:.0f}\text{{--}}{hi_u:.0f}", GREY_A),
                (r"P(next move up), lowest and highest imbalance bucket",
                 rf"{100 * m['p_up'][0]:.0f}\%,\ {100 * m['p_up'][-1]:.0f}\%", MICRO_C),
                (r"trade arrivals: Hawkes branching ratio; sign-memory exponent",
                 rf"{h['branching']:.2f};\ {me['gamma']:.2f}", HURDLE),
                (r"OFI: $R^2$ over 10 s; slope of impact on depth", rf"{100 * r10:.0f}\%;\ {o['depth_slope']:.2f}", OFI_C),
                (r"10-s forecast error, test days: Stoikov, table of mean moves", rf"{st:+.0f}\%,\ {-em:+.0f}\%",
                 MICRO_C),
                (r"next-second direction, test days: linear, network",
                 rf"{100 * d['1 s']['linear']['test_acc']:.1f}\%,\ {100 * d['1 s']['network']['test_acc']:.1f}\%", NET_C),
                (r"simulator: kurtosis of 10-s changes, data and model",
                 rf"{q['data_train']['kurt_10s']:.0f},\ {q['model']['kurt_10s']:.1f}", SIM_C),
                (r"1-s markout of a passive fill, back and front of queue, ticks",
                 rf"{z['back']['markout']['1 s']:+.1f},\ {z['front']['markout']['1 s']:+.1f}", BAD)]
        hx = [-2.2, 4.8]
        tab = VGroup()
        for j, (txt, val, col) in enumerate(rows):
            y = 2.5 - 0.6 * j
            tab.add(VGroup(label(txt, font_size=16, color=col).move_to([hx[0], y, 0]),
                           MathTex(val, font_size=24).move_to([hx[1], y, 0])))
        title = label(r"The order-book desk's first sheet", font_size=28).to_edge(UP, buff=0.25)
        foot = wrapped_label(r"computed in this part from Binance's public best-quote stream and trade tape for the "
                             r"BTCUSDT perpetual, 16--21 May 2023; none is advice", 12.0, 15, GREY_A).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "The first sheet. <bookmark mark='a'/> A book that sits at one tick nearly all the time and updates a "
            "hundred times a second. Queues that predict the next tick. Trade arrivals that excite each other, and signs "
            "with long memory. Order-flow imbalance that explains much of the price change, with an impact close to one "
            "over depth. A microprice that overshoots on a small-tick book, and a plain table that does its job. A network that does not beat a "
            "linear rule. A simulator with tails far too thin. And passive fills that lose, badly at the back of the "
            "queue."
        ) as vo:
            self.play(FadeIn(title))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in tab], lag_ratio=0.4), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def limits(self):
        cards = VGroup(
            desk_question(r"one level, one venue, four days", r"the best quotes only, on one exchange's perpetual, in "
                          r"one week of May 2023: every number here is a measurement of that market, not a constant",
                          width=12.0, font_size=19),
            desk_question(r"snapshots, not events", r"a 100-ms grid hides what happened between snapshots; the order of "
                          r"events inside a step, and so some fills, are approximations", width=12.0, font_size=19),
            desk_question(r"no fees, no latency, no hidden size", r"the markouts ignore fees and rebates, assume the "
                          r"order arrives instantly, and see only displayed size", width=12.0, font_size=19),
        ).arrange(DOWN, buff=0.25)
        head = label(r"What this part did not measure", font_size=28).to_edge(UP, buff=0.4)
        if cards.height > 6.0:
            cards.scale_to_fit_height(6.0)
        cards.next_to(head, DOWN, buff=0.3)
        with self.voiceover(
            "What this part did not measure, so that nobody quotes it for more than it is. <bookmark mark='a'/> The best "
            "quotes only, on one exchange, in four days of one week: every number is a measurement of that market, not "
            "a constant of nature. <bookmark mark='b'/> Snapshots a tenth of a second apart, not every event: what "
            "happens inside a step is approximated. <bookmark mark='c'/> And no fees, no latency, no hidden size. The "
            "House writes these limits next to the numbers, every time."
        ) as vo:
            self.play(FadeIn(head))
            for k_, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k_], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def lab(self):
        card = house_lab(r"Order-flow imbalance", L.ofi, "e = np.zeros", 4, width=10.6)
        card.move_to(ORIGIN)
        with self.voiceover(
            "Chapter four's definition in one expression. For the bid, the new size if the bid rose or stayed, less the "
            "old size if it fell or stayed; for the ask, the mirror image, subtracted. Every term is a whole queue or "
            "nothing, which is why it captures additions and cancellations without seeing a single order."
        ):
            self.play(FadeIn(card))
            self.wait(1.5)
        self.clear_scene()

    def lab2(self):
        card = house_lab(r"Stoikov's microprice", L.microprice_fit, "A = np.linalg.inv", 11, width=10.6)
        card.move_to(ORIGIN)
        with self.voiceover(
            "Chapter five's estimator. Invert one minus the no-move matrix, which sums over the steps before the mid "
            "moves. That gives the first expected change and the state after it. Then add the expected change at every "
            "later move, four hundred terms, and record how much the last two hundred changed the answer: on our fit, "
            "nothing at all."
        ):
            self.play(FadeIn(card))
            self.wait(1.5)
        self.clear_scene()

    def lab3(self):
        card = house_lab(r"The queue-reactive simulator", L.qr_simulate, "for t in range(n):", 16, width=10.6)
        card.move_to(ORIGIN)
        with self.voiceover(
            "Chapter seven's simulator. Each step, each queue grows or shrinks by one unit with the probabilities "
            "fitted to its current size. When one empties, the mid moves half a tick that way and both queues are "
            "redrawn from the data. The scorecard's failures are visible in the code: the rates look only at the "
            "current queue, and nothing moves more than one unit."
        ):
            self.play(FadeIn(card))
            self.wait(1.5)
        self.clear_scene()

    def lab4(self):
        card = house_lab(r"Replaying a passive order", L.queue_fills, "if at_p > ahead + 1e-12 or through:", 13,
                         width=10.6)
        card.move_to(ORIGIN)
        with self.voiceover(
            "And Chapter eight's replay. A trade at our price larger than the queue ahead fills us, as does any trade "
            "through our price. Otherwise the trades eat the queue ahead, net cancellations are taken in proportion, and "
            "if the level vanishes we are alone at the front."
        ):
            self.play(FadeIn(card))
            self.wait(1.5)
        self.clear_scene()

    def lab5(self):
        card = house_lab(r"The table that worked", L.horizon_fit, "ok = (S[:-horizon] >= 1)", 11, width=10.6)
        card.move_to(ORIGIN)
        with self.voiceover(
            "And Chapter five's humble winner. For every snapshot with a usable spread, take the state and the mid's "
            "change over the horizon; mirror the data so the table is antisymmetric; and average by state. No chain, no "
            "limit, no theorem: an honest conditional mean, fitted for the horizon at which it will be used."
        ):
            self.play(FadeIn(card))
            self.wait(1.5)
        self.clear_scene()

    def module(self):
        chart = house_chart(PART, lit=("data", "research")).scale(0.62).to_edge(UP, buff=0.2)
        rows = [
            (r"\texttt{data.binance\_book\_day}, \texttt{data.binance\_aggtrades\_day}", r"best quotes, trade tape"),
            (r"\texttt{mid}, \texttt{imbalance}, \texttt{weighted\_mid}, \texttt{ofi}", r"features"),
            (r"\texttt{microprice\_fit}, \texttt{microprice\_apply}, \texttt{forecast\_mse}", r"the microprice"),
            (r"\texttt{sign\_acf}, \texttt{signature}", r"memory"),
            (r"\texttt{qr\_fit}, \texttt{qr\_simulate}, \texttt{queue\_fills}", r"simulation, fills"),
        ]
        tab = VGroup(*[VGroup(label(a_, font_size=15, color=QC.HOUSE), label(b_, font_size=15, color=GREY_A)).arrange(
            RIGHT, buff=0.4) for a_, b_ in rows]).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        for r_ in tab:
            r_[1].align_to(tab, LEFT).shift(RIGHT * 9.6)
        tab.next_to(chart, DOWN, buff=0.25)
        if tab.width > 13.0:
            tab.scale_to_fit_width(13.0)
        rule = wrapped_label(r"Rule 36: an order-book signal is scored on days it never saw, against the mid and a linear "
                             r"rule, and in ticks against the spread it must pay; a simulator ships with its stylised-fact "
                             r"scorecard and is used only where it passes; and every passive fill is marked out at one, ten "
                             r"and sixty seconds.", 12.4, 17, QC.HOUSE).to_edge(DOWN, buff=0.2)
        with self.voiceover(
            "The tools this part adds. <bookmark mark='a'/> Two loaders for the best-quote stream and the trade tape; the "
            "features; the microprice; memory; and the simulator with the replay of fills. <bookmark mark='b'/> And the "
            "thirty-sixth rule. An order-book signal is scored on days it never saw, against the mid and a linear rule, "
            "and in ticks against the spread it must pay. A simulator ships with its scorecard and is used only where it "
            "passes. And every passive fill is marked out at one, ten and sixty seconds."
        ) as vo:
            self.play(FadeIn(chart))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab], lag_ratio=0.4, run_time=4))
            vo.wait_until("b")
            self.play(FadeIn(rule))
        self.wait(0.4)
        self.clear_scene()

    def test(self):
        cards = VGroup(
            desk_question(r"the paper with 85\% accuracy on FI-2010", r"ask for another market and another year, the "
                          r"linear baseline, and the profit after the spread (Chapter 6)", width=12.0, font_size=19),
            desk_question(r"the execution algorithm tuned in a simulator", r"ask for the simulator's scorecard, and "
                          r"whether the price reacts to the algorithm's own orders (Chapter 7)", width=12.0, font_size=19),
            desk_question(r"the maker who reports a high fill rate", r"ask for the markouts: a high fill rate at the back "
                          r"of the queue is a measure of being picked off (Chapter 8)", width=12.0, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "The rule against three cases. <bookmark mark='a'/> A paper with eighty-five percent accuracy on the "
            "benchmark: ask for another market and another year, the linear baseline, and the profit after the spread. "
            "<bookmark mark='b'/> An execution algorithm tuned in a simulator: ask for the scorecard, and whether the "
            "price reacts to the algorithm's own orders. <bookmark mark='c'/> A maker proud of a high fill rate: ask for "
            "the markouts. At the back of the queue, a high fill rate measures how often you were picked off."
        ) as vo:
            for k_, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k_], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()
