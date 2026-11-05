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
            two(r"worst cases are often fragile:", r"perturb them slightly and they disappear", 21, GREY_A),
            two(r"\textbf{smoothed analysis} \ (Spielman and Teng, \ 2001):", r"the worst input, \ after random noise",
                21, YES),
            two(r"it explained why the simplex method,", r"exponential in the worst case, \ is fast in practice", 21,
                GREY_A),
            label(r"G\"odel Prize, \ 2008", font_size=19, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        if side.width > 5.6:
            side.scale_to_fit_width(5.6)
        side.to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "The worst case is a guarantee, and often a pessimistic one. The average assumes inputs are random, "
            "which they are not. Is there something in between? <bookmark mark='a'/> Take quicksort with the "
            "first element as pivot, on its worst input, a sorted array of two thousand keys. Now add a little "
            "random noise to every key, and measure. <bookmark mark='b'/> With no noise: two million comparisons. "
            "As the noise grows, the count falls, smoothly, all the way to the random-input average. A worst case "
            "this fragile does not survive contact with real data. <bookmark mark='c'/> Daniel Spielman and Shang-"
            "Hua Teng made this a theory in 2001: smoothed analysis measures the worst input after a random "
            "perturbation. It explained why the simplex method for linear programming, exponential in the worst "
            "case, is fast in practice, and won the Gödel Prize."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xt), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(Create(worst), FadeIn(wl), Create(avg), FadeIn(al), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(line), FadeIn(dots), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(side[1:]))
        self.wait(0.3)
        self.clear_scene()

    def integers(self):
        head = label(r"How fast can integers be sorted?", font_size=34).to_edge(UP, buff=0.3)
        rows = [[r"comparison sorts", r"$\Theta(n \log n)$", r"proved optimal"],
                [r"van Emde Boas trees \ (1975)", r"$O(n \log \log U)$", r"keys below $U$"],
                [r"fusion trees \ (Fredman and Willard, \ 1990)", r"$O(n \log n / \log \log n)$", r"first below $n \log n$"],
                [r"Andersson et al. \ (1995)", r"$O(n \log \log n)$", r"deterministic"],
                [r"Han and Thorup \ (2002)", r"$O(n \sqrt{\log \log n})$", r"expected"],
                [r"linear time?", r"$O(n)$", r"open"]]
        tab = grid_table([r"result", r"time for $n$ word-size integers", r""], rows, widths=[5.2, 4.2, 2.8],
                         row_h=0.5, font_size=20, mono_cols=(),
                         colors=[[WHITE, WHITE, GREY_B]] * 5 + [[HEAD, HEAD, HEAD]]).next_to(head, DOWN, buff=0.5)
        note = label(r"on the word-RAM, \ with words of $w \ge \log n$ bits and the usual arithmetic", font_size=20,
                     color=GREY_B).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Chapter ten's question has a long history. <bookmark mark='a'/> Comparison sorts are stuck at n log n. "
            "Sorting word-sized integers on a word-RAM is not: van Emde Boas trees, Fredman and Willard's fusion "
            "trees, the first to break n log n, then n log log n, and Han and Thorup's n times the square root of "
            "log log n, in 2002. <bookmark mark='b'/> Whether n integers can always be sorted in linear time is "
            "one of the oldest open questions in algorithms."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(tab.rule), *[FadeIn(c) for c in tab.cells[0]],
                      LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:6]], lag_ratio=0.3), run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(VGroup(*tab.cells[6])), FadeIn(note))
        self.wait(0.3)
        self.clear_scene()

    def finegrained(self):
        head = label(r"Fine-grained complexity", font_size=34).to_edge(UP, buff=0.3)
        rows = [[r"SETH: \ $k$-SAT needs $2^{(1 - o(1)) n}$ as $k$ grows", r"edit distance, \ longest common subsequence: "
                 r"\ no $n^{2 - \varepsilon}$ \ (Backurs and Indyk, \ 2015)"],
                [r"3SUM: \ no $n^{2 - \varepsilon}$ algorithm", r"many problems in computational geometry"],
                [r"APSP: \ no $n^{3 - \varepsilon}$ for all-pairs shortest paths", r"dozens of graph problems, \ "
                 r"equivalent to each other"]]
        tab = grid_table([r"if this conjecture holds", r"then these cannot be done faster"], rows, widths=[5.8, 6.6],
                         row_h=0.7, font_size=18, mono_cols=()).next_to(head, DOWN, buff=0.6)
        pts = VGroup(
            label(r"not ``polynomial or not'', \ but ``which polynomial'': \ reductions that preserve exponents",
                  font_size=21, color=GREY_A),
            label(r"explains why forty years of effort never beat quadratic edit distance", font_size=21, color=YES),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "The other frontier asks why some polynomial algorithms resist every improvement. <bookmark mark='a'/> "
            "Fine-grained complexity starts from a few precise conjectures. The strong exponential time hypothesis "
            "says satisfiability needs nearly two to the n time. The three-sum and all-pairs shortest paths "
            "conjectures say certain quadratic and cubic algorithms are essentially optimal. <bookmark mark='b'/> "
            "Then it builds reductions that keep track of exponents. Backurs and Indyk showed in 2015 that a truly "
            "subquadratic algorithm for edit distance would break the first conjecture, which explains why forty years of effort never found one. <bookmark mark='c'/> The question is no longer whether a problem is "
            "polynomial, but which polynomial."
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
            label(r"can $n$ word-size integers be sorted in $O(n)$ time?", font_size=22, color=GREY_A),
            label(r"the exact number of comparisons to sort $n$ items, \ for $n$ beyond about 20", font_size=22,
                  color=GREY_A),
            label(r"which conjectures of fine-grained complexity are true, \ and are they equivalent?", font_size=22,
                  color=GREY_A),
            label(r"a theory of ``beyond the worst case'' that predicts real running times", font_size=22,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(head, DOWN, buff=0.6)
        star = label(r"$\bigstar$ \ the part's research problem takes the first one", font_size=22,
                     color=HEAD).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Here is where the field stands. <bookmark mark='a'/> Can integers be sorted in linear time on a "
            "word-RAM? <bookmark mark='b'/> What is the exact number of comparisons needed to sort n items? It is "
            "known only for small n, and computing it is a search problem in its own right. <bookmark mark='c'/> "
            "Which of fine-grained complexity's conjectures are true, and are they secretly the same? <bookmark "
            "mark='d'/> And can a theory beyond the worst case predict how long real programs take on real data? "
            "<bookmark mark='e'/> This part's research problem takes up the first."
        ) as vo:
            self.play(FadeIn(head))
            for mk, q in zip("abcd", qs):
                vo.wait_until(mk)
                self.play(FadeIn(q, shift=RIGHT * 0.1))
            vo.wait_until("e")
            self.play(FadeIn(star))
        self.wait(0.3)
        self.clear_scene()
