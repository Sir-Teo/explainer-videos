from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs27.common import (BG, CTRL, DATA, HEAD, LAM, NO, PART, YES, fit_right, grid_table, load, mono, words)


class Counting(VoiceoverScene):
    def construct(self):
        self.card()
        self.sharp()
        self.permanent()
        self.toda()

    def card(self):
        card = chapter_card(13, r"Counting", r"Is counting solutions harder than finding one?", lit=(1979, 2004),
                            extra=((1979, r"Valiant: \ \#P"), (1991, r"Toda"), (2004, r"Jerrum--Sinclair--Vigoda")),
                            part=PART)
        with self.voiceover("Chapter thirteen. Counting."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def sharp(self):
        head = label(r"\#P: \ how many certificates?", font_size=34).to_edge(UP, buff=0.3)
        perm = MathTex(r"\mathrm{perm}(A) = \sum_{\sigma} \prod_{i=1}^{n} a_{i, \sigma(i)}", font_size=40,
                       color=HEAD)
        det = MathTex(r"\det(A) = \sum_{\sigma} \mathrm{sgn}(\sigma) \prod_{i=1}^{n} a_{i, \sigma(i)}", font_size=40,
                      color=DATA)
        forms = VGroup(det, perm).arrange(DOWN, buff=0.35).next_to(head, DOWN, buff=0.45)
        sign = SurroundingRectangle(det[0][9:15], color=YES, buff=0.06)
        lines = VGroup(
            label(r"\#P \ (Valiant, 1979): \ count the accepting certificates of an NP verifier", font_size=22,
                  color=WHITE),
            label(r"\#SAT: \ how many satisfying assignments? \ \ (chapter 6 counted them with sum-check)",
                  font_size=22, color=GREY_A),
            label(r"the two formulas differ only by a \textbf{sign}", font_size=22, color=YES),
            label(r"the determinant: \ Gaussian elimination, \ $O(n^3)$", font_size=22, color=DATA),
            label(r"the permanent of a 0/1 matrix counts the \textbf{perfect matchings} of a bipartite graph",
                  font_size=22, color=HEAD),
            label(r"Valiant: \ the permanent is \textbf{\#P-complete}, \ though deciding if a matching exists is "
                  r"in P \ (Part 18)", font_size=22, color=NO),
        ).arrange(DOWN, buff=0.24).next_to(forms, DOWN, buff=0.45)
        with self.voiceover(
            "NP asks whether a certificate exists. <bookmark mark='a'/> Leslie Valiant defined the class sharp-P in "
            "1979: count the certificates. <bookmark mark='b'/> How many assignments satisfy this formula? Chapter "
            "six's sum-check protocol was exactly such a count. <bookmark mark='c'/> Here are two famous functions of "
            "a matrix. They differ only by a sign. <bookmark mark='d'/> The determinant, with the signs, is computed "
            "by Gaussian elimination in cubic time. <bookmark mark='e'/> The permanent, without them, counts the "
            "perfect matchings of a bipartite graph when the matrix has zeros and ones. <bookmark mark='f'/> Valiant "
            "proved the permanent sharp-P-complete. Finding one perfect matching is easy, as Part 18 showed; counting "
            "them is as hard as counting the solutions of any NP problem."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(FadeIn(lines[1]))
            vo.wait_until("c")
            self.play(Write(det), Write(perm))
            self.play(Create(sign), FadeIn(lines[2]))
            vo.wait_until("d")
            self.play(FadeIn(lines[3]))
            vo.wait_until("e")
            self.play(FadeIn(lines[4]))
            vo.wait_until("f")
            self.play(FadeIn(lines[5]))
        self.wait(0.3)
        self.clear_scene()

    def permanent(self):
        d = load("permanent")
        head = label(r"Permanent against determinant, \ measured", font_size=32).to_edge(UP, buff=0.3)
        ax = Axes(x_range=[7, 21, 2], y_range=[0, 6, 1], x_length=6.0, y_length=4.0,
                  axis_config={"color": GREY_D, "include_numbers": False}).next_to(head, DOWN, buff=0.6).to_edge(
            LEFT, buff=1.0)
        xt = VGroup(*[label(str(x), font_size=15, color=GREY_A).next_to(ax.c2p(x, 0), DOWN, buff=0.08)
                      for x in (8, 12, 16, 20)])
        yt = VGroup(*[label(t, font_size=15, color=GREY_A).next_to(ax.c2p(7, y + 5), LEFT, buff=0.08)
                      for y, t in ((-4, r"0.1 ms"), (-3, r"1 ms"), (-2, r"10 ms"), (-1, r"0.1 s"), (0, r"1 s"))])
        xl = label(r"matrix size $n$", font_size=17, color=GREY_A).next_to(ax, DOWN, buff=0.35)
        def lg(t):
            return math.log10(t) + 5
        pp = VGroup(*[Dot(ax.c2p(r["n"], lg(r["perm_s"])), radius=0.07, color=HEAD) for r in d["rows"]])
        dp = VGroup(*[Dot(ax.c2p(r["n"], lg(r["det_s"])), radius=0.07, color=DATA) for r in d["rows"]])
        pl = VMobject(color=HEAD, stroke_width=2).set_points_as_corners([p.get_center() for p in pp])
        dl = VMobject(color=DATA, stroke_width=2).set_points_as_corners([p.get_center() for p in dp])
        lp = label(r"permanent \ (Ryser)", font_size=18, color=HEAD).next_to(pp[-1], UP, buff=0.15).shift(LEFT * 0.6)
        ld = label(r"determinant \ (Bareiss)", font_size=18, color=DATA).next_to(dp[-1], UP, buff=0.15).shift(
            LEFT * 0.8)
        last = d["rows"][-1]
        big = {r["n"]: r["det_s"] for r in d["det_big"]}
        notes = VGroup(
            label(r"random 0/1 matrices, \ exact integer arithmetic", font_size=20, color=GREY_A),
            label(r"Ryser \ (1963): \ inclusion--exclusion over \\ column subsets, \ $O(2^n n)$: \ the best known",
                  font_size=20, color=HEAD),
            label(rf"$n = {last['n']}$: \ {words(last['perm'])} \\ perfect matchings, \ in {last['perm_s']:.1f} s",
                  font_size=20, color=HEAD),
            label(rf"the determinant: \ {last['det_s'] * 1000:.2f} ms; \\ at $n = 200$, \ {big[200]:.2f} s",
                  font_size=20, color=DATA),
            label(r"each $+2$ in $n$ multiplies \\ the permanent's time by about 4", font_size=20, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(ax, RIGHT, buff=0.7).align_to(ax, UP)
        fit_right(notes)
        with self.voiceover(
            "We timed both on random zero-one matrices, with exact integers. <bookmark mark='a'/> The best known "
            "algorithm for the permanent is still Herbert Ryser's from 1963: inclusion and exclusion over subsets of "
            "columns, about two to the n steps. <bookmark mark='b'/> At n equals twenty, our matrix has over two "
            "trillion perfect matchings, and counting them took two point three seconds. <bookmark mark='c'/> The "
            "determinant of the same matrix took a quarter of a millisecond, and a two-hundred by two-hundred "
            "determinant takes under a second. <bookmark mark='d'/> Every two extra rows multiply the permanent's "
            "time by about four. One sign separates polynomial from exponential."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl), FadeIn(notes[0]))
            vo.wait_until("a")
            self.play(FadeIn(notes[1]), LaggedStart(*[FadeIn(p) for p in pp], lag_ratio=0.15), Create(pl),
                      FadeIn(lp))
            vo.wait_until("b")
            self.play(FadeIn(notes[2]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(p) for p in dp], lag_ratio=0.15), Create(dl), FadeIn(ld),
                      FadeIn(notes[3]))
            vo.wait_until("d")
            self.play(FadeIn(notes[4]))
        self.wait(0.3)
        self.clear_scene()

    def toda(self):
        head = label(r"How powerful is counting?", font_size=34).to_edge(UP, buff=0.35)
        lines = VGroup(
            label(r"\textbf{Toda} \ (1991): \ $\mathrm{PH} \subseteq \mathrm{P}^{\#\mathrm{P}}$: \ one counting "
                  r"oracle answers the whole polynomial hierarchy \ (Part 26)", font_size=22, color=HEAD),
            label(r"\textbf{Valiant and Vazirani} \ (1986): \ random constraints isolate one solution: \ unique SAT "
                  r"is as hard as SAT, \ under randomized reductions", font_size=22, color=DATA),
            label(r"\textbf{Stockmeyer} \ (1983): \ counting \textbf{approximately} needs only an NP oracle, \ with "
                  r"randomness", font_size=22, color=WHITE),
            label(r"\textbf{Jerrum, \ Sinclair and Vigoda} \ (2004): \ the permanent of a non-negative matrix, "
                  r"\ within $1 \pm \varepsilon$, \ in polynomial time", font_size=22, color=YES),
            label(r"by a Markov chain on matchings \ (\textit{AI, Built} 5, \ MCMC): \ sampling and counting are one "
                  r"problem", font_size=22, color=GREY_A),
            label(r"FKT \ (Kasteleyn, 1961): \ matchings of a \textbf{planar} graph exactly: \ a Pfaffian, \ a "
                  r"determinant with chosen signs", font_size=22, color=LAM),
        ).arrange(DOWN, buff=0.32).next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "How much power does counting give? <bookmark mark='a'/> Seinosuke Toda proved in 1991 that a machine "
            "with a sharp-P oracle can decide everything in the polynomial hierarchy of Part 26. One count is worth "
            "any number of alternating quantifiers. <bookmark mark='b'/> Leslie Valiant and Vijay Vazirani showed "
            "that random constraints can isolate a single solution, so even deciding satisfiability for formulas "
            "promised to have at most one solution is hard. <bookmark mark='c'/> Approximate counting is much "
            "weaker: Larry Stockmeyer showed it needs only an NP oracle and randomness. <bookmark mark='d'/> And for "
            "the permanent of a non-negative matrix, Mark Jerrum, Alistair Sinclair and Eric Vigoda found a "
            "polynomial-time approximation in 2004, <bookmark mark='e'/> using a Markov chain that samples random "
            "matchings, the Markov chain Monte Carlo of AI, Built, Part 5. <bookmark mark='f'/> And one exact special case: Pieter "
            "Kasteleyn counted the perfect matchings of planar graphs in 1961, by turning the permanent into a "
            "determinant with cleverly chosen signs."
        ) as vo:
            self.play(FadeIn(head))
            for mk, ln in zip("abcdef", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
