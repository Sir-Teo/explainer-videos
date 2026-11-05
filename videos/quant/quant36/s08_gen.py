from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant36.common import (BAD, GOOD, PART, SIM_C, fit_right, load)


class Gen(VoiceoverScene):
    def construct(self):
        q = load("qr")
        self.card()
        self.why_sim()
        self.literature()
        self.zero_intelligence()
        self.rates(q)
        self.path(q)
        self.scorecard(q)
        self.diagnosis(q)
        self.realism()
        self.question()

    def card(self):
        c = chapter_card(7, r"A book of our own", r"Can a model generate an order book that behaves like the real one?",
                         part=PART)
        with self.voiceover("Chapter seven. The answer to the pause is no, and this chapter shows why. A forecast says "
                            "what happens next; a simulator must produce whole days that behave like the real market. "
                            "That is a much harder test, and the next two parts need one."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def why_sim(self):
        cards = VGroup(
            desk_question(r"replay is not enough", r"a historical book cannot react: an order you add in a replay never "
                          r"moves the price, never takes a place in the queue and is never picked off", width=12.4,
                          font_size=19),
            desk_question(r"what a simulator is for", r"testing execution and market-making algorithms, stress "
                          r"scenarios that never happened, and training reinforcement learners (Part 8) without "
                          r"trading real money", width=12.4, font_size=19),
            desk_question(r"the risk", r"an algorithm tuned on a simulator learns the simulator: any fact it gets wrong "
                          r"becomes a profit that does not exist", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Why build one. <bookmark mark='a'/> Replaying history is not enough: an order added to a replay never moves "
            "the price, never queues and is never picked off. <bookmark mark='b'/> A simulator lets the desk test "
            "execution and market making, run stresses that never happened, and train the reinforcement learners of "
            "Part eight without risking money. <bookmark mark='c'/> The danger is the mirror image: an algorithm tuned on "
            "a simulator learns the simulator, and every fact the simulator gets wrong becomes a profit that does not "
            "exist."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def literature(self):
        cards = VGroup(
            desk_question(r"queue-reactive and Hawkes models", r"Huang, Lehalle and Rosenbaum (2015); Hawkes-driven "
                          r"books: rates estimated from data, interpretable, fast", width=12.4, font_size=18),
            desk_question(r"agent-based markets", r"ABIDES (Byrd, Hybinette and Balch, 2020): many simulated traders "
                          r"with strategies, meeting in a matching engine", width=12.4, font_size=18),
            desk_question(r"deep generative books", r"Coletta et al. (2021), a conditional GAN of order flow; Nagy et "
                          r"al. (2023), a token-by-token generator of every message, in the manner of a language model",
                          width=12.4, font_size=18),
            desk_question(r"realism metrics", r"Vyetrenko et al. (2020): score a simulator on a list of stylised facts "
                          r"of real books, not on its likelihood", width=12.4, font_size=18),
        ).arrange(DOWN, buff=0.2)
        with self.voiceover(
            "Four families. <bookmark mark='a'/> Statistical models, the queue-reactive model and Hawkes-driven books: "
            "rates read from data, interpretable and fast. <bookmark mark='b'/> Agent-based markets such as ABIDES, "
            "where simulated traders with strategies meet in a matching engine. <bookmark mark='c'/> Deep generative "
            "books: a conditional adversarial network of order flow, and Peer Nagy and colleagues' generator, which "
            "writes the message stream token by token, the way a language model writes text. <bookmark mark='d'/> And "
            "how to judge any of them: Svitlana Vyetrenko and colleagues proposed scoring a simulator on a list of the "
            "real book's stylised facts. We do that next."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c", "d")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def zero_intelligence(self):
        rows = [cmath(r"\text{orders}", r"\sim", r"\text{Poisson, at random prices}", font_size=38),
                cmath(r"\text{spread}", r"\sim", r"\frac{\mu}{\alpha}\,f\!\left(\frac{\delta\,\alpha^2}{\mu\,\sigma}\right)",
                      font_size=36, colors={r"\text{spread}": SIM_C}),
                cmath(r"\text{lesson}", r":", r"\text{mechanics explain much; strategy explains the rest}", font_size=30)]
        whys = [why(r"Smith, Farmer, Gillemot and Krishnamurthy (2003): limit orders, market orders and cancellations "
                    r"arrive at random, with no intelligence at all"),
                why(r"dimensional analysis: market-order rate $\mu$, limit-order rate density $\alpha$, cancellation rate "
                    r"$\delta$ and order size $\sigma$ fix the spread up to a function of one number"),
                why(r"Farmer, Patelli and Zovko (2005): on London stocks the random model predicted much of how the "
                    r"average spread varies across stocks; what it missed is where strategy lives")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "The simplest simulator of all has no traders in it. <bookmark mark='a'/> Eric Smith, Doyne Farmer and "
            "colleagues let orders arrive at random, at random prices, and cancel at random. <bookmark mark='b'/> "
            "Dimensional analysis then fixes the spread from four rates, up to a function of a single number. "
            "<bookmark mark='c'/> On London stocks, this zero-intelligence model predicted much of how the average "
            "spread differs from stock to stock. The mechanics of the book explain a lot; what they miss is where "
            "strategy, and information, live."
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

    def rates(self, q):
        pu = 10 * np.asarray(q["p_up"], float)
        pd = 10 * np.asarray(q["p_dn"], float)
        n = 16
        xs = np.arange(1, n)
        top = float(np.ceil(max(pu[1:n].max(), pd[1:n].max()) * 2) / 2)
        g = axes([0, n], [0, top], x_length=6.4, y_length=4.4, xlabel=rf"best queue size, units of {q['unit']:.1f} BTC",
                 ylabel=r"events per second", xticks=[0, 5, 10, 15], yticks=[0, top / 2, top], yfmt=lambda v: f"{v:.1f}",
                 font_size=15).move_to(LEFT * 1.6 + DOWN * 0.2)
        ax = g.ax
        cu = curve(ax, xs, pu[1:n], GOOD, stroke_width=3)
        cd = curve(ax, xs, pd[1:n], BAD, stroke_width=3)
        leg = legend([(GOOD, r"the queue grows (adds)"), (BAD, r"the queue shrinks (cancels, trades)")],
                     font_size=16).to_edge(RIGHT, buff=0.3).shift(UP * 1.6)
        fit_right(leg)
        rf = np.asarray(q["refill"], float)
        k_med = int(np.searchsorted(np.cumsum(rf), 0.5)) + 1
        p1 = rf[0]
        with self.voiceover(
            "The House's simulator is the queue-reactive model, fitted to the seventeenth of May. The unit is the typical "
            f"order, {q['unit']:.1f} bitcoin. <bookmark mark='a'/> For each size of the best queue, how often it grows "
            "and how often it shrinks, per second. <bookmark mark='b'/> Small queues grow faster than they shrink, and "
            "large ones shrink faster than they grow: queues are pulled toward a typical size, the reaction that "
            "Chapter two's random walk lacked. When a queue is emptied, the price moves, and the new queue is drawn "
            f"from what the data show: {100 * p1:.0f} percent of the time a single unit, with a median of {k_med}."
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg))
            vo.wait_until("a")
            self.play(Create(cu))
            vo.wait_until("b")
            self.play(Create(cd))
        self.wait(0.4)
        self.clear_scene()

    def path(self, q):
        m = np.asarray(q["sim_mid"], float) / 2 * 0.1
        m = m - m[0]
        t = np.arange(len(m)) / 60
        lo, hi = float(np.floor(m.min())), float(np.ceil(m.max()))
        if hi - lo < 1:
            hi = lo + 1
        g = axes([0, t[-1]], [lo, hi], x_length=9.6, y_length=4.2, xlabel=r"minutes", ylabel=r"simulated mid, \$",
                 xticks=[0, 20, 40, 60], yticks=[lo, hi], yfmt=lambda v: f"{v:.0f}", font_size=15).move_to(DOWN * 0.2)
        c_ = curve(g.ax, t, m, SIM_C, stroke_width=2)
        with self.voiceover(
            "An hour of the simulated mid, from the fitted rates alone. <bookmark mark='a'/> It wanders like a price, "
            f"one half-tick at a time, ending {abs(m[-1]):.2f} dollars from where it began. It looks plausible. The "
            "question is whether it is plausible in the ways that matter."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(Create(c_), run_time=4)
        self.wait(0.4)
        self.clear_scene()

    def scorecard(self, q):
        tr, te, mo = q["data_train"], q["data_test"], q["model"]
        facts = [("moves_per_min", r"mid moves per minute", "{:.1f}"), ("gap_cv", r"burstiness of moves (Poisson = 1)",
                                                                       "{:.2f}"),
                 ("move_ac1", r"same-direction pairs (sign autocorrelation)", "{:.2f}"),
                 ("kurt_10s", r"fat tails (kurtosis of 10-s changes)", "{:.1f}"),
                 ("queue_med", r"median best queue, units", "{:.1f}")]
        hx = [-3.6, 1.2, 3.2, 5.2]
        head = VGroup(*[label(t, font_size=16, color=GREY_B) for t in (r"stylised fact", r"17 May", r"20 May",
                                                                         r"simulator")])
        tab = VGroup(head)
        for k, name, fmt in facts:
            tab.add(VGroup(label(name, font_size=17), MathTex(fmt.format(tr[k]), font_size=24),
                           MathTex(fmt.format(te[k]), font_size=24), MathTex(fmt.format(mo[k]), font_size=24,
                                                                             color=SIM_C)))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                if i == 0:
                    cell.move_to([hx[0], 2.3 - 0.75 * j, 0], aligned_edge=LEFT).shift(LEFT * 2.0)
                else:
                    cell.move_to([hx[i], 2.3 - 0.75 * j, 0])
        foot = wrapped_label(r"fitted on 17 May; 20 May is a weekend day the simulator never saw", 11.0, 16,
                             GREY_A).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "The scorecard. <bookmark mark='a'/> The simulator gets the size of the queues right, about "
            f"{mo['queue_med']:.0f} units. <bookmark mark='b'/> It moves too slowly: {mo['moves_per_min']:.1f} mid moves "
            f"a minute, against {tr['moves_per_min']:.0f} on the day it was fitted to. Its moves are only "
            f"{mo['gap_cv']:.1f} times as bursty as a Poisson clock, against {tr['gap_cv']:.1f} in the data. It has no "
            f"same-direction pairs, an autocorrelation of {abs(mo['move_ac1']):.2f} against "
            f"{tr['move_ac1']:.2f}. And its ten-second changes have a kurtosis of {mo['kurt_10s']:.1f}, against "
            f"{tr['kurt_10s']:.0f}: thin tails. One fact right; four wrong."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(foot))
            vo.wait_until("a")
            self.play(FadeIn(tab[5]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[1:5]], lag_ratio=0.4))
        self.wait(0.4)
        self.clear_scene()

    def diagnosis(self, q):
        rows = [cmath(r"\text{Markov in } (q^b, q^a)", r"\Rightarrow", r"\text{no memory}", font_size=36,
                      colors={r"\text{no memory}": BAD}),
                cmath(r"\pm 1\ \text{unit per step}", r"\Rightarrow", r"\text{no sweeps}", font_size=36,
                      colors={r"\text{no sweeps}": BAD}),
                cmath(r"\text{fix}", r":", r"\text{Hawkes rates, marks, the spread as a state}", font_size=32,
                      colors={r"\text{fix}": GOOD})]
        whys = [why(r"rates that depend only on the current queues cannot cluster: Chapter 3's self-excitation and "
                    r"order-sign memory are missing, so the tails are thin"),
                why(r"in the data one market order can take a whole queue in a single step; here a queue empties one "
                    r"unit at a time, so the price moves too rarely"),
                why(r"let rates depend on recent events, let an event remove many units, and model the spread opening "
                    r"and closing: each fix is a line on the scorecard")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "The diagnosis. <bookmark mark='a'/> The rates depend only on the current queues, so the model has no "
            "memory: none of Chapter three's self-excitation and order-sign memory, so no clustering and thin tails. "
            "<bookmark mark='b'/> A queue changes one unit per step, while in the data a single market order can take "
            "a whole queue at once: so the price moves too rarely. <bookmark mark='c'/> Each fix is a line on the "
            "scorecard: rates that depend on recent events, events that remove many units, and the spread as part of "
            "the state. The research desk keeps this simulator, and its scorecard, as the baseline every better one "
            "must beat."
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

    def realism(self):
        cards = VGroup(
            desk_question(r"match the facts, not just the likelihood", r"a model can fit each step well and still miss "
                          r"the clustering of a day", width=12.4, font_size=19),
            desk_question(r"react to the agent", r"the test that matters for execution: when an algorithm trades, does "
                          r"the simulated price respond as much as a real one would (Part 37's impact)?", width=12.4,
                          font_size=19),
            desk_question(r"test out of sample", r"a different day, a different regime: the weekend's slower book is "
                          r"in the scorecard for that reason", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Three rules for anyone who builds a market simulator. <bookmark mark='a'/> Match the facts, not only the "
            "likelihood: a model can fit each step and still miss the shape of a day. <bookmark mark='b'/> Check that "
            "it reacts: when an algorithm trades in it, the simulated price must respond as a real one would, which is "
            "Part thirty-seven's subject. <bookmark mark='c'/> And test out of sample, on another day and another "
            "regime."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"you join the back of a 5-BTC queue on the bid. Later your order is filled. Is that good news?")
        with self.voiceover(
            "Pause and predict. You join the back of a five-bitcoin queue on the bid. Later, your order is filled. Is "
            "that good news?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
