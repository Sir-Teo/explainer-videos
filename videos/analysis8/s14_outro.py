from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis8.common import plain_axes, polyline


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.ledger_row()
        self.next_time()
        self.credits()

    # ------------------------------------------------------------------
    def recap(self):
        items = [
            (r"Banach spaces; \ bounded $=$ continuous; \ $\|V\| = 2/\pi$", C.OPERATOR),
            (r"Fr\'echet spaces need many seminorms; \ no compact balls in infinite dimensions", C.INNER),
            (r"Baire: \ complete spaces are not countable unions of thin sets", C.EPS),
            (r"uniform boundedness: \ most continuous functions have divergent Fourier series", C.PATHOLOGY),
            (r"open mappings, \ bounded inverses, \ closed graphs, \ Hellinger--Toeplitz", C.OPERATOR),
            (r"Hahn--Banach: \ the sandwich; \ separation; \ enough functionals", C.FUNCTIONAL),
            (r"duals: \ $\ell^q$, $\ell^1$, $\ell^\infty$, \ measures; \ reflexivity", C.FUNCTIONAL),
            (r"weak convergence: \ oscillate, concentrate, escape; \ Mazur", C.INNER),
            (r"Banach--Alaoglu: \ dual balls are weak-$*$ compact", C.EPS),
            (r"Krein--Milman; \ $L^1$ has no extreme points, \ so it is no dual", C.CONNECTED_SET),
            (r"compact operators: \ the string's modes; \ Fredholm's alternative", C.OPERATOR),
            (r"Banach limits, \ Grothendieck, \ Haar measure, \ an uncomplemented subspace", GREY_A),
        ]
        rows = VGroup(*[label(rf"{i + 1}.\; {t}", font_size=25, color=c) for i, (t, c) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.13).move_to(DOWN * 0.35)
        head = label(r"Part 8, in twelve lines", font_size=40).to_edge(UP, buff=0.3)
        with self.voiceover(
            "Let's take stock. Banach spaces gathered the complete spaces of earlier parts into one family, where "
            "continuity means boundedness, and where the unit ball is never compact. Baire's theorem gave uniform "
            "boundedness, which proved that most continuous functions have divergent Fourier series; and it gave the "
            "open mapping and closed graph theorems. Hahn-Banach supplied enough functionals, and duality identified "
            "them. Weak convergence and the Banach-Alaoglu theorem brought compactness back, Krein-Milman found the "
            "corners, and compact operators kept linear algebra alive."
        ) as vo:
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.5),
                      run_time=max(4.0, vo.duration - 2.0))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ledger_row(self):
        before = ledger(filled=7, highlight=8).scale(0.95)
        after = ledger(filled=8, highlight=8).scale(0.95)
        with self.voiceover(
            "The ledger's eighth row. <bookmark mark='a'/> The spaces: Banach and Fréchet. <bookmark mark='c2'/> Completeness pays through "
            "Baire's theorem. <bookmark mark='c3'/> Compactness returns in the weak-star topology. <bookmark mark='c4'/> The new interchange: pointwise bounds "
            "become uniform bounds. <bookmark mark='c5'/> And the Fourier answer is now sharp: divergence for most continuous functions, and, "
            "by Carleson's theorem, convergence almost everywhere for square-integrable ones."
        ) as vo:
            self.play(FadeIn(before))
            vo.wait_until("a")
            self.play(FadeOut(before.rows[7]), *[TransformFromCopy(after.rows[7][i], after.rows[7][i]) for i in (0, 1)],
                      Indicate(before.head[1], color=C.EPS), run_time=1.5)
            for k_ in range(2, len(after.rows[7])):  # each cell arrives with its sentence
                vo.wait_until(f"c{k_}")
                self.play(TransformFromCopy(after.rows[7][k_], after.rows[7][k_]),
                          Indicate(before.head[k_], color=C.EPS), run_time=1.2)
        self.wait(0.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_time(self):
        head = label(r"Next: Part 9, \ distributions and the Fourier transform", font_size=36).to_edge(UP, buff=0.3)
        ax = plain_axes([-2, 2, 1], [-1.2, 2.2, 1], 5.2, 3.2).move_to([-3.4, -0.5, 0])
        x = np.linspace(-2, 2, 2001)
        g_abs = polyline(ax, x, np.abs(x), color=C.FUNC, stroke_width=3.5)
        g_sgn = VGroup(Line(ax.c2p(-2, -1), ax.c2p(0, -1), color=C.APPROX, stroke_width=3.5),
                       Line(ax.c2p(0, 1), ax.c2p(2, 1), color=C.APPROX, stroke_width=3.5))
        epsT = ValueTracker(0.5)

        def bump():  # the derivative of the smoothed sign erf(x / (e sqrt 2)): a Gaussian of total mass 2
            e = epsT.get_value()
            y = 2 * np.exp(-x * x / (2 * e * e)) / (e * math.sqrt(2 * math.pi))
            g = VGroup(polyline(ax, x, np.minimum(y, 2.2), color=C.EPS, stroke_width=3))
            if y.max() > 2.2:  # off the top of the axes: say so
                g.add(Arrow(ax.c2p(0, 1.75), ax.c2p(0, 2.55), buff=0, color=C.EPS, stroke_width=3,
                            max_tip_length_to_length_ratio=0.35))
            return g

        xx_ = np.linspace(-2, 2, 200001)
        for e_ in (0.5, 0.08):
            m_ = np.sum(2 * np.exp(-xx_**2 / (2 * e_ * e_)) / (e_ * math.sqrt(2 * math.pi))) * (xx_[1] - xx_[0])
            assert abs(m_ - 2) < 2e-3  # mass two

        bp = always_redraw(bump)
        lab = VGroup(MathTex(r"|x|", font_size=28, color=C.FUNC).next_to(ax.c2p(1.5, 1.5), DR, buff=0.1),
                     MathTex(r"|x|' = \operatorname{sign} x", font_size=26, color=C.APPROX).next_to(ax.c2p(1.0, -0.9), RIGHT,
                                                                                                buff=0.1),
                     MathTex(r"(\operatorname{sign} x)' = 2\delta", font_size=26, color=C.EPS).next_to(ax.c2p(0.2, 1.9),
                                                                                                    RIGHT, buff=0.1))
        side = VGroup(
            label(r"differentiate anything: \ $f' $ is defined by", font_size=26),
            MathTex(r"\langle f', \varphi\rangle = -\langle f, \varphi'\rangle", font_size=32, color=C.EPS),
            label(r"for smooth test functions $\varphi$ \ (a Fr\'echet-type space)", font_size=24, color=GREY_A),
            label(r"the Fourier transform, \ Plancherel, \ Sobolev spaces,", font_size=26),
            label(r"and the equations of physics", font_size=26),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([3.4, -0.4, 0])
        with self.voiceover(
            "Next time, in Part 9: distributions. <bookmark mark='a'/> The absolute value has a corner, but its "
            "derivative is the sign function. The sign function jumps, and its derivative is a spike of total mass "
            "two, the Dirac delta, which no function can be. <bookmark mark='b'/> Distributions make that honest: "
            "define the derivative by moving it onto smooth test functions. Then everything can be differentiated, "
            "and the Fourier transform becomes a symmetry of the whole theory."
        ) as vo:
            self.play(FadeIn(head), Create(ax), Create(g_abs), FadeIn(lab[0]))
            vo.wait_until("a")
            self.play(Create(g_sgn), FadeIn(lab[1]))
            self.add(bp)
            self.play(epsT.animate.set_value(0.08), FadeIn(lab[2]), run_time=3.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.1) for r_ in side], lag_ratio=0.4), run_time=3.0)
        bp.clear_updaters()
        self.wait(0.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def credits(self):
        lines = VGroup(
            label(r"Following W.~Rudin, \textit{Real and Complex Analysis}, chapter 5, \ and \textit{Functional Analysis}, "
                  r"2nd ed.\ (1991), chapters 1--5", font_size=22),
            label(r"S.~Banach (1932), \ H.~Steinhaus, \ R.~Baire (1899), \ H.~Hahn (1927), \ L.~Alaoglu (1940), "
                  r"\ M.~Krein and D.~Milman (1940)", font_size=22, color=GREY_A),
            label(r"P.~du Bois-Reymond (1873), \ L.~Carleson (1966), \ A.~Grothendieck, \ A.~Haar (1933), "
                  r"\ R.~S.~Phillips (1940)", font_size=22, color=GREY_A),
            label(r"Companions: \ P.~Lax, \textit{Functional Analysis}; \ H.~Brezis, \textit{Functional Analysis, Sobolev "
                  r"Spaces and PDE}", font_size=22, color=GREY_A),
            label(r"Every number on screen is computed and checked; \ the pictures marked schematic are the exceptions.",
                  font_size=24, color=C.EPS),
            label(r"Animated with Manim Community; narrated by Kokoro-82M.", font_size=22, color=GREY_B),
        ).arrange(DOWN, buff=0.3).move_to(UP * 0.2)
        with self.voiceover(
            "This part followed chapter five of Real and Complex Analysis and the first five chapters of Functional "
            "Analysis. Thanks for watching, and see you in Part 9."
        ):
            self.play(LaggedStart(*[FadeIn(l_, shift=UP * 0.1) for l_ in lines], lag_ratio=0.25), run_time=3)
        self.wait(2.0)
        self.play(FadeOut(lines))
