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
                [r"\textbf{coRP}", 'never wrong on yes; rejects no with probability $\\ge \\tfrac12$', r"primality, \ the same test read backwards"],
                [r"\textbf{ZPP}", 'zero error; expected polynomial time on every input', r"Las Vegas: \ quicksort with "
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
            "Randomized decision classes use probabilities over the algorithm’s own independent coins, for each fixed input. <bookmark mark='a'/> RP has polynomial worst-case running time, rejects every no-instance, and accepts each yes-instance with probability at least one half. Compositeness supplies an example. <bookmark mark='b'/> coRP reverses those roles: yes-instances always pass, and no-instances are rejected with probability at least one half. <bookmark mark='c'/> ZPP requires zero error and expected polynomial running time on every input. Randomized quicksort illustrates the Las Vegas style, although sorting itself is a function problem. <bookmark mark='d'/> BPP has polynomial worst-case running time and error at most one third on every input. Identity testing is a one-sided example within BPP. <bookmark mark='e'/> P is contained in ZPP, which equals the intersection of RP and coRP; these classes lie within BPP and PSPACE. <bookmark mark='f'/> None of these definitions averages over an input distribution. An adversary may choose the input."
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
            label('the binomial tail, evaluated numerically; exact rational cross-check',
                  font_size=21, color=DATA),
            label(r"Chernoff: \ error $\le e^{-k/18}$: \ exponentially small \\ (the tail bounds of "
                  r"\textit{AI, Built} Part 5)", font_size=21, color=HEAD),
            label(r"so ``$\tfrac13$'' is arbitrary: \ any constant below $\tfrac12$ \\ defines the same class",
                  font_size=21, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).next_to(tab, RIGHT, buff=0.8).align_to(tab, UP)
        fit_right(notes)
        with self.voiceover(
            "Any fixed error bound below one half can be amplified. <bookmark mark='a'/> Run the algorithm independently an odd number of times and take the majority answer. <bookmark mark='b'/> The displayed binomial tail assumes each run errs with probability exactly one third; for smaller errors it is an upper bound. We evaluate this expression numerically and check it against exact rational sums. <bookmark mark='c'/> Hoeffding’s inequality gives the simpler upper bound exponential in minus the number of runs divided by eighteen. <bookmark mark='d'/> Thus a linear number of independent repetitions in the desired error exponent suffices; independence and a constant gap below one half are essential."
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
            "Amplification also gives a nonuniform simulation of BPP. <bookmark mark='a'/> Reduce each fixed input’s failure probability below one divided by two raised to the quantity n plus one, using polynomially many independent runs. <bookmark mark='b'/> A union bound over all two-to-the-n inputs of length n makes the probability that a coin string fails on any of them less than one half. <bookmark mark='c'/> Hence at least one fixed coin string works for every input of that length. This is an existence argument. <bookmark mark='d'/> Hardwire that polynomial-length string into a polynomial-size circuit or advice string. The argument does not give a uniform efficient procedure for finding it. <bookmark mark='e'/> This proves BPP is contained in P over poly. The Sipser–Gács–Lautemann theorem separately places BPP in the second level of the polynomial hierarchy and its dual."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab))
            for mk, ln in zip("abcde", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
