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
            label(r"proof idea: \ take SAT and \textbf{punch holes} in it: \\ pad the formulas of some lengths, \ "
                  r"keep others", font_size=21, color=DATA),
            label(r"the lengths are chosen by a slow diagonalization: \\ too many holes and it is in P; \ too few and "
                  r"it is complete", font_size=21, color=GREY_A),
            label(r"the construction defeats every polynomial algorithm \\ and every polynomial reduction in turn",
                  font_size=21, color=YES),
            label(r"the problem it builds is artificial: \\ the question is which \textbf{natural} problems sit there",
                  font_size=21, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4).shift(DOWN * 0.1)
        fit_right(lines)
        with self.voiceover(
            "Suppose P is not NP. Must every problem in NP be either easy or complete? <bookmark mark='a'/> No. "
            "Richard Ladner proved in 1975 that, if P differs from NP, there are problems in NP that are neither in "
            "P nor NP-complete. <bookmark mark='b'/> The proof takes SAT and punches holes in it: for some input "
            "lengths it keeps the formulas, for others it pads them into triviality. <bookmark mark='c'/> The "
            "lengths are chosen by a slow diagonal process. With too many holes the problem would be easy, with too "
            "few it would still be complete, <bookmark mark='d'/> and the construction steers between the two, "
            "defeating each polynomial algorithm and each polynomial reduction in turn. <bookmark mark='e'/> The "
            "problem it builds is artificial. The real question is which natural problems live in between."
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
            label(r"\textbf{factoring} \ and \textbf{discrete logarithm}: \ in NP $\cap$ coNP; \ the security of RSA "
                  r"and Diffie--Hellman \ (Part 30)", font_size=22, color=HEAD),
            label(r"\textbf{graph isomorphism}: \ quasi-polynomial \ (Babai, 2015); \ not NP-complete unless the "
                  r"hierarchy collapses", font_size=22, color=DATA),
            label(r"\textbf{minimum circuit size}: \ is this truth table computed by a circuit of size $s$? \ "
                  r"(chapter 16)", font_size=22, color=LAM),
            label(r"each could still turn out to be in P, \ or NP-complete: \ none is \textbf{proved} intermediate",
                  font_size=22, color=NO),
            label(r"and for many natural families, \ a \textbf{dichotomy}: \ every case is in P or NP-complete \ "
                  r"(constraint satisfaction: \ Bulatov; \ Zhuk, \ 2017)", font_size=21, color=YES),
        ).arrange(DOWN, buff=0.35).next_to(head, DOWN, buff=0.55)
        with self.voiceover(
            "A few natural problems are suspected to be intermediate. <bookmark mark='a'/> Factoring and the "
            "discrete logarithm: both in NP intersect coNP, and the security of RSA and Diffie-Hellman, in Part 30, "
            "rests on their being hard. <bookmark mark='b'/> Graph isomorphism, now known to be quasi-polynomial; it "
            "cannot be NP-complete unless the polynomial hierarchy collapses. <bookmark mark='c'/> And the minimum "
            "circuit size problem, which chapter sixteen returns to. <bookmark mark='d'/> None of these is proved to "
            "be intermediate. Any of them might fall into P. <bookmark mark='e'/> Meanwhile, for large natural "
            "families there is a dichotomy. Andrei Bulatov and Dmitriy Zhuk proved independently in 2017 that every "
            "constraint satisfaction problem over a finite domain is either in P or NP-complete, with nothing in "
            "between."
        ) as vo:
            self.play(FadeIn(head))
            for mk, ln in zip("abcde", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
