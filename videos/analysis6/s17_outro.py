from __future__ import annotations

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis6.common import square_axes


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.ledger_row()
        self.next_time()
        self.credits()

    # ------------------------------------------------------------------
    def recap(self):
        items = [
            (r"convexity and Jensen: \ the average of $\varphi$ beats $\varphi$ of the average", C.EPS),
            (r"Young's two areas $\Rightarrow$ H\"older $\Rightarrow$ Minkowski: \ the $p$-norms are norms", C.DIST),
            (r"$L^p$: \ classes of functions equal a.e.; \ $L^1$ and $L^2$ do not contain each other on $\R$", C.FUNC),
            (r"Riesz--Fischer: \ summable steps, \ so $L^p$ is complete", C.MEASURE),
            (r"inner products; \ only $L^2$ satisfies the parallelogram law", C.INNER),
            (r"the nearest point, \ and projection onto a subspace", C.CONNECTED_SET),
            (r"every functional on $H$ is $\langle \cdot, y\rangle$", C.FUNCTIONAL),
            (r"Gram--Schmidt, \ Bessel, \ Parseval: \ $H \cong \ell^2$", C.INNER),
            (r"Fourier: \ $s_N \to f$ in $L^2$ for every $f \in L^2$; \ Fej\'er: uniform for continuous $f$", C.EPS),
            (r"complex measures; \ total variation is a length", C.MEASURE),
            (r"Radon--Nikodym, \ by von Neumann's Hilbert-space proof", C.APPROX),
            (r"$(L^p)^* = L^q$; \ $C_0(X)^*$ is the space of measures", C.FUNCTIONAL),
            (r"Lebesgue points: \ $\frac{d}{dx}\int_a^x f = f$ a.e.; \ Vitali's $3\times$", C.SEQ),
            (r"absolute continuity is the FTC; \ the Cantor function is not", C.PATHOLOGY),
            (r"change of variables: \ the factor $|J_T|$, \ and $\int e^{-x^2} = \sqrt\pi$", C.CLOSED_SET),
        ]
        rows = VGroup(*[label(rf"{i + 1}.\; {t}", font_size=24, color=c) for i, (t, c) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to(DOWN * 0.35)
        head = label(r"Part 6, in fifteen lines", font_size=40).to_edge(UP, buff=0.25)
        with self.voiceover(
            "Let's take stock. Convexity gave Jensen's inequality, and Young's two areas gave Hölder and Minkowski, "
            "so the p-norms really are distances. The spaces L p consist of classes of functions, and Riesz and "
            "Fischer showed they're complete. Among them, only L two has an inner product, and with it come nearest "
            "points, the representation of functionals by vectors, and orthonormal bases with Parseval's identity. "
            "That answered the Fourier question in L two, while Fejér's means converge uniformly. Then measures "
            "with signs and complex values, the Radon-Nikodym theorem, the duals of L p and of the continuous "
            "functions, Lebesgue's differentiation theorem, the fundamental theorem of calculus for absolutely "
            "continuous functions, and the change of variables formula."
        ) as vo:
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.5),
                      run_time=max(4.0, vo.duration - 2.0))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ledger_row(self):
        before = ledger(filled=5, highlight=6).scale(0.95)
        after = ledger(filled=6, highlight=6).scale(0.95)
        with self.voiceover(
            "The ledger's sixth row. <bookmark mark='a'/> The spaces: L p, and Hilbert space. <bookmark mark='c2'/> Complete, by Riesz and "
            "Fischer's summable steps. <bookmark mark='c3'/> Compactness still fails: the unit vectors stay root two apart. <bookmark mark='c4'/> The limits we "
            "may swap: the derivative of the integral is the function, almost everywhere. <bookmark mark='c5'/> And Fourier series "
            "converge in L two, for every square-integrable function, with Fejér's means converging uniformly."
        ) as vo:
            self.play(FadeIn(before))
            vo.wait_until("a")
            self.play(FadeOut(before.rows[5]), *[TransformFromCopy(after.rows[5][i], after.rows[5][i]) for i in (0, 1)],
                      Indicate(before.head[1], color=C.EPS), run_time=1.5)
            for k_ in range(2, len(after.rows[5])):  # each cell arrives with its sentence
                vo.wait_until(f"c{k_}")
                self.play(TransformFromCopy(after.rows[5][k_], after.rows[5][k_]),
                          Indicate(before.head[k_], color=C.EPS), run_time=1.2)
        self.wait(0.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_time(self):
        head = label(r"Next: Part 7, \ complex analysis", font_size=38).to_edge(UP, buff=0.3)
        S = 4.2
        ax = square_axes([-2, 2, 1], [-2, 2, 1], S / 4).move_to([-3.4, -0.3, 0])
        img = domain_image(lambda Z: (Z**3 - 1) / (Z**2 + 0.5), (-2, 2), (-2, 2), S, S).move_to(ax.c2p(0, 0))
        frame = Square(side_length=S, color=GREY_C, stroke_width=2).move_to(ax.c2p(0, 0))
        f_l = MathTex(r"f(z) = \frac{z^3 - 1}{z^2 + \frac12}", font_size=30).next_to(frame, DOWN, buff=0.15)
        key = label(r"color = $\arg f$, \ brightness = $|f|$", font_size=22, color=GREY_A).next_to(f_l, DOWN, buff=0.08)
        zeros = [np.exp(2j * np.pi * k / 3) for k in range(3)]
        poles = [1j / np.sqrt(2), -1j / np.sqrt(2)]
        for z in zeros:
            assert abs(z**3 - 1) < 1e-12
        zd = VGroup(*[Circle(radius=0.12, color=WHITE, stroke_width=2).move_to(ax.c2p(z.real, z.imag)) for z in zeros])
        pd = VGroup(*[Square(side_length=0.22, color=WHITE, stroke_width=2).move_to(ax.c2p(z.real, z.imag)) for z in poles])
        side = VGroup(
            label(r"one complex derivative \ $\Rightarrow$ \ infinitely many", font_size=26),
            label(r"a power series at every point", font_size=26),
            label(r"Cauchy's formula: \ boundary values decide the inside", font_size=26, color=C.EPS),
            label(r"zeros (circles) and poles (squares) \ tell the whole story", font_size=26),
            label(r"none of this is true on the real line \ (Part 2's $e^{-1/x^2}$)", font_size=24, color=C.PATHOLOGY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([3.3, -0.4, 0])
        for r_ in side:
            if r_.width > 6.4:
                r_.width = 6.4
        side.arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([3.3, -0.4, 0])
        with self.voiceover(
            "Next time, in Part 7: complex analysis, the part the rest of analysis needs. <bookmark mark='a'/> Here's "
            "a rational function, colored by its phase, with brightness for size. Its three zeros are dark points "
            "where every color meets; its two poles are bright. <bookmark mark='b'/> A function that's "
            "differentiable once in the complex sense is differentiable infinitely often, equals its power series, "
            "and is determined inside a region by its values on the boundary. None of that is true on the real "
            "line, and finding out why is the next part."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(img), Create(frame), FadeIn(f_l), FadeIn(key))
            self.play(Create(zd), Create(pd))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.1) for r_ in side], lag_ratio=0.5), run_time=4.0)
        self.wait(0.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def credits(self):
        lines = VGroup(
            label(r"Following W.~Rudin, \textit{Real and Complex Analysis}, 3rd ed.\ (1987), chapters 3, 4, 6 and 7",
                  font_size=24),
            label(r"J.~L.~W.~V.~Jensen (1906), \ O.~H\"older (1889), \ H.~Minkowski (1896), \ F.~Riesz and E.~Fischer (1907), "
                  r"\ L.~Fej\'er (1900)", font_size=22, color=GREY_A),
            label(r"J.~Radon (1913), \ O.~Nikodym (1930), \ J.~von Neumann (1940), \ G.~H.~Hardy and J.~E.~Littlewood (1930), "
                  r"\ G.~Vitali (1908)", font_size=22, color=GREY_A),
            label(r"Companions: \ E.~M.~Stein and R.~Shakarchi, \textit{Real Analysis}; \ G.~Folland, \textit{Real Analysis}",
                  font_size=22, color=GREY_A),
            label(r"Every number on screen is computed and checked; \ the pictures marked schematic are the exceptions.",
                  font_size=24, color=C.EPS),
            label(r"Animated with Manim Community; narrated by Kokoro-82M.", font_size=22, color=GREY_B),
        ).arrange(DOWN, buff=0.3).move_to(UP * 0.2)
        with self.voiceover(
            "This part followed chapters three, four, six and seven of Rudin's Real and Complex Analysis. Thanks for "
            "watching, and see you in Part 7."
        ):
            self.play(LaggedStart(*[FadeIn(l_, shift=UP * 0.1) for l_ in lines], lag_ratio=0.25), run_time=3)
        self.wait(2.0)
        self.play(FadeOut(lines))
