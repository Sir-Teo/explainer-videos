from __future__ import annotations

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis7.common import plain_axes


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.ledger_row()
        self.next_time()
        self.credits()

    # ------------------------------------------------------------------
    def recap(self):
        items = [
            (r"the exponential: \ $e^{2\pi i} = 1$ and $\pi$, \ from one series", C.EPS),
            (r"complex derivatives are rotations: \ Cauchy--Riemann; \ conformal maps", C.SEQ),
            (r"path integrals; \ winding numbers are integers; \ Goursat's bisection", C.APPROX),
            (r"Cauchy's formula: \ power series, \ Liouville, \ the fundamental theorem of algebra", C.EPS),
            (r"isolated zeros, \ the identity theorem, \ open maps, \ maximum modulus", C.CONNECTED_SET),
            (r"residues: \ real integrals from the complex plane; \ Rouch\'e", C.MEASURE),
            (r"Schwarz's lemma, \ the disk's symmetries, \ three lines", C.INNER),
            (r"Runge: \ polynomials approximate when the poles can escape", C.CONNECTED_SET),
            (r"Montel: \ bounded families are normal", C.EPS),
            (r"Riemann mapping, \ computed for an L-shaped hexagon", C.APPROX),
            (r"tours: \ Poisson's integral; \ Weierstrass products; \ Blaschke; \ continuation", GREY_A),
            (r"$H^2$ and the shift: \ Beurling's invariant subspaces", C.FUNCTIONAL),
        ]
        rows = VGroup(*[label(rf"{i + 1}.\; {t}", font_size=25, color=c) for i, (t, c) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.13).move_to(DOWN * 0.35)
        head = label(r"Part 7, in twelve lines", font_size=40).to_edge(UP, buff=0.3)
        with self.voiceover(
            "Let's take stock. Everything grew from one series, the exponential. A complex derivative is a rotation "
            "and a scaling, so holomorphic maps preserve angles. Integrals around closed paths count turns, and "
            "Goursat's bisection proves Cauchy's theorem. Cauchy's formula then gives power series, Liouville's "
            "theorem, and the fundamental theorem of algebra; zeros are isolated, maps are open, and the maximum is "
            "on the boundary. Residues compute real integrals. Schwarz's lemma pins down the disk's symmetries, "
            "Runge's theorem says when polynomials approximate, and Montel's theorem gives compactness, which builds "
            "the Riemann map. Then a tour, ending with the shift operator."
        ) as vo:
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.5),
                      run_time=max(4.0, vo.duration - 2.0))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ledger_row(self):
        before = ledger(filled=6, highlight=7).scale(0.95)
        after = ledger(filled=7, highlight=7).scale(0.95)
        with self.voiceover(
            "The ledger's seventh row. <bookmark mark='a'/> The space: holomorphic functions on a region, with "
            "locally uniform convergence. It's complete, because locally uniform limits of holomorphic functions are "
            "holomorphic. Its compact sets are the bounded ones, by Montel. Power series may be differentiated term "
            "by term, and the Cauchy integral commutes with limits. And on the Fourier side: H two, the functions "
            "with no negative frequencies."
        ) as vo:
            self.play(FadeIn(before))
            vo.wait_until("a")
            self.play(LaggedStart(*[TransformFromCopy(after.rows[6][i], after.rows[6][i])
                                    for i in range(len(after.rows[6]))], lag_ratio=0.6),
                      FadeOut(before.rows[6]), run_time=6)
        self.wait(0.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_time(self):
        head = label(r"Next: Part 8, \ Banach spaces", font_size=38).to_edge(UP, buff=0.3)
        ax = plain_axes([0.5, 12.5, 1], [0, 1.15, 0.5], 6.0, 2.4).move_to([-3.3, 0.6, 0])
        nT = ValueTracker(1)
        y = 1 / np.arange(1, 13)

        def bar():
            n = int(round(nT.get_value()))
            return VGroup(Rectangle(width=0.3, height=ax.c2p(0, 1)[1] - ax.c2p(0, 0)[1], stroke_width=0, fill_color=C.EPS,
                                    fill_opacity=0.9).move_to(ax.c2p(n, 0.5)),
                          MathTex(rf"e_{{{n}}}", font_size=26, color=C.EPS).next_to(ax.c2p(n, 1), UP, buff=0.08))

        eb = always_redraw(bar)
        ydots = VGroup(*[Dot(ax.c2p(k + 1, v), radius=0.05, color=C.INNER) for k, v in enumerate(y)])
        y_l = MathTex(r"y = (1, \tfrac12, \tfrac13, \ldots)", font_size=24, color=C.INNER).next_to(ax, DOWN, buff=0.15)
        rd = always_redraw(lambda: VGroup(
            MathTex(rf"\|e_n\| = 1", font_size=28),
            MathTex(rf"\langle e_n, y\rangle = \tfrac{{1}}{{{int(round(nT.get_value()))}}}", font_size=28, color=C.INNER),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([-3.3, -1.9, 0]))
        side = VGroup(
            label(r"$e_n \to 0$ \emph{weakly}, \ never in norm", font_size=26, color=C.EPS),
            label(r"Baire's theorem and its three children", font_size=26),
            label(r"Hahn--Banach: \ enough functionals to see everything", font_size=26),
            label(r"weak topologies, \ where the unit ball is compact again", font_size=26, color=C.INNER),
            label(r"and the dual of $L^\infty$, \ which chapter 12 promised", font_size=24, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([3.4, -0.4, 0])
        with self.voiceover(
            "Next time, in Part 8: general Banach spaces. <bookmark mark='a'/> Watch the unit vectors slide off to "
            "the right. Each has length one, so they never converge in norm; but against any fixed vector, their "
            "inner products go to zero. <bookmark mark='b'/> That's weak convergence, and Part 8 builds the "
            "topology where the unit ball becomes compact again, along with Baire's theorem and the Hahn-Banach "
            "theorem."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(ydots), FadeIn(y_l), FadeIn(eb), FadeIn(rd))
            vo.wait_until("a")
            self.play(nT.animate.set_value(12), run_time=5.0, rate_func=linear)
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.1) for r_ in side[1:]], lag_ratio=0.4), run_time=3.0)
        for m in (eb, rd):
            m.clear_updaters()
        self.wait(0.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def credits(self):
        lines = VGroup(
            label(r"Following W.~Rudin, \textit{Real and Complex Analysis}, 3rd ed.\ (1987), the prologue and chapters "
                  r"10--14, \ with tours of 11, 15--17, 19, 20", font_size=22),
            label(r"A.-L.~Cauchy (1825), \ B.~Riemann (1851), \ K.~Weierstrass, \ \'E.~Goursat (1900), \ C.~Runge (1885), "
                  r"\ P.~Montel (1907)", font_size=22, color=GREY_A),
            label(r"H.~A.~Schwarz, \ E.~B.~Christoffel, \ L.~Fej\'er and F.~Riesz (1922), \ A.~Beurling (1949), "
                  r"\ S.~Kakutani (1944)", font_size=22, color=GREY_A),
            label(r"Companions: \ L.~Ahlfors, \textit{Complex Analysis}; \ T.~Needham, \textit{Visual Complex Analysis}; "
                  r"\ E.~Wegert, \textit{Visual Complex Functions}", font_size=22, color=GREY_A),
            label(r"Every number on screen is computed and checked; \ the pictures marked schematic are the exceptions.",
                  font_size=24, color=C.EPS),
            label(r"Animated with Manim Community; narrated by Kokoro-82M.", font_size=22, color=GREY_B),
        ).arrange(DOWN, buff=0.3).move_to(UP * 0.2)
        with self.voiceover(
            "This part followed chapters ten through fourteen of Rudin's Real and Complex Analysis. Thanks for "
            "watching, and see you in Part 8."
        ):
            self.play(LaggedStart(*[FadeIn(l_, shift=UP * 0.1) for l_ in lines], lag_ratio=0.25), run_time=3)
        self.wait(2.0)
        self.play(FadeOut(lines))
