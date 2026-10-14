from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis6.common import area_under, load, p_ball, plain_axes, pnorm, polyline, square_axes, trap


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
        ax = square_axes([0, 1.7, 0.5], [0, 1.7, 0.5], 2.45, numbers=True, font_size=18,
                         x_axis_config={"decimal_number_config": {"num_decimal_places": 1}},
                         y_axis_config={"decimal_number_config": {"num_decimal_places": 1}}).move_to([-3.4, -0.15, 0])
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

        shown = ValueTracker(0)

        def reads():
            # all four rows from the start, in grey with a '?' until their area is drawn
            b = bT.get_value()
            A, B = a0**p / p, b**q / q
            vals = [f"{A:.3f}", f"{B:.3f}", f"{a0 * b:.3f}", rf"{max(A + B - a0 * b, 0.0) + 0.0:.3f} \ge 0"]
            k = int(shown.get_value())
            v = [vals[i] if i < k else "?" for i in range(4)]
            cols = [c_ if i < k else GREY_C for i, c_ in enumerate((C.MEASURE, C.SEQ, C.EPS, C.PATHOLOGY))]
            rows = VGroup(
                MathTex(rf"\text{{orange}} = \int_0^a x^{{p-1}}dx = \frac{{a^p}}{{p}} = {v[0]}", font_size=28, color=cols[0]),
                MathTex(rf"\text{{blue}} = \int_0^b y^{{q-1}}dy = \frac{{b^q}}{{q}} = {v[1]}", font_size=28, color=cols[1]),
                MathTex(rf"\text{{rectangle}} = ab = {v[2]}", font_size=28, color=cols[2]),
                MathTex(rf"\text{{leftover}} = {v[3]}", font_size=28, color=cols[3]),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
            rows.next_to([0.9, 0.25 + rows.height / 2, 0], DR, buff=0)
            return rows

        # the leftover region: above y = b under the curve (b < a^(p-1)), or right of x = a left of it (b > a^(p-1));
        # always 61 points, so the redraw keeps its shape
        n_left = 60

        def leftover_pts(b):
            c0 = a0 ** (p - 1)
            if b <= c0:
                xs_ = np.linspace(b ** (1 / (p - 1)), a0, n_left)
                pts = [(x_, x_ ** (p - 1)) for x_ in xs_] + [(a0, b)]
            else:
                ys_ = np.linspace(c0, b, n_left)
                pts = [(y_ ** (q - 1), y_) for y_ in ys_] + [(a0, b)]
            return np.array(pts)

        def shoelace(P):
            return 0.5 * abs(np.dot(P[:, 0], np.roll(P[:, 1], -1)) - np.dot(P[:, 1], np.roll(P[:, 0], -1)))

        for b_ in (0.6, 1.0, 1.3, 1.55, 1.65):  # the red region's area is the leftover number
            lo_ = a0**p / p + b_**q / q - a0 * b_
            assert abs(shoelace(leftover_pts(b_)) - lo_) < 2e-3 * max(lo_, 0.05)

        left_reg = always_redraw(lambda: Polygon(*[ax.c2p(*pt) for pt in leftover_pts(bT.get_value())], stroke_width=0,
                                                 fill_color=C.PATHOLOGY, fill_opacity=0.6))
        rd = always_redraw(reads)
        for b in np.linspace(0.2, 1.65, 30):
            assert a0 * b <= a0**p / p + b**q / q + 1e-12
        assert abs(a0 ** (p - 1) - 1.44) < 1e-12 and abs(a0 * 1.44 - (a0**p / p + 1.44**q / q)) < 1e-12
        head = label(r"Young's inequality", font_size=34).to_edge(UP, buff=0.3)
        stmt = VGroup(label(r"$p = 3$, \ $q = \tfrac32$, \ $\tfrac1p + \tfrac1q = 1$:", font_size=28),
                      MathTex(r"ab \le \frac{a^p}{p} + \frac{b^q}{q}", font_size=34, color=C.EPS)
                      ).arrange(RIGHT, buff=0.4).next_to(head, DOWN, buff=0.15)
        foot = VGroup(label(r"the two areas always cover the rectangle; \ equality exactly when $b = a^{p-1}$",
                            font_size=24, color=GREY_A),
                      label(r"(the inverse of $y = x^{p-1}$ is $x = y^{q-1}$: \ that is what $\tfrac1p + \tfrac1q = 1$ means)",
                            font_size=22, color=GREY_B)).arrange(DOWN, buff=0.08).to_edge(DOWN, buff=0.35)
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
            self.play(FadeIn(head), FadeIn(stmt), Create(ax), Create(curve), FadeIn(c_l), FadeIn(rd))
            vo.wait_until("b")
            self.play(Indicate(curve, color=C.EPS))
            shown.set_value(1)
            self.play(FadeIn(A1), FadeIn(a_l))
            vo.wait_until("c")
            shown.set_value(2)
            self.play(FadeIn(A2), FadeIn(b_l))
            vo.wait_until("d")
            shown.set_value(4)
            self.play(Create(rect), FadeIn(left_reg))
            vo.wait_until("e")
            self.play(bT.animate.set_value(1.44), run_time=2.5)
            self.wait(0.4)
            self.play(bT.animate.set_value(1.65), run_time=1.5)
            self.play(bT.animate.set_value(1.44), run_time=1.2)
            self.play(FadeIn(foot))
        for m in (A2, rect, b_l, rd, left_reg):
            m.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def holder(self):
        d = load("holder")
        x, F, G, U, L = d["x"], d["F"], d["G"], d["U"], d["L"]
        iL, iU, lhs, rhs = float(d["iL"]), float(d["iU"]), float(d["lhs"]), float(d["rhs"])
        ax = plain_axes([0, 1, 0.25], [0, 2.2, 0.5], 5.6, 3.3, numbers=True, font_size=18,
                        x_axis_config={"decimal_number_config": {"num_decimal_places": 2}},
                        y_axis_config={"decimal_number_config": {"num_decimal_places": 1}}).move_to([-3.3, -0.8, 0])
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
                     rf"\|f\|_3 \|g\|_{{3/2}} = {rhs:.4f}", font_size=26, color=GREY_A).to_edge(DOWN, buff=0.35)
        assert np.all(L <= U + 1e-12) and abs(lhs / rhs - iL) < 1e-9
        head = label(r"H\"older's inequality", font_size=34).to_edge(UP, buff=0.3)
        stmt = VGroup(VGroup(label(r"\textbf{RCA 3.5} \ (H\"older, 1889) \ \ $\frac1p + \frac1q = 1$, \ $1 < p < \infty$:",
                                   font_size=26),
                             MathTex(r"\int |fg|\,d\mu \le \|f\|_p\, \|g\|_q", font_size=32, color=C.EPS)
                             ).arrange(RIGHT, buff=0.4),
                      label(r"$p = q = 2$: \ Cauchy--Schwarz", font_size=24, color=C.INNER)
                      ).arrange(DOWN, buff=0.08).next_to(head, DOWN, buff=0.12)
        # f and g themselves first, then scaled to norm one (the same curves, divided by their norms)
        f_raw = x
        g_raw = np.cos(np.pi * x / 2) + 0.15
        assert np.allclose(F * trap(np.abs(f_raw) ** float(d["p"]), x) ** (1 / float(d["p"])), f_raw, atol=1e-3)
        assert np.allclose(G * trap(np.abs(g_raw) ** float(d["q"]), x) ** (1 / float(d["q"])), g_raw, atol=1e-3)
        gf = polyline(ax, x, f_raw, color=C.FUNC, stroke_width=3)
        gg = polyline(ax, x, g_raw, color=C.APPROX, stroke_width=3)
        lfg = VGroup(MathTex(r"f = x", font_size=26, color=C.FUNC).next_to(ax.c2p(1, 1), RIGHT, buff=0.1),
                     MathTex(r"g", font_size=26, color=C.APPROX).next_to(ax.c2p(1, float(g_raw[-1])), RIGHT, buff=0.1))
        gF = polyline(ax, x, F, color=C.FUNC, stroke_width=3)
        gG = polyline(ax, x, G, color=C.APPROX, stroke_width=3)
        lFG = VGroup(MathTex(r"F", font_size=26, color=C.FUNC).next_to(ax.c2p(1, float(F[-1])), RIGHT, buff=0.1),
                     MathTex(r"G", font_size=26, color=C.APPROX).next_to(ax.c2p(1, float(G[-1])), RIGHT, buff=0.1))
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
            self.play(FadeIn(head), FadeIn(stmt), Create(ax), Create(gf), Create(gg), FadeIn(lfg))
            vo.wait_until("b")
            self.play(FadeIn(steps[:2]), ReplacementTransform(gf, gF), ReplacementTransform(gg, gG),
                      FadeTransform(lfg, lFG))
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
        ax = square_axes([-1.25, 1.25, 1], [-1.25, 1.25, 1], 1.4).move_to([-3.8, -0.55, 0])
        bx = square_axes([-1.25, 1.25, 1], [-1.25, 1.25, 1], 1.4).move_to([1.0, -0.55, 0])
        b3 = p_ball(ax, 3.0, C.DIST)
        b05 = p_ball(bx, 0.5, C.PATHOLOGY)
        u = np.array([1.0, 0.35]) / pnorm([1.0, 0.35], 3)
        v = np.array([-0.3, 1.0]) / pnorm([-0.3, 1.0], 3)
        m = (u + v) / 2
        assert abs(pnorm(u, 3) - 1) < 1e-12 and pnorm(m, 3) < 1
        dots3 = VGroup(Dot(ax.c2p(*u), radius=0.07, color=WHITE), Dot(ax.c2p(*v), radius=0.07, color=WHITE))
        seg3 = DashedLine(ax.c2p(*u), ax.c2p(*v), color=WHITE, stroke_width=2)
        mid3 = Dot(ax.c2p(*m), radius=0.08, color=C.EPS)
        uv3 = VGroup(MathTex("u", font_size=28).next_to(dots3[0], RIGHT, buff=0.1),
                     MathTex("v", font_size=28).next_to(dots3[1], UP, buff=0.1))
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
        uv05 = VGroup(MathTex("u", font_size=28).next_to(dots05[0], DR, buff=0.05),
                      MathTex("v", font_size=28).next_to(dots05[1], LEFT, buff=0.15))
        l05 = VGroup(MathTex(r"p = \tfrac12", font_size=30, color=C.PATHOLOGY),
                     MathTex(rf"\|\tfrac{{u + v}}{{2}}\|_{{1/2}} = ({{\textstyle\sqrt{{\tfrac12}} + \sqrt{{\tfrac12}}}})^2 = "
                             rf"{n05:.0f}", font_size=28, color=C.PATHOLOGY)).arrange(DOWN, buff=0.1).next_to(
            bx, DOWN, buff=0.15)
        card = museum_card(r"$p < 1$", r"the ball is not convex", r"the triangle inequality", width=2.8,
                           font_size=22)
        card.move_to([6.6 - card.width / 2, -0.75, 0])
        assert card.get_left()[0] > bx.get_right()[0] + 0.3
        head = label(r"Minkowski's inequality: \ the triangle inequality for $\|\cdot\|_p$", font_size=34).to_edge(
            UP, buff=0.3)
        thm = VGroup(label(r"\textbf{RCA 3.5} \ (Minkowski) \ for $1 \le p \le \infty$:", font_size=26),
                     MathTex(r"\|f + g\|_p \le \|f\|_p + \|g\|_p", font_size=32, color=C.EPS)
                     ).arrange(RIGHT, buff=0.4).next_to(head, DOWN, buff=0.15)
        idea = VGroup(label(r"$\displaystyle \frac{f + g}{\|f\| + \|g\|} = t\,\frac{f}{\|f\|} + (1 - t)\,\frac{g}{\|g\|}$, "
                            r"\ $t = \frac{\|f\|}{\|f\| + \|g\|}$", font_size=24),
                      label(r"triangle inequality $\iff$ the unit ball is convex", font_size=24, color=C.EPS)
                      ).arrange(DOWN, buff=0.1).next_to(thm, DOWN, buff=0.15)
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
            self.play(FadeIn(head), FadeIn(thm), Create(ax), FadeIn(b3))
            vo.wait_until("b")
            self.play(FadeIn(dots3), FadeIn(uv3), Create(seg3), FadeIn(mid3), FadeIn(l3))
            vo.wait_until("c")
            self.play(FadeIn(idea))
            vo.wait_until("d")
            self.play(Create(bx), FadeIn(b05))
            self.play(FadeIn(dots05), FadeIn(uv05), Create(seg05), FadeIn(mid05), FadeIn(l05))
            self.play(FadeIn(card))
        self.wait(0.4)
        self.clear_scene()
