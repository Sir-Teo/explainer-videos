from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis.analysis9.common import load, plain_axes, polyline


class Structure(VoiceoverScene):
    def construct(self):
        self.card()
        self.support()
        self.local()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(4, r"Supports and local structure", r"What does a distribution look like up close?",
                            lit=(1945,), part=9)
        with self.voiceover("Chapter four: where a distribution lives, and what it's made of."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def support(self):
        from videos.analysis.analysis9.common import bump
        line = NumberLine(x_range=[-2, 2, 0.5], length=11, include_numbers=True, font_size=22,
                          decimal_number_config={"num_decimal_places": 1}).move_to([0, 0.6, 0])
        y0 = line.n2p(0)[1]  # the axis itself (move_to centred the line together with its numbers)

        def X(v):
            return line.n2p(v)[0]

        f_reg = Rectangle(width=X(1.6) - X(0.8), height=0.5, stroke_width=0, fill_color=C.FUNC,
                          fill_opacity=0.4).move_to([(X(0.8) + X(1.6)) / 2, y0 + 0.25, 0])  # sits on the axis
        d_pt = VGroup(Arrow([X(-0.9), y0, 0], [X(-0.9), y0 + 1.3, 0], buff=0, color=C.DISTRIBUTION,
                            stroke_width=5, tip_length=0.18),
                      MathTex(r"\delta'_{-0.9}", font_size=26, color=C.DISTRIBUTION).next_to([X(-0.9), y0 + 1.3, 0], UP,
                                                                                          buff=0.05))
        f_l = MathTex(r"f = \mathbf 1_{[0.8, 1.6]}", font_size=26, color=C.FUNC).next_to(f_reg, UP, buff=0.6)  # over phi
        # the support, marked on the axis itself (clear of the numbers under it)
        supp = VGroup(Dot([X(-0.9), y0, 0], radius=0.1, color=C.EPS),
                      Line([X(0.8), y0, 0], [X(1.6), y0, 0], color=C.EPS, stroke_width=9))
        s_l = label(r"support of $T = \delta'_{-0.9} + f$: \ $\{-0.9\} \cup [0.8, 1.6]$", font_size=24, color=C.EPS).next_to(
            line, DOWN, buff=0.5)
        # a test function slid along the line: <T, phi_c> = -phi_c'(-0.9) + int_0.8^1.6 phi_c, zero while phi_c lives in
        # the gap (-0.9, 0.8) where T vanishes
        w = 0.35
        xg = np.linspace(-2, 2, 2001)
        cT = ValueTracker(0.0)

        def phi_c(v, c):
            return bump((np.asarray(v, float) - c) / w) * math.e  # peak 1

        def dphi_c(v, c):
            u = (v - c) / w
            return 0.0 if abs(u) >= 1 else math.exp(-1 / (1 - u * u)) * math.e * (-2 * u / (1 - u * u) ** 2) / w

        xi = np.linspace(0.8, 1.6, 4001)

        def act(c):
            yv = phi_c(xi, c)
            return -dphi_c(-0.9, c) + float(np.sum((yv[1:] + yv[:-1]) * np.diff(xi)) / 2)

        assert act(0.0) == 0.0 and act(1.2) > 0.4  # in the gap: exactly 0; over the block: its area
        h_ = 1e-6
        assert abs(dphi_c(-0.9, -0.7) - (phi_c(-0.9 + h_, -0.7) - phi_c(-0.9 - h_, -0.7)) / (2 * h_)) < 1e-6

        def phi_pts():
            c = cT.get_value()
            m = np.abs(xg - c) <= w
            return VMobject(color=C.TEST_FN, stroke_width=4).set_points_as_corners(
                np.array([[X(v), y0 + 0.9 * yv, 0] for v, yv in zip(xg[m], phi_c(xg[m], c))]))

        phi_g = always_redraw(phi_pts)
        rd = VGroup(MathTex(r"\langle T,", r"\varphi", r"\rangle =", font_size=30),
                    DecimalNumber(0.0, num_decimal_places=3, font_size=30, color=C.EPS)).arrange(RIGHT, buff=0.15)
        rd[0][1].set_color(C.TEST_FN)  # phi: the green bump
        rd.move_to([-4.3, y0 + 2.0, 0])
        rd[1].add_updater(lambda m: m.set_value(act(cT.get_value())))
        rows = VGroup(
            label(r"\textbf{FA 6.20} \ $T$ vanishes on an open set $\omega$ if $\langle T, \varphi\rangle = 0$ whenever "
                  r"$\operatorname{supp}\varphi \subset \omega$", font_size=22),
            label(r"the support is what is left when every such $\omega$ is removed: \ where $T$ is awake", font_size=22),
            label(r"\textbf{FA 6.25} \ a distribution supported at one point is $\sum_{|\alpha| \le N} c_\alpha "
                  r"\partial^\alpha\delta$", font_size=24, color=C.EPS),
            label(r"\textbf{FA 6.24} \ compactly supported distributions are exactly the dual of $C^\infty$", font_size=22,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.12).to_edge(DOWN, buff=0.35)
        head = label(r"Where a distribution lives", font_size=34).to_edge(UP, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> A distribution vanishes on an open set if it gives zero on every test function "
            "living there. Remove all such sets, and what's left is the support: where the distribution is awake. "
            "<bookmark mark='b'/> Delta prime at minus 0.9, plus the indicator of an interval, has support the point "
            "and the interval. <bookmark mark='c'/> And a distribution supported at a single point can only be a "
            "finite combination of delta and its derivatives. There's nothing else that small."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), Create(line), GrowArrow(d_pt[0]), FadeIn(d_pt[1]), FadeIn(f_reg), FadeIn(f_l),
                      FadeIn(rows[0]))
            self.play(FadeIn(phi_g), FadeIn(rd))
            self.play(cT.animate.set_value(1.2), run_time=2.0)  # over the block: T acts
            self.play(cT.animate.set_value(-0.7), FadeIn(rows[1]), run_time=2.2)  # over the point: delta' reads the slope
            self.play(cT.animate.set_value(0.0), run_time=1.5)  # back in the gap: 0
            vo.wait_until("b")
            self.play(FadeIn(supp), FadeIn(s_l))
            vo.wait_until("c")
            self.play(FadeIn(rows[2:]))
        for m_ in (phi_g, rd[1]):
            m_.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def local(self):
        d = load("structure")
        x, F, lhs, rhs = d["x"], d["F"], float(d["lhs"]), float(d["rhs"])
        # x numbered (the narration places the singularities at 0.3 and -0.4); no y numbers: the arrows carry no height
        ax = plain_axes([-3, 3, 1], [-0.2, 3.2, 1], 6.2, 3.4, numbers=True, font_size=18,
                        x_axis_config={"decimal_number_config": {"num_decimal_places": 0}},
                        y_axis_config={"include_numbers": False}).move_to([-3.2, -0.6, 0])
        g = runs(ax, x, F, C.FUNC, 3.5)  # cut where it leaves the window (clamping would draw a false plateau)
        kinks = VGroup(*[Dot(ax.c2p(a, float(np.interp(a, x, F))), radius=0.06, color=C.EPS) for a in (-0.4, 0.3, 1.0)])
        f_l = MathTex(r"F(x) = (x - 0.3)_+ + \tfrac{2}{3!}(x + 0.4)_+^3 + \tfrac{1}{5!}(x - 1)_+^5", font_size=24,
                      color=C.FUNC).next_to(ax, UP, buff=0.1)
        rows = VGroup(
            label(r"a continuous $F$, \ differentiated five times:", font_size=24),
            MathTex(r"F^{(5)} = \delta'''_{0.3} + 2\,\delta'_{-0.4} + \mathbf 1_{[1, \infty)}", font_size=30,
                    color=C.DISTRIBUTION),
            label(r"tested against $\varphi = e^{-x^2/0.72}$:", font_size=22, color=GREY_A),
            MathTex(rf"\langle F^{{(5)}}, \varphi\rangle = -\langle F, \varphi^{{(5)}}\rangle = {rhs:.6f}", font_size=26),
            MathTex(rf"-\varphi'''(0.3) - 2\varphi'(-0.4) + \int_1^\infty \varphi = {lhs:.6f}", font_size=26),
            label(r"\textbf{FA 6.26--6.27} \ every distribution is, on each compact set,", font_size=24, color=C.EPS),
            label(r"a derivative of some continuous function", font_size=24, color=C.EPS),
            label(r"$\mathcal D'$ is ``continuous functions, differentiated''", font_size=24, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([3.4, -0.5, 0])
        for r_ in rows:
            if r_.width > 6.4:
                r_.width = 6.4
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([3.4, -0.5, 0])
        assert abs(lhs - rhs) < 1e-6
        # the five derivatives drawn: a regular part (cut at the window) plus labelled arrows for the deltas
        xr = np.linspace(-3, 3, 6001)

        def pp(t, k):
            return np.where(t > 0, t ** k, 0.0) / math.factorial(k)

        H = lambda t: np.where(t > 0, 1.0, 0.0)  # noqa: E731
        reg = [pp(xr - 0.3, 1) + 2 * pp(xr + 0.4, 3) + pp(xr - 1, 5),
               H(xr - 0.3) + 2 * pp(xr + 0.4, 2) + pp(xr - 1, 4),
               2 * pp(xr + 0.4, 1) + pp(xr - 1, 3),
               2 * H(xr + 0.4) + pp(xr - 1, 2),
               pp(xr - 1, 1),
               H(xr - 1)]
        away = (np.abs(xr + 0.4) > 0.02) & (np.abs(xr - 0.3) > 0.02) & (np.abs(xr - 1) > 0.02) & (np.abs(xr) < 2.9)
        for k in range(5):  # each regular part differentiates into the next, away from the kinks
            assert np.abs(np.gradient(reg[k], xr) - reg[k + 1])[away].max() < 2e-2
        assert abs(np.interp(0.301, xr, reg[1]) - np.interp(0.299, xr, reg[1]) - 1) < 5e-3  # jump 1 -> delta_0.3
        assert abs(np.interp(-0.399, xr, reg[3]) - np.interp(-0.401, xr, reg[3]) - 2) < 5e-3  # jump 2 -> 2 delta_-0.4
        sing = [[], [], [(0.3, r"\delta_{0.3}", 2.7, UR)], [(0.3, r"\delta'_{0.3}", 2.7, UR)],
                [(0.3, r"\delta''_{0.3}", 2.7, UR), (-0.4, r"2\delta_{-0.4}", 2.0, UL)],
                [(0.3, r"\delta'''_{0.3}", 2.7, UR), (-0.4, r"2\delta'_{-0.4}", 2.0, UL)]]

        def stage(k):  # (regular part, {position: arrow}, {position: label})
            arrs, labs = {}, {}
            for a_, t_, h_, dir_ in sing[k]:
                arrs[a_] = Arrow(ax.c2p(a_, 0), ax.c2p(a_, h_), buff=0, color=C.DISTRIBUTION, stroke_width=5,
                                 max_tip_length_to_length_ratio=0.12)
                labs[a_] = MathTex(t_, font_size=26, color=C.DISTRIBUTION).next_to(ax.c2p(a_, h_), dir_, buff=0.06)
            return runs(ax, xr, reg[k], C.FUNC if k == 0 else C.DISTRIBUTION, 3.5), arrs, labs

        stages = [stage(k) for k in range(6)]
        slabs = [MathTex(r"F" + ("" if k == 0 else rf"^{{({k})}}"), font_size=30, color=C.DISTRIBUTION).move_to(
            ax.c2p(-2.4, 2.7)) for k in range(6)]
        head = label(r"Every distribution is locally a derivative of a continuous function", font_size=34).to_edge(UP,
                                                                                                              buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Here's the deepest structure theorem. Take this continuous function F, with a few "
            "kinks. <bookmark mark='b'/> Differentiate it five times, as a distribution. Each kink sharpens step by "
            "step into a jump, then a delta, then derivatives of delta: the fifth derivative is delta triple prime at "
            "0.3, plus twice delta prime at minus 0.4, plus a step. <bookmark mark='c'/> Tested against a Gaussian, "
            "both sides agree to every digit shown. <bookmark mark='d'/> And it works in general: on each compact set, "
            "every distribution is some derivative of a continuous function. The whole space is just continuous "
            "functions, differentiated."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), Create(ax), Create(g), FadeIn(f_l), FadeIn(kinks))
            vo.wait_until("b")
            self.play(FadeIn(rows[0]), FadeIn(slabs[0]), FadeOut(g), FadeIn(stages[0][0]))
            for k in range(1, 6):
                # the regular part morphs on its own (one transform across differently shaped groups throws stray
                # strokes); an arrow already up stays put, a new one grows, the labels cross-fade
                (r0, a0, l0), (r1, a1, l1) = stages[k - 1], stages[k]
                anims = [ReplacementTransform(r0, r1), FadeTransform(slabs[k - 1], slabs[k])]
                for p_ in a1:
                    if p_ in a0:
                        a1[p_] = a0[p_]
                        anims.append(FadeTransform(l0[p_], l1[p_]))
                    else:
                        anims += [GrowArrow(a1[p_]), FadeIn(l1[p_])]
                if k == 1:
                    anims.append(FadeOut(kinks))
                self.play(*anims, run_time=1.3)
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2:5]))
            vo.wait_until("d")
            self.play(FadeIn(rows[5:]))
        self.wait(0.4)
        self.clear_scene()
