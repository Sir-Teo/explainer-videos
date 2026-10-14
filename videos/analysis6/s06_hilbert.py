from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis6.common import (between, dict_table, load, plain_axes, pnorm, polyline, right_angle,
                                     square_axes, trap)


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
        head = label(r"Inner products, \ and the Cauchy--Schwarz inequality", font_size=34).to_edge(UP, buff=0.3)
        axs = VGroup(
            label(r"\textbf{RCA 4.1} \ an inner product: \ $\langle x, y\rangle = \overline{\langle y, x\rangle}$, "
                  r"\ linear in $x$, \ $\langle x, x\rangle > 0$ for $x \ne 0$", font_size=26),
            MathTex(r"L^2(\mu):\ \langle f, g\rangle = \int f\,\bar g\,d\mu, \qquad \|f\| = \sqrt{\langle f, f\rangle}",
                    font_size=30, color=C.INNER),
        ).arrange(DOWN, buff=0.12).next_to(head, DOWN, buff=0.15)
        ax = plain_axes([0, 1, 0.5], [0, 5.6, 1], 3.6, 3.0, numbers=True, font_size=18,  # lambda t sweeps to 5.5
                        x_axis_config={"decimal_number_config": {"num_decimal_places": 1}},
                        y_axis_config={"decimal_number_config": {"num_decimal_places": 0}}).move_to([-4.6, -1.2, 0])
        ax_home = ax.get_center().copy()
        ax.scale(1.35).move_to([-1.0, -1.0, 0])  # alone at first: bigger, centred; it slides left at 'b'
        gx = polyline(ax, t[::500], X[::500], color=C.FUNC, stroke_width=4)
        lT = ValueTracker(0.5)
        gy = always_redraw(lambda: polyline(ax, t[::500], lT.get_value() * Y[::500], color=C.APPROX, stroke_width=3.5))
        gap = always_redraw(lambda: between(ax, t[::500], X[::500], lT.get_value() * Y[::500], C.INNER, 0.3))
        xl = MathTex(r"x = e^t", font_size=26, color=C.FUNC).next_to(ax.c2p(0.2, 1.4), UP, buff=0.05)
        stat = VGroup(ax, gx, xl)  # the static part; the redrawn curves follow ax
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
                      MathTex(rf"\min = {qmin:.4f} \ge 0", font_size=24, color=C.EPS).move_to(qx.c2p(lam_star, 1.6)))
        # inside the U: q = 1.6 at lambda = 3 +- 2.05, wider than the label
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
            if r_.width > 3.75:
                r_.width = 3.75
        side.arrange(DOWN, aligned_edge=LEFT, buff=0.14).next_to([3.05, -1.1, 0], RIGHT, buff=0)
        # the angle itself: two unit arrows 14.3 degrees apart, under the readouts
        o_ = np.array([3.6, side.get_bottom()[1] - 0.45, 0])
        th_r = math.radians(theta)
        ang_pic = VGroup(Arrow(o_, o_ + 1.1 * RIGHT, buff=0, color=C.FUNC, stroke_width=4, tip_length=0.15),
                         Arrow(o_, o_ + 1.1 * np.array([math.cos(th_r), math.sin(th_r), 0]), buff=0, color=C.APPROX,
                               stroke_width=4, tip_length=0.15),
                         Arc(radius=0.75, start_angle=0, angle=th_r, arc_center=o_, color=C.INNER, stroke_width=3),
                         MathTex(rf"{theta:.1f}^\circ", font_size=24, color=C.INNER).next_to(o_ + 0.8 * RIGHT, RIGHT,
                                                                                         buff=0.5).shift(UP * 0.1))
        assert abs(theta - 14.3) < 0.05 and ang_pic.get_bottom()[1] > -3.6
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
            self.play(FadeIn(head), FadeIn(axs[0]), Create(ax), Create(gx), FadeIn(xl), FadeIn(gy), FadeIn(yl))
            self.play(FadeIn(axs[1]))
            vo.wait_until("b")
            self.play(stat.animate.scale(1 / 1.35).move_to(ax_home + (stat.get_center() - ax.get_center()) / 1.35),
                      FadeIn(gap))
            self.play(Create(qx), FadeIn(q_l), FadeIn(lam_l), Create(par), FadeIn(qdot), FadeIn(side[:2]))
            vo.wait_until("c")
            self.play(lT.animate.set_value(5.5), run_time=2.5)
            self.play(lT.animate.set_value(lam_star), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(vert), FadeIn(side[2:4]))
            self.play(FadeIn(side[4]))
            vo.wait_until("e")
            self.play(FadeIn(side[5]), FadeIn(ang_pic))
        for m in (gy, gap, yl, qdot):
            m.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def parallelogram(self):
        d = load("parallel")
        res = d["res"]
        ax = square_axes([-0.6, 2.6, 1], [-0.4, 2.0, 1], 1.35).move_to([-3.7, 0.2, 0])
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

            def at(P, Q, t, off):  # a point t of the way from P to Q, pushed off the segment to its left
                d_ = (Q - P) / np.linalg.norm(Q - P)
                return ax.c2p(*(P + t * (Q - P) + off * np.array([-d_[1], d_[0]])))

            def beyond(P, Q, dist):  # dist scene units past Q, on the line from P through Q
                p_, q_ = ax.c2p(*P), ax.c2p(*Q)
                return q_ + dist * (q_ - p_) / np.linalg.norm(q_ - p_)

            g.add(MathTex("x", font_size=26, color=C.SEQ).move_to(at(O, A, 0.5, -0.2)),
                  MathTex("y", font_size=26, color=C.APPROX).move_to(at(O, B, 0.5, 0.2)),
                  MathTex("x + y", font_size=24, color=C.EPS).move_to(beyond(O, S, 0.45)),
                  MathTex("x - y", font_size=24, color=C.MEASURE).move_to(beyond(A, B, 0.5)))
            return g

        for th in (35, 130):  # the swing's extremes: every label stays inside the frame
            thT.set_value(math.radians(th))
            assert pic().get_left()[0] > -6.9, th
        thT.set_value(math.radians(65))
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
        head = label(r"The parallelogram law: \ $\|x + y\|^2 + \|x - y\|^2 = 2\|x\|^2 + 2\|y\|^2$", font_size=34).to_edge(
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
        head = label(r"The dictionary: \ geometry that survives into infinite dimensions", font_size=34).to_edge(UP,
                                                                                                              buff=0.3)
        card = dict_table(r"$\R^n$", r"a Hilbert space $H$ \ (e.g.\ $L^2$, $\ell^2$)", [
            (r"$x \cdot y = \sum x_i y_i$", r"$\langle f, g\rangle = \int f \bar g$"),
            (r"length $|x|$", r"$\|f\| = \langle f, f\rangle^{1/2}$, \ complete"),
            (r"right angles: \ Pythagoras", r"$\langle f, g\rangle = 0 \Rightarrow \|f + g\|^2 = \|f\|^2 + \|g\|^2$"),
            (r"nearest point of a plane", r"projection onto a closed subspace \ (ch.~6)"),
            (r"a functional is $x \mapsto x \cdot y$", r"Riesz: \ every bounded functional is $\langle \cdot, g\rangle$ \ (ch.~7)"),
            (r"an orthonormal basis", r"orthonormal bases; \ Parseval \ (ch.~8)"),
            (r"closed bounded sets are compact",
             r"fails: \ $e_1, e_2, \ldots$ in the unit ball, \ $\|e_m - e_n\| = \sqrt 2$"),
        ], xs=(-1.55, 0.3, 3.6), widths=(2.8, 5.6), top=2.55, font_size=24, gap=0.42, colors={6: C.PATHOLOGY})
        assert card.get_bottom()[1] > -3.55 and card.get_right()[0] < 6.6 and card.get_left()[0] > -3.1

        # the plane's side, drawn: one small picture of R^2 per row, every number computed
        ix = square_axes([-1.6, 1.6, 1], [-1.6, 1.6, 1], 1.0).move_to([-5.0, 0.05, 0])
        ix.set_opacity(0.35)
        cap_y = ix.get_bottom()[1] - 0.35

        def cap(*lines, color=WHITE):  # one or two centred lines under the picture, at most 3.4 wide
            g_ = VGroup(*[MathTex(t_, font_size=26, color=color) for t_ in lines]).arrange(DOWN, buff=0.1)
            return g_.next_to([ix.get_center()[0], cap_y + 0.15, 0], DOWN, buff=0)

        def arrow(a, b, color, sw=4):
            return Arrow(ix.c2p(*a), ix.c2p(*b), buff=0, color=color, stroke_width=sw, tip_length=0.16,
                         max_tip_length_to_length_ratio=0.3)

        def tag(tex, at, direction, color, buff=0.08):
            return MathTex(tex, font_size=26, color=color).next_to(ix.c2p(*at), direction, buff=buff)

        O = np.zeros(2)
        xv, yv = np.array([1.2, 0.5]), np.array([0.4, 1.1])
        xy_arrows = VGroup(arrow(O, xv, C.SEQ), arrow(O, yv, C.APPROX), tag("x", xv, RIGHT, C.SEQ),
                           tag("y", yv, UP, C.APPROX))
        dot_ = float(xv @ yv)
        assert abs(dot_ - (1.2 * 0.4 + 0.5 * 1.1)) < 1e-12
        P0 = VGroup(cap(rf"x \cdot y = {dot_:.2f}", color=C.INNER))
        nx = float(np.linalg.norm(xv))
        P1 = VGroup(DashedVMobject(Circle(radius=nx * ix.x_length / 3.2, color=C.DIST, stroke_width=2).move_to(ix.c2p(0, 0)),
                                   num_dashes=40),
                    cap(rf"|x| = \sqrt{{x \cdot x}} = {nx:.2f}", color=C.DIST))
        assert abs(nx - math.sqrt(xv @ xv)) < 1e-12
        yp = 0.8 * np.array([-xv[1], xv[0]]) / nx  # perpendicular to x, length 0.8
        hyp = xv + yp
        assert abs(xv @ yp) < 1e-12 and abs(hyp @ hyp - (xv @ xv + yp @ yp)) < 1e-12
        P2 = VGroup(arrow(O, xv, C.SEQ), arrow(xv, hyp, C.APPROX), arrow(O, hyp, C.EPS),
                    right_angle(ix, xv, -xv / nx, yp / 0.8, size=0.14),
                    cap(rf"|x + y|^2 = {hyp @ hyp:.2f}", rf"= |x|^2 + |y|^2 = {xv @ xv:.2f} + {yp @ yp:.2f}", color=C.EPS))
        m_ = np.array([1.0, 0.3]) / math.hypot(1.0, 0.3)
        z = np.array([-0.2, 1.3])
        pz = (z @ m_) * m_
        ts = np.linspace(-1.6, 1.6, 64001)
        dmin = float(np.min(np.linalg.norm(z[None, :] - ts[:, None] * m_[None, :], axis=1)))
        assert abs(dmin - np.linalg.norm(z - pz)) < 1e-4 and abs((z - pz) @ m_) < 1e-12
        P3 = VGroup(Line(ix.c2p(*(-1.5 * m_)), ix.c2p(*(1.5 * m_)), color=C.INNER, stroke_width=3),
                    tag("M", 1.45 * m_, DOWN, C.INNER, 0.12),
                    DashedLine(ix.c2p(*z), ix.c2p(*pz), color=C.EPS, stroke_width=2.5),
                    right_angle(ix, pz, m_, (z - pz) / np.linalg.norm(z - pz), size=0.14),
                    Dot(ix.c2p(*z), radius=0.07, color=WHITE), Dot(ix.c2p(*pz), radius=0.07, color=C.EPS),
                    tag("z", z, UP, WHITE), tag("Pz", pz, DR, C.EPS, 0.05),
                    cap(rf"|z - Pz| = {np.linalg.norm(z - pz):.2f}", r"= \min_{w \in M} |z - w|", color=C.EPS))
        gvec = np.array([0.6, 0.8])
        tg = np.array([-gvec[1], gvec[0]])
        def level_seg(c):  # the level line {x . y = c}, cut to the inset's square
            ts_ = np.linspace(-3, 3, 1201)
            pts_ = c * gvec[None, :] + ts_[:, None] * tg[None, :]
            ok_ = np.all(np.abs(pts_) <= 1.5, axis=1)
            return Line(ix.c2p(*pts_[ok_][0]), ix.c2p(*pts_[ok_][-1]), color=C.FUNCTIONAL, stroke_width=2.5).set_stroke(
                opacity=0.9 if c == 0 else 0.55)

        P4 = VGroup(*[level_seg(c) for c in (-1.0, -0.5, 0.0, 0.5, 1.0)],
                    arrow(O, gvec, C.INNER, 5), tag("y", gvec, RIGHT, C.INNER),
                    cap(r"\text{level lines of } x \mapsto x \cdot y,", r"\text{perpendicular to } y", color=C.FUNCTIONAL))
        assert abs(np.linalg.norm(gvec) - 1) < 1e-12
        th = math.radians(30)
        e1, e2 = np.array([math.cos(th), math.sin(th)]), np.array([-math.sin(th), math.cos(th)])
        v = np.array([0.4, 1.3])
        c1, c2 = float(v @ e1), float(v @ e2)
        assert abs(e1 @ e2) < 1e-12 and np.allclose(c1 * e1 + c2 * e2, v) and abs(c1**2 + c2**2 - v @ v) < 1e-12
        P5 = VGroup(arrow(O, e1, C.INNER, 5), arrow(O, e2, C.INNER, 5), tag("e_1", e1, DOWN, C.INNER),
                    tag("e_2", e2, LEFT, C.INNER),
                    DashedLine(ix.c2p(*v), ix.c2p(*(c1 * e1)), color=GREY_B, stroke_width=2),
                    DashedLine(ix.c2p(*v), ix.c2p(*(c2 * e2)), color=GREY_B, stroke_width=2),
                    arrow(O, v, WHITE, 3), tag("v", v, UP, WHITE),
                    cap(rf"v = {c1:.2f}\,e_1 + {c2:.2f}\,e_2"))
        # compact: points of a bounded sequence (on the circle r = 0.85, angles 2.4 n) and a subsequence whose angles
        # approach 0.6 ever more closely
        nn = np.arange(1, 400)
        ang = (2.4 * nn) % (2 * np.pi)
        sub, best = [], np.inf
        for k_, a_ in zip(nn, ang):
            if abs(a_ - 0.6) < best:
                best = abs(a_ - 0.6)
                sub.append(int(k_))
        assert len(sub) >= 5 and best < 0.01
        pts = 0.85 * np.stack([np.cos(2.4 * nn[:60]), np.sin(2.4 * nn[:60])], 1)
        lim = 0.85 * np.array([math.cos(0.6), math.sin(0.6)])
        P6 = VGroup(Circle(radius=ix.x_length / 3.2, color=C.DIST, stroke_width=2.5).set_fill(C.DIST, 0.12).move_to(ix.c2p(0, 0)),
                    *[Dot(ix.c2p(*q_), radius=0.035, color=GREY_B) for q_ in pts],
                    *[Dot(ix.c2p(*(0.85 * np.array([math.cos(2.4 * k_), math.sin(2.4 * k_)]))), radius=0.06,
                          color=C.EPS) for k_ in sub[-6:]],
                    Circle(radius=0.11, color=C.EPS, stroke_width=2.5).move_to(ix.c2p(*lim)),
                    cap(r"\text{a bounded sequence:}", r"\text{a convergent subsequence}", color=C.EPS))
        pics = [P0, P1, P2, P3, P4, P5, P6]
        for P in pics:
            assert P.get_left()[0] > -6.7 and P.get_right()[0] < card.get_left()[0] - 0.1

        # the row that does not survive, made concrete: e_n = sqrt2 sin(n pi x) in L^2[0, 1]
        xs = np.linspace(0, 1, 4001)
        ecols = [C.SEQ, C.APPROX, C.CLOSED_SET, C.CONNECTED_SET]
        E = [np.sqrt(2) * np.sin(n * np.pi * xs) for n in range(1, 5)]

        def l2(g):
            return math.sqrt(float(np.trapezoid(g * g, xs)))

        norms = [l2(e) for e in E]
        d12, d24 = l2(E[0] - E[1]), l2(E[1] - E[3])
        assert max(abs(v_ - 1) for v_ in norms) < 1e-6 and abs(d12 - math.sqrt(2)) < 1e-6 and abs(d24 - math.sqrt(2)) < 1e-6
        eax = plain_axes([0, 1, 0.25], [-1.6, 1.6, 1], 6.0, 3.2).move_to([-3.4, -0.85, 0])
        eg = [polyline(eax, xs, E[n], color=ecols[n], stroke_width=3) for n in range(4)]
        el = MathTex(r"e_n(x) = \sqrt2\,\sin(n\pi x) \ \text{in } L^2[0, 1]", font_size=28).next_to(eax, UP, buff=0.12)
        ekey = VGroup(*[MathTex(rf"e_{n + 1}", font_size=28, color=ecols[n]) for n in range(4)]).arrange(
            RIGHT, buff=0.45).next_to(eax, DOWN, buff=0.2)
        eside = VGroup(
            MathTex(r"\|e_n\| = 1, \qquad \langle e_m, e_n\rangle = 0 \ (m \ne n)", font_size=28),
            MathTex(r"\|e_m - e_n\|^2 = \|e_m\|^2 + \|e_n\|^2 = 2", font_size=28),
            MathTex(rf"\|e_1 - e_2\| = {d12:.5f}, \quad \|e_2 - e_4\| = {d24:.5f}", font_size=26, color=C.EPS),
            label(r"no subsequence is Cauchy: \ the closed unit ball is not compact", font_size=24, color=C.PATHOLOGY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([3.5, -0.85, 0])
        for r_ in eside:
            if r_.width > 6.2:
                r_.width = 6.2
        eside.arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to([0.35, -0.85, 0], RIGHT, buff=0)
        assert eside.get_left()[0] > eax.get_right()[0] + 0.2 and eside.get_right()[0] < 6.6
        with self.voiceover(
            "<bookmark mark='a'/> A complete inner-product space is a Hilbert space, and almost all of the plane's "
            "geometry carries over. <bookmark mark='b'/> Dot products become integrals. <bookmark mark='b2'/> Lengths "
            "become norms, and the space is complete. <bookmark mark='b3'/> Pythagoras holds for perpendicular "
            "functions. <bookmark mark='c'/> And the next three chapters carry over three more facts: nearest points, "
            "<bookmark mark='c2'/> functionals as vectors, <bookmark mark='c3'/> and orthonormal bases. "
            "<bookmark mark='d'/> One thing does not survive. <bookmark mark='e'/> In L two of the unit interval, "
            "take e n equal to root two times sine of n pi x. Each has norm one and any two are perpendicular, so by "
            "Pythagoras they are all at distance root two from each other: no subsequence can converge, and the closed "
            "unit ball is not compact. Compactness is the price of infinitely many dimensions."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), FadeIn(card.titles), Create(ix), FadeIn(xy_arrows))
            shown = None
            for i, mark in enumerate(("b", "b2", "b3", "c", "c2", "c3", "d")):
                vo.wait_until(mark)
                anims = [FadeIn(card.rows[i]), FadeIn(card.arrows[i]), FadeIn(pics[i])]
                if shown is not None:
                    anims.append(FadeOut(shown))
                if i == 2:  # the plain x and y give way to the right triangle
                    anims.append(FadeOut(xy_arrows))
                self.play(*anims, run_time=0.8)
                shown = pics[i]
            vo.wait_until("e")
            keep = VGroup(card.rows[6], card.arrows[6])
            self.play(FadeOut(VGroup(card.titles, *card.rows[:6], *card.arrows[:6], ix, shown)),
                      keep.animate.next_to(head, DOWN, buff=0.35))
            self.play(Create(eax), FadeIn(el), Create(eg[0]), FadeIn(ekey[0]), run_time=0.9)
            for n in range(1, 4):
                self.play(Create(eg[n]), FadeIn(ekey[n]), run_time=0.8)
            self.play(FadeIn(eside[:2]))
            self.play(FadeIn(eside[2:]))
        self.wait(0.4)
        self.clear_scene()
