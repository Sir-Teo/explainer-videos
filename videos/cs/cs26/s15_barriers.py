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
            label('many standard diagonal / simulation arguments relativize; no claim about every use of these tools',
                  font_size=22, color=DATA),
            label(r"so no such proof can settle P vs NP: \ it would have to give the same answer for $A$ and $B$",
                  font_size=22, color=NO),
            label(r"the hierarchy theorems of chapter 2 relativize: \ that is why they cannot reach NP", font_size=22,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.25).next_to(two, DOWN, buff=0.5)
        with self.voiceover(
            "Some theorems constrain possible proof techniques. <bookmark mark='a'/> Baker, Gill and Solovay constructed an oracle relative to which P equals NP. A PSPACE-complete oracle makes both sides equal PSPACE. <bookmark mark='b'/> They also constructed an oracle relative to which P differs from NP. <bookmark mark='c'/> An argument that remains valid with every oracle cannot decide the unrelativized question, because it would give the same answer in these incompatible worlds. <bookmark mark='d'/> Many standard simulation and diagonal arguments relativize in this sense; this is not a claim about every possible use of those tools. <bookmark mark='e'/> Time hierarchy results survive relativization and separate appropriate time classes. They do not by themselves separate P from NP."
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
            label('natural = constructive in truth-table length + large + useful against the target circuit class',
                  font_size=22, color=DATA),
            label(r"Razborov and Rudich \ (1994): \ such a property would \textbf{distinguish} random functions from "
                  r"pseudorandom ones", font_size=22, color=HEAD),
            label('sufficiently strong pseudorandomness excludes the targeted natural circuit lower-bound proofs', font_size=22, color=NO),
            label('conditional circuit barrier; does not exclude every possible proof of P $\\ne$ NP', font_size=22, color=LAM),
        ).arrange(DOWN, buff=0.3).next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "Circuit lower bounds face another barrier. <bookmark mark='a'/> A superpolynomial circuit lower bound for SAT would imply P differs from NP, and in fact the stronger statement that NP is not contained in P over poly. <bookmark mark='b'/> Strong results exist for restricted models, including parity against constant-depth AND-OR circuits and clique against monotone circuits. <bookmark mark='c'/> A natural property is constructive in polynomial time in the FULL truth-table length, holds for a sufficiently large fraction of truth tables, and is useful against the specified small circuits. All three conditions matter. <bookmark mark='d'/> Such a test can distinguish genuinely random functions from suitably secure pseudorandom functions. <bookmark mark='e'/> Under a sufficiently strong quantitative pseudorandomness assumption, Razborov and Rudich rule out natural properties proving the targeted general circuit bounds. Ordinary one-way-function existence alone is not the stated quantitative hypothesis. <bookmark mark='f'/> This is a conditional barrier to a class of circuit arguments, not a theorem excluding every proof of P differs from NP."
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
            label('test each argument against its precise barrier; natural-proof claims are conditional and circuit-specific', font_size=22,
                  color=HEAD),
            label('Williams (2011): NEXP $\\not\\subseteq$ ACC$^0$; polynomial size, nonuniform, constant depth, fixed modular gates', font_size=22, color=DATA),
            label(r"chapter 16 returns to where this leads", font_size=22, color=GREY_A),
        ).arrange(DOWN, buff=0.35).next_to(head, DOWN, buff=0.55)
        with self.voiceover(
            "Arithmetization escapes some relativization limits. <bookmark mark='a'/> The interactive-proof results in Part 27 turn Boolean computations into low-degree polynomial questions. <bookmark mark='b'/> Aaronson and Wigderson formalized a stronger limitation called algebrization, showing that important algebraic techniques still do not settle P versus NP. <bookmark mark='c'/> A proposed argument must be assessed against the precise barrier it encounters. Calling a proof simultaneously nonrelativizing, nonnatural and nonalgebrizing is only shorthand, with the natural-proof claim conditional and circuit-specific. <bookmark mark='d'/> Williams's algorithm-to-lower-bound method proves that NEXP has no polynomial-size, nonuniform, constant-depth ACC-zero circuit family. The permitted gates and depth are part of the statement. <bookmark mark='e'/> These results supply new methods, without resolving the central P versus NP question."
        ) as vo:
            self.play(FadeIn(head))
            for mk, ln in zip("abcde", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
