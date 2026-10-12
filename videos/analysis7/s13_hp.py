from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis7.common import cplot, plain_axes, square_axes
from videos.analysis7.s11_harmonic import tour_tag


def bars(ax, coeffs, color, width=0.32):
    """Coefficient bars c_n at n (dict n -> value), on ax."""
    g = VGroup()
    for n, v in coeffs.items():
        h = ax.c2p(0, v)[1] - ax.c2p(0, 0)[1]
        g.add(Rectangle(width=width, height=max(h, 0.001), stroke_width=0, fill_color=color, fill_opacity=0.9)
              .move_to(ax.c2p(n, v / 2)))
    return g


class Hp(VoiceoverScene):
    def construct(self):
        self.card()
        self.hardy()
        self.shift()
        self.beurling()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(12, r"A tour: $H^p$ and the shift", r"Which functions on the circle extend into the disk?",
                            lit=(), part=7)
        with self.voiceover("Chapter twelve, the last stop of the tour: Hardy spaces, and the first operator of the "
                            "series."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def hardy(self):
        ax = plain_axes([-8.5, 8.5, 1], [0, 1.1, 0.5], 9.0, 2.4).move_to([-1.6, -0.6, 0])
        nums = VGroup(*[MathTex(str(n), font_size=20).next_to(ax.c2p(n, 0), DOWN, buff=0.1) for n in range(-8, 9, 2)])
        c = {n: 0.5**n for n in range(0, 9)}
        b = bars(ax, c, C.SEQ)
        empty = VGroup(*[Line(ax.c2p(n - 0.16, 0), ax.c2p(n + 0.16, 0), color=C.PATHOLOGY, stroke_width=4)
                         for n in range(-8, 0)])
        norm2 = sum(v * v for v in c.values())
        exact = 4 / 3
        assert abs(norm2 - exact) < 1e-4
        rows = VGroup(
            MathTex(r"f(z) = \frac{1}{1 - z/2} = \sum_{n \ge 0} 2^{-n} z^n", font_size=30),
            label(r"on the circle: \ Fourier coefficients only for $n \ge 0$", font_size=24),
            MathTex(rf"\|f\|_{{H^2}}^2 = \sum |c_n|^2 = \tfrac43", font_size=28, color=C.EPS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        for r_ in rows:
            if r_.width > 5.4:
                r_.width = 5.4
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([3.9, 1.95, 0])
        defn = VGroup(
            label(r"\textbf{RCA 17.7--17.11} \ $H^2$: \ holomorphic $f$ on $D$ with $\sup_r \frac{1}{2\pi}\int |f(re^{i\theta})|^2"
                  r"\,d\theta < \infty$", font_size=24),
            label(r"= power series with $\sum |c_n|^2 < \infty$ \ = \ the part of $L^2(T)$ with no negative frequencies",
                  font_size=24, color=C.EPS),
        ).arrange(DOWN, buff=0.1).to_edge(DOWN, buff=0.4)
        n_l = MathTex(r"n", font_size=24, color=GREY_B).next_to(ax, RIGHT, buff=0.1)
        head = label(r"Hardy space: \ functions on the circle that extend holomorphically", font_size=32).to_edge(UP,
                                                                                                         buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Which functions on the circle are boundary values of holomorphic functions on the "
            "disk? <bookmark mark='b'/> Expand one in a Fourier series. A power series has only nonnegative "
            "frequencies, so on the circle the negative half of the spectrum is empty. <bookmark mark='c'/> The "
            "Hardy space H two is exactly that: square-integrable functions on the circle whose negative Fourier "
            "coefficients vanish, or equivalently, power series with square-summable coefficients."
        ) as vo:
            self.add(tour_tag())
            vo.wait_until("a")
            self.play(FadeIn(head), Create(ax), FadeIn(nums), FadeIn(n_l))
            vo.wait_until("b")
            self.play(FadeIn(rows[0]), LaggedStart(*[GrowFromEdge(r_, DOWN) for r_ in b], lag_ratio=0.15), run_time=2.0)
            self.play(Create(empty), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(defn))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def shift(self):
        ax = plain_axes([-0.5, 9.5, 1], [0, 1.1, 0.5], 8.4, 2.6).move_to([-2.0, 0.3, 0])
        nums = VGroup(*[MathTex(str(n), font_size=20).next_to(ax.c2p(n, 0), DOWN, buff=0.1) for n in range(0, 10)])
        rng = np.random.default_rng(8)
        c = rng.uniform(0.2, 1.0, 7)
        b0 = bars(ax, {n: float(v) for n, v in enumerate(c)}, C.SEQ)
        b1 = bars(ax, {n + 1: float(v) for n, v in enumerate(c)}, C.APPROX)
        b2 = bars(ax, {n + 2: float(v) for n, v in enumerate(c)}, C.EPS)
        f_l = MathTex(r"f", font_size=28, color=C.SEQ).next_to(ax, LEFT, buff=0.2)
        rows = VGroup(
            MathTex(r"(Sf)(z) = z f(z): \ (c_0, c_1, c_2, \ldots) \mapsto (0, c_0, c_1, \ldots)", font_size=28),
            label(r"the shift moves every coefficient one step to the \emph{right}", font_size=24, color=C.APPROX),
            MathTex(rf"\|Sf\| = \|f\| = {math.sqrt(float(np.sum(c**2))):.4f}: \ \text{{an isometry}}", font_size=26),
            label(r"but not onto: \ nothing maps to $1$ \ (the slot $n = 0$ stays empty)", font_size=24,
                  color=C.PATHOLOGY),
            label(r"an isometry that is not unitary: \ impossible in finite dimensions", font_size=24, color=C.EPS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([0.2, -2.3, 0])
        head = label(r"The shift operator on $H^2$", font_size=34).to_edge(UP, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Multiply by z. On the coefficients, that moves everything one step to the right "
            "and leaves the first slot empty. <bookmark mark='b'/> Do it again, and again. Lengths never change: the "
            "shift is an isometry. <bookmark mark='c'/> But it isn't onto: nothing lands on the constant one. An "
            "isometry of a space onto a proper part of itself can't happen in finite dimensions. This operator will "
            "be the star of Part 10, where its spectrum is the whole closed disk."
        ) as vo:
            self.add(tour_tag())
            vo.wait_until("a")
            self.play(FadeIn(head), Create(ax), FadeIn(nums), FadeIn(b0), FadeIn(f_l), FadeIn(rows[0]))
            self.play(TransformFromCopy(b0, b1), run_time=1.5)
            self.play(FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(b0.animate.set_fill(opacity=0.25), TransformFromCopy(b1, b2), run_time=1.5)
            self.play(FadeIn(rows[2]))
            vo.wait_until("c")
            self.play(FadeIn(rows[3]))
            self.play(FadeIn(rows[4]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def beurling(self):
        S = 4.2
        cx = square_axes([-1.02, 1.02, 1], [-1.02, 1.02, 1], S / 2.04).move_to([-4.2, -0.7, 0])
        inner = lambda Z: np.exp(-(1 + Z) / (1 - Z))  # noqa: E731
        img = cplot(cx, inner, (-1.02, 1.02), (-1.02, 1.02), px=800, mask=lambda Z: np.abs(Z) <= 1)
        unit = Circle(radius=cx.c2p(1, 0)[0] - cx.c2p(0, 0)[0], color=WHITE, stroke_width=2).move_to(cx.c2p(0, 0))
        c_l = MathTex(r"\varphi(z) = \exp\Big(-\frac{1 + z}{1 - z}\Big)", font_size=28).next_to(cx, UP, buff=0.12)
        th = np.linspace(0.05, 2 * np.pi - 0.05, 400)
        assert np.allclose(np.abs(inner(np.exp(1j * th))), 1, atol=1e-12)
        rows = VGroup(
            label(r"an \emph{inner} function: \ $|\varphi| = 1$ on the circle,", font_size=24),
            label(r"no zeros, \ and it crushes everything near $z = 1$", font_size=24),
            label(r"\textbf{RCA 17.21} \ (Beurling, 1949) \ every closed subspace", font_size=24, color=C.EPS),
            label(r"$M \ne \{0\}$ of $H^2$ with $SM \subset M$ is $\varphi H^2$", font_size=24, color=C.EPS),
            label(r"for an inner function $\varphi$", font_size=24, color=C.EPS),
            label(r"the first theorem about an operator's invariant subspaces", font_size=22, color=GREY_A),
            label(r"also on the tour: \ F.~and M.~Riesz (17.13), \ Mergelyan (20.5),", font_size=22, color=GREY_A),
            label(r"Paley--Wiener (19.3, \ in Part 9)", font_size=22, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.13).move_to([2.6, -0.6, 0])
        for r_ in rows:
            if r_.width > 7.0:
                r_.width = 7.0
        head = label(r"Which subspaces does the shift leave invariant?", font_size=34).to_edge(UP, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Which closed subspaces does the shift map into themselves? Beurling's answer: "
            "exactly the multiples of an inner function, a bounded holomorphic function with size one on the "
            "circle. <bookmark mark='b'/> This one has no zeros at all, yet it presses everything near the point one "
            "down to nothing: an essential singularity on the boundary. <bookmark mark='c'/> It's the first theorem "
            "of the series about the invariant subspaces of an operator, and the tour ends here. Part 9 will use the "
            "Paley-Wiener theorem from the same part of the book."
        ) as vo:
            self.add(tour_tag())
            vo.wait_until("a")
            self.play(FadeIn(head), FadeIn(rows[2:5]))
            vo.wait_until("b")
            self.play(FadeIn(img), Create(unit), FadeIn(c_l), FadeIn(rows[:2]))
            vo.wait_until("c")
            self.play(FadeIn(rows[5:]))
        self.wait(0.4)
        self.clear_scene()
