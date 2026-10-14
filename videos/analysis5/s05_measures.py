from __future__ import annotations

from fractions import Fraction

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis5.common import dirichlet_graph, plain_axes


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
        head = VGroup(label(r"A measure on $(X, \mathfrak M)$", font_size=34),
                      MathTex(r"\mu: \mathfrak M \to [0, \infty], \qquad \mu\Big(\bigcup_k A_k\Big) = \sum_k \mu(A_k) "
                              r"\ \text{ for disjoint } A_k", r"\qquad \text{(RCA 1.18)}", font_size=32, color=C.MEASURE)
                      ).arrange(DOWN, buff=0.15).to_edge(UP, buff=0.3)
        head[1][1].set_color(GREY_B)
        # countable additivity, drawn while it is stated: three disjoint sets and their union
        al = NumberLine(x_range=[0, 6, 1], length=9.0, include_numbers=False).move_to([0, -0.4, 0])
        Ak = [(0.4, 1.4), (2.0, 2.8), (3.6, 5.3)]
        assert all(Ak[i][1] < Ak[i + 1][0] for i in range(2))  # disjoint
        ln = [b - a for a, b in Ak]
        Abars = VGroup(*[Line(al.n2p(a), al.n2p(b), color=C.MEASURE, stroke_width=10,
                              stroke_opacity=1.0 if i % 2 == 0 else 0.6).shift(UP * 0.3) for i, (a, b) in enumerate(Ak)])
        Alabs = VGroup(*[MathTex(rf"A_{i + 1}", font_size=28, color=C.MEASURE).next_to(b_, UP, buff=0.12)
                         for i, b_ in enumerate(Abars)])
        Asum = MathTex(rf"\mu(A_1 \cup A_2 \cup A_3) = {ln[0]:.1f} + {ln[1]:.1f} + {ln[2]:.1f} = {sum(ln):.1f}",
                       font_size=30, color=C.MEASURE).next_to(al, DOWN, buff=0.45)
        Apic = VGroup(al, Abars, Alabs, Asum)
        W = 3.9
        cx = (-4.55, 0.0, 4.55)
        lines = [NumberLine(x_range=[0, 4, 1], length=W, include_numbers=True, font_size=18).move_to([c, -0.6, 0])
                 for c in cx]
        # counting measure: every point weighs 1
        pts = [0.5, 1.2, 1.9, 2.4, 3.1, 3.6]
        cnt = VGroup(*[VGroup(Dot(lines[0].n2p(p), radius=0.07, color=C.SEQ),
                              Line(lines[0].n2p(p), lines[0].n2p(p) + UP * 0.6, color=C.SEQ, stroke_width=4)) for p in pts])
        A0 = Line(lines[0].n2p(1.0), lines[0].n2p(3.3), color=C.MEASURE, stroke_width=10).shift(DOWN * 0.75)
        c0 = MathTex(r"\mu(A) = \#A = 4", font_size=28, color=C.MEASURE).next_to(lines[0], DOWN, buff=0.65)
        assert sum(1 for p in pts if 1.0 <= p <= 3.3) == 4
        # Dirac mass at a = 2
        dirac = VGroup(Dot(lines[1].n2p(2.0), radius=0.08, color=C.DISTRIBUTION),
                       Arrow(lines[1].n2p(2.0), lines[1].n2p(2.0) + UP * 1.6, buff=0, color=C.DISTRIBUTION,
                             stroke_width=5))
        A1 = Line(lines[1].n2p(1.4), lines[1].n2p(3.6), color=C.MEASURE, stroke_width=10).shift(DOWN * 0.75)
        c1 = MathTex(r"\delta_2(A) = 1 \text{ if } 2 \in A", font_size=28, color=C.MEASURE).next_to(lines[1], DOWN,
                                                                                                buff=0.65)
        # length
        A2 = Line(lines[2].n2p(0.7), lines[2].n2p(2.9), color=C.MEASURE, stroke_width=10).shift(DOWN * 0.75)
        c2 = MathTex(rf"m([0.7, 2.9]) = {2.9 - 0.7:.1f}", font_size=28, color=C.MEASURE).next_to(lines[2], DOWN,
                                                                                                buff=0.65)
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
            self.play(FadeIn(head), Create(al), LaggedStart(*[Create(b_) for b_ in Abars], lag_ratio=0.3),
                      FadeIn(Alabs))
            self.play(FadeIn(Asum))
            vo.wait_until("b")
            self.play(FadeOut(Apic))
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
        # the increasing sets live in [0, 1]: their own scale, with the limit 1 marked
        nl = NumberLine(x_range=[0, 1.2, 0.25], length=11.0, include_numbers=True, font_size=18,
                        decimal_number_config={"num_decimal_places": 2}).move_to([0, 0.6, 0])
        one = Line(nl.n2p(1) + DOWN * 0.15, nl.n2p(1) + UP * 0.6, color=WHITE, stroke_width=3)
        nT = ValueTracker(1)

        def n_():  # the sets form a sequence: n steps through the integers
            return max(1, round(nT.get_value()))

        def below():
            n = n_()
            return Line(nl.n2p(0), nl.n2p(1 - 1 / n), color=C.MEASURE, stroke_width=10).shift(UP * 0.35)

        bl = always_redraw(below)
        blab = always_redraw(lambda: MathTex(rf"A_{{{n_()}}} = [0, 1 - \tfrac1{{{n_()}}}]: \ m(A_n) = {1 - 1 / n_():.3f} "
                                             r"\nearrow 1", font_size=28, color=C.MEASURE).next_to(nl, UP, buff=0.75))
        mT = ValueTracker(1)
        nl2 = NumberLine(x_range=[0, 6, 1], length=11.0, include_numbers=True, font_size=18).move_to([0, -1.9, 0])

        def above():
            n = max(1, round(mT.get_value()))
            return VGroup(Line(nl2.n2p(n), nl2.n2p(6), color=C.PATHOLOGY, stroke_width=10).shift(UP * 0.35),
                          Arrow(nl2.n2p(5.6) + UP * 0.35, nl2.n2p(6.25) + UP * 0.35, buff=0, color=C.PATHOLOGY,
                                stroke_width=6))

        ab = always_redraw(above)
        alab = always_redraw(lambda: MathTex(rf"B_{{{max(1, round(mT.get_value()))}}} = ({max(1, round(mT.get_value()))}, "
                                             r"\infty): \ m(B_n) = \infty, \quad "
                                             r"\bigcap B_n = \varnothing", font_size=28, color=C.PATHOLOGY)
                             .next_to(nl2, UP, buff=0.75))
        head = VGroup(label(r"Measures are continuous along monotone sequences", font_size=34),
                      label(r"\textbf{RCA 1.19} \ $A_n \nearrow A \Rightarrow \mu(A_n) \to \mu(A)$; \ "
                            r"$A_n \searrow A$ and $\mu(A_1) < \infty \Rightarrow \mu(A_n) \to \mu(A)$", font_size=26),
                      ).arrange(DOWN, buff=0.15).to_edge(UP, buff=0.3)
        note_ = label(r"the second needs $\mu(A_1) < \infty$: \ $\infty, \infty, \infty, \dots$ does not tend to "
                      r"$m(\varnothing) = 0$", font_size=24, color=GREY_A).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "<bookmark mark='a'/> Countable additivity makes measures continuous along monotone sequences. "
            "<bookmark mark='b'/> If sets increase to a union, their measures increase to the measure of the union: "
            "the intervals from zero to one minus one over n fill out the half-open unit interval, and their lengths "
            "climb to one. <bookmark mark='c'/> For decreasing sets you need a finite start. The rays from n to "
            "infinity shrink to the empty set, but every one of them has infinite length."
        ) as vo:
            self.play(FadeIn(head), Create(nl), Create(one))
            vo.wait_until("a")
            self.play(FadeIn(bl), FadeIn(blab))
            vo.wait_until("b")
            self.play(nT.animate.set_value(40), run_time=4.0, rate_func=rate_functions.ease_out_cubic)
            vo.wait_until("c")
            self.play(Create(nl2), FadeIn(ab), FadeIn(alab))  # the rays' line arrives with the rays
            self.play(mT.animate.set_value(5.0), run_time=3.0, rate_func=linear)
            self.play(FadeIn(note_))
        for m in (bl, blab, ab, alab):
            m.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def almost(self):
        ax = plain_axes([0, 1, 0.25], [0, 1.15, 0.5], 9.0, 3.0).move_to([-0.9, 0.25, 0])
        # D in the series' convention: a dot at height 1 over each p/q (q <= 40, as narrated), shrinking with q so the
        # rationals never fuse into a solid line at 1; the zero part a thin line
        dg = dirichlet_graph(ax, 40)
        zero, dots = dg.zero, dg.dots
        rats = sorted({Fraction(p, q) for q in range(1, 41) for p in range(q + 1)})
        assert [Fraction(p, q) for p, q in dg.fracs] == rats
        tl = MathTex(r"D(x) = \begin{cases} 1 & x \in \mathbb Q \\ 0 & x \notin \mathbb Q \end{cases}", font_size=32)
        tl.next_to(ax, RIGHT, buff=0.2).shift(UP * 0.4)
        head = VGroup(label(r"Almost everywhere: \ except on a set of measure $0$", font_size=34),
                      ).to_edge(UP, buff=0.3)
        ref = note(r"(RCA 1.35)").next_to(tl, DOWN, buff=0.25).align_to(tl, LEFT)
        rows = VGroup(label(r"$D = 0$ except on $\mathbb Q$, \ which has measure $0$: \ $D = 0$ a.e.", font_size=26),
                      MathTex(r"\int D\,dm = \int 0\,dm = 0", font_size=34, color=C.EPS),
                      label(r"changing a function on a null set never changes its integral", font_size=24,
                            color=GREY_A)).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.3)
        assert rows.get_top()[1] < ax.c2p(0, 0)[1] - 0.3
        with self.voiceover(
            "<bookmark mark='a'/> Sets of measure zero are invisible to integrals, which gives the phrase almost "
            "everywhere: true except on a set of measure zero. <bookmark mark='b'/> Dirichlet's function is one on "
            "the rationals, here drawn up to denominator forty, and zero elsewhere. The rationals have measure zero, "
            "so the function is zero almost everywhere, <bookmark mark='c'/> and its Lebesgue integral is simply "
            "zero. The function Riemann could not integrate is, to Lebesgue, the same as zero."
        ) as vo:
            self.play(FadeIn(head), Create(ax))
            vo.wait_until("a")
            self.play(Create(zero), FadeIn(tl), FadeIn(ref))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(d_) for d_ in dots], lag_ratio=0.004), run_time=2.0)
            self.play(FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]), FadeIn(rows[2]))
        self.wait(0.4)
        self.clear_scene()
