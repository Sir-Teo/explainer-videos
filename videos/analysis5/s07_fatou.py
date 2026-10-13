from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis5.common import area_under, plain_axes, polyline
from videos.analysis5.compute import trap


class Fatou(VoiceoverScene):
    def construct(self):
        self.card()
        self.statement()
        self.cosines()
        self.escapes()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(6, r"Fatou's lemma", r"What survives when the functions do not increase?", lit=(), part=5)
        with self.voiceover("Chapter six: Fatou's lemma, the inequality that limits always satisfy."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def statement(self):
        head = VGroup(label(r"\textbf{RCA 1.28} \ (Fatou, 1906) \ for measurable $f_n \ge 0$:", font_size=30),
                      MathTex(r"\int \liminf_{n \to \infty} f_n\,d\mu \;\le\; \liminf_{n \to \infty} \int f_n\,d\mu",
                              font_size=40, color=C.EPS)).arrange(DOWN, buff=0.2).to_edge(UP, buff=0.3)
        rows = [
            MathTex(r"g_k", r"=", r"\inf_{i \ge k} f_i \;\nearrow\; \liminf f_n", font_size=32),
            MathTex(r"\int g_k", r"\le", r"\int f_k \quad (\text{since } g_k \le f_k)", font_size=32),
            MathTex(r"\int \liminf f_n", r"=", r"\lim_k \int g_k \le \liminf_k \int f_k", font_size=32),
        ]
        whys = [why(r"an increasing sequence", 22), why(r"monotonicity of $\int$", 22),
                why(r"monotone convergence (1.26)", 22)]
        step = ladder(self, rows, whys, keep=3, top=1.3, buff=0.45, x=2.75, edge=6.9)
        # the picture: f_i = h + (-1)^i (0.65 / i) sin 3x >= 0 oscillates around h = 1.3 + 0.6 sin x and tends to it
        x = np.linspace(0, 2 * np.pi, 801)
        h = 1.3 + 0.6 * np.sin(x)
        w = np.sin(3 * x)

        def f(i):
            return h + (-1) ** i * (0.65 / i) * w

        def g(k):  # the tail infimum, in closed form: the first term of the tail that dips below h
            kk = np.where(w > 0, k + (k % 2 == 0), k + (k % 2 == 1))
            return h - 0.65 * np.abs(w) / kk

        for k in (1, 2, 5, 8):
            tail = np.min([f(i) for i in range(k, k + 400)], axis=0)
            assert np.abs(tail - g(k)).max() < 1e-12 and np.all(g(k) <= f(k) + 1e-12) and np.all(f(k) >= 0)
            assert np.all(g(k + 1) >= g(k) - 1e-12)
        ax = plain_axes([0, 2 * np.pi, np.pi / 2], [0, 2.6, 1], 6.0, 3.3).move_to([-3.75, -1.3, 0])
        fs = VGroup(*[polyline(ax, x, f(i), color=C.FUNC, stroke_width=1.5).set_stroke(opacity=0.5) for i in range(1, 7)])
        hl = DashedVMobject(polyline(ax, x, h, color=WHITE, stroke_width=2.5), num_dashes=60)
        kT = ValueTracker(1)
        gk = always_redraw(lambda: polyline(ax, x, g(max(1, round(kT.get_value()))), color=C.CONNECTED_SET,
                                            stroke_width=4))
        fk = always_redraw(lambda: polyline(ax, x, f(max(1, round(kT.get_value()))), color=C.FUNC, stroke_width=3))

        def readout():
            k = max(1, round(kT.get_value()))
            return MathTex(rf"k = {k}: \ \int g_k = {trap(g(k), x):.4f} \ \le \ \int f_k = {trap(f(k), x):.4f}",
                           font_size=24, color=C.CONNECTED_SET).next_to(ax, DOWN, buff=0.2)

        rdk = always_redraw(readout)
        key = VGroup(MathTex(r"f_k", font_size=24, color=C.FUNC), MathTex(r"g_k", font_size=24, color=C.CONNECTED_SET),
                     VGroup(DashedLine(ORIGIN, RIGHT * 0.45, color=WHITE, stroke_width=2.5, dash_length=0.06),
                            MathTex(r"\liminf f_n = h", font_size=24)).arrange(RIGHT, buff=0.1)
                     ).arrange(RIGHT, buff=0.45).next_to(ax, UP, buff=0.1).align_to(ax, RIGHT)
        assert abs(trap(h, x) - 2.6 * np.pi) < 1e-9
        with self.voiceover(
            "<bookmark mark='a'/> When functions don't increase, we still get an inequality. Fatou's lemma: the "
            "integral of the lower limit is at most the lower limit of the integrals. <bookmark mark='b'/> The proof "
            "takes the infimum of the tail, from the k-th function on. These infima increase to the lower limit. "
            "<bookmark mark='c'/> Each is below the k-th function, so its integral is smaller. <bookmark mark='d'/> "
            "Monotone convergence moves the limit through the integral, and the inequality survives."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), Create(ax), LaggedStart(*[Create(c_) for c_ in fs], lag_ratio=0.2), run_time=2.0)
            vo.wait_until("b")
            step(0)
            self.play(Create(hl), FadeIn(key[2]), FadeIn(gk), FadeIn(key[1]))
            self.play(kT.animate.set_value(6), run_time=3.0, rate_func=linear)
            vo.wait_until("c")
            step(1)
            self.play(kT.animate.set_value(3), FadeOut(fs), run_time=0.8)
            self.play(FadeIn(fk), FadeIn(key[0]), FadeIn(rdk))
            vo.wait_until("d")
            step(2)
            self.play(kT.animate.set_value(12), run_time=3.0, rate_func=linear)
        for m_ in (gk, fk, rdk):
            m_.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def cosines(self):
        x = np.linspace(0, 2 * np.pi, 2001)
        ax = plain_axes([0, 2 * np.pi, np.pi / 2], [0, 2.1, 0.5], 7.4, 4.0).move_to([-2.7, -0.75, 0])
        nT = ValueTracker(1)

        def fn():
            n = round(nT.get_value())
            y = 1 + np.cos(n * x)
            return VGroup(area_under(ax, x, y, C.MEASURE, 0.3), polyline(ax, x, y, color=C.FUNC, stroke_width=2.5))

        g = always_redraw(fn)
        envs = []
        for k, K in ((1, 3), (1, 10), (1, 40), (1, 200)):
            e = np.min([1 + np.cos(i * x) for i in range(k, K + 1)], axis=0)
            envs.append(e)
        env_g = [polyline(ax, x, e, color=C.CONNECTED_SET, stroke_width=3.5) for e in envs]
        env_l = [MathTex(rf"\min_{{1 \le i \le {K}}} f_i: \ \int = {trap(e, x):.3f}", font_size=28,
                         color=C.CONNECTED_SET).next_to(ax, DOWN, buff=0.15)
                 for (k, K), e in zip(((1, 3), (1, 10), (1, 40), (1, 200)), envs)]
        ints = [trap(e, x) for e in envs]
        assert all(a >= b - 1e-12 for a, b in zip(ints, ints[1:])) and ints[-1] < 0.1
        for n in (1, 5, 17):
            assert abs(trap(1 + np.cos(n * x), x) - 2 * np.pi) < 1e-6
        nl = always_redraw(lambda: MathTex(rf"f_n = 1 + \cos nx, \ n = {round(nT.get_value())}: \ \int_0^{{2\pi}} f_n = "
                                           r"2\pi", font_size=28, color=C.FUNC).next_to(ax, UP, buff=0.1))
        side = VGroup(
            label(r"for almost every $x$, \ $nx \bmod 2\pi$ is dense,", font_size=24),
            label(r"so $\cos nx$ keeps coming near $-1$:", font_size=24),
            MathTex(r"\liminf_n f_n(x) = 0 \text{ a.e.}", font_size=32, color=C.CONNECTED_SET),
            MathTex(r"0 = \int \liminf f_n < \liminf \int f_n = 2\pi", font_size=30, color=C.EPS),
            label(r"the inequality can be strict", font_size=24, color=C.PATHOLOGY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([4.0, -0.6, 0])
        for r_ in side:
            if r_.width > 5.6:
                r_.width = 5.6
        side.arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([4.0, -0.6, 0])
        side.arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([4.0, -0.6, 0])
        head = label(r"Fatou, strictly: \ $f_n = 1 + \cos nx$ on $[0, 2\pi]$", font_size=32).to_edge(UP, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Here the inequality is strict. The functions one plus cosine n x all have the same "
            "integral, two pi, <bookmark mark='b'/> but they oscillate faster and faster. <bookmark mark='c'/> Their "
            "running minimum sinks toward zero: for almost every x, the multiples of x wrap densely around the circle, "
            "so cosine of n x keeps returning close to minus one. <bookmark mark='d'/> The lower limit is zero almost "
            "everywhere, with integral zero, while the integrals themselves stay at two pi."
        ) as vo:
            self.play(FadeIn(head), Create(ax))
            vo.wait_until("a")
            self.play(FadeIn(g), FadeIn(nl))
            vo.wait_until("b")
            self.play(nT.animate.set_value(12), run_time=4.0, rate_func=linear)
            vo.wait_until("c")
            self.play(FadeOut(g), Create(env_g[0]), FadeIn(env_l[0]), FadeIn(side[:2]))
            cur, cl = env_g[0], env_l[0]
            for k in range(1, 4):
                self.play(ReplacementTransform(cur, env_g[k]), FadeTransform(cl, env_l[k]), run_time=1.2)
                cur, cl = env_g[k], env_l[k]
            vo.wait_until("d")
            self.play(FadeIn(side[2:]))
        for m in (g, nl):
            m.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def escapes(self):
        tab = VGroup(
            VGroup(label(r"", font_size=26), MathTex(r"\int \liminf f_n", font_size=30),
                   MathTex(r"\liminf \int f_n", font_size=30)),
            VGroup(label(r"the spike \ $n\mathbf 1_{(0, 1/n]}$", font_size=28), MathTex("0", font_size=32),
                   MathTex("1", font_size=32)),
            VGroup(label(r"the runaway \ $\mathbf 1_{[n, n+1]}$", font_size=28), MathTex("0", font_size=32),
                   MathTex("1", font_size=32)),
            VGroup(label(r"the spreading \ $\tfrac1n\mathbf 1_{[0, n]}$", font_size=28), MathTex("0", font_size=32),
                   MathTex("1", font_size=32)),
            VGroup(label(r"$1 + \cos nx$ \ on $[0, 2\pi]$", font_size=28), MathTex("0", font_size=32),
                   MathTex(r"2\pi", font_size=32)),
        )
        for i, row in enumerate(tab):
            y = 1.4 - 0.75 * i
            row[0].move_to([-3.2, y, 0])
            row[1].move_to([1.2, y, 0])
            row[2].move_to([4.2, y, 0])
            if i:
                row[1].set_color(C.CONNECTED_SET)
                row[2].set_color(C.MEASURE)
        head = label(r"Mass can escape in the limit; \ it can never appear", font_size=34).to_edge(UP, buff=0.4)
        out = label(r"Fatou's $\le$ is exactly the room for escaping mass; \ next: \ a lid closes it", font_size=26,
                    color=C.EPS).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "<bookmark mark='a'/> The opening's three escapes fit the same pattern. In every case the lower limit is "
            "zero, with integral zero, while the integrals stay at one. <bookmark mark='b'/> Fatou's inequality "
            "points one way only: in the limit, mass can escape, but it can never appear from nowhere. The next "
            "chapter shows how to stop it escaping."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.15) for r_ in tab[1:]], lag_ratio=0.4), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(out))
        self.wait(0.4)
        self.clear_scene()
