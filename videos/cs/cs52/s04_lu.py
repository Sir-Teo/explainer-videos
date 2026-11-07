from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs52.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, grid_table, load


def sci(v: float, digits: int = 1) -> str:
    """A number as TeX: 1.6 x 10^{16} (0 stays 0)."""
    if v == 0:
        return r"0"
    e = math.floor(math.log10(abs(v)))
    m = v / 10 ** e
    if round(m, digits) >= 10:
        m, e = m / 10, e + 1
    return rf"{m:.{digits}f} \times 10^{{{e}}}"


def mat(rows, size=32, h=0.8, v=0.65, color=WHITE):
    m = Matrix([[str(x) for x in r] for r in rows], element_to_mobject_config={"font_size": size, "color": color},
               h_buff=h, v_buff=v)
    return m


class Lu(VoiceoverScene):
    def construct(self):
        self.card()
        self.elimination()
        self.cost()
        self.pivot()
        self.growth()
        self.cholesky()

    def card(self):
        card = chapter_card(3, r"Gaussian elimination", r"How do we solve $Ax = b$, \ and why swap rows?",
                            lit=(1948, 1961, 1990), extra=((1948, r"Turing: \ elimination is $LU$"),
                                                           (1961, r"Wilkinson: \ the growth bound"),
                                                           (1990, r"Trefethen and Schreiber: \ average growth")),
                            part=PART)
        with self.voiceover("Chapter three. Gaussian elimination."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def elimination(self):
        head = label(r"Elimination is a factorization", font_size=36).to_edge(UP, buff=0.3)
        A0 = [[2, 1, 1], [4, 3, 3], [8, 7, 9]]
        A1 = [[2, 1, 1], [0, 1, 1], [0, 3, 5]]
        A2 = [[2, 1, 1], [0, 1, 1], [0, 0, 2]]
        Lr = [[1, 0, 0], [2, 1, 0], [4, 3, 1]]
        pos = np.array([-4.3, 1.15, 0])
        m0, m1, m2 = (mat(a).move_to(pos) for a in (A0, A1, A2))
        for i in (1, 2):
            m1.get_rows()[i].set_color(DATA)
        m2.get_rows()[2].set_color(DATA)
        an = MathTex(r"A", font_size=34).next_to(m0, LEFT, buff=0.2)
        piv = SurroundingRectangle(m0.get_entries()[0], color=HEAD, buff=0.08)
        piv2 = SurroundingRectangle(m1.get_entries()[4], color=HEAD, buff=0.08)
        ops = VGroup(MathTex(r"r_2 \leftarrow r_2 - 2\,r_1", font_size=30),
                     MathTex(r"r_3 \leftarrow r_3 - 4\,r_1", font_size=30),
                     MathTex(r"r_3 \leftarrow r_3 - 3\,r_2", font_size=30)).arrange(DOWN, aligned_edge=LEFT,
                                                                                  buff=0.3)
        ops.set_color(HEAD).next_to(m0, RIGHT, buff=0.7)
        Lm = mat(Lr).move_to([4.6, 1.15, 0])
        ln = MathTex(r"L", font_size=34).next_to(Lm, LEFT, buff=0.2)
        ents = Lm.get_entries()
        mult = [ents[3], ents[6], ents[7]]
        for e in mult:
            e.set_color(HEAD)
        base = VGroup(Lm.get_brackets(), *[e for i, e in enumerate(ents) if i not in (3, 6, 7)])
        un = label(r"$U$: \ upper triangular", font_size=19, color=DATA).next_to(m0, DOWN, buff=0.2)
        lnote = label(r"$L$: \ the multipliers", font_size=19, color=HEAD).next_to(Lm, DOWN, buff=0.2)
        eq = VGroup(MathTex(r"A", r"=", font_size=36), mat(Lr, size=28, h=0.7, v=0.55),
                    mat(A2, size=28, h=0.7, v=0.55)).arrange(RIGHT, buff=0.2).move_to([0, -2.2, 0])
        for e in (eq[1].get_entries()[i] for i in (3, 6, 7)):
            e.set_color(HEAD)
        eq[2].set_color(DATA)
        ill = note(r"illustrative", font_size=16).to_corner(DR, buff=0.35)
        with self.voiceover(
            "Elimination is the oldest algorithm in this part: the Chinese Nine Chapters on the Mathematical Art "
            "already use it. <bookmark mark='a'/> To clear the first column below the pivot, subtract two times "
            "row one from row two, and four times row one from row three. <bookmark mark='b'/> Then three times "
            "the new row two from row three. What remains is upper triangular: call it U. "
            "<bookmark mark='c'/> Keep the multipliers, two, four and three, in a lower triangular matrix with "
            "ones on its diagonal: call it L. <bookmark mark='d'/> Then A equals L times U, as Turing pointed out "
            "in 1948. Solving A x equals b is then two triangular solves: L from the top down, then U from the "
            "bottom up."
        ) as vo:
            self.play(FadeIn(head), FadeIn(m0), FadeIn(an), FadeIn(ill))
            vo.wait_until("a")
            self.play(Create(piv), FadeIn(ops[0]), FadeIn(ops[1]))
            self.play(ReplacementTransform(m0, m1), FadeOut(piv))
            vo.wait_until("b")
            self.play(Create(piv2), FadeIn(ops[2]))
            self.play(ReplacementTransform(m1, m2), FadeOut(piv2), FadeIn(un))
            vo.wait_until("c")
            self.play(FadeIn(base), FadeIn(ln), FadeIn(lnote))
            self.play(LaggedStart(*[FadeIn(e, scale=1.4) for e in mult], lag_ratio=0.4))
            vo.wait_until("d")
            self.play(FadeIn(eq, shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def cost(self):
        head = label(r"What elimination costs", font_size=36).to_edge(UP, buff=0.3)
        n, cell = 6, 0.48
        org = np.array([-6.2, 2.2, 0])
        grid = VGroup(*[Square(side_length=cell, stroke_width=1, stroke_color=GREY_D).move_to(
            org + np.array([(j + 0.5) * cell, -(i + 0.5) * cell, 0])) for i in range(n) for j in range(n)])

        def block(k):
            s = (n - k) * cell
            r = Rectangle(width=s, height=s, stroke_color=HEAD, stroke_width=2, fill_color=HEAD, fill_opacity=0.3)
            return r.move_to(org + np.array([k * cell + s / 2, -k * cell - s / 2, 0]))
        blocks = [block(k) for k in range(1, n)]
        cap = label(r"step $k$ updates the $(n - k)^2$ entries \ of the shaded block:", font_size=18,
                    color=GREY_A).next_to(grid, DOWN, buff=0.3).align_to(grid, LEFT)
        cap2 = label(r"one multiply and one subtract each", font_size=18, color=GREY_A).next_to(cap, DOWN,
                                                                                            buff=0.1).align_to(
            cap, LEFT)
        cols = {r"\approx \tfrac{2}{3}\,n^3": HEAD}
        rows = VGroup(
            cmath(r"\text{flops}", r"=", r"\sum_{k=1}^{n-1} 2\,(n-k)^2", font_size=34),
            cmath(r"\text{flops}", r"=", r"2 \sum_{j=1}^{n-1} j^2", font_size=34),
            cmath(r"\text{flops}", r"=", r"2 \cdot \frac{(n-1)\,n\,(2n-1)}{6}", font_size=34),
            cmath(r"\text{flops}", r"\approx \tfrac{2}{3}\,n^3", colors=cols, font_size=38),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([2.6, 0.75, 0])
        whys = VGroup(label(r"add up the steps", font_size=18, color=GREY_B),
                      label(r"count from the end: \ $j = n - k$", font_size=18, color=GREY_B),
                      label(r"the sum of squares", font_size=18, color=GREY_B),
                      label(r"the leading term", font_size=18, color=GREY_B))
        for w, r in zip(whys, rows):
            w.next_to(r, RIGHT, buff=0.3)
        x0 = max(w.get_left()[0] for w in whys)
        for w in whys:
            w.align_to([x0, 0, 0], LEFT)
        grp = VGroup(rows, whys)
        if grp.get_right()[0] > 6.8:
            grp.shift(LEFT * (grp.get_right()[0] - 6.8))
        foot = VGroup(
            wrapped_label(r"each triangular solve costs about $n^2$: \ factor once, \ then solve for as many "
                          r"right-hand sides as you like", 12.4, font_size=20, color=WHITE),
            wrapped_label(r"forming $A^{-1}$ instead costs about $2n^3$, \ three times as much: \ to solve, \ "
                          r"never invert", 12.4, font_size=20, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "How much work is it? <bookmark mark='a'/> Step k updates the block below and to the right of the "
            "pivot: n minus k squared entries, each one multiply and one subtract. "
            "<bookmark mark='b'/> Add up the steps, and count from the end. "
            "<bookmark mark='c'/> The sum of the first squares is a cubic, <bookmark mark='d'/> and its leading "
            "term gives two thirds of n cubed operations. <bookmark mark='e'/> The triangular solves cost only "
            "about n squared each, so the factorization is done once and reused for every right-hand side. "
            "Computing the inverse instead would cost three times as much, hence the rule: to solve, never "
            "invert."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid))
            vo.wait_until("a")
            cur = blocks[0].copy()
            self.play(FadeIn(cur), FadeIn(cap), FadeIn(cap2))
            for b in blocks[1:]:
                self.play(Transform(cur, b), run_time=0.6)
            self.play(Write(rows[0]), FadeIn(whys[0]))
            vo.wait_until("b")
            self.play(TransformMatchingTex(rows[0].copy(), rows[1]), FadeIn(whys[1]))
            vo.wait_until("c")
            self.play(TransformMatchingTex(rows[1].copy(), rows[2]), FadeIn(whys[2]))
            vo.wait_until("d")
            self.play(TransformMatchingTex(rows[2].copy(), rows[3]), FadeIn(whys[3]))
            vo.wait_until("e")
            self.play(FadeIn(foot[0]))
            self.play(FadeIn(foot[1]))
        self.wait(0.4)
        self.clear_scene()

    def pivot(self):
        rows = load("pivot")["rows"]
        head = label(r"A tiny pivot, \ and the cure", font_size=36).to_edge(UP, buff=0.3)
        cols = {r"\tfrac{1}{\varepsilon}": NO, r"1 - \tfrac{1}{\varepsilon}": NO, r"-10^{20}": NO}
        eqs = VGroup(
            cmath(r"\begin{bmatrix} \varepsilon & 1 \\ 1 & 1 \end{bmatrix}", r"=",
                  r"\begin{bmatrix} 1 & 0 \\ \tfrac{1}{\varepsilon} & 1 \end{bmatrix}",
                  r"\begin{bmatrix} \varepsilon & 1 \\ 0 & 1 - \tfrac{1}{\varepsilon} \end{bmatrix}", font_size=30),
            cmath(r"\varepsilon = 10^{-20}:", r"\quad", r"\mathrm{fl}\big(1 - 10^{20}\big)", r"=", r"-10^{20}",
                  colors=cols, font_size=30),
            cmath(r"\tilde L\,\tilde U", r"=", r"\begin{bmatrix} \varepsilon & 1 \\ 1 & 0 \end{bmatrix}",
                  font_size=30),
            cmath(r"PA", r"=", r"\begin{bmatrix} 1 & 0 \\ \varepsilon & 1 \end{bmatrix}",
                  r"\begin{bmatrix} 1 & 1 \\ 0 & 1 - \varepsilon \end{bmatrix}", font_size=30),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).next_to(head, DOWN, buff=0.45).to_edge(LEFT, buff=0.45)
        eqs[0][2].set_color(NO)
        eqs[3][2].set_color(YES)
        lost = label(r"the 1 became 0: \ exact factors of the wrong matrix", font_size=18, color=NO).next_to(
            eqs[2], RIGHT, buff=0.3)
        zero = SurroundingRectangle(eqs[2][2], color=NO, buff=0.06)
        swap = label(r"swap the rows first: \ multipliers $|\ell| \le 1$", font_size=18, color=YES).next_to(
            eqs[3], DOWN, buff=0.15).align_to(eqs[3], LEFT)
        trs = [[rf"${sci(r['eps'], 0)}$", rf"${sci(r['err_no_pivot'])}$", rf"${sci(r['err_pivot'])}$"]
               for r in rows]
        clr = [[GREY_A, NO, YES] for _ in rows]
        tab = grid_table([r"$\varepsilon$", r"no pivoting", r"partial pivoting"], trs, widths=[1.5, 2.1, 2.3],
                         row_h=0.5, font_size=19, colors=clr, mono_cols=())
        tab.to_edge(RIGHT, buff=0.35).set_y(-0.4)
        tcap = note(r"largest error in $x$, \ computed; \ $b = (1, 2)$", font_size=17).next_to(tab, UP, buff=0.25)
        with self.voiceover(
            "Here is the hook's failure. <bookmark mark='a'/> Eliminating with the tiny pivot "
            "epsilon needs the multiplier one over epsilon, and leaves one minus one over epsilon in the corner. "
            "<bookmark mark='b'/> With epsilon ten to the minus twenty, that rounds to minus ten to the twenty. "
            "The one is gone. <bookmark mark='c'/> The computed factors are the exact factors of a "
            "different matrix, with a zero where the one was. "
            "<bookmark mark='d'/> The cure is partial pivoting: before each step, swap up the row with the "
            "largest entry in the column, so every multiplier is at most one. <bookmark mark='e'/> In our "
            "instrument's runs, without pivoting the error grows as epsilon shrinks, until no digit is right; "
            "with pivoting it stays at the level of rounding."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(eqs[0]))
            vo.wait_until("b")
            self.play(FadeIn(eqs[1]))
            vo.wait_until("c")
            self.play(FadeIn(eqs[2]), Create(zero), FadeIn(lost))
            vo.wait_until("d")
            self.play(FadeIn(eqs[3]), FadeIn(swap))
            vo.wait_until("e")
            self.play(FadeIn(tcap), FadeIn(tab.rule), FadeIn(VGroup(*tab.cells[0])),
                      LaggedStart(*[FadeIn(VGroup(*c)) for c in tab.cells[1:]], lag_ratio=0.25))
        self.wait(0.4)
        self.clear_scene()

    def growth(self):
        g = load("growth")["rows"]
        head = label(r"How much can the entries grow?", font_size=36).to_edge(UP, buff=0.3)
        cols = {r"\rho": HEAD, r"2^{\,n-1}": NO}
        rows = VGroup(
            cmath(r"u_{ij}'", r"=", r"u_{ij} - \ell_{ik}\,u_{kj}", r",\qquad |\ell_{ik}| \le 1", font_size=34),
            cmath(r"\max|u'|", r"\le", r"2\,\max|u|", font_size=34),
            cmath(r"\rho", r"=", r"\frac{\max|u_{ij}|}{\max|a_{ij}|}", r"\le", r"2^{\,n-1}", colors=cols,
                  font_size=34),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to([-3.4, 0.7, 0])
        whys = VGroup(label(r"one step of elimination, \ pivoted", font_size=18, color=GREY_B),
                      label(r"so the largest entry at most doubles", font_size=18, color=GREY_B),
                      label(r"over $n - 1$ steps: \ the growth factor \ (Wilkinson, \ 1961)", font_size=18,
                            color=GREY_B))
        for w, r in zip(whys, rows):
            w.next_to(r, DOWN, buff=0.1).align_to(r, LEFT)
        W = [[1, 0, 0, 0, 1], [-1, 1, 0, 0, 1], [-1, -1, 1, 0, 1], [-1, -1, -1, 1, 1], [-1, -1, -1, -1, 1]]
        U = [[1, 0, 0, 0, 1], [0, 1, 0, 0, 2], [0, 0, 1, 0, 4], [0, 0, 0, 1, 8], [0, 0, 0, 0, 16]]
        wm = mat(W, size=24, h=0.62, v=0.48).move_to([3.0, 1.2, 0])
        um = mat(U, size=24, h=0.62, v=0.48).move_to([3.0, 1.2, 0])
        for i in range(5):
            um.get_entries()[i * 5 + 4].set_color(NO)
        wl = label(r"Wilkinson's matrix, \ $n = 5$", font_size=18, color=GREY_A).next_to(wm, DOWN, buff=0.2)
        ul = label(r"after elimination: \ the last column doubles", font_size=18, color=NO).next_to(um, DOWN,
                                                                                                  buff=0.2)
        foot = wrapped_label(r"elimination's backward error is bounded by a modest multiple of $\rho$ times the "
                             r"unit roundoff: \ stable whenever $\rho$ is small", 12.4, font_size=20,
                             color=WHITE).to_edge(DOWN, buff=0.35)
        # the measured growth, on a log scale
        ax = CornerAxes(x_range=[2, 6, 1], y_range=[0, 20, 4], x_length=6.2, y_length=4.0, tips=False,
                        axis_config={"stroke_color": GREY_C})
        ax.move_to([-2.0, -0.2, 0])
        xt = VGroup(*[label(rf"{2 ** p}", font_size=17, color=GREY_B).next_to(ax.c2p(p, 0), DOWN, buff=0.12)
                      for p in range(2, 7)])
        yt = VGroup(*[MathTex(rf"10^{{{p}}}", font_size=22, color=GREY_B).next_to(ax.c2p(2, p), LEFT, buff=0.1)
                      for p in (0, 4, 8, 12, 16, 20)])
        xl = label(r"size $n$", font_size=18, color=GREY_A).next_to(xt, DOWN, buff=0.12)
        yl = label(r"growth factor $\rho$, \ computed", font_size=18, color=GREY_A).next_to(ax, UP,
                                                                                         buff=0.12).align_to(ax, LEFT)

        def series(key, color):
            pts = [ax.c2p(math.log2(r["n"]), math.log10(r[key])) for r in g]
            return VGroup(VMobject(color=color, stroke_width=3).set_points_as_corners(pts),
                          *[Dot(p, radius=0.06, color=color) for p in pts])
        sw, sm, sx = series("wilkinson", NO), series("random_mean", YES), series("random_max", DATA)
        last = g[-1]
        keys = VGroup(
            label(rf"Wilkinson's matrix: \ $2^{{n-1}}$, \ ${sci(last['wilkinson'])}$ at $n = {last['n']}$",
                  font_size=19, color=NO),
            label(rf"random matrices, \ mean: \ {last['random_mean']:.1f} at $n = {last['n']}$", font_size=19,
                  color=YES),
            label(rf"random matrices, \ largest of 50: \ {last['random_max']:.1f}", font_size=19, color=DATA),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(ax, RIGHT, buff=0.5).shift(UP * 0.4)
        ts = wrapped_label(r"Trefethen and Schreiber \ (1990): \ on random matrices growth is small; \ why it is "
                           r"small in practice is unproved \ (Chapter 15)", 5.0, font_size=18,
                           color=GREY_A).next_to(keys, DOWN, buff=0.4).align_to(keys, LEFT)
        with self.voiceover(
            "With pivoting, how large can the entries of U become? "
            "<bookmark mark='a'/> Each step replaces an entry by itself minus a multiplier, at most one, times "
            "another entry, <bookmark mark='b'/> so the largest entry at most doubles. <bookmark mark='c'/> Over n "
            "minus one steps, the growth factor rho is at most two to the n minus one, as Wilkinson proved, "
            "and elimination's backward error grows with rho. "
            "<bookmark mark='d'/> The bound is attained: here the last column doubles at every step. "
            "<bookmark mark='e'/> Measured, it is exactly two to the n minus one on Wilkinson's "
            "matrix, nine times ten to the eighteen at size sixty-four, <bookmark mark='f'/> but about four for "
            "random matrices of that size. Lloyd Trefethen and Robert Schreiber studied this in "
            "1990: in practice growth is small, and nobody has proved why."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(rows[0]), FadeIn(whys[0]), FadeIn(wm), FadeIn(wl))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(whys[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(whys[2]), FadeIn(foot))
            vo.wait_until("d")
            self.play(ReplacementTransform(wm, um), ReplacementTransform(wl, ul))
            vo.wait_until("e")
            self.play(FadeOut(rows), FadeOut(whys), FadeOut(um), FadeOut(ul), FadeOut(foot))
            self.play(Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl), FadeIn(yl))
            self.play(Create(sw), FadeIn(keys[0]), run_time=1.5)
            vo.wait_until("f")
            self.play(Create(sm), FadeIn(keys[1]), Create(sx), FadeIn(keys[2]), run_time=1.5)
            self.play(FadeIn(ts))
        self.wait(0.4)
        self.clear_scene()

    def cholesky(self):
        head = label(r"Symmetric and positive definite: \ Cholesky", font_size=36).to_edge(UP, buff=0.3)
        rows = VGroup(
            MathTex(r"\begin{bmatrix} a & b \\ b & c \end{bmatrix}", r"=",
                    r"\begin{bmatrix} \ell_{11} & 0 \\ \ell_{21} & \ell_{22} \end{bmatrix}",
                    r"\begin{bmatrix} \ell_{11} & \ell_{21} \\ 0 & \ell_{22} \end{bmatrix}", font_size=32),
            MathTex(r"\ell_{11}^2 = a", r",\quad", r"\ell_{11}\,\ell_{21} = b", r",\quad",
                    r"\ell_{21}^2 + \ell_{22}^2 = c", font_size=32),
            MathTex(r"\ell_{11} = \sqrt{a}", r",\quad", r"\ell_{21} = b/\sqrt{a}", r",\quad",
                    r"\ell_{22} = \sqrt{c - b^2/a}", font_size=32),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(head, DOWN, buff=0.45).to_edge(LEFT, buff=0.6)
        rows[0][2].set_color(DATA)
        rows[2].set_color(YES)
        whys = VGroup(label(r"$A = LL^{\mathsf T}$", font_size=20, color=GREY_B),
                      label(r"match the entries", font_size=20, color=GREY_B),
                      label(r"solve in order", font_size=20, color=GREY_B))
        for w, r in zip(whys, rows):
            w.next_to(r, RIGHT, buff=0.5)
        x0 = max(w.get_left()[0] for w in whys)
        for w in whys:
            w.align_to([x0, 0, 0], LEFT)
        pos = label(r"positive definite \ $\iff$ \ every square root is of a positive number", font_size=19,
                    color=YES).next_to(rows[2], DOWN, buff=0.25).align_to(rows[2], LEFT)
        # the flop counts, as bars of n^3
        specs = [(r"Cholesky", 1 / 3, YES, r"$n^3/3$"), (r"LU", 2 / 3, DATA, r"$2n^3/3$"),
                 (r"Householder QR \ (next chapter)", 4 / 3, LAM, r"$4n^3/3$")]
        bars = VGroup()
        for name, v, c, t in specs:
            b = Rectangle(width=v * 4.2, height=0.36, stroke_width=0, fill_color=c, fill_opacity=0.85)
            nm = label(name, font_size=19, color=c)
            vt = label(t, font_size=19, color=c)
            bars.add(VGroup(nm, b, vt))
        for row in bars:
            row[0].move_to([-3.3, 0, 0], aligned_edge=RIGHT)
            row[1].next_to(row[0], RIGHT, buff=0.3)
            row[2].next_to(row[1], RIGHT, buff=0.2)
        bars.arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        for row in bars:
            row[0].align_to([-3.4, 0, 0], RIGHT)
            row[1].next_to([-3.1, row[0].get_y(), 0], RIGHT, buff=0)
            row[2].next_to(row[1], RIGHT, buff=0.2)
        bars.next_to(pos, DOWN, buff=0.5).set_x(0)
        bcap = note(r"flops for an $n \times n$ matrix, \ leading terms", font_size=17).next_to(bars, DOWN, buff=0.15)
        with self.voiceover(
            "When A is symmetric and positive definite, as covariance matrices are, "
            "elimination can be halved. <bookmark mark='a'/> Write A as L times L transposed. "
            "<bookmark mark='b'/> Match the entries: l one one squared is a, l one one times l two one is b, and "
            "the corner gives c. <bookmark mark='c'/> Solve in order: square roots and a division. Positive "
            "definiteness is exactly the condition that every square root is of a positive number. Each entry of "
            "L is bounded by the square root of a diagonal entry of A, so nothing can grow, and no pivoting is "
            "needed. <bookmark mark='d'/> André-Louis Cholesky's method costs a third of n cubed operations, half "
            "of LU."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(rows[0]), FadeIn(whys[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1], shift=DOWN * 0.1), FadeIn(whys[1]))
            vo.wait_until("c")
            self.play(TransformMatchingTex(rows[1].copy(), rows[2]), FadeIn(whys[2]))
            self.play(FadeIn(pos))
            vo.wait_until("d")
            self.play(LaggedStart(*[AnimationGroup(FadeIn(r[0]), GrowFromEdge(r[1], LEFT), FadeIn(r[2]))
                                    for r in bars], lag_ratio=0.3), FadeIn(bcap))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, KERN, LAM)
