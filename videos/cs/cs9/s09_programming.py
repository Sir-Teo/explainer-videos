from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs9.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, HIST, INF, NO, PART, YES, fmt, grid_table,
                                  load, mono, plot_range)

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
        card = chapter_card(8, r"Programming for caches", "How does address order change data reuse?",
                            part=PART)
        with self.voiceover(
            "Chapter eight. Programming for caches."
        ):
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
        lines_ = VGroup(*[Rectangle(width=8 * 0.34, height=0.34, stroke_color=HEAD, stroke_width=2).move_to(
            VGroup(grid[r * n], grid[r * n + 7])) for r in range(n)])
        bfig = VGroup(grid, lines_).scale(0.9).to_corner(DR, buff=0.6)
        # Copy highlights after positioning the grid, so they stay on its cells.
        col = VGroup(*[grid[r * n + 2].copy().set_fill(NO, opacity=0.7) for r in range(n)])
        row = VGroup(*[grid[2 * n + c].copy().set_fill(YES, opacity=0.7) for c in range(n)])
        bl = label(r"$B$ in memory: \ rows of lines", font_size=20, color=GREY_B).next_to(bfig, UP, buff=0.15)
        sim = d["rows"]
        res = VGroup(
            label(rf"down a column: \ a new line for every element \ ({sim['ijk']['8-way']:,} misses, \ $n = 64$, \ 8 KiB)",
                  font_size=22, color=NO),
            label(rf"along a row: \ one line for every 8 elements \ ({sim['ikj']['8-way']:,} misses)", font_size=22,
                  color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_corner(DL, buff=0.5)
        with self.voiceover(
            "Loop order changes the address stream even when the intended matrix product is unchanged. <bookmark "
            "mark='a'/> With row-major doubles, walking a column of B separates successive elements by a row stride. "
            "In the shown sizes that spreads accesses across lines and can create set conflicts. <bookmark "
            "mark='b'/> Interchanging the inner loops makes the innermost traversal contiguous in B and C, giving "
            "several nearby elements per sixty-four-byte line. Floating-point order, vectorization and compiler "
            "transformations still deserve attention. <bookmark mark='c'/> The miss counts below come from a small "
            "explicit address-trace simulation with its stated capacity, associativity and line size. They count "
            "allocation misses, not total physical traffic or a measured cache-only explanation of the C benchmark's "
            "speedup."
        ) as vo:
            self.play(FadeIn(head), FadeIn(bl), FadeIn(bfig))
            self.play(FadeIn(a))
            vo.wait_until("a")
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
        head = label(r"C kernels measured here: \ GFLOP/s", font_size=34).to_edge(UP, buff=0.3)
        ymax, ystep = plot_range(v for k in ("ijk", "ikj", "tiled") for v in g[k].values())
        ax = Axes(x_range=[0, len(sizes) - 1, 1], y_range=[0, ymax, ystep], x_length=7.5, y_length=4.0, tips=False,
                  axis_config={"color": GREY_C, "font_size": 16}).move_to(LEFT * 1.6 + DOWN * 0.3)
        ax.y_axis.add_numbers(np.arange(0, ymax + ystep / 2, ystep).tolist(), font_size=16, num_decimal_places=0)
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
            label(rf"NumPy BLAS \ (separate library/settings): \ {blas['2048']:.0f} GFLOP/s",
                  font_size=22, color=HEAD),
            label("timing alone does not isolate cache, vector or thread effects", font_size=20, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(RIGHT, buff=0.4).shift(UP * 1.6)
        with self.voiceover(
            "These are host-dependent timings of the shown C kernels, compiled with optimization and native "
            "instruction selection. The work estimate uses two n-cubed floating-point operations. <bookmark "
            "mark='a'/> The i-j-k kernel is measured only through size one thousand twenty-four; there is no "
            "measured point at two thousand forty-eight for that curve. <bookmark mark='b'/> The interchanged loop "
            "and <bookmark mark='c'/> the fixed-tile kernel have their own curves. Their rankings and slopes are "
            "observations from these runs, not universal size trends. Each C variant is timed once, and zero "
            "initialization is included in some variants. <bookmark mark='d'/> NumPy's BLAS result uses a separate "
            "library implementation and timing path. Vectorization, packing, threading and compiler choices can all "
            "differ; this comparison does not isolate one optimization or verify use of every core."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xt))
            for mk, k in zip("abc", range(3)):
                if mk != 'a':
                    vo.wait_until(mk)
                self.play(Create(curves[k]), FadeIn(labs[k]), run_time=1.5)
                if mk == 'a':
                    vo.wait_until(mk)
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
            "Tiling tries to reuse a small set of matrix values before moving on. Three square tiles give a useful "
            "first capacity estimate, with T squared values per tile. <bookmark mark='a'/> A C tile accumulates "
            "products from matching A and B tiles. The actual loop nesting determines which tile stays resident "
            "across the reduction loop; not every tile is necessarily retained or reused T times in the same way. "
            "<bookmark mark='b'/> Three T-squared values fitting is a sufficient storage sketch for a simple blocked "
            "scheme, not a complete performance condition. Associativity, line layout, registers, vector "
            "instructions, write traffic and other data also consume resources. Under the classical multiplication "
            "model, suitable blocking reduces the leading movement scale to n cubed over T, with constants depending "
            "on the schedule."
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
        lay = load("layout")
        notes = VGroup(
            label(rf"summing \texttt{{x}} over {lay['n'] / 1e6:.1f} million particles here: \ "
                  rf"{1000 * lay['structs']:.1f} ms as 64-byte structs, \ {1000 * lay['array']:.1f} ms as an array \ "
                  rf"({lay['structs'] / lay['array']:.1f} times)", font_size=24, color=YES),
            label(r"game engines (``data-oriented design''), \ column stores in databases, \ numerical codes", font_size=24,
                  color=HEAD),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Layout determines which fields share a line. <bookmark mark='a'/> An array of structures groups one "
            "object's fields; a structure of arrays groups corresponding fields from many objects. Neither is "
            "universally better. <bookmark mark='b'/> This loop reads only the x field. The structure has sixty-four "
            "bytes per object, while the compact float array stores x values consecutively, reducing the address "
            "footprint and unused fields brought in. The displayed best-of-five times come from the same specified "
            "summation and compiler options. Cache state, vectorization, translation and bandwidth can all "
            "contribute, so timing alone does not isolate one cause. Workloads that use several fields together may "
            "favor a different layout or a blocked hybrid."
        ) as vo:
            self.play(FadeIn(head))
            self.play(FadeIn(g))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(FadeIn(notes))
        self.wait(0.3)
        self.clear_scene()
