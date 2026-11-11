from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs16.common import (CODE, COST, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, grid_table, load, mono,
                                   words)


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.smoothed()
        self.integers()
        self.finegrained()
        self.open()

    def card(self):
        card = chapter_card(16, r"Frontier: \ beyond the worst case", r"What does an algorithm really cost?",
                            lit=(2001,), extra=((2001, r"Spielman and Teng: \ smoothed analysis"),), part=PART)
        with self.voiceover("Chapter sixteen. Frontier: beyond the worst case."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def smoothed(self):
        d = load("frontier")
        head = label(r"Smoothed analysis: \ a little noise", font_size=34).to_edge(UP, buff=0.3)
        rows = [r for r in d["rows"] if r["sigma"] > 0]
        ax = Axes(x_range=[-4.2, 0.2, 1], y_range=[4, 6.5, 0.5], x_length=6.0, y_length=3.8,
                  axis_config={"color": GREY_D, "include_numbers": False}).to_edge(LEFT, buff=0.8).shift(DOWN * 0.3)
        ax.y_axis.set_opacity(0)
        left_axis=Line(ax.c2p(-4.2,4),ax.c2p(-4.2,6.5),color=GREY_D,stroke_width=2)
        yt=VGroup(*[MathTex(rf"10^{{{v}}}",font_size=16,color=GREY_B).next_to(ax.c2p(-4.2,v),LEFT,buff=0.1) for v in (4,5,6)])
        pts = [ax.c2p(np.log10(r["sigma"]), np.log10(r["cmp"])) for r in rows]
        line = VMobject(color=YES, stroke_width=3).set_points_as_corners(pts)
        dots = VGroup(*[Dot(p, radius=0.06, color=YES) for p in pts])
        worst = DashedLine(ax.c2p(-4.2, np.log10(d["worst"])), ax.c2p(0.2, np.log10(d["worst"])), color=NO,
                           stroke_width=2)
        avg = DashedLine(ax.c2p(-4.2, np.log10(d["average"])), ax.c2p(0.2, np.log10(d["average"])), color=DATA,
                         stroke_width=2)
        wl = label(r"worst case: \ sorted input", font_size=17, color=NO).next_to(worst, UP, buff=0.05).align_to(
            worst, LEFT)
        al = label(r"average: \ random input", font_size=17, color=DATA).next_to(avg, DOWN, buff=0.05).align_to(
            avg, LEFT)
        xt = VGroup(*[label(t, font_size=15, color=GREY_B).next_to(ax.c2p(v, 4), DOWN, buff=0.1)
                      for v, t in ((-4, r"$10^{-4}$"), (-3, r"$10^{-3}$"), (-2, r"$10^{-2}$"), (-1, r"$10^{-1}$"),
                                   (0, r"1"))])
        xl = label(r"noise added to each sorted key, \ $\sigma$", font_size=17, color=GREY_B).next_to(xt, DOWN,
                                                                                                    buff=0.1)
        yl = label(rf"comparisons, \ first-element pivot, \ $n = {words(d['n'])}$, \ log scale", font_size=17,
                   color=GREY_B).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)
        def two(a, b, size, col):
            return VGroup(label(a, font_size=size, color=col), label(b, font_size=size, color=col)).arrange(
                DOWN, aligned_edge=LEFT, buff=0.07)
        side = VGroup(
            two(r"sorted keys plus independent Gaussian noise", r"10 trials per noise level; one input family", 21, GREY_A),
            two(r"\textbf{smoothed analysis} \ (Spielman and Teng, \ 2001):", r"worst input, then expected perturbation cost",
                21, YES),
            two(r"a landmark application: simplex", r"within its theorem's perturbation model", 21,
                GREY_A),
            label(r"G\"odel Prize, \ 2008", font_size=19, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        if side.width > 5.6:
            side.scale_to_fit_width(5.6)
        side.to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            (
            "Worst-case and average-case analysis ask different questions. <bookmark mark='a'/> This experiment "
            "starts with one sorted input of two thousand keys, adds independent Gaussian noise with the shown "
            "standard deviation, and averages ten seeded trials per noise level. <bookmark mark='b'/> For this "
            "input family, the observed first-pivot comparison count falls toward the random-order benchmark. It "
            "does not show that every real input is harmless, or that every noisy trial improves. <bookmark "
            "mark='c'/> Formal smoothed analysis takes a worst case over the permitted initial inputs, then an "
            "expectation over the specified perturbation. Spielman and Teng developed the framework for simplex. "
            "Our single-family plot illustrates the idea; it does not compute that worst-case smoothed bound."
        )
        ) as vo:
            self.play(FadeIn(head), Create(ax),Create(left_axis),FadeIn(yt), FadeIn(xt), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(Create(worst), FadeIn(wl), Create(avg), FadeIn(al), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(line), FadeIn(dots), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(side[1:]))
        self.wait(0.3)
        self.clear_scene()

    def integers(self):
        head=label(r"Selected historical integer-sorting bounds",font_size=33).to_edge(UP,buff=0.3)
        rows=[
            [r"comparison model",r"$\Theta(n\log n)$",r"distinct keys; worst case"],
            [r"van Emde Boas (1975)",r"$O(n\log\log U)$",r"universe below $U$; structure/space assumptions"],
            [r"fusion trees (1990)",r"$O(n\log n/\log\log n)$",r"word operations beyond comparisons"],
            [r"Andersson et al. (1995)",r"$O(n\log\log n)$",r"deterministic; arbitrary $w\ge\log n$"],
            [r"Andersson et al. (1995)",r"$O(n)$ expected",r"randomized; $w\ge(\log n)^{2+\varepsilon}$"],
            [r"Han and Thorup (2002)",r"$O(n\sqrt{\log\log n})$",r"expected time; specified word-RAM"],
            [r"Belazzougui et al. (2014)",r"$O(n)$ expected",r"$w=\Omega(\log^2 n\log\log n)$"],
            [r"research direction",r"remove restrictions",r"fix operations, word widths and randomness"],
        ]
        tab=grid_table([r"result",r"time",r"conditions matter"],rows,widths=[4.3,3.5,5.3],row_h=0.49,font_size=18,mono_cols=(),colors=[[WHITE,WHITE,GREY_B]]*7+[[HEAD,HEAD,HEAD]]).next_to(head,DOWN,buff=0.45)
        note=VGroup(label(r"selected historical bounds; consult each paper's precise instruction and space model",font_size=18,color=GREY_B),
                    label(r"fixed 32-bit radix sorting does not settle every growing-word-width model",font_size=19,color=HEAD)).arrange(DOWN,buff=0.15).to_edge(DOWN,buff=0.35)
        with self.voiceover("Integer sorting depends on the precise machine model. <bookmark mark='a'/> The table collects historical word-RAM upper bounds, with their randomization and word-width conditions. Reading digits escapes the comparison lower bound, but fixed thirty-two-bit radix sort does not settle the asymptotic question for every growing word width. <bookmark mark='b'/> The author abstracts for the listed linear-time results require sufficiently large words; some results are expected-time randomized bounds. Our research question asks how such restrictions can be relaxed in an explicitly specified instruction model. These selected historical sources are not a complete survey of every recent result.") as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(tab.rule),*[FadeIn(c) for c in tab.cells[0]],LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:-1]],lag_ratio=0.12),run_time=1.8)
            vo.wait_until("b")
            self.play(FadeIn(VGroup(*tab.cells[-1])),FadeIn(note))
        self.wait(0.3);self.clear_scene()

    def finegrained(self):
        head = label(r"Fine-grained complexity", font_size=34).to_edge(UP, buff=0.3)
        rows = [[r"SETH: \ $k$-SAT needs $2^{(1 - o(1)) n}$ as $k$ grows", r"edit distance: "
                 r"\ no $n^{2 - \varepsilon}$ \ (Backurs and Indyk, \ 2015)"],
                [r"3SUM: \ no $n^{2 - \varepsilon}$ algorithm", r"many problems in computational geometry"],
                [r"weighted APSP: no $n^{3-\varepsilon}$ in the specified model", r"specific graph-problem versions, \ "
                 r"linked by exponent-sensitive reductions"]]
        tab = grid_table([r"if this conjecture holds", r"then these cannot be done faster"], rows, widths=[5.8, 6.6],
                         row_h=0.7, font_size=18, mono_cols=()).next_to(head, DOWN, buff=0.6)
        pts = VGroup(
            label(r"not ``polynomial or not'', \ but ``which polynomial'': \ reductions that preserve exponents",
                  font_size=21, color=GREY_A),
            label(r"conditional evidence for edit distance; \ not an unconditional quadratic lower bound", font_size=21, color=YES),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            (
            "Some frontiers concern the exponent itself. <bookmark mark='a'/> Fine-grained complexity studies "
            "conditional statements under precisely stated conjectures: satisfiability, three-sum, and weighted "
            "all-pairs shortest paths, in their respective models. The forbidden improvements are by a fixed "
            "power, not necessarily by logarithmic factors. <bookmark mark='b'/> Backurs and Indyk's "
            "edit-distance reduction says that a truly subquadratic algorithm would refute the relevant strong "
            "exponential-time hypothesis. This is conditional evidence, not an unconditional quadratic lower "
            "bound or a proof that every conjecture is equivalent. <bookmark mark='c'/> Reductions connect "
            "specific versions of problems. Their alphabet, weights, randomization and computational model "
            "matter."
        )
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(tab))
            vo.wait_until("b")
            self.play(FadeIn(pts[1]))
            vo.wait_until("c")
            self.play(FadeIn(pts[0]))
        self.wait(0.3)
        self.clear_scene()

    def open(self):
        head = label(r"Open questions", font_size=36).to_edge(UP, buff=0.35)
        qs = VGroup(
            label(r"integer sorting across word widths: fix instructions and randomness first", font_size=22, color=GREY_A),
            label(r"exact comparison optima beyond the small cases verified here", font_size=22,
                  color=GREY_A),
            label(r"which precise fine-grained conjectures admit reductions to each other?", font_size=22,
                  color=GREY_A),
            label(r"a theory of ``beyond the worst case'' that predicts real running times", font_size=22,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(head, DOWN, buff=0.6)
        star = label(r"$\bigstar$ \ the part's research problem takes the first one", font_size=22,
                     color=HEAD).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            (
            "Here are research directions, each needing a precise statement. <bookmark mark='a'/> Can "
            "integer-sorting bounds be improved across word widths, with a fixed permitted instruction set and a "
            "stated randomness guarantee? <bookmark mark='b'/> What are the exact optimal comparison counts "
            "beyond the small cases we checked? <bookmark mark='c'/> Which specific fine-grained conjectures "
            "admit reductions to each other? <bookmark mark='d'/> And which beyond-worst-case input models "
            "predict a chosen real workload well enough to test? <bookmark mark='e'/> The starred exercise starts "
            "by fixing a word-RAM model and checking the restrictions of known results, then proposing an "
            "extension or a reproducible finite experiment."
        )
        ) as vo:
            self.play(FadeIn(head))
            for mk, q in zip("abcd", qs):
                vo.wait_until(mk)
                self.play(FadeIn(q, shift=RIGHT * 0.1))
            vo.wait_until("e")
            self.play(FadeIn(star))
        self.wait(0.3)
        self.clear_scene()
