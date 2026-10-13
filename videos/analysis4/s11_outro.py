from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis4.common import plain_axes, polyline


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.ledger_row()
        self.next_time()
        self.credits()

    # ------------------------------------------------------------------
    def recap(self):
        items = [
            (r"linear maps: \ the norm is the largest stretch; \ invertible maps form an open set", C.OPERATOR),
            (r"the derivative is the linear map you see when you zoom in", C.FUNC),
            (r"partial derivatives are not enough; \ continuous ones are", C.PATHOLOGY),
            (r"the contraction principle: \ iterate, and converge, \ in any complete space", C.EPS),
            (r"Picard: \ $y' = F(t, y)$ solved as a fixed point in $C[a, b]$", C.APPROX),
            (r"the inverse function theorem: \ invertible derivative, \ local inverse", C.CONNECTED_SET),
            (r"the implicit function theorem: \ $f_y \ne 0$, \ the level set is a graph", C.CLOSED_SET),
            (r"mixed partials commute when continuous; \ $\frac{d}{dt}\int = \int \frac{\partial}{\partial t}$",
             C.MEASURE),
            (r"change of variables, \ partitions of unity, \ Stokes, \ closed vs exact", C.SEQ),
        ]
        rows = VGroup(*[label(rf"{i + 1}.\; {t}", font_size=28, color=c) for i, (t, c) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to(DOWN * 0.3)
        head = label(r"Part 4, in nine lines", font_size=40).to_edge(UP, buff=0.3)
        with self.voiceover(
            "Let's take stock. Linear maps have a norm, the largest stretch, and the invertible ones form an open "
            "set. The derivative is the linear map you see when you zoom in, and continuous partial derivatives "
            "always make one. The contraction principle solves equations by iteration in any complete space: "
            "differential equations in the space of continuous functions, and the inverse and implicit function "
            "theorems. Mixed partial derivatives commute when they're continuous, and derivatives pass through "
            "integrals. And chapter ten's tour ended at Stokes' theorem, where integrals detect holes."
        ) as vo:
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.5),
                      run_time=max(4.0, vo.duration - 2.0))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ledger_row(self):
        before = ledger(filled=3, highlight=4).scale(0.95)
        after = ledger(filled=4, highlight=4).scale(0.95)
        with self.voiceover(
            "The ledger's fourth row. <bookmark mark='a'/> The spaces: R n, and the continuous functions again. "
            "Completeness now pays off as fixed points of contractions. Compact sets are the same as before. The new "
            "swap: a derivative may pass through an integral when everything is continuous on a closed box. And "
            "Fourier's question hasn't moved; it waits for a better integral."
        ) as vo:
            self.play(FadeIn(before))
            vo.wait_until("a")
            self.play(LaggedStart(*[TransformFromCopy(after.rows[3][i], after.rows[3][i])
                                    for i in range(len(after.rows[3]))], lag_ratio=0.6),
                      FadeOut(before.rows[3]), run_time=6)
        self.wait(0.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_time(self):
        head = label(r"Next: Part 5, \ Measure and the Lebesgue integral", font_size=38).to_edge(UP, buff=0.3)
        ax = plain_axes([0, 1, 0.25], [0, 1.1, 0.5], 6.0, 3.4).move_to([-3.75, -0.6, 0])
        x = np.union1d(np.linspace(0, 1, 4001), np.arange(121) / 120)  # include every spike centre k / 5!

        def g(m, n):
            return np.cos(math.factorial(m) * np.pi * x) ** (2 * n)

        shown = [(1, 1), (2, 2), (3, 4), (3, 40), (4, 60), (5, 200)]
        for m, n in shown:
            y = g(m, n)
            assert y.min() >= 0 and y.max() <= 1 + 1e-12
        # at a rational p/q with q | m!, cos(m! pi x) = +-1, so the limit in n is 1; otherwise it tends to 0
        assert abs(math.cos(math.factorial(4) * math.pi * (3 / 8)) ** 2 - 1) < 1e-12
        curves = [polyline(ax, x, g(m, n), color=C.APPROX, stroke_width=2 if n < 50 else 1.4) for m, n in shown]
        labs = [MathTex(rf"\cos(m!\,\pi x)^{{2n}}, \quad m = {m},\ n = {n}", font_size=28, color=C.APPROX)
                .next_to(ax, UP, buff=0.1) for m, n in shown]
        lim = MathTex(r"\lim_{m \to \infty} \lim_{n \to \infty} \cos(m!\,\pi x)^{2n} = "
                      r"\begin{cases} 1 & x \in \mathbb Q \\ 0 & x \notin \mathbb Q \end{cases}", font_size=32,
                      color=C.PATHOLOGY)
        if lim.width > 6.2:
            lim.width = 6.2
        lim.next_to([-0.2, 0.6, 0], RIGHT, buff=0)
        q = VGroup(label(r"Dirichlet's function: \ a double limit of continuous functions", font_size=24),
                   label(r"that Riemann cannot integrate", font_size=24, color=C.PATHOLOGY),
                   label(r"Lebesgue can: \ and then limits pass under $\int$", font_size=24, color=C.EPS),
                   label(r"with no uniformity at all", font_size=24, color=C.EPS),
                   ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to([-0.2, -1.6, 0], RIGHT, buff=0)
        if q.get_right()[0] > 6.9:
            q.shift((6.9 - q.get_right()[0]) * RIGHT)
        with self.voiceover(
            "Next time, in Part 5, measure, and Lebesgue's integral. <bookmark mark='a'/> Raise cosine of m factorial "
            "pi x to a higher and higher even power, then let m grow. <bookmark mark='b'/> The functions are "
            "continuous, but in the limit they become Dirichlet's function: one at the rationals, zero elsewhere, "
            "which Part 3 showed has no Riemann integral. <bookmark mark='c'/> Lebesgue's integral handles it, and "
            "under it, limits pass through integrals without any uniformity at all."
        ) as vo:
            self.play(FadeIn(head), Create(ax))
            vo.wait_until("a")
            self.play(Create(curves[0]), FadeIn(labs[0]))
            cur, cl = curves[0], labs[0]
            for k in range(1, len(shown)):
                self.play(ReplacementTransform(cur, curves[k]), FadeTransform(cl, labs[k]), run_time=1.0)
                cur, cl = curves[k], labs[k]
            vo.wait_until("b")
            self.play(FadeIn(lim), FadeIn(q[:2]))
            vo.wait_until("c")
            self.play(FadeIn(q[2:]))
        self.wait(0.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def credits(self):
        lines = VGroup(
            label(r"Following W.~Rudin, \textit{Principles of Mathematical Analysis}, 3rd ed.\ (1976), chapter 9, "
                  r"and a tour of chapter 10", font_size=24),
            label(r"I.~Newton, \ A.-L.~Cauchy, \ R.~Lipschitz, \ G.~Peano (1890), \ \'E.~Picard (1890), "
                  r"\ S.~Banach (1922)", font_size=22, color=GREY_A),
            label(r"U.~Dini (the implicit function theorem, 1878), \ H.~A.~Schwarz (mixed partials), \ "
                  r"G.~Green (1828), \ G.~G.~Stokes, \ H.~Poincar\'e", font_size=22, color=GREY_A),
            label(r"Companions: \ C.~Pugh, \textit{Real Mathematical Analysis}, ch.~4--5; \ M.~Spivak, "
                  r"\textit{Calculus on Manifolds}", font_size=22, color=GREY_A),
            label(r"Every number on screen is computed and checked; schematics are labeled.", font_size=24, color=C.EPS),
            label(r"Animated with Manim Community; narrated by Kokoro-82M.", font_size=22, color=GREY_B),
        ).arrange(DOWN, buff=0.3).move_to(UP * 0.2)
        with self.voiceover(
            "This part followed chapter nine of Rudin's Principles of Mathematical Analysis, with a tour of chapter "
            "ten. Thanks for watching, and see you in Part 5."
        ):
            self.play(LaggedStart(*[FadeIn(l_, shift=UP * 0.1) for l_ in lines], lag_ratio=0.25), run_time=3)
        self.wait(2.0)
        self.play(FadeOut(lines))
