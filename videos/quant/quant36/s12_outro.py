from __future__ import annotations

import math

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant36.common import (BAD, GOOD, HURDLE, MICRO_C, NET_C, OFI_C, PART, SIM_C, load)

DESK = [
    (r"What is order-flow imbalance, and why does it beat signed trades?",
     r"the net change in the best queues from adds, cancels and trades; limit orders carry as much information as "
     r"trades, and the response to OFI is close to linear"),
    (r"Why does a queue imbalance predict the next tick?",
     r"with a one-tick spread the price moves when a best queue empties, and the shorter queue tends to empty first"),
    (r"What is the microprice, and when can you trust it?",
     r"the expected mid after many future mid changes, given the state: a martingale under a Markov, symmetric book; "
     r"trust it on large-tick books, test it on small-tick ones"),
    (r"Why is the weighted mid not a fair price?",
     r"it jumps toward the thin side and partly back after the tick, so its changes are predictable"),
    (r"Why is a fill at the back of the queue bad news?",
     r"it happens when the whole queue ahead has been eaten, usually just before the price goes through"),
    (r"How would you score an order-book simulator?",
     r"on stylised facts out of sample: move rate, burstiness, sign memory, fat tails, queue sizes, and its reaction to "
     r"the user's own orders"),
]

PROBLEMS = [
    r"A queue of 5 BTC ahead; trades 0.2 BTC/s, cancels 0.1 BTC/s from ahead. Time to the front, and to fill 1 BTC.",
    r"Queues of 9 and 3: the up-tick probability under Cont--de Larrard and under ``probability = imbalance''.",
    r"Hawkes: background 2/s, branching 0.68, then 0.95. Mean rates; the share of events that are endogenous.",
    r"Signs with ACF $\propto \ell^{-0.85}$: why the variance of the sum of $n$ signs grows faster than $n$.",
    r"OFI of $+12$ BTC against queues of 8 BTC, tick \$0.10: the mid move under the stylised model.",
    r"Bid 500, ask 100, tick \$0.01: the mid, the weighted mid, and the direction of the microprice's lean.",
    r"A network and a linear rule: 84\% and 87\% direction accuracy, $R^2$ under 1\%. What to report to a PM.",
    r"A simulator with no memory: which of the five scorecard facts can it match, and why not the others?",
    r"Back of a 7.6-BTC queue, fill rate 82\%, 1-s markout $-15$ ticks, spread 1 tick: the P\&L per order.",
    r"A maker cancels whenever the microprice leans against it. What happens to its fill rate and markout?",
    r"(qual) Prove that under H1--H3, $g = \sum_k B^k g^1$ converges geometrically, equals "
    r"$(\mathbb 1 - B + \mathbb 1\pi^\top)^{-1} g^1$, and makes $M + g(X)$ the unique antisymmetric martingale of that form.",
    r"(qual) Two states with $\Pr(+1 \mid \text{bid-heavy}) = q$ and persistence $p$: derive $g = (2q - 1)/(2(1 - p))$ "
    r"ticks, and show $g \to \infty$ as $p \to 1$; relate this to Bitcoin's $|\lambda_2| = 0.67$.",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.recap(load("book"), load("micro"), load("memory"), load("ofi"), load("deep"), load("qr"), load("queue"),
                   load("research"))
        self.lessons()
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

    def recap(self, bk, m, me, o, d, q, z, r):
        r10 = float(np.mean([x["r2"] for x in o["fits"]["10 s"]]))
        items = [
            (r"the book: price-time priority, one-tick spreads, queues that refill", GREY_A),
            (rf"queue imbalance moves P(up) from {100 * m['p_up'][0]:.0f}\% to {100 * m['p_up'][-1]:.0f}\%; "
             r"Cont--de Larrard is too steep", MICRO_C),
            (rf"trades excite trades (branching {me['hawkes']['branching']:.2f}); signs remember "
             rf"($\ell^{{-{me['gamma']:.2f}}}$)", HURDLE),
            (rf"OFI explains {100 * r10:.0f}\% of 10-s mid changes; impact $\propto$ depth$^{{{o['depth_slope']:.2f}}}$",
             OFI_C),
            (r"the weighted mid is not a martingale; Stoikov's microprice is, in theory", MICRO_C),
            (rf"on Bitcoin the microprice leans {abs(m['g'][9] / m['tick']):.0f} ticks and overshoots; a table of mean "
             r"moves works", BAD),
        ]
        items2 = [
            (r"DeepLOB, universal features, LOBCAST: the benchmark gains shrink on new data", NET_C),
            (rf"our network: {100 * d['1 s']['network']['test_acc']:.0f}\% against a linear "
             rf"{100 * d['1 s']['linear']['test_acc']:.0f}\% on unseen days", NET_C),
            (rf"a queue-reactive simulator: one fact right, four wrong (kurtosis {q['model']['kurt_10s']:.1f} against "
             rf"{q['data_train']['kurt_10s']:.0f})", SIM_C),
            (rf"back-of-queue fills: {z['back']['markout']['1 s']:+.0f} ticks after a second; the front is worth most "
             r"of the difference", BAD),
            (r"a limit order is a free option written to the market", HURDLE),
            (r"Rule 36: score the book against the spread", QC.HOUSE),
            (rf"research: the microprice theorem; it holds in the simulator, and on Bitcoin reaches "
             rf"{max(r['btc']['beta']):.2f}", GOOD),
        ]
        head, rows = self._rows(list(enumerate(items, 1)), r"Part 36 in thirteen lines")
        with self.voiceover(
            "Part thirty-six in thirteen lines. The book is queues at prices, served first come, first served. The "
            "balance of the two best queues predicts the next tick, less sharply than the random-walk race says. Trades "
            "excite trades, and order signs remember. Order-flow imbalance explains much of each price change. The "
            "weighted mid is not a fair price; Stoikov's microprice is, in theory, but on Bitcoin's small-tick book it "
            "overshoots, and a plain table of mean moves does its job."
        ):
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows], lag_ratio=0.6,
                                                run_time=18))
        self.wait(0.5)
        self.clear_scene()
        head, rows = self._rows(list(enumerate(items2, 7)), r"Part 36 in thirteen lines")
        with self.voiceover(
            "Deep models of the book lose much of their benchmark edge on new data, and ours did not beat a linear rule. "
            "Our simulator matched the queues and missed the clustering. Passive fills at the back of the queue are "
            "picked off, because a limit order is a free option. And the research chapter proved the microprice "
            "theorem, then found where its hypotheses hold."
        ):
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows], lag_ratio=0.6,
                                                run_time=16))
        self.wait(0.5)
        self.clear_scene()

    def lessons(self):
        cards = VGroup(
            desk_question(r"check the hypotheses, not only the proof", r"the microprice theorem is correct; Bitcoin's book "
                          r"is not the book it assumes, and a direct test of the Markov property says so before any "
                          r"forecast is made", width=12.4, font_size=19),
            desk_question(r"baselines first", r"the imbalance alone, a linear rule and a table of mean moves did as well "
                          r"as or better than the network and the theory; every claim was scored against them",
                          width=12.4, font_size=19),
            desk_question(r"measure in the units you pay", r"ticks against a one-tick spread, markouts per fill: a "
                          r"high accuracy, a high fill rate or a converging series can all be worth nothing",
                          width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Three lessons to take from this part. <bookmark mark='a'/> Check the hypotheses, not only the proof. The "
            "microprice theorem is correct, but Bitcoin's book is not the book it assumes, and a direct test of the "
            "Markov property says so before any forecast is made. <bookmark mark='b'/> Baselines first: the imbalance "
            "alone, a linear rule and a plain table did as well as the network and the theory. <bookmark mark='c'/> "
            "And measure in the units you pay: ticks against the spread, markouts per fill. A high accuracy, a high fill "
            "rate and a converging series can each be worth nothing."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def desk(self):
        def page(qs):
            cards = VGroup(*[desk_question(q_, a_, width=12.4, font_size=20) for q_, a_ in qs]).arrange(DOWN, buff=0.22)
            if cards.height > 7.4:
                cards.scale_to_fit_height(7.4)
            return cards
        cards = page(DESK[:3])
        with self.voiceover(
            "Six desk questions. What is order-flow imbalance? The net change of the best queues, from every kind of "
            "event. <bookmark mark='a'/> Why does queue imbalance predict the next tick? The short queue empties first. "
            "<bookmark mark='b'/> What is the microprice, and when can you trust it? On large-tick books, and after "
            "testing."
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
            "Why is the weighted mid not a fair price? Its changes are predictable. <bookmark mark='a'/> Why is a fill "
            "at the back of the queue bad news? It comes just before the price goes through. <bookmark mark='b'/> And "
            "how would you score a simulator? On stylised facts, out of sample, and on how it reacts to your own "
            "orders. Full solutions are in the notes."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[2], shift=UP * 0.2))
        self.wait(0.5)
        self.clear_scene()

    def answers(self):
        t_front = 5 / (0.2 + 0.1)
        t_fill = t_front + 1 / 0.2
        p_cdl = 1 - 2 / math.pi * math.atan(3 / 9)
        mean1 = 2 / (1 - 0.68)
        mean2 = 2 / (1 - 0.95)
        lean = (2 * 0.75 - 1) / (2 * (1 - 0.75))
        cards = VGroup(
            desk_question(r"Ch.~1: 5 BTC ahead", rf"ahead shrinks at 0.3 BTC/s: the front in {t_front:.1f} s; your own "
                          rf"1 BTC then takes 5 s more of trades, {t_fill:.1f} s in all", width=12.4, font_size=19),
            desk_question(r"Ch.~2: queues of 9 and 3", rf"Cont--de Larrard: $1 - \frac{{2}}{{\pi}}\arctan\frac13 = "
                          rf"{p_cdl:.3f}$; the imbalance rule: 0.75; the data sit nearer the second", width=12.4,
                          font_size=19),
            desk_question(r"Ch.~3: Hawkes, $\mu = 2$", rf"mean rate $\mu/(1 - n)$: {mean1:.2f} a second; at $n = 0.95$, "
                          rf"{mean2:.0f}, of which 95\% are triggered by other events", width=12.4, font_size=19),
            desk_question(r"Research: two states", rf"$g^1 = \frac12$ tick and $B$ has eigenvalue $2p - 1$ on it, so "
                          rf"$g = \frac{{1/2}}{{2(1 - p)}}$: {lean:.0f} tick at $p = \frac34$, unbounded as $p \to 1$",
                          width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.2)
        if cards.height > 7.3:
            cards.scale_to_fit_height(7.3)
        with self.voiceover(
            "The remaining pause questions, answered. Five bitcoin ahead shrink at three tenths a second: the front in "
            f"{t_front:.1f} seconds, filled after {t_fill:.1f}. <bookmark mark='a'/> With queues of nine and three, Cont "
            f"and de Larrard say {p_cdl:.2f}, the imbalance rule three-quarters, and the data sit nearer the second. "
            f"<bookmark mark='b'/> The Hawkes process averages {mean1:.2f} trades a second; at a branching ratio of "
            f"point nine five, {mean2:.0f}, nearly all of them triggered by other trades. <bookmark mark='c'/> And the "
            f"two-state microprice leans {lean:.0f} tick when p is three-quarters, and without bound as p goes to one: "
            "persistence after moves is exactly what inflates the lean, and what Bitcoin's chain overstates."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            for k_, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k_ + 1], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=18)
        with self.voiceover(
            "And twelve problems: time in the queue; the up-tick probability; Hawkes rates; sign memory; impact from "
            "order-flow imbalance; the interview book; reporting a network honestly; a simulator without memory; the "
            "profit of a back-of-queue order; and a maker who cancels on the microprice. Then two qualifying-exam "
            "problems: the microprice theorem in full, and the two-state book. Solutions, in English and Chinese, are in "
            "the notes."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r_) for r_ in ps.rows], lag_ratio=0.3, run_time=5))
            self.wait(3)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"impact and the optimal schedule of a large order", [37]),
            (r"market making with the microprice, inventory and queue position", [38]),
            (r"the order book of a decentralised exchange: the automated market maker", [39]),
            (r"simulators and learning agents in markets", [42]),
        ])
        with self.voiceover(
            "Where this comes back. Part thirty-seven measures the impact of large orders and schedules them. Part "
            "thirty-eight makes markets with the microprice, inventory and queue position. Part thirty-nine meets a book "
            "with no queues at all, the automated market maker. And Part forty-two puts learning agents into "
            "simulated markets like this one."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r_) for r_ in card.rows], lag_ratio=0.4, run_time=4))
        self.wait(0.4)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"Bouchaud, Bonart, Donier and Gould, \textit{Trades, Quotes and Prices} (2018); Cartea, Jaimungal and "
             r"Penalva, \textit{Algorithmic and High-Frequency Trading} (2015); Abergel, Anane, Chakraborti, Jedidi and "
             r"Toke, \textit{Limit Order Books} (2016); Gould et al., ``Limit order books'' (2013)"],
            [r"Lillo and Farmer (2004); Cont, Stoikov and Talreja (2010); Avellaneda, Reed and Stoikov (2011); Cont and "
             r"de Larrard (2013); Hardiman, Bercot and Bouchaud (2013); Cont, Kukanov and Stoikov (2014); Huang, Lehalle "
             r"and Rosenbaum (2015); Gould and Bonart (2016); Moallemi and Yuan (2017); Stoikov (2018); Xu, Gould and "
             r"Howison (2018)",
             r"Copeland and Galai (1983); Ntakaris et al.\ (2018); Sirignano and Cont (2019); Zhang, Zohren and Roberts "
             r"(2019); Byrd, Hybinette and Balch (2020); Vyetrenko et al.\ (2020); Coletta et al.\ (2021); Kolm, Turiel "
             r"and Westray (2023); Nagy et al.\ (2023); Prata et al.\ (2024). Data: Binance's public archive"])
        with self.voiceover(
            "The textbooks this part follows, Bouchaud and co-authors' Trades, Quotes and Prices above all, and the "
            "papers it draws on, from Lillo and Farmer to the benchmark that retested the deep models. Every number on "
            "screen was computed by the House's code from Binance's public best-quote stream and trade tape, or from "
            "the House's own simulator."
        ):
            self.play(FadeIn(card))
            self.wait(3)
        self.clear_scene()

    def house(self):
        chart = house_chart(PART, lit=("data", "research"))
        smap = series_map(current=PART + 1, done=PART)
        nxt = label(r"Next: Part 37, Market Impact and Execution", font_size=30, color=QC.IDEA).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The House can now read the book: its queues, its flow, its fair price where one exists, and the cost of "
            "waiting in line. <bookmark mark='a'/> Next, Part thirty-seven: market impact and execution. How much a "
            "large order moves the price, why the cost grows like a square root, and how to schedule a trade so that it "
            "costs the least."
        ) as vo:
            self.play(FadeIn(chart))
            vo.wait_until("a")
            self.play(FadeOut(chart), FadeIn(smap), FadeIn(nxt))
        self.wait(1.0)
        self.clear_scene()
