from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis.analysis9.common import bump, load, plain_axes, polyline


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
        import mpmath
        d = load("mollifier")
        tiny, xs, b = float(d["tiny"]), d["xs"], d["b"]
        ax = plain_axes([-1.4, 1.4, 0.5], [-0.05, 0.42, 0.1], 6.0, 2.5, numbers=True, font_size=18,
                        x_axis_config={"decimal_number_config": {"num_decimal_places": 1}},
                        y_axis_config={"decimal_number_config": {"num_decimal_places": 1}}).move_to([-3.2, 0.95, 0])
        g = polyline(ax, xs, b, color=C.TEST_FN, stroke_width=4)
        supp = Line(ax.c2p(-1, -0.03), ax.c2p(1, -0.03), color=C.EPS, stroke_width=6)
        s_l = MathTex(r"\operatorname{supp} = [-1, 1]", font_size=24, color=C.EPS).next_to(ax, DOWN, buff=0.08)
        f_l = MathTex(r"\rho(x) = e^{-1/(1 - x^2)} \ \text{ on } |x| < 1, \ \ 0 \text{ outside}", font_size=26,
                      color=C.TEST_FN).next_to(ax, UP, buff=0.1)
        # what the narration says: the tenth derivative dies at the edge. log10 |rho^(10)(1 - delta)| for
        # delta = 10^-u, u from 2 to 3 (mpmath, 60 digits): 10^14 at a hundredth from the edge, 10^-160 at a thousandth
        rho_ = lambda z: mpmath.exp(-1 / (1 - z * z))  # noqa: E731
        us = np.linspace(2, 3, 41)
        with mpmath.workdps(60):
            lv = np.array([float(mpmath.log10(abs(mpmath.diff(rho_, 1 - mpmath.mpf(10) ** (-mpmath.mpf(u)), 10))))
                           for u in us])
        assert abs(lv[-1] - tiny) < 1e-6 and np.all(np.diff(lv) < 0)  # the stored sympy value; a monotone plunge
        lo = -170.0
        bx = plain_axes([2, 3, 0.5], [0, 20 - lo, 50], 6.0, 1.75,
                        y_axis_config={"include_ticks": False}).move_to([-3.2, -2.45, 0])
        dcurve = polyline(bx, us, lv - lo, color=C.TEST_FN, stroke_width=3.5)
        one = DashedLine(bx.c2p(2, -lo), bx.c2p(3, -lo), color=GREY_B, stroke_width=2)
        one_l = MathTex(r"1", font_size=20, color=GREY_B).next_to(bx.c2p(3, -lo), RIGHT, buff=0.1)
        dl = VGroup(*[Dot(bx.c2p(u, v - lo), radius=0.06, color=C.EPS) for u, v in zip(us[::20], lv[::20])])
        vl = VGroup(*[MathTex(rf"10^{{{v:.0f}}}", font_size=22, color=C.EPS).next_to(d_, dir_, buff=0.1)
                      for d_, v, dir_ in zip(dl, lv[::20], (UR, DL, RIGHT))])  # each on the side away from the curve
        kl = VGroup(*[MathTex(t_, font_size=18, color=GREY_B).next_to(bx.c2p(u, 0), DOWN, buff=0.1)
                      for u, t_ in ((2, r"\delta = 10^{-2}"), (2.5, r"10^{-2.5}"), (3, r"10^{-3}"))])
        b_l = label(r"$|\rho^{(10)}(1 - \delta)|$, \ log scale: \ $\to 0$ at the edge", font_size=22,
                    color=GREY_A).next_to(bx, UP, buff=0.08)
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
            self.play(Create(bx), FadeIn(b_l), FadeIn(kl), Create(one), FadeIn(one_l), Create(dcurve), run_time=2.0)
            self.play(FadeIn(dl), FadeIn(vl), FadeIn(rows[3:5]))
            vo.wait_until("c")
            self.play(FadeIn(rows[5]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def space(self):
        ax = plain_axes([-2, 2, 1], [-0.5, 2.3, 0.5], 6.0, 2.8).move_to([-3.2, 1.0, 0])  # phi_1 peaks at 2.2
        x = np.linspace(-2, 2, 4001)
        g0 = bump(x / 1.2) / math.exp(-1)  # peak 1
        phi = g0 * (1 + 0.5 * np.sin(3 * x))
        nT = ValueTracker(1.0)

        def phin():
            n = nT.get_value()
            return polyline(ax, x, phi + g0 * np.sin(4 * n * x) / (n * n), color=C.SEQ, stroke_width=3)

        # the wiggle w_n = g0 sin(4nx) / n^2 and its second derivative, in closed form:
        # w_n'' = g0'' sin / n^2 + 8 g0' cos / n - 16 g0 sin: amplitude 16 for every n
        u = x / 1.2
        q = np.where(np.abs(u) < 1, 1 - u * u, 1.0)
        bu = np.where(np.abs(u) < 1, np.exp(-1 / q), 0.0) * math.e
        g1 = bu * (-2 * u / q**2) / 1.2
        g2 = bu * (4 * u * u / q**4 - 2 / q**2 - 8 * u * u / q**3) / 1.44

        def w2(n):
            return g2 * np.sin(4 * n * x) / n**2 + 8 * g1 * np.cos(4 * n * x) / n - 16 * g0 * np.sin(4 * n * x)

        for n in (1.0, 2.5, 4.0):
            w = g0 * np.sin(4 * n * x) / n**2
            num = np.gradient(np.gradient(w, x), x)
            assert np.abs(num - w2(n))[200:-200].max() < 1e-2  # closed form = finite differences
            assert 15.9 < np.abs(w2(n)).max() < 17.0 and np.abs(w).max() <= 1 / n**2 + 1e-12
            assert abs(np.abs(np.gradient(w, x)).max() - 4 / n) < 1e-3  # sup |w_n'| = 4/n -> 0
        cx = plain_axes([-2, 2, 1], [-20, 20, 10], 6.0, 1.9).move_to([-3.2, -2.35, 0])
        d2 = always_redraw(lambda: polyline(cx, x, w2(nT.get_value()), color=C.SEQ, stroke_width=3))
        guides = VGroup(*[DashedLine(cx.c2p(-2, h), cx.c2p(2, h), color=GREY_B, stroke_width=2) for h in (16, -16)])
        g_l = MathTex(r"\pm 16", font_size=22, color=GREY_B).next_to(cx.c2p(2, 16), RIGHT, buff=0.1)
        d2_l = MathTex(r"(\varphi_n - \varphi)''", r": \ \text{does not shrink}", font_size=24).next_to(cx, UP, buff=0.08)
        d2_l[0].set_color(C.SEQ)
        d2_l[1].set_color(C.PATHOLOGY)
        g = polyline(ax, x, phi, color=C.TEST_FN, stroke_width=4)
        gn = always_redraw(phin)
        lphi = MathTex(r"\varphi", font_size=28, color=C.TEST_FN).next_to(ax.c2p(-1.0, float(np.interp(-1.0, x, phi))), UL,
                                                                         buff=0.08)
        lphin = MathTex(r"\varphi_n", font_size=28, color=C.SEQ).next_to(ax.c2p(1.05, 1.25), RIGHT, buff=0.1)
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
            if r_.width > 6.0:
                r_.width = 6.0
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([3.5, -0.4, 0])
        head = label(r"The space of test functions, \ and convergence in it", font_size=34).to_edge(UP, buff=0.3)
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
            self.play(FadeIn(gn), FadeIn(lphi), FadeIn(lphin), Create(cx), Create(guides), FadeIn(g_l), FadeIn(d2),
                      FadeIn(d2_l))
            self.play(nT.animate.set_value(4.0), run_time=3.0)
            self.play(FadeIn(rows[6:]))
            vo.wait_until("d")
            self.play(FadeIn(rows[4:6]))
        gn.clear_updaters()
        d2.clear_updaters()
        self.wait(0.4)
        self.clear_scene()
