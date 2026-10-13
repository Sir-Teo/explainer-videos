from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis7.common import load, square_axes, trap, zcurve


class Integration(VoiceoverScene):
    def construct(self):
        self.card()
        self.powers()
        self.winding()
        self.goursat()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(2, r"Path integrals and winding numbers", r"How many times does a curve go around a point?",
                            lit=(), part=7)
        with self.voiceover("Chapter two: integrals along paths, and the number that counts turns."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def powers(self):
        ax = square_axes([-1.6, 1.6, 1], [-1.6, 1.6, 1], 1.45).move_to([-3.8, -0.6, 0])
        ax.set_opacity(0.4)
        th = np.linspace(0, 2 * np.pi, 400)
        circ = zcurve(ax, np.exp(1j * th), C.EPS, 3.5)
        arrows = VGroup(*[Arrow(ax.c2p(math.cos(a), math.sin(a)), ax.c2p(math.cos(a + 0.25), math.sin(a + 0.25)),
                                buff=0, color=C.EPS, stroke_width=4, tip_length=0.16) for a in (0.4, 2.5, 4.6)])
        g_l = MathTex(r"\gamma(t) = e^{it}, \ 0 \le t \le 2\pi", font_size=26, color=C.EPS).next_to(ax, DOWN, buff=0.15)
        t = np.linspace(0, 2 * np.pi, 4097)[:-1]
        z = np.exp(1j * t)
        rows = VGroup(MathTex(r"n", r"\quad \oint_\gamma z^n\,dz", font_size=28, color=GREY_A))
        vals = {}
        for n in (-3, -2, -1, 0, 1, 2):
            v = np.sum(z**n * 1j * z) * (2 * np.pi / len(t))
            vals[n] = v
            txt = r"2\pi i" if n == -1 else "0"
            rows.add(MathTex(f"{n}", rf"\quad {txt}", font_size=30, color=C.EPS if n == -1 else WHITE))
        assert abs(vals[-1] - 2j * np.pi) < 1e-12 and all(abs(vals[n]) < 1e-12 for n in vals if n != -1)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([0.6, -0.6, 0])
        for r_ in rows[1:]:
            r_[1].align_to(rows[0][1], LEFT)
        defs = VGroup(
            MathTex(r"\int_\gamma f(z)\,dz = \int_a^b f(\gamma(t))\,\gamma'(t)\,dt", font_size=30),
            label(r"\textbf{RCA 10.8}", font_size=22, color=GREY_B),
            label(r"$z^n$ for $n \ne -1$ has an antiderivative \ $\frac{z^{n+1}}{n+1}$:", font_size=22, color=GREY_A),
            label(r"around a closed path its integral is $0$", font_size=22, color=GREY_A),
            label(r"$\frac1z$ has none on $\C \setminus \{0\}$: \ \emph{that} is the log's $2\pi i$", font_size=22,
                  color=C.EPS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([4.6, -0.6, 0])
        for r_ in defs:
            if r_.width > 4.6:
                r_.width = 4.6
        defs.arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([4.65, -0.6, 0])
        head = label(r"Integrate around the unit circle", font_size=34).to_edge(UP, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> To integrate along a path, parametrize it and integrate f of gamma times gamma "
            "prime. <bookmark mark='b'/> Around the unit circle, the powers of z all give zero, except one. "
            "<bookmark mark='c'/> One over z gives two pi i. <bookmark mark='d'/> Every other power has an "
            "antiderivative, and around a closed path an antiderivative returns to where it started. One over z "
            "would need a logarithm, and no single-valued logarithm exists around the origin. Those two pi i's are "
            "the whole story of this part."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), FadeIn(defs[:2]), Create(ax), Create(circ), FadeIn(arrows), FadeIn(g_l))
            vo.wait_until("b")
            self.play(FadeIn(rows[0]))
            self.play(LaggedStart(*[FadeIn(rows[i]) for i in (1, 2, 4, 5, 6)], lag_ratio=0.3), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(rows[3], scale=1.2))
            vo.wait_until("d")
            self.play(FadeIn(defs[2:4]))
            self.play(FadeIn(defs[4]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def winding(self):
        d = load("winding")
        z, pts, w = d["z"], d["pts"], d["w"]
        ax = square_axes([-2.1, 2.1, 1], [-2.1, 2.1, 1], 1.4).move_to([-3.3, -0.55, 0])
        ax.set_opacity(0.3)
        curve = zcurve(ax, z, WHITE, 3, closed=True)
        cols = {0: GREY_B, 1: C.SEQ, 2: C.MEASURE}
        dots = VGroup(*[Dot(ax.c2p(p.real, p.imag), radius=0.07, color=cols[int(k)]) for p, k in zip(pts, w)])
        nums = VGroup(*[MathTex(str(int(k)), font_size=22, color=cols[int(k)]).next_to(ax.c2p(p.real, p.imag), UR,
                                                                                       buff=0.09)
                        for p, k in zip(pts, w)])
        # one point, the turning arrow
        a = complex(pts[list(w).index(2)])
        tT = ValueTracker(0.0)
        zz = np.asarray(z)
        ang = np.unwrap(np.angle(zz - a))

        def arrow():
            i = int(tT.get_value() * (len(zz) - 1))
            return VGroup(Line(ax.c2p(a.real, a.imag), ax.c2p(zz[i].real, zz[i].imag), color=C.EPS, stroke_width=3),
                          Dot(ax.c2p(zz[i].real, zz[i].imag), radius=0.07, color=C.EPS))

        arr = always_redraw(arrow)
        turn = always_redraw(lambda: MathTex(
            rf"\text{{turned: }} {(ang[int(tT.get_value() * (len(zz) - 1))] - ang[0]) / (2 * np.pi):.2f} \text{{ turns}}",
            font_size=28, color=C.EPS).move_to([3.4, 1.6, 0]))
        assert abs((ang[-1] - ang[0]) / (2 * np.pi) - 2) < 1e-6
        side = VGroup(
            MathTex(r"\mathrm{Ind}_\gamma(a) = \frac{1}{2\pi i}\oint_\gamma \frac{dz}{z - a}", font_size=32),
            label(r"\textbf{RCA 10.10} \ an integer, \ constant on each", font_size=24),
            label(r"component of the complement, \ $0$ outside", font_size=24),
            MathTex(rf"\text{{{len(pts)} points, from the integral: }} |\mathrm{{Ind}} - \text{{integer}}| < 10^{{-4}}",
                    font_size=24, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to([3.5, -0.9, 0])
        for r_ in side:
            if r_.width > 6.0:
                r_.width = 6.0
        side.arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to([3.5, -0.9, 0])
        assert set(int(k) for k in w) == {0, 1, 2} and len(pts) == 20
        head = label(r"The winding number: \ an integral that counts turns", font_size=34).to_edge(UP, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Divide by two pi i, shift the singularity to a point a, and the integral of one "
            "over z minus a counts how many times the curve winds around a. <bookmark mark='b'/> Follow an arrow "
            "from a point inside the small loop to the moving point of the curve. By the time the curve closes, the "
            "arrow has turned exactly twice. <bookmark mark='c'/> Compute the integral at twenty points: every "
            "answer is an integer, zero, one or two, constant on each piece of the complement, and zero outside the "
            "curve."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), Create(ax), Create(curve), FadeIn(side[0]))
            vo.wait_until("b")
            self.add(arr, turn)
            self.play(tT.animate.set_value(1.0), run_time=5.0, rate_func=linear)
            vo.wait_until("c")
            self.remove(arr, turn)
            arr.clear_updaters()
            turn.clear_updaters()
            self.play(LaggedStart(*[AnimationGroup(FadeIn(dt), FadeIn(n_)) for dt, n_ in zip(dots, nums)],
                                  lag_ratio=0.08), run_time=2.5)
            self.play(FadeIn(side[1:]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def goursat(self):
        d = load("goursat")
        tris, z0, eps, ratio_bad = d["tris"], complex(d["z0"]), d["eps"], d["ratio_bad"]
        ax = square_axes([-0.05, 1.05, 0.5], [-0.05, 0.95, 0.5], 5.0).move_to([-3.6, -0.65, 0])
        ax.set_opacity(0.0)
        polys = [Polygon(*[ax.c2p(v.real, v.imag) for v in T], stroke_color=interpolate_color(
            ManimColor(C.SEQ), ManimColor(C.EPS), min(1, k / 6)), stroke_width=3 if k < 5 else 2,
            fill_opacity=0.08, fill_color=C.EPS) for k, T in enumerate(tris)]
        mids = []
        for T in tris[:-1]:
            m = [(T[0] + T[1]) / 2, (T[1] + T[2]) / 2, (T[2] + T[0]) / 2]
            mids.append(Polygon(*[ax.c2p(v.real, v.imag) for v in m], stroke_color=GREY_C, stroke_width=1.5))
        z0d = Dot(ax.c2p(z0.real, z0.imag), radius=0.05, color=WHITE)
        tab = VGroup(MathTex(r"n", r"\ \ \varepsilon_n", r"\ \ \frac{|\oint_{\Delta_n} \bar z\,dz|}{d_n p_n}", font_size=26,
                             color=GREY_A))
        for n in range(8):
            tab.add(MathTex(f"{n}", rf"\ \ {sci(float(eps[n]), 2)}", rf"\ \ {ratio_bad[n]:.4f}", font_size=24))
        tab.arrange(DOWN, aligned_edge=LEFT, buff=0.08).move_to([1.5, -0.9, 0])
        regrid(tab)
        for row in tab[1:]:
            row[1].set_color(C.EPS)
            row[2].set_color(C.PATHOLOGY)
        side = VGroup(
            label(r"$f$ holomorphic at $z_0$:", font_size=24),
            MathTex(r"f(z) = f(z_0) + f'(z_0)(z - z_0) + \varepsilon_n |z - z_0|", font_size=24),
            label(r"the linear part integrates to $0$, so", font_size=22, color=GREY_A),
            MathTex(r"\Big|\oint_{\Delta_n} f\Big| \le \varepsilon_n d_n p_n = \varepsilon_n 4^{-n} d p", font_size=26,
                    color=C.EPS),
            label(r"while bisection keeps \ $|\oint_{\Delta_n}| \ge 4^{-n}|\oint_\Delta|$:", font_size=22, color=GREY_A),
            label(r"so $\oint_\Delta f = 0$", font_size=26, color=C.EPS),
            label(r"$\bar z$ is not holomorphic: \ its ratio never drops", font_size=22, color=C.PATHOLOGY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([5.0, -0.8, 0])
        for r_ in side:
            if r_.width > 3.9:
                r_.width = 3.9
        side.arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([5.05, -0.8, 0])
        assert np.all(np.diff(eps) < 0) and np.allclose(ratio_bad, ratio_bad[0], rtol=1e-6)
        head = VGroup(label(r"\textbf{RCA 10.13} \ (Cauchy--Goursat) \ $\oint_{\partial\Delta} f\,dz = 0$ \ for $f$ "
                            r"holomorphic on a triangle", font_size=28),
                      label(r"the proof is bisection, \ the fourth time in this series", font_size=24, color=GREY_A)
                      ).arrange(DOWN, buff=0.08).to_edge(UP, buff=0.2)
        with self.voiceover(
            "<bookmark mark='a'/> Cauchy's theorem starts with triangles, and Goursat's proof is bisection, the "
            "fourth time in this series that halving has proved a theorem. <bookmark mark='b'/> Cut the triangle "
            "into four by its midpoints. The four boundary integrals add up to the whole, so one of them is at least "
            "a quarter of it. Keep that one, and repeat: the triangles shrink to a point z zero. "
            "<bookmark mark='c'/> Near z zero, f is linear plus a small error, and the linear part integrates to zero "
            "around any closed path. So the n-th integral is at most epsilon n times four to the minus n, with "
            "epsilon n going to zero, here for the exponential. <bookmark mark='d'/> But bisection kept at least four "
            "to the minus n of the original. The only way out: the original integral was zero. For z bar, which "
            "isn't holomorphic, the corresponding ratio stays fixed, and the argument fails, as it must. Rudin "
            "extends this from triangles to every convex set."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), Create(polys[0]))
            vo.wait_until("b")
            for k in range(6):
                self.play(Create(mids[k]), run_time=0.5)
                self.play(FadeIn(polys[k + 1]), mids[k].animate.set_stroke(opacity=0.3), run_time=0.5)
            self.play(FadeIn(z0d))
            vo.wait_until("c")
            self.play(FadeIn(side[:4]), FadeIn(tab[0]))
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[1:]], lag_ratio=0.2), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(side[4:]))
        self.wait(0.4)
        self.clear_scene()
