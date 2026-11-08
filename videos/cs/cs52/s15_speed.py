from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs52.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, grid_table, load


def block(w, h, color, opacity=0.25, text=None, size=22):
    """A matrix or vector drawn as a filled rectangle, optionally named."""
    r = Rectangle(width=w, height=h, stroke_color=color, stroke_width=2, fill_color=color, fill_opacity=opacity)
    if text is None:
        return VGroup(r)
    return VGroup(r, MathTex(text, font_size=size, color=color).move_to(r))


def sci(v: float, digits: int = 1) -> str:
    """A number as TeX: 1.1 x 10^{18}."""
    e = math.floor(math.log10(abs(v)))
    return rf"{v / 10 ** e:.{digits}f} \times 10^{{{e}}}"


class Speed(VoiceoverScene):
    def construct(self):
        self.card()
        self.levels()
        self.measured()
        self.blocking()
        self.refinement()
        self.hpl()

    def card(self):
        card = chapter_card(14, r"Speed: \ BLAS, \ LAPACK and mixed precision",
                            r"Why is the fastest code always matrix multiplication?",
                            lit=(1979, 1990, 1992, 1993), extra=((1979, r"BLAS level 1; \ LINPACK"),
                                                                 (1990, r"BLAS level 3"), (1992, r"LAPACK"),
                                                                 (1993, r"the first Top500")), part=PART)
        with self.voiceover("Chapter fourteen. Speed: BLAS, LAPACK, and mixed precision."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def levels(self):
        b = load("blas")["rows"][0]
        head = label(r"Three levels of BLAS", font_size=36).to_edge(UP, buff=0.3)
        times = MathTex(r"\times", font_size=26)
        pics = VGroup(
            VGroup(MathTex(r"\alpha", font_size=26, color=GREY_A), block(0.3, 1.5, DATA, text=r"x"),
                   MathTex(r"+", font_size=26), block(0.3, 1.5, DATA, text=r"y")).arrange(RIGHT, buff=0.15),
            VGroup(block(1.5, 1.5, LAM, text=r"A"), times.copy(), block(0.3, 1.5, DATA, text=r"x")).arrange(
                RIGHT, buff=0.15),
            VGroup(block(1.5, 1.5, YES, text=r"A"), times.copy(), block(1.5, 1.5, YES, text=r"B")).arrange(
                RIGHT, buff=0.15),
        )
        names = VGroup(label(r"level 1 \ (1979): \ \texttt{axpy}", font_size=20, color=KERN),
                       label(r"level 2 \ (1988): \ \texttt{gemv}", font_size=20, color=LAM),
                       label(r"level 3 \ (1990): \ \texttt{gemm}", font_size=20, color=YES))
        xs = (-4.5, 0.0, 4.5)
        for p, nm, x in zip(pics, names, xs):
            p.move_to([x, 1.45, 0])
            nm.next_to(p, UP, buff=0.25)
        maths = []
        for (fl, by, ints, res, c), x in zip(
                ((r"2n", r"24n", r"\frac{2n}{24n}", r"\frac{1}{12}", KERN),
                 (r"2n^2", r"8n^2", r"\frac{2n^2}{8n^2}", r"\frac14", LAM),
                 (r"2n^3", r"24n^2", r"\frac{2n^3}{24n^2}", r"\frac{n}{12}", YES)), xs):
            g = VGroup(
                cmath(r"\text{flops}", r"=", fl, font_size=28),
                cmath(r"\text{bytes}", r"=", by, font_size=28),
                cmath(r"\text{intensity}", r"=", ints, font_size=28),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([x, -1.1, 0])
            fin = cmath(r"\text{intensity}", r"=", res, font_size=28, color=c).move_to(g[2], aligned_edge=LEFT)
            maths.append((g, fin))
        cap = note(r"bytes moved in double precision, \ 8 bytes a number: \ read $x, y$ and write $y$; \ read $A$; \ "
                   r"read $A, B$ and write $C$", font_size=17).to_edge(DOWN, buff=0.6)
        foot = label(rf"$n = {b['n']}$: \ {b['axpy_intensity']:.3f}, \ {b['gemv_intensity']:.2f} and "
                     rf"{b['gemm_intensity']:.1f} flops per byte", font_size=20, color=HEAD).to_edge(DOWN, buff=0.2)
        with self.voiceover(
            "Almost every algorithm in this part spends its time in a few kernels, standardized as the "
            "Basic Linear Algebra Subprograms, the BLAS. <bookmark mark='a'/> Level one, from 1979, works"
            " on vectors: a times x plus y does two operations per element and moves twenty-four bytes, "
            "one twelfth of an operation per byte. <bookmark mark='b'/> Level two, from 1988, multiplies "
            "a matrix by a vector, and uses each matrix entry once: a quarter per byte. <bookmark "
            "mark='c'/> Level three, from 1990, multiplies matrices: two n cubed operations on three n "
            "squared numbers, an intensity of n over twelve, growing with n. <bookmark mark='d'/> That is"
            " Part 9's roofline in one line: only level three does enough arithmetic per byte to keep a "
            "processor busy."
        ) as vo:
            self.play(FadeIn(head))
            for mk, p, nm, (g, fin) in zip("abc", pics, names, maths):
                vo.wait_until(mk)
                self.play(FadeIn(p), FadeIn(nm), FadeIn(g[0]), FadeIn(g[1]))
                self.play(FadeIn(g[2]))
                self.play(TransformMatchingTex(g[2], fin))
            self.play(FadeIn(cap))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def measured(self):
        rows_ = load("blas")["rows"]
        head = label(r"Timed on this machine", font_size=36).to_edge(UP, buff=0.3)
        ax = CornerAxes(x_range=[-1.5, 2.5, 1], y_range=[-1.5, 1.5, 1], x_length=6.4, y_length=4.4, tips=False,
                        axis_config={"stroke_color": GREY_C})
        ax.move_to([-2.5, 0.0, 0])
        xt = VGroup(*[MathTex(t, font_size=20, color=GREY_B).next_to(ax.c2p(p, -1.5), DOWN, buff=0.1)
                      for t, p in ((r"0.1", -1), (r"1", 0), (r"10", 1), (r"100", 2))])
        yt = VGroup(*[MathTex(t, font_size=20, color=GREY_B).next_to(ax.c2p(-1.5, p), LEFT, buff=0.1)
                      for t, p in ((r"0.1", -1), (r"1", 0), (r"10", 1))])
        xl = label(r"arithmetic intensity, \ flops per byte \ (log scale)", font_size=17, color=GREY_A).next_to(
            xt, DOWN, buff=0.08)
        yl = label(r"billions of flops per second, \ measured \ (log scale)", font_size=17, color=GREY_A).next_to(
            ax, UP, buff=0.15).align_to(ax, LEFT)
        specs = (("axpy", KERN), ("gemv", LAM), ("gemm", YES))
        dots = {}
        for key, c in specs:
            g = VGroup()
            for r in rows_:
                p = ax.c2p(math.log10(r[f"{key}_intensity"]), math.log10(r[f"{key}_gflops"]))
                g.add(Dot(p, radius=0.07, color=c))
            dots[key] = g
        gl = VGroup(*[label(f"{r['n']:,}", font_size=16, color=YES).next_to(d, RIGHT, buff=0.1)
                      for r, d in zip(rows_, dots["gemm"])])
        gline = VMobject(color=YES, stroke_width=2).set_points_as_corners([d.get_center() for d in dots["gemm"]])
        kl = VGroup(label(r"\texttt{axpy}", font_size=18, color=KERN).next_to(dots["axpy"], LEFT, buff=0.15),
                    label(r"\texttt{gemv}", font_size=18, color=LAM).next_to(dots["gemv"], RIGHT, buff=0.15),
                    label(r"\texttt{gemm}", font_size=18, color=YES).next_to(dots["gemm"][0], DOWN, buff=0.15))
        big = rows_[-1]
        tab = grid_table([r"$n = %s$" % f"{big['n']:,}".replace(",", "{,}"), r"GFLOP/s"],
                         [[r"\texttt{axpy}", f"{big['axpy_gflops']:.2f}"],
                          [r"\texttt{gemv}", f"{big['gemv_gflops']:.2f}"],
                          [r"\texttt{gemm}", f"{big['gemm_gflops']:.1f}"]],
                         widths=[1.8, 1.6], row_h=0.45, font_size=19, mono_cols=())
        tab.move_to([4.6, 1.5, 0])
        for row, c in zip(tab.cells[1:], (KERN, LAM, YES)):
            row[0].set_color(c)
            row[1].set_color(c)
        notes = VGroup(
            wrapped_label(rf"\texttt{{gemm}} runs {big['gemm_gflops'] / big['axpy_gflops']:.0f} and "
                          rf"{big['gemm_gflops'] / big['gemv_gflops']:.0f} times faster than the other two", 4.0,
                          font_size=19, color=YES),
            wrapped_label(r"small \texttt{axpy} problems fit in cache and run fast; \ from "
                          r"memory they crawl \ (Part 9)", 4.0, font_size=19, color=WHITE),
            wrapped_label(r"NumPy's BLAS on this machine's cores, \ best of 3--5 runs", 4.0, font_size=16,
                          color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(tab, DOWN, buff=0.4)
        notes.align_to(tab, LEFT)
        with self.voiceover(
            "Here are the three levels timed on this machine, through NumPy, which calls an optimized BLAS. "
            "<bookmark mark='a'/> Matrix multiplication climbs as n grows, to about "
            f"{big['gemm_gflops']:.0f} billion operations per second at two thousand and forty-eight. "
            "<bookmark mark='b'/> The other two, at that size, manage "
            f"{big['axpy_gflops']:.1f} and {big['gemv_gflops']:.0f} billion: "
            f"{big['gemm_gflops'] / big['axpy_gflops']:.0f} and {big['gemm_gflops'] / big['gemv_gflops']:.0f} times "
            "slower, doing the same kind of arithmetic. <bookmark mark='c'/> Small vector additions fit in cache "
            "and run faster than large ones, which is Part 9's "
            "memory hierarchy, not arithmetic. <bookmark mark='d'/> So the craft of numerical linear algebra "
            "since 1990 has been to recast every algorithm so that most of its work is level three."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in dots["gemm"]], lag_ratio=0.3), Create(gline),
                      FadeIn(gl), FadeIn(kl[2]))
            vo.wait_until("b")
            self.play(FadeIn(dots["axpy"]), FadeIn(dots["gemv"]), FadeIn(kl[0]), FadeIn(kl[1]))
            self.play(FadeIn(tab), FadeIn(notes[0]))
            vo.wait_until("c")
            self.play(FadeIn(notes[1]), FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(Indicate(dots["gemm"][-1], color=YES, scale_factor=1.8))
        self.wait(0.4)
        self.clear_scene()

    def blocking(self):
        head = label(r"LAPACK: \ blocked elimination", font_size=36).to_edge(UP, buff=0.3)
        N, nb = 4.4, 4
        bw = N / nb
        C = np.array([-3.9, -0.25, 0])
        frame = Square(side_length=N, color=GREY_C, stroke_width=2).move_to(C)
        TL = C + np.array([-N / 2, N / 2, 0])

        def rect(c0, r0, w, h, color, op):
            return Rectangle(width=w, height=h, stroke_width=1.5, stroke_color=color, fill_color=color,
                             fill_opacity=op).move_to(TL + np.array([c0 + w / 2, -(r0 + h / 2), 0]))

        def stage(k):
            o = k * bw
            rest = N - o
            g = VGroup(rect(o, o, bw, rest, KERN, 0.55))                  # the panel
            if rest > bw:
                g.add(rect(o + bw, o, rest - bw, bw, LAM, 0.45))          # U12, a triangular solve
                g.add(rect(o + bw, o + bw, rest - bw, rest - bw, YES, 0.35))  # the trailing update
            if o > 0:
                g.add(rect(0, 0, o, N, GREY_D, 0.5), rect(o, 0, rest, o, GREY_D, 0.5))
            return g
        stages = [stage(k) for k in range(nb)]
        items = [VGroup(Square(0.24, stroke_width=0, fill_color=c, fill_opacity=0.8),
                        label(t, font_size=17, color=GREY_B if c is GREY_D else c)).arrange(RIGHT, buff=0.12)
                 for c, t in ((KERN, r"panel: \ level 2"), (LAM, r"$U_{12}$: \ level 3"),
                              (YES, r"trailing update: \ \texttt{gemm}"), (GREY_D, r"done"))]
        key = VGroup(VGroup(items[0], items[1]).arrange(RIGHT, buff=0.4),
                     VGroup(items[2], items[3]).arrange(RIGHT, buff=0.4))
        key.arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(frame, DOWN, buff=0.25).align_to(frame, LEFT)
        cols = {r"L_{21} U_{12}": YES}
        rows = VGroup(
            cmath(r"A_{22}", r"\leftarrow", r"A_{22} - ", r"L_{21} U_{12}", colors=cols, font_size=30),
            cmath(r"\text{panel flops}", r"\approx", r"\sum_k (n - kb)\, b^2", r"\approx", r"\tfrac12 n^2 b",
                  font_size=30),
            cmath(r"\frac{\tfrac12 n^2 b}{\tfrac23 n^3}", r"=", r"\frac{3b}{4n}", font_size=32),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.7).move_to([3.0, 1.0, 0])
        whys = VGroup(
            label(r"the trailing update: \ one matrix product", font_size=18, color=YES),
            label(r"only the narrow panels run at level 2", font_size=18, color=KERN),
            label(r"the fraction outside level 3", font_size=18, color=GREY_B),
        )
        for w, rr in zip(whys, rows):
            w.next_to(rr, DOWN, buff=0.1).align_to(rr, LEFT)
        frac = 3 * 64 / (4 * 10000)
        ex = wrapped_label(rf"$n = 10{{,}}000$, \ panels of $b = 64$: \ {100 * frac:.1f}\% of the work; \ "
                           r"\texttt{numpy.linalg.solve} calls LAPACK's \texttt{gesv}, \ which does exactly this",
                           5.8, font_size=19, color=HEAD).next_to(whys[2], DOWN, buff=0.4).align_to(rows, LEFT)
        with self.voiceover(
            "LAPACK, released in 1992, does exactly that. <bookmark mark='a'/> Take chapter three's "
            "elimination, but instead of one column at a time, factor a narrow panel of b columns, "
            "<bookmark mark='b'/> then update everything to its lower right at once: the trailing matrix "
            "minus a product of two thin blocks, a matrix multiplication. <bookmark mark='c'/> Move to "
            "the next panel. Only the panels run at level two, about n squared b over two operations out "
            "of two thirds n cubed, <bookmark mark='d'/> a fraction of three b over four n. For ten "
            "thousand unknowns and panels of sixty-four, half of one percent. When NumPy solves a linear "
            "system, it calls exactly this routine."
        ) as vo:
            self.play(FadeIn(head), Create(frame))
            vo.wait_until("a")
            cur = stages[0]
            self.play(FadeIn(cur[0]), FadeIn(key[0][0]))
            vo.wait_until("b")
            self.play(FadeIn(cur[1:]), FadeIn(key[0][1]), FadeIn(key[1]))
            self.play(Write(rows[0]), FadeIn(whys[0]))
            vo.wait_until("c")
            for st in stages[1:]:
                self.play(ReplacementTransform(cur, st), run_time=0.9)
                cur = st
            self.play(FadeIn(rows[1]), FadeIn(whys[1]))
            vo.wait_until("d")
            self.play(FadeIn(rows[2]), FadeIn(whys[2]))
            self.play(FadeIn(ex))
        self.wait(0.4)
        self.clear_scene()

    def refinement(self):
        rows_ = load("refine")["rows"]
        r = next(x for x in rows_ if round(math.log10(x["kappa"])) == 5)
        head = label(r"Mixed precision: \ fast factors, \ exact corrections", font_size=36).to_edge(UP, buff=0.3)
        cols = {r"\text{single}": KERN, r"\text{double}": YES}
        rows = VGroup(
            cmath(r"A = LU", r"\quad", r"\text{single}", font_size=30, colors=cols),
            cmath(r"r_k = b - A x_k", r"\quad", r"\text{double}", font_size=30, colors=cols),
            cmath(r"LU\, d_k = r_k", r",\quad", r"x_{k+1} = x_k + d_k", r"\quad", r"\text{single}", font_size=30,
                  colors=cols),
            cmath(r"\|e_{k+1}\|", r"\lesssim", r"c\, \kappa(A)\, u_{\text{single}}", r"\, \|e_k\|", font_size=30),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.62).move_to([-3.4, 0.4, 0])
        whys = VGroup(
            label(r"the $\tfrac23 n^3$ work, \ in fast low precision", font_size=18, color=GREY_B),
            label(r"the residual, \ carefully: \ $2n^2$ work", font_size=18, color=GREY_B),
            label(r"a correction from the cheap factors", font_size=18, color=GREY_B),
            wrapped_label(r"each round multiplies the error by about $\kappa u$: \ it converges when "
                          r"$\kappa\, u_{\text{single}} < 1$", 5.6, font_size=18, color=HEAD),
        )
        for w, rr in zip(whys, rows):
            w.next_to(rr, DOWN, buff=0.1).align_to(rr, LEFT)
        ax = CornerAxes(x_range=[0, 7, 1], y_range=[0, 16, 4], x_length=4.6, y_length=3.6, tips=False,
                        axis_config={"stroke_color": GREY_C})
        ax.move_to([3.9, 0.3, 0])
        yt = VGroup(*[label(f"{v}", font_size=16, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.1)
                      for v in (0, 4, 8, 12, 16)])
        xt = VGroup(*[label(f"{v}", font_size=16, color=GREY_B).next_to(ax.c2p(v + 0.5, 0), DOWN, buff=0.1)
                      for v in range(7)])
        xl = label(r"refinement rounds", font_size=17, color=GREY_A).next_to(xt, DOWN, buff=0.08)
        yl = label(rf"correct digits, \ $\kappa = 10^5$, \ $n = 400$, \ computed", font_size=17,
                   color=GREY_A).next_to(ax, UP, buff=0.15).align_to(ax, LEFT)
        digits = [-math.log10(e) for e in r["errors"]]
        bars = VGroup(*[Rectangle(width=0.42, height=ax.c2p(0, d)[1] - ax.c2p(0, 0)[1], stroke_width=0,
                                  fill_color=KERN if k == 0 else YES, fill_opacity=0.85).move_to(
            ax.c2p(k + 0.5, 0), aligned_edge=DOWN) for k, d in enumerate(digits)])
        dd = -math.log10(r["double_solve"])
        dl = DashedLine(ax.c2p(0, dd), ax.c2p(7, dd), color=WHITE, stroke_width=2)
        dlab = label(r"a full double-precision solve", font_size=16, color=WHITE).next_to(ax.c2p(7, dd), UP,
                                                                                          buff=0.08)
        dlab.align_to(ax.c2p(7, 0), RIGHT)
        steps = " \\ $\\to$ \\ ".join(f"{d:.1f}" for d in digits[:5])
        dn = label(rf"digits: \ {steps}", font_size=18, color=YES).next_to(xl, DOWN, buff=0.2)
        fw = label(r"Chapter 15 takes this down to 16 bits", font_size=19, color=GREY_A).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Speed also comes from fewer bits: single precision moves half the bytes, and usually runs at"
            " least twice as fast. <bookmark mark='a'/> So factor the matrix once in single precision: "
            "that is the n cubed work. <bookmark mark='b'/> Compute the residual in double, which costs "
            "only n squared, <bookmark mark='c'/> solve for a correction with the cheap factors, and add "
            "it. <bookmark mark='d'/> Each round multiplies the error by about kappa times single "
            "precision's rounding unit, so it converges when that product is below one. <bookmark "
            "mark='e'/> With kappa ten to the five, our instrument gains nearly three digits a round, and"
            " after four rounds is about as accurate as a full double-precision solve. Chapter fifteen "
            "goes down to sixteen bits."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(yt), FadeIn(xt), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(Write(rows[0]), FadeIn(whys[0]), GrowFromEdge(bars[0], DOWN))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(whys[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(whys[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]), FadeIn(whys[3]))
            vo.wait_until("e")
            self.play(Create(dl), FadeIn(dlab))
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars[1:]], lag_ratio=0.3), FadeIn(dn),
                      run_time=2.5)
            self.play(FadeIn(fw))
        self.wait(0.4)
        self.clear_scene()

    def hpl(self):
        rows_ = load("blas")["rows"]
        big = rows_[-1]
        head = label(r"Linpack and the Top500", font_size=36).to_edge(UP, buff=0.3)
        rate = cmath(r"\text{rate}", r"=", r"\frac{\tfrac23 n^3 + 2n^2}{\text{time}}", font_size=34)
        rate.next_to(head, DOWN, buff=0.45)
        rw = wrapped_label(r"High-Performance Linpack: \ a dense random $Ax = b$ by LU with partial pivoting "
                           r"\ (Chapter 3), \ $n$ as large as memory allows; \ almost all of it is \texttt{gemm}",
                           11.0, font_size=19, color=GREY_B).next_to(rate, DOWN, buff=0.2)
        x0, x1, lo, hi = -5.8, 5.8, 8.0, 19.0
        y = -1.35

        def X(p):
            return x0 + (x1 - x0) * (p - lo) / (hi - lo)
        axis = Line([x0, y, 0], [x1, y, 0], color=GREY_C, stroke_width=2)
        ticks = VGroup(*[VGroup(Line([X(p), y - 0.08, 0], [X(p), y + 0.08, 0], color=GREY_C),
                                MathTex(rf"10^{{{p}}}", font_size=20, color=GREY_B).next_to([X(p), y, 0], DOWN,
                                                                                            buff=0.15))
                         for p in range(8, 20, 2)])
        al = label(r"floating-point operations per second \ (log scale)", font_size=17, color=GREY_A).next_to(
            ticks, DOWN, buff=0.12)
        ratio = 1.102e18 / (big["gemm_gflops"] * 1e9)
        pts = [(big["axpy_gflops"] * 1e9, [r"this machine, \ \texttt{axpy}"], KERN, 1.35),
               (big["gemm_gflops"] * 1e9, [r"this machine, \ \texttt{gemm}"], YES, 0.6),
               (1.102e18, [r"Frontier, \ June 2022: \ the first exaflop",
                           rf"$\times\, {sci(ratio)}$ our \texttt{{gemm}}"], HEAD, 0.6)]
        marks = VGroup()
        for v, ts, c, hgt in pts:
            p = math.log10(v)
            d = Dot([X(p), y, 0], radius=0.1, color=c)
            stem = Line([X(p), y, 0], [X(p), y + hgt, 0], color=c, stroke_width=2)
            tx = VGroup(label(ts[0], font_size=18, color=c), MathTex(sci(v), font_size=22, color=c),
                        *[label(t, font_size=18, color=c) for t in ts[1:]]).arrange(DOWN, buff=0.06)
            tx.next_to(stem, UP, buff=0.08)
            if tx.get_right()[0] > 6.9:
                tx.shift(LEFT * (tx.get_right()[0] - 6.9))
            if tx.get_left()[0] < -6.9:
                tx.shift(RIGHT * (-6.9 - tx.get_left()[0]))
            marks.add(VGroup(d, stem, tx))
        foot = wrapped_label(r"the Top500 list, \ twice a year since 1993, \ ranks by this one number; \ HPCG, \ a "
                             r"conjugate-gradient benchmark, \ sparse and memory-bound, \ reaches only a few percent of "
                             r"the same machines' peak: \ Part 9's roofline, \ at the scale of a building", 12.4,
                             font_size=19, color=WHITE).to_edge(DOWN, buff=0.15)
        with self.voiceover(
            "Since 1993 the world's fastest computers have been ranked twice a year, in the Top500 list, "
            "by one program: High-Performance Linpack, descended from the LINPACK library that Jack "
            "Dongarra co-wrote in 1979. <bookmark mark='a'/> It solves a dense random system by "
            "elimination with partial pivoting, and divides two thirds n cubed operations by the time. "
            "Almost all of it is matrix multiplication, so it measures a machine at its best. <bookmark "
            "mark='b'/> On this scale, our machine's level-one speed sits here, and its matrix "
            "multiplication here. <bookmark mark='c'/> In June 2022 Frontier, at Oak Ridge, became the "
            "first to pass ten to the eighteen operations per second: about "
            f"{ratio / 1e6:.0f} million times our matrix multiplication. <bookmark mark='d'/> A conjugate-gradient benchmark, sparse and memory-"
            "bound like most real simulations, reaches only a few percent of the same machines' peak."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(rate), FadeIn(rw))
            vo.wait_until("b")
            self.play(Create(axis), FadeIn(ticks), FadeIn(al))
            self.play(FadeIn(marks[0]))
            self.play(FadeIn(marks[1]))
            vo.wait_until("c")
            self.play(FadeIn(marks[2]))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, DATA, HEAD, KERN, LAM, NO, YES)
