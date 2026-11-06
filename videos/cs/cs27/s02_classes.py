from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs27.common import (CTRL, DATA, HEAD, LAM, NO, PART, YES, fit_right, grid_table, load, sci)


class Classes(VoiceoverScene):
    def construct(self):
        self.card()
        self.kinds()
        self.amplify()
        self.adleman()

    def card(self):
        card = chapter_card(1, r"Randomized classes", r"What can an algorithm with coins decide?", lit=(1977, 1983),
                            extra=((1977, r"Gill"), (1978, r"Adleman"), (1983, r"Sipser--G\'acs--Lautemann")),
                            part=PART)
        with self.voiceover("Chapter one. Randomized classes."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def kinds(self):
        head = label(r"Four ways to use coins \ (Gill, 1977)", font_size=34).to_edge(UP, buff=0.35)
        rows = [[r"\textbf{RP}", r"never wrong on \textbf{no}; \ says yes with probability $\ge \tfrac12$ on yes",
                 r"compositeness \ (Miller--Rabin, \ Part 20)"],
                [r"\textbf{coRP}", r"never wrong on \textbf{yes}", r"primality, \ the same test read backwards"],
                [r"\textbf{ZPP}", r"never wrong; \ the \textbf{running time} is random", r"Las Vegas: \ quicksort with "
                 r"random pivots"],
                [r"\textbf{BPP}", r"wrong with probability $\le \tfrac13$ \ on every input", r"polynomial identity "
                 r"testing \ (Part 20)"]]
        tab = grid_table([r"class", r"guarantee", r"example"], rows, widths=[1.6, 6.4, 4.8], row_h=0.62, font_size=20,
                         mono_cols=(), colors=[[DATA, WHITE, GREY_A], [LAM, WHITE, GREY_A], [YES, WHITE, GREY_A],
                                               [HEAD, WHITE, GREY_A]])
        tab.next_to(head, DOWN, buff=0.45).set_x(0)
        notes = VGroup(
            label(r"$\mathrm{P} \subseteq \mathrm{ZPP} = \mathrm{RP} \cap \mathrm{coRP} \subseteq \mathrm{BPP}"
                  r"\subseteq \mathrm{PSPACE}$", font_size=26, color=WHITE),
            label(r"``on every input'': \ the probability is over the coins, \ never over a random input", font_size=21,
                  color=NO),
        ).arrange(DOWN, buff=0.22).next_to(tab, DOWN, buff=0.45)
        with self.voiceover(
            "Part 20 used coins to make algorithms simpler and faster. Here are the classes they define, named by "
            "John Gill in 1977. <bookmark mark='a'/> RP allows one-sided error: never a false yes, and a true yes at "
            "least half the time. Compositeness is the classic example, with the Miller-Rabin test. <bookmark "
            "mark='b'/> coRP is the mirror image. <bookmark mark='c'/> ZPP never errs, but its running time is a "
            "random variable, like quicksort with random pivots. <bookmark mark='d'/> And BPP allows error on both "
            "sides, at most a third, on every input. <bookmark mark='e'/> They nest: P inside ZPP, which is exactly "
            "RP intersect coRP, inside BPP, inside polynomial space. <bookmark mark='f'/> Notice that the probability "
            "is over the algorithm's coins. The input is arbitrary, even chosen by an adversary."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule))
            for mk, r in zip("abcd", tab.cells[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(VGroup(*r)))
            for mk, n_ in zip("ef", notes):
                vo.wait_until(mk)
                self.play(FadeIn(n_))
        self.wait(0.3)
        self.clear_scene()

    def amplify(self):
        a = load("amplify")
        head = label(r"Amplification: \ repeat and vote", font_size=34).to_edge(UP, buff=0.35)
        rows = [[str(r["k"]), f"{r['error']:#.3g}" if r["error"] > 1e-4 else rf"${sci(r['error'], 2)}$"]
                for r in a["rows"]]
        tab = grid_table([r"runs $k$", r"error of the majority"], rows, widths=[1.8, 3.6], row_h=0.4, font_size=20,
                         mono_cols=(), colors=[[WHITE, YES]] * len(rows))
        tab.next_to(head, DOWN, buff=0.4).to_edge(LEFT, buff=1.2)
        notes = VGroup(
            label(r"each run errs with probability $\tfrac13$, \ independently", font_size=21, color=WHITE),
            label(r"the majority errs only if more than half the runs do: \\ the binomial tail, \ computed exactly",
                  font_size=21, color=DATA),
            label(r"Chernoff: \ error $\le e^{-k/18}$: \ exponentially small \\ (the tail bounds of "
                  r"\textit{AI, Built} Part 5)", font_size=21, color=HEAD),
            label(r"so ``$\tfrac13$'' is arbitrary: \ any constant below $\tfrac12$ \\ defines the same class",
                  font_size=21, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).next_to(tab, RIGHT, buff=0.8).align_to(tab, UP)
        fit_right(notes)
        with self.voiceover(
            "Why a third? Any constant below a half would do, because errors can be driven down. <bookmark "
            "mark='a'/> Run the algorithm k times with fresh coins and take the majority answer. <bookmark "
            "mark='b'/> The majority is wrong only if more than half of the runs are. We computed the exact binomial "
            "tail: a hundred and one runs bring the error from a third to under three in ten thousand; two hundred "
            "and one runs, to about one in two million. <bookmark mark='c'/> The Chernoff bound, from the tail "
            "bounds of AI, Built, guarantees exponential decay in k. <bookmark mark='d'/> So the threshold of a "
            "third is arbitrary: any error bounded away from a half defines the same class."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(tab), FadeIn(notes[0]))
            for mk, n_ in zip("bcd", notes[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(n_))
        self.wait(0.3)
        self.clear_scene()

    def adleman(self):
        a = load("amplify")["adleman"]
        head = label(r"Adleman \ (1978): \ BPP $\subseteq$ P/poly", font_size=34).to_edge(UP, buff=0.35)
        rows = [[str(r["n"]), str(r["runs"]), rf"${sci(r['error'], 2)}$", rf"{r['union']:.2f}"] for r in a]
        tab = grid_table([r"input length $n$", r"runs", r"error per input", r"$2^n \times$ error"], rows,
                         widths=[2.6, 1.6, 2.6, 2.4], row_h=0.42, font_size=20, mono_cols=(),
                         colors=[[WHITE, DATA, YES, HEAD]] * len(rows))
        tab.next_to(head, DOWN, buff=0.4).set_x(0)
        lines = VGroup(
            label(r"amplify until the error on each input is below $2^{-(n+1)}$", font_size=22, color=WHITE),
            label(r"there are $2^n$ inputs: \ the chance that a random coin string fails \textbf{any} of them is "
                  r"below $\tfrac12$ \ (union bound)", font_size=22, color=DATA),
            label(r"so some \textbf{single} string of coins works for every input of length $n$", font_size=22,
                  color=YES),
            label(r"hard-wire it: \ a polynomial-size circuit for each $n$, \ no coins at all", font_size=22,
                  color=HEAD),
            label(r"Sipser, \ G\'acs, \ Lautemann \ (1983): \ BPP $\subseteq \Sigma_2 \cap \Pi_2$, \ inside the "
                  r"hierarchy of Part 26", font_size=21, color=GREY_A),
        ).arrange(DOWN, buff=0.22).next_to(tab, DOWN, buff=0.4)
        with self.voiceover(
            "Amplification has a surprising consequence. <bookmark mark='a'/> Amplify until the error on each "
            "input is below two to the minus n plus one: for inputs of a hundred bits, about eleven hundred runs. "
            "<bookmark mark='b'/> There are two to the n inputs of length n, so the probability that a random "
            "string of coins is bad for any of them is at most two to the n times the error: below a half. <bookmark "
            "mark='c'/> So some single string of coins is good for every input of that length. <bookmark "
            "mark='d'/> Build it into the circuit, and the randomness disappears: one polynomial-size circuit per "
            "input length. Leonard Adleman proved this in 1978. <bookmark mark='e'/> And Michael Sipser, Péter Gács "
            "and Clemens Lautemann showed that BPP sits in the second level of the polynomial hierarchy of Part 26."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab))
            for mk, ln in zip("abcde", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
