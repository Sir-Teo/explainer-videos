from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs26.common import (BG, CTRL, DATA, HEAD, LAM, NO, PART, YES, fit_right)


class Barriers(VoiceoverScene):
    def construct(self):
        self.card()
        self.relativize()
        self.natural()
        self.algebrize()

    def card(self):
        card = chapter_card(14, r"Why it is hard", r"Why haven't fifty years of attacks worked?", lit=(1975, 2008),
                            extra=((1975, r"Baker--Gill--Solovay"), (1994, r"natural proofs"), (2008, r"algebrization")),
                            part=PART)
        with self.voiceover("Chapter fourteen. Why it is hard."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def relativize(self):
        head = label(r"Barrier 1: \ relativization", font_size=34).to_edge(UP, buff=0.35)
        two = VGroup()
        for nm, eq, col, why in ((r"oracle $A$", r"$\mathrm{P}^A = \mathrm{NP}^A$", YES,
                                  r"$A$ = a PSPACE-complete problem: \\ both sides become PSPACE"),
                                 (r"oracle $B$", r"$\mathrm{P}^B \ne \mathrm{NP}^B$", NO,
                                  r"$B$ built by diagonalization, \\ hiding strings no fast machine can find")):
            box_ = RoundedRectangle(width=5.4, height=2.4, corner_radius=0.15, stroke_color=col, fill_color=BG,
                                    fill_opacity=1)
            t = VGroup(label(nm, font_size=22, color=GREY_A), label(eq, font_size=30, color=col),
                       label(why, font_size=19, color=WHITE)).arrange(DOWN, buff=0.2).move_to(box_)
            two.add(VGroup(box_, t))
        two.arrange(RIGHT, buff=0.6).next_to(head, DOWN, buff=0.5)
        lines = VGroup(
            label(r"Baker, \ Gill and Solovay \ (1975): \ both oracles exist", font_size=22, color=WHITE),
            label(r"diagonalization and simulation work the same with any oracle attached: \ they \textbf{relativize}",
                  font_size=22, color=DATA),
            label(r"so no such proof can settle P vs NP: \ it would have to give the same answer for $A$ and $B$",
                  font_size=22, color=NO),
            label(r"the hierarchy theorems of chapter 2 relativize: \ that is why they cannot reach NP", font_size=22,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.25).next_to(two, DOWN, buff=0.5)
        with self.voiceover(
            "There are precise reasons the problem is hard: theorems about proofs that cannot work. <bookmark "
            "mark='a'/> In 1975 Theodore Baker, John Gill and Robert Solovay gave every machine an oracle. With one "
            "oracle, a PSPACE-complete problem, P and NP become equal. <bookmark mark='b'/> With another, built by "
            "diagonalization, they are provably different. <bookmark mark='c'/> Diagonalization and simulation, the "
            "tools of Part 1 and chapter two, work exactly the same with an oracle attached: they relativize. "
            "<bookmark mark='d'/> So a proof built only from them would settle the question the same way for both "
            "oracles, which is impossible. <bookmark mark='e'/> This is why the hierarchy theorems separate P from "
            "exponential time but cannot touch NP."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(two[0]), FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(FadeIn(two[1]))
            for mk, ln in zip("cde", lines[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def natural(self):
        head = label(r"Barrier 2: \ natural proofs", font_size=34).to_edge(UP, buff=0.35)
        lines = VGroup(
            label(r"the plan of the 1980s: \ prove that SAT needs \textbf{circuits} of superpolynomial size", font_size=22,
                  color=WHITE),
            label(r"successes: \ parity is not in $\mathrm{AC}^0$ \ (Furst--Saxe--Sipser; \ Ajtai; \ Yao; \ H\aa stad); "
                  r"\ monotone circuits \ (Razborov, 1985)", font_size=21, color=YES),
            label(r"each proof finds a simple property that random functions have \ and small circuits lack",
                  font_size=22, color=DATA),
            label(r"Razborov and Rudich \ (1994): \ such a property would \textbf{distinguish} random functions from "
                  r"pseudorandom ones", font_size=22, color=HEAD),
            label(r"so if strong pseudorandom functions exist \ (Part 29's cryptography), \ no natural proof shows "
                  r"P $\ne$ NP", font_size=22, color=NO),
            label(r"the better our cryptography, \ the harder it is to prove we need it", font_size=22, color=LAM),
        ).arrange(DOWN, buff=0.3).next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "The next attack counted gates instead of steps. <bookmark mark='a'/> If SAT needed circuits of "
            "superpolynomial size, P would differ from NP. <bookmark mark='b'/> The 1980s brought real successes. "
            "Parity cannot be computed by constant-depth circuits, and Alexander Razborov proved large lower bounds "
            "for circuits without negations. <bookmark mark='c'/> Every such proof identifies a simple, checkable "
            "property that random functions have and small circuits lack. <bookmark mark='d'/> In 1994 Razborov and "
            "Steven Rudich showed that any such property could be used to tell truly random functions from "
            "pseudorandom ones. <bookmark mark='e'/> So if strong pseudorandom functions exist, which is exactly "
            "what Part 29's cryptography assumes, no natural proof can show P differs from NP. <bookmark mark='f'/> "
            "The better our cryptography, the harder it is to prove the hardness it relies on."
        ) as vo:
            self.play(FadeIn(head))
            for mk, ln in zip("abcdef", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def algebrize(self):
        head = label(r"Barrier 3: \ algebrization, \ and what is left", font_size=32).to_edge(UP, buff=0.35)
        lines = VGroup(
            label(r"the 1990s escaped relativization with \textbf{arithmetization}: \ IP = PSPACE \ (Part 27)",
                  font_size=22, color=YES),
            label(r"Aaronson and Wigderson \ (2008): \ those techniques \textbf{algebrize}, \ and algebrizing proofs "
                  r"cannot settle P vs NP either", font_size=22, color=NO),
            label(r"a proof must be non-relativizing, \ non-natural, \ and non-algebrizing at once", font_size=22,
                  color=HEAD),
            label(r"the few results that evade all three: \ Williams \ (2011), \ NEXP $\not\subseteq$ ACC$^0$, \ "
                  r"by turning \textbf{algorithms} into lower bounds", font_size=22, color=DATA),
            label(r"chapter 16 returns to where this leads", font_size=22, color=GREY_A),
        ).arrange(DOWN, buff=0.35).next_to(head, DOWN, buff=0.55)
        with self.voiceover(
            "There is a third barrier. <bookmark mark='a'/> In the 1990s, arithmetization, turning formulas into "
            "polynomials, gave results that do not relativize, such as IP equals PSPACE, which Part 27 proves. "
            "<bookmark mark='b'/> In 2008 Scott Aaronson and Avi Wigderson showed that these techniques satisfy a "
            "generalized form of relativization they called algebrization, and that algebrizing proofs cannot "
            "settle P versus NP either. <bookmark mark='c'/> A proof must avoid all three barriers at once. "
            "<bookmark mark='d'/> A few results do. Ryan Williams proved in 2011 that nondeterministic exponential "
            "time is not contained in a class of small circuits called ACC zero, by showing that faster algorithms "
            "for satisfiability of such circuits imply lower bounds against them. <bookmark mark='e'/> Chapter "
            "sixteen returns to where this leads."
        ) as vo:
            self.play(FadeIn(head))
            for mk, ln in zip("abcde", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
