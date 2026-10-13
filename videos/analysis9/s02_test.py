from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis9.common import bump, load, plain_axes, polyline


class TestFunctions(VoiceoverScene):
    def construct(self):
        self.card()
        self.bump_()
        self.space()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(1, r"Test functions", r"Which functions are smooth enough to test with?", lit=(1945,), part=9)
        with self.voiceover("Chapter one: test functions, smooth and compactly supported."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def bump_(self):
        d = load("mollifier")
        edge, tiny, xs, b = d["edge"], float(d["tiny"]), d["xs"], d["b"]
        ax = plain_axes([-1.4, 1.4, 0.5], [-0.05, 0.42, 0.1], 6.0, 3.0, numbers=True, font_size=18,
                        x_axis_config={"decimal_number_config": {"num_decimal_places": 1}},
                        y_axis_config={"decimal_number_config": {"num_decimal_places": 1}}).move_to([-3.2, 0.4, 0])
        g = polyline(ax, xs, b, color=C.TEST_FN, stroke_width=4)
        supp = Line(ax.c2p(-1, -0.03), ax.c2p(1, -0.03), color=C.EPS, stroke_width=6)
        s_l = MathTex(r"\operatorname{supp} = [-1, 1]", font_size=24, color=C.EPS).next_to(ax, DOWN, buff=0.08)
        f_l = MathTex(r"\rho(x) = e^{-1/(1 - x^2)} \ \text{ on } |x| < 1, \ \ 0 \text{ outside}", font_size=26,
                      color=C.TEST_FN).next_to(ax, UP, buff=0.1)
        bx = plain_axes([-0.5, 10.5, 1], [0, 1, 0.5], 6.0, 1.5).move_to([-3.2, -2.95, 0])
        assert tiny < -100
        lv = np.log10(np.maximum(edge, 1e-300))
        hts = 1.35 * (lv - lv.min() + 0.5) / (lv.max() - lv.min() + 0.5)
        bars = VGroup(*[Rectangle(width=0.35, height=h, stroke_width=0, fill_color=C.TEST_FN, fill_opacity=0.8).move_to(
            [bx.c2p(k, 0)[0], bx.c2p(0, 0)[1] + h / 2, 0]) for k, h in enumerate(hts)])
        b_l = label(r"$|\rho^{(k)}(0.98)|$ for $k = 0, \ldots, 10$ \ (log scale): \ large but finite", font_size=20,
                    color=GREY_A).next_to(bx, UP, buff=0.05)
        kl = VGroup(*[MathTex(str(k), font_size=16, color=GREY_B).next_to(bx.c2p(k, 0), DOWN, buff=0.08) for k in (0, 5, 10)],
                    MathTex(rf"{sci(float(edge[0]), 0)}", font_size=16, color=C.TEST_FN).next_to(bars[0], UP, buff=0.05),
                    MathTex(rf"{sci(float(edge[-1]), 0)}", font_size=16, color=C.TEST_FN).next_to(bars[-1], RIGHT, buff=0.08))
        rows = VGroup(
            label(r"Part 2's flat function, \ $e^{-1/x}$, \ finally earns its keep:", font_size=24),
            label(r"glued at both ends, \ it gives a $C^\infty$ function", font_size=24),
            label(r"that is exactly $0$ outside $[-1, 1]$", font_size=24),
            MathTex(rf"|\rho^{{(10)}}(1 - 10^{{-3}})| \approx 10^{{{tiny:.0f}}}", font_size=28, color=C.EPS),
            label(r"every derivative dies at the edge \ (sympy, 50 digits)", font_size=22, color=GREY_A),
            label(r"no analytic function can do this \ (Part 7)", font_size=22, color=C.PATHOLOGY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to([3.5, -0.4, 0])
        for r_ in rows:
            if r_.width > 6.0:
                r_.width = 6.0
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to([3.5, -0.4, 0])
        head = label(r"A smooth function that is exactly zero outside an interval", font_size=34).to_edge(UP, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Test functions must be smooth, and vanish outside a bounded set. Do any exist? Part "
            "2's flat function says yes. Glue e to the minus one over one minus x squared into the interval from "
            "minus one to one, and zero outside. <bookmark mark='b'/> It's infinitely differentiable, even at the two "
            "gluing points: every derivative goes to zero there, faster than any power. The tenth derivative, a "
            "thousandth from the edge, is about ten to the minus one hundred sixty. <bookmark mark='c'/> No analytic "
            "function can vanish on an interval without vanishing everywhere, as Part 7 showed. Test functions are "
            "smooth, but deliberately not analytic."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), Create(ax), Create(g), FadeIn(f_l), FadeIn(rows[:3]))
            self.play(Create(supp), FadeIn(s_l))
            vo.wait_until("b")
            self.play(Create(bx), FadeIn(b_l), FadeIn(kl), LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars], lag_ratio=0.1),
                      run_time=2.0)
            self.play(FadeIn(rows[3:5]))
            vo.wait_until("c")
            self.play(FadeIn(rows[5]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def space(self):
        ax = plain_axes([-2, 2, 1], [-0.5, 2.3, 0.5], 6.0, 3.0).move_to([-3.2, -0.3, 0])  # phi_1 peaks at 2.2
        x = np.linspace(-2, 2, 2001)
        phi = bump(x / 1.2) * (1 + 0.5 * np.sin(3 * x)) / math.exp(-1)
        nT = ValueTracker(1.0)

        def phin():
            n = nT.get_value()
            y = bump(x / 1.2) * (1 + 0.5 * np.sin(3 * x)) / math.exp(-1) + bump(x / 1.2) * np.sin(4 * n * x) / (n * n) / math.exp(-1)
            return polyline(ax, x, y, color=C.SEQ, stroke_width=3)

        g = polyline(ax, x, phi, color=C.TEST_FN, stroke_width=4)
        gn = always_redraw(phin)
        K = Line(ax.c2p(-1.2, -0.35), ax.c2p(1.2, -0.35), color=C.EPS, stroke_width=6)
        K_l = MathTex(r"K", font_size=26, color=C.EPS).next_to(ax.c2p(1.2, -0.35), RIGHT, buff=0.1)
        rows = VGroup(
            label(r"$\mathcal D(\Omega)$: \ $C^\infty$ functions with compact support in $\Omega$", font_size=26),
            label(r"\textbf{FA 6.2--6.5} \ $\varphi_n \to \varphi$ in $\mathcal D$ \ when", font_size=24),
            label(r"all supports stay in one compact $K$, \ and", font_size=24),
            MathTex(r"\sup |\partial^\alpha(\varphi_n - \varphi)| \to 0 \ \text{ for every } \alpha", font_size=28,
                    color=C.EPS),
            label(r"each $\mathcal D_K$ is a Fr\'echet space \ (Part 8, chapter 2);", font_size=22, color=GREY_A),
            label(r"$\mathcal D(\Omega)$ glues them: \ complete, \ but not metrizable", font_size=22, color=GREY_A),
            label(r"here: \ the wiggle $\sin(4nx)/n^2$ has $k$-th derivative $\sim 4^k n^{k-2}$:", font_size=22),
            label(r"it goes to $0$ in sup and in $\varphi'$, \ not in $\varphi''$ and beyond", font_size=22,
                  color=C.PATHOLOGY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([3.5, -0.4, 0])
        for r_ in rows:
            if r_.width > 6.4:
                r_.width = 6.4
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([3.5, -0.4, 0])
        head = label(r"The space of test functions, \ and what convergence means there", font_size=32).to_edge(UP, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> The test functions on a region form the space D. <bookmark mark='b'/> A sequence "
            "converges there when all the supports stay inside one compact set, and every derivative converges "
            "uniformly. <bookmark mark='c'/> These blue functions add a fast wiggle of size one over n squared. The "
            "wiggle shrinks in the sup norm and in the first derivative, but its second derivative stays the same "
            "size and higher ones grow, so the sequence does not converge in D. "
            "<bookmark mark='d'/> On each compact set this is a Fréchet space, from Part 8, and D glues them "
            "together, which is why Rudin needed topological vector spaces."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), Create(ax), Create(g), Create(K), FadeIn(K_l), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1:4]))
            vo.wait_until("c")
            self.play(FadeIn(gn))
            self.play(nT.animate.set_value(4.0), run_time=3.0)
            self.play(FadeIn(rows[6:]))
            vo.wait_until("d")
            self.play(FadeIn(rows[4:6]))
        gn.clear_updaters()
        self.wait(0.4)
        self.clear_scene()
