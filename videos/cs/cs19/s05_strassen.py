from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs19.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, grid_table, load,
                                   mono, words)

OMEGA = [(1969, 2.8074, r"Strassen"), (1978, 2.796, r"Pan"), (1979, 2.780, r"Bini et al."),
         (1981, 2.522, r"Sch\"onhage"), (1982, 2.496, r"Coppersmith, \ Winograd"), (1986, 2.479, r"Strassen"),
         (1990, 2.3755, r"Coppersmith, \ Winograd"), (2010, 2.3737, r"Stothers"),
         (2012, 2.3729, r"Vassilevska Williams"), (2014, 2.37286, r"Le Gall"),
         (2020, 2.37286, r"Alman, \ Vassilevska Williams"), (2023, 2.37187, r"Duan, \ Wu, \ Zhou"),
         (2024, 2.37134, r"Alman et al.")]


class Strassen(VoiceoverScene):
    def construct(self):
        self.card()
        self.seven()
        self.counts()
        self.omega()
        self.practice()

    def card(self):
        card = chapter_card(4, r"Seven products instead of eight", r"Is matrix multiplication really $n^3$?",
                            lit=(1969,), extra=((1969, r"Strassen"), (1990, r"Coppersmith and Winograd")), part=PART)
        with self.voiceover("Chapter four. Seven products instead of eight."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def seven(self):
        head = label(r"Strassen \ (1969): \ \textit{Gaussian elimination is not optimal}", font_size=32).to_edge(
            UP, buff=0.3)
        blocks = MathTex(r"\begin{pmatrix} C_{11} & C_{12} \\ C_{21} & C_{22} \end{pmatrix} = "
                         r"\begin{pmatrix} A_{11} & A_{12} \\ A_{21} & A_{22} \end{pmatrix}"
                         r"\begin{pmatrix} B_{11} & B_{12} \\ B_{21} & B_{22} \end{pmatrix}", font_size=30)
        blocks.to_edge(LEFT, buff=0.5).shift(UP * 1.6)
        naive = MathTex(r"C_{11} = A_{11}B_{11} + A_{12}B_{21}, \ \ldots: \ 8 \text{ block products}", font_size=26,
                        color=NO).next_to(blocks, DOWN, buff=0.3).align_to(blocks, LEFT)
        cols = [DATA, YES, HEAD, LAM, CTRL, NO, FUNC]
        ms = [r"M_1 = (A_{11} + A_{22})(B_{11} + B_{22})", r"M_2 = (A_{21} + A_{22})\,B_{11}",
              r"M_3 = A_{11}\,(B_{12} - B_{22})", r"M_4 = A_{22}\,(B_{21} - B_{11})",
              r"M_5 = (A_{11} + A_{12})\,B_{22}", r"M_6 = (A_{21} - A_{11})(B_{11} + B_{12})",
              r"M_7 = (A_{12} - A_{22})(B_{21} + B_{22})"]
        M = VGroup(*[MathTex(m, font_size=26, color=c) for m, c in zip(ms, cols)]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.14).to_edge(RIGHT, buff=0.5).shift(UP * 0.6)
        def cline(lhs, terms):
            parts = [lhs + r" ="]
            for k, (sign, m) in enumerate(terms):
                parts += ([sign] if k else []) + [rf"M_{m}"]
            t = MathTex(*parts, font_size=28)
            j = 1
            for k, (sign, m) in enumerate(terms):
                j += 1 if k else 0
                t[j].set_color(cols[m - 1])
                j += 1
            return t
        C = VGroup(cline(r"C_{11}", [("", 1), ("+", 4), ("-", 5), ("+", 7)]), cline(r"C_{12}", [("", 3), ("+", 5)]),
                   cline(r"C_{21}", [("", 2), ("+", 4)]), cline(r"C_{22}", [("", 1), ("-", 2), ("+", 3), ("+", 6)])
                   ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).next_to(naive, DOWN, buff=0.5).align_to(blocks, LEFT)
        rec = MathTex(r"T(n) = 7\,T(n/2) + O(n^2) = O(n^{\lg 7}) = O(n^{2.807})", font_size=32,
                      color=YES).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Nine years later Volker Strassen did the same to matrices, in a paper titled Gaussian elimination is "
            "not optimal. <bookmark mark='a'/> Split each matrix into four blocks. The product needs eight block "
            "products, two for each block of the answer. <bookmark mark='b'/> Strassen found seven products of "
            "sums and differences of blocks, coloured here, from which all four answer blocks follow by addition "
            "alone. <bookmark mark='c'/> They work because blocks need not commute: no step ever swaps the order of "
            "a product, so the identities hold for blocks, and the method recurses. <bookmark mark='d'/> Seven "
            "half-size products and some additions give n to the log of seven, about n to the two point eight "
            "one, against n cubed."
        ) as vo:
            self.play(FadeIn(head), FadeIn(blocks))
            vo.wait_until("a")
            self.play(FadeIn(naive))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(m, shift=LEFT * 0.1) for m in M], lag_ratio=0.25), run_time=3)
            vo.wait_until("c")
            self.play(FadeIn(C))
            vo.wait_until("d")
            self.play(FadeIn(rec))
        self.wait(0.3)
        self.clear_scene()

    def counts(self):
        d = load("strassen")
        head = label(r"Counting the operations", font_size=34).to_edge(UP, buff=0.3)
        rows = [[words(r["n"]), f"{r['naive_mults']:,}", f"{r['strassen_mults']:,}", f"{r['naive_adds']:,}",
                 f"{r['strassen_adds']:,}"] for r in d["counts"] if r["n"] in (2, 4, 16, 64, 256, 1024)]
        tab = grid_table([r"$n$", r"products, \ $n^3$", r"products, \ $7^{\lg n}$", r"additions, \ usual",
                          r"additions, \ Strassen"], rows, widths=[1.4, 2.8, 2.8, 2.8, 2.8], row_h=0.46, font_size=19,
                         colors=[[WHITE, NO, YES, GREY_A, LAM]] * len(rows)).next_to(head, DOWN, buff=0.5)
        last = d["counts"][-1]
        pts = VGroup(
            label(rf"at $n = 1024$: \ {last['naive_mults'] / last['strassen_mults']:.1f}$\times$ fewer products, \ "
                  rf"but {last['strassen_adds'] / last['naive_adds']:.1f}$\times$ more additions", font_size=22,
                  color=HEAD),
            label(r"the additions are $O(n^2)$ per level, \ so they lose in the end, \ but only for large $n$",
                  font_size=21, color=GREY_A),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Counted exactly, all the way down to single numbers. <bookmark mark='a'/> At a thousand by a thousand, "
            "Strassen does a quarter as many multiplications, but one and a half times as many additions, eighteen "
            "block additions per level instead of four. <bookmark mark='b'/> Asymptotically the additions do not "
            "matter, since they are only n squared per level; but they show why the method pays only for large "
            "matrices, and why real implementations stop recursing long before single numbers."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab))
            vo.wait_until("a")
            self.play(FadeIn(pts[0]))
            vo.wait_until("b")
            self.play(FadeIn(pts[1]))
        self.wait(0.3)
        self.clear_scene()

    def omega(self):
        head = label(r"The exponent $\omega$", font_size=34).to_edge(UP, buff=0.3)
        ax = Axes(x_range=[1965, 2028, 10], y_range=[2.0, 3.05, 0.2], x_length=8.2, y_length=4.6,
                  axis_config={"color": GREY_D, "include_numbers": False}).to_edge(LEFT, buff=0.9).shift(DOWN * 0.3)
        xt = VGroup(*[label(str(y), font_size=15, color=GREY_B).next_to(ax.c2p(y, 2.0), DOWN, buff=0.1)
                      for y in (1970, 1990, 2010)])
        yt = VGroup(*[label(f"{v:.1f}", font_size=15, color=GREY_B).next_to(ax.c2p(1965, v), LEFT, buff=0.1)
                      for v in (2.0, 2.4, 2.8)])
        three = DashedLine(ax.c2p(1965, 3.0), ax.c2p(2028, 3.0), color=NO, stroke_width=1.5)
        two = DashedLine(ax.c2p(1965, 2.0), ax.c2p(2028, 2.0), color=YES, stroke_width=1.5)
        steps = [(1965, 3.0)] + [(y, v) for y, v, _ in OMEGA] + [(2028, OMEGA[-1][1])]
        pts = []
        for (y0, v0), (y1, v1) in zip(steps, steps[1:]):
            pts += [ax.c2p(y0, v0), ax.c2p(y1, v0)]
        pts.append(ax.c2p(2028, OMEGA[-1][1]))
        line = VMobject(color=HEAD, stroke_width=3).set_points_as_corners(pts)
        dots = VGroup(*[Dot(ax.c2p(y, v), radius=0.05, color=HEAD) for y, v, _ in OMEGA])
        side = VGroup(
            label(r"$\omega$: \ the smallest exponent with $n^{\omega + \epsilon}$ multiplication", font_size=20,
                  color=GREY_A),
            label(r"1969: \ 2.807 \ (Strassen)", font_size=20, color=GREY_A),
            label(r"1990: \ 2.376 \ (Coppersmith and Winograd)", font_size=20, color=GREY_A),
            label(r"2024: \ 2.3713 \ (Alman, \ Duan, \ Vassilevska Williams, \ Xu, \ Xu, \ Zhou)", font_size=20,
                  color=HEAD),
            label(r"the lower bound: \ only $\omega \ge 2$", font_size=21, color=YES),
            label(r"the newer exponents are \textbf{galactic}: \ faster only for matrices too large to exist",
                  font_size=20, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(RIGHT, buff=0.35)
        if side.width > 5.2:
            side.scale_to_fit_width(5.2).to_edge(RIGHT, buff=0.35)
        with self.voiceover(
            "Strassen's paper started a race that is still going. <bookmark mark='a'/> Call omega the best exponent "
            "of matrix multiplication. <bookmark mark='b'/> Strassen brought it from three to two point eight "
            "one. <bookmark mark='c'/> In 1990 Don Coppersmith and Shmuel Winograd reached two point three seven "
            "six, by a far more indirect method, and nothing moved for twenty years. <bookmark mark='d'/> Since "
            "2010 a series of papers, most recently by Josh Alman, Ran Duan, Virginia Vassilevska Williams and "
            "three coauthors in 2024, have shaved it to two point three seven one three. <bookmark mark='e'/> The "
            "only lower bound is the obvious one, two: an answer has n squared entries to write. Many researchers "
            "suspect omega is two. <bookmark mark='f'/> None of the recent methods will ever run. Their constants "
            "are so large that they win only on matrices too big to exist, which Richard Lipton and Ken Regan call "
            "galactic algorithms."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xt), FadeIn(yt), Create(three), Create(two))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(line), FadeIn(dots), run_time=3)
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
            vo.wait_until("f")
            self.play(FadeIn(side[5]))
        self.wait(0.3)
        self.clear_scene()

    def practice(self):
        d = load("strassen")
        head = label(r"Strassen in practice", font_size=34).to_edge(UP, buff=0.3)
        rows = [[words(r["n"]), f"{r['numpy_s'] * 1000:.0f} ms" if r["numpy_s"] < 1 else f"{r['numpy_s']:.2f} s",
                 f"{r['strassen_s'] * 1000:.0f} ms" if r["strassen_s"] < 1 else f"{r['strassen_s']:.2f} s"]
                for r in d["timed"]]
        tab = grid_table([r"$n$", r"numpy's product \ (BLAS)", r"Strassen over numpy"], rows,
                         widths=[1.8, 3.8, 3.8], row_h=0.5, font_size=21,
                         colors=[[WHITE, YES, NO]] * len(rows)).next_to(head, DOWN, buff=0.5)
        pts = VGroup(
            label(r"a tuned $n^3$ product beats our Strassen at every size here: \ cache blocking, \ SIMD and four "
                  r"cores \ (Parts 9 and 10)", font_size=20, color=GREY_A),
            label(rf"and Strassen's rounding error was {d['err_strassen'] / d['err_numpy']:.0f}$\times$ larger in a "
                  r"test: \ the subtractions cancel digits", font_size=20, color=NO),
            label(r"used where it pays: \ very large matrices, \ exact arithmetic, \ some GPU libraries", font_size=20,
                  color=HEAD),
            label(r"2022: \ AlphaTensor searched for schemes, \ found 47 products for $4 \times 4$ mod 2 \ "
                  r"(Strassen: \ 49) \ (\textit{AI, Built}, \ Part 26)", font_size=20, color=LAM),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "And in practice? <bookmark mark='a'/> We timed Strassen's recursion, handing blocks of two hundred and "
            "fifty-six to numpy, against numpy's own product. The tuned cubic method won at every size, by three "
            "to five times, because it uses the cache blocking, vector instructions and four cores of Parts 9 and "
            "10, and does no extra additions. <bookmark mark='b'/> Strassen's subtractions also cost accuracy: in "
            "a test its rounding error was ten times larger. <bookmark mark='c'/> It is used where it pays, on "
            "very large matrices or exact arithmetic. <bookmark mark='d'/> The search for such schemes is not "
            "over. In 2022 DeepMind's AlphaTensor, a reinforcement learner, found a way to multiply four by four "
            "matrices with forty-seven products in arithmetic modulo two, where Strassen's method needs forty-nine."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab))
            for mk, p in zip("abcd", pts):
                vo.wait_until(mk)
                self.play(FadeIn(p))
        self.wait(0.3)
        self.clear_scene()
