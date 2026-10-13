from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis9.common import load, plain_axes, polyline


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
        line = NumberLine(x_range=[-2, 2, 0.5], length=11, include_numbers=True, font_size=22,
                          decimal_number_config={"num_decimal_places": 1}).move_to([0, 0.6, 0])
        f_reg = Rectangle(width=line.n2p(1.6)[0] - line.n2p(0.8)[0], height=0.5, stroke_width=0, fill_color=C.FUNC,
                          fill_opacity=0.4).move_to([(line.n2p(0.8)[0] + line.n2p(1.6)[0]) / 2, 0.6, 0])
        d_pt = VGroup(Arrow(line.n2p(-0.9) + DOWN * 0.0, line.n2p(-0.9) + UP * 1.3, buff=0, color=C.DISTRIBUTION,
                            stroke_width=5, tip_length=0.18),
                      MathTex(r"\delta'_{-0.9}", font_size=26, color=C.DISTRIBUTION).next_to(line.n2p(-0.9) + UP * 1.3, UP,
                                                                                          buff=0.05))
        f_l = MathTex(r"f = \mathbf 1_{[0.8, 1.6]}", font_size=26, color=C.FUNC).next_to(f_reg, UP, buff=0.15)
        supp = VGroup(Line(line.n2p(-0.9) + DOWN * 0.45, line.n2p(-0.9) + DOWN * 0.45, color=C.EPS, stroke_width=8),
                      Dot(line.n2p(-0.9) + DOWN * 0.45, radius=0.08, color=C.EPS),
                      Line(line.n2p(0.8) + DOWN * 0.45, line.n2p(1.6) + DOWN * 0.45, color=C.EPS, stroke_width=8))
        s_l = label(r"support of $T = \delta'_{-0.9} + f$: \ $\{-0.9\} \cup [0.8, 1.6]$", font_size=24, color=C.EPS).next_to(
            line, DOWN, buff=0.8)
        rows = VGroup(
            label(r"\textbf{FA 6.20} \ $T$ vanishes on an open set $\omega$ if $\langle T, \varphi\rangle = 0$ whenever "
                  r"$\operatorname{supp}\varphi \subset \omega$", font_size=22),
            label(r"the support is what is left when every such $\omega$ is removed: \ where $T$ is awake", font_size=22),
            label(r"\textbf{FA 6.25} \ a distribution supported at one point is $\sum_{|\alpha| \le N} c_\alpha "
                  r"\partial^\alpha\delta$", font_size=24, color=C.EPS),
            label(r"\textbf{FA 6.24} \ compactly supported distributions are exactly the dual of $C^\infty$", font_size=22,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.12).to_edge(DOWN, buff=0.3)
        head = label(r"Where a distribution lives", font_size=34).to_edge(UP, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> A distribution vanishes on an open set if it gives zero on every test function "
            "living there. Remove all such sets, and what's left is the support: where the distribution is awake. "
            "<bookmark mark='b'/> Delta prime at minus 0.9, plus the indicator of an interval, has support the point "
            "and the interval. <bookmark mark='c'/> And a distribution supported at a single point can only be a "
            "finite combination of delta and its derivatives. There's nothing else that small."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), Create(line), FadeIn(rows[:2]))
            vo.wait_until("b")
            self.play(GrowArrow(d_pt[0]), FadeIn(d_pt[1]), FadeIn(f_reg), FadeIn(f_l))
            self.play(FadeIn(supp), FadeIn(s_l))
            vo.wait_until("c")
            self.play(FadeIn(rows[2:]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def local(self):
        d = load("structure")
        x, F, lhs, rhs = d["x"], d["F"], float(d["lhs"]), float(d["rhs"])
        ax = plain_axes([-3, 3, 1], [-0.2, 3.2, 1], 6.2, 3.4, numbers=True, font_size=18,
                        x_axis_config={"decimal_number_config": {"num_decimal_places": 0}},
                        y_axis_config={"decimal_number_config": {"num_decimal_places": 0}}).move_to([-3.2, -0.6, 0])
        g = polyline(ax, x, np.minimum(F, 3.2), color=C.FUNC, stroke_width=3.5)
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
        head = label(r"Every distribution is locally a derivative of a continuous function", font_size=32).to_edge(UP,
                                                                                                              buff=0.25)
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
            self.play(FadeIn(rows[:2]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2:5]))
            vo.wait_until("d")
            self.play(FadeIn(rows[5:]))
        self.wait(0.4)
        self.clear_scene()
