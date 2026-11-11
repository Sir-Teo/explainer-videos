from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs25.common import (CTRL, DATA, HEAD, LAM, NO, PART, YES, mono)


class Classes(VoiceoverScene):
    def construct(self):
        self.card()
        self.defs()
        self.map_()

    def card(self):
        card = chapter_card(1, r"Decidable and recognizable", r"What does it mean to half-solve a problem?",
                            lit=(1936, 1944), extra=((1936, r"Turing; \ Church"), (1944, r"Post's r.e. sets")), part=PART)
        with self.voiceover("Chapter one. Decidable, and recognizable."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def defs(self):
        head = label(r"Three ways a machine can answer", font_size=34).to_edge(UP, buff=0.35)
        rows = VGroup(
            label(r"\textbf{decidable}: \ a machine that \textbf{always halts}, \ saying yes on members and no on the "
                  r"rest", font_size=22, color=YES),
            label('\\textbf{recognizable}: accepts every member, never a nonmember; \\ nonmembers may reject or diverge', font_size=22, color=DATA),
            label(r"\textbf{co-recognizable}: \ its complement is recognizable: \ the machine can confirm every "
                  r"\textbf{no}", font_size=22, color=LAM),
            MathTex(r"K = \{\, \langle M \rangle : M \text{ halts on its own description} \,\}", font_size=34,
                    color=HEAD),
            label(r"$K$ is recognizable: \ run $M$ on $\langle M \rangle$ and say yes if it stops \ (the universal "
                  r"machine of Part 1)", font_size=22, color=WHITE),
            label(r"$K$ is not decidable: \ Part 1's diagonal argument", font_size=22, color=NO),
        ).arrange(DOWN, buff=0.32).next_to(head, DOWN, buff=0.45)
        with self.voiceover(
            "Part 1 proved that halting is undecidable. <bookmark mark='a'/> A decider always halts and answers membership correctly. <bookmark mark='b'/> A recognizer accepts every member and never accepts a nonmember. On a nonmember it may reject or run forever. <bookmark mark='c'/> Co-recognizable means that the complement has a recognizer. <bookmark mark='d'/> K contains machine descriptions whose machines halt on their own descriptions, whether accepting or rejecting. <bookmark mark='e'/> Simulate the machine; any halt confirms membership in K. <bookmark mark='f'/> But the diagonal argument proves no decider for K exists."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r_ in zip("abcdef", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def map_(self):
        head = label(r"The map", font_size=34).to_edge(UP, buff=0.3)
        re_ = Ellipse(width=7.0, height=4.2, color=DATA).set_fill(DATA, 0.08).shift(LEFT * 1.3 + DOWN * 0.3)
        co = Ellipse(width=7.0, height=4.2, color=LAM).set_fill(LAM, 0.08).shift(RIGHT * 1.3 + DOWN * 0.3)
        rl = label(r"recognizable", font_size=22, color=DATA).move_to(re_.get_center() + LEFT * 2.0 + UP * 1.4)
        cl = label(r"co-recognizable", font_size=22, color=LAM).move_to(co.get_center() + RIGHT * 2.0 + UP * 1.4)
        dl = label(r"decidable", font_size=22, color=YES).move_to(DOWN * 0.3 + UP * 0.9)
        dots_ = VGroup(
            VGroup(Dot(LEFT * 3.3 + DOWN * 0.4, color=HEAD), mono("K, HALT", 18, HEAD).next_to(LEFT * 3.3 + DOWN * 0.4,
                                                                                               DOWN, buff=0.1)),
            VGroup(Dot(RIGHT * 3.3 + DOWN * 0.4, color=HEAD), mono("complement of K", 18, HEAD).next_to(
                RIGHT * 3.3 + DOWN * 0.4, DOWN, buff=0.1)),
            VGroup(Dot(DOWN * 0.3, color=YES), mono("primes, CFG membership", 16, YES).next_to(DOWN * 0.3, DOWN,
                                                                                               buff=0.1)),
            VGroup(Dot(RIGHT * 5.2 + UP * 1.9, color=NO), mono("TOT: halts on every input", 16, NO).next_to(
                RIGHT * 5.2 + UP * 1.9, LEFT, buff=0.15)),
        )
        thm = label('\\textbf{theorem}: decidable $=$ recognizable $\\cap$ co-recognizable \\\\ dovetail both recognizers; wait for one to ACCEPT', font_size=21,
                    color=YES).to_edge(DOWN, buff=0.35)
        cor = label(r"so the complement of $K$ is \textbf{not} recognizable: \ otherwise $K$ would be decidable",
                    font_size=21, color=NO).next_to(thm, UP, buff=0.15)
        with self.voiceover(
            "Draw the classes. <bookmark mark='a'/> Recognizable sets on the left, co-recognizable on the right. <bookmark mark='b'/> Their intersection is exactly the decidable sets. Dovetail recognizers for a language and its complement. Wait for one to ACCEPT, not merely halt. Exactly one accepts eventually, and neither gives a false acceptance. <bookmark mark='c'/> K is recognizable and undecidable, so its complement cannot be recognizable. <bookmark mark='d'/> TOT, the machines halting on every input, is neither recognizable nor co-recognizable. This forbids uniform recognizers for the two sides; it does not rule out finite proofs for particular machines."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Create(re_), Create(co), FadeIn(rl), FadeIn(cl))
            vo.wait_until("b")
            self.play(FadeIn(dl), FadeIn(dots_[2]), FadeIn(thm))
            vo.wait_until("c")
            self.play(FadeIn(dots_[0]), FadeIn(dots_[1]), FadeIn(cor))
            vo.wait_until("d")
            self.play(FadeIn(dots_[3]))
        self.wait(0.3)
        self.clear_scene()
