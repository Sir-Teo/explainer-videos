from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs9.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, HIST, INF, NO, PART, YES, fmt, grid_table,
                                  load, mono)

IJK = ["for i: for j: for k:", "    C[i][j] += A[i][k] * B[k][j]   # B walks down a column"]
IKJ = ["for i: for k: for j:", "    C[i][j] += A[i][k] * B[k][j]   # every array walks along a row"]


class Programming(VoiceoverScene):
    def construct(self):
        self.card()
        self.order()
        self.measured()
        self.tiles()
        self.layout()

    def card(self):
        card = chapter_card(8, r"Programming for caches", r"Can the same arithmetic run seven times faster?",
                            part=PART)
        with self.voiceover("Chapter eight. Programming for caches."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def order(self):
        d = load("matmul")["sim"]
        head = label(r"Matrix multiply: \ the same operations, \ two orders", font_size=34).to_edge(UP, buff=0.35)
        a = VGroup(*[mono(s, 20) for s in IJK]).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        b = VGroup(*[mono(s, 20) for s in IKJ]).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        codes = VGroup(a, b).arrange(DOWN, aligned_edge=LEFT, buff=0.5).move_to(UP * 1.2)
        n = 8
        grid = VGroup(*[Square(side_length=0.32, stroke_color=GREY_D, stroke_width=1) for _ in range(n * n)])
        grid.arrange_in_grid(rows=n, cols=n, buff=0.02)
        col = VGroup(*[grid[r * n + 2].copy().set_fill(NO, opacity=0.7) for r in range(n)])
        row = VGroup(*[grid[2 * n + c].copy().set_fill(YES, opacity=0.7) for c in range(n)])
        lines_ = VGroup(*[Rectangle(width=4 * 0.34, height=0.34, stroke_color=HEAD, stroke_width=2).move_to(
            VGroup(grid[r * n], grid[r * n + 3])) for r in range(n)])
        bfig = VGroup(grid, lines_).scale(0.9).to_corner(DR, buff=0.6)
        bl = label(r"$B$ in memory: \ rows of lines", font_size=20, color=GREY_B).next_to(bfig, UP, buff=0.15)
        sim = d["rows"]
        res = VGroup(
            label(rf"down a column: \ a new line for every element \ ({sim['ijk']['8-way']:,} misses, \ $n = 64$, \ 8 KB)",
                  font_size=22, color=NO),
            label(rf"along a row: \ one line for every 8 elements \ ({sim['ikj']['8-way']:,} misses)", font_size=22,
                  color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_corner(DL, buff=0.5)
        with self.voiceover(
            "Now the programmer's side. Here are two ways to multiply matrices, with exactly the same arithmetic. "
            "<bookmark mark='a'/> In the textbook order, the innermost loop walks down a column of B. In C, a matrix "
            "is stored row after row, so consecutive elements of a column are a whole row apart: each one is in a "
            "different cache line. <bookmark mark='b'/> Swap the two inner loops, and the innermost loop walks along a "
            "row of B and a row of C. Now one cache line delivers eight doubles in a row. <bookmark mark='c'/> In our "
            "simulator, with an eight-kilobyte, eight-way cache, the column walk misses eight times as often. Part of "
            "that is conflict: the column's elements are a power of two apart, so they pile into the same few sets."
        ) as vo:
            self.play(FadeIn(head), FadeIn(bl), FadeIn(bfig))
            vo.wait_until("a")
            self.play(FadeIn(a))
            self.play(LaggedStart(*[FadeIn(c) for c in col], lag_ratio=0.15))
            vo.wait_until("b")
            self.play(FadeIn(b), FadeOut(col))
            self.play(LaggedStart(*[FadeIn(c) for c in row], lag_ratio=0.15))
            vo.wait_until("c")
            self.play(FadeIn(res))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def measured(self):
        m = load("matmul")
        g = m["gflops"]
        sizes = [str(s) for s in m["sizes"]]
        head = label(r"Measured on this computer: \ GFLOP/s, \ one core", font_size=34).to_edge(UP, buff=0.3)
        ax = Axes(x_range=[0, len(sizes) - 1, 1], y_range=[0, 4.5, 1], x_length=7.5, y_length=4.0, tips=False,
                  axis_config={"color": GREY_C, "font_size": 16}).move_to(LEFT * 1.6 + DOWN * 0.3)
        ax.y_axis.add_numbers([0, 1, 2, 3, 4], font_size=16, num_decimal_places=0)
        xt = VGroup(*[label(rf"$n = {s}$", font_size=18, color=GREY_B).next_to(ax.c2p(k, 0), DOWN, buff=0.12)
                      for k, s in enumerate(sizes)])
        curves = VGroup()
        labs = VGroup()
        for key, col, nm in (("ijk", NO, r"i-j-k"), ("ikj", DATA, r"i-k-j"), ("tiled", YES, r"tiled")):
            pts = [(k, g[key][s]) for k, s in enumerate(sizes) if s in g[key]]
            c = VMobject(color=col, stroke_width=4).set_points_as_corners([ax.c2p(x, y) for x, y in pts])
            curves.add(c)
            labs.add(label(nm, font_size=22, color=col).next_to(ax.c2p(*pts[-1]), RIGHT, buff=0.15))
        blas = g["blas"]
        side = VGroup(
            label(rf"a tuned library \ (numpy's BLAS, \ all cores, \ wide vectors): \ {blas['2048']:.0f} GFLOP/s",
                  font_size=22, color=HEAD),
            label(r"Part 10 and \textit{AI, Built} 17 explain the rest", font_size=20, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(RIGHT, buff=0.4).shift(UP * 1.6)
        with self.voiceover(
            "Now the real thing, in C, on this computer, for matrices from two hundred fifty-six to two thousand and "
            "forty-eight on a side. <bookmark mark='a'/> The textbook order starts at two billion operations a second "
            "and falls to half a billion as the matrices outgrow the caches. <bookmark mark='b'/> The swapped order "
            "is two to six times faster, until at two thousand and forty-eight the matrices are thirty-two "
            "megabytes each and even it starts to sink. <bookmark mark='c'/> The tiled version, which the next "
            "picture explains, holds steady at every size. <bookmark mark='d'/> And a tuned library does thirty times "
            "better again, using every core and the widest vector instructions, which is Part 10's subject."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xt))
            for mk, k in zip("abc", range(3)):
                vo.wait_until(mk)
                self.play(Create(curves[k]), FadeIn(labs[k]), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(side))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def tiles(self):
        head = label(r"Tiling: \ finish with a block while it is still in the cache", font_size=32).to_edge(UP, buff=0.35)
        n, T = 8, 4

        def mat(color, name):
            g = VGroup(*[Square(side_length=0.3, stroke_color=GREY_D, stroke_width=1) for _ in range(n * n)])
            g.arrange_in_grid(rows=n, cols=n, buff=0.02)
            return VGroup(g, label(name, font_size=26, color=color).next_to(g, UP, buff=0.12))

        A, B, Cm = mat(DATA, r"$A$"), mat(CTRL, r"$B$"), mat(YES, r"$C$")
        eq = VGroup(Cm, MathTex(r"=", font_size=40), A, MathTex(r"\times", font_size=40), B).arrange(RIGHT, buff=0.4)
        eq.move_to(UP * 0.3)

        def block(m, bi, bj, color):
            cells = VGroup(*[m[0][(bi * T + r) * n + bj * T + c] for r in range(T) for c in range(T)])
            return SurroundingRectangle(cells, color=color, buff=0.03, stroke_width=4)

        steps = [(0, 0, 0), (0, 0, 1), (0, 1, 0), (0, 1, 1)]
        hl = VGroup()
        expl = label(r"$C_{IJ} \mathrel{+}= A_{IK} B_{KJ}$: \ three $T \times T$ blocks, \ $3T^2 \le$ the cache",
                     font_size=28, color=HEAD).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Tiling attacks the problem directly. Cut each matrix into square blocks, small enough that three of them "
            "fit in the cache together. <bookmark mark='a'/> Then multiply block by block: a block of C accumulates "
            "the products of a row of blocks of A with a column of blocks of B. While one block of each is in the "
            "cache, every element in it is used T times before it is thrown out, instead of once. <bookmark "
            "mark='b'/> The condition is only that three blocks fit: three T-squared numbers no more than the cache. "
            "Choose T for the cache you have, and the traffic to memory falls by a factor of about T."
        ) as vo:
            self.play(FadeIn(head), FadeIn(eq))
            vo.wait_until("a")
            for i, j, k in steps:
                new = VGroup(block(Cm, i, j, YES), block(A, i, k, DATA), block(B, k, j, CTRL))
                if len(hl):
                    self.play(Transform(hl, new), run_time=0.8)
                else:
                    hl = new
                    self.play(Create(hl), run_time=0.8)
                self.wait(0.4)
            vo.wait_until("b")
            self.play(FadeIn(expl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def layout(self):
        head = label(r"Data layout: \ arrays of structs, \ structs of arrays", font_size=34).to_edge(UP, buff=0.35)
        aos = mono("struct {x, y, z, mass, colour, id...} particles[N];", 20)
        soa = mono("float x[N], y[N], z[N], mass[N] ...;", 20)
        g = VGroup(label(r"array of structs", font_size=24, color=NO), aos, label(r"struct of arrays", font_size=24,
                                                                                  color=YES), soa).arrange(
            DOWN, aligned_edge=LEFT, buff=0.2).move_to(UP * 0.8)
        notes = VGroup(
            label(r"a loop that reads only \texttt{x}: \ with structs, \ most of every line is wasted", font_size=24,
                  color=GREY_A),
            label(r"game engines (``data-oriented design''), \ column stores in databases, \ numerical codes", font_size=24,
                  color=HEAD),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "The same reasoning shapes data. <bookmark mark='a'/> An array of structures keeps all the fields of one "
            "particle together; a structure of arrays keeps each field in its own array. <bookmark mark='b'/> A loop "
            "that reads only the x coordinates of every particle wastes most of every cache line in the first layout, "
            "and uses all of it in the second. Game engines call the second style data-oriented design; databases "
            "that store each column separately, which Part 35 builds, are the same idea at scale."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(g))
            vo.wait_until("b")
            self.play(FadeIn(notes))
        self.wait(0.3)
        self.clear_scene()
