from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis10.common import cplot, load, phase_wheel, plain_axes, square_axes


class Spectrum(VoiceoverScene):
    def construct(self):
        self.card()
        self.nonempty()
        self.radius()
        self.volterra()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(2, r"The spectrum", r"Why is the spectrum never empty?", lit=(), part=10)
        with self.voiceover("Chapter two: the spectrum, which is never empty, and how big it is."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def nonempty(self):
        d = load("calculus")
        A, ev = d["A"], d["ev"]
        I = np.eye(6)

        def trace_res(Z):
            z = np.asarray(Z, complex).ravel()
            out = np.sum(1 / (z[:, None] - ev[None, :]), axis=1)  # tr (l - A)^-1 = sum 1/(l - l_i)
            return out.reshape(np.shape(Z))

        # the trace formula, checked at a few points against the matrix inverse
        for l_ in (2.0 + 1j, -0.3 - 1.7j, 2.5j):
            assert abs(np.trace(np.linalg.inv(l_ * I - A)) - trace_res(np.array([l_]))[0]) < 1e-10
        cx = square_axes([-3, 3, 1], [-2.2, 2.2, 1], 1.05).move_to([-3.4, -0.3, 0])
        img = cplot(cx, trace_res, (-3, 3), (-2.2, 2.2), px=720)
        evd = VGroup(*[Dot(cx.c2p(l_.real, l_.imag), radius=0.05, color=WHITE) for l_ in ev])
        nrm = np.linalg.norm(A, 2)
        nc = DashedVMobject(Circle(radius=nrm * (cx.c2p(1, 0)[0] - cx.c2p(0, 0)[0]), color=C.EPS, stroke_width=2.5).move_to(
            cx.c2p(0, 0)), num_dashes=50)
        ncl = MathTex(rf"|\lambda| = \|A\| = {nrm:.3f}", font_size=22, color=C.EPS).next_to(cx, DOWN, buff=0.1)
        wheel = phase_wheel(0.3).next_to(cx, LEFT, buff=0.15).shift(DOWN * 0.5)
        tl = MathTex(r"\operatorname{tr}(\lambda - A)^{-1}", font_size=24).next_to(cx, UP, buff=0.08)
        assert np.abs(ev).max() <= nrm + 1e-12
        pm = ProofMap([
            r"$|\lambda| > \|x\|$: \ $x - \lambda e = -\lambda(e - x/\lambda)$ is invertible",
            r"invertibles are open: \ $\sigma(x)$ is closed, \ so compact",
            r"$\lambda \mapsto \Lambda\big((x - \lambda e)^{-1}\big)$ is holomorphic off $\sigma(x)$, \ $\to 0$ at $\infty$",
            r"if $\sigma(x) = \varnothing$: \ entire and bounded, \ so $0$ (Liouville, Part 7)",
            r"for every $\Lambda$: \ so $(x - \lambda e)^{-1} = 0$ (Hahn--Banach): \ absurd",
        ], font_size=20, width=6.2, buff=0.12, direction=DOWN).move_to([3.6, -0.15, 0])
        cor = label(r"\textbf{Gelfand--Mazur} \ a Banach algebra in which every $x \ne 0$ is invertible is $\mathbb C$",
                    font_size=22, color=C.EPS).to_edge(DOWN, buff=0.2)
        head = label(r"\textbf{RCA 18.5} \ the spectrum is compact and never empty", font_size=32).to_edge(UP, buff=0.25)
        with self.voiceover(
            "<bookmark mark='a'/> For a six by six matrix, here's the trace of the resolvent, lambda minus A "
            "inverse, colored by phase. It's holomorphic except at the eigenvalues, where it has poles. "
            "<bookmark mark='b'/> In any Banach algebra the same is true. Outside the circle of radius the norm of x, "
            "the Neumann series inverts x minus lambda, and the invertibles are open, so the spectrum is closed and "
            "bounded. <bookmark mark='c'/> And it's never empty: if it were, every functional of the resolvent "
            "would be an entire function going to zero at infinity, so zero, by Liouville's theorem, and then "
            "Hahn-Banach makes the resolvent itself zero, which is absurd. <bookmark mark='d'/> A corollary: a "
            "Banach algebra where every nonzero element is invertible is just the complex numbers."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), FadeIn(img), Create(cx), FadeIn(tl), FadeIn(wheel))
            self.play(LaggedStart(*[FadeIn(d_, scale=2) for d_ in evd], lag_ratio=0.2))
            vo.wait_until("b")
            self.play(FadeIn(pm), Create(nc), FadeIn(ncl))
            self.play(*pm.light(0))
            self.play(*pm.light(1))
            vo.wait_until("c")
            for i in (2, 3, 4):
                self.play(*pm.light(i), run_time=0.9)
            vo.wait_until("d")
            self.play(*pm.done(), FadeIn(cor))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def radius(self):
        d = load("radius")
        curves, ratio = d["curves"], d["ratio"]
        n = np.arange(1, 1001, 5)
        ax = plain_axes([0, 3, 1], [0.9, 1.8, 0.2], 6.4, 3.6, numbers=True, font_size=18,
                        x_axis_config={"decimal_number_config": {"num_decimal_places": 0}},
                        y_axis_config={"decimal_number_config": {"num_decimal_places": 1}}).move_to([-3.1, -0.5, 0])
        xl = MathTex(r"\log_{10} n", font_size=22).next_to(ax.x_axis, DOWN, buff=0.35)
        yl = MathTex(r"\|A^n\|^{1/n} \big/ \max|\lambda_i|", font_size=24).next_to(ax, UP, buff=0.1)
        cols = [C.OPERATOR, C.SEQ, C.APPROX, C.FREQ, C.TEST_FN, C.EPS, C.MEASURE, C.INNER, C.SPECTRUM, GREY_A]
        gs = VGroup(*[polyline_(ax, np.log10(n), np.minimum(c_, 1.8), col) for c_, col in zip(curves, cols)])
        one = DashedLine(ax.c2p(0, 1), ax.c2p(3, 1), color=WHITE, stroke_width=2)
        assert np.all(np.abs(ratio[:, -1] - 1) < 0.01)
        lad = VGroup(
            MathTex(r"(x - \lambda e)^{-1} = -\sum_{n \ge 0} \frac{x^n}{\lambda^{n+1}}", font_size=30),
            label(r"a Laurent series in $1/\lambda$: \ it converges outside the smallest circle that holds $\sigma(x)$",
                  font_size=22, color=GREY_A),
            label(r"its radius, \ by Part 2's root test:", font_size=24),
            MathTex(r"\rho(x) = \max_{\lambda \in \sigma(x)}|\lambda| = \lim_{n \to \infty}\|x^n\|^{1/n}", font_size=32,
                    color=C.EPS),
            label(r"\textbf{RCA 18.9} \ (Gelfand's spectral radius formula)", font_size=22),
            MathTex(r"\text{10 random } 8 \times 8: \ " + r",\ ".join(f"{r:.3f}" for r in ratio[:3, -1]) +
                    r", \ldots \ \text{at } n = 1000", font_size=22, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to([3.6, -0.2, 0])
        for r_ in lad:
            if r_.width > 6.4:
                r_.width = 6.4
        head = label(r"How big is the spectrum?", font_size=34).to_edge(UP, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Expand the resolvent in powers of one over lambda. That's a Laurent series, Part "
            "7's tool, and it converges exactly outside the smallest circle that contains the spectrum. "
            "<bookmark mark='b'/> By the root test from Part 2, its radius is the limit of the n-th root of the "
            "norm of x to the n. That's Gelfand's spectral radius formula: a purely algebraic, metric quantity "
            "equals the size of the spectrum. <bookmark mark='c'/> For ten random matrices, the n-th roots start "
            "well above the largest eigenvalue, and settle onto it, within a tenth of a percent by n equal to a "
            "thousand."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), FadeIn(lad[:2]))
            vo.wait_until("b")
            self.play(FadeIn(lad[2:5]))
            vo.wait_until("c")
            self.play(Create(ax), FadeIn(xl), FadeIn(yl), Create(one))
            self.play(LaggedStart(*[Create(g) for g in gs], lag_ratio=0.15), run_time=3.0)
            self.play(FadeIn(lad[5]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def volterra(self):
        d = load("radius")
        ns, vn, nf, roots = d["ns"], d["vn"], d["nf"], d["roots"]
        ax = plain_axes([0, 21, 5], [0, 0.7, 0.2], 6.2, 3.4, numbers=True, font_size=18,
                        x_axis_config={"decimal_number_config": {"num_decimal_places": 0}},
                        y_axis_config={"decimal_number_config": {"num_decimal_places": 1}}).move_to([-3.2, -0.4, 0])
        xl = MathTex(r"n", font_size=22).next_to(ax.x_axis, RIGHT, buff=0.1)
        d1 = VGroup(*[Dot(ax.c2p(n, r), radius=0.06, color=C.OPERATOR) for n, r in zip(ns, roots)])
        d2 = VGroup(*[Dot(ax.c2p(n, v), radius=0.06, color=C.EPS) for n, v in zip(ns, nf)])
        half = DashedLine(ax.c2p(0, 0.5), ax.c2p(21, 0.5), color=C.EPS, stroke_width=2)
        l1 = MathTex(r"\|V^n\|^{1/n} \to 0", font_size=26, color=C.OPERATOR).next_to(ax.c2p(14, 0.18), UP, buff=0.25)
        l2 = MathTex(r"n!\,\|V^n\| \to \tfrac12", font_size=26, color=C.EPS).next_to(ax.c2p(14, 0.5), UP, buff=0.12)
        assert abs(vn[0] - 2 / math.pi) < 1e-5 and abs(nf[-1] - 0.5) < 0.01 and np.all(np.diff(roots) < 0)
        rows = VGroup(
            MathTex(r"Vf(x) = \int_0^x f(t)\,dt \ \text{ on } L^2[0, 1]", font_size=30, color=C.OPERATOR),
            MathTex(rf"\|V\| = {vn[0]:.5f} = \tfrac{{2}}{{\pi}} \ \ (\text{{Part 8}})", font_size=26),
            MathTex(r"V^n f(x) = \int_0^x \frac{(x - t)^{n-1}}{(n-1)!} f(t)\,dt", font_size=28),
            MathTex(rf"\|V^{{20}}\| = {sci(vn[-1], 2)}, \quad n!\,\|V^n\| = " + r",\ ".join(f"{v:.3f}" for v in nf[[0, 3, 5, 8]]),
                    font_size=22, color=GREY_A),
            label(r"so $\rho(V) = 0$ and $\sigma(V) = \{0\}$", font_size=26, color=C.SPECTRUM),
            label(r"yet $0$ is not an eigenvalue: \ $Vf = 0 \Rightarrow f = (Vf)' = 0$", font_size=24),
            label(r"a nonzero operator whose spectrum is a single point, \ with no eigenvector", font_size=22,
                  color=C.PATHOLOGY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([3.6, -0.3, 0])
        for r_ in rows:
            if r_.width > 6.6:
                r_.width = 6.6
        head = label(r"The museum: \ the Volterra operator", font_size=34).to_edge(UP, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Part 8's Volterra operator integrates from zero. Its norm is two over pi. "
            "<bookmark mark='b'/> Its powers are repeated integrals, with kernel x minus t to the n minus one over "
            "n minus one factorial, and their norms collapse like one over n factorial: n factorial times the norm "
            "tends to one half. <bookmark mark='c'/> So the n-th roots go to zero, and by Gelfand's formula the "
            "spectrum is the single point zero. <bookmark mark='d'/> Yet zero isn't an eigenvalue, because if V f "
            "vanishes, so does its derivative, which is f. A nonzero operator, a one-point spectrum, and no "
            "eigenvector at all."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), FadeIn(rows[:2]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2:4]), Create(ax), FadeIn(xl), Create(half))
            self.play(LaggedStart(*[FadeIn(d_, scale=0.5) for d_ in d2], lag_ratio=0.15), FadeIn(l2), run_time=1.8)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(d_, scale=0.5) for d_ in d1], lag_ratio=0.15), FadeIn(l1), run_time=1.8)
            self.play(FadeIn(rows[4]))
            vo.wait_until("d")
            self.play(FadeIn(rows[5:]))
        self.wait(0.4)
        self.clear_scene()


def polyline_(ax, xs, ys, color, stroke_width=2.5):
    m = VMobject(color=color, stroke_width=stroke_width)
    m.set_points_as_corners([ax.c2p(float(a), float(b)) for a, b in zip(xs, ys)])
    return m
