from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis6.common import load, plain_axes, polyline, right_angle, square_axes


LEG_TEX = [r"e_0 = \tfrac{1}{\sqrt2}", r"e_1 = \sqrt{\tfrac32}\, x", r"e_2 = \sqrt{\tfrac58}\,(3x^2 - 1)",
           r"e_3 = \sqrt{\tfrac78}\,(5x^3 - 3x)", r"e_4 = \tfrac{3}{8\sqrt2}\,(35x^4 - 30x^2 + 3)"]


class Orthonormal(VoiceoverScene):
    def construct(self):
        self.card()
        self.gram_schmidt()
        self.bessel()
        self.parseval()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(8, r"Orthonormal bases, Bessel and Parseval",
                            r"When do perpendicular vectors span everything?", lit=(), part=6)
        with self.voiceover("Chapter eight: orthonormal bases, and Pythagoras with infinitely many sides."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def gram_schmidt(self):
        d = load("legendre")
        xs, curves, maxdiff = d["xs"], d["curves"], float(d["maxdiff"])
        # the schematic: subtract the shadow
        sx = square_axes([-0.3, 2.2, 1], [-0.3, 1.8, 1], 1.0).move_to([-5.0, 1.0, 0])
        sx.set_opacity(0)
        e0 = np.array([1.0, 0.0])
        v = np.array([1.6, 1.2])
        shadow = (v @ e0) * e0
        arrs = VGroup(Arrow(sx.c2p(0, 0), sx.c2p(*e0), buff=0, color=C.SEQ, stroke_width=5, tip_length=0.16),
                      Arrow(sx.c2p(0, 0), sx.c2p(*v), buff=0, color=GREY_B, stroke_width=4, tip_length=0.16))
        shad = Line(sx.c2p(0, 0), sx.c2p(*shadow), color=C.EPS, stroke_width=6).set_stroke(opacity=0.7)
        perp = Arrow(sx.c2p(*shadow), sx.c2p(*v), buff=0, color=C.APPROX, stroke_width=5, tip_length=0.16)
        ra = right_angle(sx, shadow, np.array([-1.0, 0]), np.array([0, 1.0]), size=0.14)
        s_l = VGroup(MathTex(r"v - \langle v, e_0\rangle e_0", font_size=24, color=C.APPROX).next_to(perp, RIGHT, buff=0.1),
                     MathTex(r"e_0", font_size=24, color=C.SEQ).next_to(arrs[0], DOWN, buff=0.08),
                     MathTex(r"v", font_size=24, color=GREY_B).next_to(sx.c2p(*v), UP, buff=0.08))
        sch = note(r"schematic").next_to(sx, DOWN, buff=0.0).shift(DOWN * 0.1)
        ax = plain_axes([-1, 1, 0.5], [-2.2, 2.2, 1], 5.4, 3.6, numbers=True, font_size=18,
                        x_axis_config={"decimal_number_config": {"num_decimal_places": 1}},
                        y_axis_config={"decimal_number_config": {"num_decimal_places": 0}}).move_to([0.6, -1.15, 0])
        cols = [C.SEQ, C.APPROX, C.CONNECTED_SET, C.MEASURE, C.INNER]
        monos = [polyline(ax, xs, xs**k, color=GREY_C, stroke_width=2) for k in range(5)]
        legs = [polyline(ax, xs, curves[k], color=cols[k], stroke_width=3.5) for k in range(5)]
        texs = VGroup(*[MathTex(t, font_size=26, color=c) for t, c in zip(LEG_TEX, cols)]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.17).move_to([5.0, -0.6, 0])
        step2 = MathTex(r"x^2 - \langle x^2, e_0\rangle e_0 - \langle x^2, e_1\rangle e_1 = x^2 - \tfrac13", font_size=26,
                        color=C.CONNECTED_SET).next_to(ax, UP, buff=0.12)
        # the step shown on screen, exactly
        from numpy.polynomial import legendre as L
        xg, wg = L.leggauss(40)
        e0v, e1v = np.full_like(xg, 1 / math.sqrt(2)), math.sqrt(1.5) * xg
        r2 = xg**2 - np.sum(wg * xg**2 * e0v) * e0v - np.sum(wg * xg**2 * e1v) * e1v
        assert np.allclose(r2, xg**2 - 1 / 3, atol=1e-13)
        gram = MathTex(rf"\langle e_i, e_j\rangle = \delta_{{ij}}; \quad \max_n |e_n - \text{{Legendre}}_n| = {sci(maxdiff, 0)}",
                       font_size=24, color=GREY_A).to_edge(DOWN, buff=0.15)
        assert maxdiff < 1e-12
        head = VGroup(label(r"Gram--Schmidt: \ from any independent sequence, subtract its shadow on what came before",
                            font_size=28),
                      label(r"$1, x, x^2, \ldots$ \ in $L^2[-1, 1]$ \ $\longrightarrow$ \ the Legendre polynomials (Legendre, 1782)",
                            font_size=24, color=GREY_A)).arrange(DOWN, buff=0.08).to_edge(UP, buff=0.2)
        with self.voiceover(
            "<bookmark mark='a'/> To make perpendicular vectors out of any independent ones, Gram-Schmidt "
            "subtracts shadows. Take the next vector, remove its projection onto what you already have, and what's "
            "left is perpendicular. Scale it to length one. <bookmark mark='b'/> Do it to the powers one, x, x "
            "squared and so on, in L two of minus one to one. <bookmark mark='c'/> The constant becomes one over root "
            "two. x is already perpendicular to it. x squared loses its shadow on the constant, a third, and becomes a "
            "multiple of three x squared minus one. <bookmark mark='d'/> Continue, and out come the Legendre "
            "polynomials, each one perpendicular to all the others. The computed functions agree with Legendre's "
            "formulas to twelve digits."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head[0]), FadeIn(arrs), FadeIn(s_l[1:]), FadeIn(sch))
            self.play(Create(shad), GrowArrow(perp), Create(ra), FadeIn(s_l[0]))
            vo.wait_until("b")
            self.play(FadeIn(head[1]), Create(ax), LaggedStart(*[Create(m) for m in monos], lag_ratio=0.2), run_time=2)
            vo.wait_until("c")
            for k in range(3):
                self.play(ReplacementTransform(monos[k], legs[k]), FadeIn(texs[k]), run_time=1.0)
                if k == 2:
                    self.play(FadeIn(step2))
            vo.wait_until("d")
            for k in range(3, 5):
                self.play(ReplacementTransform(monos[k], legs[k]), FadeIn(texs[k]), run_time=1.0)
            self.play(FadeIn(gram))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def bessel(self):
        d = load("bessel")
        c, partial, xs, curves, Ms = d["c"], d["partial"], d["xs"], d["curves"], d["Ms"]
        ax = plain_axes([-1, 1, 0.5], [-1.5, 1.5, 0.5], 5.6, 3.2, numbers=True, font_size=18,
                        x_axis_config={"decimal_number_config": {"num_decimal_places": 1}},
                        y_axis_config={"decimal_number_config": {"num_decimal_places": 1}}).move_to([-3.5, 0.0, 0])
        sg = VGroup(Line(ax.c2p(-1, -1), ax.c2p(0, -1), color=WHITE, stroke_width=4),
                    Line(ax.c2p(0, 1), ax.c2p(1, 1), color=WHITE, stroke_width=4))
        s_l = MathTex(r"f = \operatorname{sign} x, \quad \|f\|^2 = 2", font_size=28).next_to(ax, UP, buff=0.1)
        pc = [polyline(ax, xs, cv, color=C.EPS, stroke_width=3) for cv in curves]
        pl = [MathTex(rf"s_N = \sum_{{n < {M}}} \langle f, e_n\rangle e_n", font_size=24, color=C.EPS).next_to(
            ax.c2p(-1, 1.3), RIGHT, buff=0.05) for M in Ms]  # the empty upper-left corner (sign x = -1 there)
        # the bar: the squares of the coefficients stacked, against ||f||^2 = 2
        W, x0, y0 = 11.0, -5.5, -2.55
        frame = Rectangle(width=W, height=0.5, stroke_color=WHITE, stroke_width=2).move_to([x0 + W / 2, y0, 0])
        f_l = MathTex(r"\|f\|^2 = 2", font_size=26).next_to(frame, RIGHT, buff=0.1).shift(LEFT * 0.05)
        segs = VGroup()
        acc = 0.0
        odd = [n for n in range(len(c)) if abs(c[n]) > 1e-12]
        palette = [C.SEQ, C.APPROX, C.CONNECTED_SET, C.MEASURE, C.INNER, C.DIST]
        for j, n in enumerate(odd):
            w = float(c[n] ** 2) / 2 * W
            segs.add(Rectangle(width=w, height=0.5, stroke_width=0.6, stroke_color=BACKGROUND,
                               fill_color=palette[j % len(palette)], fill_opacity=0.9).move_to([x0 + acc + w / 2, y0, 0]))
            acc += w
        counts = [int(np.sum(np.array(odd) < M)) for M in Ms]
        sums = [MathTex(rf"\sum_{{n < {M}}} |\langle f, e_n\rangle|^2 = {partial[M - 1]:.5f}", font_size=26,
                        color=C.EPS).next_to(frame, UP, buff=0.12).align_to(frame, LEFT) for M in Ms]
        lefts = [MathTex(rf"\|f - s_N\|^2 = {2 - partial[M - 1]:.5f}", font_size=26, color=C.PATHOLOGY).next_to(
            frame, UP, buff=0.12).align_to(frame, RIGHT).shift(LEFT * 0.9) for M in Ms]
        assert abs(partial[1] - 1.5) < 1e-12 and np.all(partial <= 2)
        tri = square_axes([0, 3.2, 1], [0, 2.4, 1], 1.0).move_to([3.4, 0.9, 0])
        tri.set_opacity(0)
        Tf = np.array([2.6, 2.0])
        Ts = np.array([2.6, 0.0])
        T = VGroup(Arrow(tri.c2p(0, 0), tri.c2p(*Tf), buff=0, color=WHITE, stroke_width=4, tip_length=0.18),
                   Line(tri.c2p(0, 0), tri.c2p(*Ts), color=C.EPS, stroke_width=5),
                   Line(tri.c2p(*Ts), tri.c2p(*Tf), color=C.PATHOLOGY, stroke_width=5),
                   right_angle(tri, Ts, np.array([-1.0, 0]), np.array([0, 1.0]), size=0.16))
        T_l = VGroup(MathTex(r"f", font_size=28).next_to(tri.c2p(1.3, 1.0), UL, buff=0.05),
                     MathTex(r"s_N", font_size=28, color=C.EPS).next_to(tri.c2p(1.3, 0), DOWN, buff=0.1),
                     MathTex(r"f - s_N", font_size=28, color=C.PATHOLOGY).next_to(tri.c2p(*Ts), RIGHT, buff=0.1).shift(UP * 0.9))
        thm = VGroup(label(r"\textbf{RCA 4.17} \ Bessel: \ $\sum |\langle f, e_n\rangle|^2 \le \|f\|^2$", font_size=26),
                     label(r"Pythagoras with a leftover \ (schematic)", font_size=22, color=GREY_B)).arrange(
            DOWN, buff=0.08).next_to(tri, DOWN, buff=0.2)
        head = label(r"Bessel's inequality: \ the squares of the coefficients never exceed the whole", font_size=30).to_edge(
            UP, buff=0.25)
        with self.voiceover(
            "<bookmark mark='a'/> Now expand a function in an orthonormal set: the sign function, whose squared "
            "norm is two. Its coefficients are its inner products with the Legendre polynomials. "
            "<bookmark mark='b'/> The partial sum is the projection onto the first N of them, and the error is "
            "perpendicular to it. So we have a right triangle: f is the hypotenuse, the partial sum and the error "
            "are the legs. <bookmark mark='c'/> Pythagoras: the squares of the coefficients add up to the squared "
            "length of the partial sum, which can never exceed the hypotenuse, two. That's Bessel's inequality. "
            "<bookmark mark='d'/> Watch the bar fill: one and a half from the first coefficient, then 1.72, 1.85, "
            "1.92, and 1.97 with forty polynomials. The red leftover is the squared error, and it keeps shrinking."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), Create(ax), Create(sg), FadeIn(s_l))
            vo.wait_until("b")
            self.play(Create(pc[0]), FadeIn(pl[0]))
            self.play(FadeIn(T), FadeIn(T_l))
            vo.wait_until("c")
            self.play(FadeIn(thm), Create(frame), FadeIn(f_l))
            vo.wait_until("d")
            self.play(LaggedStart(*[GrowFromEdge(s_, LEFT) for s_ in segs[:counts[0]]]), FadeIn(sums[0]),
                      FadeIn(lefts[0]))
            for k in range(1, len(Ms)):
                self.play(ReplacementTransform(pc[k - 1], pc[k]), FadeTransform(pl[k - 1], pl[k]),
                          LaggedStart(*[GrowFromEdge(s_, LEFT) for s_ in segs[counts[k - 1]:counts[k]]], lag_ratio=0.2),
                          FadeTransform(sums[k - 1], sums[k]), FadeTransform(lefts[k - 1], lefts[k]), run_time=1.3)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def parseval(self):
        rows = VGroup(
            label(r"\textbf{RCA 4.18} \ for an orthonormal set $\{e_n\}$ in $H$, \ these are equivalent:", font_size=28),
            label(r"(a) \ it is maximal: \ only $0$ is perpendicular to every $e_n$", font_size=26),
            label(r"(b) \ finite combinations of the $e_n$ are dense in $H$", font_size=26),
            label(r"(c) \ Parseval: \ $\sum_n |\langle f, e_n\rangle|^2 = \|f\|^2$ \ for every $f$", font_size=26,
                  color=C.EPS),
            label(r"(d) \ $\langle f, g\rangle = \sum_n \langle f, e_n\rangle\,\overline{\langle g, e_n\rangle}$: "
                  r"\ $H$ is a copy of $\ell^2$", font_size=26, color=C.INNER),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(UP, buff=0.35)
        rf = VGroup(
            label(r"Riesz--Fischer for coefficients: \ if $\sum |c_n|^2 < \infty$, \ then $\sum c_n e_n$ converges, since",
                  font_size=24),
            MathTex(r"\Big\|\sum_{m < n \le M} c_n e_n\Big\|^2 = \sum_{m < n \le M} |c_n|^2 \to 0", font_size=30),
        ).arrange(DOWN, buff=0.12).next_to(rows, DOWN, buff=0.35)
        ax = plain_axes([-1, 1, 0.5], [-1.1, 1.1, 1], 2.8, 1.6).move_to([-4.9, -2.45, 0])
        xs = np.linspace(-1, 1, 200)
        gx = polyline(ax, xs, xs, color=C.PATHOLOGY, stroke_width=3)
        from numpy.polynomial import legendre as L
        xg, wg = L.leggauss(40)
        cfs = [float(np.sum(wg * xg * L.legval(xg, [0] * n + [1]) * math.sqrt((2 * n + 1) / 2))) for n in range(8)]
        assert abs(cfs[1] ** 2 - 2 / 3) < 1e-12 and all(abs(cf) < 1e-13 for i, cf in enumerate(cfs) if i != 1)
        bars = VGroup()
        for n in range(8):
            h = 0.06 if n != 1 else 0.9
            col = C.EPS if n == 1 else C.SEQ  # the one nonzero coefficient; greyed when e_1 is dropped
            r_ = Rectangle(width=0.22, height=h, stroke_width=0, fill_color=col, fill_opacity=0.9)
            r_.move_to([-2.9 + 0.36 * n, -2.9 + h / 2, 0])
            bars.add(r_)
        cross = VGroup(Line(bars[1].get_corner(UL), bars[1].get_corner(DR), color=C.PATHOLOGY, stroke_width=3),
                       Line(bars[1].get_corner(DL), bars[1].get_corner(UR), color=C.PATHOLOGY, stroke_width=3))
        b_l = label(r"drop $e_1$: \ every coefficient of $x$ is $0$, \ but $\|x\|^2 = \tfrac23$", font_size=22,
                    color=C.PATHOLOGY).next_to(bars, RIGHT, buff=0.3)
        if b_l.get_right()[0] > 6.8:
            b_l.width = 6.8 - b_l.get_left()[0]
            b_l.next_to(bars, RIGHT, buff=0.3)
        g_l = MathTex(r"x", font_size=24, color=C.PATHOLOGY).next_to(ax, LEFT, buff=0.1)
        ok_l = label(r"all of the $e_n$: \ $\sum |\langle x, e_n\rangle|^2 = \tfrac23 = \|x\|^2$ \ (Parseval)",
                     font_size=22, color=C.EPS).next_to(bars, RIGHT, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> When does the bar fill completely? Rudin's theorem gives four equivalent answers. "
            "The orthonormal set is maximal, or its finite combinations are dense, or Parseval's identity holds for "
            "every vector, or inner products can be computed from coefficients. Then the Hilbert space is just a copy "
            "of the space of square-summable sequences. <bookmark mark='b'/> And the other direction is free: any "
            "square-summable coefficients define a vector, because the tails of the series have small norm, and the "
            "space is complete. <bookmark mark='c'/> Without maximality, Parseval fails. Remove e one from the "
            "Legendre polynomials, and the function x is perpendicular to everything left: all its coefficients are "
            "zero, but it isn't. <bookmark mark='d'/> Every Hilbert space has a maximal orthonormal set, by "
            "Hausdorff's maximality principle; that step is pure logic, with no picture. A separable one has a "
            "countable one, from Gram-Schmidt."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), Create(ax), Create(gx), FadeIn(g_l))
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.15) for r_ in rows[1:]], lag_ratio=0.5),
                      LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars], lag_ratio=0.2), run_time=4.0)
            self.play(FadeIn(ok_l))
            vo.wait_until("b")
            self.play(FadeIn(rf))
            vo.wait_until("c")
            self.play(bars[1].animate.set_fill(GREY_D), Create(cross), FadeOut(ok_l), FadeIn(b_l))
            vo.wait_until("d")
            self.play(Indicate(rows[1], color=C.EPS, scale_factor=1.02))
        self.wait(0.4)
        self.clear_scene()
