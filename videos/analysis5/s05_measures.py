from __future__ import annotations

from fractions import Fraction

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis5.common import plain_axes


class Measures(VoiceoverScene):
    def construct(self):
        self.card()
        self.definition()
        self.continuity()
        self.almost()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(4, r"Measures", r"What rules must a length obey?", lit=(), part=5)
        with self.voiceover("Chapter four: measures, the abstract notion of size."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def definition(self):
        head = VGroup(label(r"\textbf{Rudin, RCA 1.18} \ a measure on $(X, \mathfrak M)$:", font_size=30),
                      MathTex(r"\mu: \mathfrak M \to [0, \infty], \qquad \mu\Big(\bigcup_k A_k\Big) = \sum_k \mu(A_k) "
                              r"\ \text{ for disjoint } A_k", font_size=34, color=C.MEASURE)
                      ).arrange(DOWN, buff=0.15).to_edge(UP, buff=0.3)
        W = 3.9
        cx = (-4.55, 0.0, 4.55)
        lines = [NumberLine(x_range=[0, 4, 1], length=W, include_numbers=False).move_to([c, -0.6, 0]) for c in cx]
        # counting measure: every point weighs 1
        pts = [0.5, 1.2, 1.9, 2.4, 3.1, 3.6]
        cnt = VGroup(*[VGroup(Dot(lines[0].n2p(p), radius=0.07, color=C.SEQ),
                              Line(lines[0].n2p(p), lines[0].n2p(p) + UP * 0.6, color=C.SEQ, stroke_width=4)) for p in pts])
        A0 = Line(lines[0].n2p(1.0), lines[0].n2p(3.3), color=C.MEASURE, stroke_width=10).shift(DOWN * 0.3)
        c0 = MathTex(r"\mu(A) = \#A = 4", font_size=28, color=C.MEASURE).next_to(lines[0], DOWN, buff=0.6)
        assert sum(1 for p in pts if 1.0 <= p <= 3.3) == 4
        # Dirac mass at a = 2
        dirac = VGroup(Dot(lines[1].n2p(2.0), radius=0.08, color=C.DISTRIBUTION),
                       Arrow(lines[1].n2p(2.0), lines[1].n2p(2.0) + UP * 1.6, buff=0, color=C.DISTRIBUTION,
                             stroke_width=5))
        A1 = Line(lines[1].n2p(1.4), lines[1].n2p(3.6), color=C.MEASURE, stroke_width=10).shift(DOWN * 0.3)
        c1 = MathTex(r"\delta_2(A) = 1 \text{ if } 2 \in A", font_size=28, color=C.MEASURE).next_to(lines[1], DOWN,
                                                                                                buff=0.6)
        # length
        A2 = Line(lines[2].n2p(0.7), lines[2].n2p(2.9), color=C.MEASURE, stroke_width=10).shift(DOWN * 0.3)
        c2 = MathTex(r"m([0.7, 2.9]) = 2.2", font_size=28, color=C.MEASURE).next_to(lines[2], DOWN, buff=0.6)
        names = VGroup(label(r"counting measure", font_size=26), label(r"a Dirac mass", font_size=26),
                       label(r"length (Lebesgue measure)", font_size=26))
        for n_, l_ in zip(names, lines):
            n_.next_to(l_, UP, buff=1.9)
        with self.voiceover(
            "<bookmark mark='a'/> A measure assigns a size, possibly infinite, to each set of a sigma-algebra, so that "
            "the size of a countable disjoint union is the sum of the sizes. <bookmark mark='b'/> Counting measure "
            "counts points. <bookmark mark='c'/> A Dirac mass puts weight one at a single point and none anywhere "
            "else. <bookmark mark='d'/> And length, Lebesgue's measure, which chapter nine builds properly."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head))
            vo.wait_until("b")
            self.play(Create(lines[0]), FadeIn(names[0]), FadeIn(cnt))
            self.play(Create(A0), FadeIn(c0))
            vo.wait_until("c")
            self.play(Create(lines[1]), FadeIn(names[1]), FadeIn(dirac))
            self.play(Create(A1), FadeIn(c1))
            vo.wait_until("d")
            self.play(Create(lines[2]), FadeIn(names[2]), Create(A2), FadeIn(c2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def continuity(self):
        nl = NumberLine(x_range=[0, 6, 1], length=11.0, include_numbers=True, font_size=22).move_to([0, 0.6, 0])
        nT = ValueTracker(1)

        def below():
            n = nT.get_value()
            return Line(nl.n2p(0), nl.n2p(1 - 1 / n), color=C.MEASURE, stroke_width=10).shift(UP * 0.35)

        bl = always_redraw(below)
        blab = always_redraw(lambda: MathTex(rf"A_n = [0, 1 - \tfrac1n]: \ m(A_n) = {1 - 1 / nT.get_value():.3f} "
                                             r"\nearrow 1", font_size=28, color=C.MEASURE).next_to(nl, UP, buff=0.75))
        mT = ValueTracker(1)
        nl2 = NumberLine(x_range=[0, 6, 1], length=11.0, include_numbers=True, font_size=22).move_to([0, -1.9, 0])

        def above():
            n = mT.get_value()
            return VGroup(Line(nl2.n2p(n), nl2.n2p(6), color=C.PATHOLOGY, stroke_width=10).shift(UP * 0.35),
                          Arrow(nl2.n2p(5.6) + UP * 0.35, nl2.n2p(6.25) + UP * 0.35, buff=0, color=C.PATHOLOGY,
                                stroke_width=6))

        ab = always_redraw(above)
        alab = always_redraw(lambda: MathTex(rf"B_n = ({mT.get_value():.1f}, \infty): \ m(B_n) = \infty, \quad "
                                             r"\bigcap B_n = \varnothing", font_size=28, color=C.PATHOLOGY)
                             .next_to(nl2, UP, buff=0.75))
        head = VGroup(label(r"\textbf{RCA 1.19} \ continuity: \ $A_n \nearrow A \Rightarrow \mu(A_n) \to \mu(A)$; \ "
                            r"$A_n \searrow A$ and $\mu(A_1) < \infty \Rightarrow \mu(A_n) \to \mu(A)$", font_size=26),
                      ).to_edge(UP, buff=0.3)
        note_ = label(r"the second needs $\mu(A_1) < \infty$: \ $\infty, \infty, \infty, \dots$ does not tend to "
                      r"$m(\varnothing) = 0$", font_size=24, color=GREY_A).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "<bookmark mark='a'/> Countable additivity makes measures continuous along monotone sequences. "
            "<bookmark mark='b'/> If sets increase to a union, their measures increase to the measure of the union: "
            "the intervals from zero to one minus one over n fill out the half-open unit interval, and their lengths "
            "climb to one. <bookmark mark='c'/> For decreasing sets you need a finite start. The rays from n to "
            "infinity shrink to the empty set, but every one of them has infinite length."
        ) as vo:
            self.play(FadeIn(head), Create(nl), Create(nl2))
            vo.wait_until("a")
            self.play(FadeIn(bl), FadeIn(blab))
            vo.wait_until("b")
            self.play(nT.animate.set_value(40), run_time=4.0, rate_func=rate_functions.ease_out_cubic)
            vo.wait_until("c")
            self.play(FadeIn(ab), FadeIn(alab))
            self.play(mT.animate.set_value(5.0), run_time=3.0, rate_func=linear)
            self.play(FadeIn(note_))
        for m in (bl, blab, ab, alab):
            m.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def almost(self):
        ax = plain_axes([0, 1, 0.25], [0, 1.15, 0.5], 9.0, 3.4).move_to([-0.9, -0.7, 0])
        zero = Line(ax.c2p(0, 0), ax.c2p(1, 0), color=C.FUNC, stroke_width=5)
        rats = sorted({Fraction(p, q) for q in range(1, 41) for p in range(q + 1)})
        dots = VGroup(*[Dot(ax.c2p(float(r), 1), radius=0.03, color=C.PATHOLOGY) for r in rats])
        tl = MathTex(r"D(x) = \begin{cases} 1 & x \in \mathbb Q \\ 0 & x \notin \mathbb Q \end{cases}", font_size=32)
        tl.next_to(ax, RIGHT, buff=0.2).shift(UP * 0.4)
        head = VGroup(label(r"\textbf{Almost everywhere} \ (RCA 1.35): \ except on a set of measure $0$", font_size=30),
                      ).to_edge(UP, buff=0.3)
        rows = VGroup(label(r"$D = 0$ except on $\mathbb Q$, \ which has measure $0$: \ $D = 0$ a.e.", font_size=26),
                      MathTex(r"\int D\,dm = \int 0\,dm = 0", font_size=34, color=C.EPS),
                      label(r"changing a function on a null set never changes its integral", font_size=24,
                            color=GREY_A)).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Sets of measure zero are invisible to integrals, which gives the phrase almost "
            "everywhere: true except on a set of measure zero. <bookmark mark='b'/> Dirichlet's function is one on "
            "the rationals, here drawn up to denominator forty, and zero elsewhere. The rationals have measure zero, "
            "so the function is zero almost everywhere, <bookmark mark='c'/> and its Lebesgue integral is simply "
            "zero. The function Riemann could not integrate is, to Lebesgue, the same as zero."
        ) as vo:
            self.play(FadeIn(head), Create(ax))
            vo.wait_until("a")
            self.play(Create(zero), FadeIn(tl))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(d_) for d_ in dots], lag_ratio=0.004), run_time=2.0)
            self.play(FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]), FadeIn(rows[2]))
        self.wait(0.4)
        self.clear_scene()
