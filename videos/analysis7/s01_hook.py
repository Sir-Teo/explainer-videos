from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis7.common import cplot, cplot_fine, load, phase_wheel, plain_axes, polyline, square_axes


class Hook(VoiceoverScene):
    def construct(self):
        self.recap()
        self.flat()
        self.exponential()
        self.plan()

    # ------------------------------------------------------------------
    def recap(self):
        led = ledger(filled=6, highlight=7).scale(0.9)
        with self.voiceover(
            "Six rows of the ledger are filled. Part 7 takes a step sideways, into the complex plane. "
            "<bookmark mark='l'/> It's the part the rest of the series needs: the spectral theory of Part 10 runs on "
            "Cauchy's integral formula."
        ) as vo:
            self.play(FadeIn(led))
            vo.wait_until("l")
            self.play(Indicate(led.rows[6], color=C.EPS, scale_factor=1.03))
        self.play(FadeOut(led))

    # ------------------------------------------------------------------
    def flat(self):
        ax = plain_axes([-1.5, 1.5, 0.5], [0, 1, 0.5], 5.4, 2.6, numbers=True, font_size=18,
                        x_axis_config={"decimal_number_config": {"num_decimal_places": 1}},
                        y_axis_config={"decimal_number_config": {"num_decimal_places": 1}}).move_to([-3.6, 0.2, 0])
        x = np.linspace(-1.5, 1.5, 801)
        with np.errstate(divide="ignore", over="ignore"):
            y = np.where(x == 0, 0.0, np.exp(-1 / x**2))
        g = polyline(ax, x, y, color=C.FUNC, stroke_width=4)
        g_l = MathTex(r"e^{-1/x^2}", font_size=32, color=C.FUNC).next_to(ax.c2p(0.85, 0.3), DR, buff=0.12)
        real_t = VGroup(label(r"on $\R$: \ infinitely differentiable,", font_size=24),
                        label(r"every derivative $0$ at $0$: \ Taylor series $\equiv 0$", font_size=24, color=C.PATHOLOGY)
                        ).arrange(DOWN, aligned_edge=LEFT, buff=0.08).next_to(ax, DOWN, buff=0.3)
        S = 4.4
        cx = square_axes([-1, 1, 0.5], [-1, 1, 0.5], S / 2).move_to([3.2, 0.0, 0])

        def F(Z):  # e^(-1/z^2) with the exponent clipped (no overflow); the disk |z| < 0.18 is masked: there the
            W = -1 / Z**2  # phase and the rings of |f| turn faster than any pixel (an essential singularity)
            return np.exp(np.clip(W.real, -60, 40)) * np.exp(1j * W.imag)

        r_hole = 0.18
        img = cplot_fine(cx, F, (-1, 1), (-1, 1), px=960, ss=3, mask=lambda Z: np.abs(Z) > r_hole)
        u = cx.c2p(1, 0)[0] - cx.c2p(0, 0)[0]
        hole = Circle(radius=r_hole * u, color=GREY_B, stroke_width=1.5).move_to(cx.c2p(0, 0))
        frame = Square(side_length=S, color=GREY_C, stroke_width=2).move_to(cx.c2p(0, 0))
        c_l = MathTex(r"e^{-1/z^2} \text{ on } |\mathrm{Re}\,z|, |\mathrm{Im}\,z| \le 1", font_size=28).next_to(frame, UP,
                                                                                                          buff=0.12)
        ys = np.array([0.5, 0.3, 0.2])
        vals = np.exp(1 / ys**2)
        assert np.allclose(np.abs(np.exp(-1 / (1j * ys) ** 2)), vals) and ys.min() > r_hole  # the quoted points show
        assert np.allclose(np.abs(F(1j * ys)), vals)  # the clip never touches the picture's values (1/0.18^2 < 40)
        cplx_t = VGroup(
            MathTex(r"z = iy: \ e^{-1/(iy)^2} = e^{1/y^2}", font_size=26),
            MathTex(r"y = 0.5,\ 0.3,\ 0.2: \ " + r",\ ".join(sci(v, 1) for v in vals), font_size=24, color=C.PATHOLOGY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.08).next_to(frame, DOWN, buff=0.15)
        wheel = phase_wheel(0.3).move_to([6.05, 2.4, 0])
        assert wheel.get_right()[0] <= 6.6 and wheel.get_left()[0] > frame.get_right()[0] + 0.05
        miracles = VGroup(
            label(r"in $\C$, \ one derivative gives:", font_size=26, color=C.EPS),
            label(r"1. \ infinitely many derivatives", font_size=26),
            label(r"2. \ a power series that converges to $f$", font_size=26),
            label(r"3. \ values on any tiny arc decide $f$ everywhere", font_size=26),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        head = label(r"Why is $\C$ so much better behaved than $\R$?", font_size=36).to_edge(UP, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Part 2 met this function: e to the minus one over x squared. On the real line it's "
            "infinitely differentiable, and every derivative at zero vanishes, so its Taylor series is zero, and "
            "says nothing about it. <bookmark mark='b'/> Now feed it complex numbers. Here's the same formula on a "
            "square of the complex plane, colored by phase, with brightness for size. Along the imaginary axis, "
            "minus one over z squared is positive, and the function explodes: at 0.2 i it's already about seven times "
            "ten to the ten. <bookmark mark='c'/> The real line hid a catastrophe. In the complex plane a function with a "
            "derivative can't behave like this, and that buys three miracles: one derivative gives infinitely many; "
            "the function is its own power series; and its values on any tiny arc decide it everywhere."
        ) as vo:
            vo.wait_until("a")
            real = VGroup(ax, g, g_l, real_t)
            real.shift(RIGHT * 3.6)  # centred while it is alone; it makes room for the complex picture at 'b'
            self.play(FadeIn(head), Create(ax), Create(g), FadeIn(g_l))
            self.play(FadeIn(real_t))
            vo.wait_until("b")
            self.play(real.animate.shift(LEFT * 3.6), run_time=1.0)
            self.play(FadeIn(img), Create(frame), Create(hole), FadeIn(c_l), FadeIn(wheel))
            self.play(FadeIn(cplx_t))
            vo.wait_until("c")
            self.play(FadeOut(ax), FadeOut(g), FadeOut(g_l), FadeOut(real_t))
            miracles.move_to([-3.6, 0.0, 0])
            self.play(LaggedStart(*[FadeIn(m, shift=RIGHT * 0.15) for m in miracles], lag_ratio=0.5), run_time=3.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def exponential(self):
        d = load("exp")
        e2pi, half_pi, partial = complex(d["e2pi"]), float(d["half_pi"]), d["partial"]
        cx = square_axes([-2, 2, 1], [-1, 7, 1], 0.62).move_to([-4.0, -0.35, 0])
        img = cplot(cx, np.exp, (-2, 2), (-1, 7))
        frame = Rectangle(width=4 * 0.62, height=8 * 0.62, color=GREY_C, stroke_width=2).move_to(cx.c2p(0, 3))
        per = VGroup(*[DashedLine(cx.c2p(-2, 2 * math.pi * k), cx.c2p(2, 2 * math.pi * k), color=WHITE, stroke_width=2)
                       for k in (0, 1)])
        per_l = VGroup(MathTex(r"0", font_size=26).next_to(cx.c2p(2, 0), RIGHT, buff=0.1),
                       MathTex(r"2\pi i", font_size=26).next_to(cx.c2p(2, 2 * math.pi), RIGHT, buff=0.1))
        rows = VGroup(
            MathTex(r"\exp(z) = \sum_{n \ge 0} \frac{z^n}{n!}", font_size=36),
            label(r"Rudin's prologue builds everything from this series:", font_size=24, color=GREY_A),
            MathTex(r"\exp(z + w) = \exp(z)\exp(w), \quad \exp(z) \ne 0", font_size=28),
            MathTex(r"\tfrac{\pi}{2} = \text{the first zero of } \cos t = \mathrm{Re}\exp(it):", font_size=28),
            MathTex(rf"\text{{bisection on the series: }} {half_pi:.15f}", font_size=26, color=C.EPS),
            VGroup(MathTex(r"\Big|\sum_{n < N} \frac{(2\pi i)^n}{n!} - 1\Big| \ \text{ for } N = 10, 20, 30, 40:",
                           font_size=24),
                   MathTex(r"= " + r",\ ".join(sci(v, 1) for v in partial), font_size=24)).arrange(DOWN, aligned_edge=LEFT,
                                                                                             buff=0.1),
            label(r"so $e^{2\pi i} = 1$: \ $\exp$ repeats every $2\pi i$", font_size=26, color=C.EPS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([2.6, -0.3, 0])
        assert rows.width < 7.0 and rows.get_right()[0] <= 6.6 and rows.get_bottom()[1] > -3.6
        assert abs(half_pi - math.pi / 2) < 1e-14 and abs(e2pi - 1) < 1e-12
        head = label(r"The exponential, \ the most important function in mathematics", font_size=34).to_edge(UP,
                                                                                                         buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Rudin begins Real and Complex Analysis with one series: the exponential. "
            "<bookmark mark='b'/> On the left, its domain coloring. Moving up, the colors cycle, and the whole "
            "picture repeats. <bookmark mark='c'/> From the series alone come the addition law, and the fact that "
            "exp never vanishes. Even pi comes out of it: half of pi is the first positive zero of the cosine, the "
            "real part of e to the i t. Bisection on the series pins it down to every digit. "
            "<bookmark mark='d'/> And the partial sums at two pi i converge to one: the exponential repeats every two "
            "pi i, which is the horizontal stripe pattern in the picture."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(img), Create(frame))
            self.play(Create(per), FadeIn(per_l))
            vo.wait_until("c")
            self.play(FadeIn(rows[1:3]))
            self.play(FadeIn(rows[3:5]))
            vo.wait_until("d")
            self.play(FadeIn(rows[5]))
            self.play(FadeIn(rows[6]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def plan(self):
        chapters = [
            r"Complex derivatives are rotations", r"Path integrals and winding numbers", r"Cauchy's formula and its miracles",
            r"Zeros, open maps, the maximum modulus", r"The global Cauchy theorem; residues",
            r"The Schwarz lemma; three lines", r"Runge's theorem", r"Normal families (Montel)",
            r"The Riemann mapping theorem", r"Tours: harmonic functions; products; $H^p$",
        ]
        items = VGroup(*[label(rf"{i + 1}.\; {t}", font_size=27) for i, t in enumerate(chapters)])
        items.arrange(DOWN, aligned_edge=LEFT, buff=0.2).shift(DOWN * 0.5)
        head = label(r"Part 7: Complex analysis", font_size=42).to_edge(UP, buff=0.4)
        sub = label(r"Rudin, \textit{Real and Complex Analysis}: the prologue and chapters 10--14, \ with tours of 11, 15--17, 19, 20",
                    font_size=24, color=GREY_B).next_to(head, DOWN, buff=0.15)
        with self.voiceover(
            "Here's the plan, following chapters ten through fourteen of Real and Complex Analysis. "
            "<bookmark mark='a'/> First the derivative, path integrals, and Cauchy's formula with its miracles. "
            "<bookmark mark='b'/> Then the global theorems: residues, the Schwarz lemma, Runge's approximation "
            "theorem. <bookmark mark='c'/> Then Arzelà and Ascoli's grandest payoff, the Riemann mapping theorem, "
            "computed for a real polygon, and a guided tour of the rest."
        ) as vo:
            self.play(FadeIn(head), FadeIn(sub))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(items[i], shift=RIGHT * 0.2) for i in range(4)], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(items[i], shift=RIGHT * 0.2) for i in range(4, 7)], lag_ratio=0.3))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(items[i], shift=RIGHT * 0.2) for i in range(7, 10)], lag_ratio=0.3))
        self.wait(0.6)
        self.clear_scene()
