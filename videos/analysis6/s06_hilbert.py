from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis6.common import between, load, plain_axes, pnorm, polyline, square_axes, trap


class Hilbert(VoiceoverScene):
    def construct(self):
        self.card()
        self.schwarz()
        self.parallelogram()
        self.dictionary()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(5, r"Inner products and the parallelogram law", r"Which norms come from an angle?", lit=(),
                            part=6)
        with self.voiceover("Chapter five: inner products, where distances come with angles."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def schwarz(self):
        t = np.linspace(0, 1, 200001)
        X, Y = np.exp(t), t
        xx, xy, yy = trap(X * X, t), trap(X * Y, t), trap(Y * Y, t)
        assert abs(xx - (math.e**2 - 1) / 2) < 1e-9 and abs(xy - 1) < 1e-9 and abs(yy - 1 / 3) < 1e-9
        lam_star, qmin = xy / yy, xx - xy**2 / yy
        theta = math.degrees(math.acos(xy / math.sqrt(xx * yy)))
        axs = VGroup(
            label(r"\textbf{RCA 4.1} \ an inner product: \ $\langle x, y\rangle = \overline{\langle y, x\rangle}$, "
                  r"\ linear in $x$, \ $\langle x, x\rangle > 0$ for $x \ne 0$", font_size=26),
            MathTex(r"L^2(\mu):\ \langle f, g\rangle = \int f\,\bar g\,d\mu, \qquad \|f\| = \sqrt{\langle f, f\rangle}",
                    font_size=32, color=C.INNER),
        ).arrange(DOWN, buff=0.15).to_edge(UP, buff=0.25)
        ax = plain_axes([0, 1, 0.5], [0, 3.2, 1], 3.6, 3.0, numbers=True, font_size=18,
                        x_axis_config={"decimal_number_config": {"num_decimal_places": 1}},
                        y_axis_config={"decimal_number_config": {"num_decimal_places": 0}}).move_to([-4.6, -1.2, 0])
        gx = polyline(ax, t[::500], X[::500], color=C.FUNC, stroke_width=4)
        lT = ValueTracker(0.5)
        gy = always_redraw(lambda: polyline(ax, t[::500], lT.get_value() * Y[::500], color=C.APPROX, stroke_width=3.5))
        gap = always_redraw(lambda: between(ax, t[::500], X[::500], lT.get_value() * Y[::500], C.INNER, 0.3))
        xl = MathTex(r"x = e^t", font_size=26, color=C.FUNC).next_to(ax.c2p(0.2, 1.4), UP, buff=0.05)
        yl = always_redraw(lambda: MathTex(rf"\lambda y = {lT.get_value():.2f}\,t", font_size=26,
                                           color=C.APPROX).next_to(ax, UP, buff=0.1))
        qx = plain_axes([0, 6, 1], [0, 3.6, 1], 4.4, 3.0, numbers=True, font_size=18,
                        x_axis_config={"decimal_number_config": {"num_decimal_places": 0}},
                        y_axis_config={"decimal_number_config": {"num_decimal_places": 0}}).move_to([0.4, -1.2, 0])
        ls = np.linspace(0, 6, 300)
        par = polyline(qx, ls, xx - 2 * ls * xy + ls**2 * yy, color=C.INNER, stroke_width=3.5)
        q_l = MathTex(r"q(\lambda) = \|x - \lambda y\|^2", font_size=26, color=C.INNER).next_to(qx, UP, buff=0.1)
        lam_l = MathTex(r"\lambda", font_size=24, color=GREY_B).next_to(qx, DOWN, buff=0.35)
        qdot = always_redraw(lambda: Dot(qx.c2p(lT.get_value(), xx - 2 * lT.get_value() * xy + lT.get_value()**2 * yy),
                                         radius=0.08, color=C.EPS))
        vert = VGroup(DashedLine(qx.c2p(lam_star, 0), qx.c2p(lam_star, qmin), color=C.EPS, stroke_width=2),
                      MathTex(rf"\min = {qmin:.4f} \ge 0", font_size=24, color=C.EPS).next_to(qx.c2p(lam_star, qmin), UP,
                                                                                           buff=0.4))
        side = VGroup(
            MathTex(r"q(\lambda) = \|x\|^2 - 2\lambda\,\mathrm{Re}\langle x, y\rangle + \lambda^2 \|y\|^2", font_size=26),
            MathTex(rf"= {xx:.4f} - 2\lambda \cdot {xy:.0f} + \lambda^2 \cdot \tfrac13", font_size=26, color=GREY_A),
            label(r"never negative, \ so its discriminant is $\le 0$:", font_size=22, color=GREY_B),
            MathTex(r"|\langle x, y\rangle|^2 \le \|x\|^2\, \|y\|^2", font_size=32, color=C.EPS),
            MathTex(rf"1 \le {xx:.4f} \cdot \tfrac13 = {xx * yy:.4f}", font_size=26, color=GREY_A),
            MathTex(rf"\text{{angle}}(e^t, t) = \arccos \tfrac{{\langle x, y\rangle}}{{\|x\|\|y\|}} = {theta:.1f}^\circ",
                    font_size=28, color=C.INNER),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([4.9, -1.1, 0])
        for r_ in side:
            if r_.width > 3.9:
                r_.width = 3.9
        side.arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([4.9, -1.1, 0])
        side.arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([4.95, -1.1, 0])
        assert qmin > 0 and abs(lam_star - 3) < 1e-6
        with self.voiceover(
            "<bookmark mark='a'/> An inner product is a way to multiply two vectors and get a number: symmetric, "
            "after a complex conjugate, linear, and positive. On L two, it's the integral of f times the conjugate "
            "of g, and its norm is the square root of the inner product of f with itself. "
            "<bookmark mark='b'/> The Cauchy-Schwarz inequality comes straight from positivity. Take x equals e to "
            "the t and y equals t, on the unit interval. The squared distance from x to lambda times y is a "
            "quadratic in lambda, <bookmark mark='c'/> and it can never go below zero. <bookmark mark='d'/> Its "
            "minimum, at lambda equals three, is 0.1945. A quadratic that stays positive has a negative "
            "discriminant, and that's Cauchy-Schwarz. <bookmark mark='e'/> It also means the ratio of the inner "
            "product to the two lengths is a cosine. In L two, e to the t and t meet at an angle of 14.3 degrees."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(axs[0]), Create(ax), Create(gx), FadeIn(xl), FadeIn(gy), FadeIn(yl))
            self.play(FadeIn(axs[1]))
            vo.wait_until("b")
            self.play(FadeIn(gap))
            self.play(Create(qx), FadeIn(q_l), FadeIn(lam_l), Create(par), FadeIn(qdot), FadeIn(side[:2]))
            vo.wait_until("c")
            self.play(lT.animate.set_value(5.5), run_time=2.5)
            self.play(lT.animate.set_value(lam_star), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(vert), FadeIn(side[2:4]))
            self.play(FadeIn(side[4]))
            vo.wait_until("e")
            self.play(FadeIn(side[5]))
        for m in (gy, gap, yl, qdot):
            m.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def parallelogram(self):
        d = load("parallel")
        res = d["res"]
        ax = square_axes([-0.6, 2.6, 1], [-1.2, 2.0, 1], 1.35).move_to([-4.2, -0.4, 0])
        ax.set_opacity(0.35)
        x = np.array([1.6, 0.0])
        thT = ValueTracker(math.radians(65))
        r_y = 1.1
        normT = ValueTracker(2.0)

        def yv():
            return r_y * np.array([math.cos(thT.get_value()), math.sin(thT.get_value())])

        def pic():
            y = yv()
            O, A, B, S = np.zeros(2), x, y, x + y
            g = VGroup(
                Polygon(*[ax.c2p(*P) for P in (O, A, S, B)], stroke_width=0, fill_color=C.INNER, fill_opacity=0.12),
                Arrow(ax.c2p(*O), ax.c2p(*A), buff=0, color=C.SEQ, stroke_width=4, tip_length=0.18),
                Arrow(ax.c2p(*O), ax.c2p(*B), buff=0, color=C.APPROX, stroke_width=4, tip_length=0.18),
                DashedLine(ax.c2p(*A), ax.c2p(*S), color=C.APPROX, stroke_width=2),
                DashedLine(ax.c2p(*B), ax.c2p(*S), color=C.SEQ, stroke_width=2),
                Line(ax.c2p(*O), ax.c2p(*S), color=C.EPS, stroke_width=4),
                Line(ax.c2p(*A), ax.c2p(*B), color=C.MEASURE, stroke_width=4),
            )
            return g

        pg = always_redraw(pic)

        def reads():
            y = yv()
            p = np.inf if normT.get_value() > 50 else (1.0 if normT.get_value() < 1.5 else 2.0)
            n = lambda v: pnorm(v, p)  # noqa: E731
            lhs = n(x + y) ** 2 + n(x - y) ** 2
            rhs = 2 * n(x) ** 2 + 2 * n(y) ** 2
            name = {1.0: r"\|\cdot\|_1", 2.0: r"\|\cdot\|_2", np.inf: r"\|\cdot\|_\infty"}[p]
            ok = abs(lhs - rhs) < 1e-9
            return VGroup(
                MathTex(rf"\text{{norm: }} {name}", font_size=28, color=C.DIST),
                MathTex(rf"\|x + y\|^2 + \|x - y\|^2 = {lhs:.3f}", font_size=28, color=C.EPS),
                MathTex(rf"2\|x\|^2 + 2\|y\|^2 = {rhs:.3f}", font_size=28, color=C.SEQ),
                MathTex(r"\text{equal}" if ok else r"\text{not equal}", font_size=28,
                        color=C.CONNECTED_SET if ok else C.PATHOLOGY),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([-4.0, -2.75, 0])

        rd = always_redraw(reads)
        tab = VGroup(
            label(r"$f = x$, \ $g = 1 - x^2$ \ in $L^p[0, 1]$:", font_size=26),
            MathTex(r"p", r"\quad \|f + g\|^2 + \|f - g\|^2", r"\quad 2\|f\|^2 + 2\|g\|^2", font_size=26, color=GREY_A),
        )
        for p, lhs, rhs in res:
            col = C.CONNECTED_SET if abs(lhs - rhs) < 1e-8 else C.PATHOLOGY
            tab.add(MathTex(f"{p:.0f}", rf"\quad {lhs:.5f}", rf"\quad {rhs:.5f}", font_size=28, color=col))
        tab.arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([3.6, 0.2, 0])
        for row in tab[2:]:
            row[0].align_to(tab[1][0], LEFT)
            row[1].align_to(tab[1][1], LEFT)
            row[2].align_to(tab[1][2], LEFT)
        thm = VGroup(
            label(r"the law holds in every inner-product space \ (expand the squares),", font_size=24),
            label(r"and only there: \ if it holds, \ $\langle x, y\rangle = \tfrac14(\|x + y\|^2 - \|x - y\|^2)$",
                  font_size=24),
            label(r"is an inner product \ (Jordan and von Neumann, 1935)", font_size=24, color=GREY_A),
            label(r"so among the $L^p$, \ only $L^2$ has angles", font_size=26, color=C.INNER),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(tab, DOWN, buff=0.35)
        for r_ in thm:
            if r_.width > 6.4:
                r_.width = 6.4
        thm.arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(tab, DOWN, buff=0.35)
        head = label(r"The parallelogram law: \ $\|x + y\|^2 + \|x - y\|^2 = 2\|x\|^2 + 2\|y\|^2$", font_size=32).to_edge(
            UP, buff=0.3)
        assert abs(res[1, 1] - res[1, 2]) < 1e-8 and abs(res[0, 1] - res[0, 2]) > 0.1 and abs(res[2, 1] - res[2, 2]) > 0.1
        with self.voiceover(
            "<bookmark mark='a'/> Which norms come from an inner product? The test is a fact about parallelograms: "
            "the squares of the two diagonals add up to the squares of the four sides. <bookmark mark='b'/> With "
            "the ordinary length, turn the parallelogram any way you like and the two sides of the equation agree. "
            "<bookmark mark='c'/> Measure with the taxicab norm instead, and they don't. <bookmark mark='d'/> For "
            "functions: x and one minus x squared, in L p of the unit interval. For p equals one and three, the law "
            "fails; for p equals two it holds, to every digit. <bookmark mark='e'/> And the law is exactly the "
            "test: when it holds, the polarization formula defines an inner product that gives back the norm. So of "
            "all the L p spaces, only L two has angles."
        ) as vo:
            self.play(FadeIn(head), Create(ax))
            vo.wait_until("a")
            self.play(FadeIn(pg))
            vo.wait_until("b")
            self.play(FadeIn(rd))
            self.play(thT.animate.set_value(math.radians(130)), run_time=2.5)
            self.play(thT.animate.set_value(math.radians(35)), run_time=2.0)
            vo.wait_until("c")
            self.play(normT.animate.set_value(1.0), run_time=0.1)
            self.play(thT.animate.set_value(math.radians(100)), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(tab[:2]))
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[2:]], lag_ratio=0.5), run_time=2.0)
            vo.wait_until("e")
            self.play(FadeIn(thm[:3]))
            self.play(FadeIn(thm[3]))
        for m in (pg, rd):
            m.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def dictionary(self):
        card = dictionary_card(r"$\R^n$", r"a Hilbert space $H$ \ (e.g.\ $L^2$, $\ell^2$)", [
            (r"$x \cdot y = \sum x_i y_i$", r"$\langle f, g\rangle = \int f \bar g$"),
            (r"length $|x|$", r"$\|f\| = \langle f, f\rangle^{1/2}$, \ complete"),
            (r"right angles: \ Pythagoras", r"$\langle f, g\rangle = 0 \Rightarrow \|f + g\|^2 = \|f\|^2 + \|g\|^2$"),
            (r"nearest point of a plane", r"projection onto a closed subspace \ (ch.~6)"),
            (r"a functional is $x \mapsto x \cdot y$", r"Riesz: \ every bounded functional is $\langle \cdot, g\rangle$ \ (ch.~7)"),
            (r"an orthonormal basis", r"orthonormal bases; \ Parseval \ (ch.~8)"),
            (r"closed bounded sets are compact", r"$e_1, e_2, \ldots$: \ $\|e_m - e_n\| = \sqrt 2$, \ no limit"),
        ], font_size=24, strike=(6,))
        card.scale(0.95).to_edge(DOWN, buff=0.3)
        head = label(r"The dictionary: \ geometry that survives into infinite dimensions", font_size=32).to_edge(UP,
                                                                                                              buff=0.25)
        with self.voiceover(
            "<bookmark mark='a'/> A complete inner-product space is a Hilbert space, and almost all of the plane's "
            "geometry carries over. <bookmark mark='b'/> Dot products become integrals. Lengths become norms, and "
            "the space is complete. Pythagoras holds for perpendicular functions. <bookmark mark='c'/> And the next "
            "three chapters carry over three more facts: nearest points, functionals as vectors, and orthonormal "
            "bases. <bookmark mark='d'/> One thing does not survive. The unit vectors e one, e two, and so on are "
            "all at distance root two from each other, so the closed unit ball is not compact. Compactness is the "
            "price of infinitely many dimensions."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), FadeIn(card.titles))
            vo.wait_until("b")
            for i in range(3):
                self.play(FadeIn(card.rows[i][:2]), FadeIn(card.arrows[i]), run_time=0.7)
            vo.wait_until("c")
            for i in range(3, 6):
                self.play(FadeIn(card.rows[i][:2]), FadeIn(card.arrows[i]), run_time=0.7)
            vo.wait_until("d")
            self.play(FadeIn(card.rows[6][:2]), FadeIn(card.arrows[6]))
            self.play(Create(card.rows[6][2]))
        self.wait(0.4)
        self.clear_scene()
