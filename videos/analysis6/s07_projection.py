from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis6.common import load, p_ball, plain_axes, polyline, square_axes


def ellipse(th, c=(1.3, 0.7), a=1.15, b=0.62, rot=math.radians(25)):
    th = np.asarray(th, float)
    u, v = a * np.cos(th), b * np.sin(th)
    return np.stack([c[0] + u * math.cos(rot) - v * math.sin(rot), c[1] + u * math.sin(rot) + v * math.cos(rot)], -1)


class Projection(VoiceoverScene):
    def construct(self):
        self.card()
        self.nearest()
        self.unique()
        self.subspace()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(6, r"The nearest point", r"Which point of a closed convex set is closest?", lit=(), part=6)
        with self.voiceover("Chapter six: nearest points, the first theorem that needs both the angle and the "
                            "completeness."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def nearest(self):
        ax = square_axes([-1.6, 2.8, 1], [-1.3, 1.9, 1], 1.4).move_to([-3.6, -0.75, 0])
        ax.set_opacity(0.3)
        x = np.array([-1.1, -0.9])
        th = np.linspace(0, 2 * np.pi, 20001)
        P = ellipse(th)
        dist = np.linalg.norm(P - x, axis=1)
        i0 = int(np.argmin(dist))
        th0, delta = th[i0], float(dist[i0])
        y0 = P[i0]
        E = Polygon(*[ax.c2p(*p) for p in ellipse(np.linspace(0, 2 * np.pi, 400))], stroke_color=C.CONNECTED_SET,
                    stroke_width=3, fill_color=C.CONNECTED_SET, fill_opacity=0.2)
        E_l = MathTex(r"E", font_size=34, color=C.CONNECTED_SET).move_to(ax.c2p(1.5, 0.75))
        xd = Dot(ax.c2p(*x), radius=0.08, color=WHITE)
        x_l = MathTex(r"x", font_size=32).next_to(xd, DL, buff=0.08)
        circ = Circle(radius=delta * 1.4, color=C.DIST, stroke_width=2).move_to(ax.c2p(*x))
        y_d = Dot(ax.c2p(*y0), radius=0.09, color=C.EPS)
        y_l = MathTex(r"y_0", font_size=30, color=C.EPS).next_to(y_d, DOWN, buff=0.12).shift(RIGHT * 0.15)
        seg = Line(ax.c2p(*x), ax.c2p(*y0), color=C.DIST, stroke_width=3)
        # a minimizing sequence on the boundary, from alternating sides
        ths = np.array([th0 + (-1) ** n * 1.4 * 0.62**n for n in range(8)])
        Y = ellipse(ths)
        dn = np.linalg.norm(Y - x, axis=1)
        assert np.all(dn >= delta - 1e-9) and np.all(np.diff(dn[1:]) < 0)
        seq = VGroup(*[Dot(ax.c2p(*p), radius=0.06, color=C.SEQ) for p in Y])
        seq_l = VGroup(*[MathTex(rf"y_{{{n + 1}}}", font_size=22, color=C.SEQ).next_to(seq[n], UL if n % 2 == 0 else DR,
                                                                                    buff=0.04) for n in range(3)])
        # parallelogram law bound for consecutive pairs (the midpoint is in E, so its distance is at least delta)
        rows = []
        for n in range(1, 6):
            a, b = Y[n], Y[n + 1]
            lhs = float(np.sum((a - b) ** 2))
            bound = 2 * dn[n] ** 2 + 2 * dn[n + 1] ** 2 - 4 * delta**2
            mid = (a + b) / 2
            assert np.linalg.norm(mid - x) >= delta - 1e-9 and lhs <= bound + 1e-12
            rows.append((n, lhs, bound))
        mid = (Y[1] + Y[2]) / 2
        mid_d = Dot(ax.c2p(*mid), radius=0.07, color=C.MEASURE)
        mid_seg = DashedLine(ax.c2p(*Y[1]), ax.c2p(*Y[2]), color=C.MEASURE, stroke_width=2)
        formula = VGroup(
            MathTex(r"\|y_n - y_m\|^2 = 2\|x - y_n\|^2 + 2\|x - y_m\|^2 - 4\Big\|x - \tfrac{y_n + y_m}{2}\Big\|^2",
                    font_size=26),
            label(r"the midpoint is in $E$ (convex), \ so the last term is at least $4\delta^2$:", font_size=22,
                  color=GREY_B),
            MathTex(r"\|y_n - y_m\|^2 \le 2\|x - y_n\|^2 + 2\|x - y_m\|^2 - 4\delta^2 \to 0", font_size=26, color=C.EPS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([3.3, 1.0, 0])
        for r_ in formula:
            if r_.width > 6.6:
                r_.width = 6.6
        tab = VGroup(MathTex(r"n", r"\quad \|y_n - y_{n+1}\|^2", r"\quad \text{bound}", font_size=24, color=GREY_A))
        for n, lhs, bound in rows:
            tab.add(MathTex(f"{n}", rf"\quad {sci(lhs, 2)}", rf"\quad {sci(bound, 2)}", font_size=24))
        tab.arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to([3.0, -1.55, 0])
        for row in tab[1:]:
            row[1].align_to(tab[0][1], LEFT)
            row[2].align_to(tab[0][2], LEFT)
        concl = label(r"Cauchy, \ so it converges \ (completeness), \ and the limit is in $E$ \ (closed)", font_size=24,
                      color=C.EPS).to_edge(DOWN, buff=0.2)
        head = VGroup(label(r"\textbf{RCA 4.10} \ a nonempty closed convex set $E$ in a Hilbert space", font_size=28),
                      label(r"has exactly one point nearest to $x$", font_size=28)).arrange(DOWN, buff=0.08).to_edge(
            UP, buff=0.2)
        d_l = MathTex(rf"\delta = \inf_{{y \in E}} \|x - y\| = {delta:.4f}", font_size=26, color=C.DIST).next_to(
            ax, DOWN, buff=0.1)
        with self.voiceover(
            "<bookmark mark='a'/> The projection theorem. A closed convex set in a Hilbert space has exactly one "
            "point nearest to any given x. <bookmark mark='b'/> Let delta be the distance from x to the set. By "
            "definition there's a sequence of points in the set whose distances to x approach delta. "
            "<bookmark mark='c'/> Here's the key: the parallelogram law, applied to x minus y n and x minus y m. "
            "The midpoint of y n and y m lies in the set, because the set is convex, so it's at least delta from x. "
            "<bookmark mark='d'/> That squeezes the distance between y n and y m to zero: the minimizing sequence is "
            "Cauchy. The table shows each gap under its bound. <bookmark mark='e'/> Completeness gives a limit, and "
            "since the set is closed, the limit is in it. It's the nearest point, and the same inequality shows "
            "there's only one."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), Create(ax), FadeIn(E), FadeIn(E_l), FadeIn(xd), FadeIn(x_l))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(s_, scale=1.5) for s_ in seq], lag_ratio=0.3), FadeIn(seq_l), run_time=2.5)
            self.play(Create(circ), FadeIn(d_l))
            vo.wait_until("c")
            self.play(Create(mid_seg), FadeIn(mid_d), FadeIn(formula[0]))
            self.play(FadeIn(formula[1]))
            vo.wait_until("d")
            self.play(FadeIn(formula[2]))
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab], lag_ratio=0.3), run_time=2.0)
            vo.wait_until("e")
            self.play(FadeIn(y_d), Create(seg), FadeIn(y_l), FadeIn(concl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def unique(self):
        ax = square_axes([-0.6, 2.0, 1], [-0.6, 2.0, 1], 1.9).move_to([-3.5, -0.7, 0])
        bx = square_axes([-0.6, 2.0, 1], [-0.6, 2.0, 1], 1.9).move_to([3.0, -0.7, 0])
        for a in (ax, bx):
            a.set_opacity(0.35)
        rT = ValueTracker(0.2)
        lineA = Line(ax.c2p(-0.4, 1.9), ax.c2p(1.9, -0.4), color=C.CONNECTED_SET, stroke_width=4)
        lineB = Line(bx.c2p(-0.4, 1.9), bx.c2p(1.9, -0.4), color=C.CONNECTED_SET, stroke_width=4)
        circ = always_redraw(lambda: p_ball(ax, 2.0, C.DIST, r=min(rT.get_value(), 1.5 / math.sqrt(2)), fill=0.12))
        diam = always_redraw(lambda: p_ball(bx, 1.0, C.DIST, r=min(rT.get_value(), 1.5), fill=0.12))
        o1, o2 = Dot(ax.c2p(0, 0), radius=0.07), Dot(bx.c2p(0, 0), radius=0.07)
        touch1 = Dot(ax.c2p(0.75, 0.75), radius=0.09, color=C.EPS)
        touch2 = Line(bx.c2p(1.5, 0), bx.c2p(0, 1.5), color=C.EPS, stroke_width=8)
        l1 = VGroup(MathTex(r"\|\cdot\|_2: \text{ one nearest point } (0.75, 0.75)", font_size=26, color=C.EPS),
                    MathTex(rf"\text{{distance }} {1.5 / math.sqrt(2):.4f}", font_size=26, color=C.DIST)
                    ).arrange(DOWN, buff=0.1).next_to(ax, DOWN, buff=0.15)
        l2 = VGroup(MathTex(r"\|\cdot\|_1: \text{ a whole segment of nearest points}", font_size=26, color=C.EPS),
                    MathTex(r"\text{distance } 1.5 \text{ from every point of it}", font_size=26, color=C.DIST)
                    ).arrange(DOWN, buff=0.1).next_to(bx, DOWN, buff=0.15)
        for a_ in np.linspace(0, 1.5, 7):
            assert abs(abs(a_) + abs(1.5 - a_) - 1.5) < 1e-12
        lab = VGroup(MathTex(r"E = \{x + y = 1.5\}", font_size=26, color=C.CONNECTED_SET).next_to(ax.c2p(1.4, 0.3), RIGHT,
                                                                                                   buff=0.05),
                     MathTex(r"E", font_size=26, color=C.CONNECTED_SET).next_to(bx.c2p(1.6, -0.1), RIGHT, buff=0.1))
        head = VGroup(label(r"Why the angle matters: \ grow a ball around $0$ until it touches $E$", font_size=30),
                      label(r"round balls touch once; \ the $L^1$ ball can touch along an edge", font_size=24,
                            color=GREY_A)).arrange(DOWN, buff=0.1).to_edge(UP, buff=0.25)
        with self.voiceover(
            "<bookmark mark='a'/> Uniqueness is where the inner product earns its keep. Grow a ball around the "
            "origin until it first touches a line. <bookmark mark='b'/> The round ball touches at one point. "
            "<bookmark mark='c'/> The diamond of the one-norm can arrive flat against the line, and then every "
            "point of a whole segment is nearest. The parallelogram law is what rules this out: it makes the ball "
            "strictly round."
        ) as vo:
            self.play(FadeIn(head), Create(ax), Create(bx), Create(lineA), Create(lineB), FadeIn(lab), FadeIn(o1),
                      FadeIn(o2))
            vo.wait_until("a")
            self.play(FadeIn(circ), FadeIn(diam))
            vo.wait_until("b")
            self.play(rT.animate.set_value(1.5 / math.sqrt(2)), run_time=2.5)
            self.play(FadeIn(touch1, scale=2), FadeIn(l1))
            vo.wait_until("c")
            self.play(rT.animate.set_value(1.5), run_time=2.0)
            self.play(Create(touch2), FadeIn(l2))
        for m in (circ, diam):
            m.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def subspace(self):
        d = load("projection")
        c, err, terr, xs, fx, px, tx, ip = d["c"], float(d["err"]), float(d["terr"]), d["xs"], d["fx"], d["px"], d["tx"], d["ip"]
        ax = plain_axes([0, 1, 0.25], [0.9, 2.8, 0.5], 5.0, 2.7, numbers=True, font_size=16,
                        x_axis_config={"decimal_number_config": {"num_decimal_places": 2}},
                        y_axis_config={"decimal_number_config": {"num_decimal_places": 1}}).move_to([-3.7, 0.35, 0])
        gf = polyline(ax, xs, fx, color=C.FUNC, stroke_width=5)
        gp = polyline(ax, xs, px, color=C.EPS, stroke_width=3)
        gt = DashedVMobject(polyline(ax, xs, tx, color=C.APPROX, stroke_width=3), num_dashes=40)
        lf = MathTex(r"e^x", font_size=28, color=C.FUNC).next_to(ax.c2p(0.95, math.exp(0.95)), UL, buff=0.08)
        lt = MathTex(r"1 + x + \tfrac{x^2}{2}", font_size=24, color=C.APPROX).next_to(ax.c2p(1, 2.5), DOWN, buff=0.3)
        bx = plain_axes([0, 1, 0.25], [-0.016, 0.016, 0.008], 5.0, 1.6).move_to([-3.7, -2.35, 0])
        r = fx - px
        gr = polyline(bx, xs, r, color=C.EPS, stroke_width=3)
        zero = DashedLine(bx.c2p(0, 0), bx.c2p(1, 0), color=GREY_C, stroke_width=1.5)
        r_l = MathTex(r"e^x - Pe^x \ \ (\pm 0.016)", font_size=22, color=C.EPS).next_to(bx, UP, buff=0.05).align_to(bx, LEFT)
        sign_changes = int(np.sum(np.diff(np.sign(r)) != 0))
        assert sign_changes >= 3 and np.abs(r).max() < 0.016
        right = VGroup(
            label(r"$M = \mathrm{span}\{1, x, x^2\}$ in $L^2[0, 1]$: \ nearest point $Pe^x = c_0 + c_1 x + c_2 x^2$",
                  font_size=24),
            MathTex(r"\begin{pmatrix} 1 & \tfrac12 & \tfrac13 \\ \tfrac12 & \tfrac13 & \tfrac14 \\ \tfrac13 & \tfrac14 & "
                    r"\tfrac15 \end{pmatrix} \begin{pmatrix} c_0 \\ c_1 \\ c_2 \end{pmatrix} = "
                    r"\begin{pmatrix} \langle e^x, 1\rangle \\ \langle e^x, x\rangle \\ \langle e^x, x^2\rangle "
                    r"\end{pmatrix}", font_size=26),
            MathTex(rf"c = ({c[0]:.4f},\ {c[1]:.4f},\ {c[2]:.4f})", font_size=28, color=C.EPS),
            MathTex(r"|\langle e^x - Pe^x,\ x^k\rangle| < 10^{-15} \quad (k = 0, 1, 2)", font_size=24, color=GREY_A),
            MathTex(rf"\|e^x - Pe^x\|_2 = {err:.5f}", font_size=28, color=C.EPS),
            MathTex(rf"\|e^x - (1 + x + \tfrac{{x^2}}{{2}})\|_2 = {terr:.5f}", font_size=28, color=C.APPROX),
            label(r"\textbf{RCA 4.11} \ $H = M \oplus M^\perp$: \ $x = Px + (x - Px)$, \ uniquely", font_size=24,
                  color=C.INNER),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to([3.3, -0.35, 0])
        for r_ in right:
            if r_.width > 6.5:
                r_.width = 6.5
        right.arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to([3.3, -0.4, 0])
        assert np.all(np.abs(ip) < 1e-15) and terr > 10 * err
        head = label(r"Projection onto a subspace: \ the error is perpendicular to it", font_size=32).to_edge(UP,
                                                                                                           buff=0.25)
        with self.voiceover(
            "<bookmark mark='a'/> When the convex set is a closed subspace, the nearest point is the orthogonal "
            "projection, and the error is perpendicular to the whole subspace. <bookmark mark='b'/> Project e to the "
            "x onto the quadratics, in L two of the unit interval. Perpendicular to one, x and x squared gives three "
            "linear equations, and their matrix is the Hilbert matrix of inner products of powers. "
            "<bookmark mark='c'/> The solution is the best quadratic in the mean-square sense, the yellow curve, "
            "almost on top of e to the x. <bookmark mark='d'/> Its error, magnified below, crosses zero three times, "
            "and its inner products with one, x and x squared vanish to rounding. <bookmark mark='e'/> For "
            "comparison, the Taylor quadratic is fifteen times worse in this norm. Taylor fits one point; projection "
            "fits the whole interval. Every vector splits uniquely into a piece in the subspace and a piece "
            "perpendicular to it."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), Create(ax), Create(gf), FadeIn(lf))
            vo.wait_until("b")
            self.play(FadeIn(right[0]))
            self.play(FadeIn(right[1]))
            vo.wait_until("c")
            self.play(FadeIn(right[2]), Create(gp))
            vo.wait_until("d")
            self.play(Create(bx), Create(zero), FadeIn(r_l), Create(gr))
            self.play(FadeIn(right[3]), FadeIn(right[4]))
            vo.wait_until("e")
            self.play(Create(gt), FadeIn(lt), FadeIn(right[5]))
            self.play(FadeIn(right[6]))
        self.wait(0.4)
        self.clear_scene()
