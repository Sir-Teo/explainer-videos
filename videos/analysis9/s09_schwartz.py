from __future__ import annotations

import math

import numpy as np
from numpy.polynomial.hermite import hermval

from explainer.analysis import *  # noqa: F403
from videos.analysis9.common import SQ2PI, load, plain_axes, polyline, trap


def fft_hat(f, L=40.0, N=1 << 13):
    """Rudin's transform of the samples f(x) on the periodic grid x in [-L/2, L/2): returns (x, t, f^(t))."""
    x = (np.arange(N) - N / 2) * (L / N)
    F = np.fft.fftshift(np.fft.fft(np.fft.ifftshift(f(x)))) * (L / N) / SQ2PI
    t = np.fft.fftshift(np.fft.fftfreq(N, L / N)) * 2 * math.pi
    return x, t, F


class Schwartz(VoiceoverScene):
    def construct(self):
        self.card()
        self.rapid()
        self.quarter()
        self.tempered()
        self.poisson()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(8, r"Tempered distributions", r"Can every distribution be transformed?", lit=(1945,), part=9)
        with self.voiceover("Chapter eight: the space where the Fourier transform is perfect, and its dual."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def rapid(self):
        ax = plain_axes([-6, 6, 2], [0, 1.3, 0.5], 6.0, 2.6).move_to([-3.3, 1.1, 0])
        bx = plain_axes([-6, 6, 2], [0, 4.2, 1], 6.0, 2.6).move_to([3.4, 1.1, 0])
        x = np.linspace(-6, 6, 1201)
        cols = [C.FUNC, C.SEQ, C.APPROX, C.EPS]
        ga = VGroup(*[polyline(ax, x, np.abs(x) ** k * np.exp(-x * x / 2), color=c, stroke_width=3)
                      for k, c in zip(range(4), cols)])
        gb = VGroup(*[runs(bx, x, np.abs(x) ** k / (1 + x * x), c, 3) for k, c in zip(range(4), cols)])
        la = MathTex(r"|x|^k e^{-x^2/2}, \ \ k = 0, 1, 2, 3", font_size=26).next_to(ax, UP, buff=0.12)
        lb = MathTex(r"|x|^k \big/ (1 + x^2), \ \ k = 0, 1, 2, 3", font_size=26).next_to(bx, UP, buff=0.12)
        ok = label(r"in $\mathcal S$: \ every $x^k f$ stays bounded", font_size=22, color=C.TEST_FN).next_to(ax, DOWN,
                                                                                                           buff=0.12)
        no = label(r"smooth and integrable, \ but not in $\mathcal S$", font_size=22, color=C.PATHOLOGY).next_to(
            bx, DOWN, buff=0.12)
        # the seminorms of the Gaussian: sup |x^k e^(-x^2/2)| = (k/e)^(k/2), attained at x = sqrt k
        xx = np.linspace(0, 12, 1200001)
        sups = [float(np.max(xx**k * np.exp(-xx * xx / 2))) for k in range(0, 9, 2)]
        exact = [(k / math.e) ** (k / 2) if k else 1.0 for k in range(0, 9, 2)]
        assert np.allclose(sups, exact, rtol=1e-9)
        semis = MathTex(r"\sup_x |x^k e^{-x^2/2}| = (k/e)^{k/2}: \ \ " + r",\ ".join(f"{s:.3f}" for s in sups) +
                        r" \ \ (k = 0, 2, \ldots, 8)", font_size=24)
        rows = VGroup(
            label(r"\textbf{FA 7.3} \ $\mathcal S$: \ smooth $f$ with $\sup_x (1 + x^2)^N |f^{(m)}(x)| < \infty$ "
                  r"for all $N, m$", font_size=24),
            semis,
            label(r"countably many seminorms: \ a Fr\'echet space \ (Part 8)", font_size=22, color=GREY_A),
        ).arrange(DOWN, buff=0.12).to_edge(DOWN, buff=0.35)
        rows[1].set_color(C.EPS)
        head = label(r"Rapidly decreasing functions", font_size=34).to_edge(UP, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Test functions with compact support are too few for the Fourier transform, because "
            "the transform of a bump never has compact support. So Schwartz enlarged the space: smooth functions "
            "that, with all their derivatives, decay faster than every power of x. <bookmark mark='b'/> The Gaussian "
            "qualifies: multiply it by x to any power and it stays bounded, with sup exactly k over e, to the power "
            "k over two. <bookmark mark='c'/> One over one plus x squared is smooth and integrable, but x squared "
            "times it never decays, so it's out. <bookmark mark='d'/> Countably many seminorms again: the Schwartz "
            "space is a Fréchet space."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(ax), FadeIn(la))
            self.play(LaggedStart(*[Create(g) for g in ga], lag_ratio=0.4), run_time=2.4)
            self.play(FadeIn(ok), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(bx), FadeIn(lb))
            self.play(LaggedStart(*[Create(g) for g in gb], lag_ratio=0.4), run_time=2.4)
            self.play(FadeIn(no))
            vo.wait_until("d")
            self.play(FadeIn(rows[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def quarter(self):
        def f(x):
            return (1 + 1.2 * x) * np.exp(-((x - 0.6) ** 2))

        # transform on a grid whose x and t spacings agree (L^2 = 2 pi N), so the DFT can be applied twice
        N = 1 << 13
        Ls = math.sqrt(2 * math.pi * N)
        xs = (np.arange(N) - N / 2) * (Ls / N)

        def dft(v):
            return np.fft.fftshift(np.fft.fft(np.fft.ifftshift(v))) * (Ls / N) / SQ2PI

        v1 = dft(f(xs))
        v2 = dft(v1)
        v4 = dft(dft(v2))
        e2 = np.abs(v2 - f(-xs)).max()
        e4 = np.abs(v4 - f(xs)).max()
        assert e2 < 1e-12 and e4 < 1e-12
        m = np.abs(xs) <= 4
        pos = [RIGHT * 4.0, UP * 1.55, LEFT * 4.0, DOWN * 1.85]
        names = [r"f", r"\hat f", r"f(-x)", r"\hat f(-t)"]
        data = [f(xs), v1, v2, dft(v2)]
        cols = [C.FUNC, C.FREQ, C.FUNC, C.FREQ]
        panels = VGroup()
        for p_, nm, v, c in zip(pos, names, data, cols):
            a = plain_axes([-4, 4, 2], [-1.0, 2.0, 1], 3.0, 1.35).move_to(p_ + DOWN * 0.25)
            g = VGroup(polyline(a, xs[m], v[m].real, color=c, stroke_width=3))
            if np.abs(v[m].imag).max() > 1e-6:
                g.add(DashedVMobject(polyline(a, xs[m], v[m].imag, color=c, stroke_width=2.5), num_dashes=40))
            lab = MathTex(nm, font_size=28, color=c).next_to(a, UP, buff=0.05)
            panels.add(VGroup(a, g, lab))
        ring = VGroup()
        for k in range(4):
            a0 = panels[k][0].get_center()
            a1 = panels[(k + 1) % 4][0].get_center()
            arc = ArcBetweenPoints(a0 + (a1 - a0) * 0.32, a0 + (a1 - a0) * 0.68, angle=PI / 4, color=C.OPERATOR,
                                   stroke_width=3)
            arc.add_tip(tip_length=0.15)
            ring.add(VGroup(arc, MathTex(r"\mathcal F", font_size=26, color=C.OPERATOR).move_to(
                arc.point_from_proportion(0.5) + 0.32 * normalize(arc.point_from_proportion(0.5) - DOWN * 0.25))))
        key = label(r"solid: real part, \ dashed: imaginary part", font_size=18, color=GREY_B)
        mid = VGroup(MathTex(r"\mathcal F^2 f = f(-x)", font_size=28), MathTex(r"\mathcal F^4 = I", font_size=28),
                     MathTex(rf"\text{{DFT check: }} {sci(max(e2, e4), 0)}", font_size=20, color=GREY_A)).arrange(
            DOWN, buff=0.12).move_to(DOWN * 0.25)
        # Hermite functions are the eigenvectors: F h_n = (-i)^n h_n
        herr = []
        for n in range(4):
            h = hermval(xs, [0] * n + [1]) * np.exp(-xs * xs / 2)
            herr.append(np.abs(dft(h) - (-1j) ** n * h).max() / np.abs(h).max())
        assert max(herr) < 1e-12
        rows = VGroup(
            label(r"\textbf{FA 7.7} \ $\mathcal F$ maps $\mathcal S$ onto $\mathcal S$, \ continuously, \ with inverse "
                  r"$\mathcal F^3$", font_size=24),
            label(r"because $\mathcal F(xf) = i(\hat f)'$ \ and \ $\mathcal F(f') = it\hat f$: \ decay $\leftrightarrow$ "
                  r"smoothness", font_size=22, color=GREY_A),
            label(r"eigenvalues $1, -i, -1, i$: \ the Hermite functions, \ $\mathcal F h_n = (-i)^n h_n$ \ "
                  rf"(error ${sci(max(herr), 0)}$)", font_size=22, color=C.SPECTRUM),
        ).arrange(DOWN, buff=0.1).to_edge(DOWN, buff=0.2)
        key.next_to(rows, UP, buff=0.15).to_edge(LEFT, buff=0.4)
        head = label(r"The transform is a quarter turn", font_size=34).to_edge(UP, buff=0.25)
        panels.shift(UP * 0.35)
        ring.shift(UP * 0.35)
        mid.shift(UP * 0.35)
        with self.voiceover(
            "<bookmark mark='a'/> On this space the transform is perfect. Multiplying by x becomes differentiating, "
            "and differentiating becomes multiplying, so decay and smoothness trade places, and the Schwartz space "
            "maps onto itself. <bookmark mark='b'/> Watch a lopsided function go around. Its transform is complex. "
            "Transform again, and you get the function reflected. <bookmark mark='c'/> Four times, and you're back: "
            "the Fourier transform is a quarter turn. <bookmark mark='d'/> So its only eigenvalues are the fourth "
            "roots of unity, and the eigenvectors are the Hermite functions, the quantum oscillator's states."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), FadeIn(rows[:2]))
            vo.wait_until("b")
            self.play(Create(panels[0][0]), Create(panels[0][1]), FadeIn(panels[0][2]))
            for k in range(1, 3):
                self.play(Create(ring[k - 1]), Create(panels[k][0]), Create(panels[k][1]), FadeIn(panels[k][2]),
                          run_time=1.1)
            self.play(FadeIn(key), FadeIn(mid[0]))
            vo.wait_until("c")
            self.play(Create(ring[2]), Create(panels[3][0]), Create(panels[3][1]), FadeIn(panels[3][2]), run_time=1.1)
            self.play(Create(ring[3]), FadeIn(mid[1:]))
            vo.wait_until("d")
            self.play(FadeIn(rows[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def tempered(self):
        ax = plain_axes([-3, 3, 1], [0, 5.0, 1], 5.4, 2.8).move_to([-3.5, 0.7, 0])
        bx = plain_axes([-12, 12, 4], [0, 0.6, 0.2], 5.4, 2.8, numbers=True, font_size=16,
                        x_axis_config={"decimal_number_config": {"num_decimal_places": 0}},
                        y_axis_config={"decimal_number_config": {"num_decimal_places": 1}}).move_to([3.4, 0.7, 0])
        sT = ValueTracker(0.8)
        x = np.linspace(-3, 3, 1201)
        t = np.linspace(-12, 12, 1201)

        def pics():
            s = sT.get_value()
            g = np.exp(-x * x / (2 * s * s)) / (s * SQ2PI)
            gh = np.exp(-s * s * t * t / 2) / SQ2PI
            return VGroup(runs(ax, x, g, C.DISTRIBUTION, 3.5), polyline(bx, t, gh, color=C.FREQ, stroke_width=3.5))

        pp = always_redraw(pics)
        flat = DashedLine(bx.c2p(-12, 1 / SQ2PI), bx.c2p(12, 1 / SQ2PI), color=GREY_B, stroke_width=2)
        fl = MathTex(r"\tfrac{1}{\sqrt{2\pi}}", font_size=24, color=GREY_B).next_to(bx.c2p(12, 1 / SQ2PI), UP, buff=0.08)
        rd = always_redraw(lambda: MathTex(rf"\rho_\sigma = \tfrac{{1}}{{\sigma\sqrt{{2\pi}}}}e^{{-x^2/2\sigma^2}}, \ \ "
                                           rf"\sigma = {sT.get_value():.3f}", font_size=26,
                                           color=C.DISTRIBUTION).next_to(ax, UP, buff=0.1))
        l2 = MathTex(r"\hat\rho_\sigma(t) = \tfrac{1}{\sqrt{2\pi}}e^{-\sigma^2 t^2/2} \ \to \ \hat\delta = "
                     r"\tfrac{1}{\sqrt{2\pi}}", font_size=26, color=C.FREQ).next_to(bx, UP, buff=0.1)
        # the multiplication formula, int f^ g = int f g^, on f = Gaussian and g = the box
        xx = np.linspace(-40, 40, 800001)
        lhs = SQ2PI * math.erf(1 / math.sqrt(2))  # int_{-1}^{1} e^(-t^2/2) dt
        with np.errstate(invalid="ignore", divide="ignore"):
            sinc = np.where(xx == 0, 1.0, np.sin(xx) / np.where(xx == 0, 1, xx))
        rhs = trap(np.exp(-xx * xx / 2) * math.sqrt(2 / math.pi) * sinc, xx)
        assert abs(lhs - rhs) < 1e-6
        rows = VGroup(
            label(r"\textbf{FA 7.11} \ $\mathcal S'$: \ continuous linear functionals on $\mathcal S$", font_size=24),
            MathTex(r"\langle \hat T, \varphi\rangle = \langle T, \hat\varphi\rangle \qquad \text{because } \int \hat f g = "
                    rf"\int f\hat g \ \ ({lhs:.6f} = {rhs:.6f})", font_size=24, color=C.EPS),
            label(r"in $\mathcal S'$: \ $L^p$, \ polynomials, \ $\delta$ and its derivatives, \ combs; \ "
                  r"not $e^x$ \ (too big)", font_size=22, color=GREY_A),
            MathTex(r"\hat\delta = \tfrac{1}{\sqrt{2\pi}}, \qquad \hat 1 = \sqrt{2\pi}\,\delta, \qquad \widehat{x^n} = "
                    r"i^n\sqrt{2\pi}\,\delta^{(n)}", font_size=28, color=C.DISTRIBUTION),
        ).arrange(DOWN, buff=0.14).to_edge(DOWN, buff=0.3)
        head = label(r"Transforming distributions, \ by duality", font_size=34).to_edge(UP, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> The dual of the Schwartz space is the space of tempered distributions: everything "
            "that doesn't grow faster than a polynomial. <bookmark mark='b'/> Its transform is defined by passing "
            "the hat to the test function, which is legal because the integral of f hat times g equals the integral "
            "of f times g hat; here, for a Gaussian and a box, both sides agree. <bookmark mark='c'/> Now squeeze a "
            "unit mass toward delta. Its transform flattens out, to the constant one over root two pi. "
            "<bookmark mark='d'/> So delta's transform is a constant, a constant's is a delta, and powers of x go "
            "to derivatives of delta."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), FadeIn(rows[0]), FadeIn(rows[2]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(ax), Create(bx), FadeIn(pp), FadeIn(rd), FadeIn(l2), Create(flat), FadeIn(fl))
            self.play(sT.animate.set_value(0.03), run_time=4.0, rate_func=smooth)
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        for m in (pp, rd):
            m.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def poisson(self):
        d = load("poisson")
        ts, lhs, rhs = d["ts"], d["lhs"], d["rhs"]
        a = math.sqrt(2 * math.pi)
        # a comb of narrow Gaussians (spacing sqrt(2 pi)), under a wide Gaussian envelope, and its transform
        w, Lenv = 0.12, 5.0

        def comb(x):
            return sum(np.exp(-((x - k * a) ** 2) / (2 * w * w)) for k in range(-12, 13)) * np.exp(-x * x / (2 * Lenv**2))

        x, t, F = fft_hat(comb, L=160.0, N=1 << 15)
        Fr = F.real
        mx = np.abs(x) <= 3.2 * a
        mt = np.abs(t) <= 3.2 * a
        # peaks of the transform sit at the same spacing sqrt(2 pi)
        pk = [float(t[mt][np.argmax(np.where(np.abs(t[mt] - k * a) < 1, Fr[mt], -1))]) for k in range(-3, 4)]
        assert np.allclose(pk, a * np.arange(-3, 4), atol=0.02) and np.abs(F.imag).max() < 1e-9
        ax = plain_axes([-3.2 * a, 3.2 * a, a], [0, 1.1, 0.5], 6.0, 1.8).move_to([-3.4, 1.4, 0])
        bx = plain_axes([-3.2 * a, 3.2 * a, a], [0, Fr.max() * 1.1, 1], 6.0, 1.8).move_to([3.4, 1.4, 0])
        g1 = polyline(ax, x[mx], comb(x[mx]), color=C.DISTRIBUTION, stroke_width=2.5)
        g2 = polyline(bx, t[mt], Fr[mt], color=C.FREQ, stroke_width=2.5)
        l1 = MathTex(r"\textstyle\sum_k \delta_{k\sqrt{2\pi}}, \ \text{smoothed and windowed}", font_size=24,
                     color=C.DISTRIBUTION).next_to(ax, UP, buff=0.1)
        l2 = MathTex(r"\text{its transform: \ the same comb}", font_size=24, color=C.FREQ).next_to(bx, UP, buff=0.1)
        # the theta identity as two curves
        cx = plain_axes([0, 3, 0.5], [0.8, 3.4, 1], 5.4, 2.2, numbers=True, font_size=16,
                        x_axis_config={"decimal_number_config": {"num_decimal_places": 1}},
                        y_axis_config={"decimal_number_config": {"num_decimal_places": 0}}).move_to([-3.4, -2.05, 0])
        tt = np.linspace(0.1, 3, 300)
        n = np.arange(-60, 61)
        th1 = np.array([np.sum(np.exp(-math.pi * n * n * s)) for s in tt])
        th2 = np.array([np.sum(np.exp(-math.pi * n * n / s)) for s in tt]) / np.sqrt(tt)
        assert np.allclose(th1, th2, rtol=1e-12)
        c1 = polyline(cx, tt, np.minimum(th1, 3.4), color=C.FUNC, stroke_width=4)
        c2 = DashedVMobject(polyline(cx, tt, np.minimum(th2, 3.4), color=C.FREQ, stroke_width=3), num_dashes=50)
        dots = VGroup(*[Dot(cx.c2p(s, v), radius=0.05, color=C.EPS) for s, v in zip(ts, lhs) if s <= 3 and v <= 3.4])
        tab = VGroup(MathTex(r"t", r"\quad \textstyle\sum_n e^{-\pi n^2 t}", r"\quad t^{-1/2}\sum_n e^{-\pi n^2/t}",
                             font_size=22, color=GREY_A))
        for s, l_, r_ in zip(ts, lhs, rhs):
            tab.add(MathTex(f"{s:g}", rf"\quad {l_:.12f}", rf"\quad {r_:.12f}", font_size=22))
        tab.arrange(DOWN, aligned_edge=LEFT, buff=0.08).move_to([3.5, -2.0, 0])
        regrid(tab)
        rule = MathTex(r"\textstyle\sum_k f(2\pi k) = \frac{1}{\sqrt{2\pi}}\sum_n \hat f(n)", font_size=30,
                       color=C.EPS).move_to([3.5, -0.35, 0])
        head = label(r"The comb is its own transform: \ Poisson summation", font_size=34).to_edge(UP, buff=0.25)
        with self.voiceover(
            "<bookmark mark='a'/> The Dirac comb, a delta at every multiple of root two pi, is tempered. Smooth it "
            "slightly and window it, and transform: the result is the same comb. In the limit the comb is exactly "
            "its own transform. <bookmark mark='b'/> Tested against a function, that's Poisson summation: the sum of "
            "the samples of f equals the sum of the samples of f hat. <bookmark mark='c'/> With a Gaussian, it's "
            "Jacobi's identity for the theta function: the two sides, as curves, coincide, and at every t they agree "
            "to twelve digits. It's the identity behind the functional equation of the zeta function, in the Riemann "
            "video."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), Create(ax), Create(g1), FadeIn(l1))
            self.play(Create(bx), Create(g2), FadeIn(l2))
            vo.wait_until("b")
            self.play(Write(rule))
            vo.wait_until("c")
            self.play(Create(cx), Create(c1))
            self.play(Create(c2), FadeIn(dots), FadeIn(tab[0]))
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[1:]], lag_ratio=0.3), run_time=2.0)
        self.wait(0.4)
        self.clear_scene()
