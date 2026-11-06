from __future__ import annotations

from videos.philosophy.philosophy26.common import *  # noqa: F403


class EPR(VoiceoverScene):
    def construct(self):
        card = chapter_card(3, r"Einstein, \ Podolsky and Rosen", r"Is the quantum description complete?",
                            lit=(1935,), part=PART)
        with self.voiceover("Chapter three. Einstein, Podolsky and Rosen."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.criterion()
        self.spins()
        self.argument()

    def criterion(self):
        q = quote_card(r"If, \ without in any way disturbing a system, \ we can predict with certainty \dots\ the value "
                       r"of a physical quantity, \ then there exists an element of physical reality corresponding to "
                       r"this physical quantity.", r"Einstein, \ Podolsky and Rosen",
                       r"`Can Quantum-Mechanical Description of Physical Reality Be Considered Complete?' \ (1935)",
                       width=11.0, font_size=24).to_edge(UP, buff=0.5)
        rows = stack([(r"the criterion of reality: \ sufficient, \ not necessary", ABS),
                      (r"locality: \ what is done here cannot disturb what is there, \ instantly", CLASS),
                      (r"completeness: \ every element of reality has a counterpart in the theory", WAVE)],
                     font_size=22, aligned_edge=LEFT, width=11.0, buff=0.3).move_to([0, -1.3, 0])
        with self.voiceover(
            "In 1935 Einstein, Boris Podolsky and Nathan Rosen asked whether the quantum description is complete. "
            "<bookmark mark='a'/>Their argument rests on a criterion: if, without in any way disturbing a system, we "
            "can predict with certainty the value of a physical quantity, then there exists an element of physical "
            "reality corresponding to it. <bookmark mark='b'/>It is offered as sufficient for reality, not "
            "necessary. <bookmark mark='c'/>Add locality: what is done here cannot instantly disturb what is far "
            "away. <bookmark mark='d'/>And define completeness: a theory is complete if every element of reality has "
            "a counterpart in it."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(q))
            for mk, r in zip("bcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def spins(self):
        head = label(r"Bohm's version", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        src = Dot([0, 0.4, 0], radius=0.15, color=WAVE)
        sl = label(r"source: \ a singlet pair", font_size=19, color=WAVE).next_to(src, DOWN, buff=0.2)
        A = RoundedRectangle(width=1.4, height=1.0, corner_radius=0.15, color=ALICE).move_to([-5.0, 0.4, 0])
        B = RoundedRectangle(width=1.4, height=1.0, corner_radius=0.15, color=BOB).move_to([5.0, 0.4, 0])
        Al = label(r"Alice", font_size=22, color=ALICE).next_to(A, DOWN, buff=0.15)
        Bl = label(r"Bob", font_size=22, color=BOB).next_to(B, DOWN, buff=0.15)
        pa = Dot(src.get_center(), radius=0.09, color=PART_C)
        pb = Dot(src.get_center(), radius=0.09, color=PART_C)
        rows = stack([(r"Alice measures spin along $z$ and gets $+$", ALICE),
                      (r"she can now predict with certainty: \ Bob's $z$ will be $-$", WHITE),
                      (r"she has not touched Bob's particle: \ by locality, \ it already had $z = -$", CLASS),
                      (r"she could have measured $x$ instead: \ so it already had an $x$ value too", CLASS)],
                     font_size=21, aligned_edge=LEFT, width=11.0, buff=0.26).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "David Bohm's version uses spins. <bookmark mark='a'/>A source emits pairs of particles in the singlet "
            "state, one to Alice and one to Bob, far apart. <bookmark mark='b'/>Alice measures her particle's spin "
            "along the z axis and gets plus. <bookmark mark='c'/>She can now predict with certainty that Bob's z "
            "measurement will give minus. <bookmark mark='d'/>She did nothing to Bob's particle, so by locality its z "
            "value was an element of reality all along. <bookmark mark='e'/>But she could have measured along x "
            "instead, and then predicted Bob's x with certainty; so Bob's particle had a definite x value too."
        ) as vo:
            self.play(FadeIn(head), Create(A), Create(B), FadeIn(Al), FadeIn(Bl))
            vo.wait_until("a")
            self.play(FadeIn(src), FadeIn(sl), FadeIn(pa), FadeIn(pb))
            self.play(pa.animate.move_to(A.get_center()), pb.animate.move_to(B.get_center()), run_time=1.6)
            for mk, r in zip("bcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def argument(self):
        head = label(r"The argument", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        steps = stack([(r"1. \ Bob's particle has definite values of both $z$ and $x$ spin \ (criterion + locality)",
                        CLASS),
                       (r"2. \ no quantum state gives definite values of both: \ they do not commute", WAVE),
                       (r"3. \ so the quantum description leaves out elements of reality: \ it is incomplete", BAD),
                       (r"Bohr's reply: \ the very conditions that define the quantities are affected", HIST),
                       (r"Einstein \ (1947): \ the alternative is `spooky action at a distance'", ALICE),
                       (r"Bell \ (1964) \ turned the dispute into an experiment", GOAL)], font_size=22,
                      aligned_edge=LEFT, width=11.6, buff=0.32).move_to([0, -0.2, 0])
        with self.voiceover(
            "So the argument runs. <bookmark mark='a'/>Bob's particle has definite values of both z spin and x spin, "
            "by the criterion and locality. <bookmark mark='b'/>No quantum state gives definite values of both: the "
            "two spins do not commute. <bookmark mark='c'/>So the quantum description leaves out elements of "
            "reality; it is incomplete. <bookmark mark='d'/>Niels Bohr replied, obscurely, that Alice's choice "
            "influences the very conditions that define what can be predicted about Bob's particle. "
            "<bookmark mark='e'/>Einstein thought the only alternative to incompleteness was what he called, in a "
            "letter of 1947, spooky action at a distance. <bookmark mark='f'/>For thirty years the dispute looked "
            "like philosophy. Then John Bell turned it into an experiment."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcdef", steps):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
