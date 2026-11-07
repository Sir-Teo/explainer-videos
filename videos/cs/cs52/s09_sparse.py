from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs52.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, code_block, grid_table, load, mono


def pattern(rows, size=26, color=WHITE):
    """A matrix of x's and zeros, the shape of a matrix or of its factor."""
    m = Matrix([[r"\times" if c == "x" else r"0" for c in r] for r in rows],
               element_to_mobject_config={"font_size": size, "color": color}, h_buff=0.55, v_buff=0.45)
    for e, c in zip(m.get_entries(), "".join(rows)):
        if c == "0":
            e.set_color(GREY_D)
    return m


def poisson_dense(m: int) -> list[list[float]]:
    """The 5-point Laplacian on an m x m grid, numbered row by row (the structure of iterative.poisson2d)."""
    n = m * m
    A = [[0.0] * n for _ in range(n)]
    for i in range(m):
        for j in range(m):
            k = i * m + j
            A[k][k] = 4.0
            for di, dj in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                if 0 <= i + di < m and 0 <= j + dj < m:
                    A[k][(i + di) * m + j + dj] = -1.0
    return A


def nested_order(m: int) -> list[int]:
    """Nested dissection of an m x m grid, as in iterative.nested_dissection: the halves, then the separator."""
    order = []

    def rec(r0, r1, c0, c1):
        if r1 - r0 <= 2 or c1 - c0 <= 2:
            order.extend(i * m + j for i in range(r0, r1) for j in range(c0, c1))
            return
        if r1 - r0 >= c1 - c0:
            mid = (r0 + r1) // 2
            rec(r0, mid, c0, c1)
            rec(mid + 1, r1, c0, c1)
            order.extend(mid * m + j for j in range(c0, c1))
        else:
            mid = (c0 + c1) // 2
            rec(r0, r1, c0, mid)
            rec(r0, r1, mid + 1, c1)
            order.extend(i * m + mid for i in range(r0, r1))

    rec(0, m, 0, m)
    return order


def size_text(b: int) -> str:
    return f"{b / 1e6:,.0f} MB" if b >= 1e6 else f"{b / 1e3:,.1f} kB"


class Sparse(VoiceoverScene):
    def construct(self):
        self.card()
        self.poisson()
        self.csr()
        self.fill()
        self.orderings()
        self.measured()

    def card(self):
        card = chapter_card(8, r"Sparse matrices", r"How do we store and factor a matrix that is almost all zeros?",
                            lit=(1957, 1961, 1973), extra=((1957, r"Markowitz: \ sparse pivoting"),
                                                           (1961, r"Parter: \ elimination as a graph"),
                                                           (1973, r"George: \ nested dissection")), part=PART)
        with self.voiceover("Chapter eight. Sparse matrices."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def poisson(self):
        head = label(r"Where sparse matrices come from: \ Poisson's equation", font_size=36).to_edge(UP, buff=0.3)
        m, sp_ = 6, 0.62
        C = np.array([-4.75, -0.35, 0])
        x0 = C + np.array([-(m + 1) * sp_ / 2, -(m + 1) * sp_ / 2, 0])
        frame = Square(side_length=(m + 1) * sp_, color=GREY_C, stroke_width=2).move_to(C)
        dots = VGroup(*[Dot(x0 + np.array([(j + 1) * sp_, (i + 1) * sp_, 0]), radius=0.05, color=GREY_B)
                        for i in range(m) for j in range(m)])
        ec = label(r"$u = 0$ on the edge", font_size=17, color=GREY_B).next_to(frame, DOWN, buff=0.15)
        ci, cj = 2, 3

        def P(i, j):
            return x0 + np.array([(j + 1) * sp_, (i + 1) * sp_, 0])
        nb = [(ci - 1, cj), (ci + 1, cj), (ci, cj - 1), (ci, cj + 1)]
        arms = VGroup(*[Line(P(ci, cj), P(i, j), color=HEAD, stroke_width=3) for i, j in nb])
        cdot = Dot(P(ci, cj), radius=0.11, color=HEAD)
        ndots = VGroup(*[Dot(P(i, j), radius=0.09, color=DATA) for i, j in nb])
        cval = MathTex(r"4", font_size=26, color=HEAD).next_to(cdot, UR, buff=0.04)
        nvals = VGroup(*[MathTex(r"-1", font_size=24, color=DATA).next_to(P(i, j), d, buff=0.12)
                         for (i, j), d in zip(nb, (DOWN, UP, LEFT, RIGHT))])
        top_y = frame.get_top()[1]
        hb = BraceBetweenPoints([P(0, 0)[0], top_y, 0], [P(0, 1)[0], top_y, 0], UP, color=GREY_B)
        hl = MathTex(r"h", font_size=24, color=GREY_B).next_to(hb, UP, buff=0.05)
        cols = {r"u''(x)": HEAD}
        rows = VGroup(
            cmath(r"-\nabla^2 u", r"=", r"f", font_size=32),
            cmath(r"u(x+h) + u(x-h)", r"=", r"2u(x)", r"+", r"h^2", r"u''(x)", r"+", r"O(h^4)", colors=cols,
                  font_size=32),
            cmath(r"-", r"u''(x)", r"\approx", r"\frac{-u(x-h) + 2u(x) - u(x+h)}{h^2}", colors=cols, font_size=32),
            cmath(r"4u_{i,j} - u_{i-1,j} - u_{i+1,j} - u_{i,j-1} - u_{i,j+1}", r"=", r"h^2 f_{i,j}",
                  font_size=32),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).move_to([2.6, 0.3, 0])
        rows[3][0].set_color(HEAD)
        whys = VGroup(
            label(r"Poisson's equation: \ steady heat, \ electric potential, \ pressure", font_size=18,
                  color=GREY_B),
            label(r"add the Taylor series of $u(x \pm h)$: \ the odd terms cancel", font_size=18, color=GREY_B),
            label(r"the second difference", font_size=18, color=GREY_B),
            label(r"the same in $y$, \ added: \ the five-point stencil", font_size=18, color=HEAD),
        )
        for w, r in zip(whys, rows):
            w.next_to(r, DOWN, buff=0.1).align_to(r, LEFT)
        with self.voiceover(
            "The matrices of chapters seven and nine come from equations like Poisson's, which governs steady "
            "heat, electric potential and pressure. <bookmark mark='a'/> We want u on a square, given f, with u "
            "zero on the edge. Sample u on a grid with spacing h. <bookmark mark='b'/> Adding the Taylor series of "
            "u at x plus h and at x minus h cancels the odd terms, <bookmark mark='c'/> so the second derivative "
            "becomes a second difference, divided by h squared. <bookmark mark='d'/> Do the same in y and add: each "
            "grid point is coupled to its four neighbours, four times itself minus each neighbour once. That is one "
            "equation per grid point, with at most five unknowns in each."
        ) as vo:
            self.play(FadeIn(head), Write(rows[0]), FadeIn(whys[0]))
            vo.wait_until("a")
            self.play(Create(frame), FadeIn(dots), FadeIn(ec), GrowFromCenter(hb), FadeIn(hl))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(whys[1]))
            vo.wait_until("c")
            self.play(TransformMatchingTex(rows[1].copy(), rows[2]), FadeIn(whys[2]))
            vo.wait_until("d")
            self.play(Create(arms), FadeIn(cdot), FadeIn(ndots), FadeIn(cval), FadeIn(nvals))
            self.play(FadeIn(rows[3]), FadeIn(whys[3]))
        self.wait(0.4)
        self.clear_scene()

    def csr(self):
        rows_ = load("fill")["rows"]
        head = label(r"Storing only the nonzeros: \ CSR", font_size=36).to_edge(UP, buff=0.3)
        A = poisson_dense(2)
        M = Matrix([[f"{v:g}" for v in r] for r in A], element_to_mobject_config={"font_size": 26},
                   h_buff=0.75, v_buff=0.5)
        for e, v in zip(M.get_entries(), [v for r in A for v in r]):
            e.set_color(HEAD if v != 0 else GREY_D)
        val, col, ptr = [], [], [0]
        for r in A:
            for j, v in enumerate(r):
                if v != 0:
                    val.append(v)
                    col.append(j)
            ptr.append(len(val))
        arr = VGroup(mono("val = [" + " ".join(f"{v:>2g}" for v in val) + "]", size=17, color=HEAD),
                     mono("col = [" + " ".join(f"{v:>2d}" for v in col) + "]", size=17, color=DATA),
                     mono("ptr = [" + " ".join(f"{v:>2d}" for v in ptr) + "]", size=17, color=YES))
        arr.arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        names = VGroup(label(r"the nonzeros, \ row by row", font_size=17, color=GREY_B),
                       label(r"their column numbers", font_size=17, color=GREY_B),
                       label(r"where each row starts", font_size=17, color=GREY_B))
        for nm, a in zip(names, arr):
            nm.next_to(a, RIGHT, buff=0.3)
        Ml = label(r"a $2 \times 2$ grid's matrix", font_size=17, color=GREY_A).next_to(M, DOWN, buff=0.12)
        top = VGroup(VGroup(M, Ml), VGroup(arr, names)).arrange(RIGHT, buff=0.6).next_to(head, DOWN, buff=0.4)
        code = code_block(["for i in range(n):", "    s = 0.0", "    for k in range(ptr[i], ptr[i + 1]):",
                           "        s += val[k] * x[col[k]]", "    y[i] = s"], size=15)
        code[3].set_color(KERN)
        cnote = wrapped_label(r"two flops per nonzero; \ \texttt{x[col[k]]} is a scattered load, \ so the product "
                              r"is limited by memory bandwidth \ (Part 9)", 4.6, font_size=17, color=KERN)
        left = VGroup(code, cnote).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        trs = [[f"{r['m']} $\\times$ {r['m']}", f"{r['n']:,}", f"{r['nnz_A']:,}", size_text(r["csr_bytes"]),
                size_text(r["dense_bytes"])] for r in rows_]
        tab = grid_table([r"grid", r"unknowns", r"nonzeros", r"CSR", r"dense"], trs,
                         widths=[1.4, 1.3, 1.35, 1.25, 1.25], row_h=0.44, font_size=18, mono_cols=())
        for c in tab.cells[1:]:
            c[3].set_color(YES)
            c[4].set_color(NO)
        tcap = label(r"the Poisson matrix, \ computed", font_size=17, color=GREY_A)
        right = VGroup(tcap, tab).arrange(DOWN, buff=0.2)
        VGroup(left, right).arrange(RIGHT, buff=0.7, aligned_edge=UP).next_to(top, DOWN, buff=0.55)
        big = rows_[-1]
        with self.voiceover(
            "Number the grid points row by row, and almost every entry of the matrix is zero. "
            "<bookmark mark='a'/> Compressed sparse row format stores only the nonzeros: their values, row by row, "
            "<bookmark mark='b'/> their column numbers, <bookmark mark='c'/> and where each row starts. "
            "<bookmark mark='d'/> Multiplying by a vector walks those arrays once, two operations per nonzero. "
            "Each load of x at a column number lands somewhere unpredictable, so the product is limited by memory "
            "bandwidth, as in Part 9. <bookmark mark='e'/> For a sixty-four by sixty-four grid, four thousand and "
            f"ninety-six unknowns, the matrix has {big['nnz_A']:,} nonzeros: about two hundred and sixty kilobytes "
            "in this format, against a hundred and thirty-four megabytes stored densely."
        ) as vo:
            self.play(FadeIn(head), FadeIn(M), FadeIn(Ml))
            for mk, a, nm in zip("abc", arr, names):
                vo.wait_until(mk)
                self.play(FadeIn(a, shift=RIGHT * 0.1), FadeIn(nm))
            vo.wait_until("d")
            self.play(FadeIn(left))
            vo.wait_until("e")
            self.play(FadeIn(tcap), FadeIn(tab.rule), FadeIn(VGroup(*tab.cells[0])),
                      LaggedStart(*[FadeIn(VGroup(*c)) for c in tab.cells[1:]], lag_ratio=0.3))
        self.wait(0.4)
        self.clear_scene()

    def fill(self):
        rows_ = load("fill")["rows"]
        big = rows_[-1]
        head = label(r"Fill-in: \ the order of elimination matters", font_size=36).to_edge(UP, buff=0.3)
        n = 6

        def arrow(hub_first):
            h = 0 if hub_first else n - 1
            return ["".join("x" if (i == j or i == h or j == h) else "0" for j in range(n)) for i in range(n)]

        def star(hub_first):
            hub = Dot(radius=0.13, color=HEAD)
            leaves = VGroup(*[Dot([0.85 * math.cos(math.pi / 2 + 2 * math.pi * k / 5),
                                   0.85 * math.sin(math.pi / 2 + 2 * math.pi * k / 5), 0], radius=0.1, color=DATA)
                              for k in range(5)])
            spokes = VGroup(*[Line(hub.get_center(), lf.get_center(), color=GREY_B, stroke_width=2,
                                   buff=0.1) for lf in leaves])
            return VGroup(spokes, hub, leaves)
        rowsv = VGroup()
        for hub_first in (True, False):
            pat = pattern(arrow(hub_first), size=22)
            pat.scale_to_fit_width(3.0)
            g = star(hub_first)
            t = label(r"hub first" if hub_first else r"hub last", font_size=20, color=HEAD)
            rowsv.add(VGroup(t, pat, g))
        for rv, y in zip(rowsv, (1.05, -1.95)):
            rv[1].move_to([-5.0, y, 0])
            rv[2].move_to([-2.0, y, 0])
            rv[0].next_to(rv[1], UP, buff=0.08)
        # hub first: the five leaves become a clique, and the factor fills
        pat0, g0 = rowsv[0][1], rowsv[0][2]
        leaves0 = g0[2]
        clique = VGroup(*[Line(leaves0[a].get_center(), leaves0[b].get_center(), color=NO, stroke_width=2.5,
                               buff=0.1) for a in range(5) for b in range(a + 1, 5)])
        ents0 = pat0.get_entries()
        news = VGroup()
        for i in range(1, n):
            for j in range(1, n):
                if i != j:
                    e = ents0[i * n + j]
                    news.add(MathTex(r"\times", font_size=22, color=NO).match_height(ents0[0]).move_to(e))
        olds = VGroup(*[ents0[i * n + j] for i in range(1, n) for j in range(1, n) if i != j])
        pat1, g1 = rowsv[1][1], rowsv[1][2]
        rule = VGroup(
            wrapped_label(r"eliminating an unknown couples all of its neighbours to one another: \ Parter's graph "
                          r"view \ (1961)", 5.6, font_size=19, color=WHITE),
            wrapped_label(r"hub first: \ every pair of the others becomes coupled; \ the factor fills in completely",
                          5.6, font_size=19, color=NO),
            wrapped_label(r"hub last: \ each leaf has only the hub as neighbour; \ nothing fills in", 5.6,
                          font_size=19, color=YES),
            wrapped_label(rf"the $64 \times 64$ grid numbered row by row: \ the Cholesky factor has {big['natural']:,} "
                          rf"nonzeros, \ the matrix {big['nnz_A']:,}", 5.6, font_size=19, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([3.7, -0.1, 0])
        ill = note(r"illustrative arrow matrix", font_size=16).next_to(rowsv[1], DOWN, buff=0.2)
        with self.voiceover(
            "Direct solvers factor the matrix, and there sparsity is fragile. <bookmark mark='a'/> In this arrow "
            "matrix one unknown, the hub, is coupled to all the others. Seymour Parter's view of elimination, from "
            "1961, is a graph: eliminating an unknown couples all of its neighbours to one another. "
            "<bookmark mark='b'/> Eliminate the hub first and every pair of the others becomes coupled: the factor "
            "fills in completely. <bookmark mark='c'/> Eliminate it last, and nothing fills in at all. Same matrix, "
            "same answer; only the order differs. <bookmark mark='d'/> On the sixty-four by sixty-four grid, "
            "numbered row by row, the Cholesky factor has two hundred and sixty-two thousand nonzeros, "
            f"{big['natural'] / big['nnz_A']:.0f} times as many as the matrix."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rowsv), FadeIn(ill))
            vo.wait_until("a")
            self.play(FadeIn(rule[0]))
            vo.wait_until("b")
            self.play(g0[1].animate.set_color(GREY_D), g0[0].animate.set_stroke(opacity=0.25))
            self.play(Create(clique), FadeOut(olds), FadeIn(news), FadeIn(rule[1]), run_time=1.5)
            vo.wait_until("c")
            for lf in g1[2]:
                self.play(lf.animate.set_color(GREY_D), run_time=0.25)
            self.play(FadeIn(rule[2]), Indicate(pat1, color=YES, scale_factor=1.05))
            vo.wait_until("d")
            self.play(FadeIn(rule[3]))
        self.wait(0.4)
        self.clear_scene()

    def order_grid(self, order, m=16, cell=0.19):
        rank = {k: r for r, k in enumerate(order)}
        g = VGroup()
        for i in range(m):
            for j in range(m):
                k = i * m + j
                a = rank[k] / (m * m - 1)
                g.add(Square(side_length=cell, stroke_color=BG, stroke_width=0.6,
                             fill_color=interpolate_color(ManimColor(DATA), ManimColor(HEAD), a ** 1.5),
                             fill_opacity=1).move_to([j * cell, -i * cell, 0]))
        seq = [g[k] for k in order]
        return g, seq

    def orderings(self):
        m = 16
        head = label(r"Orderings: \ minimum degree, \ nested dissection", font_size=36).to_edge(UP, buff=0.3)
        gn, sn = self.order_grid(list(range(m * m)))
        gd, sd = self.order_grid(nested_order(m))
        gn.move_to([-4.6, 0.35, 0])
        gd.move_to([-0.9, 0.35, 0])
        ln = label(r"row by row", font_size=19, color=GREY_A).next_to(gn, DOWN, buff=0.2)
        ld = label(r"nested dissection", font_size=19, color=GREY_A).next_to(gd, DOWN, buff=0.2)
        key = VGroup(Square(0.22, stroke_width=0, fill_color=DATA, fill_opacity=1),
                     label(r"eliminated first", font_size=16, color=GREY_B),
                     Square(0.22, stroke_width=0, fill_color=HEAD, fill_opacity=1),
                     label(r"last", font_size=16, color=GREY_B)).arrange(RIGHT, buff=0.12)
        key.next_to(VGroup(ln, ld), DOWN, buff=0.3)
        txt = VGroup(
            wrapped_label(r"row by row, \ the front of half-eliminated unknowns couples everything behind it to "
                          r"everything ahead: \ a band of width $m$ fills", 4.4, font_size=18, color=WHITE),
            wrapped_label(r"\textbf{minimum degree} \ (after Markowitz, \ 1957): \ always eliminate the unknown with "
                          r"the fewest neighbours; \ greedy, \ and very good", 4.4, font_size=18, color=YES),
            wrapped_label(r"\textbf{nested dissection} \ (George, \ 1973): \ cut the grid with a line of unknowns, "
                          r"\ number the line last, \ recurse on the halves; \ on a 2D grid, \ fill "
                          r"$O(n \log n)$ \ and work $O(n^{3/2})$, \ the best possible order", 4.4, font_size=18,
                          color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([4.5, 0.1, 0])
        with self.voiceover(
            "So the order of elimination is the whole game. <bookmark mark='a'/> Numbered row by row, the grid is "
            "eliminated like a broom sweeping a floor, and the front of partly eliminated unknowns couples "
            "everything behind it to everything ahead: a band of width m fills completely. <bookmark mark='b'/> "
            "Minimum degree, a greedy rule that goes back to Harry Markowitz in 1957, always eliminates the unknown "
            "with the fewest neighbours next. <bookmark mark='c'/> Nested dissection, Alan George's idea of 1973, "
            "cuts the grid in two with a line of unknowns, numbers the line last, and does the same to each half. "
            "<bookmark mark='d'/> On a two-dimensional grid its fill grows like n log n and its work like n to the "
            "three halves, which is the best possible order of growth."
        ) as vo:
            self.play(FadeIn(head), FadeIn(key))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c) for c in sn], lag_ratio=0.02), FadeIn(ln), FadeIn(txt[0]),
                      run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(txt[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(c) for c in sd], lag_ratio=0.02), FadeIn(ld), run_time=4)
            vo.wait_until("d")
            self.play(FadeIn(txt[2]))
        self.wait(0.4)
        self.clear_scene()

    def measured(self):
        rows_ = load("fill")["rows"]
        big, prev = rows_[-1], rows_[-2]
        head = label(r"What the orderings buy", font_size=36).to_edge(UP, buff=0.3)
        specs = [(r"the matrix $A$ itself", "nnz_A", GREY_B), (r"row by row", "natural", NO),
                 (r"reverse Cuthill--McKee", "rcm", KERN), (r"minimum degree", "min_degree", YES),
                 (r"nested dissection", "nested", HEAD)]
        vmax = big["natural"]
        bars = VGroup()
        for name, key, c in specs:
            nm = label(name, font_size=19, color=c)
            b = Rectangle(width=max(0.03, 6.4 * big[key] / vmax), height=0.36, stroke_width=0, fill_color=c,
                          fill_opacity=0.85)
            v = label(f"{big[key]:,}", font_size=19, color=c)
            bars.add(VGroup(nm, b, v))
        bars.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        for r in bars:
            r[0].align_to([-2.4, 0, 0], RIGHT)
            r[1].next_to([-2.2, r[0].get_y(), 0], RIGHT, buff=0)
            r[2].next_to(r[1], RIGHT, buff=0.15)
        bars.next_to(head, DOWN, buff=0.75)
        bars.shift(RIGHT * (0 - bars.get_center()[0]))
        bcap = label(rf"nonzeros in the Cholesky factor, \ {big['n']:,} unknowns, \ computed with SciPy's SuperLU",
                     font_size=17, color=GREY_A).next_to(bars, UP, buff=0.2)
        growth = VGroup(*[label(rf"{name}: \ $\times${big[key] / prev[key]:.1f}", font_size=19, color=c)
                          for name, key, c in specs[1:]]).arrange(RIGHT, buff=0.5)
        gl = label(rf"when the grid side doubles \ ({prev['m']} $\to$ {big['m']}):", font_size=19, color=GREY_A)
        gg = VGroup(gl, growth).arrange(DOWN, buff=0.15).next_to(bars, DOWN, buff=0.45)
        foot = wrapped_label(r"in 2D a well-ordered direct solver is hard to beat; \ in 3D the separators are planes, "
                             r"\ fill grows like $n^{4/3}$, \ and the iterative methods of Chapters 7 and 9 take "
                             r"over", 12.4, font_size=20, color=WHITE).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Here is what the orderings buy on our grid of four thousand and ninety-six unknowns. <bookmark "
            "mark='a'/> Row by row, the factor has two hundred and sixty-two thousand nonzeros. Reverse "
            "Cuthill–McKee, which only narrows the band, a hundred and eighty-one thousand. <bookmark mark='b'/> "
            "Minimum degree, sixty-three thousand, about three times the matrix itself; our simple nested "
            "dissection, eighty-nine thousand. <bookmark mark='c'/> Nested dissection's advantages are growth and "
            "parallelism: its halves are independent, which is why libraries such as METIS use it on large "
            "meshes. When the grid side doubles, row-by-row fill grows eightfold, the good orderings' less than "
            "sixfold. <bookmark mark='d'/> In three dimensions the separators are planes, fill grows like n to "
            "the four thirds, and iterative methods take over."
        ) as vo:
            self.play(FadeIn(head), FadeIn(bcap), FadeIn(bars[0][0]), GrowFromEdge(bars[0][1], LEFT),
                      FadeIn(bars[0][2]))
            vo.wait_until("a")
            for r in bars[1:3]:
                self.play(FadeIn(r[0]), GrowFromEdge(r[1], LEFT), FadeIn(r[2]))
            vo.wait_until("b")
            for r in bars[3:]:
                self.play(FadeIn(r[0]), GrowFromEdge(r[1], LEFT), FadeIn(r[2]))
            vo.wait_until("c")
            self.play(FadeIn(gg))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, LAM, YES)
