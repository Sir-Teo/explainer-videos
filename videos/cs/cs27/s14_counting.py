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
            "NP asks whether a polynomially bounded witness exists. Counting asks how many such witnesses are accepted. <bookmark mark='a'/> A number-P function counts accepting witnesses of a polynomial-time verifier under a fixed polynomial witness-length convention. <bookmark mark='b'/> For zero-one matrices, compare the determinant’s signed permutation sum with the permanent’s unsigned sum. <bookmark mark='c'/> The determinant is computable in polynomial time. Gaussian elimination has cubic arithmetic-operation complexity; integer bit complexity needs an additional size analysis. <bookmark mark='d'/> The permanent of a bipartite adjacency matrix counts perfect matchings exactly. <bookmark mark='e'/> Valiant proved that this counting problem is number-P-complete even though deciding whether a perfect matching exists is in P. <bookmark mark='f'/> This is a complexity classification, not a proof that counting requires exponential time. Such a separation would require an unproved complexity assumption."
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
            label('Ryser: subset inclusion--exclusion, $O(n2^n)$ integer arithmetic operations',
                  font_size=20, color=HEAD),
            label(rf"$n = {last['n']}$: \ {words(last['perm'])} \\ perfect matchings, \ in {last['perm_s']:.1f} s",
                  font_size=20, color=HEAD),
            label(rf"the determinant: \ {last['det_s'] * 1000:.2f} ms; \\ at $n = 200$, \ {big[200]:.2f} s",
                  font_size=20, color=DATA),
            label('30 actual call intervals per matrix; medians on this host; arithmetic bit costs matter', font_size=20, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(ax, RIGHT, buff=0.7).align_to(ax, UP)
        fit_right(notes)
        with self.voiceover(
            "The measurements compare two exact integer implementations on retained random zero-one matrices. <bookmark mark='a'/> Ryser’s inclusion-exclusion formula uses exponentially many subsets with Gray-code updates. We independently check its complete integer result using a native assignment-subset dynamic program. <bookmark mark='b'/> The twenty-by-twenty matrix has the displayed exact perfect-matching count. The time is a median of thirty actual calls on this host, not a universal runtime claim. <bookmark mark='c'/> Bareiss elimination gives exact determinants, including for the retained two-hundred-by-two-hundred matrix. An independent native modular determinant plus Chinese-remainder reconstruction certifies each complete integer using a Hadamard bound. <bookmark mark='d'/> The observed growth illustrates these implementations. Increasing n by two does not force an exact factor-four wall-clock increase, and this comparison does not prove an exponential lower bound for every permanent algorithm."
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
            label('Toda: $\\mathrm{PH}\\subseteq\\mathrm{P}^{\\#\\mathrm{P}}$; polynomial-time computation with a counting oracle', font_size=22, color=HEAD),
            label(r"\textbf{Valiant and Vazirani} \ (1986): \ random constraints isolate one solution: \ unique SAT "
                  r"is as hard as SAT, \ under randomized reductions", font_size=22, color=DATA),
            label('Stockmeyer: randomized multiplicative approximate counting with an NP oracle', font_size=22, color=WHITE),
            label('JSV: FPRAS for nonnegative rational permanent; polynomial in input bits and $1/\\varepsilon$', font_size=22, color=YES),
            label(r"by a Markov chain on matchings \ (\textit{AI, Built} 5, \ MCMC): \ sampling and counting are one "
                  r"problem", font_size=22, color=GREY_A),
            label(r"FKT \ (Kasteleyn, 1961): \ matchings of a \textbf{planar} graph exactly: \ a Pfaffian, \ a "
                  r"determinant with chosen signs", font_size=22, color=LAM),
        ).arrange(DOWN, buff=0.32).next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "Counting has striking relationships with decision and approximation. <bookmark mark='a'/> Toda’s theorem places the polynomial hierarchy inside deterministic polynomial time with a number-P oracle. We state this oracle-class inclusion without deriving a query-count refinement here. <bookmark mark='b'/> Valiant and Vazirani give randomized isolation reductions connecting SAT with the promise of a unique solution. This is not a deterministic NP-completeness claim for the unique-solution promise problem. <bookmark mark='c'/> Stockmeyer’s approximate counting uses randomness and an NP oracle to obtain a specified multiplicative accuracy with polynomial dependence on the relevant precision parameters. It is not an ordinary polynomial-time counting algorithm. <bookmark mark='d'/> Jerrum, Sinclair and Vigoda give a fully polynomial randomized approximation scheme for the permanent of nonnegative rational matrices, including input-bit, accuracy and failure-probability costs. <bookmark mark='e'/> Their sampling method depends on a carefully analysed Markov chain; the existence of a chain alone does not guarantee fast mixing or accurate counting. <bookmark mark='f'/> For planar graphs, Pfaffian methods count perfect matchings exactly under their specified graph and weight conventions. Structural restrictions can therefore change the counting problem substantially."
        ) as vo:
            self.play(FadeIn(head))
            for mk, ln in zip("abcdef", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
