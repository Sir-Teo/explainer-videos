from __future__ import annotations

from explainer.analysis import *  # noqa: F403
from explainer.analysis import TIMELINE


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.ledger_row()
        self.timeline_()
        self.beyond()
        self.credits()

    # ------------------------------------------------------------------
    def recap(self):
        items = [
            (r"Banach algebras: \ the Neumann series; \ the invertibles are open", C.OPERATOR),
            (r"the spectrum: \ compact, \ nonempty (Liouville); \ $\rho = \lim\|x^n\|^{1/n}$; \ the Volterra operator",
             C.SPECTRUM),
            (r"functions of operators by Cauchy's formula; \ spectral mapping", C.EPS),
            (r"Gelfand: \ elements become functions; \ Wiener's $1/f$ in three lines; \ $C^*$-algebras", C.FREQ),
            (r"Hilbert space: \ adjoints, \ projections, \ the numerical range", C.INNER),
            (r"compact self-adjoint: \ an eigenbasis; \ the string's sines; \ the heat equation", C.APPROX),
            (r"multiplication by $x$: \ a spectrum without eigenvectors; \ the Born rule", C.MEASURE),
            (r"the spectral theorem: \ $T = \int \lambda\, dE$, \ proved with the whole series", C.SPECTRUM),
            (r"unbounded operators: \ domains, \ a circle of self-adjoint extensions", C.PATHOLOGY),
            (r"the Cayley transform; \ momentum diagonalized by the Fourier transform", C.OPERATOR),
            (r"Stone's theorem: \ time evolution is a unitary group", C.EPS),
            (r"quantum mechanics' assumptions, \ now theorems", C.CONNECTED_SET),
        ]
        rows = VGroup(*[label(rf"{i + 1}.\; {t}", font_size=25, color=c) for i, (t, c) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.13).move_to(DOWN * 0.35)
        for r_ in rows:
            if r_.width > 13.0:
                r_.width = 13.0
        head = label(r"Part 10, in twelve lines", font_size=40).to_edge(UP, buff=0.3)
        with self.voiceover(
            "Let's take stock one last time. Banach algebras gave operators an arithmetic, with the Neumann series "
            "and an open set of invertibles. The spectrum is compact and never empty, and Gelfand's formula measures "
            "it. Cauchy's formula gave functions of operators, and Gelfand's transform turned commutative algebras "
            "into functions. In Hilbert space, compact self-adjoint operators have eigenbases, multiplication by x "
            "has none and is still diagonal, and the spectral theorem handles every normal operator, then every "
            "self-adjoint one, through the Cayley transform. Stone's theorem closed the loop with quantum mechanics."
        ) as vo:
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.5),
                      run_time=max(4.0, vo.duration - 2.0))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ledger_row(self):
        before = ledger(filled=9, highlight=10).scale(0.95)
        after = ledger(filled=10, highlight=10).scale(0.95)
        full = ledger(filled=10).scale(0.95)
        with self.voiceover(
            "The ledger's last row. <bookmark mark='a'/> The space: bounded operators, and the C-star algebras they "
            "generate. Completeness: they're closed in norm, and Gelfand-Naimark makes them function algebras. "
            "Compactness: Alaoglu again, behind the maximal ideal space. The interchange: f of T for every Borel "
            "function f, so limits of functions become limits of operators. And the Fourier answer: the Fourier "
            "transform is the spectral theorem, for momentum. <bookmark mark='b'/> And that's the whole ledger: ten "
            "rows, from the least upper bound property to the spectral theorem."
        ) as vo:
            self.play(FadeIn(before))
            vo.wait_until("a")
            self.play(LaggedStart(*[TransformFromCopy(after.rows[9][i], after.rows[9][i])
                                    for i in range(len(after.rows[9]))], lag_ratio=0.6),
                      FadeOut(before.rows[9]), run_time=6)
            vo.wait_until("b")
            self.play(FadeOut(before), FadeOut(after.rows[9]), FadeIn(full))
        self.wait(1.0)
        self.clear_scene()

    # ------------------------------------------------------------------
    def timeline_(self):
        years = [y for y, _ in TIMELINE]
        strip = timeline(lit=tuple(years), width=12.6, font_size=16).move_to(DOWN * 0.2)
        head = label(r"The Fourier thread, \ from 1807 to 1966", font_size=36).to_edge(UP, buff=0.4)
        with self.voiceover(
            "And the timeline is complete: from Fourier's claim in 1807 that every function is a sum of sines, "
            "through Dirichlet, Riemann, Cantor, Lebesgue, Fréchet, Riesz and Fischer, Banach and Schwartz, to "
            "Carleson's theorem in 1966. Every idea in the series was invented to answer a question about Fourier "
            "series."
        ) as vo:
            self.play(FadeIn(head))
            self.play(Create(strip), run_time=max(3.0, vo.duration - 2.0))
        self.wait(0.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def beyond(self):
        items = [
            (r"operator algebras: \ von Neumann algebras, \ noncommutative geometry", C.INNER),
            (r"index theory: \ Fredholm operators, \ Atiyah--Singer", C.OPERATOR),
            (r"nonlinear analysis: \ fixed points, \ variational methods, \ Sobolev spaces at work", C.APPROX),
            (r"partial differential equations: \ distributions, \ Fourier, \ and spectra, \ together", C.FREQ),
            (r"harmonic analysis: \ Carleson's theorem, \ singular integrals, \ wavelets", C.EPS),
        ]
        rows = VGroup(*[label(t, font_size=28, color=c) for t, c in items]).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        rows.move_to(DOWN * 0.2)
        head = label(r"Where the road goes next", font_size=38).to_edge(UP, buff=0.4)
        with self.voiceover(
            "From here the road divides. Operator algebras and noncommutative geometry. Index theory. Nonlinear "
            "analysis, where Sobolev spaces do their real work. Partial differential equations, which use all of it. "
            "And harmonic analysis, which is still answering Fourier's question."
        ) as vo:
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.15) for r_ in rows], lag_ratio=0.5),
                      run_time=max(3.0, vo.duration - 1.5))
        self.wait(0.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def credits(self):
        lines = VGroup(
            label(r"Following W.~Rudin, \textit{Functional Analysis}, 2nd ed.\ (1991), chapters 4 and 10--13, \ and "
                  r"\textit{Real and Complex Analysis}, chapter 18", font_size=22),
            label(r"I.~Gelfand (1941), \ M.~Naimark, \ J.~von Neumann (1929--32), \ M.~H.~Stone (1932), \ "
                  r"H.~Wielandt (1949), \ V.~Lomonosov (1973)", font_size=22, color=GREY_A),
            label(r"D.~Hilbert, \ E.~Schmidt, \ F.~Riesz, \ C.~Neumann, \ V.~Volterra, \ A.~Cayley, \ J.~Rydberg",
                  font_size=22, color=GREY_A),
            label(r"Companions: \ M.~Reed and B.~Simon, \textit{Methods of Modern Mathematical Physics I}; \ "
                  r"J.~Conway, \textit{A Course in Functional Analysis}", font_size=22, color=GREY_A),
            label(r"Toured, \ not proved: \ GNS, \ Lomonosov, \ Fuglede--Putnam, \ Hille--Yosida, \ deficiency-index "
                  r"classification", font_size=22, color=GREY_B),
            label(r"Every number on screen is computed and checked; \ the pictures marked schematic are the exceptions.",
                  font_size=24, color=C.EPS),
            label(r"Animated with Manim Community; narrated by Kokoro-82M.", font_size=22, color=GREY_B),
        ).arrange(DOWN, buff=0.28).move_to(UP * 0.1)
        for l_ in lines:
            if l_.width > 13.2:
                l_.width = 13.2
        with self.voiceover(
            "This part followed chapters ten to thirteen of Functional Analysis and chapter eighteen of Real and "
            "Complex Analysis. That's the end of the series. Thanks for watching all of it."
        ):
            self.play(LaggedStart(*[FadeIn(l_, shift=UP * 0.1) for l_ in lines], lag_ratio=0.25), run_time=3)
        self.wait(2.5)
        self.play(FadeOut(lines))
