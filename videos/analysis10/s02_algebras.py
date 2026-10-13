from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis10.common import heatmap, load, plain_axes, square_axes


class BanachAlgebras(VoiceoverScene):
    def construct(self):
        self.card()
        self.examples()
        self.neumann()
        self.open_set()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(1, r"Banach algebras", r"What can we do with operators that we do with numbers?", lit=(1932,),
                            part=10)
        with self.voiceover("Chapter one: Banach algebras, where elements can be multiplied as well as added."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def examples(self):
        card = dictionary_card(r"algebra", r"product, \ norm", [
            (r"$C(K)$, \ $K$ compact", r"$(fg)(x) = f(x)g(x)$, \ $\sup|f|$"),
            (r"$B(X)$, \ $X$ a Banach space", r"composition $ST$, \ operator norm"),
            (r"$L^1(\mathbb R)$", r"convolution $f * g$, \ $\int |f|$ \ (Part 9)"),
            (r"$\ell^1(\mathbb Z)$", r"$(a * b)_n = \sum_k a_k b_{n-k}$, \ $\sum |a_n|$"),
            (r"the disc algebra $A(\mathbb D)$", r"products of holomorphic functions, \ sup norm"),
        ], font_size=24)
        card.scale_to_fit_width(12.0).move_to(UP * 0.35)
        # submultiplicativity, checked on random matrices and random l^1 sequences
        rng = np.random.default_rng(2)
        worst_m = 0.0
        for _ in range(2000):
            A, B = rng.normal(size=(2, 5, 5))
            worst_m = max(worst_m, np.linalg.norm(A @ B, 2) / (np.linalg.norm(A, 2) * np.linalg.norm(B, 2)))
        worst_l = 0.0
        for _ in range(2000):
            a, b = rng.normal(size=(2, 30))
            worst_l = max(worst_l, np.abs(np.convolve(a, b)).sum() / (np.abs(a).sum() * np.abs(b).sum()))
        assert worst_m <= 1 + 1e-12 and worst_l <= 1 + 1e-12
        rule = VGroup(
            MathTex(r"\|xy\| \le \|x\|\,\|y\|, \qquad \|e\| = 1", font_size=36, color=C.EPS),
            MathTex(rf"\text{{largest ratio in 2000 random tries: matrices }} {worst_m:.4f}, \ \ \ell^1 \ {worst_l:.4f}",
                    font_size=24, color=GREY_A),
        ).arrange(DOWN, buff=0.12).to_edge(DOWN, buff=0.3)
        head = label(r"\textbf{RCA 18.1, FA 10.1} \ a complete normed space with a product", font_size=32).to_edge(UP, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> A Banach algebra is a complete normed space where you can also multiply, with the "
            "norm of a product at most the product of the norms. <bookmark mark='b'/> The continuous functions on a "
            "compact set, with the pointwise product. The bounded operators on a Banach space, with composition: the "
            "main example. The integrable functions with convolution, from Part 9, and summable sequences with "
            "convolution, and the disc algebra of Part 7. <bookmark mark='c'/> In random trials the ratio never "
            "exceeds one."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), FadeIn(rule[0]))
            vo.wait_until("b")
            self.play(FadeIn(card.titles))
            self.play(LaggedStart(*[AnimationGroup(FadeIn(r_), FadeIn(a_)) for r_, a_ in zip(card.rows, card.arrows)],
                                  lag_ratio=0.5), run_time=5.0)
            vo.wait_until("c")
            self.play(FadeIn(rule[1]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def neumann(self):
        d = load("neumann")
        errs, bound = d["errs"], d["bound"]
        n = np.arange(40)
        ax = plain_axes([0, 40, 10], [-7, 1, 1], 6.2, 4.4, numbers=True, font_size=18,
                        x_axis_config={"decimal_number_config": {"num_decimal_places": 0}},
                        y_axis_config={"decimal_number_config": {"num_decimal_places": 0}}).move_to([-3.2, -0.5, 0])
        xl = MathTex(r"n", font_size=22).next_to(ax.x_axis, RIGHT, buff=0.1)
        yl = MathTex(r"\log_{10}\Big\|\sum_{k \le n} A^k - (I - A)^{-1}\Big\|", font_size=22).next_to(ax, UP, buff=0.1)
        bl = polyline_(ax, n, np.log10(bound), C.PATHOLOGY)
        dots = VGroup(*[Dot(ax.c2p(k, math.log10(e)), radius=0.045, color=C.OPERATOR) for k, e in zip(n, errs)])
        bt = MathTex(r"\frac{0.8^{\,n+1}}{1 - 0.8}", font_size=26, color=C.PATHOLOGY).next_to(ax.c2p(30, math.log10(bound[30])),
                                                                                         UP, buff=0.15)
        assert np.all(errs <= bound * (1 + 1e-9))
        lad = VGroup(
            MathTex(r"(I - A)(I + A + \cdots + A^n) = I - A^{n+1}", font_size=30),
            MathTex(r"\|A^{n+1}\| \le \|A\|^{n+1} \to 0 \quad \text{if } \|A\| < 1", font_size=30),
            MathTex(r"(I - A)^{-1} = \sum_{n \ge 0} A^n", font_size=36, color=C.EPS),
            MathTex(r"\big\|(I - A)^{-1}\big\| \le \frac{1}{1 - \|A\|}", font_size=30, color=GREY_A),
            label(r"a random $6 \times 6$ complex $A$ with $\|A\| = 0.8$:", font_size=24),
            label(r"every error under the geometric bound", font_size=24, color=C.OPERATOR),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([3.6, -0.3, 0])
        head = label(r"The geometric series, \ for operators", font_size=34).to_edge(UP, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> The first tool is the oldest series there is. Multiply I minus A by one plus A "
            "plus up to A to the n, and everything telescopes to I minus A to the n plus one. "
            "<bookmark mark='b'/> If the norm of A is below one, that last term dies, so I minus A is invertible, "
            "and its inverse is the geometric series: the Neumann series. <bookmark mark='c'/> For a random matrix "
            "of norm 0.8, the partial sums close in on the inverse, always under the geometric bound."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), FadeIn(lad[0]))
            vo.wait_until("b")
            self.play(FadeIn(lad[1]))
            self.play(FadeIn(lad[2]), FadeIn(lad[3]))
            vo.wait_until("c")
            self.play(Create(ax), FadeIn(xl), FadeIn(yl), FadeIn(lad[4]))
            self.play(Create(bl), FadeIn(bt))
            self.play(LaggedStart(*[FadeIn(d_, scale=0.5) for d_ in dots], lag_ratio=0.05), FadeIn(lad[5]), run_time=2.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def open_set(self):
        # a slice through the 2 x 2 matrices: M(s, t) = [[1 + s, t], [t, 1 - s]], det = 1 - s^2 - t^2
        ax = square_axes([-2.2, 2.8, 1], [-2.2, 2.2, 1], 1.15, numbers=True, font_size=16,
                         x_axis_config={"decimal_number_config": {"num_decimal_places": 0}},
                         y_axis_config={"decimal_number_config": {"num_decimal_places": 0}}).move_to([-3.3, -0.4, 0])
        img = heatmap(lambda X, Y: np.log10(np.abs(1 - X * X - Y * Y) + 1e-3), (-2.2, 2.8), (-2.2, 2.2),
                      ax.c2p(2.8, 0)[0] - ax.c2p(-2.2, 0)[0], ax.c2p(0, 2.2)[1] - ax.c2p(0, -2.2)[1], -1.5, 1.5,
                      neg=C.PATHOLOGY, pos=C.OPERATOR).move_to(ax.c2p(0.3, 0))
        unit = ax.c2p(1, 0)[0] - ax.c2p(0, 0)[0]
        sing = Circle(radius=unit, color=C.PATHOLOGY, stroke_width=4).move_to(ax.c2p(0, 0))
        sl = MathTex(r"\det = 0", font_size=24, color=C.PATHOLOGY).next_to(ax.c2p(-0.72, 0.72), UL, buff=0.05)
        # the Neumann balls: around I (radius 1 / ||I^-1|| = 1) and around A = M(1.6, 0) (radius 1 / ||A^-1|| = 0.6)
        A = np.array([[2.6, 0], [0, -0.6]])
        rA = 1 / np.linalg.norm(np.linalg.inv(A), 2)
        assert abs(rA - 0.6) < 1e-12
        # in this slice ||M(s, t) - M(s', t')|| = |(s, t) - (s', t')|, so the balls are discs, tangent to det = 0
        E1, E2 = np.diag([1.0, -1.0]), np.array([[0.0, 1.0], [1.0, 0.0]])
        rng = np.random.default_rng(4)
        for _ in range(200):
            s, t = rng.normal(size=2)
            assert abs(np.linalg.norm(s * E1 + t * E2, 2) - math.hypot(s, t)) < 1e-12
        b1 = DashedVMobject(Circle(radius=unit * 0.999, color=C.EPS, stroke_width=3).move_to(ax.c2p(0, 0)), num_dashes=40)
        b2 = Circle(radius=unit * rA, color=C.EPS, stroke_width=3, fill_color=C.EPS, fill_opacity=0.15).move_to(
            ax.c2p(1.6, 0))
        dI = Dot(ax.c2p(0, 0), radius=0.06, color=WHITE)
        dA = Dot(ax.c2p(1.6, 0), radius=0.06, color=WHITE)
        lI = MathTex(r"I", font_size=26).next_to(dI, DOWN, buff=0.08)
        lA = MathTex(r"A", font_size=26).next_to(dA, DOWN, buff=0.08)
        sl2 = MathTex(r"M(s, t) = \begin{pmatrix} 1 + s & t \\ t & 1 - s\end{pmatrix}", font_size=26).next_to(ax, UP,
                                                                                                         buff=0.1)
        rows = VGroup(
            label(r"\textbf{RCA 18.4} \ if $x$ is invertible and $\|y\| < 1/\|x^{-1}\|$:", font_size=24),
            MathTex(r"x - y = x\,(e - x^{-1}y) \ \text{ is invertible (Neumann)}", font_size=28),
            label(r"so the invertible elements form an open set,", font_size=24, color=C.EPS),
            label(r"and $x \mapsto x^{-1}$ is continuous", font_size=24, color=C.EPS),
            MathTex(rf"\text{{here: }} 1/\|A^{{-1}}\| = {rA:.1f}, \ \text{{exactly the distance to }} \det = 0", font_size=24,
                    color=GREY_A),
            label(r"Part 4's lemma (PMA 9.8), \ in its final home", font_size=22, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to([3.6, -0.2, 0])
        for r_ in rows:
            if r_.width > 6.4:
                r_.width = 6.4
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to([3.6, -0.2, 0])
        head = label(r"The invertible elements form an open set", font_size=34).to_edge(UP, buff=0.25)
        with self.voiceover(
            "<bookmark mark='a'/> Here's a slice through the two by two matrices, around the identity. The red circle "
            "is where the determinant vanishes. <bookmark mark='b'/> The Neumann series says: if x is invertible, "
            "anything closer to x than one over the norm of x inverse is invertible too. Around the identity that's a "
            "disc of radius one, and around this matrix A, radius 0.6. <bookmark mark='c'/> Both discs touch the "
            "singular circle exactly, so the bound is sharp. The invertible elements form an open set, and inversion "
            "is continuous: the lemma from Part 4, in its final home."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), FadeIn(img), Create(ax), FadeIn(sl2))
            self.play(Create(sing), FadeIn(sl))
            vo.wait_until("b")
            self.play(FadeIn(dI), FadeIn(lI), Create(b1), FadeIn(rows[:2]))
            self.play(FadeIn(dA), FadeIn(lA), DrawBorderThenFill(b2))
            vo.wait_until("c")
            self.play(FadeIn(rows[2:5]))
            self.play(FadeIn(rows[5]))
        self.wait(0.4)
        self.clear_scene()


def polyline_(ax, xs, ys, color, stroke_width=3):
    m = VMobject(color=color, stroke_width=stroke_width)
    m.set_points_as_corners([ax.c2p(float(a), float(b)) for a, b in zip(xs, ys)])
    return m
