from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis7.common import load, plain_axes, polyline, square_axes


class NormalFamilies(VoiceoverScene):
    def construct(self):
        self.card()
        self.flatness()
        self.subsequence()
        self.dictionary()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(8, r"Normal families", r"When does a bounded family have a convergent subsequence?", lit=(),
                            part=7)
        with self.voiceover("Chapter eight: Montel's theorem, where Arzelà and Ascoli pay off in the complex plane."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def flatness(self):
        d = load("montel")
        ns, sin_sup = d["ns"], d["sin_sup"]
        ax = plain_axes([-1, 1, 0.5], [-1.2, 1.2, 1], 5.0, 2.6).move_to([-3.6, 0.6, 0])
        x = np.linspace(-1, 1, 1200)
        waves = [polyline(ax, x, np.sin(n * x), color=c, stroke_width=2.5) for n, c in
                 ((3, C.SEQ), (12, C.APPROX), (40, C.EPS))]
        a_l = label(r"on $\R$: \ $|\sin nx| \le 1$, \ but steeper and steeper (Part 3)", font_size=22).next_to(ax, UP,
                                                                                                         buff=0.1)
        bx = plain_axes([0, 12.5, 2], [-0.5, 2.8, 1], 5.0, 2.4, numbers=True, font_size=18,
                        x_axis_config={"decimal_number_config": {"num_decimal_places": 0}},
                        y_axis_config={"decimal_number_config": {"num_decimal_places": 0}}).move_to([-3.6, -2.35, 0])
        bars = VGroup(*[Rectangle(width=0.25, height=abs(bx.c2p(0, math.log10(v))[1] - bx.c2p(0, 0)[1]), stroke_width=0,
                                  fill_color=C.PATHOLOGY, fill_opacity=0.85).move_to(bx.c2p(n, math.log10(v) / 2))
                        for n, v in zip(ns, sin_sup)])
        b_l = MathTex(r"\log_{10} \max_{|z| \le 1/2} |\sin nz|", font_size=24, color=C.PATHOLOGY).next_to(bx, UP, buff=0.1)
        assert np.allclose(sin_sup, np.sinh(ns / 2), rtol=1e-3)
        rows = VGroup(
            label(r"on $\C$: \ $\sin(iy) = i\sinh y$:", font_size=24),
            MathTex(rf"\max_{{|z| \le 1/2}}|\sin 12 z| = \sinh 6 = {sin_sup[-1]:.1f}", font_size=28, color=C.PATHOLOGY),
            label(r"a family bounded on a disk cannot wiggle:", font_size=24),
            label(r"Cauchy's estimate on $|z| \le r < R$:", font_size=22, color=GREY_A),
            MathTex(r"|f'(z)| \le \frac{M}{R - r}", font_size=32, color=C.EPS),
            label(r"so bounded $\Rightarrow$ equicontinuous on compact sets", font_size=24, color=C.EPS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to([3.3, -0.4, 0])
        head = label(r"In $\C$, \ a bound is also a speed limit", font_size=34).to_edge(UP, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> On the real line, sine n x stays between minus one and one, but gets steeper and "
            "steeper: bounded, and not equicontinuous, as Part 3 showed. <bookmark mark='b'/> In the complex plane "
            "the same functions aren't even bounded: on the imaginary axis sine becomes hyperbolic sine, and on the "
            "disk of radius one half, sine of twelve z reaches two hundred. <bookmark mark='c'/> For holomorphic "
            "functions a bound is also a speed limit: Cauchy's estimate bounds the derivative on a smaller disk by "
            "the bound on the larger one. So a uniformly bounded family is automatically equicontinuous on compact "
            "sets."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), Create(ax), FadeIn(a_l))
            for w_ in waves:
                self.play(Create(w_), run_time=0.9)
            vo.wait_until("b")
            self.play(Create(bx), FadeIn(b_l), LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars], lag_ratio=0.1),
                      run_time=2.0)
            self.play(FadeIn(rows[:2]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2:4]))
            self.play(FadeIn(rows[4:]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def subsequence(self):
        d = load("montel")
        nk, errs_in, errs_out = d["nk"], d["errs_in"], d["errs_out"]
        panels = Group()
        S = 2.6
        for k, n in enumerate(nk[:3]):
            ax = square_axes([-1.05, 1.05, 1], [-1.05, 1.05, 1], S / 2.1).move_to([-4.6 + 3.1 * k, 0.1, 0])
            px = 360
            x = np.linspace(-1.05, 1.05, px)
            X, Y = np.meshgrid(x, x[::-1])
            Z = X + 1j * Y
            with np.errstate(over="ignore", invalid="ignore"):
                E = np.abs((math.cos(n) * Z + math.sin(n) * Z * Z) / 2 + Z ** int(n) / 2 - Z / 2)
            t = np.clip(E / 0.6, 0, 1)[..., None]
            lo, hi = np.array(ManimColor(BACKGROUND).to_rgb()), np.array(ManimColor(C.EPS).to_rgb())
            rgb = lo + t * (hi - lo)
            alpha = (np.abs(Z) <= 1).astype(float)[..., None]
            im = ImageMobject((np.concatenate([rgb, alpha], -1) * 255).astype(np.uint8))
            im.set_resampling_algorithm(RESAMPLING_ALGORITHMS["bilinear"])
            im.stretch_to_fit_width(S).stretch_to_fit_height(S).move_to(ax.c2p(0, 0))
            u = ax.c2p(1, 0)[0] - ax.c2p(0, 0)[0]
            ring = Circle(radius=u, color=WHITE, stroke_width=2).move_to(ax.c2p(0, 0))
            inner = DashedVMobject(Circle(radius=0.9 * u, color=C.CONNECTED_SET, stroke_width=2).move_to(ax.c2p(0, 0)),
                                   num_dashes=30)
            t_ = MathTex(rf"n = {int(n)}", font_size=26).next_to(ring, UP, buff=0.1)
            r_ = VGroup(MathTex(rf"\sup_{{|z| \le 0.9}} = {sci(float(errs_in[k]), 1)}", font_size=22, color=C.CONNECTED_SET),
                        MathTex(rf"\sup_{{|z| \le 1}} = {errs_out[k]:.3f}", font_size=22, color=C.EPS)
                        ).arrange(DOWN, buff=0.06).next_to(ring, DOWN, buff=0.12)
            panels.add(Group(im, ring, inner, t_, r_))
        rows = VGroup(
            MathTex(r"f_n(z) = \tfrac12(\cos n\cdot z + \sin n \cdot z^2) + \tfrac12 z^n", font_size=26),
            label(r"$|f_n| \le \frac{1 + \sqrt 2}{2}$ on $D$: \ a bounded family", font_size=22, color=GREY_A),
            label(r"along $n = 6, 44, 710, 103993$ \ ($n \bmod 2\pi \to 0$):", font_size=22),
            MathTex(r"f_{n_k} \to \tfrac{z}{2}", font_size=30, color=C.EPS),
            label(r"brightness: \ $|f_n - z/2|$", font_size=22, color=GREY_A),
            label(r"uniformly on $|z| \le 0.9$, \ not on $|z| \le 1$:", font_size=22, color=C.CONNECTED_SET),
            label(r"``normal'' means \emph{locally} uniformly", font_size=22, color=C.CONNECTED_SET),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.13).move_to([5.0, -0.2, 0])
        for r_ in rows:
            if r_.width > 3.9:
                r_.width = 3.9
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.13).move_to([5.05, -0.2, 0])
        thm = label(r"\textbf{RCA 14.6} \ (Montel) \ a family of holomorphic functions, \ uniformly bounded on compact "
                    r"sets, \ is normal", font_size=26, color=C.EPS).to_edge(DOWN, buff=0.3)
        assert np.all(np.diff(errs_in) < 0) and np.all(errs_out > 0.45)
        zb = np.exp(1j * np.linspace(0, 2 * math.pi, 4001))  # max modulus: the sup over D is on the circle
        assert all(np.abs((math.cos(n) * zb + math.sin(n) * zb ** 2) / 2 + zb ** n / 2).max() <= (1 + math.sqrt(2)) / 2
                   for n in range(1, 200))
        head = label(r"A bounded family has a locally uniformly convergent subsequence", font_size=32).to_edge(UP, buff=0.25)
        with self.voiceover(
            "<bookmark mark='a'/> Here's a bounded family on the disk: a rotating mixture of z and z squared, plus "
            "z to the n, over two. <bookmark mark='b'/> Pick n so that n is nearly a multiple of two pi: six, "
            "forty-four, seven hundred and ten. The functions converge to z over two. <bookmark mark='c'/> Brightness "
            "shows the error. It retreats to a thinner and thinner rim: on the disk of radius 0.9 it drops to ten to "
            "the minus five, but right at the edge, z to the n keeps it at one half. Convergence is uniform on "
            "every compact subset, not on the whole disk. <bookmark mark='d'/> Montel's theorem: every uniformly "
            "bounded family of holomorphic functions has such a subsequence."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), FadeIn(rows[:2]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2:4]))
            self.play(FadeIn(panels[0]))
            vo.wait_until("c")
            self.play(FadeIn(panels[1]), FadeIn(rows[4]))
            self.play(FadeIn(panels[2]), FadeIn(rows[5:]))
            vo.wait_until("d")
            self.play(FadeIn(thm))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def dictionary(self):
        card = dictionary_card(r"Part 3: \ continuous functions", r"Part 7: \ holomorphic functions", [
            (r"Arzel\`a--Ascoli", r"Montel"),
            (r"bounded \emph{and} equicontinuous", r"bounded \ (equicontinuity is free)"),
            (r"$\Rightarrow$ a uniformly convergent subsequence", r"$\Rightarrow$ a locally uniformly convergent one"),
            (r"uniform limits are continuous", r"locally uniform limits are holomorphic \ (10.28)"),
            (r"the payoff: \ Peano's existence theorem", r"the payoff: \ the Riemann mapping theorem"),
        ], font_size=24)
        card.move_to(DOWN * 0.3)
        head = label(r"The same compactness theorem, \ one level up", font_size=34).to_edge(UP, buff=0.35)
        with self.voiceover(
            "<bookmark mark='a'/> Montel's theorem is Arzelà and Ascoli in the complex plane, with equicontinuity "
            "coming for free. <bookmark mark='b'/> And the limits stay holomorphic, by Morera's theorem. "
            "<bookmark mark='c'/> In Part 3 the payoff was existence of solutions to differential equations. Here it's "
            "the Riemann mapping theorem."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), FadeIn(card.titles))
            for i in range(3):
                self.play(FadeIn(card.rows[i]), FadeIn(card.arrows[i]), run_time=0.6)
            vo.wait_until("b")
            self.play(FadeIn(card.rows[3]), FadeIn(card.arrows[3]))
            vo.wait_until("c")
            self.play(FadeIn(card.rows[4]), FadeIn(card.arrows[4]))
        self.wait(0.4)
        self.clear_scene()
