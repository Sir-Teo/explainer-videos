from __future__ import annotations

import numpy as np

from explainer.analysis import *  # noqa: F403


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.ledger_row()
        self.next_time()
        self.credits()

    # ------------------------------------------------------------------
    def recap(self):
        items = [
            (r"the integral: \ upper and lower sums squeeze; \ $U - L < \varepsilon$", C.UPPER_SUM),
            (r"continuous and monotone functions are integrable; \ Dirichlet's is not, \ Thomae's is", C.LOWER_SUM),
            (r"Stieltjes: \ integrate against a staircase, \ even the Cantor function", C.MEASURE),
            (r"the fundamental theorem; \ length $= \int |\gamma'|$; \ the Koch curve has none", C.FUNC),
            (r"uniform convergence: \ one $N$ for every $x$; \ the sup norm; \ the M-test", C.EPS),
            (r"uniform limits are continuous; \ Dini; \ $C(X)$ is complete", C.CONNECTED_SET),
            (r"integrals pass through uniform limits; \ derivatives need more", C.MEASURE),
            (r"Weierstrass: \ continuous everywhere, \ differentiable nowhere", C.PATHOLOGY),
            (r"equicontinuity: \ one $\delta$ for a whole family", C.DELTA),
            (r"Arzel\`a--Ascoli: \ bounded and equicontinuous $\Rightarrow$ a convergent subsequence", C.COMPACT_SET),
            (r"every continuous function is a uniform limit of polynomials", C.APPROX),
            (r"Stone--Weierstrass: \ separate points, vanish nowhere \ (and close under conjugation)", C.SEQ),
            (r"power series: \ $\exp$, $\cos$, $\sin$, and $\pi$, \ all from one series", C.FREQ),
            (r"Fourier: \ $s_N$ is the best approximation; \ Bessel; \ Dini's test", C.INNER),
            (r"Parseval: \ convergence in energy; \ $\sum 1/n^2 = \pi^2/6$; \ Gibbs' $9\%$", C.EPS),
        ]
        rows = VGroup(*[label(rf"{i + 1}.\; {t}", font_size=24, color=c) for i, (t, c) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to(DOWN * 0.3)
        head = label(r"Part 3, in fifteen lines", font_size=38).to_edge(UP, buff=0.25)
        with self.voiceover(
            "Let's take stock. We built the Riemann integral from upper and lower sums, found which functions it can "
            "integrate, and generalized it to integrals against a staircase. The fundamental theorem tied it to "
            "derivatives, and gave curves a length, though not every curve has one. Then the main problem: limits of "
            "functions. Uniform convergence makes limits pass through continuity and integrals, and turns the "
            "continuous functions into a complete space, where Weierstrass's monster lives. Equicontinuity is what "
            "compactness costs there, by Arzelà and Ascoli. Polynomials, and any algebra that separates points, "
            "approximate everything. Power series gave us the exponential and pi, and Fourier series turned out to be "
            "best approximations: they converge in energy, which summed one over n squared, and at jumps they "
            "overshoot by nine percent."
        ) as vo:
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.5),
                      run_time=max(4.0, vo.duration - 2.0))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ledger_row(self):
        before = ledger(filled=2, highlight=3).scale(0.95)
        after = ledger(filled=3, highlight=3).scale(0.95)
        with self.voiceover(
            "And the ledger gets its third row. <bookmark mark='a'/> The space: continuous functions on a compact set, "
            "with the sup norm. It's complete, because uniform limits of continuous functions are continuous. Its "
            "compact sets are the closed, bounded, equicontinuous ones. The swap it makes legal: the limit of the "
            "integrals is the integral of the limit, when the convergence is uniform. And Fourier's series: they "
            "converge in mean square, pointwise where the function is Lipschitz, and with Gibbs' overshoot at jumps."
        ) as vo:
            self.play(FadeIn(before))
            vo.wait_until("a")
            self.play(LaggedStart(*[TransformFromCopy(after.rows[2][i], after.rows[2][i])
                                    for i in range(len(after.rows[2]))], lag_ratio=0.6),
                      FadeOut(before.rows[2]), run_time=6)
        self.wait(0.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_time(self):
        head = label(r"Next: Part 4, \ Calculus in many dimensions", font_size=38).to_edge(UP, buff=0.3)

        def F(p):
            x, y = p
            return np.array([x + 0.35 * np.sin(1.4 * y), y + 0.35 * np.sin(1.4 * x)])

        def J(p):
            x, y = p
            return np.array([[1.0, 0.49 * np.cos(1.4 * y)], [0.49 * np.cos(1.4 * x), 1.0]])

        oL, oR, u = np.array([-4.3, -0.6, 0]), np.array([1.0, -0.6, 0]), 0.95

        def toL(q):
            return oL + u * np.array([q[0], q[1], 0])

        def toR(q):
            return oR + u * np.array([q[0], q[1], 0])

        t = np.linspace(-2, 2, 81)
        gridL, gridR = VGroup(), VGroup()
        for c in np.linspace(-2, 2, 9):
            for line in (np.c_[t, np.full_like(t, c)], np.c_[np.full_like(t, c), t]):
                gridL.add(VMobject(color=GREY_C, stroke_width=1.5).set_points_as_corners([toL(q) for q in line]))
                gridR.add(VMobject(color=C.OPERATOR, stroke_width=1.5).set_points_as_corners([toR(F(q)) for q in line]))
        p = np.array([0.5, 0.5])
        h = 0.5
        sq = np.array([p + [-h, -h], p + [h, -h], p + [h, h], p + [-h, h], p + [-h, -h]])
        sqL = Polygon(*[toL(q) for q in sq[:-1]], color=C.EPS, stroke_width=3, fill_opacity=0.15)
        edge = np.concatenate([np.linspace(sq[i], sq[i + 1], 30) for i in range(4)])
        imgR = VMobject(color=C.EPS, stroke_width=3).set_points_as_corners([toR(F(q)) for q in edge])
        lin = Polygon(*[toR(F(p) + J(p) @ (q - p)) for q in sq[:-1]], color=WHITE, stroke_width=2)
        lin = DashedVMobject(lin, num_dashes=40)
        arrow = Arrow(oL + RIGHT * 2.2, oR + LEFT * 2.2, buff=0.1, color=GREY_B, stroke_width=3)
        fl = MathTex(r"F", font_size=32, color=GREY_B).next_to(arrow, UP, buff=0.05)
        side = VGroup(label(r"the derivative is the linear map", font_size=24),
                      label(r"that best fits $F$ near a point", font_size=24),
                      MathTex(r"F(p + h) \approx F(p) + DF(p)\,h", font_size=30, color=C.EPS),
                      label(r"contractions, \ the inverse and", font_size=24, color=GREY_A),
                      label(r"implicit function theorems, \ and", font_size=24, color=GREY_A),
                      label(r"Picard's theorem: \ an ODE solved", font_size=24, color=GREY_A),
                      label(r"in the space $C[a, b]$ of this part", font_size=24, color=GREY_A),
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([5.3, -0.6, 0])
        with self.voiceover(
            "Next time, in Part 4, calculus in many dimensions. <bookmark mark='a'/> A map of the plane bends a square "
            "grid. <bookmark mark='b'/> Up close, it acts like a linear map: a small square goes to almost a "
            "parallelogram, the one the derivative predicts. In many dimensions the derivative is that linear map. "
            "<bookmark mark='c'/> From it come contractions, the inverse and implicit function theorems, and "
            "Picard's theorem, which solves differential equations by iterating in the space of continuous functions "
            "we just built."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Create(gridL), run_time=1.5)
            self.play(GrowArrow(arrow), FadeIn(fl), TransformFromCopy(gridL, gridR), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(sqL), Create(imgR))
            self.play(Create(lin), FadeIn(side[:3]))
            vo.wait_until("c")
            self.play(FadeIn(side[3:]))
        self.wait(0.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def credits(self):
        lines = VGroup(
            label(r"Following W.~Rudin, \textit{Principles of Mathematical Analysis}, 3rd ed.\ (1976), chapters 6--8",
                  font_size=24),
            label(r"B.~Riemann (1854), \ G.~Darboux (1875), \ T.~J.~Stieltjes (1894), \ H.~von Koch (1904), "
                  r"\ U.~Dini (1878)", font_size=22, color=GREY_A),
            label(r"K.~Weierstrass (1872, 1885), \ G.~Ascoli (1884), \ C.~Arzel\`a (1889), \ E.~Landau (1908), "
                  r"\ S.~Bernstein (1912)", font_size=22, color=GREY_A),
            label(r"M.~H.~Stone (1937, 1948), \ J.~Fourier (1807), \ P.~G.~L.~Dirichlet (1829), \ L.~Fej\'er (1900), "
                  r"\ J.~W.~Gibbs (1899)", font_size=22, color=GREY_A),
            label(r"Companions: S.~Abbott, \textit{Understanding Analysis}; \ C.~Pugh, \textit{Real Mathematical Analysis};"
                  r" \ T.~Tao, \textit{Analysis I}", font_size=22, color=GREY_A),
            label(r"Every number on screen is computed and checked; schematics are labeled.", font_size=24, color=C.EPS),
            label(r"Animated with Manim Community; narrated by Kokoro-82M.", font_size=22, color=GREY_B),
        ).arrange(DOWN, buff=0.3).move_to(UP * 0.2)
        with self.voiceover(
            "This part followed chapters six to eight of Rudin's Principles of Mathematical Analysis. Thanks for "
            "watching, and see you in Part 4."
        ):
            self.play(LaggedStart(*[FadeIn(l_, shift=UP * 0.1) for l_ in lines], lag_ratio=0.25), run_time=3)
        self.wait(2.0)
        self.play(FadeOut(lines))
