from __future__ import annotations

import numpy as np
from scipy.stats import binom

from explainer.quant import *  # noqa: F403
from videos.quant.quant4.common import DRIFT, LOSS, MART, PART

N_MAJ = 21


def majority_paths(k=6, seed=1):
    """P(at least 11 heads in 21 fair tosses | the first n): a martingale that ends at 0 or 1."""
    rng = np.random.default_rng(seed)
    out = []
    for _ in range(k):
        h = rng.random(N_MAJ) < 0.5
        heads = np.concatenate([[0], np.cumsum(h)])
        n = np.arange(N_MAJ + 1)
        need = 11 - heads
        p = binom.sf(need - 1, N_MAJ - n, 0.5)
        p = np.where(need <= 0, 1.0, np.where(need > N_MAJ - n, 0.0, p))
        out.append(p)
    return np.array(out)


class Martingales(VoiceoverScene):
    def construct(self):
        self.card()
        self.definition()
        self.majority()
        self.stopping()

    def card(self):
        c = chapter_card(2, r"Martingales and optional stopping", r"Can a betting system beat a fair game?",
                         part=PART)
        with self.voiceover("Chapter two. Martingales, and optional stopping."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def definition(self):
        d = definition_card(r"Martingale", r"A process $M_0, M_1, \dots$ that is known at each time ($M_n$ depends only "
                            r"on $\mathcal{F}_n$), has a finite mean, and whose best forecast of tomorrow is today: "
                            r"$\mathbb{E}[M_{n+1} \mid \mathcal{F}_n] = M_n$.", width=8.6, color=MART, font_size=25)
        h = history_card(1939, r"Jean Ville, \textit{\'Etude critique de la notion de collectif}",
                         r"named fair games after the ``martingale'', the gamblers' doubling system; Joseph Doob built "
                         r"the theory (1940; \textit{Stochastic Processes}, 1953)", width=8.6)
        ex = VGroup(
            label(r"examples", font_size=24, color=GREY_A),
            MathTex(r"\text{a gambler's wealth in a fair game}", font_size=28),
            MathTex(r"S_n^2 - n \quad \text{for a walk of } \pm 1 \text{ steps}", font_size=28),
            MathTex(r"\mathbb{E}[X \mid \mathcal{F}_n] \quad \text{for any } X\text{: Doob's martingale}", font_size=28,
                    color=MART),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        VGroup(d, h, ex).arrange(DOWN, buff=0.4).move_to(ORIGIN)
        with self.voiceover(
            "A martingale is a process whose best forecast of tomorrow is today. It is known at each time, it has a "
            "finite mean, and its conditional expectation one step ahead equals its current value. It is the "
            "mathematical form of a fair game. <bookmark mark='a'/> The name comes from Jean Ville's thesis of 1939, "
            "which borrowed it from the most famous betting system, the martingale, in which you double your stake "
            "after every loss. Joseph Doob read Ville and built the theory. <bookmark mark='b'/> Examples: a "
            "gambler's wealth in a fair game. The square of a random walk minus the number of steps. And, from the "
            "previous chapter, the conditional expectation of anything, as information arrives: Doob's martingale."
        ) as vo:
            self.play(FadeIn(d, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(h))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(e) for e in ex], lag_ratio=0.4))
        self.wait(0.4)
        self.clear_scene()

    def majority(self):
        P = majority_paths()
        g = axes([0, N_MAJ], [0, 1], x_length=8.0, y_length=4.4, xlabel=r"tosses seen", ylabel=r"chance that heads "
                 r"wins a best-of-21", xticks=[0, 7, 14, 21], yticks=[0, 0.5, 1], font_size=18)
        g.to_edge(LEFT, buff=0.7).shift(DOWN * 0.2)
        ax = g.ax
        cols = color_gradient([MART, QC.SPOT], len(P))
        paths = VGroup(*[curve(ax, np.arange(N_MAJ + 1), p, c, stroke_width=3) for p, c in zip(P, cols)])
        side = VGroup(
            label(r"a live forecast is a martingale:", font_size=22, color=GREY_A),
            label(r"it starts at its mean, 50\%,", font_size=22, color=GREY_A),
            label(r"moves only on news,", font_size=22, color=GREY_A),
            label(r"and ends at 0 or 1", font_size=22, color=GREY_A),
            wrapped_label(r"a betting market's price, or an option's risk-neutral probability of finishing in the "
                          r"money, behaves the same way (Part 9)", 4.4, 20, MART),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(RIGHT, buff=0.5)
        with self.voiceover(
            "Here is a Doob martingale you can watch. Two players toss a fair coin twenty-one times, and heads wins "
            "if it comes up eleven times or more. After each toss, compute the chance that heads wins, given the "
            "tosses so far. <bookmark mark='a'/> Each line is one match. Every forecast starts at fifty percent, "
            "jumps with each toss, more sharply as the end approaches, and finishes at zero or one. Yet on average "
            "it never moves: today's forecast is the average of tomorrow's. <bookmark mark='b'/> A betting market's "
            "price behaves like this, and so, under the right measure, does an option's probability of finishing in "
            "the money."
        ) as vo:
            self.play(FadeIn(g), FadeIn(side[:4]))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(p) for p in paths], lag_ratio=0.4, run_time=5))
            vo.wait_until("b")
            self.play(FadeIn(side[4]))
        self.wait(0.4)
        self.clear_scene()

    def stopping(self):
        th = theorem_card(r"Optional stopping",
                          r"If $M$ is a martingale and $\tau$ a stopping time (the decision to stop uses only the past), "
                          r"then $\mathbb{E}[M_\tau] = M_0$, provided $\tau$ is bounded; or $\mathbb{E}[\tau] < \infty$ and "
                          r"the steps are bounded; or $M$ stays bounded up to $\tau$.",
                          who=r"Doob", color=MART, width=9.4, font_size=24).to_edge(UP, buff=0.5)
        cases = VGroup(
            VGroup(label(r"doubling with an endless bankroll", font_size=24, color=LOSS),
                   MathTex(r"\mathbb{E}[\tau] = 2, \text{ but the bets } 1, 2, 4, \dots \text{ are unbounded}", font_size=28),
                   MathTex(r"\Rightarrow\ \mathbb{E}[M_\tau] = M_0 + 1", font_size=30, color=LOSS)).arrange(
                DOWN, aligned_edge=LEFT, buff=0.12),
            VGroup(label(r"doubling with a bankroll of 1{,}023", font_size=24, color=DRIFT),
                   MathTex(r"\text{at most ten doublings: the steps are bounded}", font_size=28),
                   MathTex(r"\tfrac{1023}{1024}\,(+1) + \tfrac{1}{1024}\,(-1023) = 0", font_size=30, color=DRIFT)).arrange(
                DOWN, aligned_edge=LEFT, buff=0.12),
        ).arrange(RIGHT, buff=0.8, aligned_edge=UP).next_to(th, DOWN, buff=0.6)
        adm = wrapped_label(r"In continuous time a doubling scheme can win any amount in a finite time; finance rules it "
                            r"out by allowing only strategies whose losses are bounded: ``admissible'' strategies "
                            r"(Part 9).", 11.0, 23, GREY_A).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Part one showed by experiment that stopping rules can't beat a fair game. Here is the theorem. If you "
            "stop a martingale at a time chosen using only the past, its expected value when you stop is its value "
            "at the start, provided one of three things holds: you stop by some fixed time; or your expected wait is "
            "finite and each step is bounded; or the martingale stays bounded until you stop. <bookmark mark='a'/> "
            "The doubling system is exactly what the conditions exclude. With an endless bankroll you stop at the "
            "first win, after two tosses on average, and you are always one unit up. The theorem doesn't apply, "
            "because the bets grow without limit. <bookmark mark='b'/> Give the gambler a real bankroll of a "
            "thousand and twenty-three units, ten doublings, and the steps are bounded. Now the theorem holds: a "
            "thousand and twenty-three times in a thousand and twenty-four the gambler wins one unit, and once loses "
            "everything. The average is exactly zero. <bookmark mark='c'/> In continuous time the problem is worse: "
            "doubling can win any amount in finite time. Finance rules it out by allowing only strategies whose "
            "losses are bounded, and we will meet those admissible strategies in Part nine."
        ) as vo:
            self.play(FadeIn(th, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(cases[0]))
            vo.wait_until("b")
            self.play(FadeIn(cases[1]))
            vo.wait_until("c")
            self.play(FadeIn(adm))
        self.wait(0.4)
        self.clear_scene()
