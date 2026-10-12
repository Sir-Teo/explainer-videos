from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis9.common import plain_axes


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.ledger_row()
        self.next_time()
        self.credits()

    # ------------------------------------------------------------------
    def recap(self):
        items = [
            (r"test functions: \ smooth bumps with compact support, \ an inductive limit of Fr\'echet spaces", C.TEST_FN),
            (r"distributions: \ continuous functionals; \ $\delta$, \ $\delta'$, \ p.v.\,$1/x$, \ combs", C.DISTRIBUTION),
            (r"differentiate anything: \ $\langle T', \varphi\rangle = -\langle T, \varphi'\rangle$; \ Fourier was right",
             C.EPS),
            (r"supports; \ one-point distributions; \ locally a derivative of a continuous function", C.DISTRIBUTION),
            (r"convolution smooths; \ every distribution is a limit of test functions", C.APPROX),
            (r"the Fourier transform: \ pairs, \ rules, \ the self-dual Gaussian, \ uncertainty", C.FREQ),
            (r"inversion with Gibbs; \ Plancherel: \ a unitary map of $L^2$", C.INNER),
            (r"$\mathcal S$ and $\mathcal S'$: \ a quarter turn; \ $\hat\delta$ constant; \ Poisson summation", C.FREQ),
            (r"Paley--Wiener: \ support is growth; \ Denjoy--Carleman", C.SPECTRUM),
            (r"Sobolev: \ $s > k + n/2$ buys $C^k$; \ the sawtooth sits at $s = \tfrac12$", C.EPS),
            (r"fundamental solutions: \ contours around the zeros; \ Malgrange--Ehrenpreis", C.OPERATOR),
            (r"Wiener's Tauberian theorem, \ and the prime number theorem", C.EPS),
        ]
        rows = VGroup(*[label(rf"{i + 1}.\; {t}", font_size=25, color=c) for i, (t, c) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.13).move_to(DOWN * 0.35)
        for r_ in rows:
            if r_.width > 13.0:
                r_.width = 13.0
        head = label(r"Part 9, in twelve lines", font_size=40).to_edge(UP, buff=0.3)
        with self.voiceover(
            "Let's take stock. Test functions gave us a way to ask what an object does instead of what it is, and the "
            "answer was distributions, which can all be differentiated, as often as we like. Locally they're all "
            "derivatives of continuous functions, and smoothing turns them back into functions. The Fourier transform "
            "became a unitary map of L two, a quarter turn of the Schwartz space, and an operation on tempered "
            "distributions. Paley-Wiener read support as growth, Sobolev read smoothness as decay, fundamental "
            "solutions dodged the zeros of symbols, and Wiener's algebra led all the way to the primes."
        ) as vo:
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.5),
                      run_time=max(4.0, vo.duration - 2.0))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ledger_row(self):
        before = ledger(filled=8, highlight=9).scale(0.95)
        after = ledger(filled=9, highlight=9).scale(0.95)
        with self.voiceover(
            "The ledger's ninth row. <bookmark mark='a'/> The spaces: test functions, Schwartz functions, and their "
            "duals. Completeness comes in Fréchet pieces, and compactness from weak-star limits of bounded sets. The "
            "interchange is finally free: differentiation commutes with every limit. And the Fourier answer is the "
            "most generous yet: every trigonometric series with coefficients of polynomial size converges, as a "
            "distribution."
        ) as vo:
            self.play(FadeIn(before))
            vo.wait_until("a")
            self.play(LaggedStart(*[TransformFromCopy(after.rows[8][i], after.rows[8][i])
                                    for i in range(len(after.rows[8]))], lag_ratio=0.6),
                      FadeOut(before.rows[8]), run_time=6)
        self.wait(0.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_time(self):
        head = label(r"Next: Part 10, \ Banach algebras and the spectral theorem", font_size=36).to_edge(UP, buff=0.3)
        # the Volterra operator V f(x) = int_0^x f on L^2[0, 1]: ||V|| = 2/pi, no eigenvalues, ||V^n||^(1/n) -> 0
        N = 600
        h = 1.0 / N
        V = np.tril(np.full((N, N), h), -1) + np.eye(N) * h / 2  # midpoint rule
        norms, P = [], np.eye(N)
        for n in range(1, 13):
            P = P @ V
            norms.append(np.linalg.norm(P, 2) ** (1 / n))
        norms = np.array(norms)
        assert abs(norms[0] - 2 / math.pi) < 1e-3 and np.all(np.diff(norms) < 0)
        # ||V^n|| is about 1/n! (up to a factor), so ||V^n||^(1/n) is about e/n
        ax = plain_axes([0, 13, 2], [0, 0.7, 0.2], 6.0, 3.2, numbers=True, font_size=18,
                        x_axis_config={"decimal_number_config": {"num_decimal_places": 0}},
                        y_axis_config={"decimal_number_config": {"num_decimal_places": 1}}).move_to([-3.3, -0.4, 0])
        dots = VGroup(*[Dot(ax.c2p(n, v), radius=0.06, color=C.OPERATOR) for n, v in zip(range(1, 13), norms)])
        nl = MathTex(r"n", font_size=22).next_to(ax.x_axis, RIGHT, buff=0.1)
        top = MathTex(r"\|V^n\|^{1/n}, \ \ Vf(x) = \int_0^x f", font_size=28, color=C.OPERATOR).next_to(ax, UP, buff=0.15)
        side = VGroup(
            MathTex(rf"\|V\| = {norms[0]:.4f} \approx 2/\pi \ \ (\text{{Part 8}})", font_size=26),
            MathTex(rf"\|V^{{12}}\|^{{1/12}} = {norms[-1]:.4f} \to 0", font_size=26, color=C.OPERATOR),
            label(r"no eigenvalues at all, \ yet a spectrum: \ $\sigma(V) = \{0\}$", font_size=24, color=C.SPECTRUM),
            MathTex(r"r(T) = \lim_n \|T^n\|^{1/n} = \max |\sigma(T)|", font_size=30, color=C.EPS),
            label(r"Gelfand: \ the spectral radius formula, \ from Part 7's Cauchy formula", font_size=22,
                  color=GREY_A),
            label(r"and the spectral theorem: \ diagonalizing self-adjoint operators", font_size=24),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([3.5, -0.3, 0])
        for r_ in side:
            if r_.width > 6.6:
                r_.width = 6.6
        with self.voiceover(
            "Next time, in Part 10: operators, and their spectra. <bookmark mark='a'/> Part 8's Volterra operator, "
            "integration from zero, has norm two over pi. Its powers shrink, and the n-th root of the norm of the n-th "
            "power goes to zero. <bookmark mark='b'/> It has no eigenvalues at all, yet it has a spectrum: the single "
            "point zero. Gelfand's spectral radius formula, built from Part 7's complex analysis, explains why. "
            "<bookmark mark='c'/> And then the spectral theorem: how to diagonalize an operator that has no "
            "eigenvectors."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(nl), FadeIn(top))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d_, scale=0.5) for d_ in dots], lag_ratio=0.2), FadeIn(side[:2]), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(side[2:5]))
            vo.wait_until("c")
            self.play(FadeIn(side[5]))
        self.wait(0.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def credits(self):
        lines = VGroup(
            label(r"Following W.~Rudin, \textit{Real and Complex Analysis}, chapters 9 and 19, \ and \textit{Functional "
                  r"Analysis}, 2nd ed.\ (1991), chapters 6--9", font_size=22),
            label(r"L.~Schwartz (1945--50), \ S.~Sobolev (1938), \ R.~Paley and N.~Wiener (1934), \ N.~Wiener (1932), "
                  r"\ A.~Denjoy (1921), \ T.~Carleman (1926)", font_size=22, color=GREY_A),
            label(r"B.~Malgrange (1955), \ L.~Ehrenpreis (1954), \ J.~Hadamard and C.~de la Vall\'ee Poussin (1896)",
                  font_size=22, color=GREY_A),
            label(r"Companions: \ R.~Strichartz, \textit{A Guide to Distribution Theory and Fourier Transforms}; \ "
                  r"L.~H\"ormander, \textit{ALPDO I}", font_size=22, color=GREY_A),
            label(r"Every number on screen is computed and checked; \ the pictures marked schematic are the exceptions.",
                  font_size=24, color=C.EPS),
            label(r"Animated with Manim Community; narrated by Kokoro-82M.", font_size=22, color=GREY_B),
        ).arrange(DOWN, buff=0.3).move_to(UP * 0.2)
        for l_ in lines:
            if l_.width > 13.2:
                l_.width = 13.2
        with self.voiceover(
            "This part followed chapter nine of Real and Complex Analysis and chapters six through nine of Functional "
            "Analysis. Thanks for watching, and see you in Part 10."
        ):
            self.play(LaggedStart(*[FadeIn(l_, shift=UP * 0.1) for l_ in lines], lag_ratio=0.25), run_time=3)
        self.wait(2.0)
        self.play(FadeOut(lines))
