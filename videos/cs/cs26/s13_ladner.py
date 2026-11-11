from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs26.common import (CTRL, DATA, HEAD, LAM, NO, PART, YES, fit_right)


class Ladner(VoiceoverScene):
    def construct(self):
        self.card()
        self.theorem()
        self.candidates()

    def card(self):
        card = chapter_card(12, r"Between P and NP-complete", r"If P $\ne$ NP, \ is every problem easy or complete?",
                            lit=(1975,), extra=((1975, r"Ladner"),), part=PART)
        with self.voiceover("Chapter twelve. Between P and NP-complete."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def theorem(self):
        head = label(r"Ladner's theorem \ (1975)", font_size=34).to_edge(UP, buff=0.35)
        np_ = Ellipse(width=6.4, height=3.8, color=HEAD).set_fill(HEAD, 0.05).shift(LEFT * 3.4 + DOWN * 0.5)
        p_ = Ellipse(width=2.0, height=1.4, color=DATA).set_fill(DATA, 0.2).move_to(np_.get_center() + LEFT * 1.7
                                                                                  + DOWN * 0.3)
        npc = Ellipse(width=2.0, height=1.4, color=NO).set_fill(NO, 0.2).move_to(np_.get_center() + RIGHT * 1.7
                                                                               + UP * 0.3)
        mid = Ellipse(width=1.6, height=1.0, color=LAM).set_fill(LAM, 0.25).move_to(np_.get_center() + DOWN * 1.0
                                                                                  + RIGHT * 0.4)
        labs = VGroup(label(r"P", font_size=22, color=DATA).move_to(p_), label(r"NP-complete", font_size=18,
                                                                              color=NO).move_to(npc),
                      label(r"NPI", font_size=20, color=LAM).move_to(mid),
                      label(r"NP \ (if P $\ne$ NP)", font_size=20, color=HEAD).next_to(np_.get_top(), DOWN, buff=0.15))
        lines = VGroup(
            label(r"if P $\ne$ NP, \ there are problems in NP \\ that are \textbf{neither} in P \textbf{nor} "
                  r"NP-complete", font_size=21, color=WHITE),
            label('proof sketch: restrict or pad SAT \\\\ at carefully selected lengths; \\\\ ordinary padding is not trivialization', font_size=21, color=DATA),
            label('choose lengths by slow diagonalization: \\\\ too many holes puts it in P; \\\\ too few can retain completeness', font_size=21, color=GREY_A),
            label(r"the construction defeats every polynomial algorithm \\ and every polynomial reduction in turn",
                  font_size=21, color=YES),
            label(r"the problem it builds is artificial: \\ the question is which \textbf{natural} problems sit there",
                  font_size=21, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(RIGHT * 3.5 + DOWN * 0.1)
        fit_right(lines)
        with self.voiceover(
            "Suppose P differs from NP. <bookmark mark='a'/> Ladner's theorem then supplies languages in NP that are neither in P nor NP-complete under polynomial-time many-one reductions. <bookmark mark='b'/> One proof uses a carefully controlled restriction or padding of satisfiability. This is a proof sketch, not a claim that ordinary padding makes SAT trivial. <bookmark mark='c'/> Delayed diagonalization chooses the growth rate slowly enough that the resulting language remains in NP. <bookmark mark='d'/> It defeats polynomial-time deciders and candidate completeness reductions in successive stages, under the assumption P differs from NP. <bookmark mark='e'/> The construction is artificial. Proving that a familiar natural candidate is intermediate remains a separate challenge."
        ) as vo:
            self.play(FadeIn(head), FadeIn(np_), FadeIn(p_), FadeIn(npc), FadeIn(labs[0]), FadeIn(labs[1]),
                      FadeIn(labs[3]))
            vo.wait_until("a")
            self.play(FadeIn(mid), FadeIn(labs[2]), FadeIn(lines[0]))
            for mk, ln in zip("bcde", lines[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def candidates(self):
        head = label(r"The suspects", font_size=34).to_edge(UP, buff=0.35)
        lines = VGroup(
            label('factoring / discrete-log decision variants: NP $\\cap$ coNP; related crypto assumptions are distinct', font_size=22, color=HEAD),
            label(r"\textbf{graph isomorphism}: \ quasi-polynomial \ (Babai, 2015); \ not NP-complete unless the "
                  r"hierarchy collapses", font_size=22, color=DATA),
            label(r"\textbf{minimum circuit size}: \ is this truth table computed by a circuit of size $s$? \ "
                  r"(chapter 16)", font_size=22, color=LAM),
            label('none is proved intermediate; each might be in P; NP-completeness has problem-specific consequences',
                  font_size=22, color=NO),
            label('Bulatov / Zhuk (2017): for each fixed finite constraint language on a finite domain, CSP is P or NP-complete', font_size=21, color=YES),
        ).arrange(DOWN, buff=0.35).next_to(head, DOWN, buff=0.55)
        with self.voiceover(
            "Several natural problems motivate the question. <bookmark mark='a'/> Suitable decision versions of factoring and discrete logarithm lie in NP intersect coNP. RSA inversion and Diffie-Hellman assumptions are related to those searches, but should not be described as proved equivalent to them. <bookmark mark='b'/> Graph isomorphism has a quasipolynomial algorithm and cannot be NP-complete under standard reductions unless the polynomial hierarchy collapses. <bookmark mark='c'/> The minimum circuit size problem is another candidate: given a full truth table, is there a small circuit computing it? <bookmark mark='d'/> None of these is proved intermediate; each might still be in P. Their possible NP-completeness has different known consequences. <bookmark mark='e'/> In contrast, Bulatov and Zhuk proved a dichotomy for each FIXED finite constraint language over a finite domain: its decision CSP is in P or NP-complete. The fixed-template condition matters."
        ) as vo:
            self.play(FadeIn(head))
            for mk, ln in zip("abcde", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
