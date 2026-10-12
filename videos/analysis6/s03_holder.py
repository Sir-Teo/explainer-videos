from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis6.common import area_under, load, p_ball, plain_axes, pnorm, polyline, square_axes


class Holder(VoiceoverScene):
    def construct(self):
        self.card()
        self.young()
        self.holder()
        self.minkowski()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(2, r"Young, H\"older and Minkowski", r"Why is the $p$-norm a distance?", lit=(), part=6)
        with self.voiceover("Chapter two: three inequalities, and the pictures that prove them."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def young(self):
        d = load("young")
        p, a0 = float(d["p"]), float(d["a"])
        q = p / (p - 1)
        ax = square_axes([0, 1.7, 0.5], [0, 1.7, 0.5], 2.6, numbers=True, font_size=18,
                         x_axis_config={"decimal_number_config": {"num_decimal_places": 1}},
                         y_axis_config={"decimal_number_config": {"num_decimal_places": 1}}).move_to([-3.4, -0.4, 0])
        xs = np.linspace(0, 1.3, 300)
        curve = polyline(ax, xs, xs ** (p - 1), color=WHITE, stroke_width=3.5)
        c_l = MathTex(r"y = x^{p-1}", font_size=28).next_to(ax.c2p(1.3, 1.69), RIGHT, buff=0.1).shift(DOWN * 0.25)
        bT = ValueTracker(float(d["b"]))
        A1 = area_under(ax, np.linspace(0, a0, 200), np.linspace(0, a0, 200) ** (p - 1), C.MEASURE, 0.45)

        def a2():
            b = bT.get_value()
            ys = np.linspace(0, b, 200)
            pts = [ax.c2p(0, 0)] + [ax.c2p(y ** (1 / (p - 1)), y) for y in ys] + [ax.c2p(0, b)]
            return Polygon(*pts, stroke_width=0, fill_color=C.SEQ, fill_opacity=0.45)

        A2 = always_redraw(a2)
        rect = always_redraw(lambda: Polygon(ax.c2p(0, 0), ax.c2p(a0, 0), ax.c2p(a0, bT.get_value()),
                                             ax.c2p(0, bT.get_value()), stroke_color=C.EPS, stroke_width=3.5,
                                             fill_opacity=0))
        a_l = MathTex(r"a", font_size=30, color=C.MEASURE).next_to(ax.c2p(a0, 0), DOWN, buff=0.35)
        b_l = always_redraw(lambda: MathTex(r"b", font_size=30, color=C.SEQ).next_to(ax.c2p(0, bT.get_value()), LEFT,
                                                                                   buff=0.75))  # clear of the ticks

        shown = ValueTracker(1)

        def reads():
            b = bT.get_value()
            A, B = a0**p / p, b**q / q
            rows = VGroup(
                MathTex(rf"\text{{orange}} = \int_0^a x^{{p-1}}dx = \frac{{a^p}}{{p}} = {A:.3f}", font_size=28,
                        color=C.MEASURE),
                MathTex(rf"\text{{blue}} = \int_0^b y^{{q-1}}dy = \frac{{b^q}}{{q}} = {B:.3f}", font_size=28,
                        color=C.SEQ),
                MathTex(rf"\text{{rectangle}} = ab = {a0 * b:.3f}", font_size=28, color=C.EPS),
                MathTex(rf"\text{{leftover}} = {A + B - a0 * b:.3f} \ge 0", font_size=28, color=C.PATHOLOGY),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([3.3, 0.25, 0])
            return VGroup(*rows[:int(shown.get_value())])

        rd = always_redraw(reads)
        for b in np.linspace(0.2, 1.65, 30):
            assert a0 * b <= a0**p / p + b**q / q + 1e-12
        assert abs(a0 ** (p - 1) - 1.44) < 1e-12 and abs(a0 * 1.44 - (a0**p / p + 1.44**q / q)) < 1e-12
        head = VGroup(label(r"Young's inequality \ ($p = 3$, \ $q = \tfrac32$, \ $\tfrac1p + \tfrac1q = 1$)",
                            font_size=30),
                      MathTex(r"ab \le \frac{a^p}{p} + \frac{b^q}{q}", font_size=38, color=C.EPS)
                      ).arrange(RIGHT, buff=0.5).to_edge(UP, buff=0.3)
        foot = VGroup(label(r"the two areas always cover the rectangle; \ equality exactly when $b = a^{p-1}$",
                            font_size=24, color=GREY_A),
                      label(r"(the inverse of $y = x^{p-1}$ is $x = y^{q-1}$: \ that is what $\tfrac1p + \tfrac1q = 1$ means)",
                            font_size=22, color=GREY_B)).arrange(DOWN, buff=0.08).to_edge(DOWN, buff=0.2)
        with self.voiceover(
            "<bookmark mark='a'/> Pick conjugate exponents, p and q, with one over p plus one over q equal to one: "
            "here three and three halves. Young's inequality says a b is at most a to the p over p, plus b to the q "
            "over q. <bookmark mark='b'/> The proof is a picture. Draw y equals x to the p minus one. The orange area "
            "under it, up to a, is a to the p over p. <bookmark mark='c'/> The blue area to its left, up to height b, "
            "is b to the q over q, because the inverse function is y to the q minus one. "
            "<bookmark mark='d'/> Together the two areas cover the rectangle a by b, with something left over. "
            "<bookmark mark='e'/> Move b. The leftover shrinks to zero exactly when the corner of the rectangle sits "
            "on the curve, and then grows again on the other side. It never goes negative."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), Create(ax), Create(curve), FadeIn(c_l))
            vo.wait_until("b")
            self.play(Indicate(curve, color=C.EPS))
            self.play(FadeIn(A1), FadeIn(a_l), FadeIn(rd))
            vo.wait_until("c")
            shown.set_value(2)
            self.play(FadeIn(A2), FadeIn(b_l))
            vo.wait_until("d")
            shown.set_value(4)
            self.play(Create(rect))
            vo.wait_until("e")
            self.play(bT.animate.set_value(1.44), run_time=2.5)
            self.wait(0.4)
            self.play(bT.animate.set_value(1.65), run_time=1.5)
            self.play(bT.animate.set_value(1.44), run_time=1.2)
            self.play(FadeIn(foot))
        for m in (A2, rect, b_l, rd):
            m.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def holder(self):
        d = load("holder")
        x, F, G, U, L = d["x"], d["F"], d["G"], d["U"], d["L"]
        iL, iU, lhs, rhs = float(d["iL"]), float(d["iU"]), float(d["lhs"]), float(d["rhs"])
        ax = plain_axes([0, 1, 0.25], [0, 2.2, 0.5], 5.6, 3.6, numbers=True, font_size=18,
                        x_axis_config={"decimal_number_config": {"num_decimal_places": 2}},
                        y_axis_config={"decimal_number_config": {"num_decimal_places": 1}}).move_to([-3.3, -1.0, 0])
        gU = polyline(ax, x, U, color=C.EPS, stroke_width=3.5)
        gL = polyline(ax, x, L, color=C.INNER, stroke_width=3.5)
        aL = area_under(ax, x, L, C.INNER, 0.4)
        aU = area_under(ax, x, U, C.EPS, 0.12)
        lU = MathTex(r"\frac{|F|^p}{p} + \frac{|G|^q}{q}", font_size=26, color=C.EPS).next_to(
            ax.c2p(0.62, float(np.interp(0.62, x, U))), UP, buff=0.12)
        lL = MathTex(r"|FG|", font_size=26, color=C.INNER).move_to(ax.c2p(0.62, 0.25))
        rU = MathTex(rf"\int = \tfrac1p + \tfrac1q = {iU:.4f}", font_size=26, color=C.EPS)
        rL = MathTex(rf"\int |FG| = {iL:.4f} \le 1", font_size=26, color=C.INNER)
        VGroup(rU, rL).arrange(DOWN, aligned_edge=LEFT, buff=0.1).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)
        steps = VGroup(
            label(r"1. \ scale: \ $F = f / \|f\|_p$, \ $G = g / \|g\|_q$", font_size=26),
            label(r"so $\int |F|^p = \int |G|^q = 1$", font_size=22, color=GREY_B),
            label(r"2. \ Young at every point:", font_size=26),
            MathTex(r"|F(x) G(x)| \le \frac{|F(x)|^p}{p} + \frac{|G(x)|^q}{q}", font_size=30),
            label(r"3. \ integrate: \ $\int |FG| \le \tfrac1p + \tfrac1q = 1$", font_size=26),
            label(r"multiply back by $\|f\|_p \|g\|_q$", font_size=22, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([3.4, -0.75, 0])
        for i in (1, 5):
            steps[i].shift(RIGHT * 0.35)
        ex = MathTex(rf"f = x,\ g = \cos\tfrac{{\pi x}}{{2}} + 0.15: \quad \int_0^1 |fg| = {lhs:.4f} \le "
                     rf"\|f\|_3 \|g\|_{{3/2}} = {rhs:.4f}", font_size=26, color=GREY_A).to_edge(DOWN, buff=0.18)
        assert np.all(L <= U + 1e-12) and abs(lhs / rhs - iL) < 1e-9
        head = VGroup(VGroup(label(r"\textbf{RCA 3.5} \ (H\"older, 1889) \ \ $\frac1p + \frac1q = 1$, \ $1 < p < \infty$:",
                                   font_size=28),
                             MathTex(r"\int |fg|\,d\mu \le \|f\|_p\, \|g\|_q", font_size=38, color=C.EPS)
                             ).arrange(RIGHT, buff=0.45),
                      label(r"$p = q = 2$: \ Cauchy--Schwarz", font_size=24, color=C.INNER)
                      ).arrange(DOWN, buff=0.08).to_edge(UP, buff=0.25)
        if head.width > 13:
            head.width = 13
        gF = polyline(ax, x, F, color=C.FUNC, stroke_width=3)
        gG = polyline(ax, x, G, color=C.SPECTRUM, stroke_width=3)
        lFG = VGroup(MathTex(r"F", font_size=26, color=C.FUNC), MathTex(r"G", font_size=26, color=C.SPECTRUM)).arrange(
            RIGHT, buff=0.4).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)
        with self.voiceover(
            "<bookmark mark='a'/> Hölder's inequality: the integral of f times g is at most the p-norm of f times "
            "the q-norm of g. With p equal to two, it's the Cauchy-Schwarz inequality. <bookmark mark='b'/> The "
            "proof is Young's inequality, applied at every point. First scale both functions so their norms are "
            "one. <bookmark mark='c'/> Then at each x, the product F G sits below the yellow curve, Young's right "
            "hand side. <bookmark mark='d'/> Integrate. The yellow curve has integral exactly one over p plus one "
            "over q, which is one, so the purple area is at most one: here 0.594. <bookmark mark='e'/> Scale back, "
            "and that's Hölder."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), Create(ax))
            vo.wait_until("b")
            self.play(FadeIn(steps[:2]), Create(gF), Create(gG), FadeIn(lFG))
            vo.wait_until("c")
            self.play(FadeIn(steps[2:4]))
            self.play(FadeOut(gF), FadeOut(gG), FadeOut(lFG), Create(gL), FadeIn(lL), Create(gU), FadeIn(lU), run_time=1.8)
            vo.wait_until("d")
            self.play(FadeIn(aU), FadeIn(rU))
            self.play(FadeIn(aL), FadeIn(rL), FadeIn(steps[4]))
            vo.wait_until("e")
            self.play(FadeIn(steps[5]), FadeIn(ex))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def minkowski(self):
        ax = square_axes([-1.25, 1.25, 1], [-1.25, 1.25, 1], 1.6).move_to([-3.6, -0.45, 0])
        bx = square_axes([-1.25, 1.25, 1], [-1.25, 1.25, 1], 1.6).move_to([1.6, -0.45, 0])
        b3 = p_ball(ax, 3.0, C.DIST)
        b05 = p_ball(bx, 0.5, C.PATHOLOGY)
        u = np.array([1.0, 0.35]) / pnorm([1.0, 0.35], 3)
        v = np.array([-0.3, 1.0]) / pnorm([-0.3, 1.0], 3)
        m = (u + v) / 2
        assert abs(pnorm(u, 3) - 1) < 1e-12 and pnorm(m, 3) < 1
        dots3 = VGroup(Dot(ax.c2p(*u), radius=0.07, color=WHITE), Dot(ax.c2p(*v), radius=0.07, color=WHITE))
        seg3 = DashedLine(ax.c2p(*u), ax.c2p(*v), color=WHITE, stroke_width=2)
        mid3 = Dot(ax.c2p(*m), radius=0.08, color=C.EPS)
        l3 = VGroup(MathTex(r"p = 3", font_size=30, color=C.DIST),
                    MathTex(rf"\|\tfrac{{u + v}}{{2}}\|_3 = {pnorm(m, 3):.3f} \le 1", font_size=28, color=C.EPS)
                    ).arrange(DOWN, buff=0.1).next_to(ax, DOWN, buff=0.15)
        u2, v2 = np.array([1.0, 0.0]), np.array([0.0, 1.0])
        m2 = (u2 + v2) / 2
        n05 = (np.sqrt(m2[0]) + np.sqrt(m2[1])) ** 2
        assert abs(n05 - 2.0) < 1e-12
        dots05 = VGroup(Dot(bx.c2p(*u2), radius=0.07, color=WHITE), Dot(bx.c2p(*v2), radius=0.07, color=WHITE))
        seg05 = DashedLine(bx.c2p(*u2), bx.c2p(*v2), color=WHITE, stroke_width=2)
        mid05 = Dot(bx.c2p(*m2), radius=0.08, color=C.PATHOLOGY)
        l05 = VGroup(MathTex(r"p = \tfrac12", font_size=30, color=C.PATHOLOGY),
                     MathTex(rf"\|\tfrac{{u + v}}{{2}}\|_{{1/2}} = ({{\textstyle\sqrt{{\tfrac12}} + \sqrt{{\tfrac12}}}})^2 = "
                             rf"{n05:.0f}", font_size=28, color=C.PATHOLOGY)).arrange(DOWN, buff=0.1).next_to(
            bx, DOWN, buff=0.15)
        card = museum_card(r"$p < 1$", r"the ball is not convex", r"the triangle inequality", width=3.0,
                           font_size=20).move_to([5.45, -0.6, 0])
        thm = VGroup(label(r"\textbf{RCA 3.5} \ (Minkowski) \ for $1 \le p \le \infty$:", font_size=28),
                     MathTex(r"\|f + g\|_p \le \|f\|_p + \|g\|_p", font_size=36, color=C.EPS)
                     ).arrange(RIGHT, buff=0.45).to_edge(UP, buff=0.3)
        idea = VGroup(label(r"$\displaystyle \frac{f + g}{\|f\| + \|g\|} = t\,\frac{f}{\|f\|} + (1 - t)\,\frac{g}{\|g\|}$, "
                            r"\ $t = \frac{\|f\|}{\|f\| + \|g\|}$", font_size=24),
                      label(r"triangle inequality $\iff$ the unit ball is convex", font_size=24, color=C.EPS)
                      ).arrange(DOWN, buff=0.1).next_to(thm, DOWN, buff=0.2)
        with self.voiceover(
            "<bookmark mark='a'/> The third inequality makes the p-norm a distance: Minkowski's triangle "
            "inequality. Rudin derives it from Hölder in two lines, but here's what it means. "
            "<bookmark mark='b'/> Take two vectors on the unit sphere for p equal to three. The point halfway "
            "between them lies inside the ball. <bookmark mark='c'/> That's convexity of the ball, and it's the "
            "triangle inequality in disguise: f plus g, divided by the sum of the norms, is an average of two unit "
            "vectors, so it lies in the ball. <bookmark mark='d'/> For p below one, the formula still makes sense, "
            "but the ball caves in. The midpoint of these two unit vectors has size two, and the triangle "
            "inequality fails. That's why p runs from one to infinity."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(thm), Create(ax), FadeIn(b3))
            vo.wait_until("b")
            self.play(FadeIn(dots3), Create(seg3), FadeIn(mid3), FadeIn(l3))
            vo.wait_until("c")
            self.play(FadeIn(idea))
            vo.wait_until("d")
            self.play(Create(bx), FadeIn(b05))
            self.play(FadeIn(dots05), Create(seg05), FadeIn(mid05), FadeIn(l05))
            self.play(FadeIn(card))
        self.wait(0.4)
        self.clear_scene()
