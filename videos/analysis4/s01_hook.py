from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis4.common import line_through, load, mapped_grid, square_axes
from videos.analysis4.compute import F_newton, J_newton


class Hook(VoiceoverScene):
    def construct(self):
        self.recap()
        self.newton()
        self.contraction()
        self.plan()

    # ------------------------------------------------------------------
    def recap(self):
        led = ledger(filled=3, highlight=4).scale(0.9)
        with self.voiceover(
            "Three rows of the ledger are filled: the real line, limits, and the first space of functions. "
            "<bookmark mark='l'/> Part 4 takes calculus into many dimensions, and it runs on one idea."
        ) as vo:
            self.play(FadeIn(led))
            vo.wait_until("l")
            self.play(Indicate(led.rows[3], color=C.EPS, scale_factor=1.03))
        self.play(FadeOut(led))

    # ------------------------------------------------------------------
    def newton(self):
        d = load("newton")
        its, res, root = d["its"], d["res"], d["root"]
        ax = square_axes([-0.3, 3.3, 1], [-0.3, 2.5, 1], 1.75, numbers=True, font_size=20,
                         x_axis_config={"decimal_number_config": {"num_decimal_places": 0}},
                         y_axis_config={"decimal_number_config": {"num_decimal_places": 0}}).move_to([-2.8, -0.75, 0])
        xs, ys = np.linspace(-0.3, 3.3, 241), np.linspace(-0.3, 2.5, 201)
        circ = contour_mobject(ax, contour_segments(lambda X, Y: X**2 + Y**2 - 4, xs, ys), C.SEQ, 3.5)
        hyp = contour_mobject(ax, contour_segments(lambda X, Y: X * Y - 1, xs, ys), C.APPROX, 3.5)
        cl = MathTex(r"x^2 + y^2 = 4", font_size=28, color=C.SEQ).move_to(ax.c2p(2.35, 1.7))
        hl = MathTex(r"xy = 1", font_size=28, color=C.APPROX).move_to(ax.c2p(2.95, 0.6))
        dots = [Dot(ax.c2p(*p), radius=0.07, color=WHITE) for p in its[:5]]
        tangents = []
        for k in range(4):
            p = its[k]
            Fp, Jp = F_newton(p), J_newton(p)
            # the zero set of each linearization: grad . (q - p) + F(p) = 0, a line with direction perp to grad
            g1, g2 = Jp[0], Jp[1]
            q1 = p - Fp[0] * g1 / (g1 @ g1)
            q2 = p - Fp[1] * g2 / (g2 @ g2)
            L1 = line_through(ax, q1, np.array([-g1[1], g1[0]]), C.SEQ, 2.0)
            L2 = line_through(ax, q2, np.array([-g2[1], g2[0]]), C.APPROX, 2.0)
            nxt = p - np.linalg.solve(Jp, Fp)
            assert np.allclose(nxt, its[k + 1])  # the tangent lines cross at the next iterate
            tangents.append(VGroup(L1, L2))
        steps = [Arrow(ax.c2p(*its[k]), ax.c2p(*its[k + 1]), buff=0.05, color=C.EPS, stroke_width=3,
                       tip_length=0.15, max_tip_length_to_length_ratio=0.3) for k in range(4)]
        head = VGroup(label(r"Two equations, two unknowns: \ where do the curves cross?", font_size=30),
                      MathTex(r"F(x, y) = (x^2 + y^2 - 4,\ xy - 1) = 0", font_size=32)).arrange(DOWN, buff=0.12)
        head.to_edge(UP, buff=0.25)
        tab = VGroup(MathTex(r"k", r"\quad |F(p_k)|", font_size=28, color=GREY_A))
        for k in range(6):
            r_ = float(res[k])
            txt = f"{r_:.3g}" if r_ > 1e-3 else (sci(r_, 1) if r_ > 0 else "0")
            tab.add(MathTex(rf"{k}", rf"\quad {txt}", font_size=28))
        tab.arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([4.6, 0.2, 0])
        regrid(tab)
        rule = VGroup(label(r"each step: replace $F$ by its linearization", font_size=24, color=GREY_A),
                      label(r"at $p_k$: two lines; \ they cross at $p_{k+1}$", font_size=24, color=GREY_A),
                      label(r"correct digits double each step", font_size=24, color=C.EPS)
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.08).next_to(tab, DOWN, buff=0.35)
        assert 0.5e-11 < res[4] < 2e-11 and abs(root[0] ** 2 + root[1] ** 2 - 4) < 1e-12
        with self.voiceover(
            "<bookmark mark='a'/> Here are two equations in two unknowns: a circle and a hyperbola, and we want a "
            "point where they cross. <bookmark mark='b'/> Newton's method starts from a guess. At the guess, replace "
            "each of the two functions by its best linear approximation. Where each approximation is zero is a "
            "straight line, and two lines are easy: they cross at one point, the next guess. <bookmark mark='c'/> Repeat. <bookmark mark='d'/> After four "
            "steps F is about ten to the minus eleven away from zero. Once close, the number of correct digits doubles at every "
            "step."
        ) as vo:
            self.play(FadeIn(head), Create(ax))
            vo.wait_until("a")
            self.play(Create(circ), Create(hyp), FadeIn(cl), FadeIn(hl))
            vo.wait_until("b")
            self.play(FadeIn(dots[0], scale=1.5), FadeIn(tab[0]), FadeIn(tab[1]))
            self.play(Create(tangents[0]), run_time=1.2)
            self.play(GrowArrow(steps[0]), FadeIn(dots[1]), FadeIn(tab[2]))
            vo.wait_until("c")
            for k in range(1, 4):
                self.play(FadeOut(tangents[k - 1]), Create(tangents[k]), run_time=0.9)
                self.play(GrowArrow(steps[k]), FadeIn(dots[k + 1]), FadeIn(tab[k + 2]), run_time=0.8)
            self.play(FadeOut(tangents[3]))
            vo.wait_until("d")
            self.play(FadeIn(tab[6]), FadeIn(rule))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def contraction(self):
        ax = square_axes([-3.6, 3.6, 1], [-2.4, 2.4, 1], 1.0).move_to([-2.4, -0.5, 0])
        ax.set_opacity(0)
        star = np.array([0.6, -0.3])
        c, th = 0.62, math.radians(48)
        R = c * np.array([[math.cos(th), -math.sin(th)], [math.sin(th), math.cos(th)]])

        def T(P, k):
            Q = P - star
            for _ in range(k):
                Q = Q @ R.T
            return Q + star

        copies = []
        cols = [interpolate_color(ManimColor(C.SEQ), ManimColor(C.EPS), k / 6) for k in range(7)]
        for k in range(7):
            copies.append(mapped_grid(ax, lambda P, k=k: T(P, k), (-3.0, 3.0), (-2.0, 2.0), n=7, color=cols[k],
                                      stroke_width=2.0 if k < 4 else 1.4))
        fixed = Dot(ax.c2p(*star), radius=0.08, color=WHITE)
        head = label(r"A contraction of the plane: \ every distance shrinks by the factor $c = 0.62$", font_size=30)
        head.to_edge(UP, buff=0.3)
        side = VGroup(
            MathTex(r"d(Tp, Tq) \le c\, d(p, q)", font_size=34, color=C.EPS),
            label(r"iterate from anywhere: \ one fixed point", font_size=24),
            label(r"in this part, the same theorem", font_size=24, color=GREY_A),
            label(r"solves four problems:", font_size=24, color=GREY_A),
            label(r"Newton's method near a root", font_size=24, color=C.SEQ),
            label(r"differential equations (Picard)", font_size=24, color=C.APPROX),
            label(r"the inverse function theorem", font_size=24, color=C.CONNECTED_SET),
            label(r"the implicit function theorem", font_size=24, color=C.CLOSED_SET),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([4.6, -0.4, 0])
        side[2].shift(DOWN * 0.15)
        side[3].shift(DOWN * 0.15)
        side[4:].shift(DOWN * 0.15 + RIGHT * 0.2)
        with self.voiceover(
            "<bookmark mark='a'/> Behind Newton's method is a simpler picture. Take a map of the plane that shrinks "
            "every distance by a fixed factor, here 0.62, while it turns and slides. <bookmark mark='b'/> Apply it "
            "again and again, and the whole plane collapses onto one point, the only point the map leaves where it is. "
            "<bookmark mark='c'/> That's the contraction principle, and this part uses it four times: for Newton's "
            "method, for differential equations, and for the inverse and implicit function theorems. Equation after "
            "equation, the solution is the fixed point of a contraction."
        ) as vo:
            self.play(FadeIn(head), Create(copies[0]), run_time=1.5)
            vo.wait_until("a")
            self.play(FadeIn(side[0]), TransformFromCopy(copies[0], copies[1]), run_time=1.5)
            vo.wait_until("b")
            for k in range(2, 7):
                self.play(TransformFromCopy(copies[k - 1], copies[k]), copies[k - 2].animate.set_stroke(opacity=0.35),
                          run_time=0.8)
            self.play(FadeIn(fixed, scale=2), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.1) for r_ in side[2:]], lag_ratio=0.3), run_time=3.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def plan(self):
        chapters = [
            r"Linear maps and their norms", r"The derivative is a linear map", r"Partial derivatives are not enough",
            r"The contraction principle", r"Picard: differential equations in $C[a, b]$",
            r"The inverse function theorem", r"The implicit function theorem",
            r"Mixed partials; differentiating under $\int$", r"A tour of integration in many variables",
        ]
        items = VGroup(*[label(rf"{i + 1}.\; {t}", font_size=28) for i, t in enumerate(chapters)])
        items.arrange(DOWN, aligned_edge=LEFT, buff=0.24).shift(DOWN * 0.45)
        head = label(r"Part 4: Calculus in many dimensions", font_size=42).to_edge(UP, buff=0.45)
        sub = label(r"Rudin, \textit{Principles}, chapter 9, \ and a tour of chapter 10", font_size=26,
                    color=GREY_B).next_to(head, DOWN, buff=0.15)
        with self.voiceover(
            "Here's the plan, following chapter nine of Rudin's Principles. <bookmark mark='a'/> First the linear "
            "maps, and the derivative as a linear map, and why partial derivatives alone don't make one. "
            "<bookmark mark='b'/> Then the contraction principle, and what it builds: solutions of differential "
            "equations, and the inverse and implicit function theorems. <bookmark mark='c'/> We finish with mixed "
            "partial derivatives, one more swap of limits, and a guided tour of chapter ten."
        ) as vo:
            self.play(FadeIn(head), FadeIn(sub))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(items[i], shift=RIGHT * 0.2) for i in range(3)], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(items[i], shift=RIGHT * 0.2) for i in range(3, 7)], lag_ratio=0.3))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(items[i], shift=RIGHT * 0.2) for i in range(7, 9)], lag_ratio=0.3))
        self.wait(0.6)
        self.clear_scene()
