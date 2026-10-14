from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis9.common import area_under, load, plain_axes, polyline, trap


class Plancherel(VoiceoverScene):
    def construct(self):
        self.card()
        self.inversion()
        self.unitary()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(7, r"Inversion and Plancherel", r"Can a function be rebuilt from its frequencies?", lit=(),
                            part=9)
        with self.voiceover("Chapter seven: getting the function back, and the transform as a rotation of L two."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def inversion(self):
        d = load("plancherel")
        xs, Ts, curves, over = d["xs"], d["Ts"], d["curves"], d["over"]
        ax = plain_axes([-3, 3, 1], [-0.25, 1.25, 0.5], 6.4, 3.6, numbers=True, font_size=18,
                        x_axis_config={"decimal_number_config": {"num_decimal_places": 0}},
                        y_axis_config={"include_numbers": False}).move_to([-3.0, -0.6, 0])
        # no y numbers on the central axis (the box top and every reconstruction pass 1 there, the first Poisson
        # curve 0.5): the one height that matters, 1, is labelled beside the box
        one_l = MathTex(r"1", font_size=18).next_to(ax.c2p(1.05, 1), RIGHT, buff=0.08)
        box = VGroup(Line(ax.c2p(-3, 0), ax.c2p(-1, 0), color=WHITE, stroke_width=2.5),
                     Line(ax.c2p(-1, 1), ax.c2p(1, 1), color=WHITE, stroke_width=2.5),
                     Line(ax.c2p(1, 0), ax.c2p(3, 0), color=WHITE, stroke_width=2.5))
        cols = [C.SEQ, C.APPROX, C.EPS]
        gs = [polyline(ax, xs, c_, color=col, stroke_width=2.5) for c_, col in zip(curves, cols)]
        ls = [MathTex(rf"\frac{{1}}{{\sqrt{{2\pi}}}}\int_{{-{T}}}^{{{T}}} \hat f(t)\,e^{{ixt}}dt: \ \max = 1 + {o:.4f}",
                      font_size=26, color=c).next_to(ax, UP, buff=0.1) for T, o, c in zip(Ts, over, cols)]
        rows = VGroup(
            label(r"\textbf{RCA 9.11} \ if $f, \hat f \in L^1$:", font_size=24),
            MathTex(r"f(x) = \frac{1}{\sqrt{2\pi}}\int \hat f(t)\, e^{ixt}\,dt \ \text{ a.e.}", font_size=28, color=C.EPS),
            VGroup(label(r"proof: \ insert $e^{-\lambda |t|}$ \ (in space: the Poisson kernel,", font_size=22, color=GREY_A),
                   label(r"an approximate identity), \ let $\lambda \to 0$", font_size=22, color=GREY_A)).arrange(
                DOWN, aligned_edge=LEFT, buff=0.08),
            label(r"the box's $\hat f$ is not integrable: \ cut it at $\pm T$", font_size=22),
            label(r"converges in $L^2$; \ the overshoot tends to Gibbs' $8.95\%$", font_size=22, color=C.PATHOLOGY),
            label(r"\textbf{9.12} \ uniqueness: \ $\hat f = \hat g$ $\Rightarrow$ $f = g$ a.e.", font_size=22),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([3.5, -0.5, 0])
        for r_ in rows:
            if r_.width > 6.0:
                r_.width = 6.0
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([3.5, -0.5, 0])
        assert rows.get_right()[0] <= 6.6
        assert abs(over[-1] - 0.0895) < 0.003 and np.all(np.diff(over) > 0)
        # Rudin's proof, live: damp the frequencies by e^{-lambda|t|}. In space that convolves the box with the
        # Poisson kernel lambda / (pi (lambda^2 + x^2)): (arctan((x + 1)/lambda) - arctan((x - 1)/lambda)) / pi
        xp = np.linspace(-3, 3, 1201)

        def pbox(lam, x_=xp):
            return (np.arctan((x_ + 1) / lam) - np.arctan((x_ - 1) / lam)) / math.pi

        tq = np.linspace(-3000, 3000, 3_000_001)
        fh = math.sqrt(2 / math.pi) * np.sinc(tq / math.pi)  # the box's transform, sqrt(2/pi) sin t / t
        for lam in (1.0, 0.3, 0.1):
            for x0 in (0.0, 0.9, 1.5):
                v_ = np.trapezoid(fh * np.exp(-lam * np.abs(tq)) * np.cos(x0 * tq), tq) / math.sqrt(2 * math.pi)
                assert abs(v_ - pbox(lam, np.array([x0]))[0]) < 1e-6
        lv = ValueTracker(0.0)  # log10 lambda
        pc = always_redraw(lambda: polyline(ax, xp, pbox(10 ** lv.get_value()), color=C.TEST_FN, stroke_width=3))
        pl = VGroup(MathTex(r"\text{damped by } e^{-\lambda |t|}: \ \text{Poisson kernel} * \text{box}, \ \lambda =",
                            font_size=26, color=C.TEST_FN),
                    DecimalNumber(1.0, num_decimal_places=2, font_size=26, color=C.TEST_FN)).arrange(RIGHT, buff=0.12)
        pl.next_to(ax, UP, buff=0.1)
        pl[1].add_updater(lambda m: m.set_value(10 ** lv.get_value()))
        head = label(r"Rebuilding the box from its frequencies", font_size=34).to_edge(UP, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> The inversion theorem: the same integral, with the opposite sign in the exponent, "
            "gives the function back. Rudin's proof inserts a damping factor in frequency, e to "
            "the minus lambda times the size of t. In space that's the Poisson kernel, an approximate identity, and "
            "as lambda shrinks it closes in on the function. <bookmark mark='b'/> For the box, the transform isn't integrable, so cut it "
            "off at plus and minus T. <bookmark mark='c'/> As T grows the reconstruction hugs the box, converging in "
            "L two, but near each jump it overshoots, and the overshoot tends to Gibbs' 8.95 percent, the same as for "
            "Fourier series in Part 3."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), FadeIn(rows[:3]), Create(ax), Create(box), FadeIn(one_l))
            self.play(FadeIn(pc), FadeIn(pl))
            self.play(lv.animate.set_value(-1.7), run_time=11.0)  # lambda from 1 down to 0.02: it closes in on the box
            vo.wait_until("b")
            pc.clear_updaters()
            pl[1].clear_updaters()
            self.play(FadeOut(pc), FadeOut(pl), run_time=0.6)
            self.play(Create(gs[0]), FadeIn(ls[0]), FadeIn(rows[3]))
            vo.wait_until("c")
            for k in (1, 2):
                self.play(gs[k - 1].animate.set_stroke(opacity=0.3), Create(gs[k]), FadeTransform(ls[k - 1], ls[k]),
                          run_time=1.3)
            self.play(FadeIn(rows[4:]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def unitary(self):
        d = load("plancherel")
        ratios = d["ratios"]
        rng = np.random.default_rng(9)
        ax = plain_axes([-6, 6, 2], [-2.5, 2.5, 1], 5.4, 2.6).move_to([-3.4, 1.0, 0])
        bx = plain_axes([-14, 14, 7], [0, 0.8, 0.4], 5.4, 2.0).move_to([-3.4, -2.1, 0])
        x = np.linspace(-6, 6, 2400)
        c = rng.normal(size=6)
        f = sum(c[k] * np.exp(-((x - rng.uniform(-3, 3)) ** 2) * rng.uniform(0.5, 3)) * np.cos(rng.uniform(0, 6) * x)
                for k in range(6))
        # zero-padded (L = 160): the transform is sampled every 2 pi / 160 = 0.039, so |f^| is drawn smooth
        N = 1 << 16
        L = 160.0
        xx = (np.arange(N) - N / 2) * (L / N)
        rng2 = np.random.default_rng(9)
        c2 = rng2.normal(size=6)
        ff = sum(c2[k] * np.exp(-((xx - rng2.uniform(-3, 3)) ** 2) * rng2.uniform(0.5, 3)) * np.cos(rng2.uniform(0, 6) * xx)
                 for k in range(6))
        F = np.fft.fftshift(np.fft.fft(np.fft.ifftshift(ff))) * (L / N) / math.sqrt(2 * math.pi)
        tt = np.fft.fftshift(np.fft.fftfreq(N, L / N)) * 2 * math.pi
        m = np.abs(tt) <= 14
        mx = np.abs(xx) <= 6
        assert 1 - np.sum(np.abs(F[m]) ** 2) / np.sum(np.abs(F) ** 2) < 1e-6 and np.abs(F).max() < 0.8  # all of it shows
        assert np.abs(ff[~mx]).max() < 1e-9 and (ff**2).max() < 2.5 and (np.abs(F) ** 2).max() < 0.8  # the squares fit
        # direct quadrature at a few t: the FFT samples are the transform
        for i in (N // 2, N // 2 + 44, N // 2 + 107):  # t = 0, 1.73, 4.20
            q_ = np.sum(ff[mx] * np.exp(-1j * xx[mx] * tt[i])) * (L / N) / math.sqrt(2 * math.pi)
            assert abs(q_ - F[i]) < 1e-8
        gf = polyline(ax, xx[mx][::2], ff[mx][::2], color=C.FUNC, stroke_width=2.5)
        gF = polyline(bx, tt[m], np.abs(F[m]), color=C.FREQ, stroke_width=2.5)
        l1 = MathTex(r"f", font_size=26, color=C.FUNC).next_to(ax, LEFT, buff=0.1)
        l2 = MathTex(r"|\hat f|", font_size=26, color=C.FREQ).next_to(bx, LEFT, buff=0.1)
        n1 = math.sqrt(np.sum(np.abs(ff) ** 2) * (L / N))
        n2 = math.sqrt(np.sum(np.abs(F) ** 2) * (2 * math.pi / L))
        assert abs(n1 - n2) < 1e-9 and np.allclose(ratios, 1, atol=1e-10)
        # the norms as areas: |f|^2 and |f^|^2 enclose the same area, n1^2
        A1 = trap(ff[mx] ** 2, xx[mx])
        A2 = trap(np.abs(F[m]) ** 2, tt[m])
        assert abs(A1 - n1**2) < 1e-6 and abs(A2 - n1**2) < 1e-5
        sq1 = VGroup(area_under(ax, xx[mx][::2], ff[mx][::2] ** 2, C.FUNC, 0.4),
                     polyline(ax, xx[mx][::2], ff[mx][::2] ** 2, color=C.FUNC, stroke_width=3))
        sq2 = VGroup(area_under(bx, tt[m], np.abs(F[m]) ** 2, C.FREQ, 0.4),
                     polyline(bx, tt[m], np.abs(F[m]) ** 2, color=C.FREQ, stroke_width=3))
        a1l = MathTex(r"|f|^2:", rf"\ \text{{area }} {A1:.4f}", font_size=24, color=C.FUNC).next_to(ax, UP, buff=0.08)
        a2l = MathTex(r"|\hat f|^2:", rf"\ \text{{area }} {A2:.4f}", font_size=24, color=C.FREQ).next_to(bx, UP, buff=0.08)
        assert f"{A1:.4f}" == f"{A2:.4f}"
        rows = VGroup(
            label(r"\textbf{RCA 9.13} \ (Plancherel)", font_size=26),
            MathTex(r"\|\hat f\|_2 = \|f\|_2", font_size=34, color=C.EPS),
            MathTex(rf"\text{{here: }} {n1:.10f} = {n2:.10f}", font_size=24),
            label(r"20 random functions: \ equal to $10^{-10}$", font_size=22, color=GREY_A),
            label(r"so $f \mapsto \hat f$ extends from $L^1 \cap L^2$", font_size=24),
            label(r"to a \emph{unitary} map of $L^2$ onto itself", font_size=24, color=C.EPS),
            label(r"the dictionary: \ an orthogonal change of basis \ $\leftrightarrow$ \ the Fourier transform",
                  font_size=22, color=C.INNER),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([3.5, -0.4, 0])
        for r_ in rows:
            if r_.width > 6.0:
                r_.width = 6.0
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([3.5, -0.4, 0])
        head = label(r"The Fourier transform preserves length", font_size=34).to_edge(UP, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Plancherel's theorem: the transform preserves the L two norm. "
            "<bookmark mark='b'/> Here's a random wave packet and the size of its transform; <bookmark mark='n'/> their "
            "norms agree to ten digits, and so do those of twenty other random functions. <bookmark mark='c'/> So the "
            "transform extends "
            "from the nice functions to all of L two, as a unitary map: it's an orthogonal change of basis, from "
            "positions to frequencies, in an infinite-dimensional Hilbert space."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), FadeIn(rows[:2]))
            vo.wait_until("b")
            self.play(Create(ax), Create(gf), FadeIn(l1))
            self.play(Create(bx), Create(gF), FadeIn(l2))
            vo.wait_until("n")
            self.play(gf.animate.set_stroke(opacity=0.3), gF.animate.set_stroke(opacity=0.3), FadeIn(sq1), FadeIn(sq2),
                      FadeIn(a1l), FadeIn(a2l), FadeIn(rows[2:4]))
            vo.wait_until("c")
            self.play(FadeIn(rows[4:]))
        self.wait(0.4)
        self.clear_scene()
